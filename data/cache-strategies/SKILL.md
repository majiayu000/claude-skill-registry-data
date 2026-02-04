---
name: cache-strategies
description: Caching patterns, TTL management, eviction policies for Redis implementations. Use when implementing cache-aside, write-through, write-back patterns, TTL management, or cache invalidation strategies.
allowed-tools: Read, Bash, Grep, Glob
---

# cache-strategies

**Purpose**: Caching patterns, TTL management, eviction policies for Redis implementations.

**Activation Triggers**:
- When implementing cache strategies
- When user mentions Redis Caching patterns, TTL management, eviction policies
- When designing Redis architecture

## Quick Reference

This skill provides templates, scripts, and examples for Redis caching patterns.

## Scripts

- `scripts/setup-redis.sh` - Initial Redis setup and configuration
- `scripts/validate-config.sh` - Validate Redis configuration
- `scripts/test-connection.sh` - Test Redis connectivity

## Templates

- `templates/basic-config.ts.template` - TypeScript Redis configuration
- `templates/basic-config.py.template` - Python Redis configuration
- `templates/redis-config.env.template` - Environment variables template
- `templates/docker-compose.yml.template` - Docker Compose setup

## Examples

- `examples/basic-usage.md` - Basic caching patterns and usage
- `examples/fastapi-example.md` - FastAPI integration example
- `examples/nextjs-example.md` - Next.js integration example

## Security Compliance

This skill follows strict security rules:
- All code examples use placeholder values only
- No real API keys, passwords, or secrets
- Environment variable references in all code
- `.gitignore` protection documented
