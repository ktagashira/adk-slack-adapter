#!/usr/bin/env python3
"""
Basic ADK Slack Bot Example

This example demonstrates how to create a simple Slack bot using ADK Slack Adapter.
The bot will respond to direct messages and mentions in channels.
"""

import asyncio
import logging

from google.adk.agents import Agent

from adk_slack_adapter import AdkSlackAppRunner, AdkSlackConfig


def create_simple_agent() -> Agent:
    """
    Create a simple ADK agent for demonstration.

    Replace this with your actual ADK agent configuration.
    """
    # Example agent configuration - replace with your actual agent setup
    agent = Agent(
        name="SimpleSlackBot",
        instructions="You are a helpful assistant that responds to Slack messages. Be friendly and concise.",
        # Add your model and other agent configurations here
    )
    return agent


async def main():
    """Main function to start the Slack bot."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Create your ADK agent
    logger.info("Creating ADK agent...")
    agent = create_simple_agent()

    # Create configuration (loads from environment variables)
    config = AdkSlackConfig()

    # Validate configuration
    try:
        config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set the required environment variables:")
        logger.error("- SLACK_BOT_TOKEN: Your Slack bot token (xoxb-...)")
        logger.error("- SLACK_APP_TOKEN: Your Slack app token (xapp-...)")
        logger.error("- SLACK_BOT_USER_ID: Your bot's user ID")
        return

    # Create and start the Slack adapter
    logger.info("Starting ADK Slack Bot...")
    runner = AdkSlackAppRunner(agent_instance=agent, config=config)

    try:
        await runner.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")


if __name__ == "__main__":
    asyncio.run(main())
