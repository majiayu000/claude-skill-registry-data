---
name: backend-standards
description: Hono/Bun patterns and backend best practices for this project. Use when implementing API endpoints, WebSocket handlers, services, or server-side logic in packages/server.
---

# Backend Standards

## Key Principles

- **Server is the source of truth** - Backend manages all session/worker state
- **Structured logging** - Use Pino with context objects
- **Resource cleanup** - Always clean up PTY processes and connections
- **Type safety** - Define types in shared package, validate at boundaries

## Tech Stack

- Bun, Hono, bun-pty, Pino, Valibot

## Backend Best Practices

- **Resource Cleanup** - PTY processes, WebSocket connections, file handles must be cleaned up
- **Callback Detachment** - Detach callbacks when resources are destroyed (memory leak prevention)
- **WebSocket Message Types** - Define and validate server→client and client→server types explicitly
- **Output Buffering** - Buffer rapid PTY output before WebSocket send to reduce message frequency
- **Structured Logging** - Use Pino with structured data: `logger.info({ sessionId }, 'message')`

## Detailed Documentation

- [backend-standards.md](backend-standards.md) - Directory structure, Hono, logging, services, testing, security, best practices
- [websocket-patterns.md](websocket-patterns.md) - Dual WebSocket architecture, message protocol, broadcasting
