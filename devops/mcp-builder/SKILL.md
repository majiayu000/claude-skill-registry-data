---
name: mcp-builder
description: Use when designing, implementing, testing, or reviewing a Model Context Protocol server that exposes tools, resources, or prompts to an external service. Do not use for ordinary API clients or MCP client configuration unless server design is in scope.
license: Apache-2.0
---

# MCP Server Builder

Design MCP servers around safe, discoverable workflows. The server is an
integration boundary: its tools must be understandable to an agent, constrained
by explicit schemas, and safe to operate against an external system.

## Compatibility and approval

MCP protocol details and SDK APIs change. Identify the target protocol revision,
SDK, language, transport, and host capabilities before implementation. Use
`source-driven-development` to consult the current MCP specification and the
chosen SDK's official documentation. Keep SDK and host mechanics conditional;
do not make one language, vendor, inspector, or client a repository-wide
requirement.

Pause for explicit approval before adding an external integration, credentials,
network access, tool registration, deployment configuration, or a write-capable
operation. A server's annotations and descriptions help hosts make decisions;
they do not replace host-side authorization or user approval.

## Phase 1: Scope and research

1. Identify the external service, users, data classes, API version, auth model,
   rate limits, pagination, failure modes, and operations that are in scope.
2. Mark every operation as read-only, mutating, or destructive. Define the
   confirmation and authorization boundary for each mutating operation.
3. Choose MCP primitives deliberately:
   - Tools perform bounded actions or queries.
   - Resources expose addressable read-oriented context.
   - Prompts provide reusable interaction templates only when the host needs
     them.
4. Decide whether the server is local or remote and select a transport from
   current official documentation. Document lifecycle, state, timeout, and
   cancellation behavior.
5. Write a compact tool inventory before coding. Prefer broad enough coverage
   for real workflows, but do not expose an unbounded proxy over the service.

The research output must contain the API and MCP sources, selected operations,
trust boundaries, compatibility assumptions, and unresolved questions.

## Phase 2: Tool design

For every tool:

- Use a stable domain prefix and an action-oriented name.
- Keep the description concise, specific, and useful for tool discovery.
- Define strict input schemas with types, bounds, allowed values, examples, and
  clear descriptions. Reject unknown or unsafe input where the SDK supports it.
- Return focused results. Support filtering, pagination, field selection, and
  stable ordering instead of returning an entire remote dataset.
- Prefer structured output where the SDK and host support it, with a concise
  human-readable summary when useful.
- Return actionable errors that identify the safe next step without exposing
  credentials, raw provider responses, internal paths, or stack traces.
- Declare read-only, destructive, idempotent, and open-world annotations when
  supported, and make them match the implementation exactly.

Do not design a tool whose name or description hides side effects. Separate
preview, plan, and apply operations when that makes approval and review clearer.

## Phase 3: Implementation

Build the smallest shared infrastructure that keeps behavior consistent:

- An API client that centralizes authentication, timeouts, retries, pagination,
  rate-limit handling, and response normalization.
- Validation at the MCP boundary and again before sensitive service calls.
- Error mapping that preserves useful status and retry information without
  leaking sensitive data.
- A response formatter that keeps tool output bounded and predictable.
- Dependency injection or another local seam for deterministic tests.

Use the repository's package manager, language conventions, and lockfile. Do
not install packages, create credentials, or enable networked services without
approval. Keep secrets in an approved secret mechanism, never in source,
fixtures, tool output, logs, prompts, or command arguments.

Apply `security-and-hardening` to authentication, authorization, tenant scope,
URL/path handling, request validation, sensitive data, dependency risk, and
destructive operations. Treat model-generated arguments as untrusted input.
For prompt injection, retrieval, memory, model-output, or agent/tool trust
boundary analysis, pair this with `ai-security-review`.

## Phase 4: Review and test

Verify the protocol contract and the external-service boundary separately:

1. Run formatting, lint, type, build, and unit checks available in the project.
2. Test valid and invalid schemas, missing permissions, expired auth, timeouts,
   rate limits, pagination boundaries, empty results, partial failures, and
   provider errors.
3. Exercise read-only tools against safe fixtures or a separately approved
   test service. Do not use production data for local testing.
4. Test mutating tools with mocks or an isolated environment first. Confirm
   confirmation, authorization, idempotency, and retry behavior.
5. Use an MCP protocol client or inspector only when it is already available
   or explicitly approved; record its version and the checks it performed.
6. Review the final diff for secret exposure, unintended network access,
   missing authorization, unbounded results, unsafe defaults, and tool metadata
   that contradicts behavior.

Do not treat compilation or a successful handshake as proof that workflows are
correct. Verify representative tool calls and their failure paths.

## Optional evaluation

When the server is intended for repeated agent use, create a separate,
read-only evaluation set. Questions should be independent, realistic, stable,
multi-step, and have answers that can be verified from the service data. First
inspect the available tools, then solve each question yourself and document
the expected answer. Keep evaluation artifacts local and do not require a
remote repository at runtime.

## Completion record

Report:

- Protocol/SDK/transport versions and official sources consulted.
- Tool inventory, schemas, side-effect classification, and auth boundary.
- Tests, fixtures, protocol checks, and external checks that actually ran.
- Approval-gated actions that remain, compatibility assumptions, and residual
  security or operational risk.

## Upstream basis

Adapted for this harness-agnostic repository from
[anthropics/skills mcp-builder](https://github.com/anthropics/skills/tree/34040c9c568585f6929bedeaad110ad08f079624/skills/mcp-builder).
The upstream skill is Apache-2.0; this entrypoint is a modified local version
dated 2026-09-11 with provider-specific commands and external reference-file
dependencies removed.
