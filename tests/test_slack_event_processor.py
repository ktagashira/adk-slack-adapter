"""Tests for SlackEventProcessor."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from adk_slack_adapter.features.interaction_flow import InteractionFlow
from adk_slack_adapter.features.slack_event_processor import SlackEventProcessor


class TestSlackEventProcessor:
    """Test cases for SlackEventProcessor."""

    @pytest.fixture
    def mock_interaction_flow(self):
        """Create a mock InteractionFlow."""
        mock_flow = MagicMock(spec=InteractionFlow)
        # Mock the async generator
        async def mock_response_stream():
            yield "テスト応答です"
        mock_flow.get_agent_response_stream.return_value = mock_response_stream()
        return mock_flow

    @pytest.fixture
    def mock_say_fn(self):
        """Create a mock say function."""
        return AsyncMock()

    @pytest.fixture
    def mock_client(self):
        """Create a mock AsyncWebClient."""
        return AsyncMock()

    def test_init_with_allowed_channels(self, mock_interaction_flow):
        """Test SlackEventProcessor initialization with allowed channels."""
        allowed_channels = ["C1234567", "C2345678"]
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456",
            allowed_channels=allowed_channels
        )
        assert processor.allowed_channels == allowed_channels

    def test_init_without_allowed_channels(self, mock_interaction_flow):
        """Test SlackEventProcessor initialization without allowed channels (all channels allowed)."""
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456"
        )
        assert processor.allowed_channels is None

    @pytest.mark.asyncio
    async def test_process_message_in_allowed_channel(
        self, mock_interaction_flow, mock_say_fn, mock_client
    ):
        """Test that messages in allowed channels are processed."""
        allowed_channels = ["C1234567", "C2345678"]
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456",
            allowed_channels=allowed_channels
        )

        event_data = {
            "channel_type": "channel",
            "channel": "C1234567",  # Allowed channel
            "user": "U999999",
            "text": "<@U123456> こんにちは",
            "ts": "1234567890.123"
        }

        await processor.process_message_event(event_data, mock_say_fn, mock_client)

        # Verify that the interaction flow was called
        mock_interaction_flow.get_agent_response_stream.assert_called_once()
        # Verify that say function was called
        mock_say_fn.assert_called()

    @pytest.mark.asyncio
    async def test_process_message_in_disallowed_channel(
        self, mock_interaction_flow, mock_say_fn, mock_client
    ):
        """Test that messages in disallowed channels are ignored."""
        allowed_channels = ["C1234567", "C2345678"]
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456",
            allowed_channels=allowed_channels
        )

        event_data = {
            "channel_type": "channel",
            "channel": "C9999999",  # Not in allowed channels
            "user": "U999999",
            "text": "<@U123456> こんにちは",
            "ts": "1234567890.123"
        }

        await processor.process_message_event(event_data, mock_say_fn, mock_client)

        # Verify that the interaction flow was NOT called
        mock_interaction_flow.get_agent_response_stream.assert_not_called()
        # Verify that say function was NOT called
        mock_say_fn.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_message_when_no_whitelist_configured(
        self, mock_interaction_flow, mock_say_fn, mock_client
    ):
        """Test that all channels are allowed when no whitelist is configured."""
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456",
            allowed_channels=None  # No whitelist
        )

        event_data = {
            "channel_type": "channel",
            "channel": "C9999999",  # Any channel should work
            "user": "U999999",
            "text": "<@U123456> こんにちは",
            "ts": "1234567890.123"
        }

        await processor.process_message_event(event_data, mock_say_fn, mock_client)

        # Verify that the interaction flow was called
        mock_interaction_flow.get_agent_response_stream.assert_called_once()
        # Verify that say function was called
        mock_say_fn.assert_called()

    @pytest.mark.asyncio
    async def test_direct_message_also_respects_whitelist(
        self, mock_interaction_flow, mock_say_fn, mock_client
    ):
        """Test that direct messages are also filtered by whitelist when configured."""
        allowed_channels = ["C1234567"]
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456",
            allowed_channels=allowed_channels
        )

        event_data = {
            "channel_type": "im",  # Direct message
            "channel": "D9999999",  # DM channel (not in whitelist)
            "user": "U999999",
            "text": "こんにちは",
            "ts": "1234567890.123"
        }

        await processor.process_message_event(event_data, mock_say_fn, mock_client)

        # Verify that the interaction flow was NOT called (DMs should respect whitelist)
        mock_interaction_flow.get_agent_response_stream.assert_not_called()
        # Verify that say function was NOT called
        mock_say_fn.assert_not_called()

    @pytest.mark.asyncio
    async def test_direct_message_in_allowed_channel(
        self, mock_interaction_flow, mock_say_fn, mock_client
    ):
        """Test that direct messages work when DM channel is in whitelist."""
        allowed_channels = ["C1234567", "D9999999"]  # Include DM channel in whitelist
        processor = SlackEventProcessor(
            interaction_flow=mock_interaction_flow,
            bot_user_id="U123456",
            allowed_channels=allowed_channels
        )

        event_data = {
            "channel_type": "im",  # Direct message
            "channel": "D9999999",  # DM channel (in whitelist)
            "user": "U999999",
            "text": "こんにちは",
            "ts": "1234567890.123"
        }

        await processor.process_message_event(event_data, mock_say_fn, mock_client)

        # Verify that the interaction flow was called
        mock_interaction_flow.get_agent_response_stream.assert_called_once()
        # Verify that say function was called
        mock_say_fn.assert_called()
