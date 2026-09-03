"""Contract tests for the Google ADK integration boundary."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from google.genai.types import Content, Part

from adk_slack_adapter.infrastructure.adk_adapter import AdkAdapter


@pytest.fixture
def adapter():
    """Create an adapter with isolated ADK services."""
    with (
        patch("adk_slack_adapter.infrastructure.adk_adapter.App") as app_class,
        patch("adk_slack_adapter.infrastructure.adk_adapter.Runner") as runner_class,
    ):
        session_service = Mock()
        artifact_service = Mock()
        adapter = AdkAdapter(
            agent_instance=Mock(),
            adk_app_name="test-app",
            session_service=session_service,
            artifact_service=artifact_service,
        )
        yield (
            adapter,
            session_service,
            artifact_service,
            app_class,
            runner_class,
        )


@pytest.mark.asyncio
async def test_query_agent_stream_uses_adk_v2_app_and_runner(adapter):
    """ADK v2 receives the expected app, session, and user message."""
    adapter, session_service, artifact_service, app_class, runner_class = adapter

    async def events():
        yield SimpleNamespace(
            content=Content(role="user", parts=[Part(text="ignored")])
        )
        yield SimpleNamespace(
            content=Content(
                role="model",
                parts=[Part(text="Hello"), Part(text=" "), Part(text="world")],
            )
        )

    runner_class.return_value.run_async.return_value = events()
    responses = [
        response
        async for response in adapter.query_agent_stream(
            message_text="question",
            user_id="U123",
            session_id_suffix="thread-ts",
        )
    ]

    assert responses == ["Hello", "world"]
    app_class.assert_called_once_with(name="test-app", root_agent=adapter.root_agent)
    runner_class.assert_called_once_with(
        app=app_class.return_value,
        artifact_service=artifact_service,
        session_service=session_service,
        auto_create_session=True,
    )
    runner_class.return_value.run_async.assert_called_once()
    run_arguments = runner_class.return_value.run_async.call_args.kwargs
    assert run_arguments["session_id"] == "slack_U123_thread-ts"
    assert run_arguments["user_id"] == "U123"
    new_message = runner_class.return_value.run_async.call_args.kwargs["new_message"]
    assert new_message.role == "user"
    assert new_message.parts[0].text == "question"
