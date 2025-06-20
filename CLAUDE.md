# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `adk-slack-adapter`, a Python library that enables integration between Google Agent Development Kit (ADK) agents and Slack. It provides a structured adapter pattern to connect ADK agents with Slack channels through Socket Mode.

## Project Structure

```
src/adk_slack_adapter/
├── app_runner.py              # Main orchestrator class
├── infrastructure/            # Infrastructure layer
│   ├── adk_adapter.py        # ADK agent interface
│   ├── slack_adapter.py      # Slack Socket Mode interface  
│   └── config.py             # Environment configuration
└── features/                  # Business logic layer
    ├── interaction_flow.py   # Message flow orchestration
    └── slack_event_processor.py # Event filtering and processing

examples/                      # Usage examples
├── basic_bot.py              # Simple bot implementation
├── advanced_bot.py           # Advanced features demo
└── custom_agent_bot.py       # Custom agent integration

tests/                         # Test suite
├── test_app_runner.py        # Unit tests for main orchestrator
├── test_config.py            # Configuration tests
└── test_interaction_flow.py  # Flow logic tests
```

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

- `SLACK_BOT_TOKEN`: Slack bot token (xoxb-...) - Required for API access
- `SLACK_APP_TOKEN`: Slack app token for Socket Mode (xapp-...) - Required for real-time events
- `SLACK_BOT_USER_ID`: Bot's user ID for mention detection - Required for proper event filtering
- `ADK_APP_NAME`: ADK application name (optional, defaults to "adk_slack_agent")
- `LOGGING_LEVEL`: Logging level (optional, defaults to "INFO")

See `examples/.env.example` for a template with all required variables.

## Configuration Management

The `AdkSlackConfig` class handles environment variable loading and validation:
- Automatically loads from environment variables
- Provides validation for required values
- Offers sensible defaults for optional settings
- Raises clear errors for missing required configuration

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
# Install dependencies (including dev dependencies)
uv sync --extra dev

# Run with Python
uv run python -m your_script

# Add dependencies
uv add package-name

# Development tools
uv run ruff check .          # Linting
uv run black --check .       # Code formatting check
uv run isort --check-only .  # Import sorting check
uv run mypy src             # Type checking
uv run pytest              # Run tests
uv run pip-audit            # Security audit
```

## Code Quality Standards

This project enforces strict code quality standards:

- **Type Safety**: All functions must have proper type annotations (mypy compliance)
- **Code Style**: Black formatting with 88-character line length
- **Import Organization**: isort with black profile
- **Linting**: ruff with Python 3.11+ target
- **Testing**: pytest with asyncio support
- **Security**: pip-audit for dependency vulnerabilities

## Important Implementation Notes

### Async/Await Patterns
- ADK session services (`get_session`, `create_session`) are async and require `await`
- All message processing uses async generators for streaming responses
- Slack event handlers are async functions

### Type Annotations
- Use `collections.abc.AsyncGenerator` instead of `typing.AsyncGenerator` (Python 3.9+)
- Use `collections.abc.Callable` instead of `typing.Callable` (Python 3.9+)
- All parameters and return values must be properly typed

### Error Handling
- Always wrap ADK operations in try-catch blocks
- Log errors appropriately with context
- Provide user-friendly error messages in Japanese for Slack responses

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

- **Testing**: Python 3.11 and 3.12 matrix
- **Code Quality**: ruff, black, isort, mypy checks
- **Security**: pip-audit for vulnerability scanning
- **Coverage**: pytest-cov with Codecov integration

All PRs must pass CI checks before merging.