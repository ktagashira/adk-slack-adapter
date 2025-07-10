# ADK Slack Adapter

A Python library for integrating Google Agent Development Kit (ADK) agents with Slack through Socket Mode. This adapter enables seamless communication between your ADK-powered AI agents and Slack workspaces.

## Features

- **Real-time Communication**: Uses Slack Socket Mode for instant message processing
- **Thread-aware Conversations**: Maintains conversation context within Slack threads
- **Session Management**: Automatic session handling per user and thread
- **Streaming Responses**: Real-time streaming of agent responses to Slack
- **Flexible Configuration**: Environment-based configuration with validation
- **Event Filtering**: Smart handling of direct messages, mentions, and thread replies

## Installation

Install from PyPI:

```bash
pip install adk-slack-adapter
```

Or with uv:

```bash
uv add adk-slack-adapter
```

## Quick Start

### 1. Setup Slack App

Create a Slack app with the following settings:

- **Socket Mode**: Enabled
- **Bot Token Scopes**: `chat:write`, `channels:read`, `groups:read`, `im:read`, `mpim:read`
- **Event Subscriptions**: `message.channels`, `message.groups`, `message.im`, `message.mpim`, `app_mention`

### 2. Environment Variables

Set the required environment variables:

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"  
export SLACK_BOT_USER_ID="U01234567"
export ADK_APP_NAME="my-adk-agent"  # optional
export LOGGING_LEVEL="INFO"  # optional
```

### 3. Basic Usage

```python
import asyncio
from google.adk.agents import Agent
from adk_slack_adapter import AdkSlackAppRunner

# Create your ADK agent
agent = Agent(
    # Your agent configuration
)

# Create and start the Slack adapter
async def main():
    runner = AdkSlackAppRunner(agent_instance=agent)
    await runner.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Advanced Configuration

```python
from adk_slack_adapter import AdkSlackAppRunner, AdkSlackConfig

# Custom configuration
config = AdkSlackConfig(
    slack_bot_token="xoxb-your-token",
    slack_app_token="xapp-your-token", 
    slack_bot_user_id="U01234567",
    adk_app_name="my-custom-agent",
    logging_level="DEBUG"
)

runner = AdkSlackAppRunner(
    agent_instance=agent,
    config=config
)
```

## How It Works

The adapter follows a layered architecture:

1. **SlackAdapter**: Handles Slack Socket Mode connection and events
2. **SlackEventProcessor**: Filters and processes relevant messages
3. **InteractionFlow**: Orchestrates message flow between Slack and ADK
4. **AdkAdapter**: Manages ADK agent sessions and streaming responses

### Message Flow

1. User sends message in Slack (DM, mention, or thread reply)
2. SlackAdapter receives event via Socket Mode
3. SlackEventProcessor filters relevant messages
4. InteractionFlow coordinates with AdkAdapter
5. AdkAdapter streams responses from ADK agent
6. Responses are sent back to Slack in real-time

### Session Management

- Sessions are created per Slack thread: `slack_{user_id}_{thread_id}`
- Uses ADK's built-in session management for conversation continuity
- Automatic cleanup and memory management

## Event Handling

The adapter intelligently handles different types of Slack events:

- **Direct Messages**: Processes all DMs automatically
- **Channel Mentions**: Responds when bot is @mentioned
- **Thread Conversations**: Continues conversations in threads where bot was initially mentioned
- **Bot Loop Prevention**: Ignores bot's own messages

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/ktagashira/adk-slack-adapter.git
cd adk-slack-adapter

# Install dependencies
uv sync

# Install development dependencies
uv sync --group dev
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Format code
uv run black .
uv run isort .

# Lint code  
uv run ruff check .

# Type checking
uv run mypy .
```

## Requirements

- Python 3.11+
- Google Agent Development Kit (ADK) 1.2.1+
- Slack Bolt SDK 1.23.0+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions and support:

- Create an issue on [GitHub](https://github.com/ktagashira/adk-slack-adapter/issues)
- Check the [documentation](https://github.com/ktagashira/adk-slack-adapter#readme)
