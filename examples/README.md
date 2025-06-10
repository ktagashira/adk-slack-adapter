# ADK Slack Adapter Examples

This directory contains example implementations showing how to use the ADK Slack Adapter in different scenarios.

## Prerequisites

Before running any examples, make sure you have:

1. **Slack App Setup**: Create a Slack app with Socket Mode enabled
2. **Environment Variables**: Set the required environment variables
3. **Dependencies**: Install the package and dependencies

### Required Environment Variables

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
export SLACK_BOT_USER_ID="U1234567890"
```

### Optional Environment Variables

```bash
export ADK_APP_NAME="my-slack-bot"
export LOGGING_LEVEL="INFO"
```

## Examples

### 1. Basic Bot (`basic_bot.py`)

A simple example showing the minimal setup required to create a Slack bot with ADK.

**Features:**
- Basic configuration loading
- Simple agent setup
- Error handling
- Logging

**Usage:**
```bash
python examples/basic_bot.py
```

### 2. Advanced Bot (`advanced_bot.py`)

A more sophisticated example with enhanced features and production-ready patterns.

**Features:**
- Enhanced logging with file output
- Graceful shutdown handling
- Signal handling (SIGINT, SIGTERM)
- Custom configuration
- Comprehensive error handling
- Status monitoring

**Usage:**
```bash
python examples/advanced_bot.py
```

### 3. Custom Agent Bot (`custom_agent_bot.py`)

Examples of creating specialized bots with custom agent configurations.

**Included Agents:**
- **Help Desk Bot**: IT support assistant
- **Code Review Bot**: Programming assistance

**Usage:**
```bash
# Run help desk bot
python examples/custom_agent_bot.py helpdesk

# Run code review bot
python examples/custom_agent_bot.py codereview
```

## Slack App Configuration

### Required Bot Token Scopes

Your Slack app needs these OAuth scopes:

- `chat:write` - Send messages
- `channels:read` - Read channel information
- `groups:read` - Read private channel information
- `im:read` - Read direct message information
- `mpim:read` - Read multi-party direct message information

### Required Event Subscriptions

Enable these events in your Slack app:

- `message.channels` - Messages in public channels
- `message.groups` - Messages in private channels
- `message.im` - Direct messages
- `message.mpim` - Multi-party direct messages
- `app_mention` - When the bot is mentioned

### Socket Mode

Make sure Socket Mode is enabled in your Slack app settings.

## Development Tips

### 1. Testing Your Bot

Start with the basic bot example and verify:
- Bot responds to direct messages
- Bot responds to @mentions in channels
- Bot continues conversations in threads

### 2. Debugging

Enable debug logging by setting:
```bash
export LOGGING_LEVEL="DEBUG"
```

### 3. Custom Agents

When creating custom agents:
- Provide clear, specific instructions
- Define the agent's role and capabilities
- Include examples of expected behavior
- Consider the Slack context in your instructions

### 4. Error Handling

Always implement proper error handling:
- Validate configuration before starting
- Handle network interruptions gracefully
- Provide meaningful error messages
- Log errors for debugging

## Common Issues

### 1. Bot Not Responding

Check:
- Slack app has correct permissions
- Socket Mode is enabled
- Environment variables are set correctly
- Bot user ID matches your Slack app

### 2. Permission Errors

Ensure your Slack app has the required OAuth scopes and event subscriptions.

### 3. Network Issues

The adapter automatically handles connection retries, but persistent network issues may require manual intervention.

## Production Deployment

For production deployment:

1. Use the advanced bot example as a starting point
2. Implement proper logging and monitoring
3. Use environment-specific configuration
4. Set up health checks and restart policies
5. Consider using container orchestration

## Support

For questions and issues:
- Check the main README for troubleshooting
- Review the ADK documentation
- Open an issue on GitHub