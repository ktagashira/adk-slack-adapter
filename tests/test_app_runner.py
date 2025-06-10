"""Tests for AdkSlackAppRunner."""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from adk_slack_adapter.app_runner import AdkSlackAppRunner
from adk_slack_adapter.infrastructure.config import AdkSlackConfig


class TestAdkSlackAppRunner:
    """Test cases for AdkSlackAppRunner."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_agent = Mock()
        self.valid_config = AdkSlackConfig(
            slack_bot_token="xoxb-test-token",
            slack_app_token="xapp-test-token",
            slack_bot_user_id="U123456",
            adk_app_name="test-app",
        )

    @patch("adk_slack_adapter.infrastructure.slack_adapter.AsyncSocketModeHandler")
    @patch("adk_slack_adapter.infrastructure.slack_adapter.AsyncApp")
    def test_init_with_valid_config(self, mock_app, mock_handler):
        """Test initialization with valid configuration."""
        runner = AdkSlackAppRunner(
            agent_instance=self.mock_agent,
            config=self.valid_config,
        )
        assert runner.agent_instance == self.mock_agent
        assert runner.config == self.valid_config

    @patch("adk_slack_adapter.infrastructure.slack_adapter.AsyncSocketModeHandler")
    @patch("adk_slack_adapter.infrastructure.slack_adapter.AsyncApp")
    def test_init_without_config_loads_from_env(self, mock_app, mock_handler):
        """Test initialization without config loads from environment."""
        with patch.dict(
            "os.environ",
            {
                "SLACK_BOT_TOKEN": "xoxb-env-token",
                "SLACK_APP_TOKEN": "xapp-env-token",
                "SLACK_BOT_USER_ID": "U654321",
            },
        ):
            runner = AdkSlackAppRunner(agent_instance=self.mock_agent)
            assert runner.config.slack_bot_token == "xoxb-env-token"
            assert runner.config.slack_app_token == "xapp-env-token"

    def test_init_with_invalid_config_raises_error(self):
        """Test initialization with invalid configuration raises error."""
        invalid_config = AdkSlackConfig()  # Missing required tokens
        with pytest.raises(ValueError):
            AdkSlackAppRunner(
                agent_instance=self.mock_agent,
                config=invalid_config,
            )

    @pytest.mark.asyncio
    async def test_start_calls_slack_adapter_start(self):
        """Test that start method calls slack adapter start."""
        with patch.object(
            AdkSlackAppRunner, "__init__", lambda x, agent_instance, config=None: None
        ):
            runner = AdkSlackAppRunner(agent_instance=self.mock_agent)
            runner.slack_adapter = Mock()
            runner.slack_adapter.start = AsyncMock()

            await runner.start()
            runner.slack_adapter.start.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_handles_cancellation(self):
        """Test that start method handles cancellation gracefully."""
        with patch.object(
            AdkSlackAppRunner, "__init__", lambda x, agent_instance, config=None: None
        ):
            runner = AdkSlackAppRunner(agent_instance=self.mock_agent)
            runner.slack_adapter = Mock()
            runner.slack_adapter.start = AsyncMock(side_effect=asyncio.CancelledError())

            # Should not raise exception
            await runner.start()
            runner.slack_adapter.start.assert_called_once()
