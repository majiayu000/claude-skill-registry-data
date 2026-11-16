---
name: mcp-server-development
description: Design, implement, and validate an MCP server that exposes a bounded set of tools or resources to AI clients. Use when integrating an external API, service, or local capability through MCP.
---

# MCP Server Development

Design the server around a real client workflow and current MCP protocol requirements.

1. Confirm the client/runtime, SDK, transport, deployment model (local stdio or remote HTTP), authentication needs, and target MCP version from current official documentation.
2. Define the smallest useful set of tools, resources, or prompts. Give each a narrow purpose, stable name, clear description, strict input schema, and predictable output shape.
3. Treat tool inputs and upstream data as untrusted. Validate parameters, authorize each operation, constrain file/network access, and keep secrets in approved environment or secret-management systems.
4. Design safe failure behavior: structured errors, timeouts, cancellation, rate limits, bounded responses, and idempotency for operations that may be retried.
5. Implement with a maintained official SDK where practical. Separate protocol handling from business logic so the core behavior can be tested without an MCP client.
6. Test valid and invalid inputs, permission boundaries, missing credentials, upstream failures, large responses, cancellation, and transport startup/reconnection using an MCP inspector or representative client when available.
7. Document capabilities, input/output schemas, side effects, required permissions, configuration, launch/deployment steps, and known client compatibility limits.
8. Review logs and telemetry for secret or personal-data leakage. Obtain approval before connecting to production services or publishing/deploying the server.

Deliver architecture choices, tool/resource inventory, implementation, reproducible tests, setup instructions, and limitations. Do not claim client compatibility without testing it. Do not expose broad shell, filesystem, database, or network access when a narrower tool will do.
