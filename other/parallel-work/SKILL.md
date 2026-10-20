---
name: parallel-work
description: Split a multi-area agent-office task across parallel subagents per .claude/rules/PARALLEL_WORK.md — contract first, disjoint file ownership, lead-only shared config, phased integration. Use for any task touching two or more of assets, core, adapters, desktop, renderer logic, renderer adapters or docs, or whenever the user asks to work in parallel.
---

# Parallel work (lead checklist)

1. **Map areas → agents.** List the areas the task touches; one agent per area/layer (hexagon). ≤ 5 running at once.
   1b. **Pick each agent's model** (rule §6): the cheapest competent tier — `haiku` for mechanical work, `sonnet` for implementation against a written contract, `opus` for protocol/lifecycle/security/core-refactor work. Escalate one tier after two failed gates.
2. **Contract first (you, alone):**
   - Shared types and docs (`docs/*.md`, `packages/shared`, `packages/web/src/app/office-types.ts`), port interfaces, IPC/HTTP shapes — additive only.
   - `pnpm add` every dependency the agents will need.
   - All shared-config edits (package.json, Makefile, vitest/tsconfig, depcruise, CI, gitignore/gitattributes).
3. **Launch producers in parallel** (assets, backend, pure logic), then consumers (they may start against contract + fixtures). Background agents; one message with all launches.
4. **Relay** every cross-agent fact via `SendMessage`; broadcast contract changes to every affected agent.
5. **Integrate and verify** yourself after each phase: `make check`, `make build test-ui`, `pnpm arch`, screenshots for UI/assets. Route failures to the owner.
6. **Don't enter plan mode while agents run** (it pauses them); if you did, resume each with `SendMessage`.

## Agent prompt template

```
Model: <haiku|sonnet|opus> — <one-line reason>   (set the Agent `model` parameter to match)

You are agent <ID> on the agent-office repo (/Users/asilva/youtube/workspace). Read first (authoritative):
- <plan file §…>, docs/<contract>.md §…, AGENTS.md, .claude/rules/{ARCHITECTURE,TESTING,PRIVACY_SECURITY,SCENE,PARALLEL_WORK}.md

## Your job
<scope, numbered, with acceptance criteria>

## Rules
- Owns ONLY: <files/globs>. Must NOT touch: <files/globs> (owned by <agents>), package.json, lockfile, Makefile, configs.
- No pnpm add/install (report missing deps). No git add/commit/push.
- Strict TDD; keep `pnpm arch` green; run only: <targeted commands>.
- Strip ELECTRON_* env vars when spawning Electron/Blender (VS Code exports ELECTRON_RUN_AS_NODE=1); use make targets.
- If a producer isn't done, develop against the contract + fixtures and report.

## Final report (under N words)
<what to report: APIs, test counts, deviations, open issues>
```
