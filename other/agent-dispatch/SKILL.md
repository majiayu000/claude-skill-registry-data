---
name: agent-dispatch
description: "Use when deciding whether to do work directly, delegate it, or which agent/skill gets it: routing a task, picking a spawn type, project-knowledge lookups before a curator spawn. On-demand; moved out of CLAUDE.md."
---
# Agent dispatch (main session, PDs, Coords)

## Act directly vs route
The main session plans and routes; it does not execute project work. Act directly only for: a single read/write, an edit under ~5 lines, one CLI command, a factual answer from loaded context, or when the operator says "do this yourself". Otherwise: (1) work out the intent (ask one sharp question if the "why" would change the build), (2) write a detailed L1→L3 plan (file paths, exact changes, acceptance criteria, risks) to the project's `memory/tasks/ongoing/`, (3) hand it to the project's PD (`/pd-routing`).

## Spawning
- Default executor: `general-purpose`, `model: "sonnet"`, with `Skills: /x, /y` (1-3) in the prompt. Opus only for architecture, hard debugging, final review. Role expertise: tell it to read the role file listed in `{agency-root}/agents-archive/ROLE-MAP.md`.
- Structural agents by name: `{slug}-pd`, pd-coordinator (fallback), coord, mini-coord, critique-* critics, Delegator (ambiguous or cross-domain routing only), curator, codebase-search, save-state-runner, project-scaffolder.
- 2+ independent tasks → one agent each, in parallel, one message. Coupled or sequential implementation → one Coord owns the chain. Only the main session's trivial items (see "Act directly") and a PD's knowledge work (analysis, research, planning, memory) are done directly; implementation never is (`pd-coordinator.md` §Role). Give the reason in one line. The operator wants independent tasks delegated.
- Agent tool for agents, never the Skill tool. Never spawn a new agent when a live one exists: SendMessage it.
- A skill that covers the task beats a new agent: check `{agency-root}/skills/INDEX.md`.

## Lookups before spawns (each spawn costs ~30k tokens of startup)
- Project knowledge: graphify MCP query, Pinecone search or the project's memory files first; spawn `curator` only for multi-source synthesis. Emit `curator_skip` or `curator_spawn` (`{agency-root}/runbooks/metrics-emit-contracts.md`).
- Routing: exact match in `{agency-root}/core/memory/delegator-cache.md` first (exact string only). No match: grep `skills/INDEX.md` and pick 1-3 skills yourself; spawn Delegator only for ambiguous or cross-domain tasks.
- Unknown file location across the agency root: `codebase-search`. Skip it when you have the path.
Full protocol: `{agency-root}/runbooks/service-lookups.md`.

## After a spawn
Own the outcome. A background agent that returns deliverables is verified per `{agency-root}/runbooks/bg-agent-completion-gate.md` (diff or re-check, never its own claim). On failure: fix its environment → retry → re-route → do it yourself last. Review is 3 rounds (Correctness → Design → Polish, `pd-resume/SKILL.md`); after 5 failed attempts, a critique agent is mandatory.
