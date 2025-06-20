import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AdkSlackConfig:
    """
    Configuration for ADK Slack adapter.

    This class manages all configuration settings for the Slack integration,
    including Slack tokens, bot settings, and logging configuration.
    Environment variables are automatically loaded in __post_init__.

    Attributes:
        slack_bot_token: Slack bot token (xoxb-...) for API calls
        slack_app_token: Slack app token (xapp-...) for Socket Mode
        slack_bot_user_id: Bot's user ID for mention detection
        adk_app_name: Name of the ADK application
        logging_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        allowed_channels: List of channel IDs where bot is allowed to respond (None means all channels)
    """

    slack_bot_token: str | None = None
    slack_app_token: str | None = None
    slack_bot_user_id: str | None = None
    adk_app_name: str = "adk_slack_agent"
    logging_level: str = "INFO"
    allowed_channels: list[str] | None = None

    def __post_init__(self) -> None:
        if self.slack_bot_token is None:
            self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        if self.slack_app_token is None:
            self.slack_app_token = os.environ.get("SLACK_APP_TOKEN")
        if self.slack_bot_user_id is None:
            self.slack_bot_user_id = os.environ.get("SLACK_BOT_USER_ID")

        _adk_app_name_env = os.environ.get("ADK_APP_NAME")
        if _adk_app_name_env and self.adk_app_name == "adk_slack_agent":
            self.adk_app_name = _adk_app_name_env

        self.logging_level = os.environ.get("LOGGING_LEVEL", self.logging_level).upper()

        # Parse allowed channels from environment variable
        if self.allowed_channels is None:
            allowed_channels_env = os.environ.get("ALLOWED_CHANNELS")
            if allowed_channels_env:
                # Split by comma and strip whitespace
                self.allowed_channels = [
                    channel.strip()
                    for channel in allowed_channels_env.split(",")
                    if channel.strip()
                ]

    def validate(self) -> None:
        """
        Validate that essential configuration values are set.

        Raises:
            ValueError: If required configuration values are missing.
        """
        if not self.slack_bot_token:
            raise ValueError(
                "SLACK_BOT_TOKEN is not set. Provide it via constructor or environment variable."
            )
        if not self.slack_app_token:
            raise ValueError(
                "SLACK_APP_TOKEN is not set. Provide it via constructor or environment variable."
            )
        if not self.slack_bot_user_id:
            logger.warning(
                "SLACK_BOT_USER_ID is not set. This may impact bot functionality."
            )
        if not self.adk_app_name:
            raise ValueError("ADK_APP_NAME is not set.")


# Example of how to get a config instance:
# config = AdkSlackConfig()
# config.validate()
# logger.info(f"Logging level set to: {config.logging_level}")

# For direct use if not using AdkSlackAppRunner or similar orchestrator
# SLACK_BOT_TOKEN_ENV = os.environ.get("SLACK_BOT_TOKEN")
# SLACK_APP_TOKEN_ENV = os.environ.get("SLACK_APP_TOKEN")
# SLACK_BOT_USER_ID_ENV = os.environ.get("SLACK_BOT_USER_ID")
# ADK_APP_NAME_ENV = os.environ.get("ADK_APP_NAME", "adk_slack_agent")
# LOGGING_LEVEL_ENV = os.environ.get("LOGGING_LEVEL", "INFO").upper()

# def get_env_validated_config() -> AdkSlackConfig:
#     cfg = AdkSlackConfig()
#     cfg.validate()
#     return cfg
