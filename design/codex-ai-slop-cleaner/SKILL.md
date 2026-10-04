---
name: codex-ai-slop-cleaner
description: Use when working code or generated content feels AI-bloated, noisy, repetitive, over-abstracted, fallback-heavy, generic, visually clichéd, weakly tested, or slop-like; clean behavior-preservingly with scoped regression checks, smell-by-smell passes, minimal diffs, and evidence.
---

# Codex AI Slop Cleaner

Clean AI-generated slop without changing intended behavior. This is the native Codex adaptation of OMX `$ai-slop-cleaner`: regression checks first, bounded scope, smell-by-smell cleanup, fallback classification, and evidence-dense reporting.

## Contract

- Preserve behavior unless the user explicitly asks to change it.
- Keep scope bounded to requested files or the current workflow's changed files.
- Do not perform broad rewrites, architecture pivots, or dependency additions without approval.
- Protect user work and unrelated dirty files.
- Verify after each meaningful cleanup pass.

## Workflow

1. Lock behavior with targeted tests, smoke checks, or visual evidence.
2. Make a cleanup plan naming smells and file scope.
3. Classify fallback-like code before editing:
   - Masking slop: swallowed errors, silent defaults, untested alternate paths, broad bypasses.
   - Grounded fallback: scoped compatibility/fail-safe boundary with rationale and tests.
4. Execute one smell category at a time: dead code, duplication, needless wrappers, naming/error handling, test reinforcement, or UI/design slop.
5. Verify after each pass.
6. Report changed files, simplifications, tests, fallback decisions, and remaining risks.

## Slop Signals

- "temporary" code that became permanent
- fallback branches that hide errors
- generic wrappers around one call site
- repeated content scaffolding or duplicated helpers
- comments that narrate obvious code
- over-engineered option objects or config layers
- default AI palettes, gratuitous gradients, emoji badges, card grids, and filler UI copy without product reason

## Output Shape

- Scope
- Behavior lock
- Cleanup plan
- Passes completed
- Verification
- Changed files
- Fallback review
- Remaining risks

## References

Read `references/slop-checklist.html` for smell categories and cleanup gates.
