from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# D:\family-portfolio-intelligence
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Application configuration."""

    app_name: str = "Family Portfolio Intelligence"
    app_env: str = "development"
    debug: bool = True

    database_path: Path = Path("warehouse/portfolio.duckdb")

    data_dir: Path = Path("data")
    raw_data_dir: Path = Path("data/raw")
    bronze_data_dir: Path = Path("data/bronze")
    silver_data_dir: Path = Path("data/silver")
    gold_data_dir: Path = Path("data/gold")

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def model_post_init(self, __context: object) -> None:
        """Resolve relative paths against the project root."""
        path_fields = (
            "database_path",
            "data_dir",
            "raw_data_dir",
            "bronze_data_dir",
            "silver_data_dir",
            "gold_data_dir",
        )

        for field_name in path_fields:
            value = getattr(self, field_name)

            if not value.is_absolute():
                object.__setattr__(
                    self,
                    field_name,
                    PROJECT_ROOT / value,
                )


settings = Settings()