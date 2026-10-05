---
name: oncokb-ai-code-review
description: Run an AI-assisted PR review that validates issue linkage, local quality gates, manageable scope, and review comments.
---

## Scope

- Use for end-to-end AI code review on an existing PR.
- Use this skill when the user asks for an AI review workflow, not just a single lint/test command.
- Keep the review auditable: report commands run, outcomes, and the final PR URL.
- This skill does not create or update pull requests. Use `oncokb-make-pull-request` for PR creation/update.

## Required skill chain

Follow this order and do not skip steps:

1. Confirm target PR context
   - `oncokb-make-pull-request` first if a PR does not exist yet.
2. (Optional Ask User First) Local validation (format, lint, tests)
3. Manageability and scope review
4. `oncokb-database-review`
5. `oncokb-logging-review`
6. `oncokb-html-accessibility-reference`
7. `oncokb-datastar-review` (when Datastar usage is present)
8. Repo-specific code-review skill discovery
9. PR review comments prefixed with `[ai-generated]`
10. `oncokb-code-comments-standards`
11. `oncokb-test-planning-and-coverage`

## Workflow

1. Get the related GitHub issue first.
   - Start by invoking the `oncokb-github-issues` skill.
   - Ask for the issue associated with the change, or create/find it via that skill workflow.
   - Do not proceed to PR work without an issue link or issue ID.
   - Completion criterion: issue URL/ID is confirmed and ready to reference in the PR.

2. Run local quality gates.
   - Run all project formatting, linting, and test commands that apply to the changed code.
   - Discover commands from the project environment (for example package scripts, Make targets, Gradle/Maven tasks, or other repo-standard tooling).
   - If any command fails, stop and report failures before proceeding with PR review comments.
   - Completion criterion: formatting, lint, and tests all complete with no errors.

3. Check that the change is manageable.
   - Verify the change is atomic: one focused feature/fix/refactor and no unrelated scope.
   - Verify only relevant files are included for that purpose.
   - Measure diff size against soft limits:
     - under 500 changed lines of source code
     - under 20 changed source files
   - If soft limits are exceeded or scope is mixed, recommend a PR stack split plan.
   - Completion criterion: reviewer can clearly see either (a) manageable scope or (b) a concrete split recommendation.

4. Confirm target PR context.
   - Ask for the PR URL to review.
   - If a PR does not exist yet, stop this skill and hand off to `oncokb-make-pull-request` first.
   - Do not create or update PR metadata from this skill.
   - Completion criterion: PR URL is confirmed and accessible for review/commenting.

5. Review database access risks.
   - Invoke `oncokb-database-review` and assess changed DB access for N+1 query risks, SQL injection risks, and deterministic pagination ordering.
   - If paging exists, require `ORDER BY` to include a unique tie-breaker (for example `id` or another unique key).
   - Add `[ai-generated]` review comments for any blockers or high-value follow-ups from the database review.
   - Completion criterion: database-review findings are documented and actionable.

6. Review logging quality and severity.
   - Invoke `oncokb-logging-review` and assess changed logging for correct `TRACE`/`DEBUG`/`INFO`/`WARN`/`ERROR`/`FATAL` usage.
   - Require level labels on all changed application logs.
   - Ensure changed error/fatal events are logged and intentionally ignored errors are logged as `WARN`.
   - Add `[ai-generated]` review comments for blockers and high-value `INFO` suggestions from the logging review.
   - Completion criterion: logging-review findings are documented and actionable.

7. Review HTML accessibility basics.
   - Invoke `oncokb-html-accessibility-reference` and use its references to review changed HTML/UI markup.
   - Check semantic HTML usage, accessible form labeling, heading/landmark structure, keyboard access, and ARIA misuse.
   - Add `[ai-generated]` review comments for accessibility blockers or high-value follow-ups.
   - Completion criterion: accessibility findings are documented and actionable.

8. Review Datastar architecture and semantics (conditional).
   - If changed files contain Datastar usage (`data-*` Datastar attributes, `@get/@post/...` actions, Datastar SSE patch patterns, Datastar plugin code), invoke `oncokb-datastar-review`.
   - Use its Tao-based checks to assess state placement, patch strategy, signal usage, loading/optimistic behavior, and accessibility implications.
   - Add `[ai-generated]` review comments for Datastar blockers or high-value follow-ups.
   - Completion criterion: when Datastar usage exists, Datastar-review findings are documented and actionable.

9. Check for additional repo-specific code review skills.
   - Inspect the current repository for any additional skills intended for code review (for example under `skills/` and referenced in local agent docs).
   - Identify skills not already covered by this chain that are applicable to the current PR.
   - Invoke each applicable additional review skill and capture actionable findings.
   - Add `[ai-generated]` review comments for blockers or high-value follow-ups from those skills.
   - Completion criterion: repo-specific applicable review skills are either run with findings recorded, or explicitly reported as none found.

10. Add AI review comments on the PR.
   - Post review comments that begin with `[ai-generated]`.
   - Keep comments specific, actionable, and tied to files/lines or clear review concerns.
   - Do not post vague praise-only comments.
   - Completion criterion: PR contains useful `[ai-generated]` review comments or an explicit no-issues-found note.

11. Review code comments quality.
   - Invoke `oncokb-code-comments-standards` and assess whether comments explain non-obvious logic, invariants, and decisions.
   - Add `[ai-generated]` PR comments for missing or weak comments in non-trivial areas.
   - Completion criterion: comment-quality findings are documented in the PR.

12. Review testing adequacy.
   - Invoke `oncokb-test-planning-and-coverage` and assess whether tests are sufficient for changed behavior and risk.
   - Add `[ai-generated]` PR comments for missing high-value tests or coverage gaps.
   - Completion criterion: test-coverage findings are documented in the PR.

## Output requirements

- Report:
  - issue reference used
  - formatting/lint/test commands run and outcomes
  - scope metrics (source lines changed, source files changed)
  - manageable vs needs-split decision
  - database review findings (N+1, injection, pagination determinism, and key follow-ups)
  - logging review findings (level correctness, label coverage, error/fatal observability, ignored-error WARN logging, and INFO suggestions)
  - HTML accessibility findings (semantic structure, labels, keyboard access, ARIA usage, and follow-ups)
  - Datastar review findings when applicable (Tao alignment, state placement, patch strategy, signal usage, and reliability checks)
  - additional repo-specific review skills found and findings (or explicit none-found)
  - PR URL
  - count and summary of `[ai-generated]` comments posted
- If work is blocked (permissions, failing checks, missing issue), report the exact blocker and the next command or action needed.

## Quality bar

- Never claim a command passed unless it was actually run.
- Never perform PR review work without an issue reference and a target PR URL.
- Treat 500 lines and 20 source files as soft limits: recommend PR stacking when exceeded.
- Run `oncokb-datastar-review` whenever Datastar usage appears in changed code.
- Do not skip applicable repo-specific code review skills discovered in the current repository.
- Keep all automated review comments clearly marked with `[ai-generated]` at the start.
