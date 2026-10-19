---
name: aule
description: Use when the user runs /aule <tracker> <project> [--filter <id-or-jql>] [--max N] [--ready] [--auto] [--dry-run] [--confirm]. Sweeps a project for tickets bearing an approved counsel awaiting the forge ([COUNSEL] + [FORTH], no [GWAITH]), takes the first N qualifiers (default 3), and dispatches /celebrimbor per ticket. Also closes already-forged tickets whose PR/MR has since merged — moving them to the project's merged= state and threading a [METTA] note. Each invocation forges N; re-running picks up the next N, with the tracker itself as the bookmark via the no-[GWAITH] gate. Hard cap by default — bulk-forge has a real blast radius. --auto forges the manifest without the outer confirmation.
purpose: Sweeps a project for approved-but-unforged tickets and dispatches the forge on each.
user_invocable: true
stage: forge
composes: celebrimbor:dispatch
---

# Aulë — The Master Smith

Aulë the Vala wrought the world's bones and taught the elven smiths their craft; in dwarvish tongue he is Mahal, the maker of the Seven Fathers. So this skill: where Celebrimbor forges one approved counsel into one PR/MR, Aulë walks the qualifying tickets in a project and dispatches Celebrimbor at each in turn — bounded, gated, and bookmarked by the tracker's own marks.

## Ethos

- **Aulë directs; Celebrimbor still forges.** Per-ticket behavior matches `/celebrimbor --ticket <id>` exactly. Aulë never opens a PR/MR Celebrimbor would not.
- **Bounded by default.** `--max N` defaults to **3**. Bulk-forge writes to four places per ticket (branch, PR/MR, ticket comment, optional state transition); a runaway sweep multiplies fast.
- **The tracker is the bookmark.** Celebrimbor posts `[GWAITH]` after each forge; the gate excludes already-forged tickets on the next run. No state file, no offset — re-run `/aule` to pick up the next N.
- **One outer gate, on by default.** The manifest stands before the user, who approves the whole sweep once. The slash invocation alone is not authority; `--dry-run` passes the gate by dispatching nothing, and `--auto` passes it by the user's explicit word at invocation — the flag itself is the approval, given in advance for whatever the manifest holds.

## Argument parsing

`/aule <tracker> <project> [--filter <filter>] [--max N] [--ready] [--auto] [--dry-run] [--confirm]`

| Argument | Required | Meaning |
|---|---|---|
| `<tracker>` | yes | `youtrack` (alias `yt`) or `jira` |
| `<project>` | yes | Project shortName / key (e.g. `MET`, `PSG`) |
| `--filter <filter>` | no* | Same semantics as `/glorfindel` and `/celebrimbor` |
| `--max N` | no | Cap on forges per invocation. Default 3. Refuse `N < 1`; cap at 10 with a warning. |
| `--ready` | no | Open each PR/MR as ready-for-review (default: draft). Propagated to every `/celebrimbor` dispatch. |
| `--auto` | no | Forge the manifest without the outer confirmation — render it, then dispatch straight through. The flag is the approval, given in advance. Refuse when combined with `--dry-run` or `--confirm` (they contradict it). |
| `--dry-run` | no | Render the manifest, never dispatch Celebrimbor. |
| `--confirm` | no | Propagate `--confirm` to each `/celebrimbor` dispatch (per-ticket prompt before PR-open). Use to stop mid-sweep. |

*If `--filter` is omitted, follow the same resolution order as `/glorfindel`: explicit > `default_filters.md` keyed by `<tracker>:<project>` > stop with an error naming the missing key.

## Tracker routing

Same as `/glorfindel` and `/celebrimbor`:

| Tracker | List hook | Fetch hook |
|---|---|---|
| `youtrack` / `yt` | `~/.claude/hooks/glorfindel-youtrack-list.sh` | `~/.claude/hooks/council-youtrack-fetch.sh` |
| `jira` | `~/.claude/hooks/glorfindel-jira-list.sh` | `~/.claude/hooks/council-jira-fetch.sh` |

Per-ticket dispatch invokes `/celebrimbor` via the Skill tool; the forge hook (`forge-github-pr.sh` / `forge-gitlab-mr.sh`) is Celebrimbor's own concern.

## Workflow

### 1. Pre-flight

a. **Tracker dispatch.** Apply the council hybrid dispatch (see `skills/council/SKILL.md`) to bind `<list-hook>` and `<fetch-hook>` for the chosen tracker.

