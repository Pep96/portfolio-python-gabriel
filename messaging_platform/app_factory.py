from pathlib import Path
import sys

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Make data/ importable regardless of working directory
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
if str(_DATA_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_DATA_DIR.parent))

from data.profile import profile  # noqa: E402
from data.translations import get_t  # noqa: E402
from data import demos  # noqa: E402

from messaging_platform.config import settings
from messaging_platform.data import (
    FEATURE_CARDS,
    HERO_METRICS,
    INTEGRATION_STEPS,
    LIVE_FEED,
    PORTFOLIO_PROJECTS,
    PRICING_CARDS,
    PRODUCT_PILLARS,
    TESTIMONIALS,
    sample_dashboard_metrics,
)
from messaging_platform.providers.mock import MockMessagingProvider
from messaging_platform.schemas import (
    DashboardMetricsResponse,
    EmailMessageRequest,
    HealthResponse,
    MessageListResponse,
    MessageResponse,
    ProviderInfo,
    ProvidersResponse,
    StatusWebhookRequest,
    WhatsAppMessageRequest,
    SmsMessageRequest,
)
from messaging_platform.services.messaging import MessageStore, MessagingService


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
store = MessageStore()
service = MessagingService(provider=MockMessagingProvider(), store=store)


def require_api_key(x_api_key: str = Header(default="")) -> str:
    if x_api_key != settings.default_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )
    return x_api_key


def require_webhook_secret(x_webhook_secret: str = Header(default="")) -> str:
    if x_webhook_secret != settings.webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook secret.",
        )
    return x_webhook_secret


def create_app() -> FastAPI:
    app = FastAPI(
        title="PulseSend API",
        summary="Messaging API with WhatsApp-ready architecture, webhooks and premium landing page.",
        version="1.0.0",
        description=(
            "MVP de plataforma para envio de WhatsApp, SMS e email com abstração de provider, "
            "webhooks de status e frontend de marketing no mesmo projeto."
        ),
    )
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

    from fastapi.responses import RedirectResponse

    @app.get("/", response_class=RedirectResponse)
    async def home() -> RedirectResponse:
        return RedirectResponse(url="/portfolio", status_code=302)

    @app.get(f"{settings.api_prefix}/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            environment=settings.app_env,
            app_name=settings.app_name,
            version=app.version,
        )

    @app.get(f"{settings.api_prefix}/providers", response_model=ProvidersResponse)
    async def providers(_: str = Depends(require_api_key)) -> ProvidersResponse:
        return ProvidersResponse(
            providers=[
                ProviderInfo(
                    name="mock-whatsapp",
                    channel="whatsapp",
                    capabilities=["text", "template", "status-webhook"],
                    mode="mock",
                ),
                ProviderInfo(
                    name="mock-sms",
                    channel="sms",
                    capabilities=["text", "status-webhook"],
                    mode="mock",
                ),
                ProviderInfo(
                    name="mock-email",
                    channel="email",
                    capabilities=["text", "subject", "status-webhook"],
                    mode="mock",
                ),
            ]
        )

    @app.post(f"{settings.api_prefix}/messages/whatsapp/send", response_model=MessageResponse)
    async def send_whatsapp(
        payload: WhatsAppMessageRequest,
        _: str = Depends(require_api_key),
    ) -> MessageResponse:
        return service.send_whatsapp(payload)

    @app.post(f"{settings.api_prefix}/messages/sms/send", response_model=MessageResponse)
    async def send_sms(
        payload: SmsMessageRequest,
        _: str = Depends(require_api_key),
    ) -> MessageResponse:
        return service.send_sms(payload)

    @app.post(f"{settings.api_prefix}/messages/email/send", response_model=MessageResponse)
    async def send_email(
        payload: EmailMessageRequest,
        _: str = Depends(require_api_key),
    ) -> MessageResponse:
        return service.send_email(payload)

    @app.get(f"{settings.api_prefix}/messages", response_model=MessageListResponse)
    async def list_messages(
        channel: str | None = None,
        limit: int = 20,
        _: str = Depends(require_api_key),
    ) -> MessageListResponse:
        return store.list(channel=channel, limit=limit)

    @app.get(f"{settings.api_prefix}/messages/{{message_id}}", response_model=MessageResponse)
    async def get_message(message_id: str, _: str = Depends(require_api_key)) -> MessageResponse:
        message = store.get(message_id)
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found.")
        return MessageResponse(message=message)

    @app.get(f"{settings.api_prefix}/metrics", response_model=DashboardMetricsResponse)
    async def dashboard_metrics(_: str = Depends(require_api_key)) -> DashboardMetricsResponse:
        return DashboardMetricsResponse(**sample_dashboard_metrics())

    @app.post(f"{settings.api_prefix}/webhooks/whatsapp/status", response_model=MessageResponse)
    async def whatsapp_status_webhook(
        payload: StatusWebhookRequest,
        _: str = Depends(require_webhook_secret),
    ) -> MessageResponse:
        message = store.apply_status_update(payload)
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found for webhook update.")
        return MessageResponse(message=message)

    # ── Portfolio routes ──────────────────────────────────────────────────────

    @app.get("/portfolio", response_class=HTMLResponse, name="index")
    async def index(request: Request, lang: str = "pt") -> HTMLResponse:
        return templates.TemplateResponse(
            request,
            "index.html",
            {"profile": profile, "t": get_t(lang), "lang": lang},
        )

    @app.get("/portfolio/{slug}", response_class=HTMLResponse, name="project_detail")
    async def project_detail(
        request: Request, slug: str, lang: str = "pt"
    ) -> HTMLResponse:
        project = next((p for p in profile["projects"] if p["slug"] == slug), None)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found.")

        # Build demo context per project
        demo: dict = {}
        if slug == "avenue-pulse":
            scenario_key = request.query_params.get("scenario", "buy_aapl_50")
            demo = demos.get_avenue_demo(scenario_key)
        elif slug == "ai-code-review-sandbox":
            sample_key = request.query_params.get("sample", "fizzbuzz")
            demo = demos.get_code_review_demo(sample_key)
        elif slug == "python-challenge-generator":
            topic = request.query_params.get("topic", "data_structures")
            difficulty = request.query_params.get("difficulty", "junior")
            demo = demos.get_challenge_demo(topic, difficulty)
        elif slug == "remote-productivity-portal":
            status_filter = request.query_params.get("status", "all")
            demo = demos.get_portal_demo(status_filter)
        elif slug == "bug-triage-board":
            severity = request.query_params.get("severity", "all")
            demo = demos.get_triage_demo(severity)
        elif slug == "api-response-auditor":
            payload_key = request.query_params.get("payload", "user_profile")
            demo = demos.get_auditor_demo(payload_key)
        elif slug == "test-case-studio":
            scenario_key = request.query_params.get("scenario", "login")
            demo = demos.get_test_studio_demo(scenario_key)
        elif slug == "dotnet-api-monitor":
            status_filter = request.query_params.get("status", "all")
            demo = demos.get_monitor_demo(status_filter)
        elif slug == "dotnet-validation-lab":
            case_key = request.query_params.get("case", "missing_fields")
            demo = demos.get_validation_demo(case_key)

        return templates.TemplateResponse(
            request,
            "project.html",
            {"profile": profile, "project": project, "demo": demo, "t": get_t(lang), "lang": lang},
        )

    return app
