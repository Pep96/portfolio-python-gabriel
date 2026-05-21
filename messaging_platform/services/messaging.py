from datetime import UTC, datetime
from uuid import uuid4

from messaging_platform.providers.base import BaseProvider
from messaging_platform.schemas import (
    EmailMessageRequest,
    MessageListResponse,
    MessageRecord,
    MessageResponse,
    SmsMessageRequest,
    StatusWebhookRequest,
    WhatsAppMessageRequest,
)


class MessageStore:
    def __init__(self) -> None:
        self._messages: dict[str, MessageRecord] = {}

    def create_from_provider(
        self,
        *,
        channel: str,
        to: str,
        content: str,
        metadata: dict,
        provider: str,
        provider_result: dict,
        subject: str | None = None,
        template_name: str | None = None,
    ) -> MessageRecord:
        now = datetime.now(UTC)
        message_id = f"msg_{uuid4().hex[:18]}"
        record = MessageRecord(
            id=message_id,
            channel=channel,
            provider=provider,
            to=to,
            content=content,
            status=provider_result["status"],
            created_at=now,
            updated_at=now,
            metadata=metadata,
            external_id=provider_result.get("external_id"),
            subject=subject,
            template_name=template_name,
            events=[
                {
                    "type": "accepted",
                    "at": now.isoformat(),
                    "provider": provider,
                    "details": provider_result,
                }
            ],
        )
        self._messages[message_id] = record
        return record

    def get(self, message_id: str) -> MessageRecord | None:
        return self._messages.get(message_id)

    def list(self, channel: str | None = None, limit: int = 20) -> MessageListResponse:
        items = sorted(
            self._messages.values(),
            key=lambda item: item.created_at,
            reverse=True,
        )
        if channel:
            items = [item for item in items if item.channel == channel]
        sliced = items[:limit]
        return MessageListResponse(items=sliced, total=len(items))

    def apply_status_update(self, payload: StatusWebhookRequest) -> MessageRecord | None:
        record = self._messages.get(payload.message_id)
        if record is None:
            return None

        record.status = payload.status
        record.updated_at = payload.timestamp
        record.events.append(
            {
                "type": "status_update",
                "at": payload.timestamp.isoformat(),
                "provider_event_id": payload.provider_event_id,
                "details": payload.details,
                "status": payload.status,
            }
        )
        return record


class MessagingService:
    def __init__(self, provider: BaseProvider, store: MessageStore) -> None:
        self.provider = provider
        self.store = store

    def send_whatsapp(self, payload: WhatsAppMessageRequest) -> MessageResponse:
        provider_result = self.provider.send_whatsapp(payload)
        record = self.store.create_from_provider(
            channel=payload.channel,
            to=payload.to,
            content=payload.content,
            metadata=payload.metadata,
            provider=self.provider.name,
            provider_result=provider_result,
            template_name=payload.template_name,
        )
        return MessageResponse(message=record)

    def send_sms(self, payload: SmsMessageRequest) -> MessageResponse:
        provider_result = self.provider.send_sms(payload)
        record = self.store.create_from_provider(
            channel=payload.channel,
            to=payload.to,
            content=payload.content,
            metadata=payload.metadata,
            provider="mock-sms",
            provider_result=provider_result,
        )
        return MessageResponse(message=record)

    def send_email(self, payload: EmailMessageRequest) -> MessageResponse:
        provider_result = self.provider.send_email(payload)
        record = self.store.create_from_provider(
            channel=payload.channel,
            to=str(payload.to),
            content=payload.content,
            metadata=payload.metadata,
            provider="mock-email",
            provider_result=provider_result,
            subject=payload.subject,
        )
        return MessageResponse(message=record)