b. **Filter resolution.** Per `/glorfindel`'s rule — explicit `--filter` wins; otherwise read `default_filters.md` for `<tracker>:<project>`; otherwise stop with: *"No filter specified and no entry for `<tracker>:<project>` in `default_filters.md`. Pass `--filter <value>` or seed the memory file."*

c. **`--max` sanity.** If `--max N` was passed: refuse `N < 1` with *"--max must be a positive integer."* Cap at 10 silently with a one-line warning if `N > 10` (*"Aulë holds the bellows steady — capped at 10 per sweep; pass --max again or re-run."*); the default of 3 stands when `--max` is omitted.

d. **Flag-conflict check.** If `--auto` is combined with `--dry-run` or `--confirm`, stop with *"--auto contradicts --dry-run/--confirm — pick one intent."* One flag asks to forge unattended; the others ask to hold back. Aulë does not guess which the user meant.

e. **Jira post-safety warning.** Same rule as `/glorfindel` — if `<tracker>` is `jira` and none of `--auto`, `--dry-run`, or `--confirm` is set, AskUserQuestion before proceeding with three options (proceed unattended / re-run with `--confirm` / re-run with `--dry-run`). Forge writes are public on Jira; the warning is hard-earned. Stop unless the user picks "proceed unattended". `--auto` skips the prompt — the flag *is* the deliberate intent the warning exists to confirm.

There is **no clean-tree gate** on the source repo — Celebrimbor acquires its own isolated workspace per ticket inside its own dispatch.

### 2. Build the qualifier set

Invoke the list hook:

```bash
<list-hook> <PROJECT> <FILTER>
```

Parse the JSON. On error or wrapped-truncation, surface the message and stop. (Truncation on a forge sweep is a sign the filter is too broad — the user narrows it before bulk-forging.)

For each ticket in the list, fetch its thread:

```bash
<fetch-hook> <ticket-id>
```

**YouTrack rung dispatch.** For each listed ticket, run the decider:

```bash
~/.claude/hooks/council-youtrack-fetch.sh <ticket> | ~/.claude/hooks/skeleton-rung.py
```

Map the action to a dispatch:

| action | Dispatch |
|---|---|
| `draft_skeleton`, `redraft_skeleton`, `answer_skeleton` | `/celebrimbor youtrack <project> --ticket <id> --skeleton` |
| `forge` | `/celebrimbor youtrack <project> --ticket <id>` |
| `draft_plan`, `redraft_plan`, `answer_plan` | `/council youtrack:<id>` (plan rung — or leave to `/glorfindel`) |
| `done` | close-watch — forged, not yet closed; check the PR/MR for merge (step 5b) |
| `await_start` | skip — dormant, no `[MELLON]` summons yet (counted in the report) |
| `await_plan`, `await_skeleton`, `at_rest` | skip (no-op) |

The `answer_*` actions route to the same sub-skill as their rung's draft/redraft;
the sub-skill re-runs the decider and takes its own answer path (post `[PEDO]`,
advance the watermark, leave the plan/skeleton standing). Aulë needs no special
case beyond the routing above.

**These dispatches are queued, not immediate.** A ticket whose rung action maps to
a dispatch (`draft_skeleton`, `redraft_skeleton`, `answer_skeleton`, `forge`,
`draft_plan`, `redraft_plan`, `answer_plan`) enters the **qualifier set** built by
this step exactly like a Jira ticket that clears the `[COUNSEL vN]` forge gate
below — it is not dispatched on the spot. Step 3's `--max` cap, step 4's manifest
render, and step 4's outer gate (`--dry-run` / `--auto` / confirm-once) all apply
uniformly across both trackers; a rung-dispatched `forge` opens a real PR/MR just
as a Jira forge does, so it never bypasses the bound that "Bounded by default" and
"One outer gate" (Ethos, above) promise.

A ticket whose action is a no-op is dropped from the manifest silently — exactly
the loop-safety the watermark buys. Two exceptions: `await_start` is dropped from
the work manifest but surfaced as the dormant tally below rather than silently;
`done` is not dropped at all — it enters the **close-watch set** for step 5b,
where a merged PR/MR closes the ticket. (`at_rest` — a `[METTA]` already posted —
is the true terminal no-op: the ticket is forged *and* closed, nothing left to do.)
(The `[COUNSEL vN]` forge gate below still governs the Jira path.)

