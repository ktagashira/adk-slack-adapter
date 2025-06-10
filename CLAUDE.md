# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `adk-slack-adapter`, a Python library that enables integration between Google Agent Development Kit (ADK) agents and Slack. It provides a structured adapter pattern to connect ADK agents with Slack channels through Socket Mode.

## Architecture

The codebase follows a layered architecture:

- **Core Orchestrator**: `AdkSlackAppRunner` initializes and coordinates all components
- **Infrastructure Layer**: Contains adapters and configuration
  - `AdkAdapter`: Interfaces with Google ADK agents and manages sessions
  - `SlackAdapter`: Handles Slack Socket Mode connection and event routing
  - `AdkSlackConfig`: Environment-based configuration management
- **Features Layer**: Business logic for message processing
  - `SlackEventProcessor`: Processes Slack events (messages, mentions, threads)
  - `InteractionFlow`: Orchestrates message flow between Slack and ADK

## Required Environment Variables

- `SLACK_BOT_TOKEN`: Slack bot token (xoxb-...)
- `SLACK_APP_TOKEN`: Slack app token for Socket Mode (xapp-...)
- `SLACK_BOT_USER_ID`: Bot's user ID for mention detection
- `ADK_APP_NAME`: ADK application name (optional, defaults to "adk_slack_agent")
- `LOGGING_LEVEL`: Logging level (optional, defaults to "INFO")

## Key Components

### Session Management
- Sessions are created per Slack thread using format: `slack_{user_id}_{thread_id}`
- Uses ADK's `InMemorySessionService` and `InMemoryArtifactService`

### Message Processing Flow
1. SlackAdapter receives events via Socket Mode
2. SlackEventProcessor filters relevant messages (DMs, mentions, thread replies)
3. InteractionFlow coordinates with AdkAdapter
4. AdkAdapter streams responses from ADK agent
5. Responses are sent back to Slack in real-time

### Event Handling Logic
- Processes direct messages automatically
- Responds to @bot mentions in channels
- Continues conversations in threads where bot was initially mentioned
- Ignores bot's own messages to prevent loops

## Development Commands

This project uses uv for dependency management. Common commands:

```bash
# Install dependencies
uv sync

# Run with Python
uv run python -m your_script

# Add dependencies
uv add package-name
```