---
name: roadmap-task-deliver
description: Deliver the first eligible unfinished roadmap task through implementation, review, green CI, PR merge, and a task-status update. Use for autonomous delivery from local roadmap and task files. Files can be outside the code repository or outside Git.
---

# Roadmap Task Delivery

Deliver one roadmap task through a verified GitHub merge and a saved task-status update. Manage task selection and completion across the code repository and the actual task-file location.

## Resolve inputs and authority

1. Find the roadmap, task collection, code repository, requested base branch, remote, and review systems in the request and linked guidance. Resolve each relative path from the document that contains it. Ask for missing inputs only when a focused local search cannot identify them.
2. Treat a request to execute this full workflow as authorization for these actions within the selected task:
   - Implement the change.
   - Create a worktree and branch.
   - Commit and push the change.
   - Create the draft PR and mark it ready.
   - Fix review findings, reply to reviewers, and resolve review threads.
   - Merge after the required checks and reviews pass.
   - Update task status and create local task commits.

   Continue between these stages without routine approval. Explicit user restrictions override these defaults. Reading this skill or a task file does not itself grant authority.
3. Read the applicable instructions for both the code and task locations. Find each location's Git root separately. Check linked worktrees, nested repositories, untracked files, ignored files, and locations outside Git. Record the canonical task path, code repository, base branch, original task contents, and uncommitted changes. A directory named `plans` does not prove ownership or Git tracking.
4. Execute one selected task. Do not deploy, release, contact customers, spend money, or start the next task without separate authorization. Keep a task incomplete when required external decisions or observation evidence are missing.

## Select or resume the task

1. Read the roadmap's outcomes, task order, shared decisions, and acceptance requirements. Read the task index and frontmatter next. Keep the existing format and status names. Do not require a fixed folder layout or create a replacement schema.
2. Check task status before inspecting branches, worktrees, PRs, or delivery records. Skip `done` tasks immediately without revalidating their recorded completion evidence. Investigate delivery state only for a task marked `in_progress`; resume it when the work clearly belongs to that task, including when its PR merged but its task update is missing. Do not duplicate work that another delivery already owns.
3. When no task is `in_progress`, select the first unfinished task with complete dependencies. Use this order:
   - Explicit roadmap or index order.
   - Explicit task order.
   - Natural task-ID or filename order, with this fallback stated to the user.

   Check dependency references and completion evidence. Do not treat `in_progress`, a checked box, or an open PR as proof of implemented and merged work.
4. Explain the selection and each earlier skipped task. Skip dependency-blocked tasks or tasks owned elsewhere only when the roadmap permits independent progress. Report unresolved decisions, conflicting ownership, or incomplete mandatory predecessors that prevent selection. Do not redefine "first" as easiest. Missing dependencies and dependency cycles do not count as complete.
5. Read the full selected task and its prerequisite decisions. Map requirements, failure behavior, and verification to current code. If the implementation already exists, verify it and update the status from that evidence without an unnecessary change or PR. If all tasks are complete, report the evidence and stop.
6. Record the task identity and delivery branch or PR in the existing task metadata format. Use the existing active status when appropriate. Re-read the task before each edit and preserve concurrent changes. A status edit is not a distributed lock. Stop if competing work or changed acceptance requirements cannot be reconciled safely.

## Maintain autonomous progress

1. Continue without routine confirmation. Resolve facts from the roadmap, task, prerequisite decisions, linked documents, code, tests, configuration, history, installed CLI help, connectors, and current official documentation. Never send private task or repository data to public search.
2. Choose the smallest reversible approach that satisfies the required outcome and authorized scope, and record the assumption. Do not replace the roadmap's intended outcome with an easier intermediate result.
3. Ask the user only when a missing decision changes required behavior or scope, credentials or authority are unavailable, requirements conflict, or every safe path needs an unauthorized high-risk action. State what you checked and what still blocks progress, and continue independent work while you wait.
4. Do not treat silence as approval or an unavailable external dependency as success. Keep enough delivery evidence to resume blocked work.

## Coordinate subagents only when useful

