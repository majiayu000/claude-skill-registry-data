---
name: council-review
description: Multi-model validation council — auto-validate plans, architecture changes, and PRs via validate-plan/review before executing
when-to-use: When you write a plan to ~/.claude/plans/, make architectural changes, or before marking a PR done; required for CLAUDE-tier tasks
user-invocable: false
allowed-tools: [Bash, Read]
effort: high
---

# Council of Experts — Multi-Model Validation

> **⚠️ Status (2026-07-15, ADR-0008 FIX).** Command paths corrected `~/bin/` → `bin/`
> (`bin/validate-plan` is real and on PATH; `~/bin/` is empty. **`bin/review` was CUT
> 2026-07-27, ADR-0014** — review is Claude-only by decision, so this skill covers PLAN
> validation only.)
> **Not yet provisioned here, and deliberately not rewritten:** `~/.claude/council.yaml`
> (absent — the binaries do not read it), a `claude-fable-5` wrapper (absent — Claude is the
> host), and the **Codex** reviewer (`codex` absent). The real roster + config mechanism is a
> **conclave/council design decision** (ADR-0008, handoff item 1), not a prune edit — until then,
> treat the roster and `council.yaml` references below as *illustrative*, and rely on
> `bin/validate-plan`'s own honest exit codes (voted / unavailable / broken → exit 2, no verdict).
>
> **Where that decision now lives (2026-07-17):** `docs/contracts/three-project-cohesion.md` — the
> canonical map of the Conclave·Tessera·pr-arbiter system. The roster/config question is Open
> decision **D1** (routing home: do these `bin/` wrappers collapse into conclave gateway calls?).
> **Tension to carry into that decision — this skill is NOT shielded by anti-conflation guard (a).**
> Guard (a) protects pr-arbiter's *union-recall code review* from conclave's "route, don't judge"
> null. But council-review's **plan-VALIDATION** path (a panel judging one plan → approve/revise) is
> **select-best, not union-recall** — the exact regime where conclave's null is a *genuine caution*,
> not a false blocker. So: a multi-model plan panel must justify itself against the select-best null
> (does fan-out+judge beat routing the plan to the one strongest reviewer?), whereas the multi-engine
> **PR-review** path inherits pr-arbiter's union-recall win. Two paths, two verdicts — do not let the
> code-review win launder the plan-validation panel.

## When to Auto-Trigger

### Plans (auto_validate_plans)
When you write a plan to `~/.claude/plans/`, automatically validate it:
```bash
bin/validate-plan --threshold 2 ~/.claude/plans/<plan-file>.md
```
- 2+ of 3 approve → execute immediately
- 1 of 3 → surface reviewer feedback to user before proceeding
- 0 of 3 → revise plan, re-validate

### Architecture Decisions (auto_review_architecture)
When making architectural changes (new services, API redesigns, database schema changes), run:
```bash
# Architecture review: use Claude Code's native /code-review (ADR-0014).
# bin/review was cut — it had no working backend and had never run.
```

### PR Review (auto_review_prs)
Before marking a PR as done, run:
```bash
# Changed-file review: native /code-review (ADR-0014).
```

## Configuration

Council behavior is *intended* to be configured in `~/.claude/council.yaml` — **not present here, and not read by the binaries yet** (see Status banner). The config mechanism is pending the conclave design.

### Chief of the Council

`chief: claude-fable-5` — Claude Fable 5 (Anthropic's most capable widely-released
model, GA 2026-06-09) leads every panel as the chief: it reviews first and casts
the deciding synthesis. Claude is the host model (no `bin/` wrapper). Chief-override config is pending the conclave design.

### Reviewer Contexts

The chief leads each context, followed by the panel:

| Context | Default Reviewers | When |
|---------|-------------------|------|
| `plan` | **Claude Fable 5 (chief)**, DeepSeek Pro, Codex, Gemini Pro | Before executing any plan |
| `review` | **Claude Fable 5 (chief)**, DeepSeek Pro, Kimi | Code review, PR review |
| `architecture` | **Claude Fable 5 (chief)**, DeepSeek Pro, Gemini Pro, Grok | System design, schema changes |

### Threshold Rules

The `threshold` setting controls how many approvals are needed:
- `threshold: 2` with 3 reviewers → need 2/3 to auto-execute
- Clamped to [1, reviewer_count] — can't be 0 or exceed available reviewers

## Model Inventory

All 13 tiers are listed in `~/.claude/council.yaml` under `models:`. Each has:
- `id` — unique identifier
- `cmd` — CLI command to invoke (null for Claude models, which are the host)
- `tier` — routing priority (0=cheapest, 12=most capable)
- `label` — human-readable name

Use `POST /api/models/health` to verify all models are responding.

## How This Skill is Used

This skill is loaded by Claude Code on session start. It provides the behavioral rules for when to invoke multi-model validation. The actual execution happens via `bin/validate-plan` (real, on PATH). **Code review is NOT
in scope here** — ADR-0014 declared it Claude-only and cut `bin/review`; use the native
`/code-review`. What survives is the multi-model PLAN validation council, kept deliberately
per ADR-0007 pending the conclave design.

**Do not skip council validation for CLAUDE-tier tasks.** The whole point is that architecture and security decisions get independent verification before execution.
