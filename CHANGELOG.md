# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-10

### Added
- Initial release of ADK Slack Adapter
- Support for Google Agent Development Kit (ADK) integration with Slack
- Socket Mode connection for real-time message processing
- Session management per user and thread
- Streaming responses from ADK agents to Slack
- Environment-based configuration with validation
- Smart event filtering for direct messages, mentions, and thread replies
- Comprehensive documentation and examples
- Unit tests for core components
- Type hints throughout the codebase

### Features
- **Real-time Communication**: Uses Slack Socket Mode for instant message processing
- **Thread-aware Conversations**: Maintains conversation context within Slack threads
- **Session Management**: Automatic session handling per user and thread
- **Streaming Responses**: Real-time streaming of agent responses to Slack
- **Flexible Configuration**: Environment-based configuration with validation
- **Event Filtering**: Smart handling of direct messages, mentions, and thread replies

### Architecture
- Layered architecture with clear separation of concerns
- Infrastructure layer for adapters and configuration
- Features layer for business logic and message processing
- Comprehensive error handling and logging

[Unreleased]: https://github.com/ktagashira/adk-slack-adapter/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ktagashira/adk-slack-adapter/releases/tag/v0.1.0