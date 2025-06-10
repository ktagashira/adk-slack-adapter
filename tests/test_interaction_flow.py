"""Tests for InteractionFlow."""

from unittest.mock import Mock

import pytest

from adk_slack_adapter.features.interaction_flow import InteractionFlow


class TestInteractionFlow:
    """Test cases for InteractionFlow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_adk_adapter = Mock()
        self.interaction_flow = InteractionFlow(adk_adapter=self.mock_adk_adapter)

    @pytest.mark.asyncio
    async def test_get_agent_response_stream_success(self):
        """Test successful agent response streaming."""

        # Mock the ADK adapter to return some response parts
        async def mock_stream():
            for item in ["Hello", " ", "world", "!"]:
                yield item

        self.mock_adk_adapter.query_agent_stream.return_value = mock_stream()

        responses = []
        async for response_part in self.interaction_flow.get_agent_response_stream(
            message_text="Hi there",
            user_id="U123456",
            thread_id="1234567890.123",
        ):
            responses.append(response_part)

        assert responses == ["Hello", " ", "world", "!"]
        self.mock_adk_adapter.query_agent_stream.assert_called_once_with(
            message_text="Hi there",
            user_id="U123456",
            session_id_suffix="1234567890.123",
        )

    @pytest.mark.asyncio
    async def test_get_agent_response_stream_filters_empty_responses(self):
        """Test that empty response parts are filtered out."""

        # Mock the ADK adapter to return some empty and non-empty parts
        async def mock_stream():
            for item in ["Hello", "", "world", None, "!"]:
                yield item

        self.mock_adk_adapter.query_agent_stream.return_value = mock_stream()

        responses = []
        async for response_part in self.interaction_flow.get_agent_response_stream(
            message_text="Hi there",
            user_id="U123456",
            thread_id="1234567890.123",
        ):
            responses.append(response_part)

        # Should filter out empty string and None
        assert responses == ["Hello", "world", "!"]

    @pytest.mark.asyncio
    async def test_get_agent_response_stream_handles_exception(self):
        """Test that exceptions are handled gracefully."""
        # Mock the ADK adapter to raise an exception directly
        self.mock_adk_adapter.query_agent_stream.side_effect = Exception("Test error")

        responses = []
        async for response_part in self.interaction_flow.get_agent_response_stream(
            message_text="Hi there",
            user_id="U123456",
            thread_id="1234567890.123",
        ):
            responses.append(response_part)

        # Should yield an error message
        assert len(responses) == 1
        assert "申し訳ありません、処理中にエラーが発生しました" in responses[0]
        assert "Test error" in responses[0]
