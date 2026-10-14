---
name: cross-provider-agent
description: Dispatch a bounded task to a Claude, Codex, Cursor, or OpenCode CLI agent with least authority. Use for independent reviews, named authority profiles, or external-provider subagents.
---

# Cross-Provider Agent
Use a subagent through a cli. Per cli invocations are under skills:

 `/claude-agent`
 `/codex-agent`
 `/cursor-agent`
 `/opencode-agent`

## Choosing harness/model provider

 1. For models with a particular provider plan, always use their native harness and subsidized plan
    - e.g. codex - gpt models, claude code - anthropic models, cursor - grok models
 2. Deffering to 1 or user instructions, prefer spwaning subagents using the harnesses own subagent tool
 3. When independence matters (e.g. reviewing or judging work) exclude the
   model provider that produced the work.

## Authority profiles

Profiles are provider-neutral authority contracts applied by adapters to one
fresh child. Adapter encodings live under `profiles/<name>/` beside each
adapter's SKILL.md.

### Profile index

- [`github-pr-reviewer`](profiles/github-pr-reviewer.md) — read and enforce
  before choosing an adapter.

## Workspace ownership

Require an absolute path to a caller-prepared workspace. The caller owns
checkout creation, pinning, verification, and deletion.

## Distinguish network denial from authentication failure

Transport errors (`dial`, `lookup`, `connect`, loopback failures) indicate
sandboxed network access; an HTTP 401 "Bad credentials" response indicates
authentication failure.