Apply the **forge gate** (identical to `/celebrimbor` step 2):

A ticket qualifies iff *all* of:

1. The thread contains at least one `[COUNSEL vN]` (or alias `[PLAN vN]`) from the bot.
2. A verdict token `[FORTH]` (or alias `[APPROVE]`) appears in non-bot comments somewhere in the thread.
3. The thread does **not** contain `[GWAITH]` / `[FORGED]` / `[SHIPPED]` from the bot anywhere — already forged, leave it alone.
4. **Jira skeleton road.** When the thread carries a `[SKELETON]` (the opt-in rung,
   carved by `/celebrimbor jira <project> --ticket <id> --skeleton`), rules 1–2 no
   longer qualify it; route by `council-jira-fetch.sh <ticket> | jira-skeleton-rung.py`
   instead, queued exactly like the YouTrack rung dispatch above:

   | action | Dispatch |
   |---|---|
   | `forge` | `/celebrimbor jira <project> --ticket <id>` |
   | `redraft_skeleton`, `answer_skeleton` | `/celebrimbor jira <project> --ticket <id> --skeleton` |
   | `await_skeleton` | skip (no-op) |

   Aulë never *starts* the skeleton rung on Jira — a ticket with no `[SKELETON]`
   forges on rules 1–3 as it always has.

Drop tickets failing rule 1 or 2 silently from the qualifier set. A ticket failing **only** rule 3 (already forged) is the Jira path's close-watch analogue to YouTrack's `done` action: if the thread bears no bot `[METTA]` yet, add it to the **close-watch set** for step 5b instead of dropping it outright — a forged-but-unmerged Jira ticket needs the same merge check YouTrack's decider already routes there. If the thread does bear a bot `[METTA]`, it is the true terminal no-op (forged and closed) and is dropped for real, mirroring YouTrack's `at_rest`.

Do not report per-ticket gate failures here — the manifest is for what *will* be forged, not what was excluded; a verbose gate report would dwarf the actual work.

### 3. Pick the first N

From the qualifier set, in the list hook's order, take the first `--max` (default 3). The remainder waits for the next invocation; the no-`[GWAITH]` gate keeps the cursor honest without state.

If the qualifier set is empty: stop with *"The road lies empty — no tickets bear approval awaiting the forge."*

If the qualifier set is smaller than `--max`: take the whole set. The report names what was found versus what was capped.

### 4. Render the manifest and the gate

Print one block:

```
Aulë at <tracker>:<project> — picked <K> of <Q> qualifier(s), max <N>

| # | Ticket | Counsel | Title |
|---|---|---|---|
| 1 | MET-3  | [COUNSEL v2] (approved 2026-05-14) | Add session-summary hook    |
| 2 | MET-7  | [COUNSEL v1] (approved 2026-05-15) | Refactor cleanup-dev report |
| 3 | MET-12 | [COUNSEL v1] (approved 2026-05-16) | Wire amon-din to TeamCity   |

<Q-K> qualifier(s) wait for the next sweep.
```

`Counsel` cell names the latest `[COUNSEL vN]` and the date of its approval verdict (the `[FORTH]` comment's `created_at`).

Then:

- **`--dry-run`**: skip step 5 (no forging) but still run step 5b in its own dry-run mode — rendering the close-watch preview (what would close, and why) without transitioning or posting. Stop after that; the manifest plus the close-watch preview are the deliverable.
- **`--auto`**: proceed straight to step 5. The manifest is still rendered first — the record of what was forged, even when no one stood at the gate.
- **Otherwise**: AskUserQuestion (options: `forge all <K>` / `abort`). On `abort`, stop. On `forge all`, proceed to step 5.

### 5. Per-ticket Celebrimbor dispatch

For each ticket in the manifest, in order, invoke the Celebrimbor skill via the Skill tool:

```
/celebrimbor <tracker> <project> --ticket <ticket-id> [--ready] [--confirm]
```

Use `skill: celebrimbor`, `args: "<tracker> <project> --ticket <ticket-id>"` (append `--ready` and/or `--confirm` if Aulë was passed them). Each invocation re-enters Celebrimbor's full workflow for that one ticket — pre-flight, counsel verification, workspace acquire, smith dispatch, push, PR/MR open, `[GWAITH]` post, state transition, workspace cleanup.

The `--ticket` flag bypasses Celebrimbor's own qualifier-pick prompt (see Celebrimbor's step 2 — when `--ticket` is set, the candidate set is just that one ticket). Aulë's outer gate replaces the inner prompt.

