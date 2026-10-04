---
name: aws-agentcore
description: Build, test, migrate, integrate, and deploy Amazon Bedrock AgentCore agents. Use for AgentCore runtime, local development, import/migration, deployment, Memory, Gateway/MCP tools, Identity, Observability, Browser, Code Interpreter, Evaluations, Registry, Payments, policy, and harness-vs-code-path decisions. Load references only when that component is needed.
allowed-tools: Read Edit Write MultiEdit Grep Glob Bash
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.8"
  updated: "2026-06-02"
  category: ai
---

# AWS AgentCore

## Purpose

Build and operate Amazon Bedrock AgentCore agents without stuffing runtime, harness, Memory, Gateway, Identity, Observability, Browser, Code Interpreter, Evaluations, Registry, Payments, policy, and environment/skills details into every prompt.

## When to use

Use this skill when the user asks to:

- create or adapt an AgentCore project,
- configure local development, invocation, packaging, deployment, runtime settings, harness settings, or environment/skills paths,
- integrate AgentCore Memory, Gateway, MCP tools, Identity, Observability, Browser, Code Interpreter, Evaluations, Registry, or Payments,
- review AgentCore security, least privilege, policy, tool exposure, credential handling, migration, or production readiness.

## Lean operating rules

- First decide whether the user has an existing agent or needs a new project. Do not scaffold over an existing codebase.
- For new projects, prefer the npm AgentCore CLI package `@aws/agentcore` because current AWS documentation recommends it.
- Treat the Python starter toolkit as legacy/migration-oriented unless the user is explicitly working inside an existing Python-based toolkit workflow.
- Separate code-based agents from config-based harnesses. Do not mix their guidance casually; current AWS docs describe the harness path as preview.
- Prefer current AWS documentation tools for AgentCore service behavior. Use the component facts and sampled live evidence in `references/official-sources.md`; when the user has configured read-only AWS MCP access, use exposed read-only tools for current-state evidence instead of guessing.
- Treat CLI syntax as version-sensitive; verify exact commands with installed tooling before production use.
- Treat Gateway policy, identity propagation, skill-path and filesystem loading, observability prerequisites, evaluation loops, registry governance, and payment spending controls as first-class concerns, not afterthoughts.
- Never ask users to paste AWS credentials, client secrets, access tokens, account IDs, customer data, or private keys into chat.
- Load only the reference needed for the component in scope.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use for end-to-end AgentCore project, local test, deployment, and output formatting.
- [Safety checklist](references/safety-checklist.md) — use before deployment, tool exposure, credential integration, Memory/Gateway changes, or production recommendations.
- [Official sources](references/official-sources.md) — use when grounding current AgentCore service behavior and docs URLs.
- [Getting started](references/getting-started.md) — use for project/runtime/harness/local workflow details, direct code deployment, filesystem mounts, and CLI/Inspector caveats, then verify commands against current toolkit version.
- [Memory integration](references/memory-integration.md) — use only for AgentCore Memory resource and agent wiring work.
- [Gateway integration](references/gateway-integration.md) — use only for Gateway, MCP tools, and tool target integration.

## Response minimum

Return, at minimum:

- the AgentCore component in scope,
- evidence level and docs/tooling used,
- safest next action,
- command or code path to verify,
- security and rollback caveats.
