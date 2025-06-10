#!/usr/bin/env python3
"""
Advanced ADK Slack Bot Example

This example demonstrates advanced usage of ADK Slack Adapter with:
- Custom configuration
- Enhanced logging
- Error handling
- Graceful shutdown
"""

import asyncio
import logging
import signal
import sys

from google.adk.agents import Agent

from adk_slack_adapter import AdkSlackAppRunner, AdkSlackConfig


class AdvancedSlackBot:
    """Advanced Slack bot with enhanced features."""

    def __init__(self):
        self.runner: AdkSlackAppRunner | None = None
        self.logger = logging.getLogger(__name__)
        self._shutdown_event = asyncio.Event()

    def create_agent(self) -> Agent:
        """
        Create an advanced ADK agent with custom configuration.

        Replace this with your actual ADK agent setup.
        """
        agent = Agent(
            name="AdvancedSlackBot",
            instructions="""
            You are an advanced AI assistant integrated with Slack.
            You can help with:
            - Answering questions
            - Providing explanations
            - Assisting with tasks
            - Code help and explanations
            Always be helpful, accurate, and professional in your responses.
            Keep responses concise but comprehensive.
            """,
            # Add your model configuration, tools, and other settings here
        )
        return agent

    def setup_logging(self) -> None:
        """Set up enhanced logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler("slack_bot.log"),
            ],
        )

        # Set specific log levels for different components
        logging.getLogger("adk_slack_adapter").setLevel(logging.INFO)
        logging.getLogger("slack_bolt").setLevel(logging.WARNING)
        logging.getLogger("aiohttp").setLevel(logging.WARNING)

    def create_config(self) -> AdkSlackConfig:
        """Create and validate configuration."""
        config = AdkSlackConfig(
            # You can override default values here
            adk_app_name="advanced-slack-bot",
            logging_level="INFO",
        )

        try:
            config.validate()
            self.logger.info("✅ Configuration validated successfully")
            self.logger.info(f"Bot User ID: {config.slack_bot_user_id}")
            self.logger.info(f"ADK App Name: {config.adk_app_name}")
            return config
        except ValueError as e:
            self.logger.error(f"❌ Configuration error: {e}")
            self.logger.error("Required environment variables:")
            self.logger.error("  SLACK_BOT_TOKEN=xoxb-your-bot-token")
            self.logger.error("  SLACK_APP_TOKEN=xapp-your-app-token")
            self.logger.error("  SLACK_BOT_USER_ID=U1234567890")
            self.logger.error("Optional environment variables:")
            self.logger.error("  ADK_APP_NAME=your-app-name")
            self.logger.error("  LOGGING_LEVEL=INFO")
            raise

    def setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""

        def signal_handler(signum, _):
            self.logger.info(
                f"Received signal {signum}, initiating graceful shutdown..."
            )
            self._shutdown_event.set()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def start(self) -> None:
        """Start the advanced Slack bot."""
        self.setup_logging()
        self.logger.info("🚀 Starting Advanced ADK Slack Bot")

        try:
            # Create agent and configuration
            self.logger.info("Creating ADK agent...")
            agent = self.create_agent()

            self.logger.info("Loading configuration...")
            config = self.create_config()

            # Set up signal handlers
            self.setup_signal_handlers()

            # Create runner
            self.logger.info("Initializing Slack adapter...")
            self.runner = AdkSlackAppRunner(agent_instance=agent, config=config)

            # Start the bot in a task so we can handle shutdown
            self.logger.info("🎯 Bot is now running and ready to respond!")
            self.logger.info("Send a direct message or mention the bot in a channel")

            bot_task = asyncio.create_task(self.runner.start())
            shutdown_task = asyncio.create_task(self._shutdown_event.wait())

            # Wait for either the bot to finish or shutdown signal
            _, pending = await asyncio.wait(
                [bot_task, shutdown_task], return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            self.logger.info("🛑 Bot stopped gracefully")

        except Exception as e:
            self.logger.error(f"❌ Error running bot: {e}", exc_info=True)
            raise

    async def stop(self) -> None:
        """Stop the bot gracefully."""
        self.logger.info("Stopping bot...")
        self._shutdown_event.set()


async def main():
    """Main function."""
    bot = AdvancedSlackBot()
    try:
        await bot.start()
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
