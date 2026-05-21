from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


ChannelType = Literal["whatsapp", "sms", "email"]
MessageStatus = Literal["queued", "sent", "delivered", "read", "failed"]


class MessageBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    channel: ChannelType
    content: str = Field(min_length=1, max_length=4096)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WhatsAppMessageRequest(MessageBase):
    channel: Literal["whatsapp"] = "whatsapp"
    to: str = Field(min_length=8, max_length=24)
    template_name: str | None = None


class SmsMessageRequest(MessageBase):
    channel: Literal["sms"] = "sms"
    to: str = Field(min_length=8, max_length=24)


class EmailMessageRequest(MessageBase):
    channel: Literal["email"] = "email"
    to: EmailStr
    subject: str = Field(min_length=1, max_length=180)


class MessageRecord(BaseModel):
    id: str
    channel: ChannelType
    provider: str
    to: str
    content: str
    status: MessageStatus
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)
    external_id: str | None = None
    subject: str | None = None
    template_name: str | None = None
    events: list[dict[str, Any]] = Field(default_factory=list)


class MessageResponse(BaseModel):
    message: MessageRecord


class ProviderInfo(BaseModel):
    name: str
    channel: ChannelType
    capabilities: list[str]
    mode: Literal["mock", "external-ready"]


class ProvidersResponse(BaseModel):
    providers: list[ProviderInfo]


class HealthResponse(BaseModel):
    status: str
    environment: str
    app_name: str
    version: str


class StatusWebhookRequest(BaseModel):
    message_id: str
    status: MessageStatus
    provider_event_id: str | None = None
    timestamp: datetime
    details: dict[str, Any] = Field(default_factory=dict)


class MessageListResponse(BaseModel):
    items: list[MessageRecord]
    total: int


class DashboardMetricsResponse(BaseModel):
    generated_at: datetime
    throughput_last_hour: int
    success_rate: float
    active_providers: list[str]
    next_reconciliation_at: datetime
