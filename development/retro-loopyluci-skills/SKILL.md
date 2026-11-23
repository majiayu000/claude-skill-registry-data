---
name: retro
description: Use when conducting a retrospective on a coding session.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering]
    source: mattpocock/skills
    adapted: true
---

# Retro

> **Adapted for the LoopyLuci Skills collection** from [mattpocock/skills](https://github.com/mattpocock/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Conduct a retrospective on a coding session

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Run a retrospective on a coding session and convert the findings into improvements to the agent's *environment* — the files, checks, and steering that shape future runs — rather than a critique of the person.

## Steps

1. Load the writing guidance from the `writing-for-agents` skill.
2. Read the primary sources for the session the user names; if none is named, use the current session. Session logs on this machine may need to be searched.
3. Look for improvement candidates in the categories below.
4. Present the candidates ordered by severity.

## Candidate categories

- **Navigation** — how hard was it to locate the right files? Are there hidden dependencies between files? Would a navigation pointer help? Applies when the session spent a long time finding information.
- **Automated checks** — could a check have caught the mistake? Read the repo's own check command first (its `package.json` or build tool's `lint`/`check` scripts, its CI workflow). A check that exists but is unwired or silently broken is the finding, not a reinvention. A repo with no guardrail at all (no pre-commit hook and no CI job running lint/typecheck/test) is itself a finding: an un-linted repo is a standing missed opportunity, not a neutral default. Applies when the agent made a mistake a check could have caught, or when no guardrail exists.
- **Coding standards** — should the reviewer agent gain a rule, or lose or clarify one? Classify the violation first. A *mechanical* violation (fixed syntactic pattern, banned API, import shape, file-location rule) gets a deterministic check, full stop: a custom linter rule, a pre-commit hook, or a CI job, whichever is cheapest for the repo's language and existing guardrails. Default to building the check rather than writing the rule. Reserve `CODING_STANDARDS.md` for genuine judgement calls (cross-file consistency, "matches the surrounding style", anything no guardrail could substitute for). Applies when the reviewer agent failed to catch a mistake.
- **Global AGENTS.md** — are steering instructions that belong in coding standards or automated checks sitting in AGENTS.md instead? Applies when AGENTS.md is large, in the repo or in the user's global scope.
- **Tool economy** — did the agent make expensive tool calls that could be streamlined? Is custom tooling (CLIs, MCP servers) token-inefficient? Applies when an expensive call was made.
- **No-ops** — are there instructions in steering files that do not change the agent's behavior? Applies when steering files are large and unwieldy.
- **Information access** — could the agent have better access to information (teeing dev-server logs, read-only access to third-party services)? Applies when a crucial piece of information was unavailable.

## Implementation versus review

All work passes through two stages. The implementation agent carries the most context pressure: exploration, writing code, debugging failures. The review agent carries the least — it receives a diff, needs no exploration, and often neither writes code nor debugs. Coding standards therefore belong to the review agent, not the implementation agent.

## Files and their roles

- `AGENTS.md` (or `CLAUDE.md`) — loaded into every agent's context; use sparingly, mainly for navigation pointers.
- `CODING_STANDARDS.md` — read during review, not implementation. Add navigation pointers to docs folders once it exceeds 1,000 lines.
- Docs — reference material, pointed to by other files; look for existing docs before writing new ones.
- Skills — hold documents whose description enters the agent's context, or back user-invoked commands. Follow `writing-for-agents`.

## Verification

- [ ] Candidates are ordered by severity.
- [ ] Each candidate names the evidence that produced it.
- [ ] Mechanical violations are routed to a deterministic check, not a prose rule.
- [ ] No new document duplicates an existing one.

## Related Skills in This Repo

- [pr](../pr/SKILL.md) — Use when writing a PR body.
- [software-factory](../software-factory/SKILL.md) — Use when working with shared language for designing a software factory: the tasks it runs ...
- [writing-for-agents](../writing-for-agents/SKILL.md) — Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- [chief-of-staff](../chief-of-staff/SKILL.md) — Use when working with pursue a long-running goal in a single session by co-ordinating suba...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [mattpocock/skills](https://github.com/mattpocock/skills)
- Path: `_sources/mattpocock_skills/skills/engineering/retro/SKILL.md`
- License: MIT — Copyright (c) 2026 Matt Pocock
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
