import logging

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_sdk.web.async_client import AsyncWebClient

# Config values will be passed to constructor
# from .config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_BOT_USER_ID
from adk_slack_adapter.features.slack_event_processor import SlackEventProcessor

logger = logging.getLogger(__name__)


class SlackAdapter:
    """
    Adapter for handling Slack Socket Mode connection and event routing.

    This class manages the Slack Socket Mode connection and routes incoming
    events to the appropriate processor. It handles the low-level Slack
    integration details.

    Attributes:
        app: Slack Bolt AsyncApp instance
        client: Slack Web API client
        socket_mode_handler: Handler for Socket Mode connection
        event_processor: Processor for handling Slack events
    """

    def __init__(
        self,
        event_processor: SlackEventProcessor,
        bot_token: str,
        app_token: str,
    ) -> None:
        """
        Initialize the SlackAdapter.

        Args:
            event_processor: An instance of SlackEventProcessor from the features layer.
            bot_token: The Slack Bot Token (xoxb-...).
            app_token: The Slack App Token (xapp-...) for Socket Mode.

        Raises:
            ValueError: If bot_token or app_token are not provided.
        """
        if not bot_token or not app_token:
            logger.error("Slack bot_token and app_token must be provided.")
            raise ValueError("SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set.")

        self.app = AsyncApp(token=bot_token)
        self.client = AsyncWebClient(token=bot_token)
        self.socket_mode_handler = AsyncSocketModeHandler(self.app, app_token)
        # self.bot_user_id = bot_user_id # bot_user_id is now part of SlackEventProcessor
        self.event_processor = event_processor

        self._register_event_handlers()

    def _register_event_handlers(self):
        @self.app.event("message")
        async def handle_message_wrapper(event, say, client):
            logger.debug(f"SlackAdapter received message event: {event}")
            await self.event_processor.process_message_event(
                event_data=event,
                say_fn=say,
                client=client,
            )

        @self.app.event("app_mention")
        async def handle_app_mention_wrapper(event, say, client):
            logger.debug(f"SlackAdapter received app_mention event: {event}")
            await self.event_processor.process_message_event(
                event_data=event,
                say_fn=say,
                client=client,
            )

    async def start(self) -> None:
        """Start the Socket Mode handler to begin listening for events."""
        logger.info("Starting Slack Socket Mode handler...")
        await self.socket_mode_handler.start_async()

    async def post_message(
        self, channel: str, thread_ts: str | None = None, text: str = ""
    ) -> None:
        """
        Post a message to a Slack channel or thread.

        This method can be used by the features layer if it needs to send messages
        outside the direct reply flow of an event.

        Args:
            channel: The Slack channel ID to post to
            thread_ts: Optional thread timestamp to reply in thread
            text: The message text to send
        """
        if not text or not text.strip():
            logger.debug("Attempted to send empty message. Skipping.")
            return
        try:
            await self.client.chat_postMessage(
                channel=channel, thread_ts=thread_ts, text=text
            )
            logger.debug(
                f"Message posted to channel {channel} (thread: {thread_ts}): {text}"
            )
        except Exception as e:
            logger.error(f"Error posting message to Slack: {e}")
