---
name: b-commit
description: >
  Analyze tracked, staged, and untracked working-tree changes; select
  cohesive commits after an explicit user request, then stage and create
  them on the current branch without a second approval prompt or pushing.
disable-model-invocation: true
metadata:
  phase: Ship
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-commit/prompt.md. Edit those sources, not this file. -->

# b-commit

Create cohesive commits from an explicit user request, or draft one message for an existing staged change, without pushing.

## When to use

- The user wants working-tree changes split, staged, and committed on the current branch.
- The user wants a commit message only for one cohesive staged change.
- The user wants PR copy for staged changes and needs a clear next step.

## When NOT to use

- The user wants PR copy for already-created commits -> use **b-pr-summary**. (PR copy for staged changes stays here: step 1 returns the commit-first blocker.)
- The changes cannot be grouped confidently -> use **b-plan**.
- The user wants a review before committing -> use **b-review**.

## Tool guidance

- Native `read`/`edit` for applicable repository commit rules and required preparation; `bash` for repository-mandated commit-time checks, `rtk git status --short`, metadata-only Git path lists, targeted safe-path diffs, exact staging, and commit creation.

## Commit boundary

The main session owns `b-commit`. An explicit user request to commit authorizes the smallest confident cohesive plan. Do not ask for a second approval prompt. Inspect the tracked and relevant untracked/derived candidate, preserve any user-curated index, and assign exact paths and messages before staging. Do not rerun implementation checks or independently revalidate or self-authorize an unchanged candidate solely to commit it. Run only checks explicitly required by repository rules at commit time; do not use `b-commit` to fill in missing change-phase verification. If verification evidence is unavailable, report that gap without inventing results. Do not invoke **b-reviewer** or require a prior review disposition solely to stage or commit, even for multiple groups or a pre-existing staged set.

- Before staging, confirm the selected paths and index still match the inspected candidate. If the candidate changes—including relevant untracked content or repository preparation—pause rather than commit under an obsolete plan; return it to the change-producing phase for verification and any applicable review. The original commit request remains authorization to resume once the changed candidate is verified and the plan is reconfirmed. Unexpected paths, unresolved findings, or uncertain path assignment block committing. Never regroup silently or push.

## Steps

1. If the user asks for PR copy for staged changes, return `BLOCKED: commit staged changes before generating PR copy` and stop. Do not inspect commit history or stage or commit changes.
2. If the user asks only for a commit message, list staged paths with `rtk git diff --cached --name-only`, then inspect only the targeted staged diff for non-protected paths. Block if it is empty, protected, or mixes unrelated concerns; otherwise apply step 7, output the message, and stop without staging or committing.
3. Using Bash, run `rtk git status --short` and metadata-only path lists for staged and unstaged changes. Classify protected paths before reading any content; inspect untracked files only when their paths are not likely-secret files.
4. Read diffs only for explicit non-protected paths, using `rtk git diff -- <paths>` or `rtk git diff --cached -- <paths>`. Record the initial index and working-tree snapshot. Do not read, stage, or commit likely-secret files without explicit permission.
5. Select the smallest set of cohesive commit groups. Treat a pre-existing staged set as user-curated: preserve it as one group and do not reset or reorganize it.
6. Block if a group mixes unrelated concerns, a protected file needs permission, or a file cannot be assigned confidently. Read applicable repository commit rules and perform required preparation only for this user-authorized commit. If preparation changes the candidate, pause for change-phase verification rather than run a second validation gate inside `b-commit`; do not silently add prepared files to a user-curated staged group. Run any repository-mandated commit-time checks on the final candidate; a failed mandated check blocks committing and must be reported. Message-only and staged PR-copy requests never reach this preparation step.
7. For each group, choose the narrowest accurate type: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, or `style`; write an imperative subject of at most 50 characters that starts with a lowercase letter (`docs: adopt native API shapes`, never `docs: Adopt native API shapes`) and has no trailing punctuation. The message is the subject line only: no body, description, bullets, footers, or trailers (including `Co-authored-by`).
8. Record the groups, exact file paths, and commit messages in the execution response, then continue without a second approval prompt; the explicit user commit request is sufficient authorization. If the request did not explicitly authorize committing, stop.
9. Apply the commit boundary above to the complete candidate and plan. Before staging, confirm the selected paths and index are unchanged. Stage only the selected paths for each unstaged group; do not use broad staging commands that can capture unrelated files.
10. Reinspect each staged group immediately before committing with a targeted non-protected-path diff. Create its commit with a single `-m "<type>: <subject>"` and no other `-m`, `-F`, or editor body on the current branch, then continue to the next approved group. Stop on the first Git error; do not amend, reset, push, or retry by changing history.
11. Report commit hashes, messages, remaining changes, and any blockers. Recommend `b-pr-summary <commit-count>` for PR copy.

## Output format

Execution plan:

```markdown
Commit plan:
1. <type>: <subject>
   Files: <paths>

The explicit user commit request authorizes execution; no second approval prompt is required.
```

For a message-only request:

```markdown
Commit message:
<type>: <subject>
```

After completion:

```markdown
Created commits:
- <short-hash> <type>: <subject>

Remaining changes:
- <paths or None>
```

When blocked, state the specific uncommitted concern without exposing protected file contents. For staged PR-copy requests, output exactly:

```text
BLOCKED: commit staged changes before generating PR copy
```

## Rules

- Preserve unrelated worktree changes and the user-curated index.
- Evidence-only, subject-only messages: never add a commit body or description; do not invent behavior, verification, or impact.
- Require an explicit user commit request, but do not ask for a second approval after it; do not push or create a PR.
- Commit only the inspected candidate and selected paths; a changed candidate returns to the change-producing phase rather than receiving commit-time validation.
- Never use `git add -A`, `git add .`, `git commit --amend`, reset, or history-rewriting commands.
