from datetime import UTC, datetime
from uuid import uuid4

from messaging_platform.providers.base import BaseProvider, ProviderResult
from messaging_platform.schemas import EmailMessageRequest, SmsMessageRequest, WhatsAppMessageRequest


class MockMessagingProvider(BaseProvider):
    name = "mock-whatsapp"

    def send_whatsapp(self, payload: WhatsAppMessageRequest) -> ProviderResult:
        return ProviderResult(
            external_id=f"wa_{uuid4().hex[:14]}",
            status="queued",
            accepted_at=datetime.now(UTC).isoformat(),
            template_name=payload.template_name,
        )

    def send_sms(self, payload: SmsMessageRequest) -> ProviderResult:
        return ProviderResult(
            external_id=f"sms_{uuid4().hex[:14]}",
            status="queued",
            accepted_at=datetime.now(UTC).isoformat(),
        )

    def send_email(self, payload: EmailMessageRequest) -> ProviderResult:
        return ProviderResult(
            external_id=f"email_{uuid4().hex[:14]}",
            status="queued",
            accepted_at=datetime.now(UTC).isoformat(),
            subject=payload.subject,
        )
