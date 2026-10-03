---
name: merge-cleanup
description: Consolidate multiple Git worktrees and clones of a repository into a single clean checkout, safely merge associated PRs in topological dependency order, reconcile post-merge governance state (PDDA and RELEASES DB), and safely remove leftover worktrees/clones without data loss or interrupting active sessions. Strictly complies with WORKTREE-SAFETY.md.
---

# /merge-cleanup — Worktree Consolidation, PR Sequencing, and Safe Teardown

`merge-cleanup` consolidates multiple active Git worktrees and clones of a repository into a single clean primary checkout, determines optimal topological PR merge sequences, executes GitHub PR merges, triggers post-merge PDDA & RELEASES DB reconciliations, and safely tears down disposable worktrees/clones without data loss or active process disruption.

Strictly adheres to [`WORKTREE-SAFETY.md`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/WORKTREE-SAFETY.md) and [`AGENTS.md`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/AGENTS.md).

---

## Recite this — verbatim, as the first thing in your first response

> **Merge-Cleanup Discipline:**
> 1. **Verify primary landing readiness (Phase 0).** Confirm the primary on-disk checkout is clean, on the integration branch (`development`), and ready to fast-forward before any remote action.
> 2. **Inventory checkouts & protect active sessions (Phases 1–3).** Scan worktrees and task clones across safe roots; preserve any checkout with active file handles, driver locks, `.tick` claims, or recent edits (10m/60m recency ladder).
> 3. **Sequence PRs & pre-gate conflicts (Phases 4–5).** Fetch open PRs into a topological DAG to prevent file collisions; pre-simulate landings and resolve disjoint ledger/doc conflicts.
> 4. **Merge & reconcile governance (Phase 5).** Remote squash-merge in dependency order, fast-forward primary checkout (`git merge --ff-only`), and execute post-merge reconciliation (`wave_reconcile`, `releases_app check`, `pdda.sh`).
> 5. **Safe teardown & status confirmation (Phase 6).** Deregister worktrees via canonical git protocol, move clean disposable clones to Trash, prune dangling skill symlinks, and confirm all PRs are landed.
>
> **Overall Goal:** All ready-to-merge PRs processed and local disk clones and git worktree folders safely torn down when appropriate.

Then begin work.

---

## Conversational Triggers

When the operator speaks naturally:
- `"Run merge-cleanup on this repo"`: Reviews the primary on-disk checkout first (Phase 0), then audits the other checkouts, reports the sequence, and proceeds within the session's authorized PR and cleanup scope. Discovery does not add unrelated PRs to that scope; an explicit audit/dry-run request remains read-only.
- `"Scan all clones and worktrees"`: Runs Phase 1–3 discovery and outputs the status matrix of all worktrees and clones.
- `"Sequence and merge open PRs"`: Reports Phase 0 for the primary checkout first — a PR sequence is not actionable until the tree it lands in can receive it — then determines topological order of open PRs, detects file collisions, and executes remote squash merges followed by wave reconciliation.
- `"Tear down clean task clones"`: Safely removes verified clean, non-active clones and worktrees.

---

## 7-Phase Ladder Logic

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 0: Primary On-Disk Checkout (Can It Receive The Landing?)         │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 1: Discover & Inventory (Identify Checkouts & Roots)              │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 2: Active Process & Session Inspection (Zero Disruption)          │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 3: Git Safety & Worktree Verification (Data Loss Prevention)      │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 4: PR Matrix & Topological Sorting (Dependency-Ordered Landing)   │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 5: Safe Execution & Post-Merge Reconciliation (Governed Landing)  │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 6: Safe Teardown (Worktree & Clone Pruning via Git Protocol)      │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 0: Primary On-Disk Checkout — always first, never by discovery

**Report the operator's own checkout before anything remote is fetched.** It is the tree every
PR lands in, the tree `git merge --ff-only` runs in, and the tree `wave_reconcile.py`,
`releases_app.py` and `pdda.sh` write to. A run that opens with a PR table has told the operator
about everyone else's work and nothing about their own.

