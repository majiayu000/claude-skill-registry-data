---
name: sigil-grok-bridge
description: Keyless Model Context Protocol (MCP) bridge exposing governed Sigil task submission and inbox inspection to Grok Bot.
compatibility: Node.js 22+, Sigil connector daemon running locally at SIGIL_CONNECTOR_URL (default http://127.0.0.1:4411).
---

# Sigil Grok Bridge

Exposes `sigil_send_task` and `sigil_check_inbox` MCP tools over stdio to external agents.

## Architecture & Security Model

- **Keyless RPC Client**: Operates without private keys or signing credentials. All signature generation, canonicalization, and capability intersection remain isolated inside the loopback Sigil connector daemon.
- **Loopback Isolation**: Connects to `127.0.0.1:4411` over HTTP, preventing exposure of raw filesystem paths or key stores.
- **Fail-Closed Governance**: Enforces step-up authentication and capability intersection on task submissions.

See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md) for Toolforge conventions.
