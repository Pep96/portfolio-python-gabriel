from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "PulseSend")
    app_env: str = os.getenv("APP_ENV", "development")
    api_prefix: str = "/api/v1"
    default_api_key: str = os.getenv("API_KEY", "dev-secret-key")
    whatsapp_provider: str = os.getenv("WHATSAPP_PROVIDER", "mock-whatsapp")
    whatsapp_business_account_id: str = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "sandbox-account")
    whatsapp_phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "sandbox-phone")
    webhook_secret: str = os.getenv("WHATSAPP_WEBHOOK_SECRET", "webhook-secret")


settings = Settings()
