---
name: pub-sub-patterns
description: Redis pub/sub messaging patterns and implementations. Use when implementing real-time messaging, event-driven architectures, notification systems, or message broadcasting with Redis pub/sub.
allowed-tools: Read, Bash, Grep, Glob
---

# pub-sub-patterns

**Purpose**: Redis pub/sub messaging patterns and implementations.

**Activation Triggers**:
- When implementing pub/sub messaging
- When user mentions real-time notifications, event broadcasting
- When designing event-driven architectures

## Quick Reference

This skill provides templates, scripts, and examples for Redis pub/sub patterns.

## Scripts

- `scripts/setup-redis.sh` - Initial Redis setup and configuration
- `scripts/validate-config.sh` - Validate Redis configuration
- `scripts/test-connection.sh` - Test Redis connectivity

## Templates

- `templates/basic-config.ts.template` - TypeScript Redis pub/sub config
- `templates/basic-config.py.template` - Python Redis pub/sub config
- `templates/redis-config.env.template` - Environment variables template
- `templates/docker-compose.yml.template` - Docker Compose setup

## Examples

- `examples/basic-usage.md` - Basic pub/sub patterns
- `examples/fastapi-example.md` - FastAPI integration example
- `examples/nextjs-example.md` - Next.js integration example

## Security Compliance

This skill follows strict security rules:
- All code examples use placeholder values only
- No real API keys, passwords, or secrets
- Environment variable references in all code
- `.gitignore` protection documented
