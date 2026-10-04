---
name: mcp-server-development
description: "Use when building or modifying an MCP server that exposes tools, resources, prompts, or transport behavior to an agent host to verify current protocol and SDK documentation, keep capabilities narrow, validate every boundary, and test through a local or staging client before exposing the service. Trigger for MCP server authoring, SDK upgrades, or transport changes."
---

# MCP Server Development

## Overview

This skill applies when building or modifying an MCP server that exposes tools, resources, prompts, or transport behavior to an agent host. Its intended outcome is to verify current protocol and SDK documentation, keep capabilities narrow, validate every boundary, and test through a local or staging client before exposing the service.

## When to Use

### Preserved source section: When to Use

Use when implementing the server side of Model Context Protocol. For connecting to or reviewing a third-party MCP server, use `mcp-server-integration-safety` instead; the two skills may be combined for end-to-end work.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

1. **Verify current APIs.** Check the official MCP specification and the exact SDK version's documentation before writing code. Treat older examples as potentially stale; do not assume method names or lifecycle behavior are unchanged.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Intended host/client, required MCP capabilities, and supported protocol version.
- Current SDK and runtime versions, official documentation, and transport constraints.
- Tool/resource schemas, authorization model, data sources, and side effects.
- Local test harness, secrets policy, deployment environment, and approval boundary.

## Instructions

### Preserved source section: Procedure

1. **Verify current APIs.** Check the official MCP specification and the exact SDK version's documentation before writing code. Treat older examples as potentially stale; do not assume method names or lifecycle behavior are unchanged.
2. **Choose capabilities deliberately.** Expose only the tools, resources, and prompts required. Prefer read-only resources for retrieval, and make side-effecting tools explicit in their names, descriptions, schemas, and confirmations.
3. **Separate protocol from business logic.** Keep core functions testable independently of transport. Choose stdio for local process integrations or a supported HTTP transport for remote use; document authentication and network boundaries.
4. **Define schemas and results.** Validate input types, ranges, identifiers, and size limits. Return structured, bounded results and actionable errors without secrets, raw stack traces, or ambiguous partial success.
5. **Handle effects safely.** Use least privilege, idempotency where possible, timeout and rate budgets, and human approval for consequential writes. Treat all model-supplied parameters and external service results as untrusted.
6. **Respect transport behavior.** For stdio, reserve stdout for protocol messages and send diagnostics to stderr. For HTTP, enforce authentication, origin/network controls, request limits, and safe shutdown.
7. **Test against a client.** Verify initialization, capability discovery, tool/resource/prompt invocation, malformed inputs, cancellation, errors, reconnects, and logs using a local or staging host.
8. **Review before exposure.** Pin dependencies, inspect permissions and secrets, document install/config steps, and obtain approval before opening a public listener or connecting production credentials.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Report protocol/SDK versions, exposed capabilities, transport, permissions, tests, configuration, and known limits. Accept when a real compatible client can discover and use the declared capabilities, invalid inputs fail safely, and no unapproved external service or write is reachable.

## Tools and Resources

### Preserved source section: References

Use the [official MCP server-development documentation](https://modelcontextprotocol.io/docs/develop/build-server) and current SDK documentation for version-specific APIs.

## Output Format

### Preserved source section: Output and Acceptance

Report protocol/SDK versions, exposed capabilities, transport, permissions, tests, configuration, and known limits. Accept when a real compatible client can discover and use the declared capabilities, invalid inputs fail safely, and no unapproved external service or write is reachable.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

4. **Define schemas and results.** Validate input types, ranges, identifiers, and size limits. Return structured, bounded results and actionable errors without secrets, raw stack traces, or ambiguous partial success.
5. **Handle effects safely.** Use least privilege, idempotency where possible, timeout and rate budgets, and human approval for consequential writes. Treat all model-supplied parameters and external service results as untrusted.
7. **Test against a client.** Verify initialization, capability discovery, tool/resource/prompt invocation, malformed inputs, cancellation, errors, reconnects, and logs using a local or staging host.

### Source edge/failure guidance from: Output and Acceptance

Report protocol/SDK versions, exposed capabilities, transport, permissions, tests, configuration, and known limits. Accept when a real compatible client can discover and use the declared capabilities, invalid inputs fail safely, and no unapproved external service or write is reachable.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report protocol/SDK versions, exposed capabilities, transport, permissions, tests, configuration, and known limits. Accept when a real compatible client can discover and use the declared capabilities, invalid inputs fail safely, and no unapproved external service or write is reachable.
