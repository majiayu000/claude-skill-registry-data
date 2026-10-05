---
name: do-issue-solo
description: Work on a GitHub issue end-to-end autonomously, only pausing when blocked or when clarification is needed.
argument-hint: issue number (e.g., 123)
user-invocable: true
disable-model-invocation: false
---

# Work on GitHub Issue (Autonomous)

Work on GitHub issue `$ARGUMENTS` autonomously, coordinating safely
with any other Maverick instance that might also hold a claim on this
issue. Follow every phase in order. Only pause to ask the user when you
are blocked or need clarification.

## Preflight (mandatory)

Preflight output, captured when this skill was invoked (dynamic-content
pilot — the command ran before you read this):

!`uv run maverick preflight do-issue-solo 2>&1 && echo PREFLIGHT_OK`

- Ends with `PREFLIGHT_OK` → prerequisites are met; proceed.
- Shows an error → halt and report the output verbatim to the user. Do
  not proceed, do not work around missing prerequisites.
- Empty, or shows the literal command text (dynamic skill content is
  disabled via `disableSkillShellExecution`) → run it manually first and
  apply the same rules:

  ```bash
  uv run maverick preflight do-issue-solo
  ```

The check verifies: the project is initialised, the Maverick GitHub
App is configured (`maverick gh-app status` reports `configured: true`),
and required tools (`gh`, `git`, `uv`) are on PATH.

## Before You Begin

If `$ARGUMENTS` is empty or not a valid issue number, ask the user
for the issue number before proceeding.

Determine the repo (via `gh repo view --json nameWithOwner`) — you will
pass it to every `maverick coord` command below.

PR code review runs locally during Phase 9 as the
`agent-code-reviewer` subagent — its binary PASS/FAIL
verdict is the gate. Some projects also opt into a CI-side re-run via
`mav-bp-remote-code-review` (independent verification for
multi-machine fleets or audit needs); when present it adds a status
check the auto-merge in Phase 10 will wait on, but its absence is not
a blocker.

## Phase 0: Coordination + cold-start

Before any other phase.

1. Run `uv run maverick coord read <repo> $ARGUMENTS` and inspect
   the snapshot. Decide which of the four branches in
   `mav-multi-instance-coordination` applies:
   - **Blocked** (`blocked-by:#N` label): abort cleanly, report to user.
   - **Claimed with live lease**: abort cleanly, report holder + expiry.
   - **Claimed with stale lease**: decide take-over vs defer.
   - **Free**: proceed to claim.
2. Claim the issue: `uv run maverick coord claim <repo> $ARGUMENTS`.
   The command exits non-zero if the claim is rejected — treat that as
   abort.
3. **Start the workflow report** (writes a `run-start` row that later
   `report` calls inherit `maverick_skill` from):
   ```bash
   uv run maverick report run-start do-issue-solo --issue $ARGUMENTS --phase claimed
   ```
   From here, **agent-dispatch intervals are recorded automatically** by
   the plugin's Subagent hooks (open on dispatch, closed on return), and
   invoking a tracked inner skill auto-opens its `skill-dispatch`
   interval. Your only bookkeeping obligation is the one-line
   `report end --auto --outcome <…>` after each inner *skill* returns —
   everything else is hooks. Anything left open is flushed as
   `outcome=unknown` by `report generate`.
4. Start the heartbeat daemon. It refreshes the lease every
   `HEARTBEAT_INTERVAL_MINUTES` minutes for as long as you hold the
   claim and exits on its own when the claim is released:
   ```bash
   uv run maverick coord heartbeat-loop <repo> $ARGUMENTS --daemonize
   ```
   Never background the foreground loop with `&` — a process
   backgrounded from a tool shell dies with the shell or leaks
   unobservably. Liveness is checked in the task loop with
   `coord heartbeat-status`.
