---
name: gz-check
persona: main-session
description: Use for pre-merge or pre-attestation verification; runs the per-change gate, or the full sweep with --full.
category: code-quality
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: haiku
metadata:
  skill-version: "1.7.2"
---

# gz check

## Overview

Unified quality gate for all code verification. Replaces the individual
`/lint`, `/test`, `/format`, `/gz-typecheck`, and `/gz-arb` skills.

## Individual Commands

| Command | Purpose |
|---------|---------|
| `uv run gz lint` | Ruff linting + PyMarkdown |
| `uv run gz format` | Ruff auto-formatting |
| `uv run gz typecheck` | Static type checks (ty) |
| `uv run gz smoke` | Smoke/BVT tier — build verification against a 60s budget (GHI #724) |
| `uv run gz test --obpi OBPI-X.Y.Z-NN` | Tests covering one OBPI's REQs (pipeline Stage 3) |
| `uv run gz test` | Full unittest suite |
| `uv run gz test --bdd` | Unit tests + behave (ADR closeout / Heavy-lane) |
| `uv run gz check` | Per-change gate: lint, format, typecheck, every validator, the smoke tier and the tests the change touches (GHI #1191) |
| `uv run gz check --full` | The per-change gate plus the whole unit tier, behave, the docs build, preflight and the guard-canary sweep: CI, release and the `quality-check` chore (GHI #1088, #1191) |

`gz smoke` is the cheapest useful signal: it runs only `@smoke`-marked tests and
fails closed if they exceed the budget in `.gzkit/rules/tests.md`. An empty tier
fails only when `.gzkit.json` declares `smoke.required: true`; otherwise it passes
with an advisory. It proves the build *answers*; it never substitutes for `gz test`,
which proves it is correct.

## When to Use

- **Quick fix-up:** Run individual commands (`gz lint`, `gz format`) after small edits
- **Every change:** Run `gz check`, the per-change gate. Run it once per change, after `git add -A`, so the pre-push hook reuses the pass
- **Before `gz git-sync --apply`:** Run `gz check` first
- **Gate 2:** `gz test` runs the whole unit tier; plain `gz check` runs only the tests the change touches and is not Gate 2 evidence
- **Before a release, at heavy-lane closeout, or to reproduce CI locally:** Run `gz check --full`. The whole unit tier, behave, the docs build and the guard-canary sweep are full-tier work: CI runs them on every code push (`src/gzkit/check_step_scopes.json`, shipped in the package)

## Workflow

1. Run `uv run gz check` with the required options.
2. Summarize results, including evidence and any follow-up gates.
3. **Claude surface check** (Claude Code only): After quality gates pass,
   validate Claude-specific surfaces are healthy. If issues found, invoke
   `@claude-code-guide` to diagnose against current Anthropic documentation.

## Claude Surface Check

When running in Claude Code as a pre-merge or pre-attestation check, run the
following — each item is a concrete tool invocation, not a prose claim:

1. **No hook errors at session start** — review the session start banner for
   hook failures. If any appear, invoke `@claude-code-guide` to diagnose
   against current Anthropic documentation. Do not proceed to attestation
   while hook errors are unresolved.
2. **Generated surfaces match canonical source** — run
   `uv run gz validate --surfaces`. Exit code 0 means `.claude/skills/`
   mirrors `.gzkit/skills/` and `.claude/rules/` mirrors `.gzkit/rules/`.
   Non-zero exit means run `uv run gz agent sync control-surfaces` and
   re-validate.
3. **CLAUDE.md is under budget** — read `CLAUDE.md` with the Read tool and
   check that the final line number reported is ≤ 200. Read returns
   numbered lines so the count is observable without invoking `wc`. If
   over budget, trim before attestation (200-line ceiling for optimal
   adherence).

## Full Quality Evidence Sequence

When deterministic receipts are needed (e.g., for audit evidence):

```bash
uv run gz lint
uv run gz typecheck
uv run gz test --bdd    # full suite including behave — pre-attestation
uv run gz check
```

## Validation

- Verify command output reflects the requested scope.
- If governance state changed, confirm with `uv run gz status` or `uv run gz state`.

## Example

```bash
# Per-change gate (preferred)
uv run gz check

# Full sweep: whole unit tier, behave, docs build, canary sweep (release, closeout, CI parity)
uv run gz check --full

# Individual checks when iterating
uv run gz lint
uv run gz format
uv run gz typecheck
uv run gz test

# If Claude surface issues found, diagnose:
@claude-code-guide look at .claude/settings.json — are all hook
references valid? Any deprecated patterns?
```

## Common Rationalizations

These thoughts mean STOP — you are about to skip the gate that catches drift:

| Thought | Reality |
|---------|---------|
| "I only changed one file — `gz lint` is enough" | `gz check` is the unified gate for a reason: lint passes can hide type, validator or test regressions. It runs in seconds; run it. |
| "`gz check` passed, so the whole unit tier is green" | The per-change gate runs only the tests the change touches, chosen by filename match. The whole tier is `gz test` or `gz check --full`; CI runs it on every code push. |
| "I'll run `gz check --full` after each edit to be safe" | The full sweep is release, closeout, chore and CI work. Running it per edit is the cost the per-change gate exists to remove (operator ruling 2026-10-11, GHI #1191). |
| "Tests pass locally, no need to typecheck" | `ty` catches signature drift that unittest can't. The two checks are complementary, not redundant. |
| "Hook errors at session start are cosmetic" | The Claude surface check is part of `gz check` precisely because hook errors mean an agent is operating against stale governance. Resolve before attestation. |
| "The mirrors look fine, skip the surface check" | Canon/derived drift is silent until it isn't. The mirror parity check is cheap; the bug it prevents is expensive. |
| "I'll run the individual commands instead of `gz check`" | Individual commands skip the Claude surface check and the deterministic ordering. Use them for iterative fix-up, not for pre-merge or pre-attestation. |
| "Coverage is close to 40% — round up" | The coverage floor is fail-closed at 40.00%. Rounding rationalizes a regression. |
| "PyMarkdown warnings are noise" | PyMarkdown is part of `gz lint` because docs are first-class deliverables under the Gate 5 Runbook-Code Covenant. Fix or document the exception. |

## Red Flags

- Closing a brief or attestation without running `gz check`
- Running `gz lint` but not `gz typecheck` or `gz check` before a push
- Citing a plain `gz check` pass as evidence that the whole unit tier passed
- Hook errors in session-start output that were never resolved
- `.claude/skills/` divergent from `.gzkit/skills/` (sync not run)
- CLAUDE.md over 200 lines (budget exceeded, adherence drops)
- Coverage dropped below 40% but the brief was marked complete
- Releasing or closing out an ADR without `gz check --full`

## References

- Command implementation: `src/gzkit/cli/`
- User docs: `docs/user/manpages/index.md`
