import asyncio
import logging
from typing import Optional

from google.adk.agents import Agent

from .features.interaction_flow import InteractionFlow
from .features.slack_event_processor import SlackEventProcessor
from .infrastructure.adk_adapter import AdkAdapter
from .infrastructure.slack_adapter import SlackAdapter
from .infrastructure.config import AdkSlackConfig

logger = logging.getLogger(__name__)


class AdkSlackAppRunner:
    """
    Orchestrates the initialization and running of the ADK Slack Toolkit components.
    """

    def __init__(
        self,
        agent_instance: Agent,
        config: Optional[AdkSlackConfig] = None,
    ):
        """
        Initializes the AdkSlackAppRunner.

        Args:
            agent_instance: The specific ADK Agent instance to use.
            config: Optional AdkSlackConfig object. If None, configuration will be
                    loaded from environment variables by AdkSlackConfig's default behavior.
        """
        if config is None:
            self.config = AdkSlackConfig()
        else:
            self.config = config

        # Validate the configuration
        try:
            self.config.validate()
            logger.info("Configuration validated successfully.")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise  # Re-raise the error to stop initialization if config is invalid

        # Setup logging level based on config
        logging.basicConfig(level=self.config.logging_level.upper())
        logger.info(f"Logging level set to {self.config.logging_level}")

        self.agent_instance = agent_instance

        # Initialize components
        self.adk_adapter = AdkAdapter(
            agent_instance=self.agent_instance,
            adk_app_name=self.config.adk_app_name,
        )
        logger.debug("ADK Adapter initialized.")

        self.interaction_flow = InteractionFlow(adk_adapter=self.adk_adapter)
        logger.debug("Interaction Flow initialized.")

        self.slack_event_processor = SlackEventProcessor(
            interaction_flow=self.interaction_flow,
            bot_user_id=self.config.slack_bot_user_id,
        )
        logger.debug("Slack Event Processor initialized.")

        if not self.config.slack_bot_token or not self.config.slack_app_token:
            # This should ideally be caught by config.validate(), but as a safeguard:
            err_msg = "Slack Bot Token and App Token are essential for SlackAdapter."
            logger.error(err_msg)
            raise ValueError(err_msg)

        self.slack_adapter = SlackAdapter(
            event_processor=self.slack_event_processor,
            bot_token=self.config.slack_bot_token,
            app_token=self.config.slack_app_token,
        )
        logger.debug("Slack Adapter initialized.")
        logger.info("AdkSlackAppRunner initialized successfully.")

    async def start(self):
        """
        Starts the Slack adapter to begin listening for events.
        """
        logger.info("Starting AdkSlackAppRunner (Slack Adapter)...")
        try:
            await self.slack_adapter.start()
        except asyncio.CancelledError:
            logger.info(
                "AdkSlackAppRunner task was cancelled during startup or execution."
            )
        except Exception as e:
            logger.error(f"An error occurred while running the AdkSlackAppRunner: {e}")
            # Depending on the desired behavior, you might want to re-raise or handle
        finally:
            logger.info("AdkSlackAppRunner (Slack Adapter) shutting down.")
