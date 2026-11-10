---
name: behavior-specification
description: Use to discover and specify user-facing behavior, domain rules, external contracts, and acceptance conditions, including specification work without code. Do not use for internal technical fixes that preserve agreed contracts or design limited to implementation methods.
---

# Discover and specify behavior

Organize results promised to users or external systems before deciding how to implement them. `docs/` below refers to the working repository.

## From purpose to acceptance conditions

1. Check existing stories, glossaries, features, API specifications, and agreed rules, and reuse authoritative sources. For new features, describe who can do what, in which situation, after completion. Connect technical fixes and cleanup to existing purposes and expected results.
2. Read [Shared understanding and feature documents](references/behavior.md), and separate rules, meaningful concrete examples, and unanswered questions using BDD, ATDD, and Example Mapping perspectives. Do not settle unagreed business decisions through agreement between AIs or technical prototypes.
3. Define acceptance conditions before the corresponding implementation, and show which normal, boundary, or failure results should be observed. Do not mix internal implementation procedures into business specifications; preserve externally promised responses, saved results, and notifications as contracts.
4. For domain-rule additions or changes, save `docs/behavior/<feature-name>.feature.md` before implementation, even for agreed rules. Do not unnecessarily rewrite correct existing specifications. For external technical contracts, prioritize existing authoritative API specifications or similar sources; when a shared specification is needed, features may be used with explicit readers and observable results.

Save feature documents using the metadata and repository-language Markdown with Gherkin in [Shared specification format](references/behavior.md#feature-document-format). Do not uniformly require meetings, participant counts, or automation tools.

## Handoff and completion

- For specification-only requests without code changes, present stories, concrete examples, acceptance conditions, and unanswered questions, then stop. Do not implicitly start Issue creation, publication, or TDD.
- When asked to create or update an Issue plan, check publication permission and reuse any existing record. Save its purpose, scope, success conditions, and checking method; retrieve the body, check agreement and display, and present its URL. Planning-only requests stop there without saving repository documents or implementing.
- For approved repository feature documents, reuse the saved and verified Issue plan and execution approval, or save and verify the missing plan first. Check repository instructions, current diffs/worktrees, and main health, protecting other sessions' work before preparing a task branch. Proceed through edits, commits, push, a PR, required CI, ordinary latest-HEAD review, permitted squash or merge-commit integration, actual-main checks, synchronization, and task-branch cleanup. Preserve the final PR title/body verbatim; do not bypass protections or use rebase merging.
- Confirm permission before publishing unpublished material, and confirm changes to purpose, acceptance conditions, external impact, or authority before dependent work. Retain approval for adjustments within the same scope. In Plan Mode, read-only environments, or when necessary access is unavailable, present drafts and incomplete scope without claiming saving or implementation occurred.
- When code changes are requested, carry agreed specifications, concrete examples, unanswered questions, and their mapping to tests into the approved implementation. Saving specifications alone does not approve implementation. Retain existing implementation approval without asking for the same approval again.