- Inspect the primary **by identity**, not by discovery. It is listed because it is the primary —
  never because a `SAFE_ROOTS` walk reached it or its directory name matched `--prefix`. A primary
  outside those roots, or under a non-matching prefix, used to vanish from the audit entirely
  while Phase 5 went on merging into it.
- Report and gate on five facts: current branch vs the integration branch (`--integration-branch`,
  default `development`), working-tree cleanliness, an unfinished merge/rebase/cherry-pick, local
  commits on the integration branch that `origin` does not have, and positive ancestry proof that
  HEAD can fast-forward to `origin/<integration>`.
- **Readiness is affirmative.** Every fact must be positively established; a git query that *fails*
  is unknown state, never a pass. A checkout with no `origin/<integration>` at all is not ready,
  because the landing target cannot be resolved.
- The branch that is checked is the branch that is landed. `--integration-branch` threads through
  Phase 0 and the fast-forward alike.
- **Unpushed commits on the integration branch are a blocker, not a note.** A squash-merge landing
  skips them silently, which is how local work is lost.
- Not ready is a **refusal**, reported before the PR matrix and enforced before the first mutation.
  It covers zero-PR cleanup, teardown-only cleanup, and `--reconcile-pr`; none may silently defer
  the primary checkout to the operator after reporting success.
  A dry run still prints the sequence, labelled explicitly as not executable while blockers stand.
  `--allow-unready-primary` overrides the refusal deliberately and records the blockers.
- The verdict is **re-established against the live remote** immediately before the first merge, so
  a stale cached `origin/*` cannot certify a tree that has since diverged. A refresh that *fails*
  is itself a refusal — re-checking against the cache the fetch could not update would certify
  stale evidence as current.
- **Every PR's base must be the checked integration branch.** Phase 0 vouches for one branch only;
  a PR based elsewhere would land in a tree whose readiness was never established, so the run
  refuses rather than merging it.
- Uncommitted intake docs or captures in the primary are their own commit or a park — they do not
  ride along in whatever PR happens to be open.

```bash
python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary . --scan-only   # Phase 0 + audit
```

Phase 0 runs in every mode of the orchestrator. The standalone helpers below
(`scan_clones.py`, `toposort_prs.py`) do **not** perform it — reach for `merge_cleanup.py` when
the answer will inform a landing.

### Phase 1: Discover & Inventory
- Always includes the primary checkout from Phase 0, then locates further candidate repositories under `SAFE_ROOTS` — `~/Documents/GH Repos`, `~/agent-workspaces`, `~/Documents/agent-workspaces`, `~/marathon-clones` (where `/start-task`, `/jog` and marathon flows create task clones). The list in `scan_clones.py` is the list in `WORKTREE-SAFETY.md` §16.1; a test pins the parity (GH-534 A.1).
- Evaluates component-aware containment (`_within(child, parent)`) and refuses `NEVER_DELETE` protected roots (`$HOME`, `~/Documents`, `~/Desktop`, `/`).
- Distinguishes **Linked Worktrees** (`.git` is a file with pointer `gitdir: ...`) from **Standalone Clones** (`.git` is a directory).
- Uses `git worktree list --porcelain` to determine parent-child relationships.

