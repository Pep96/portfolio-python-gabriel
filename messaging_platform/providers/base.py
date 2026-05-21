from abc import ABC, abstractmethod

from messaging_platform.schemas import EmailMessageRequest, SmsMessageRequest, WhatsAppMessageRequest


class ProviderResult(dict):
    """Small dict-like result for provider responses."""


class BaseProvider(ABC):
    name: str

    @abstractmethod
    def send_whatsapp(self, payload: WhatsAppMessageRequest) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def send_sms(self, payload: SmsMessageRequest) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def send_email(self, payload: EmailMessageRequest) -> ProviderResult:
        raise NotImplementedError
