import logging
from collections.abc import Awaitable, Mapping
from typing import Any, Protocol

from slack_sdk.web.async_client import AsyncWebClient

from .interaction_flow import InteractionFlow

logger = logging.getLogger(__name__)


class SayFunction(Protocol):
    """Subset of Slack Bolt's asynchronous ``say`` callable used here."""

    def __call__(
        self, *, text: str, thread_ts: str, channel: str
    ) -> Awaitable[Any]: ...


class SlackEventProcessor:
    """
    Processes Slack events and filters relevant messages for the bot.

    This class handles the business logic for determining which Slack messages
    should be processed by the ADK agent, including direct messages, mentions,
    and thread replies.

    Attributes:
        interaction_flow: Handles message processing coordination
        bot_user_id: The bot's Slack user ID for mention detection
    """

    def __init__(
        self,
        interaction_flow: InteractionFlow,
        bot_user_id: str | None,
        allowed_channels: list[str] | None = None,
    ) -> None:
        """
        Initialize the SlackEventProcessor.

        Args:
            interaction_flow: An instance of InteractionFlow.
            bot_user_id: The Slack Bot User ID for mention detection.
            allowed_channels: List of channel IDs where bot is allowed to respond. None means all channels.
        """
        self.interaction_flow = interaction_flow
        self.bot_user_id = bot_user_id
        self.allowed_channels = allowed_channels
        if not self.bot_user_id:
            logger.warning(
                "bot_user_id is not set. Bot may respond to its own messages or handle mentions incorrectly."
            )

    async def process_message_event(
        self,
        event_data: Mapping[str, Any],
        say_fn: SayFunction,
        client: AsyncWebClient,
    ) -> None:
        """
        Process a Slack message event (direct message or app mention).

        This method analyzes incoming Slack messages to determine if they should
        be processed by the ADK agent. It handles various scenarios including
        direct messages, channel mentions, and thread conversations.

        Args:
            event_data: The event data dictionary from Slack.
            say_fn: The 'say' function provided by slack_bolt for sending messages.
            client: An instance of AsyncWebClient for making Slack API calls.
        """
        channel_type = event_data.get("channel_type")
        thread_ts = event_data.get("thread_ts")
        message_ts = event_data.get("ts")  # 'ts' is the message timestamp
        user_id = event_data.get("user")
        text = event_data.get("text", "")
        channel_id = event_data.get("channel")

        if not user_id or not channel_id or not message_ts:
            logger.warning(
                f"Missing critical event data: user_id={user_id}, channel_id={channel_id}, message_ts={message_ts}. Ignoring event."
            )
            return

        logger.info(
            f"SlackEventProcessor: Received event: channel_type={channel_type}, user_id={user_id}, ts={message_ts}, thread_ts={thread_ts}"
        )

        if self.bot_user_id and user_id == self.bot_user_id:
            logger.debug("Message from bot itself, ignoring.")
            return

        is_dm = channel_type == "im"

        # Check channel whitelist (applies to both channels and DMs when configured)
        if self.allowed_channels is not None:
            if channel_id not in self.allowed_channels:
                logger.debug(
                    f"Channel {channel_id} is not in allowed channels list. Ignoring message."
                )
                return
        current_message_has_mention = self._mentions_bot(text)
        is_thread_reply_to_bot_mention = await self._thread_root_mentions_bot(
            client=client,
            channel_id=channel_id,
            message_ts=message_ts,
            thread_ts=thread_ts,
        )

        if not (is_dm or current_message_has_mention or is_thread_reply_to_bot_mention):
            logger.debug(
                "Message is not a DM, does not mention the bot, and is not a reply in a bot-mentioned thread. Ignoring."
            )
            return

        clean_text = self._clean_message_text(text, current_message_has_mention)

        if not clean_text and not is_thread_reply_to_bot_mention:
            logger.debug(
                "Message is empty after removing mention. Replying with help or ignoring."
            )
            await say_fn(
                text="何かご用でしょうか？メッセージ内容を続けて入力してください。",
                thread_ts=thread_ts if thread_ts else message_ts,
                channel=channel_id,
            )
            return
        effective_thread_id = thread_ts if thread_ts else message_ts
        try:
            logger.info(
                f"Processing clean text: '{clean_text}' for user {user_id} in thread {effective_thread_id}"
            )
            async for response_part in self.interaction_flow.get_agent_response_stream(
                message_text=clean_text,
                user_id=user_id,
                thread_id=effective_thread_id,
            ):
                if response_part and response_part.strip():
                    await say_fn(
                        text=response_part,
                        thread_ts=effective_thread_id,
                        channel=channel_id,
                    )
        except Exception as e:
            logger.exception("Error processing message in SlackEventProcessor: %s", e)
            try:
                await say_fn(
                    text="申し訳ありません、メッセージ処理中にエラーが発生しました",
                    thread_ts=effective_thread_id,
                    channel=channel_id,
                )
            except Exception as say_e:
                logger.exception("Failed to send error message to Slack: %s", say_e)

    def _mentions_bot(self, text: str) -> bool:
        return bool(self.bot_user_id and f"<@{self.bot_user_id}>" in text)

    def _clean_message_text(self, text: str, mentions_bot: bool) -> str:
        if self.bot_user_id and mentions_bot:
            return text.replace(f"<@{self.bot_user_id}>", "").strip()
        return text.strip()

    async def _thread_root_mentions_bot(
        self,
        *,
        client: AsyncWebClient,
        channel_id: str,
        message_ts: str,
        thread_ts: str | None,
    ) -> bool:
        if not thread_ts or message_ts == thread_ts or not self.bot_user_id:
            return False

        try:
            replies_response = await client.conversations_replies(
                channel=channel_id,
                ts=thread_ts,
                limit=1,
            )
            messages = replies_response.get("messages")
            if not isinstance(messages, list) or not messages:
                return False
            root_message = messages[0]
            if not isinstance(root_message, Mapping):
                return False
            root_mentions_bot = self._mentions_bot(root_message.get("text", ""))
            if root_mentions_bot:
                logger.debug(
                    "Message is a reply in a thread where bot was mentioned. "
                    "Thread ts: %s",
                    thread_ts,
                )
            return root_mentions_bot
        except Exception:
            logger.exception("Error fetching thread replies for ts %s", thread_ts)
            return False
