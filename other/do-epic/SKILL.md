---
name: do-epic
description: Work on a multi-story GitHub epic end-to-end. Builds a DAG from the child stories, groups them into waves, runs waves in parallel via per-story worktrees, ejects PRs that fail agent-code-review for human handling, and propagates blocks to downstream stories. Requires git worktrees.
argument-hint: epic issue number (e.g., 123)
user-invocable: true
disable-model-invocation: false
---

# Work on GitHub Epic (Autonomous, DAG-scheduled)

Work on epic issue `$ARGUMENTS` end-to-end. Builds a dependency DAG
from the epic's child stories, schedules them into waves, runs each wave
in parallel via per-story worktrees, and drives every story through agent
code review with binary PASS/FAIL verdicts.

## Preflight (mandatory)

Run this **first**. If it exits non-zero, halt and report the stderr output to the user verbatim. Do not claim, do not branch, do not start any worktree.

```bash
uv run maverick preflight do-epic
```

The check verifies: the project is initialised, the Maverick GitHub
App is configured (`maverick gh-app status` reports `configured: true`),
git worktrees are usable, and required tools (`gh`, `git`, `uv`) are on
PATH. PR code review runs locally inside each story's worktree as the
`agent-code-reviewer` subagent (delegated from
`do-issue-solo` Phase 9). For epics that fan out across
many parallel workers, consider opting into the CI-side re-run
described in `mav-bp-remote-code-review` so the merge is
gated by an independent check even if a worker's local review fails to
fire — that workflow is optional and not enforced by preflight.

## Before You Begin

`$ARGUMENTS` must be the GitHub issue number of a Maverick **epic**
— an issue whose body contains a task table of child stories. If it is
a single story, dispatch `do-issue-solo` instead.

## Phase 0: Coordination

1. **Resolve repo**: `gh repo view --json nameWithOwner`.
2. **Cold-start hydrate** per `mav-durability-on-gh`:
   - Read the `maverick-dag` marker on the epic.
   - Read the `maverick-state` marker.
   - Read the `maverick-bprop` marker — if present, **resume block
     propagation first** before continuing.
   - Read open PRs for the epic's child-story branches.
3. **Decide claim scope**:
   - Whole epic if no live claim exists.
   - A specific wave if another instance already holds other stories.
   - Single story if another instance holds the epic but not the story
     you were asked about.
4. **Claim**: `uv run maverick coord claim <repo> $ARGUMENTS --scope <csv-of-issues>`.
   On `ClaimRejected`, abort and report per
   `mav-multi-instance-coordination`.
5. **Start heartbeat daemons** for every issue in the claim scope. Each
   daemon exits on its own when the matching claim is released; check
   liveness anytime with `coord heartbeat-status`:
   ```bash
   for issue in <epic> <story1> <story2> …; do
     uv run maverick coord heartbeat-loop <repo> $issue --daemonize
   done
   ```
   Never background the foreground loop with `&` — a process backgrounded
   from a tool shell dies with the shell or leaks unobservably.
6. **Release on exit is automatic.** The plugin's SessionEnd hook runs
   `coord release-all`, releasing every claim this instance recorded —
   the matching `heartbeat-loop` processes detect the cleared labels and
   exit on their own; lease expiry covers machine death. Your only
   explicit releases are the per-story ones at workflow boundaries
   (merged / ejected). Do not attempt trap-on-exit wrappers — each Bash
   call is a fresh shell, so a trap cannot survive to session end.

## Phase 1: Design + task decomposition (if needed)

If the epic does not yet have a solution design:

1. Dispatch `agent-issue-analyst` with the epic issue.
2. Dispatch `agent-github-issue-planner` — the planner will
   create child stories as sub-issues (per the ≥ 5-tasks threshold in
   `mav-create-tasks`).
3. Extend the claim to cover every newly-created child story:
   `uv run maverick coord claim <repo> <child-issue>` for each.

If the epic already has stories, skip to Phase 2.

## Phase 2: DAG analysis

Build a machine-readable DAG of child stories.

1. For each child story, read its issue body. Look for:
   - Explicit "depends on #N" references
   - Shared files in the implementation plan
   - Shared APIs or data models
2. Construct the DAG payload per the schema in
   `docs/conventions/github-markers.md`:
   ```json
   {
     "epic": $ARGUMENTS,
     "stories": {
       "140": {"deps": [], "files": ["app/src/boot.ts"]},
       "142": {"deps": ["140"], "files": ["app/src/admin/guard.ts"]}
     }
   }
   ```
3. **Persist the DAG to GitHub** — this is durable for any instance to
   resume from. Write the payload JSON to a file and let the CLI compose
   and upsert the fenced marker (never hand-compose marker comments):
   ```bash
   uv run maverick gh-state write <repo> $ARGUMENTS maverick-dag --payload-file /tmp/dag.json
   ```

## Phase 3: Wave grouping

```bash
uv run maverick dag waves <repo> $ARGUMENTS
```

The output is a list of lists — each inner list is a set of stories with
no un-satisfied deps on later waves. Record the waves in the epic's
human-readable task-table comment as well, so a human skimming the epic
can see execution order.

## Phase 4: Initialise epic state

1. For each child story, seed `maverick-state` with initial status:
   - `pending` if not yet started
   - `merged` if already merged (detected by reading PR state)
   - `in_flight` only if another instance's heartbeat is live for it
2. Persist:
   ```bash
   uv run maverick state set <repo> $ARGUMENTS <story> <status>
   ```
   Each call mirrors the local cache to the `maverick-state` marker on
   the epic.

