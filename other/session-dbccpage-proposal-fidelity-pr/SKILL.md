---
name: session
description: "Use when merging conflicted cppms-fallback stacks. Tree-diff before merge, land unique changes, keep main governance."

operad_source_colours: ["State"]
operad_target_colour: "State"
operad_arity: 1
operad_residual: "unknown"
---

# session

**AuthorityEffect:** `None`. Enforces claim discipline (`[user_global]`), lowercase snake_case file naming, and markdown de-linting.

## invariance_level: Tier 8

## Overview

* **Date Proposed:** 2026-07-31
* **Source Session:** auto-oe-autop after RGB-W45 + PR #1639/#1642/#1652–#1656 conflict resolution
* **Confidence Level:** **HIGH** (applied as skill *edits*)
* **Category / Family:** `devops` / `git` / `governance` ext
* **Description:** Durable law for conflicted `cppms-fallback-*` stacks: tree-diff BEFORE merge; classify ONLY_PR / ONLY_MAIN / M_diff; selective land unique capital from clean worktree; keep main governance supersets; reject Wave/RGB/root-sprints deletes; empty resolve → close already-landed; land tip once then close supersedes. Applied to `/goo-commit-isolation-guard` v1.1.0, `/0-oe-commit` v1.3.1, `/github` session convention.
* **Implementation Status:** `APPLIED_TO_EXISTING` — no new admission
* **ZeroRel note:** Complements Entry 0008 isolation guard; does not replace human review of packaging PRs.

---

---

## Instructions

1. Execute skill tasks under Council governance.
2. Enforce zero markdown lint errors and lowercase snake_case file naming.

## Mandatory De-Linting & Encoding Cleanliness (`RULE_MARKDOWN_DELINTING_001`)

Every file created or modified during the execution of this skill MUST be de-linted prior to turn completion. Run `/techne-docs-lint-hunter-killer` or `npx markdownlint-cli --fix` to verify **0 linter errors and 0 linter warnings**, and ensure no CP437/Windows-1252 Mojibake character artifacts remain (`RULE_UTF8_MOJIBAKE_CLEANLINESS_001`).