Capture each Celebrimbor run's outcome for the report. A Celebrimbor-side abort (counsel bears unresolved Open questions, smith returned `[ABORT]`, push or PR-open failed) does not stop the sweep — Aulë records the row and proceeds to the next ticket.

### 5b. Close the merged

Step 5 forges the unforged. This step closes the *already* forged: a ticket in
the **close-watch set** — on YouTrack, one the decider returned `done` for; on
Jira, one the forge gate routed here per rule 3 above — bears a `[GWAITH]` whose
PR/MR may since have merged. When it has, the ticket is laid to rest — its State
moved to the project's closed value and a `[METTA]` (Quenya *"the end"*) note
threaded — so the tracker reflects the deed without a human hand.

The idempotency guard is the same shape on both trackers: a ticket enters the
close-watch set only when it bears no bot `[METTA]` yet — on YouTrack that's the
decider's `done` vs `at_rest` split (step 2); on Jira the same check runs inline
in the forge gate (rule 3, step 2) — so this step never double-closes.

For each `done` ticket from the close-watch set (step 2), in list order:

1. **Extract the forge URL.** From the latest bot `[GWAITH]` comment (or its
   aliases `[FORGED]`, `[SHIPPED]`, case-insensitive) in the fetched thread,
   take the first URL on its first line.
2. **Ask the forge if it merged.** Look up the forge in `forge_routing.md`
   (`<tracker>:<project>`), then invoke the matching hook:

   ```bash
   ~/.claude/hooks/aule-github-merged.sh <pr-url>     # github
   ~/.claude/hooks/aule-gitlab-merged.sh <mr-url>     # gitlab
   ```

   - `merged: commit=<sha> url=<url>` → it merged; proceed.
   - `unmerged: state=<…>` → still open; leave the ticket untouched and record
     nothing — it re-checks next sweep.
   - `{"error":…}` → record the ticket `error` with the message; continue.
3. **Resolve the close state.** Read `merged=` for `<tracker>:<project>` from
   `state_mapping.md`. If the row is absent or the `merged` key is missing,
   **lazy-bootstrap once per sweep** via AskUserQuestion — the same shape as
   Glorfindel's `forth` bootstrap: offer the project's State names (or an "Other"
   free-text affordance), plus a `(skip — never close on merge for this project)`
   option that seeds `merged=` empty so the prompt does not return. Save the answer.
   If the value is empty, do not transition or post — record `closed` with detail
   `merged; close-state skipped`.
