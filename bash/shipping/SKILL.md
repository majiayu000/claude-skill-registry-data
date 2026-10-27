---
name: shipping
description: >
  Internal ACE turn step — Ship an ACE change: branch → PR → wait → merge → verify it landed.
user-invocable: false
disable-model-invocation: false
---

# Shipping — ACE (stub over the fleet-canonical core)

How an ACE change gets from a worktree edit to merged `main`, and specifically **how to wait for
the PR without burning the turn**. The procedure is fleet-wide; this stub binds it to ACE.

1. **Resolve the installed canopy plugin and check freshness:**
   ```bash
   CANOPY=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['canopy@canopy'][0]['installPath'])")
   bash "$CANOPY/scripts/canopy-update-check.sh"
   ```
   `UPGRADE_AVAILABLE` → tell the human and run `/canopy:update` BEFORE following a stale core.
2. **Read `$CANOPY/agent-core/shipping.md`** and **follow it exactly**, bound to the ACE facts
   below. Step 0 (does this repo even have PR checks?) is the step that pays — run it before any
   wait. Step 3's ship checkpoint is unconditional.

Every ACE agent that opens a PR delegates here: the orchestrator's fix-and-ship dispatches, the
self-heal convention (`CLAUDE.md § Self-heal a filed issue`), `iterate-loop`, and any turn that
lands a repo change. Do not reimplement the wait inline.

## ACE repo facts (measured 2026-08-17 — the core's Step 0 row for this repo)

| Fact | Value | Re-derive |
|---|---|---|
| Workflows on `pull_request` | `clean-install.yml`, `version-check.yml` | `grep -l pull_request .github/workflows/*` |
| **Required** check | **`clean-install` only** | `gh api repos/dimagi-internal/ace/branches/main/protection --jq .required_status_checks.contexts` |
| `enforce_admins` | `true` — no `--admin` force-merge | same call, `.enforce_admins.enabled` |
| Auto-merge | **enabled** | `gh api repos/dimagi-internal/ace --jq .allow_auto_merge` |
| Merge queue | **LIVE since 2026-09-07T13:58:52Z** — ruleset `main-merge-queue` (id 22456030), `MERGE` / max-merge 1 / max-build 5 / ALLGREEN | `gh api graphql -f query='{repository(owner:"dimagi-internal",name:"ace"){mergeQueue(branch:"main"){id}}}'` — `null` means none |
| Typical create → merge | **~6 minutes through the queue** (was ~70s before it) — PR #2154, the first live queued PR: created 14:09:30Z, merged 14:15:23Z | `gh pr list --state merged --limit 5 --json number,createdAt,mergedAt` |

`version-check` runs on every PR but is **not** required — a red `version-check` will not block the
merge, so read it rather than assuming the merge is stuck on it.

**The merge-queue row's old re-derive was a FALSE PROBE — do not reuse it.** It read
`gh api repos/dimagi-internal/ace --jq .merge_queue_enabled` and concluded "none" from `null`. There
is no such field on the repos payload, so it returns `null` whether or not a queue exists:

```
$ gh api repos/dimagi-internal/ace --jq 'has("merge_queue_enabled")'
false
```

A probe that answers `null` for both states cannot distinguish them, and this one would have kept
saying "no queue" the day after one was switched on. The GraphQL form in the table is the real
probe (verified 2026-09-07 — `repository.mergeQueue(branch:"main")` returned `null` before the queue
was created and returns the queue object after, and `pullRequest.isMergeQueueEnabled` is the per-PR
equivalent `gh` itself reads). The false probe now answers `false` while the real one answers with a
queue id — exactly the divergence it was retired for.

## The ACE ship loop

```bash
git checkout -b <branch>
BRANCH="$(git branch --show-current)"          # RECORD it — see the note below
... make the edits ...
bash scripts/version-bump.sh --expect-branch "$BRANCH"   # refuses if HEAD moved
git add -A && git commit -m "<type>(<scope>): <what>"
git push -u origin "$BRANCH"
gh pr create --fill                   # origin is the ACE repo; no -R needed
gh pr merge <N> --auto --merge        # arm it, then wait per the core's Step 1
```

