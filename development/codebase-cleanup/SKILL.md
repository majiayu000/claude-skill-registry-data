---
name: codebase-cleanup
description: Multi-pass refactor / code-quality cleanup designed to be dispatched as 8 specialist subagents (one per cleanup concern), each running a research → critical-assessment → high-confidence-implementation cycle. Triggers on "clean up the codebase", "tech-debt pass", "refactor for quality", "find dead code", "remove AI slop", or any explicit request for a comprehensive quality sweep. Do NOT trigger for narrow targeted fixes ("remove this one function") or for net-new feature work.
---

# Codebase cleanup — 8-pass refactor

Eight independent specialist passes over a codebase, each scoped to one quality concern. Designed to be run as 8 separate subagent sessions (or sequentially in one) so each pass gets a clean context window and can't be tempted to bleed into another's territory.

Every pass follows the same three-phase protocol — see `reference/protocol.md`. The recommended pass ordering and why is in `reference/pass-ordering.md`.

Apply [codebase-design](../codebase-design/SKILL.md) throughout: keep each
capability together, expose complete operations, and extract only when the split
hides complexity or enables useful reuse. Preserve configured line limits with
documented, targeted exceptions. File count and net deleted lines are not goals.

## When to use

- "Clean up the codebase" / "do a tech-debt pass"
- "Refactor for quality before we ship"
- "Find and remove dead code / AI slop / weak types"
- Onboarding a codebase and wanting to know what's actually load-bearing
- Pre-1.0 / pre-release quality sweep
- Periodic (quarterly) hygiene runs

## When NOT to use

- Narrow targeted asks ("remove this one function", "fix this one type")
- Net-new feature work
- Tight deadline / minimum-viable-fix scenarios — this is a deliberate, careful sweep
- Codebases under active heavy refactor by humans (the passes will fight in-flight work)

## The 8 passes

Run in this order (rationale in `reference/pass-ordering.md`). Each links to the full subagent prompt:

1. **AI slop & stale comments** → `reference/passes/01-ai-slop.md`
   Remove generated noise, in-motion-work comments, larp, unhelpful boilerplate.
2. **Legacy / deprecated / fallback code** → `reference/passes/02-legacy-removal.md`
   Remove dead branches, deprecated APIs, fallback paths that no longer fall back to anything live.
3. **Unused code** → `reference/passes/03-unused-code.md`
   `knip`-class analysis: exports/files/deps that nothing imports.
4. **Circular dependencies** → `reference/passes/04-circular-deps.md`
   `madge`-class analysis: untangle import cycles.
5. **Weak types** → `reference/passes/05-weak-types.md`
   Replace `any` / `unknown` / `Object` / `dynamic` / `interface{}` with real types backed by research.
6. **Type consolidation** → `reference/passes/06-type-consolidation.md`
   Find duplicated / near-duplicated type definitions and unify.
7. **Defensive programming** → `reference/passes/07-defensive-programming.md`
   Remove try/catch and null-guards that don't handle a real input boundary.
8. **DRY / dedup** → `reference/passes/08-dry.md`
   Consolidate duplicated logic _only_ where it reduces complexity (not the other way).

## Tools

Each pass spec lists the tooling it expects (knip, ts-unused-exports, madge, jscpd, language-specific linters, etc.). The skill ships no scripts — orchestration happens in the calling agent runtime, which already has bash/edit/grep/etc.

## Reference

- `reference/protocol.md` — the 3-phase research/assess/implement protocol every pass follows
- `reference/pass-ordering.md` — why this order, and which passes can run in parallel
- `reference/passes/*.md` — one self-contained subagent prompt per pass
