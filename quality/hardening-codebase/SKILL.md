---
name: hardening-codebase
description: Audit and tighten codebase quality gates — architecture, lint, types,
  tests, docs, code review. Use when onboarding a project, before a release, or
  when validation is too permissive.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent
  argument-hint: "[scope: full | audit | tighten | review | fix | arch | docs]"
  stability: experimental
---

# Harden Codebase

**Scope**: $ARGUMENTS (default: full)

Systematic quality tightening. Nine phases, each with a clear gate.
KISS: tighten one level at a time — never jump to max strictness.

## Phase 1: ARCHITECTURE (read-only)

1. Identify entry points, module boundaries, and dependency flow
2. Map layering: which modules depend on which?
3. Flag circular dependencies and boundary violations
4. Output module map as indented text tree (plain markdown, no diagrams)
5. Note undocumented coupling, god modules, misplaced responsibilities

**Gate**: Module map + issue list. Present to user before
proceeding.

## Phase 2: AUDIT (read-only)

1. Does `make setup_all` (or equivalent) work from scratch?
2. What lint rules are enabled? Gap vs recommended?
   See `references/lint-tightening-checklist.md`
3. Type checker strictness level?
4. Do tests pass? Are slow/hardware tests filtered?
5. Is check-only gate separate from auto-fix?

**Gate**: Issue list ranked HIGH/MEDIUM/LOW. Present to user before
proceeding.

## Phase 3: TIGHTEN (config only — no code changes)

1. Enable next-level lint rules (baseline → recommended, not strict)
2. Bump type checker one level
3. Split auto-fix from check-only gate if missing
4. Add test marker filters for slow/hardware/network
5. Count new violations — report before fixing

**Gate**: Config committed. Violation count known.

## Phase 4: FIX (mechanical)

1. Run auto-fix
2. Fix remaining violations manually
3. Update tests broken by signature changes
4. `make validate` must pass

**Gate**: All checks green. Commit fixes.

## Phase 5: DOCS QUALITY

1. Does README exist and reflect current state?
2. Are public APIs documented (docstrings, JSDoc, rustdoc)?
3. Are architecture decisions recorded (ADRs or equivalent)?
4. Do inline comments explain *why*, not *what*?
5. Are there stale/misleading docs that contradict the code?
6. Enforce KISS in docs — no walls of text, no redundant sections
7. Enforce DRY — single source of truth, no copy-pasted explanations
8. Enforce YAGNI — remove docs for features that don't exist

**Gate**: Docs findings list. Present to user before fixing.

## Phase 6: TEST OVERHAUL (meaningful tests only)

1. Classify every test: behavioral / implementation / trivial
2. Rewrite implementation tests as behavioral (assert outcomes, not internals)
3. Delete trivial tests that add no value
4. Add missing behavioral tests for error recovery, state transitions, edge cases
5. Add property-based tests (Hypothesis) for invariants
6. Add complexity gate (complexipy, max 15/function)
7. `make validate` must pass with coverage gate

**Gate**: All tests behavioral. Coverage ≥ 80%. Complexity ≤ 15.

## Phase 7: REVIEW (4 parallel agents)

Launch all four from `references/review-agents.md`:

- **Reuse**: duplication, missing shared helpers
- **Quality**: boundary violations, magic strings, abstractions, bugs
- **Efficiency**: unnecessary work, missed caching
- **KISS/DRY/YAGNI**: over-engineering, dead code, speculative features, deletion candidates

**Gate**: Ranked findings presented to user.

## Phase 8: REFACTOR (apply findings)

1. Fix HIGH and MEDIUM only (80/20)
2. Skip LOW unless trivial
3. `make validate` after each fix
4. Commit by topic

**Gate**: All checks green. Findings addressed.

## Phase 9: SHIP

1. Push branch
2. Create PR with summary + test plan

## Scope shortcuts

- `arch` — Phase 1 only (architecture research + module map)
- `audit` — Phase 2 only (read-only report)
- `tighten` — Phases 2-4 (config + fix)
- `docs` — Phase 5 only (docs quality)
- `tests` — Phase 6 only (test overhaul)
- `review` — Phase 7 only (4-agent review)
- `fix` — Phase 8 only (apply existing findings)
- `full` — All phases

## References

See `references/lint-tightening-checklist.md` for language-specific
rule progressions and `references/review-agents.md` for agent prompts.