### Phase 2: Active Process & Session Inspection
- Checks driver locks: `.git/relay-driver.lock` (or vendored `.relay-driver.lock`) and validates holder PID liveness via `kill -0 <pid>`.
- Checks `.tick/` active claims through the **event log fold**, never `STATE.md` (a derived snapshot): `tick claims --json` with `TICK_REPO_ROOT` pinned to the coordination root (a linked worktree's is its parent clone's). Any claimed task → `ACTIVE_TICK_CLAIM` naming task and agent; a `.tick/locks/` entry of any shape counts; `tick` missing, failing, or an events directory that is missing/unreadable → `PRESERVE_UNVERIFIED_SESSION` naming why (GH-534 A.4, `decisions/2026-09-09-tick-claims-verb.md`).
- Checks live file handles via `lsof -F pcn +D <checkout>` from a CWD outside it. Three outcomes, because `lsof +D` exits 1 whether idle or held: a normal exit with code 0/1 **and** empty stderr is a complete enumeration (matches → `ACTIVE_PROCESS` naming PIDs and commands, none → verified idle); a signal-killed/timed-out/absent `lsof`, or **any** stderr line (`WARNING: can't opendir`), is incomplete → `PRESERVE_UNVERIFIED_SESSION` naming the warning.
- **Activity Window Ladder (10m + 60m Recency Detection):** Inspects non-ephemeral file modification timestamps (`mtime` ignoring `.git`, `node_modules`, `.venv`, `.DS_Store`, and `*.sqlite-wal`/`*.sqlite-shm`) to classify:
  - **`ACTIVE_WRITING`** ($\le 10$m): In-progress active editing.
  - **`RECENT_IDLE`** ($10\text{m} - 60\text{m}$): Paused session, recent edits.
  - **`DORMANT`** ($> 60$m): Zero file modifications in over an hour.
  - When open file handles are detected on a `DORMANT` checkout, `ACTIVE_PROCESS` is annotated with `(Dormant handle: 0 files modified in >60m)` to distinguish idle background handles from active editing.
- Honors explicit user exclusion patterns (e.g. `--exclude gh427`). A bare PR number (`--exclude 427`) also drops that PR from the Phase 4 queue, logged as `excluded by --exclude` (GH-736).