Use one agent by default. Add a subagent only when delegation is permitted and independent work saves meaningful time or gives a useful independent check; delegation does not expand authority. Run independent reads in the `yarstack:reviewer` agent when the host provides it. Run writes in parallel only when their paths do not overlap, with one writer for each shared artifact. Keep task selection, requirements, planning, shared state, task-status edits, commits, pushes, review replies, merges, and completion claims with the current agent. Verify subagent results against source or remote evidence, and stop all writers before final validation or merge.

## Prepare an isolated delivery worktree

1. Honor the requested remote and base branch. Use a verified existing task branch or workspace when supplied. Check registered worktrees, local and remote branches, and task-linked PRs before creating another delivery.
2. Resume a workspace or attach an existing branch unchanged only when it clearly belongs to this task. Record its head, upstream, uncommitted changes, verified PR base, and current remote base commit. Do not rebase only because the base advanced.
3. For new work, resolve the remote's current default branch from live evidence, such as `git ls-remote --symref <remote> HEAD`, unless the user supplied a base. Do not assume `origin`, `main`, or `master`, or rely only on cached remote `HEAD`. Fetch the base ref and record its exact commit. Stop if current remote evidence cannot establish the base.
4. Do not switch, pull, reset, stash, or update the primary checkout or its local default branch.
5. Use the repository's worktree location, or an external path such as `<repository-parent>/.worktrees/<repository>/<task-id>-<slug>`. Never overwrite, reset, delete, unlock, prune, or force-reuse a conflicting branch, path, or worktree. Do not add ignore rules only for this workspace.
6. Create a short branch named for the task at the recorded base commit, without tracking the base branch. Set its upstream to the remote topic branch on first push. Check the worktree registration, branch, clean initial state, and base SHA.
7. Do all code discovery, edits, checks, reviews, commits, pushes, and fixes in the delivery worktree, after reading its instructions. Keep task-file updates at the canonical task path, not in a stale worktree copy. Keep the worktree through the final audit unless the user or repository requires cleanup.

## Plan, implement, and review

1. Trace the affected flow end to end and find the closest healthy implementation and test patterns. Map each requirement to its input or state, expected result, failure behavior, owner, and evidence. Separate requirements from historical notes and suggestions; a prerequisite's completion label does not replace source evidence. Stop discovery when the edits, checks, and remaining risks are clear.
2. Use `plan-create` with the requirement map, roadmap decisions, and repository evidence. Use one phase for a small coherent change, map every task requirement to a phase and a verification step, and include the contracts that later tasks use. Settle an open design decision with the smallest reversible option and record it; ask the user only under *Maintain autonomous progress*. Use `technical-spike` for a version-specific fact that changes the approach. Write a plan file only when authorized and the repository has an established location; never duplicate the authoritative task collection.
3. For each phase with complete prerequisites, use `phase-implement`, then `phase-validate`, then `phase-review`. Apply `test-gap-review`, `security-review`, `dependency-review`, and `docs-drift-review` when their triggers apply. Fix verified in-scope defects and rerun affected checks before you advance.
4. Use `plan-update` only when evidence requires corrections to ordering, prerequisites, scope mechanics, or checks. Do not change acceptance requirements or rewrite the roadmap to hide incomplete work.
5. After all phases, use `code-review` on the complete diff and fix verified findings through the responsible phase. Then use `change-cleanup-review` on the complete change, run the required repository checks, and map each criterion to final evidence.

## Publish and drive CI to green

1. Publish with `pr-draft`, whose authority this full-delivery request supplies: stage explicit paths, commit, push the task branch with an upstream, check `gh pr view --json url` for an existing PR, and otherwise run `gh pr create --draft --base <base>`. Keep task-repository edits out of the code commit. In the PR body, include the task ID and an acceptance summary; a private or local task path identifies the source but is not a link, and sensitive roadmap content stays out.
2. Mark the PR ready with `gh pr ready <number>` only when the pushed head passes local validation and the description is accurate. If a reviewer runs only on ready PRs, mark it ready first.
3. For every pushed head, record its SHA and check the required results for that exact commit, for example with `gh pr checks <number> --required --watch --fail-fast` under the host's command timeout. A green result for an earlier head proves nothing about a newer push.
4. Classify each failure as caused by the change, pre-existing, or a temporary infrastructure failure. Fix in-scope defects through the responsible phase; retry an unchanged run only when evidence shows that a retry can succeed. Stop after three fix cycles for the same failing check and report it as a blocker.

