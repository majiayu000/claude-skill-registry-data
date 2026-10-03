---
name: deep-review
description: Use when asked for a thorough, deep, or multi-angle review of a branch, PR, or recent changes — or when a diff touches error handling, catch blocks, fallbacks, new types, or test coverage and deserves more than a quick single pass.
---

# Deep Review

## Overview

Single entry point for review work. The built-in commands do the core pass;
this skill adds specialist lenses that used to live in separate plugins
(pr-review-toolkit, code-review, audit, code-simplifier). Those plugins are
disabled — if any are still visible, prefer this skill over them.

## Routing

| Ask | Use |
|-----|-----|
| Quick correctness pass on working diff | `/code-review` (low/medium effort) |
| Reuse / simplification / efficiency cleanup | `/simplify` |
| Security-focused review | `/security-review` |
| Review a GitHub PR | `/review <PR#>` |
| Exhaustive multi-agent cloud review | `/code-review ultra` (user-triggered, billed) |
| Deep local review with specialist lenses | this skill, below |

## Deep pass

1. Scope the diff (`git diff main...` or the PR) and pick only the lenses
   that match what changed. Skip lenses with no matching surface.
2. Spawn one general-purpose subagent per lens, in parallel, on `opus`
   (review and verification are reasoning-heavy — see the model-routing rule
   in CLAUDE.md). Each returns findings as `file:line — severity
   (critical/major/minor) — one-sentence defect — failure scenario`.
3. Verify each finding against the actual code before reporting (drop
   anything you cannot reproduce from the source). Dedupe across lenses.
4. Report findings ranked most-severe first. Do not apply fixes unless asked.

## Lenses

**silent-failures** — catch blocks that swallow errors; broad catches hiding
unrelated failures; fallbacks or default values that mask a failed operation;
errors logged then execution continues with no user-visible feedback; mock or
stub behavior reachable in production paths.

**comment-accuracy** — comments or docstrings that contradict the code; stale
references to renamed symbols; comments that narrate what the next line does
or justify the change to a reviewer instead of stating a real constraint.

**type-design** — invariants left unenforced that the type system could
express; leaked internals that should be encapsulated; primitive obsession
where a domain type would prevent misuse; impossible states left representable.

**test-coverage** — new logic without tests; missing edge/error-path cases;
tests asserting implementation details instead of behavior; tests that cannot
fail.

## Common mistakes

- Running every lens on every diff — scope to what changed.
- Reporting subagent findings unverified — plausible-but-wrong findings are
  worse than none.
- Turning the review into a fix session — findings first; fix only on request.
