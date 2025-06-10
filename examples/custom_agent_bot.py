#!/usr/bin/env python3
"""
Custom Agent Bot Example

This example shows how to create a Slack bot with a custom ADK agent
that has specific instructions and behaviors.
"""

import asyncio
import logging

from google.adk.agents import Agent

from adk_slack_adapter import AdkSlackAppRunner, AdkSlackConfig


def create_help_desk_agent() -> Agent:
    """
    Create a help desk agent that specializes in IT support.
    """
    agent = Agent(
        name="HelpDeskBot",
        instructions="""
        You are a helpful IT support assistant integrated with Slack.
        Your role is to:
        
        1. Help with common technical issues
        2. Provide troubleshooting guidance
        3. Explain technical concepts in simple terms
        4. Guide users through step-by-step solutions
        
        Guidelines:
        - Be patient and understanding
        - Ask clarifying questions when needed
        - Provide clear, actionable steps
        - Escalate complex issues when appropriate
        - Always maintain a professional tone
        
        When users ask for help, start by understanding their problem
        and then provide structured guidance.
        """,
        # Add your model configuration here
    )
    return agent


def create_code_review_agent() -> Agent:
    """
    Create a code review agent that helps with programming questions.
    """
    agent = Agent(
        name="CodeReviewBot",
        instructions="""
        You are a senior software engineer assistant integrated with Slack.
        Your expertise includes:
        
        1. Code review and best practices
        2. Debugging assistance
        3. Architecture recommendations
        4. Programming language guidance
        5. Performance optimization tips
        
        When reviewing code or answering programming questions:
        - Provide constructive feedback
        - Explain the reasoning behind suggestions
        - Offer alternative approaches when applicable
        - Include code examples when helpful
        - Consider security and performance implications
        
        Be encouraging while maintaining high code quality standards.
        """,
        # Add your model configuration here
    )
    return agent


async def run_help_desk_bot():
    """Run the help desk bot."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("HelpDeskBot")

    agent = create_help_desk_agent()
    config = AdkSlackConfig(adk_app_name="help-desk-bot")

    try:
        config.validate()
        logger.info("🎧 Help Desk Bot is starting...")

        runner = AdkSlackAppRunner(agent_instance=agent, config=config)
        await runner.start()

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")


async def run_code_review_bot():
    """Run the code review bot."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("CodeReviewBot")

    agent = create_code_review_agent()
    config = AdkSlackConfig(adk_app_name="code-review-bot")

    try:
        config.validate()
        logger.info("👨‍💻 Code Review Bot is starting...")

        runner = AdkSlackAppRunner(agent_instance=agent, config=config)
        await runner.start()

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")


async def main():
    """
    Main function - choose which bot to run.

    You can modify this to run different bots or even multiple bots
    in parallel (with different Slack apps/tokens).
    """
    import sys

    if len(sys.argv) > 1:
        bot_type = sys.argv[1]
    else:
        print("Usage: python custom_agent_bot.py [helpdesk|codereview]")
        print("Example: python custom_agent_bot.py helpdesk")
        return

    if bot_type == "helpdesk":
        await run_help_desk_bot()
    elif bot_type == "codereview":
        await run_code_review_bot()
    else:
        print(f"Unknown bot type: {bot_type}")
        print("Available types: helpdesk, codereview")


if __name__ == "__main__":
    asyncio.run(main())
