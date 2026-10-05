---
name: claude-agent-sdk
description: Build and maintain applications with the current Claude Agent SDK using installed-version-first documentation, bounded tools, permissions, sessions, MCP.
license: MIT
---

# Claude Agent SDK

## Identify the product

Confirm whether the project uses the Claude Agent SDK, the general Claude API client SDK, Managed Agents, Claude Code CLI, or a third-party wrapper. Their packages and execution models differ. Inspect package manifests, imports, lockfiles, and installed docs; then verify current official Claude Platform documentation.

Do not install/upgrade a package automatically. For migrations, identify the installed predecessor/current package, breaking changes, runtime requirements, and rollback before editing.

## Agent contract

Define task scope, tools, filesystem/network boundary, permissions, human approval points, session persistence, hooks/MCP servers, output schema, budget, timeout, and stop conditions. Keep provider/model in project configuration and validate the exact current ID/capabilities at runtime. Do not choose a model or reasoning mode from this skill.

## Tool safety

- expose least-privilege tools with strict typed inputs;
- enforce authorization in code, not the system prompt alone;
- distinguish read-only, mutating, external, costly, and destructive tools;
- require confirmation for irreversible or externally visible effects;
- bound rounds, concurrency, retries, output, time, and spend;
- treat messages, files, web/MCP content, and tool results as untrusted;
- protect secrets in environment/approved stores and redact logs.

## Sessions and observability

Store only the state needed to resume: task/agent IDs, configuration version, artifact pointers, tool outcomes, usage, request/session IDs, and decisions. Do not persist private chain-of-thought. Log structured lifecycle events and errors without full sensitive payloads. Make cancellation and cleanup reliable.

## Verification

Test permissions and denied tools, schema validation, injection attempts, tool failure/timeout/cancellation, duplicate/replayed effects, session resume, MCP disconnect, budget stop, and SDK/API error classification. Run typecheck and project tests; use a bounded live smoke test only when credentials/network/cost are authorized.

Report SDK/package version, source documentation, configured model source, tools/permissions, tests, data boundary, cost controls, migration/rollback, and skipped live checks.