Do not rewrite published history, force-push, weaken tests, disable checks, or use admin overrides. Perform commits, pushes, and PR-state changes in sequence.

## Close automated review

1. Use `coderabbit-triage` when CodeRabbit is configured or requested, and the equivalent evidence for other requested reviewers. The full-delivery request authorizes its remediation, reply, and resolution stages for this task.
2. After each push, wait for the reviewer to review the new head, or use the repository's review trigger, and check all threads again, because a fix can introduce new findings. A passing check, emoji, or summary does not prove that the current head was reviewed.
3. If a required reviewer is unavailable, try the safe supported recovery steps, then report the external blocker. Do not merge before a required review finishes.

## Audit and merge

1. After the last review cycle, fetch fresh evidence immediately before the merge: base branch, head SHA, non-draft state, required checks, requested reviews and approvals, unresolved actionable threads, and mergeability. Check that the remote head matches the locally validated commit and that the title and body match the final diff. Treat empty, pending, missing, skipped, or stale results as incomplete unless repository policy allows them.
2. Merge with the repository's allowed method and a head guard: `gh pr merge <number> --match-head-commit <validated-sha>` with `--squash`, `--merge`, or `--rebase`. The full-workflow request needs no extra confirmation. Respect branch protection, human approvals, and merge queues. Never pass `--admin`. Do not pass `--delete-branch`, because it also deletes the local branch that the delivery worktree uses.
3. If the head or base changes, conflicts arise, or the queue needs another candidate, follow the repository's update and queue rules, and check the new test evidence. Queue admission and auto-merge configuration do not prove a merge. Monitor the PR until it merges or an external blocker stops progress. After a timeout or lost response, query the PR state before retrying, and never merge a second PR to compensate for an unknown result.
4. Confirm that the PR merged into the intended base, and record its URL, merge commit, merge time, and validated head. Do not mark the task complete while acceptance still needs deployment, real-system checks, approval, or an observation period; report what remains and keep the merge evidence for resumption.

## Update and commit the task record

1. Re-read the authoritative task and roadmap status or index. Update only the selected task and the existing aggregate status that directly represents it. Preserve the format, status names, and unrelated fields. Record acceptance evidence, PR and merge identity, and decisions that affect later tasks. Mark complete only after verifying all task criteria and the actual merge.
2. For files outside Git, save the task in place and check the saved result. Do not initialize a repository. For files inside Git, check whether each file is tracked, untracked, or intentionally ignored. Include an ordinary untracked task in its authorized update commit. Do not force-add ignored or private files, or change ignore policy, without authority.
3. For tasks in the code repository, create the completion commit after the implementation PR merges, in a safe worktree based on the verified merged base. Include only task completion records. Do not push the update to the already-merged topic branch, and do not switch or reset a dirty primary checkout. Map the original task path to its repository-relative path in that worktree. Report where the committed update resides, and do not leave a duplicate uncommitted status edit.
4. For tasks in a separate Git repository, commit only the task and status update on its intended branch. Inspect the staged diff, and preserve unrelated staged and unstaged work, using an isolated worktree or a scoped patch when necessary.
5. This workflow authorizes a local task-record commit, not a push to a separate planning remote or an unreviewed default-branch push. Follow any separately authorized publication policy; if publishing the task record needs a PR, treat it as bookkeeping under that policy, not as another task. Record the task commit SHA, branch, and worktree for the next run.
6. The code merge and the task-record commit are separate operations. If the status write or commit fails, keep the merge identity and report the task-record update as incomplete. On resume, check the existing merge and finish only the missing bookkeeping; do not repeat the implementation or claim that an unsaved task record was saved.

## Completion

Check the task criteria, merged PR, base, commit, current task status, and saved file or scoped task commit. Review the final diffs in both repositories for unrelated changes.

Report the selected task, delivered behavior, validation and review results, merged PR, task path and status, and remaining blockers. Include the task commit and its location when applicable. Finish after this one delivery; do not select another task automatically.