## Phase 5: Wave loop

Repeat until every story is terminal (merged or ejected) or every
remaining wave is fully blocked.

### Phase 5a: Select the next wave

1. Read waves: `uv run maverick dag waves <repo> $ARGUMENTS`.
2. Read current state: `uv run maverick state show <repo> $ARGUMENTS`.
3. Pick the first wave whose every member is not yet merged.
4. **Exclude stories carrying `blocked-by:#N`** — re-read the labels at
   selection time so human-resolved ejections automatically unblock.
5. If every remaining story in every remaining wave is blocked, halt
   the epic cleanly:
   - Update `maverick-state`.
   - Post a summary comment on the epic listing the blockers.
   - Release the epic-level claim.
   - Report to the user.

### Phase 5b: Create worktrees

Resolve the story base branch from config:

```bash
STORY_BASE=$(uv run maverick git-workflow story-base)
```

For each unblocked story in the wave, decide its base branch:

- If the story depends on a sibling in the **same wave** that is still
  unmerged, stack per `mav-stacked-prs`.
- Otherwise, branch from `$STORY_BASE`.

Create the worktree:
```bash
uv run maverick worktree create <branch> [--base <sibling-branch>]
```

### Phase 5c: Parallel-or-serial decision

Decide based on:
- **User policy**: does the user want parallel subagents? (Check the
  session; if unsure, default to serial.)
- **Capacity**: no more than `MAX_CONCURRENT_WORKTREES=4` active at once.

If parallel: dispatch one subagent per worktree, running
`do-issue-solo` for that story inside that worktree. Track
the subagents and aggregate results.

If serial: iterate worktrees one at a time, running
`do-issue-solo` in each.

### Phase 5d: Per-story flow

For each story being worked on (whether as subagent or serially):

1. **Re-verify** the claim: `uv run maverick coord heartbeat <repo> <story>`
   — if the story now carries `blocked-by:#N`, abort without pushing.
2. Run the story through `do-issue-solo`'s per-story phases
   (Phase 4 onward — branch is already created).
3. **On FAIL from agent-code-reviewer (eject)** — FAIL means the
   `MAVERICK_VERDICT: FAIL` marker parsed in `do-issue-solo`
   Phase 9; a missing or ambiguous marker counts as FAIL:
   - Mark story `ejected` in epic state:
     `uv run maverick state set <repo> $ARGUMENTS <story> ejected`.
   - Run block propagation per `mav-block-propagation`:
     - Write `maverick-bprop` marker on the epic.
     - Walk descendants, apply `blocked-by:#<story>` to each.
     - Cancel any in-flight subagent work for a now-blocked story.
     - Clear the `maverick-bprop` marker when the walk completes.
4. **On PASS + auto-merge**:
   - Mark story `merged` in epic state.
   - Release the story-level claim.
   - Destroy the worktree.

### Phase 5e: Wave completion

When every story in the wave is terminal (merged or ejected):

1. If every remaining wave is fully blocked by ejections, halt
   (Phase 5a's block check handles this on the next iteration).
2. Otherwise, return to Phase 5a for the next wave.

## Phase 6: Epic completion

1. Every child story is either merged or ejected.
2. Post a summary comment on the epic:
   - Count merged vs ejected.
   - Link to every PR.
   - Call out the ejected stories as the human's queue.
3. Update `maverick-state` one last time.
4. Release the epic-level claim:
   `uv run maverick coord release <repo> $ARGUMENTS --reason complete`.
5. The `heartbeat-loop` background processes self-terminate within one
   `--interval` window once their claims are released — `wait` for them
   if you backgrounded them with PIDs, or just let the parent shell exit.
6. Close the epic issue only if **no stories were ejected** AND the
   per-project close policy allows it (#52). Per-PR closes for child
   stories already ran via `do-issue-solo` Phase 10, but the epic
   itself spans multiple branches/PRs, so the simple `close-on-merge`
   CLI doesn't fit — query the policy and decide:
   ```bash
   policy=$(uv run maverick issue policy)
   if [ "$policy" != "manual" ] && [ "$ejected_count" -eq 0 ]; then
     gh issue close $ARGUMENTS \
       --comment "Epic complete: $merged_count stories merged."
   fi
   ```
   If any stories were ejected, leave the epic open for the human to
   resolve them and close manually. If the policy is `manual`, leave
   the epic open regardless — the team's promotion workflow handles
   final close.

## Resumption

At any entry, if another instance was mid-flight:

- A `maverick-bprop` marker means a block walk was in progress — resume it
  per `mav-block-propagation`.
- A `maverick-claim` on some stories with a stale lease means an instance
  died — decide takeover per `mav-multi-instance-coordination`.
- A `maverick-state` with stories marked `in_flight` but no live claim
  means those stories are orphaned — reclaim and resume, or mark back to
  `pending` if the worktree was destroyed.

The workflow is idempotent on every entry — you can re-run `do-epic` on
the same epic any number of times and it will converge to the same final
state.

## Rules

- **Worktrees are mandatory.** Abort on entry if unavailable.
- **The Maverick GitHub App is mandatory.** Abort on entry if `maverick gh-app status` does not report `configured: true`.
- **Binary review everywhere.** No story merges without PASS from
  `agent-code-reviewer`. No fix loop.
- **Block propagation is idempotent.** Re-running it after a crash is
  safe; the marker-walk-clear protocol handles partial completion.
- **Release every claim on every exit.** Success, eject, abort, crash.
- **Never auto-close an epic with ejected stories.** Those belong to the
  human.

<!-- maverick-plugin-version: 4.0.2-dev -->
