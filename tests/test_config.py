"""Tests for AdkSlackConfig."""

import os
from unittest.mock import patch

import pytest

from adk_slack_adapter.infrastructure.config import AdkSlackConfig


class TestAdkSlackConfig:
    """Test cases for AdkSlackConfig."""

    def test_default_values(self):
        """Test that default values are set correctly."""
        config = AdkSlackConfig()
        assert config.adk_app_name == "adk_slack_agent"
        assert config.logging_level == "INFO"

    def test_environment_variable_loading(self):
        """Test that environment variables are loaded correctly."""
        with patch.dict(
            os.environ,
            {
                "SLACK_BOT_TOKEN": "xoxb-test-token",
                "SLACK_APP_TOKEN": "xapp-test-token",
                "SLACK_BOT_USER_ID": "U123456",
                "ADK_APP_NAME": "test-app",
                "LOGGING_LEVEL": "DEBUG",
            },
        ):
            config = AdkSlackConfig()
            assert config.slack_bot_token == "xoxb-test-token"
            assert config.slack_app_token == "xapp-test-token"
            assert config.slack_bot_user_id == "U123456"
            assert config.adk_app_name == "test-app"
            assert config.logging_level == "DEBUG"

    def test_constructor_values_override_env(self):
        """Test that constructor values override environment variables."""
        with patch.dict(
            os.environ,
            {
                "SLACK_BOT_TOKEN": "xoxb-env-token",
                "ADK_APP_NAME": "env-app",
            },
        ):
            config = AdkSlackConfig(
                slack_bot_token="xoxb-constructor-token",
                adk_app_name="constructor-app",
            )
            assert config.slack_bot_token == "xoxb-constructor-token"
            assert config.adk_app_name == "constructor-app"

    def test_validation_success(self):
        """Test that validation passes with required values."""
        config = AdkSlackConfig(
            slack_bot_token="xoxb-test-token",
            slack_app_token="xapp-test-token",
            slack_bot_user_id="U123456",
            adk_app_name="test-app",
        )
        # Should not raise any exception
        config.validate()

    def test_validation_missing_bot_token(self):
        """Test that validation fails when bot token is missing."""
        config = AdkSlackConfig(
            slack_app_token="xapp-test-token",
            adk_app_name="test-app",
        )
        with pytest.raises(ValueError, match="SLACK_BOT_TOKEN is not set"):
            config.validate()

    def test_validation_missing_app_token(self):
        """Test that validation fails when app token is missing."""
        config = AdkSlackConfig(
            slack_bot_token="xoxb-test-token",
            adk_app_name="test-app",
        )
        with pytest.raises(ValueError, match="SLACK_APP_TOKEN is not set"):
            config.validate()

    def test_validation_missing_adk_app_name(self):
        """Test that validation fails when ADK app name is missing."""
        config = AdkSlackConfig(
            slack_bot_token="xoxb-test-token",
            slack_app_token="xapp-test-token",
            adk_app_name="",
        )
        with pytest.raises(ValueError, match="ADK_APP_NAME is not set"):
            config.validate()

    def test_validation_missing_bot_user_id_warning(self, caplog):
        """Test that validation warns when bot user ID is missing."""
        config = AdkSlackConfig(
            slack_bot_token="xoxb-test-token",
            slack_app_token="xapp-test-token",
            adk_app_name="test-app",
        )
        config.validate()
        assert "SLACK_BOT_USER_ID is not set" in caplog.text
