import logging

from adk_slack_adapter.infrastructure.adk_adapter import AdkAdapter

logger = logging.getLogger(__name__)


class InteractionFlow:
    def __init__(self, adk_adapter: AdkAdapter):
        """
        Initializes the InteractionFlow.
        Args:
            adk_adapter: An instance of AdkAdapter from the infrastructure layer.
        """
        self.adk_adapter = adk_adapter

    async def get_agent_response_stream(
        self, message_text: str, user_id: str, thread_id: str
    ):
        """
        Processes the user's message using the ADK agent and yields response parts.
        Args:
            message_text: The text of the user's message.
            user_id: The ID of the user who sent the message.
            thread_id: The Slack thread ID (or message TS if not in a thread)
                       to be used as part of the session ID suffix.
        Yields:
            str: Parts of the agent's response text.
        """
        logger.info(
            f"InteractionFlow: Processing message for user {user_id} in thread {thread_id}"
        )
        try:
            async for response_part in self.adk_adapter.query_agent_stream(
                message_text=message_text, user_id=user_id, session_id_suffix=thread_id
            ):
                if response_part:
                    yield response_part
        except Exception as e:
            logger.error(f"Error in InteractionFlow: {e}")
            yield f"申し訳ありません、処理中にエラーが発生しました: {str(e)}"
