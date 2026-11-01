---
name: pr
description: Creates a pull request for the current branch.
unsandboxed: true
---

When asked to create a pull request, follow these steps:

## Phase 1: Pre-flight checks

1. Run `git status`. If any of the following conditions apply, stop and report the errors:

   - There are unstaged changes
   - There are untracked files
   - The current branch is the default branch (`main`)

2. Check if this is a stacked PR:

   - Run `git merge-base main HEAD` to find the common ancestor with main
   - Run `git log --oneline <merge-base>..HEAD` to see commits since diverging from main
   - Check if any parent commits are on another feature branch (not main)
   - If so, run `gh pr list --head <parent-branch>` to check if that branch has an open PR
   - If a parent branch has an open PR, this is a **stacked PR**

3. Run `git log main..HEAD --oneline` to see the commit history.

4. Get the diff for the review:

   - If this is a **stacked PR**, run `git diff <parent-branch>...HEAD` to scope the diff to only this branch's changes.
   - Otherwise, run `git diff main...HEAD`.

5. Run the prose pass over the comments in that diff: Skill tool with skill="prose-pass". It runs here, before review, so that anything it changes is reviewed in Phase 2. If it changes files, run the checks (`lint-build-test`), commit with the message "docs: Trim comments", push, and re-run step 4 so the review sees the trimmed diff.

## Phase 2: Automated PR review (parallel subagents)

**MANDATORY — DO NOT SKIP.** This phase must run before any PR is created, regardless of how "simple", "mechanical", or "well-tested" the changes appear. Subtle bugs (e.g., semantic mismatches in API migrations) hide in exactly the changes that seem safe to skip. The only exception is docs-only changes as described below.

Before creating the PR, analyze the diff to decide **which review subagents to launch**. Not every PR needs every reviewer.

### Triage: classify the change

Categorize each changed file, then pick subagents based on which categories are present. A file belongs to exactly one category — evaluate in this order (first match wins):

1. **docs**: `.md`, `.txt`, `CHANGELOG`, `LICENSE`, `docs/`, `.claude/`
2. **ci**: `.github/workflows/`, `.github/actions/` — these often contain shell scripts with non-trivial logic
3. **config**: `.json` (not `package.json`), `.yml`, `.yaml`, `oxlint.config.*`, `.oxfmtrc*`, `tsconfig*`, `Dockerfile`, `.editorconfig`, `.gitignore`, `.gitattributes`, `.nvmrc`, `.yarnrc*`
4. **test**: files matching `*.test.ts`, `*.spec.ts`, or under `test/` directories
5. **code**: everything else (`.ts`, `.js`, `.mjs`, `.cjs`, `package.json`, etc.)

Then decide which subagents to launch:

- If **only docs** files changed: **skip the entire review phase** and go straight to Phase 3.
- Otherwise, select subagents based on which categories are present:
  - **ci** present → launch **Subagent 1 (Correctness)** (review shell logic, conditional expressions, job dependency chains)
  - **config** or **test** present → launch **Subagent 2 (Style)**
  - **test** present → also launch **Subagent 4 (Tests)**
  - **code** present → launch **Subagent 1 (Correctness)** and **Subagent 2 (Style)**
  - **code** present → also launch **Subagent 4 (Tests)**
  - **code** present and diff touches security-sensitive areas (network/HTTP, user input, auth, crypto, `eval`/`Function`, capability passing, `harden()`/SES) → also launch **Subagent 3 (Security)**

### Subagent 1: Correctness & Logic

Prompt the agent to:

- Review the diff for logical errors, off-by-one mistakes, race conditions, and incorrect assumptions
- Check that error handling is adequate at system boundaries
- Verify that new code paths are reachable and dead code hasn't been introduced
- Flag any behavior changes that aren't covered by tests

### Subagent 2: Style & Conventions

Prompt the agent to:

- Check adherence to the project's CLAUDE.md conventions (TypeScript types over interfaces, no `any`, no `enum`, kebab-case files, `@metamask/superstruct` for runtime types, options bags for 3+ args, `harden()` usage, etc.)
- Check test conventions (no "should", `toStrictEqual` for full objects, `it.each` for parameterized tests, concise verb-form titles)
- Flag unnecessary complexity, over-engineering, or missing `harden()` calls

### Subagent 3: Security & Performance

Prompt the agent to:

- Look for OWASP top-10 vulnerabilities (injection, XSS, etc.)
- Check for capability leaks in the ocap model (unhardened objects, leaked references)
- Identify performance issues (unnecessary allocations in hot paths, missing early returns, O(n^2) patterns)
- Verify that lockdown/SES compatibility isn't broken (no ambient authority, no forbidden globals)

### Subagent 4: Test Coverage

Prompt the agent to:

- Identify new or changed logic that lacks corresponding test coverage
- Check that edge cases and error paths are tested
- Verify tests are co-located correctly per project conventions
- Flag any test anti-patterns (global state, missing cleanup, overly broad mocks)

## Phase 3: Review summary

If the review phase was skipped (docs-only), proceed directly to Phase 4.

Otherwise, after all launched subagents complete:

1. Compile findings into a **Review Summary** with sections for each subagent that ran.
2. Classify each finding as one of:
   - **blocker** - Must fix before merging
   - **suggestion** - Should consider fixing
   - **nit** - Minor, optional improvement
3. If there are **blockers**, present them to the user and ask whether to:
   - Fix the blockers automatically, then re-review
   - Proceed with PR creation anyway
   - Abort
4. If there are no blockers, briefly summarize the findings and proceed.

## Phase 4: Create the PR

1. Draft the PR body, then run the prose pass over the body: Skill tool with skill="prose-pass". The comments were already swept in Phase 1; this pass is for the body only.

2. Run `gh pr create` to create a pull request. The PR body should include:

   - A brief narrative description of the PR
   - A summary of the changes (bullet points)
   - A brief description of how the code is tested (narrative, not a checklist)

   **If this is a stacked PR**, add `--draft` to create it as a draft PR.

3. Note the PR number from the created PR URL — it is needed for changelog entries. Proceed to Phase 5 before presenting results to the user.

## Phase 5: Update changelogs

**MANDATORY — DO NOT SKIP.** Analyze the diff and determine whether any changes are consumer-facing (i.e., affect the behavior or API of a published or private package).

- **If there are NO consumer-facing changes** (e.g., docs-only, CI, tooling, skill definitions, dev scripts): add the `no-changelog` label to the PR via `gh pr edit <number> --add-label no-changelog` and skip the rest of this phase.
- **If there ARE consumer-facing changes**: update changelogs as described below.

Read the instructions in [`docs/contributing/updating-changelogs.md`](../../../docs/contributing/updating-changelogs.md) and follow them **to the letter**. In particular:

- **Think from the consumer's perspective.** A changelog is not a git history. For each affected package, ask: "What changed for someone who depends on this package?" Describe changes in natural language; do not simply reuse commit messages.
- **Combine like changes.** If multiple commits contribute to a single logical change within one package, write one changelog entry — not one per commit.
- **Split disparate changes.** If one commit touches unrelated concerns in a single package, write separate entries.
- **Link the PR.** Use the PR number from Phase 4 in each entry (e.g. `([#123](https://github.com/.../pull/123))`).
- **Keep entries short.** Run the prose pass over the drafted entries, for changelogs only: Skill tool with skill="prose-pass", args="changelogs".

Commit the changelog updates to the current branch with the message "docs: Update changelogs" and push.

## Done

Present the PR URL and any relevant information to the user. If a review was performed, include the review summary.
