---
name: foundation-logging
description: Set up structured logging and basic observability
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# Foundation — Logging

Set up structured logging, error tracking, and basic observability.

## Process

1. Configure structured logging (JSON format for production, human-readable for dev)
2. Set up log levels: DEBUG, INFO, WARNING, ERROR
3. Add correlation IDs for request tracing
4. Configure log sinks (stdout for containers, file for local)
5. Add request/response logging middleware for APIs
6. Set up error tracking hooks (ready for Sentry/similar integration)
7. Document log format and conventions

## Rules

- Never log secrets or PII
- Structured JSON in production, pretty in dev
- Every error must include context (what was happening, what failed)
- Log level configurable via environment