Arm auto-merge in the same breath as creating the PR — once armed there is no review gate, so
everything between arming and merging is waiting.

**Why the branch is recorded and re-asserted (ace#2001).** A dispatched subagent inherits its
dispatcher's working directory, so a fix-and-ship agent launched without `isolation: "worktree"`
runs this whole loop **inside the orchestrator's worktree, concurrently with the orchestrator**.
Measured on `poverty-graduation/20260905-0924`: a Phase 1 subagent's `git checkout -b` at 09:48:13
moved the branch under a live `/ace:run`, and the orchestrator's next commit at 10:08:16 landed on
the subagent's branch — PRs #1995 and #1999 still carry the same head branch under unrelated
titles. Nothing errored; both actors run `git add -A`, which cannot tell whose file it is staging,
and only a happens-to-be-clean tree kept the two commits from swallowing each other. `git branch
--show-current` + `--expect-branch` turns that into an `exit 4` **before** the `git add -A`, and
catches both sides — the agent that checked out under someone and the one checked out from under.
It is a backstop, not the fix: the fix is `isolation: "worktree"` on the dispatch
(`agents/orchestrator-reference.md § Dispatch it into its OWN worktree`). *Enforced:*
`test/agents/fix-and-ship-isolation.test.ts` + `test/scripts/version-bump-expect-branch.test.ts`.

## ACE-local notes (the ONLY hand-edited section — fleet-process changes go to canopy)

- **Post-merge is mandatory: run `/ace:update` in this session.** Without it this session runs
  stale code while new sessions get the bump. This is ACE's instance of the core's "reconcile the
  running session" step.
- **A PR/issue body longer than one line goes in a UNIQUELY-NAMED file in your OWN subdirectory of
  this session's scratchpad. Both halves are load-bearing.**

  ```
  <scratchpad>/agent-<issue>/pr-body-<issue>-<slug>.md     e.g. .../agent-2019/pr-body-2019-basenames.md
  <scratchpad>/agent-<issue>/issue-<issue>-<slug>.md
  ```

  *Never `/tmp/pr-body.md`* — `/tmp` is shared across every session, worktree and macOS account on
  the host, so a predictable name may already hold someone else's file and `gh` publishes it
  silently (ace#1818; then ace#1819 again on 2026-09-05, when PR #1989 shipped 4,912 bytes of an
  unrelated 4-day-old session's file).

  *And never a generic name in the scratchpad either* — **the scratchpad is not private.** Every
  concurrent subagent of a session shares ONE directory and it survives restarts, so two agents in
  one dispatch batch invent the same name and silently overwrite each other. Measured 2026-09-05
  (ace#2019): a subagent's `<scratchpad>/pr1-body.md` was overwritten ~8 minutes later by a sibling
  from the same batch; it had already published, so the ordering was luck. That directory today
  holds ten generic basenames (`pr-body.md`, `pr1-body.md`, `pr1body.md`, `pr2-body.md`,
  `issue587.md`, `body589.md`, …) from at least four sessions over five days. **Digits alone are not
  a distinguisher** — `pr1-body.md` (a counter) and `pr-body-2019.md` (an issue number) are the same
  shape to a sibling; add a word.

  **Do not `cp`/`mv` an existing body file to a legal name** — not from shared `/tmp` (that is the
  exact move that published #1989's wrong body) and not from a generic scratchpad name (whatever is
  in it may be a sibling's body, not yours). Re-author it. Two `config/gating.json` deny rails
  enforce both halves (*enforced:* `test/hooks/gating-guard.test.ts`).

  Authoring the body with the `Write` tool sidesteps the whole class: the rails are Bash-scoped, and
  a heredoc that *quotes* one of these invocations is denied along with one that runs it.

  **Read every published body back from GitHub before moving on** — `gh pr view <n> --json body`.
  Both incidents were caught that way, and in #2010's case the read-back is the only reason we know
  the right body shipped.
- **Touched `mcp/`, or ran `/ace:setup --force-env`? Quit and reopen Claude Code.**
  `/ace:update` + `/reload-plugins` do NOT respawn MCP subprocesses — they bind their tool list,
  schemas, and env at spawn. See `CLAUDE.md § MCP changes need a full Claude restart`. Otherwise
  `/reload-plugins` is enough.
- **Version collision** (from a parallel worktree bump) — **disarm
  auto-merge FIRST, or the recovery races the merge and silently loses** (ace#1593):
  ```bash
  gh pr merge <N> --disable-auto              # STOP the race before touching the branch
  bash scripts/version-bump.sh --rebase-first # auto-resolves the 4 version files
  git push --force-with-lease
  gh pr merge <N> --auto --merge              # re-arm only after the corrected VERSION is pushed
  ```
  Then re-enter the wait. `--rebase-first` aborts cleanly if a non-version file conflicts — those
  need human review.

  **Do NOT wait for `mergeStateStatus: DIRTY` — the common collision never shows it** (ace#2175).
  Two PRs bumping to the SAME version write byte-identical VERSION files, so git merges them
  cleanly and there is no conflict to see; `check-version-unique` catches it instead, inside
  `clean-install`, and the PR sits at **`BLOCKED`**. Measured 2026-09-07 on #2166 (vs the older
  #2165, both `0.13.1325`): `state=OPEN mergeState=BLOCKED auto=MERGE`, stable — while `land-pr.sh`,
  which then keyed only on DIRTY, polled it silently for ten minutes. It now classifies a BLOCKED
  PR before deciding: `scripts/land-pr-classify.ts` re-derives the verdict from
  `lib/version-uniqueness.ts` (the same functions CI runs) and the rebase fires only on a positive
  collision — never on BLOCKED alone, which also covers a red test, a pending check and a missing
  review. *Enforced:* `test/lib/land-pr-classify.test.ts` and `test/scripts/land-pr-classify.test.ts`
  assert both directions; `land-pr-refspec.test.ts` drives the whole disarm→rebase→push→re-arm
  sequence on a BLOCKED collision and asserts a BLOCKED failing test is left untouched.

  **`main` HAS a merge queue, so this block is wrong for a QUEUED PR** — `--disable-auto` exits 0
  without disabling anything, so the force-push races a merge group that is already testing the old
  head. Check `mergeQueueEntry` first, or just use `scripts/land-pr.sh`, which does. See
  § When the merge queue goes live.

  **ONE pass often loses the race — use `scripts/land-pr.sh <pr>` rather than doing this by
  hand.** The block above is correct and incomplete: it assumes that by the time you have
  rebased, `main` has not moved again. Measured 2026-09-05 on PR #1962, `main` merged at 06:45,
  06:47, 06:57, 07:13, 07:14, 07:19 and 07:21 — every 2-4 minutes, several sibling sessions
  shipping at once — while a rebase plus `clean-install` takes 1-3 minutes. That PR returned to
  DIRTY twice; four PRs in one session hit it. The script is this recipe in a bounded retry loop,
  and it keeps the disarm/re-arm ordering above, which a hand-rolled loop forgot on the first
  attempt (it landed anyway, purely because CI had not yet greened the pre-rebase head — luck,
  not method). *Enforced:* `test/scripts/land-pr.test.ts` ratchets the disarm-before-rebase
  order; `test/scripts/land-pr-refspec.test.ts` ratchets that the push targets the PR's
  `headRefName` rather than the local branch name (ace#1974 — a bare `HEAD` refspec pushed a
  stray branch and exited 0, so the script re-armed a PR it had not updated). It still does not
  excuse you from reading the merge state yourself afterwards.

  **The script arms auto-merge itself, and is safe to run whether or not you already did.**
  Until ace#2004 its only `--auto --merge` sat inside the DIRTY branch, so it armed purely as a
  side effect of losing a version race: a PR that was CLEAN on the first read got polled to
  exhaustion for a merge nothing would perform. The failure was inversely correlated with
  contention — a busy `main` hid it, the quiet run hung — which is why it survived three
  revisions. Arm at PR-create time anyway (line above): it costs nothing, `gh pr merge --auto`
  is idempotent, and it merges the PR the moment checks green even if you never reach the
  script. *Enforced:* `land-pr.test.ts` pins one unconditional arm site ordered after the
  ancestry guard; `land-pr-refspec.test.ts` drives a CLEAN-on-first-read PR end to end.

  **Why the disarm step is load-bearing.** Auto-merge stays armed while you rebase, and
  `clean-install` (the only REQUIRED check) can go green on the **pre-rebase head** first. The
  merge then wins the race and your `--force-with-lease` is a no-op against an already-merged
  branch. The PR lands carrying the OLD version, `main` shows the same VERSION before and after,
  and because the plugin cache is keyed by version, `/ace:update` can never reach the change.
  Measured 2026-08-24: 4 of ~20 PRs in one sweep collided; the 3 that left auto-merge armed all
  needed a follow-up bump PR (#1597, #1598, #1588); the 1 that disarmed first (#1601) did not.
  `check-version` does NOT save you here — it is advisory, not required.
- **After ANY merge, verify the version actually advanced** — `state: MERGED` is not sufficient:
  ```bash
  git fetch origin main -q && git show origin/main:VERSION
  ```
  If it did not advance past your base, ship an immediate follow-up bump PR and say so in your
  report. An agent that trusts `state=MERGED` alone will report success and leave an unreachable
  fix on `main` (ace#1593).
- **From a worktree, drop `--delete-branch`** — `main` is checked out elsewhere.
- **Shipped into CANOPY? Reinstall the canopy CLI before your next email send.** Merging a
  canopy PR bumps the marketplace clone's VERSION, and the send path is the **`uv`-installed
  `canopy`**, not the plugin cache — so the moment your own bump lands, the installed engine
  lags the clone and `canopy email send` refuses at send-time with an engine-staleness error.
  A turn that ships a canopy fix and *then* tries to reply breaks its own send path, and the
  error names versions rather than the merge that caused it, so it reads as unrelated:
  ```bash
  (cd ~/.claude/plugins/marketplaces/canopy && git pull) \
    && uv tool install --reinstall ~/.claude/plugins/marketplaces/canopy
  canopy --version    # must equal the clone's VERSION
  ```
  `/ace:doctor`'s `canopy_email_engine` probe reports the gap and prints this same command;
  the point of the note is that shipping to canopy is what CREATES the gap, so do it after the
  merge rather than discovering it at the send. (Measured this turn, 2026-09-05: the machine
  started at CLI 0.2.471 vs clone 0.2.472 with the send already blocked; merging canopy#609
  moved the clone to 0.2.473 and would have re-blocked it a second time.)
- **Self-heal PRs additionally close their issue** referencing the PR, then re-run the blocked
  step (`CLAUDE.md § Self-heal a filed issue`).

  **And their ship checkpoint carries one extra line: `Remedy: as-filed | re-derived | refuted`,
  plus what you RAN.** The issue's premise is verified by its filer; its *suggested fix* is
  verified by nobody, and that is the half that fails — measured 2026-08-29..09-06 as **wrong**
  (ace#2004: the proposed one-line hoist would have armed and merged a stranger's PR),
  **under-scoped** (ace#2027), **no-op** (ace#1768), **stale** (ace#1766, fixed the day after
  filing). Two checks cover all four, and both are cheap: re-read the cited `file:line` against
  `git show origin/main:<path>` rather than the issue's quote, and *execute* the remedy — count a
  proposed matcher's hits on real input, apply a proposed edit and read what the surrounding code
  then needs. `as-filed` without a ran-command is not `as-filed`. Full contract + the four-shape
  table: `agents/orchestrator-reference.md § The filed remedy is a lead, not an instruction`
  (ace#1900). *Enforced:* `test/skills/remedy-verification-contract.test.ts`.

## The merge queue (LIVE)

**`main` has had a merge queue since 2026-09-07T13:58:52Z** — ruleset `main-merge-queue`, id
`22456030`, `enforcement: active`. It closes ace#1776 (VERSION uniqueness is checked but never
re-checked at merge time) and ace#1914 (VERSION contention is 20% of all `clean-install` runs):
`clean-install` now runs against the exact base each PR lands on, so a version collision can no
longer be a race.

It was deliberately **not** a flag day — the tooling below shipped first (PR #2151, merged 13:56Z)
and was inert until the ruleset was created two minutes later, because a session already running
keeps using the copy of these files it loaded. Undo, if it is ever needed, is one command:
`gh api -X DELETE repos/dimagi-internal/ace/rulesets/22456030` — and `land-pr.sh` degrades to its
pre-queue behaviour when the queue read comes back empty, by design.

**What changes for you: almost nothing.** Keep arming with `gh pr merge <N> --auto --merge` and keep
landing with `bash scripts/land-pr.sh <pr>`. Under a queue `gh` only prints a warning
(`The merge strategy for main is set by the merge queue`) and arms anyway — it is a warning on
stderr, not an error, and the queue's own configured method wins. Do **not** "helpfully" drop
`--merge`: without a queue, `--auto` with no strategy is a hard failure in a non-interactive shell
(`--merge, --rebase, or --squash required when not running interactively`), so the conditional form
strands a PR unarmed the moment detection is wrong in the safe-looking direction.

**What changes for the script:** `land-pr.sh` reads `pullRequest.mergeQueueEntry` once per attempt
(GraphQL — `gh pr view --json` carries no queue field) and, when the PR is IN the queue, does
nothing to it: no disarm, no rebase, no force-push. It polls, prints the queue position, and exits
**5** rather than 3 if the queue wait (`ACE_LAND_PR_QUEUE_WAIT`, default 1800s) runs out. Queued
time does not consume a rebase attempt. *Enforced:* the `merge queue` blocks in
`test/scripts/land-pr.test.ts` and `test/scripts/land-pr-refspec.test.ts`, which models a queued PR
in its `gh` stub.

**The one thing you must never do by hand: `gh pr merge <N> --disable-auto` on a QUEUED PR.** It
looks like it worked and it did not. `gh`'s `mergeRun` checks `inMergeQueue()` *before* the
disable branch (cli/cli v2.88.1 `pkg/cmd/pr/merge/merge.go:543-553`), returns
`ErrAlreadyInMergeQueue`, and the command maps that to `return nil` (`merge.go:167`) — so it prints
"already queued to merge" and **exits 0 without disabling anything**. The hand-rolled collision
recipe above (disarm → rebase → force-push → re-arm) therefore becomes *actively wrong* on a queued
PR: you would force-push over a head whose merge group is already under test, which is ace#1593's
shape again. If a queued PR genuinely has to come out, remove it from the queue in the PR's own UI
(or `gh api graphql` `dequeuePullRequest`), then recover — do not trust `--disable-auto` to have
done it.

**The rebase-on-DIRTY path is NOT retired by the queue, and should not stand down.** A queue rebases
speculatively, but it cannot resolve a real conflict: *"if there are failed required status checks
or conflicts with the base branch, the pull request will be removed from the queue"* (GitHub docs,
managing-a-merge-queue). A VERSION collision is a conflict, so it still surfaces as `DIRTY` — it
just arrives as an ejection rather than a stalled auto-merge, and the rebase is still exactly what
un-sticks it. What the queue removes is the *`BEHIND`-but-clean* case, which this script never
rebased on anyway.

**Two settings the queue needs, or it makes things worse rather than better:**

1. **`clean-install.yml` must trigger on `merge_group`** — shipped here already. GitHub: *"You must
   use the `merge_group` event to trigger your GitHub Actions workflow when a pull request is added
   to a merge queue" … "The merge will fail as the required status check will not be reported."*
   `clean-install` is `main`'s only required check, so without it every enqueued PR waits for a
   check that is never dispatched.
2. **Set the queue's "maximum pull requests to merge" to 1.** Two PRs that both bump `0.13.1099 →
   0.13.1100` make byte-identical VERSION edits, so grouped together they merge cleanly and the
   group's VERSION *does* advance past 1099 — the check passes, both land, and `main` shows 1100
   twice. That is ace#1776 surviving the fix. One PR per group makes the second PR's group read
   1100 against an `origin/main` already at 1100, which is correctly rejected.

**OBSERVED on the first live queued PR — #2154, 2026-09-07.** The three checks this section used to
list as unsettled were run against the real queue. Two confirmed; the third turned out to be
untestable as written, which is itself the finding.

Full transition, 14:09:30Z create → 14:15:23Z merged:

```
14:09:52  state=OPEN   mergeState=BLOCKED  inQueue=false  auto=MERGE   entry=null
14:12:17  state=OPEN   mergeState=CLEAN    inQueue=true   auto=null    entry={position:1, state:QUEUED}
14:12:38  state=OPEN   mergeState=CLEAN    inQueue=true   auto=null    entry={position:1, state:AWAITING_CHECKS}
14:15:23  state=MERGED                     inQueue=false  auto=null    entry=null
```

1. **`clean-install` does report against the queue ref — CONFIRMED.** A `merge_group` run of
   `Clean install + dep check` dispatched on
   `gh-readonly-queue/main/pr-2154-0a878af683b01c5037c320171ee99d959db7c8f9` and concluded
   `success`. The `merge_group` trigger is load-bearing exactly as documented: without it that run
   does not exist and the PR waits forever on `main`'s only required check.
2. **`land-pr.sh` polls rather than rebasing — CONFIRMED**, verbatim from its log:
   ```
   attempt 1/5: state=OPEN mergeable=BLOCKED queue=true queued=false entry=- pos=-
     auto-merge armed
   attempt 2/5: state=OPEN mergeable=CLEAN queue=true queued=true entry=QUEUED pos=1
     in the merge queue (entry=QUEUED position=1) — waiting; this attempt is not consumed
   merged from the queue
   ```
   Exit 0, two attempts consumed for the whole landing, no disarm and no force-push.
3. **The `--disable-auto` check is UNTESTABLE as it was written, because enqueueing CONSUMES the
   auto-merge request.** `autoMergeRequest` is `MERGE` while the PR is `BLOCKED` and **`null` from
   the moment it enters the queue** (see the transition table). The old wording — "exits 0 while
   `autoMergeRequest` stays non-null" — presumes a live auto-merge request to leave un-disabled, and
   on a queued PR there is none. Nothing was run against the live merge group to test it; a
   mutating command on a real merge group is not worth a checklist tick.

   **The hazard is unchanged and still stands.** `gh` returns `ErrAlreadyInMergeQueue` from
   `inMergeQueue()` before the disable branch and maps it to `return nil` (`merge.go:543-553`,
   `:167`), so the call exits 0 on a queued PR either way — and the destructive half was never the
   disarm, it was the `--force-with-lease` that the hand-rolled recipe runs next, over a head whose
   merge group is already under test. Keep using `scripts/land-pr.sh`, which reads
   `mergeQueueEntry` first.

**A practical consequence of #3 worth knowing before you debug one:** *`autoMergeRequest: null` on a
queued PR is normal, not a PR that lost its arm.* Read `mergeQueueEntry` / `isInMergeQueue` before
concluding a PR needs re-arming — re-arming a queued PR is the move that leads back to the
force-push hazard above.

**Still unobserved:** an *ejection* (a VERSION collision surfacing as removal from the queue rather
than a stalled auto-merge), and any group with more than one entry. #2154 was alone in the queue at
position 1 with zero other open PRs, so the contention path this queue was built for has not yet
run. The rebase-on-`DIRTY` recovery above is what covers it — do not let a clean first landing
argue for retiring it.

## MCP Tools Used

None. `git` + `gh` only.

## Mode Behavior

- **Auto / autonomous run:** run the full loop without prompting. Shipping is not a pause point —
  the PR is a CI checkpoint, not a review gate.
- **Review / interactive:** identical mechanics; the operator sees the ship checkpoint line.
- **Dry-run:** stop after `gh pr create`; do not arm auto-merge. Report `state=OPEN` and say
  auto-merge was deliberately not armed.

## Related skills

- `agent-turn-review` — gates the *report* about the merge, never the merge itself.
- `agents/orchestrator-reference.md § Fix-and-ship subagent template` — the dispatch wrapper.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-08-17 | Initial version. Created because ACE had no shipping skill and hand-rolled the wait every time — the canonical `until … sleep 30; done` template in `orchestrator-reference.md` prescribed a shape the harness blocks, and the fallback burned the full 10-min Bash timeout (`Exit code 143`) waiting on PRs that merge in ~70s. | ACE team |
| 2026-09-07 | **Merge-queue aware, ahead of the queue being enabled** (prereq for ace#1914/#1776). `land-pr.sh` detects `mergeQueueEntry` and never disarms/rebases/force-pushes a queued PR — `gh pr merge --disable-auto` is a silent no-op on one (`merge.go:543`), so the old recipe would have force-pushed over a live merge group. Queued time no longer consumes a rebase attempt and reports as progress (exit 5). `clean-install.yml` gains the `merge_group` trigger it cannot function without, and its VERSION assertion now also runs on the merge group. Also corrected the repo-facts table's merge-queue re-derive, which read a field that does not exist and answered "none" unconditionally. | ACE team |
| 2026-09-07 | **The queue went live, and the first PR through it replaced inference with measurement.** The repo-facts row said "none yet" from 13:58Z onward — a table read at the top of every ship. Corrected against ruleset `main-merge-queue` (id 22456030) plus the observed transition of PR #2154 (create 14:09:30Z → merged 14:15:23Z, ~6 min vs ~70s pre-queue). Two of the three recorded falsifiers CONFIRMED verbatim: `clean-install` dispatched on `merge_group` against `gh-readonly-queue/main/pr-2154-…` and concluded success, and `land-pr.sh` printed `in the merge queue (entry=QUEUED position=1) — waiting; this attempt is not consumed` and exited 0 without disarming or force-pushing. The third was **untestable as written**: enqueueing CONSUMES the auto-merge request (`autoMergeRequest` goes `MERGE` → `null` on entry), so there is no live arm for `--disable-auto` to leave un-disabled — added the practical corollary that `autoMergeRequest: null` on a queued PR is normal and must not be read as a lost arm, since re-arming leads back to the force-push hazard. Ejection and multi-entry groups remain unobserved and are called out as such. | ACE team |
| 2026-08-17 | **Converted to a stub over `canopy agent-core/shipping.md`** (canopy #498). The mechanics were fleet-shared — hal, eva and ACE had each written their own copy — so they were promoted to a first-class agent-core body alongside `turn.md` / `task-tracker.md`, and `turn.md`'s duplicated block was cut (444 → 399 lines). What stays here is only what is ACE-specific: the measured Step 0 row, the version-bump loop, `/ace:update` + the MCP-restart rule, and the `--rebase-first` collision recipe. Fleet-process changes now go to canopy, not here. | ACE team |