4. **Transition the ticket.** Before calling the state hook, check the ticket's current state via the fetch hook and inspect the tracker's own resolution flag:
   - **YouTrack**: parse `resolved` (boolean) from the ticket JSON. If `true`, skip the transition and record `closed` with detail `"merge detected; state transition skipped — ticket already in resolved state <state-name>; not overriding a hand-resolved ticket."` Proceed to step 5 to post `[METTA]` (the merge is still worth recording even if the state did not move).
   - **Jira**: fetch `fields.status.statusCategory.key` from the issue. If `"done"`, skip with the same note and proceed to step 5.

   If the ticket is not yet resolved, transition it via the tracker's own state
   hook — YouTrack values are state names, Jira values are transition IDs (same
   split as Celebrimbor's `forged=` handling):

   ```bash
   ~/.claude/hooks/youtrack-state.sh <ticket-id> <merged-state>   # youtrack
   ~/.claude/hooks/jira-state.sh <ticket-id> <merged-state>       # jira
   ```

5. **Post the closing note** via the council comment hook, naming the merge:

   ```
   [METTA] — closed on merge
   PR merged: <url> (commit <sha>)
   State: <from> -> <merged-state>
   ```

   Record outcome `closed`, carrying the PR/MR URL and the state transition.

Under `--dry-run`, render what *would* close (ticket, URL, merge state) and post
nothing — symmetric with the forge manifest. Under `--confirm`, prompt once per
ticket before the transition-and-`[METTA]` post.

### 6. Aggregate the report

Print one block:

```
Aulë at <tracker>:<project> — sweep complete

| # | Ticket | Outcome | PR/MR | Detail |
|---|---|---|---|---|
| 1 | [MET-3](<ticket-url>)  | forged    | <pr-url> | branch <name>; workspace released |
| 2 | [MET-7](<ticket-url>)  | aborted   | —        | counsel had unresolved Open questions |
| 3 | [MET-12](<ticket-url>) | error     | —        | gh push failed: branch already exists on origin |
| 4 | [MET-1](<ticket-url>)  | closed    | <pr-url> | PR merged; state In Progress -> Done; [METTA] posted |

Total: 4 ticket(s) — 1 forged, 1 closed, 1 aborted, 1 error.
<Q-K> qualifier(s) remain for the next sweep.
<D> ticket(s) await [MELLON] — dormant until summoned.
```

The dormant tally `<D>` counts tickets the decider returned `await_start` for — planless and un-summoned. They are dropped from the work manifest, surfaced only as this count so a backlog of un-summoned tickets does not read as an empty project.

Outcome vocabulary:

| Outcome | Meaning |
|---|---|
| `forged` | Smith committed, push succeeded, PR/MR opened, `[GWAITH]` posted. (State transition outcome appears in `Detail` if non-trivial.) |
| `closed` | A `done` ticket's PR/MR had merged (step 5b) — the ticket was moved to its `merged=` state and a `[METTA]` note threaded. Detail carries the merge and the state transition. (When `merged=` is empty, the ticket is recorded `closed` with `close-state skipped` and no write lands.) |
| `aborted` | Celebrimbor stopped before opening — counsel had unresolved Open questions, smith returned `[ABORT]`, or `--confirm` was declined. No PR. |
| `dry-run` | Reached only when Aulë's `--dry-run` was set — not present in this report; the dry-run path renders the manifest and step 5b's close-watch preview, then stops before step 5. |
| `answered` | A rung-dispatch ticket bore a question (`[CEIST]`/`[ASK]`, or bare prose); the sub-skill posted a `[PEDO]` answer and left the plan/skeleton standing. No PR. |
| `error` | A hook failed (push, PR-open, `[GWAITH]` post). Detail names which step. The PR may exist if the failure was downstream of PR-open; check the URL field. |

Do not reproduce smith diffs in this report — they live on the PRs/MRs now, and Celebrimbor's per-ticket report block is the authoritative narrative for each forge.

The closing line — *"<Q-K> qualifier(s) remain for the next sweep"* — names the bookmark Aulë leaves for the next invocation. Re-run `/aule <tracker> <project>` (with the same args) to forge the next batch.

## Rules

- `--max N` is a hard cap. The default is 3. The cap stands even if a later run finds the same tickets still qualifying for any reason — Aulë never overruns its bound in one invocation.
- The qualifier set is the order returned by the list hook; Aulë does not re-sort. Re-run order follows the same hook's order.
- The forge gate is the cursor. Do not maintain a separate "already-forged" memory — the tracker's `[GWAITH]` post is the only record needed, and the only one that survives a memory wipe.
- `--dry-run` overrides the outer gate; nothing to confirm if nothing is dispatched.
- `--auto` skips the outer gate and the Jira post-safety prompt; everything else stands unchanged — the `--max` cap, the forge gate, and Celebrimbor's own per-ticket workflow. `--auto` is never combined with `--dry-run` or `--confirm`.
- `--confirm` propagates to every `/celebrimbor` dispatch (per-ticket prompt before PR-open). Use to stop mid-sweep without aborting prior forges.
- A Celebrimbor-side abort or error on one ticket does not halt the sweep. Record the outcome and proceed.
- Aulë never invokes the forge hooks (`forge-github-pr.sh`, `forge-gitlab-mr.sh`) directly. All PR-open writes flow through `/celebrimbor`. One source of truth for the per-ticket forge.
- Aulë never invokes the council comment hook for **forge** posts — every `[GWAITH]` flows through `/celebrimbor`. The one comment Aulë posts of its own is the close-on-merge `[METTA]` note (step 5b), which has no forge stage to route through: the deed it records is the *merge*, watched by Aulë, not a PR-open.
- Close-on-merge (step 5b) is bounded by the tracker, not by `--max`. `--max` caps forges, which write to four places each; closing a merged ticket writes one transition and one comment, and the merge itself is the gate — every `done` ticket whose PR/MR has merged is closed in the pass it is seen.
- Do not surface tracker or forge tokens in logs, responses, or saved files.
- **Jira sweeps require deliberate intent** — when tracker is `jira` without `--auto`, `--dry-run`, or `--confirm`, prompt before proceeding (step 1e).
