from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    qdrant_url: str
    qdrant_api_key: str
    anthropic_api_key: str
    collection_name: str = "rai_knowledge_base"


settings = Settings()