### Phase 3: Git Safety & Worktree Verification
- **Dirty status:** reads the complete NUL-safe `git status --porcelain -z --untracked-files=all` and names **every** file in the disposition. There is no regenerable-artifact allowance: `harnesses.db` carries invocation data, `*.db.bak` may be the last pre-rebuild copy (GH-534 A.3).
- **Stashes:** Asserts `git stash list` is empty (0 unpopped stashes).
- **Landed vs unlanded refs, by provenance (A.2):** after a verified `git fetch origin <integration-branch>`, every local ref tip — all `refs/heads/*`, detached `HEAD`, any local-only ref — must be either (1) reachable from `origin/<integration-branch>`, or (2) the exact `headRefOid` of a **MERGED** PR (base = integration branch, `gh pr list --state merged`, remote identity bound to the clone's `origin`) whose merge commit is reachable **and** whose landed content equals the branch's — per-path blob ids and modes from `git diff --raw --full-index`, so whitespace and binaries count. Anything else is `PRESERVE_UNPUSHED` naming the ref, the commit and the reason (no merged PR; content differs from PR #N; lookup unavailable). Squash merges no longer read as "unpushed forever"; a changed conflict resolution or a commit after the PR head still preserves. `git cherry` is never an authorization input.
- **Completion Confidence & Agent Follow-up (Medium Scan Ladder):**
  - **Medium Scan:** Inspects commit logs for QA attestations (`relay-drive: attest ... approved`, `status — final QA approved`, `LGTM`, `QA approved`), working tree cleanliness, and PDDA task checklists under `PROJECT/2-WORKING/`.
  - **Deep Scan Escalation:** If unlanded commits exist without QA attestation, marks confidence as `MEDIUM` and recommends a deeper scan. The deeper scan is [`/merge-cleanup-deep`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/3-weekly/merge-cleanup-deep/SKILL.md) (GH-728): it consumes this skill's `scan_clones.py --json` audit, zips every preserved checkout to a dated backup, fans out ≤3 read-only sub-agents by branch family, and returns PR-WORTHY / SUPERSEDED / NEEDS-OWNER / ABANDON-CANDIDATE verdicts with the deciding evidence; disposable checkouts come back here for Phase 6 teardown. `/recon` or `/debug-mantra` remain the tools for a single clone's conflict.
  - **Agent Follow-up:** Identifies the owning agent (via `.tick` claim, author/co-author, or PID command name) and provides actionable follow-up guidance.
- **Canonical GitHub Issue Marker (`--marker`):**
  - Resolves linked canonical issue (via branch name, directory name, or commit log regex) and formats a structured status checkpoint comment to post to GitHub.
- **Worktree dependencies:** Verifies no other linked worktrees point to a clone before marking it disposable.
- **Every safety query fails closed (A.5):** a non-zero or unparseable `git status`, `stash list`, `worktree list`, `for-each-ref`, `fetch`, `tick claims` or `lsof` → `PRESERVE_UNVERIFIED_QUERY` / `PRESERVE_UNVERIFIED_SESSION` naming the query. No result is ever defaulted to "none".

### Phase 4: PR Matrix & Topological Sorting
- Runs only after Phase 0 has reported. The PR sequence is advice until the primary can receive it.
- Fetches open PRs via GitHub API (`gh pr list`). The discovery call is bounded in time and retried on transient network failures (GH-623): a FAILED discovery is an error, never an empty queue — after three transient retries it exits 2 before Phase 6, because rolling into teardown on a false "no PRs" would report success while the queue was silently skipped.
- Extracts explicit dependency references (`depends on #N`, `blocked by #N`, `after #N`) as **hard** edges.
- Analyzes touched file sets to detect unannotated file collisions and orders shared-file PRs chronologically as **soft** edges: they decide sequence only, never eligibility (GH-623).
- Builds a Directed Acyclic Graph (DAG) and computes topological merge order.

### Phase 5: Safe Execution & Post-Merge Reconciliation
- **Refuses every executing cleanup when Phase 0 says the primary is not landing-ready**, unless the operator explicitly passes `--allow-unready-primary` to defer that cleanup. This gate applies before any Phase 5 or Phase 6 mutation, including zero-PR and `--teardown-only` runs; the skill never silently chooses to leave the primary dirty or otherwise unready.
- Carries existing authorization forward. Ask only for a missing scope decision, ambiguous resolution, or an action requiring additional permission under repo policy, after completing safe preparation; do not ask the operator to reselect already authorized work.
- **Every PR is re-fetched before every decision (E).** `gh pr view` is read fresh per PR; a `mergeable` of `UNKNOWN` is polled first — GitHub recomputes mergeability for every open PR after each landing on the base, so the next PR reads `UNKNOWN` for a few seconds — up to 6 × 15s (`MERGEABLE_POLL_ATTEMPTS` / `MERGEABLE_POLL_S`, GH-736), re-reading with the transient-retry wrapper; a read that fails mid-poll ends the poll and follows the same rules as the first read (transient → deferred, anything else → stop naming the error); still undecided after that stops the run, and so does any non-transient `gh` failure (a PR whose state is unknown is never merged). A TRANSIENT network failure (DNS, refused/timed-out connection, TLS, rate limit) is retried three times first (2s, 4s between calls, GH-623); one that survives the retries DEFERS that PR — named in the end-of-run summary — and the queue continues. A hold label (`hold`, `do not merge`, `blocked`, `wip`) skips the PR (#444). A PR whose base is not the checked integration branch stops the run.
- **Pre-merge ledger gate (E.6):** the landing is simulated in a disposable full clone — PR head, then `git merge --no-ff --no-commit origin/<integration-branch>` against the integration head fetched *now* (the three-way merge keeps `MERGE_HEAD`, which the ledger resolver's generation floor reads). On a clean merge: a three-way ledger classification (a clean textual merge can still be a semantic conflict), then `releases_app.py check` and `roadmap reconcile-state --dry-run`. Any non-zero exit or `FAIL:` line is **red** and the PR is not merged; `warn:` lines, per-row identity skips and `would move` lines are diagnostics, not red.
- **Ledger-only conflicts, disjoint changes only (B1):** a conflicted landing whose unmerged set (from `git diff --diff-filter=U` + `git ls-files -u`, required non-empty with a zero-exit extraction) is within `{releases.db, releases.sql, LEADERBOARD.md, RELEASES-PREVIEW.html, LEADERBOARD.html}` is classified three-way against the merge base, per table, per key. Only when the two sides' changes are mechanically disjoint — no same-key change on both sides, no reference to a row the other side deleted, no duplicate `gh_number`, nothing outside `roadmap_items` on the replayed side — is it resolved: the side with the higher generation is kept, the other side's roadmap changes are replayed **through the writer** (`roadmap add` / `update` / `rate` / `repoint`; receipts are regenerated, gids are re-minted), then `utils/releases-merge-resolve.sh` rebuilds the DB and views, `releases check` must be clean, `git ls-files -u` must be empty, the merge commit is validated in a **second** disposable clone, and it is pushed to the PR branch only if the remote head is still the SHA that was resolved. Then the PR is re-fetched and re-gated. `harnesses.*` conflicts, code conflicts, same-key edits, deletes, inexpressible tables, a resolver refusal (generation rewind), an extraction error → **handoff** (exit 3) naming the keys; the landing clone is kept for inspection. Never an SQL union.
- **One durable attempt record per PR, at the pinned coordinator (C):** before B1 runs, the script reserves a repair slot in `<primary>/.tick/merge-cleanup/<owner>-<repo>/pr-<N>.json` — `<primary>` is the explicit `--primary` path the run started with, never a disposable clone's CWD. Every writer (this script, and each caller repair rung via `attempt_record.py`) holds `fcntl.flock` on `<record>.lock` for the whole read → reserve → write; that lock is independent of the driver's mkdir lock, so a worker under a running driver still reserves. A lock timeout **stops** the attempt (never "skipped"). Only repairs count (`B1`, `ponytail`, `start-task`); `debug-mantra`/`recon` are notes. **Two repairs per PR, whatever the head**: at the ceiling the PR is **parked** with the record path, and B1 does not run. Any handoff or park prints `export MERGE_CLEANUP_RECORD=<record>` for the caller ladder below.
- **Only HARD dependencies block on a failed predecessor (C + GH-623):** Phase 4 orders; Phase 5 keeps a runtime map of predecessor outcomes and skips a PR whose declared dependency (`depends on #N`) was handed off, parked or deferred, naming it. File-collision edges are SOFT: a collision-adjacent PR is attempted anyway and its own landing simulation decides — a genuinely conflicting successor hands off on its own merits instead of never being tried (the incident's S3 cascade: one handoff removed most of the queue). Independent PRs still land. A run with any non-landed outcome (handoff / park / defer) exits 3 after the sequence; a stop (unknown state, gate red, merge/reconcile failure, unreadable record) exits 2 immediately.
- **`--resume` continues a previous run (GH-623):** the live refresh stays first and authoritative. Only when a PR's landing actually conflicts — a repair would be needed — does the attempt record decide: at the ceiling with `--resume`, the PR is skipped as `previously parked` without re-running the B1 machinery (and without consuming a slot). A PR whose last recorded repair finished `resolved` and whose head now merges cleanly LANDS — a resume run completes a successful repair's work, never strands it. Without `--resume`, `reserve()` is the under-lock authority and the behavior is unchanged. Resume mode announces itself (`Resume mode: ...`) and the end-of-run summary breaks out parked-on-resume counts.
- Executes remote merges in topological sequence (`gh pr merge <PR_NUM> --squash --delete-branch`) — and a zero exit is not a landing: the PR is re-queried until it reads `MERGED` with a merge commit (#510 class), else the run fails.
- After each verified remote merge, performs one ordered durability sequence before looking at the next PR: **fast-forward primary → reconcile → emit `pr_merged` → commit all resulting primary-side ledger/governance writes → push `origin/<integration-branch>` → assert the primary is clean and `HEAD == origin/<integration-branch>`**. The emitter therefore runs only after both the landing fast-forward and any fast-forward performed by reconciliation; a failure at any step stops the run.
- Executes post-merge reconciliation, **gating** (a failure stops the run before emission, commit, push, the next PR, teardown, and symlink pruning; `--reconcile-pr` propagates the same exit):
  - Query the hosted `wave-reconcile.yml` run for the exact merged head and integration branch (`gh run list --workflow wave-reconcile.yml --branch <integration> --commit <merged-head>`). If it is queued or in progress, poll until completion for at most `MERGE_CLEANUP_HOSTED_WAIT_S` seconds (default 1800); timing out while it remains active stops the landing rather than racing it locally.
  - On hosted success, fetch and fast-forward the primary onto `origin/<integration>`'s reconciliation commit.
  - An empty answer inside the first `MERGE_CLEANUP_HOSTED_GRACE_S` seconds (default 60) is "not listed yet", not "no workflow" — the run for a just-pushed head can lag `gh run list` by a few seconds, and reconciling locally in that gap would race the hosted writer. After the grace window, if no hosted run/workflow/`gh` exists, or the hosted run completed unsuccessfully, fall back to `python3 utils/py/wave_reconcile.py --pr <PR_NUM>`. Never invoke that local writer while the observed hosted run is queued or in progress (`--force-local-reconcile` remains a manual recovery tool only).
  - `python3 utils/py/releases_app.py check`
  - Verify with `bash utils/pdda/pdda.sh issue-doc-sync`.

### Phase 6: Safe Teardown
- **Linked Worktrees:** Always removed via `git worktree remove <path>` from parent clone, followed by `git worktree prune` and `git worktree repair`. **Zero `rm -rf` on linked worktrees!**
- **Fresh inspection first (A.5):** the Phase 1–3 table is display. Before any removal, **every** non-exempt checkout (all `PRESERVE_*` and `SAFE_REMOVE_*` alike; only `PRIMARY_CHECKOUT`, `PRESERVED_USER_EXCLUDE`, `PRESERVE_WIKI` are exempt) is re-inspected after a fresh fetch, and only that verdict is acted on. A `PRESERVE_UNPUSHED` clone whose PR landed in Phase 5 becomes eligible here; anything that became dirty, claimed, or grew a local ref since the scan is preserved. `teardown_checkout()` refuses a record that is not a fresh Phase 6 inspection.
- **Standalone Clones:** Only removed if verified 100% clean across Phase 2 & 3, and only by moving to Trash (`~/.Trash`). If Trash is unavailable the removal is **refused** — `rmtree` is not a removal path.
- **Symlink Cleanup:** Prunes dangling skill symlinks in `~/.claude/skills/` and `~/.gemini/**/skills/`.

---

## Drive loop — how an agent runs this skill end to end (GH-623)

`/merge-cleanup` is a driven workflow, not a one-shot report. Follow the loop; do not stop at the
first refusal, do not degrade the scope silently, and do not report completion over PRs that were
never attempted:

1. **Dry run first** (Phase 0 + audit + sequence):
   `python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary "$PRIMARY" --prefix <name>`
2. **Fix the primary** so Phase 0 reports landing-ready (commit or park the dirty intake files per
   the Phase 0 rules). A dirty primary is a blocker to FIX, not a reason to silently switch to
   `--teardown-only` and still report completion (the incident's S1 false-Done). If a blocker
   cannot be resolved autonomously, report the blockers and stop — address them or report them;
   never silently truncate the task.
3. **Execute:** add `--execute`.
4. **On exit 3** (handoff / park / defer): read the printed `export MERGE_CLEANUP_RECORD=...`
   paths, work the caller ladder below for handoffs, then **re-run with `--resume --execute`** to
   continue the queue. Repeat until exit 0 or a stop. Deferred PRs (network) are named in the
   summary; they are not PR failures — re-run once the network is healthy.
5. **On exit 2**: diagnose before anything else; the diagnostic names the gate. A re-run is only
   valid once the cause is fixed.

**Done rule:** do not report Done unless Phase 5 ran to completion (exit 0; or exit 3 whose
handoffs and deferrals were worked and re-driven to exit 0), **or** the operator explicitly asked
for `--teardown-only` / `--scan-only` / `--prs-only`.

**Permission-classifier blocks:** if a harness permission layer blocks the `--execute` launch,
retry the identical command once before escalating to the operator — a block that succeeds on a
verbatim retry was non-deterministic, and surrendering the run to it is how an operator ends up
hand-driving the loop four times (the incident's S2).

## Caller decision ladder (Phase C) — what the script hands off

The script owns the evidence and the cap; the caller owns the analysis. A standalone script run never claims to have run `/recon` or `/ponytail`. Every rung starts from the handoff line's `export MERGE_CLEANUP_RECORD=<abs path>`; a worker started without it, or with a relative or unreadable path, **stops** — it never derives a record root from its own CWD.

| Rung | Skill | Budget | Record verb |
|---|---|---|---|
| 1 | `/debug-mantra` — establish the conflict as ground truth from `conflict_files` in the record | none (note) | `note --kind diagnosis` |
| 2 | `/recon`, **read-only**, over the record's conflict files only — default 8 files, 15 minutes wall-clock, consumer tracing one level out counted inside the same budget; stop and record `budget_exceeded` when hit | none (note) | `note --kind recon` / `--kind budget_exceeded` |
| 3 | `/ponytail` — the smallest reviewed resolution; "independent hunks" is not proof of independent semantics, so a code resolution lands only with caller review and tests | **1 repair** | `reserve --rung ponytail --head <sha>` … `finish --index N --outcome …` |
| 4 | `/start-task`-style handoff for semantic overlap | **1 repair** | `reserve --rung start-task --head <sha>` |
| 5 | `/unstuck` — when `reserve` exits 3 (the record already shows two repairs) | — | `show` |

`reserve` exits 0 (go; prints `index=N`), 3 (budget exhausted — go to rung 5), 2 (stopped: no/invalid record, lock timeout). Bouncing between rungs, restarting, or re-cloning never resets the count, because the record lives at the coordinator. The record is untracked state under `.tick/`; delete it by hand when the PR is closed.

## Capability table (parity guard)

Each row names who does the work; `script` rows name the test that pins them, and `test/gh534_phase_c_tests.py::TestParityGuard` fails if a row, its owner, its test, or a listed CLI option disappears.

| Capability | Phase | Owner | Pinned by |
|---|---|---|---|
| session-evidence-driver-lock | 2 | script | TestA5FailClosed.test_each_failed_git_query_preserves_naming_it |
| session-evidence-tick-claims | 2 | script | TestA4TickClaims.test_iii_claim_is_read_from_the_fold_not_state_md |
| session-evidence-open-handles | 2 | script | TestA4OpenHandles.test_ix_held_descriptor_is_active_process_naming_the_pid |
| preservation-dirty-stash-unlanded | 3 | script | TestA2Provenance.test_ii_unlanded_branch_is_preserved_naming_ref_and_commit |
| preservation-fail-closed | 3 | script | TestA5FailClosed.test_each_failed_git_query_preserves_naming_it |
| landing-refetch-and-gate | 5 | script | TestE6Gate.test_gate_red_prevents_the_merge |
| ledger-resolution-disjoint | 5 | script | TestPhase5EndToEnd.test_same_key_update_on_both_sides_is_handoff_and_nothing_is_overwritten |
| ledger-handoff-and-record | 5 | script | TestCScript.test_two_clones_one_coordinator_third_repair_is_refused |
| coordinator-pinned-to-primary | 5 | script | TestCScript.test_omitted_primary_is_refused_and_no_record_root_is_minted |
| teardown-trash-only | 6 | script | TestCScript.test_teardown_refuses_without_trash |
| dependents-blocked | 5 | script | TestCScript.test_dependent_of_a_handed_off_pr_is_not_attempted_and_an_independent_pr_proceeds |
| soft-edge-nonblocking | 5 | script | TestGh623Resilience.test_soft_edge_predecessor_does_not_block_a_collision_dependent |
| network-retry-defer | 5 | script | TestGh623Resilience.test_transient_view_failure_defers_and_independents_land |
| resume-skips-parked | 5 | script | TestGh623Resilience.test_resume_skips_a_still_conflicting_exhausted_pr |
| reconciliation-gating | 5 | script | TestCScript.test_two_ledger_prs_emit_only_after_fast_forward_and_finish_durable |
| code-conflict-recon | 5 | caller | — |
| code-conflict-resolution | 5 | caller | — |
| teardown-fresh-inspection | 6 | script | TestA5FreshInspection.test_teardown_refuses_a_stale_scan_record |
| mergeable-unknown-poll | 5 | script | TestPhase5EndToEnd.test_unknown_mergeable_settles_and_the_pr_lands |
| exclude-drops-pr | 4 | script | TestPhase5EndToEnd.test_exclude_pr_number_drops_it_from_the_queue |

CLI options this document describes and the guard asserts exist: `--primary`, `--root`, `--prefix`, `--exclude`, `--strategy`, `--scan-only`, `--prs-only`, `--teardown-only`, `--reconcile-pr`, `--integration-branch`, `--allow-unready-primary`, `--execute`, `--resume`.

## CLI Usage

Run scripts directly from the skill directory or via python:

```bash
# 1. Full Dry-Run Inspection (Default)
python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary "$HOME/Documents/GH Repos/XYZ-forge" --prefix XYZ-forge

# 2. Audit Only (Scan Clones and Worktrees)
python3 skills/2-daily/merge-cleanup/scripts/scan_clones.py --prefix XYZ-forge

# 3. PR Topological Sequencing
python3 skills/2-daily/merge-cleanup/scripts/toposort_prs.py

# 4. Execute Full Sequence (Merges, Reconciliation, and Teardown)
python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary "$HOME/Documents/GH Repos/XYZ-forge" --prefix XYZ-forge --execute

# 5. Teardown Only (Clean Clones/Worktrees without merging PRs)
python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary "$HOME/Documents/GH Repos/XYZ-forge" --prefix XYZ-forge --teardown-only --execute

# 6. Exclude Active In-Flight Work (e.g. PR 427)
python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary "$HOME/Documents/GH Repos/XYZ-forge" --prefix XYZ-forge --exclude 427 --execute

# 7. Caller repair rung (Phase C): the handoff line printed the record path
export MERGE_CLEANUP_RECORD=/abs/primary/.tick/merge-cleanup/HiQS-Labs-XYZ-forge/pr-538.json
python3 skills/2-daily/merge-cleanup/scripts/attempt_record.py note --kind diagnosis --text "same-key update on gh_number 100"
python3 skills/2-daily/merge-cleanup/scripts/attempt_record.py reserve --rung ponytail --head <sha> --clone "$PWD"   # exit 3 → /unstuck
python3 skills/2-daily/merge-cleanup/scripts/attempt_record.py finish --index 0 --outcome resolved

# 8. Continue a previous run after repairs or a network outage (GH-623)
python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary "$HOME/Documents/GH Repos/XYZ-forge" --prefix XYZ-forge --resume --execute
```

---

## Safety Guarantees

1. **Zero Data Loss:** Any dirty working tree, unpopped stash, or unlanded commit automatically stops deletion and marks the checkout `PRESERVE_*`, naming the files or refs. The primary checkout is inspected first and by identity, so it can never be skipped by a scan filter. Anything the scanner cannot prove is preserved, naming the failed query.
2. **No Silent Primary Deferral:** every executing run refuses before merge, teardown, or symlink mutation while the primary is unready; only the operator can defer primary cleanup with `--allow-unready-primary`.
3. **Zero Process Interference:** Clones with active driver locks, active tick claims (from the event fold), or open file handles are detected and preserved; an unverifiable session is preserved too.
4. **Canonical Worktree Protocol:** Linked worktrees are always cleanly deregistered from git metadata.
5. **Governed Landing:** Every PR is gated on the ledger against the current integration head before it merges, verified `MERGED` after, then fast-forwarded, reconciled, emitted, committed, pushed, and verified clean/equal to the remote integration head before the next PR is looked at; any failure stops the run.
6. **Bounded Repair:** every repair attempt on a PR — the script's B1 and each caller rung — is counted in one record at the pinned coordinator under one lock; the third is refused wherever it starts, and a dependent of a parked PR is never attempted.
