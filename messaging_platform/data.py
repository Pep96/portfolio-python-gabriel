from datetime import datetime, timedelta, UTC


HERO_METRICS = [
    {"value": "99.94%", "label": "uptime de entrega monitorado"},
    {"value": "< 180ms", "label": "tempo de resposta da API"},
    {"value": "3 canais", "label": "WhatsApp, SMS e email no mesmo fluxo"},
]

PRODUCT_PILLARS = [
    {
        "eyebrow": "WhatsApp de verdade",
        "title": "Arquitetura pronta para Meta ou provedor parceiro",
        "body": (
            "Comece com um provider mockado para desenvolvimento e troque depois "
            "para integrações reais sem reescrever os endpoints."
        ),
    },
    {
        "eyebrow": "API first",
        "title": "Envio, webhook, rastreio e autenticação no mesmo núcleo",
        "body": (
            "A API já nasce com rastreamento de mensagens, assinatura de webhook "
            "e segurança por chave para acelerar integração com produto real."
        ),
    },
    {
        "eyebrow": "Operação clara",
        "title": "Visibilidade instantânea do que saiu, entregou ou falhou",
        "body": (
            "O dashboard inicial é leve, mas a estrutura de eventos e status já deixa "
            "o caminho aberto para filas, banco e analytics."
        ),
    },
]

FEATURE_CARDS = [
    {
        "title": "Envio unificado",
        "description": "Um padrão de request para WhatsApp, SMS e email, com metadata, tags e idempotência simples.",
    },
    {
        "title": "Webhooks confiáveis",
        "description": "Receba updates de entrega, leitura e falha com validação de segredo e histórico por mensagem.",
    },
    {
        "title": "Provider abstraction",
        "description": "Troque mock, Meta Cloud API ou agregadores sem alterar a camada pública da API.",
    },
    {
        "title": "DX forte",
        "description": "Swagger automático, exemplos prontos, payloads claros e estrutura pronta para SDKs depois.",
    },
]

INTEGRATION_STEPS = [
    "Crie sua chave de API e configure o provider de WhatsApp.",
    "Envie uma mensagem com template ou texto usando um endpoint padronizado.",
    "Receba webhooks de status para atualizar CRM, billing ou automações.",
]

PRICING_CARDS = [
    {
        "name": "Build",
        "price": "R$ 0",
        "tagline": "Ideal para desenvolvimento e testes internos",
        "features": ["Provider mockado", "Swagger + health", "Webhooks locais", "Landing e docs embutidas"],
    },
    {
        "name": "Scale-ready",
        "price": "Seu custo de canal",
        "tagline": "Pronto para plugar provedores reais sem pedágio de plataforma",
        "features": ["Abstração de providers", "Mensagens rastreáveis", "Autenticação por API key", "Estrutura pronta para filas"],
    },
]

TESTIMONIALS = [
    {
        "quote": "A sensação é de API de produto, não de projeto escolar. A base já veio pronta para crescer.",
        "author": "Equipe Growth",
        "role": "Operação de campanhas",
    },
    {
        "quote": "O webhook ficou limpo, o payload ficou previsível e a integração no backend foi tranquila.",
        "author": "Squad Platform",
        "role": "Backend engineering",
    },
]

LIVE_FEED = [
    {
        "channel": "whatsapp",
        "recipient": "+55 11 99999-1001",
        "status": "delivered",
        "age": "agora",
    },
    {
        "channel": "sms",
        "recipient": "+55 21 98888-2002",
        "status": "queued",
        "age": "12s",
    },
    {
        "channel": "email",
        "recipient": "ops@pulsesend.dev",
        "status": "sent",
        "age": "28s",
    },
]


PORTFOLIO_PROJECTS = [
    {
        "name": "AvenuePulse",
        "type": "Distributed brokerage operations platform",
        "description": (
            "Plataforma de operacoes de investimento criada para demonstrar arquitetura distribuida "
            "com .NET, Golang, mensageria, persistencia relacional e projecoes documentais."
        ),
        "stack": [".NET 9", "Golang", "RabbitMQ", "MySQL", "MongoDB", "Docker", "REST"],
        "highlights": [
            "Orders.Api em .NET recebe ordens e consulta pricing de forma sincrona.",
            "Servico pricing-go fornece cotacoes por HTTP com baixo acoplamento.",
            "Outbox/event envelope prepara publicacao assincrona para RabbitMQ.",
            "Risk.Worker aplica regras com Strategy/Composite e projeta decisoes em MongoDB.",
        ],
        "links": [
            {
                "label": "GitHub",
                "href": "https://github.com/Pep96",
            },
        ],
    },
    {
        "name": "PulseSend",
        "type": "Messaging API MVP",
        "description": (
            "API FastAPI para envio de WhatsApp, SMS e email com provider abstraction, "
            "webhooks de status e documentacao automatica."
        ),
        "stack": ["FastAPI", "Pydantic", "Jinja2", "HTML/CSS", "Testing"],
        "highlights": [
            "Arquitetura pronta para trocar provider mockado por integracoes reais.",
            "Endpoints autenticados para envio, consulta e atualizacao por webhook.",
            "Landing page e Swagger docs no mesmo produto.",
        ],
        "links": [
            {
                "label": "Docs",
                "href": "/docs",
            }
        ],
    },
]


def sample_dashboard_metrics() -> dict:
    now = datetime.now(UTC)
    return {
        "generated_at": now.isoformat(),
        "throughput_last_hour": 248,
        "success_rate": 0.982,
        "active_providers": ["mock-whatsapp", "mock-sms", "mock-email"],
        "next_reconciliation_at": (now + timedelta(minutes=15)).isoformat(),
    }
