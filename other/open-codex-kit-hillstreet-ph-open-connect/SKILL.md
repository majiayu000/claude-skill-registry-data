---
name: open-codex-kit
description: Install, verify, configure, and operate OpenAI Codex CLI and the OpenAI Agents SDK with cloud terminals, isolated workspaces, browser/computer adapters, MCP servers, skills, plugins, Git workflows, and Open-Connect. Use for Codex setup, agent-runtime diagnostics, capability inventory, safe automation, plugin packaging, or publishing the Open Codex Kit to Open-Connect.
---

# Open Codex Kit

Operate a verified Codex and Agents SDK workspace through one security-conscious workflow.

1. Inspect platform, repository instructions, versions, authentication state, and writable paths.
2. Read current official OpenAI documentation before changing Codex, Agents SDK, MCP, skills, or plugin configuration.
3. Prefer a structured API or MCP tool over browser automation. Use isolated compute for untrusted code.
4. Keep credentials server-side and pass only opaque references or environment placeholders.
5. Use branch -> tests -> pull request -> required checks -> approved merge -> deployment verification.
6. Require explicit approval for destructive actions, production writes, DNS, credentials, billing, or account membership.
7. Report confirmed versions, checks, safe evidence, approvals, and blockers. Never claim unverified installation, publication, merge, or deployment.

Use the Agents SDK for managed turns, handoffs, guardrails, sessions, tracing, and sandbox agents. Use the Responses API directly when the caller owns the loop. Keep one primary connector per provider unless another has a distinct documented purpose.