5. Release is handled on every exit path without any action from you:
   the plugin's SessionEnd hook runs `coord release-all` when the session
   ends (normal exit, user interrupt, crash-caught), and lease expiry
   (10-minute TTL) covers machine death. Your only release obligations
   are the **explicit** ones at workflow boundaries: `--reason merged`
   after auto-merge lands, `--reason ejected` on eject. Do not attempt
   trap-on-exit wrappers — each Bash call is a fresh shell, so a trap
   cannot survive to session end.
6. **Authorization scopes** (only when needed): if the issue explicitly
   authorizes infrastructure changes — the `maverick-authorize-infra`
   label or a `Maverick-Authorize: infra` line in the issue body — record
   it so the scope-guard hook permits those edits in autonomous mode:
   ```bash
   uv run maverick coord authorize <repo> $ARGUMENTS infra
   ```
   If the command exits non-zero, the issue does **not** authorize the
   scope: do not make infrastructure changes; note the gap in the
   solution design instead. Never write `.maverick/session-auth.json` by
   any other means — the hook blocks it, and self-granting defeats the
   authorization model.
7. Cold-start hydrate per `mav-durability-on-gh`. The
   skill is fully resumable — a fresh agent re-entering after a crash,
   stop, or context-exhaustion must skip phases that already completed
   rather than re-running them against an in-flight or merged PR (#41).
   Do not reconstruct the resume position by hand:
   ```bash
   uv run maverick coord resume-point <repo> $ARGUMENTS
   ```
   The command reads the task-progress marker, finds the PR via the
   recorded branch, inspects CI and the review verdict, and returns
   `{next, instruction, evidence}` — follow the instruction. Also check
   for an existing worktree under `.maverick/worktrees/` before creating
   one. Each phase below ends with a `task-progress set` write so
   re-entry advances one boundary at a time without re-running anything.

## Phase 1-2: Understand the Issue and Solution Design (subagent)

Run Phases 1 and 2 as a subagent to keep the main context window clean for
implementation.

1. **Refresh the local base branch** before the analyst reads anything.
   The analyst runs against the main checkout — Phase 4 hasn't created
   the worktree yet — so a stale local base lets pre-resolved
   ambiguities slip into the design pass and surface as phantom
   blockers (#102). Follow the "Base Branch Freshness" rule in
   `mav-git-workflow`:
   ```bash
   STORY_BASE=$(uv run maverick git-workflow story-base)
   git fetch origin "$STORY_BASE"
   CURRENT=$(git rev-parse --abbrev-ref HEAD)
   if [ "$CURRENT" = "$STORY_BASE" ]; then
       git pull --ff-only origin "$STORY_BASE"
   else
       git fetch origin "$STORY_BASE:$STORY_BASE"
   fi
   ```
   If either form refuses a non-fast-forward, halt and report to the
   user — there are local commits on `$STORY_BASE` that have not been
   pushed, which violates trunk-based discipline.
2. Dispatch the **agent-issue-analyst** agent with:
   - Issue number: `$ARGUMENTS`
   - Mode: `solo`
   (The dispatch interval is recorded by the Subagent hooks — no
   `report` calls needed.)
3. When the agent returns, verify the design landed durably —
   `uv run maverick task-progress read <repo> $ARGUMENTS` shows
   `comments.design` set to a comment ID (the analyst posts it via
   `uv run maverick issue comment post --kind design`).
4. If the agent flagged ambiguities it could not resolve:
   - `uv run maverick report begin question --issue $ARGUMENTS --topic ambiguity-resolution`
   - Ask the user.
   - `uv run maverick report end --auto --issue $ARGUMENTS --outcome success`

   Otherwise continue.
5. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS design`.

## Phase 3: Create Tasks (subagent)

Run Phase 3 as a subagent.

1. Dispatch the **agent-github-issue-planner** agent with:
   - Issue number: `$ARGUMENTS`
   - Design comment ID from the task-progress marker (`comments.design`)
2. When the agent returns, verify the tasks landed durably —
   `uv run maverick task-progress read <repo> $ARGUMENTS` shows:
   - If < 5 tasks: `comments.tasks` set to a comment ID (posted via
     `uv run maverick issue comment post --kind tasks`)
   - If >= 5 tasks: sub-issues exist on the issue
3. If the agent flagged scope concerns:
   - `uv run maverick report begin question --issue $ARGUMENTS --topic scope-concerns`
   - Ask the user.
   - `uv run maverick report end --auto --issue $ARGUMENTS --outcome success`
4. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS tasks`
   (append `--has-sub-issues` when the >= 5 tasks path was taken).

## Phase 4: Create Worktree + Branch

The branch is created **inside a dedicated worktree**, not in the main
checkout.

1. Derive the branch name per the mav-github-issue-workflow skill.
2. Resolve the base branch from the project config:
   ```bash
   STORY_BASE=$(uv run maverick git-workflow story-base)
   ```
   - If this story depends on a sibling story whose PR is open but not
     merged, stack per `mav-stacked-prs` — base = sibling branch.
3. Create the worktree: `uv run maverick worktree create <branch> [--base <sibling-branch>]`.
   From this point on, all file edits happen inside the worktree path.
4. `cd` into the worktree path for the rest of the story.
5. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS branch --branch <branch>`
   (recording the branch is what lets `coord resume-point` find the PR later).

## Phase 5: Execute Tasks (push after every task)

**Push after every task, not at the end.** See
`mav-durability-on-gh`.

1. Read project-level skills at `docs/maverick/skills/`. Apply any
   topic-specific guidance they carry.

**For each task (sub-issue or checklist item), in order:**

Each step below is its own obligation. After `/do-code` returns
in step 1, **do not stop** — continue with step 2. The inner skill's
return is a hand-back, not a task-complete signal (#106).

1. **Invoke `/do-code <one-line task description>`.** The
   skill reads before writing, makes the smallest diff that satisfies
   the task, verifies per `mav-local-verification`, and
   refuses to return on red. (Invoking it auto-opens the
   `skill-dispatch` interval via the plugin's Skill hook.)
2. **Record the outcome** — the single bookkeeping obligation per task:
   ```bash
   uv run maverick report end --auto --issue $ARGUMENTS --outcome <success|failure>
   ```
   On `failure`, halt the per-task loop and diagnose per
   `mav-systematic-debugging` — do not proceed to the
   commit step with a failing build or red tests.
3. **(Optional) Sibling-dispatch `/do-test`** if the change
   needs new or updated tests that `do-code` did not
   already cover — then record its outcome the same way:
   ```bash
   uv run maverick report end --auto --issue $ARGUMENTS --outcome <success|failure>
   ```
   When `/do-test` returns, proceed to step 4.
4. **Create a conventional commit** referencing the issue number.
5. **Push immediately.**
   - If this is the first push on the branch, set upstream:
     `git push -u origin <branch>`.
   - If on a stacked branch, run the retarget check per
     `mav-stacked-prs` **before every push**.
6. **Log the commit** to the workflow report. SHA and subject come from
   git; the timestamp is wall-clock at the moment of this CLI call:
   ```bash
   SHA=$(git rev-parse HEAD)
   SUBJECT=$(git log -1 --pretty=%s)
   uv run maverick report commit --issue $ARGUMENTS \
       --phase implement --sha "$SHA" --subject "$SUBJECT"
   ```
7. **Check the task off durably** — `uv run maverick tasks check <repo> $ARGUMENTS <n>`
   (or close the sub-issue). Never PATCH the comment body by hand.
8. **Verify the heartbeat daemon is alive:**
   `uv run maverick coord heartbeat-status <repo> $ARGUMENTS` — if it
   reports not running, treat it as claim-lost: stop pushing, re-run the
   Phase 0 entry check before continuing.

After the last task, run the full verification suite once more.

**Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS implement`.

Follow `mav-plan-execution` for the broader execution loop,
verification discipline, failure handling, and crash recovery.

## Phase 6: Documentation Review (mandatory)

This phase **always runs** before the PR is opened. There is no skip
path — the heuristic-gated version used to let stale docs ship when
Claude's affected-or-not call was wrong. The agent decides whether
work is needed; the workflow decides whether the agent runs.

The agent is dispatched with a **pre-filtered shortlist** of docs the
diff plausibly touches, not the open-ended "audit every doc" brief
that made this phase the longest single subagent cost on prior issues
(observed: ~6 min on a 15-file diff). The agent still reports any
out-of-shortlist docs it believes are impacted — those surface in the
PR body as a follow-up note rather than being silently rewritten.

1. **Build the diff and candidate-doc shortlist** in one deterministic step:
   ```bash
   uv run maverick docs shortlist --base "$(uv run maverick git-workflow story-base)"
   ```
   This writes `/tmp/diff.patch`, `/tmp/changed-paths.txt`, and
   `/tmp/doc-shortlist.txt` (terms derived from changed paths and
   identifiers in the diff, matched across every `docs/` tree). The
   shortlist may legitimately be empty — that is a valid input to step 2.
2. Dispatch **agent-tech-docs-writer** with (interval
   recorded automatically by the Subagent hooks):
   - **Mode:** `update` (per `do-docs`)
   - **Diff:** `/tmp/diff.patch`
   - **Candidate docs:** the contents of `/tmp/doc-shortlist.txt`. If
     the file is empty, pass the literal string
     `<empty — scan only for gaps requiring new coverage>`.
   - **Instructions:**
     - Read each candidate doc. Update only sections rendered stale by
       the diff; do **not** refactor unrelated content.
     - If the diff introduces a component, subsystem, or architectural
       change with no coverage anywhere in `docs/`, create the new
       document.
     - If you find a doc **outside the candidate list** that you
       believe is impacted, **list its path in your return payload —
       do not edit it.** One-pass dispatch: no widen-and-retry; the
       caller folds these into a follow-up note on the PR for the
       human reviewer.
     - Returning "no doc changes required" is a valid outcome and must
       be reported explicitly (not silently inferred).
3. **Record the outcome** in the PR body or as a one-line PR comment so
   the gate is auditable:
   - If docs were updated or created: list the files changed.
   - If the agent flagged out-of-shortlist docs: append a
     `Docs follow-up: <paths>` line to the PR body so the reviewer
     sees them.
   - If no changes were required: post `Docs review: no changes required.`
4. Commit any doc changes with a `docs:` conventional commit and push
   per the push-per-task rule. If a commit was made, log it so the
   docs phase row gets its own sub-row in the report:
   ```bash
   SHA=$(git rev-parse HEAD)
   SUBJECT=$(git log -1 --pretty=%s)
   uv run maverick report commit --issue $ARGUMENTS \
       --phase docs --sha "$SHA" --subject "$SUBJECT"
   ```
5. The PR cannot proceed to Phase 7 until this phase has produced
   either committed doc changes or the auditable no-op record.
6. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS docs`.

## Phase 7: Pre-push Cybersecurity Review (mandatory)

This phase **always runs** before the PR is opened. There is no skip
path. Any changed code AND any code that could be impacted by the
changes (callers, importers, dependents) must be reviewed by
`do-cybersecurity-review` before the PR can be opened.

Each step below is its own obligation. After `/do-cybersecurity-review`
returns in step 2, **do not stop** — continue with step 3. The inner
skill's return is a hand-back, not a phase-complete signal (#106).

1. **Compute the full diff:** `git diff origin/<base>...HEAD`.
2. **Dispatch `/do-cybersecurity-review`** with (invoking it
   auto-opens the `skill-dispatch` interval via the Skill hook):
   - **Mode:** `update`
   - **Diff:** the output of step 1, passed via stdin or as a file path
   - **Instructions:** review the changed code AND the impact set
     (callers, importers, dependents — bounded to one or two hops).
     Return the structured outcome (verdict + findings) defined in the
     skill's Update Mode contract.

   When the skill returns, proceed to step 3 — do not summarise and
   stop.
3. **Record the outcome:**
   `uv run maverick report end --auto --issue $ARGUMENTS --outcome <success|failure|blocked>` (use `blocked` if the verdict was BLOCKING).
4. **Act on the verdict:**
   - **BLOCKING** — halt. Surface the findings to the user verbatim.
     Do not open the PR. The user resolves the BLOCKING items by
     returning to Phase 5 (implement, test, commit, push). Re-run
     this phase against the new diff before proceeding.
   - **FINDINGS** — append a `## Security Review` section to the PR
     body draft listing each finding (severity, location, description,
     recommendation). The PR may proceed to Phase 8 with these items
     visible to the human reviewer and to agent-code-reviewer.
   - **PASS** — record `Security review: no concerns.` in the PR body
     draft so the gate is auditable.
5. The PR cannot proceed to Phase 8 until this phase has returned a
   non-BLOCKING verdict and the outcome has been folded into the PR
   body draft.
6. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS security`.

## Phase 8: Open PR + Monitor CI

1. Pre-push verification per `mav-local-verification` — a final
   green check before asking for review.
2. Stacked-PR retarget check per `mav-stacked-prs` if the branch
   stacks on a sibling. Retarget before opening the PR if the sibling is now
   merged.
3. Resolve the PR target from config:
   ```bash
   PR_TARGET=$(uv run maverick git-workflow pr-target)
   ```
   Open the PR. The body **must** end with a literal `Closes #$ARGUMENTS`
   line (capitalised; not `Refs`, `Related to`, or any other phrasing).
   `gh pr merge --squash` carries the PR body verbatim into the squash
   commit body; GitHub only auto-closes the linked issue when one of
   `Closes`/`Fixes`/`Resolves` appears in a commit on the default
   branch. If multiple PRs land via a non-squash promotion (Gitflow:
   `develop` → `main`), each squash commit's body is what GitHub scans
   — so omitting the keyword on a single PR leaves *that* story open
   even after promotion (#56). Use `Refs #N` only for cross-references
   to *other* issues, never for the primary story:
   ```bash
   gh pr create --base "$PR_TARGET" --head <branch> \
       --title "<conventional title referencing #$ARGUMENTS>" \
       --body "$(cat <<'PR_EOF'
   ## Summary
   <1-3 bullet points>

   Closes #$ARGUMENTS
   PR_EOF
   )"
   ```
4. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS pr_open`.
5. Monitor CI with a bounded wait:
   ```bash
   uv run maverick pr wait <repo> <pr-num> --checks --timeout 30m
   ```
   - Exit 0: checks green — continue.
   - Exit 5: checks failed — read the logs per `mav-bp-cicd`,
     fix locally, push, re-run the wait.
   - Exit 3: timeout — investigate the stuck check (a required check
     that never reports blocks auto-merge too); report to the user if
     it cannot be resolved.
   Do not proceed to Phase 9 until the wait exits 0.
6. **Browser/UI verification is non-blocking.** If the change touches UI
   and Claude's global instructions or a project skill ask for browser
   verification, run it with a strict timeout (e.g. 5 min total). On
   hang, timeout, or failure, post the outcome as a non-blocking PR
   comment and proceed to Phase 9 — do **not** wait indefinitely (#41).
   Phase 9's reviewer is the binding gate; CI is the binding regression
   check; ad-hoc browser runs are advisory.
7. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS ci_green`.

## Phase 9: Code Review (binary, hard gate)

The local **agent-code-reviewer** subagent's verdict is the
review gate the auto-merge path trusts. This is a binary verdict against
the open PR, not a local-diff advisory loop.

1. Dispatch **agent-code-reviewer** with (interval
   recorded automatically by the Subagent hooks):
   - The PR URL
   - The issue body, design comment, and tasks list (so it has the spec)
2. **Parse the verdict from the marker line only.** The agent's reply
   must end with exactly one `MAVERICK_VERDICT: PASS` or
   `MAVERICK_VERDICT: FAIL` line — that line is the verdict; do not
   infer it from the prose above it.
   - `MAVERICK_VERDICT: PASS` — proceed to Phase 10 (merge).
   - `MAVERICK_VERDICT: FAIL` — proceed to Phase 11 (eject). Do not
     attempt to auto-fix.
   - Marker **missing, ambiguous, or present more than once with
     conflicting values** — treat as FAIL and eject. Do not re-dispatch
     the reviewer to "get a cleaner answer", and never substitute your
     own reading of the review body for a missing marker.
3. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS review`.

There is no fix-and-re-review loop. If the reviewer FAILs the PR, the
next step is eject-to-human, not iterate.

## Phase 10: Auto-merge (on PASS)

1. **Verify the PR body still carries the closing keyword.** The body
   becomes the squash commit body, and the closing keyword must survive
   into the commit that lands on the default branch (#56). If the body
   was edited after Phase 8 — by a reviewer, by another subagent, or by
   a force-push — re-add the line before merging:
   ```bash
   uv run maverick gh-app gh -- pr view <pr-url> --json body -q .body \
       | grep -Eq '(Closes|Fixes|Resolves) #$ARGUMENTS\b' \
       || { echo "PR body missing 'Closes #$ARGUMENTS' — re-add before merging"; exit 1; }
   ```
2. **Auth-path gate (hard).** Never auto-merge a PR that touches
   authentication/authorization surfaces or CI workflow definitions —
   those require human review regardless of the code-review verdict:
   ```bash
   uv run maverick pr auth-scan <repo> <pr-num>
   ```
   - Exit 0: clean — proceed.
   - Exit 3: gated paths touched — **do not merge.** Treat this exactly
     like a review FAIL: follow the eject path (apply `needs-human`,
     post the scan output as a comment, release the claim) and stop.
   - Exit 2: scan error — retry once; if it still fails, eject rather
     than merging unverified.
3. The Maverick GitHub App posts the approval:
   ```bash
   uv run maverick gh-app gh -- pr review <pr-url> --approve \
       --body "Approved by agent-code-reviewer at $(date -u +%FT%TZ)"
   ```
4. Enable auto-merge (squash):
   ```bash
   uv run maverick gh-app gh -- pr merge <pr-url> --auto --squash
   ```
   The merge waits on whatever required status checks the project's
   branch protection enforces — typically lint, tests, build, and (if
   the optional `mav-bp-remote-code-review` workflow is
   adopted) the CI-side re-run of agent-code-reviewer. If all required
   checks were already green, GitHub merges immediately; otherwise it
   merges when they pass.
5. **Wait for the merge to land** with a bounded wait — cleanup steps
   below assume the PR is no longer in flight:
   ```bash
   uv run maverick pr wait <repo> <pr-num> --timeout 30m
   ```
   Exit 3 (timeout) usually means a required check never reported —
   investigate rather than looping; exit 4 (closed without merge) means
   a human intervened — stop and report.
6. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS merged`.
7. Post the completion comment on the issue per
   `mav-github-issue-workflow`.
8. **Run the post-merge issue-lifecycle step.** This always posts an
   audit comment ("Resolved in PR #<P>; merged to <branch>.") and
   applies a `merged-to-<branch>` label, then closes the issue per the
   per-project policy in `.maverick/config.json`'s
   `issue_lifecycle.close_policy` (#52). The default policy
   (`on_pr_merge`) closes the issue immediately, which is right for
   trunk-based and GitHub Flow repos. Repos using Gitflow or custom
   promotion gates can set the policy to `on_default_branch_merge` or
   `manual` to keep the issue open until promotion — the audit comment
   and label still surface the merge so `gh issue list -l merged-to-develop`
   finds work pending promotion. The CLI is idempotent (re-running it
   on a closed issue is a no-op), so it is safe to retry:
   ```bash
   uv run maverick issue close-on-merge <repo> $ARGUMENTS \
       --pr <pr-num> --target <target-branch>
   ```
9. Release the claim: `uv run maverick coord release <repo> $ARGUMENTS --reason merged`.
10. Destroy the worktree: `uv run maverick worktree destroy <worktree-path>`.
11. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS complete`.
12. **Emit per-phase narrative notes** so the report's Analysis section
    has context for what happened. The JSONL is the authoritative
    record; the report is a pure render of it, so notes must land in
    the JSONL — do not edit the rendered Markdown by hand:
    ```bash
    uv run maverick report note --issue $ARGUMENTS --phase design \
        --text "<one-sentence summary of what the analyst returned>"
    uv run maverick report note --issue $ARGUMENTS --phase implement \
        --text "<one-sentence summary of what landed in Phase 5>"
    # ... one `report note` per phase that produced work worth narrating
    ```
13. **Generate the workflow report**. Written to the **main repo's**
    `.maverick/reports/` (resolved via `git rev-parse --git-common-dir`),
    not the destroyed worktree's. Re-runs are deterministic:
    ```bash
    uv run maverick report generate <repo> $ARGUMENTS
    ```

## Phase 11: Eject (on FAIL)

1. Post the reviewer's verdict as a PR comment (App identity, per
   `mav-github-issue-workflow`):
   ```bash
   uv run maverick gh-app gh -- pr comment <pr-url> --body-file /tmp/review-verdict.md
   ```
2. Apply the `needs-human` label to both the PR and the issue:
   ```bash
   gh pr edit <pr-url> --add-label needs-human
   gh issue edit $ARGUMENTS --add-label needs-human
   ```
3. Request human review on the PR:
   ```bash
   gh pr edit <pr-url> --add-reviewer <human-handle>
   ```
4. If this story belongs to an epic (look for a parent epic reference on
   the issue, or `uv run maverick state show <repo> <epic>`):
   - Mark this story `ejected`:
     `uv run maverick state set <repo> <epic> $ARGUMENTS ejected`.
   - Run block propagation (idempotent, resumable):
     `uv run maverick bprop run <repo> <epic> --ejected $ARGUMENTS`.
   - Cancel any in-flight subagent work for stories now in the blocked
     set, per `mav-block-propagation`.
5. **Checkpoint the eject** (#83): `uv run maverick task-progress set <repo> $ARGUMENTS ejected`.
6. **Emit per-phase narrative notes** so the eject report has context
   for the human reviewer:
   ```bash
   uv run maverick report note --issue $ARGUMENTS --phase review \
       --text "<one-sentence summary of what the reviewer flagged>"
   # ... one `report note` per phase that produced work worth narrating
   ```
7. **Generate the workflow report**. Do this **before** releasing the
   claim so the report lands even if release errors:
   ```bash
   uv run maverick report generate <repo> $ARGUMENTS
   ```
8. Release the claim: `uv run maverick coord release <repo> $ARGUMENTS --reason ejected`.
9. Do **not** destroy the worktree — the human may want to inspect it.
   Log the worktree path so the user can find it.

## Rules

- **Only pause for user input** when blocked or when the issue is ambiguous.
- **Never commit directly to the default branch.** All work flows through
  the feature branch → PR.
- **Always use conventional commits** referencing `#$ARGUMENTS`.
- **Push after every task.** Durability trumps CI-cost optimisation.
- **Binary review.** PASS auto-merges; FAIL ejects. No fix loop.
- **Release the claim on every exit path.** Success, eject, abort, crash —
  all of them must release.
- **Never remove a `blocked-by:#N` label from inside the workflow.** Only a
  human may clear a block.

<!-- maverick-plugin-version: 4.0.2-dev -->
