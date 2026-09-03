# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-09-04

### Changed

- Upgraded the supported Google Agent Development Kit version to 2.x.
- Reused a single ADK `App` and `Runner` across Slack messages.
- Allowed applications to inject persistent ADK session and artifact services.
- Delegated missing-session creation to `Runner(auto_create_session=True)` to
  avoid competing get-then-create operations.
- Removed Slack message content from informational logs.

### Tests

- Added ADK 2 contract tests for app and runner construction, session identity,
  user messages, and model response events.

## [0.2.2] - 2026-09-04

### Changed

- Refactored Slack event processing into focused helpers for mention handling,
  message cleanup, and thread-root detection.
- Added an explicit asynchronous protocol for Slack response callbacks.
- Improved exception logging to include tracebacks while preserving existing
  user-facing behavior.
- Updated direct and transitive dependencies to versions without known
  vulnerabilities, while keeping Google ADK on the 1.x release line.

### Tests

- Added regression coverage for incomplete events, self-authored bot messages,
  thread replies, and empty mentions.

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

[Unreleased]: https://github.com/ktagashira/adk-slack-adapter/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/ktagashira/adk-slack-adapter/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/ktagashira/adk-slack-adapter/compare/v0.2.1...v0.2.2
[0.1.0]: https://github.com/ktagashira/adk-slack-adapter/releases/tag/v0.1.0
