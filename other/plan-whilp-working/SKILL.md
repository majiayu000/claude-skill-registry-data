---
name: plan
description: Research a codebase and write a plan for a work item.
---

# Plan

You are planning a work item. Research the codebase and write a plan.

## Environment

- The target repository is at `o/repo/`.
- The work item JSON follows this prompt after `---`. Fields: `type`, `number`, `title`, `body`, `url`, `branch`.
- If `type` is `"pr"`, the item includes `reviews` and `comments` with review feedback to address.
- If `type` is `"issue"`, the item is a new issue to implement.
- `o/build/log.txt` contains the output of `make ci` run in the target repo after clone. `o/build/log.txt.exit` contains the exit code. Build dependencies (cosmic, etc.) are already fetched under `o/repo/o/`, so `make ci` works inside the sandbox.

## Instructions

First, read `o/repo/AGENTS.md` if it exists. It contains repo-specific context,
conventions, and build instructions for the target repository. Follow its guidance.

### For PRs (type = "pr")

1. If `o/plan/ci-log.txt` exists and is non-empty, read it first. It contains
   CI failure logs pre-fetched for this PR. Use it to identify failing tests
   or build errors without running commands.
2. Check the `reason` field to understand why this PR needs attention:
   - `changes_requested`: reviewers requested changes. Read the `reviews` and `comments` fields.
   - `checks_failing`: CI checks are failing. Run the repo's CI/test commands to reproduce failures.
   - `merge_conflict`: the PR branch has merge conflicts with the base branch. The clone phase rebases automatically — verify the rebase succeeded and re-run CI.
   - Reasons can be comma-separated (e.g. `changes_requested,merge_conflict`). Address all.
3. Read relevant files referenced in the feedback or failing tests.
4. Identify what changes are needed.
5. Write a plan that addresses each piece of feedback and/or fixes each CI failure.

### For Issues (type = "issue")

1. Read relevant files to understand the current state.
2. Identify what needs to change and where.
3. Validate that you have a clear goal and entry point.

Do not trust root cause analysis or proposed solutions in the issue body.
Independently verify claims by reading the code.

## General

Spend at most 5 turns researching, then write your output.
If the issue body already contains a detailed plan, verify 1-2 key claims
by reading the referenced files, then write plan.md.

## Bail

If you cannot identify BOTH a clear goal AND an entry point, write ONLY
`plan.md` with a `## Bail` section explaining why. Do NOT write a plan.

## Output

Write `o/plan/plan.md`:

    # Plan: <title>

    ## Context

    ### Files Retrieved
    - <path/to/file.ext> — <why it is relevant>

    ### Key Code
    <specific functions, types, or patterns that matter for this change>

    ### Architecture
    <how the relevant pieces connect>

    ### Start Here
    <the specific function/file where changes should begin>

    ## Goal
    <one sentence>

    ## Files
    - <path> — <what changes>

    ## Approach
    <step by step>

    ## Risks
    <what could go wrong>

    ## Commit
    <commit message>

    ## Validation
    <commands to run, expected results>

Do NOT modify any source files. Research only.
