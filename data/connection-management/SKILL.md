---
name: connection-management
description: Redis connection pooling, client configuration, and reconnection strategies. Use when setting up Redis clients, managing connection pools, handling reconnection logic, or configuring sentinel/cluster modes.
allowed-tools: Read, Bash, Grep, Glob
---

# connection-management

**Purpose**: Redis connection pooling, client configuration, and reconnection strategies.

**Activation Triggers**:
- When setting up Redis connections
- When user mentions connection pooling, client configuration
- When implementing high-availability Redis setups

## Quick Reference

This skill provides templates, scripts, and examples for Redis connection management.

## Scripts

- `scripts/setup-redis.sh` - Initial Redis setup and configuration
- `scripts/validate-config.sh` - Validate Redis configuration
- `scripts/test-connection.sh` - Test Redis connectivity

## Templates

- `templates/basic-config.ts.template` - TypeScript Redis connection config
- `templates/basic-config.py.template` - Python Redis connection config
- `templates/redis-config.env.template` - Environment variables template
- `templates/docker-compose.yml.template` - Docker Compose setup

## Examples

- `examples/basic-usage.md` - Basic connection patterns
- `examples/fastapi-example.md` - FastAPI integration example
- `examples/nextjs-example.md` - Next.js integration example

## Security Compliance

This skill follows strict security rules:
- All code examples use placeholder values only
- No real API keys, passwords, or secrets
- Environment variable references in all code
- `.gitignore` protection documented
