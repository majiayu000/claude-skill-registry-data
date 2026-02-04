---
name: redis-config-generator
description: Generate Redis configuration files and connection code for caching and session management. Triggers on "create redis config", "generate redis configuration", "redis setup", "cache config".
---

# Redis Config Generator

Generate Redis configuration files and TypeScript client setup for caching.

## Output Requirements

**File Output:** `redis.conf`, `redis.ts`
**Format:** Valid Redis configuration and TypeScript
**Standards:** Redis 7.x, ioredis

## When Invoked

Immediately generate Redis configuration and client connection code.

## Example Invocations

**Prompt:** "Create Redis config for production caching"
**Output:** Complete `redis.conf` and `redis.ts` client setup.
