---
name: spec-driven-develop
description: Mandatory default entry point for any non-trivial build/add/fix/implement/refactor request — drives work through explicit spec-driven-development phases (constitution check → specify → clarify → plan → tasks → implement → verify/converge). Adapts GitHub spec-kit's workflow (github.com/github/spec-kit) onto existing harness skills instead of installing spec-kit's `specify` CLI — no new dependency, keeps the docs/specs/<date>-<slug>/ convention. Supersedes standalone /plan as the default path for multi-step or ambiguous work; /plan remains a valid sub-phase and stays directly invocable for planning-only asks. Skip for trivial edits (<3 files, mechanical). Use whenever the user asks to build/add/fix/implement/refactor anything non-trivial and no more specific composite (hotfix, incident-response, release-cut, merge-confidently, etc.) matches.
---

# Spec-Driven Develop

Composite skill. Chains existing skills into spec-kit's phase order and terminology, without spec-kit's CLI or `.specify/` directory convention.

**See also:** `spec-driven-development` teaches the underlying SDD pattern (spec-as-contract, agent grounding, anti-patterns) in the abstract. This skill is its operational form for this harness — the concrete composite that actually chains sub-skills phase by phase. Read the pattern skill first if the "why" is unclear; use this one to execute.

## Why this exists

GitHub's spec-kit enforces a structured spec → plan → tasks → implement workflow via a `specify` CLI that scaffolds `.specify/` templates. This harness already has an equivalent skill for every phase — `adt-specs-spec-new`, `grill-with-docs`, `plan`, `plan-to-issues`, `dispatch`/`orchestrate`, `review`/`verify`. Installing the actual CLI would duplicate that coverage, add an external dependency, and fight the existing `docs/specs/<date>-<slug>/` convention. This skill gets spec-kit's discipline (explicit phases, no skipping straight to code) without the tool.

## Phase mapping

| Spec-kit phase | This skill's step | Sub-skill invoked |
|---|---|---|
| constitution | Phase 0 — confirm CLAUDE.md/CONTEXT.md exist for the repo; if `.harness/constitution.json` exists, treat it as authoritative (not `constitution.md`, its human-readable mirror) and also read `.harness/mcp-policy.json` when present; note gaps, don't block | (read-only check) |
| specify | Phase 1 — create/find the spec | `adt-specs-spec-new` → `docs/specs/<date>-<slug>/spec.md` |
| clarify | Phase 2 — resolve ambiguity inline | `grill-with-docs` |
| plan | Phase 3 — phased implementation plan | `plan` → `.claude/plans/<name>.md` (or `.agents/plans/`) — that skill's real output location; the persisted spec from Phase 1 is what carries forward past session scope, not this plan file |
| tasks | Phase 4 — externalize tasks if tracked work | `plan-to-issues` (skip if session-scoped, not tracked) |
| implement | Phase 5 — execute tasks, parallel where independent | `dispatch` / `orchestrate` / `loop` (mandatory parallel-execution rule applies) |
| analyze / converge | Phase 6 — gate before done | `review`, `verify`, `pr-merge-readiness` |

## Stop conditions

- **Trivial edit** (<3 files, mechanical, no ambiguity): skip this pipeline entirely, go straight to `add` or a direct edit. Forcing the full phase sequence on a one-line fix is the exact overhead the "negative rules" in `skill-auto-invoke.md` warn against.
- **Read-only ask** (audit, analysis, question): this skill doesn't apply — use the diagnostic skill directly.
- **A more specific composite matches** (hotfix, incident-response, release-cut, merge-confidently, debug-deep, or any other named lifecycle composite): defer to it. This skill is the default for build/add/fix/implement when nothing more specific matches, not a universal override.
- **Bailing mid-phase**: surface the blocker as this skill's output, mark the phase incomplete, resume next turn — never silently drop to ad-hoc editing (same contract as other composites, `standards/composite-contract.md`).

## Interop with actual spec-kit projects

If a repo already has a `.specify/` directory (from someone using the real spec-kit CLI), read its templates as seed input for Phase 1 — but write output under `docs/specs/<date>-<slug>/`, not `.specify/`. Never install the `specify` CLI as part of this skill; that decision needs an explicit ask (new external dependency).
