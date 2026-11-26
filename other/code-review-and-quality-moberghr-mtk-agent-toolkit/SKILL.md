---
name: code-review-and-quality
description: Review a PR (pull request), branch or diff outside implement — runs the compliance, silent-failure, test and architecture lanes with full lane accounting.
type: skill
effort: max
context: fork
user-invocable: false
---

# Code Review And Quality

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

## Overview

Adversarial review of a PR or diff that did not come through `implement` (implement Phase 4 reads the reference directly). This skill is read-only except for workflow-artifact recording.

## When To Use

- Reviewing a PR, branch, or local diff before merge, outside the implement loop

## Workflow

1. Get the diff (`gh pr diff <n>` or `git diff <base>...HEAD`) and the changed-file set; exclude files that were already dirty before the change.
2. Read `.claude/references/implement-review-lanes.md` and pick lanes from its **Outside implement** column: `compliance-reviewer` always; `silent-failure-hunter` when the trigger regex matches; `test-reviewer` when public behavior changed; `architecture-reviewer` on a new slice, boundary, or cross-project call.
3. Dispatch them per **Dispatch rules** (inline when the Agent tool is unavailable) following the **Review protocol** (scripts via `$MTK_ROOT`; no workflow artifact here, so skip review-input binding and say the review is unbound), run the **Defect-class sweep** on every confirmed finding, and apply **Lane accounting** before aggregating. `finding-verifier` is implement-only (HIGH/MAX).
4. Emit the findings table and fenced JSON per `.claude/references/review-finding-schema.md`, with the lane roster. Write the push receipt only as the protocol's **Receipt** step qualifies (its `--check` clause is implement-only).

## Verification

- [ ] Every dispatched lane is accounted for; the verdict is not PASS while any lane abstained or returned nothing
- [ ] Findings follow the schema; an empty `findings[]` carries `below_threshold_rationale`
