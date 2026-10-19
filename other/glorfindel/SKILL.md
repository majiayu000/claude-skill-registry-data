---
name: glorfindel
description: Use when the user runs /glorfindel <tracker> <project> [--filter <id-or-jql>] [--dry-run] [--confirm] [--auto]. Sweeps every open ticket in the named project, runs the council machinery on each, and aggregates one report. Loop-safe per ticket; opt-in to confirmation prompts before posting.
purpose: Sweeps every open ticket in a project through the council machinery and aggregates one report.
user_invocable: true
stage: plan
composes: council:dispatch
---

# Glorfindel — The Sweep

Glorfindel rode out from Rivendell to seek the Ringbearer, and visited each road in turn until he found him. So this skill: it visits every open ticket in a project, summons the council on those that have stirred, and brings back one report of all.

## Ethos

- **Glorfindel rides; the council still decides.** Per-ticket behavior matches `/council` exactly. Glorfindel never posts more than `/council` would.
- **Loop-safe by inheritance.** A sweep over a project where nothing has moved is a quiet ride — no posts, just a report saying so.
- **The tracker is the home of the work.** Glorfindel reports across many tickets, but the per-ticket record stays on the tracker.

## Argument parsing

`/glorfindel <tracker> <project> [--filter <filter>] [--dry-run] [--confirm] [--auto]`

| Argument | Required | Meaning |
|---|---|---|
| `<tracker>` | yes | `youtrack` (alias `yt`) or `jira` |
| `<project>` | yes | Project shortName / key (e.g. `MET`, `PSG`) |
| `--filter <filter>` | no | Tracker-aware extra scope (see below) |
| `--dry-run` | no | List what would happen; never post |
| `--confirm` | no | Ask before each post (default off) |
| `--auto` | no | Proceed unattended on Jira — skip the post-safety prompt (step 1b). The flag is the deliberate "I accept unattended Jira posting", symmetric with `/aule --auto`. No-op on YouTrack (no such gate). |

**Filter is required.** Glorfindel will not sweep without one — sweeping a whole project is too broad to be useful and too costly to be safe. The skill enforces this; the list hooks enforce it too.

**Filter semantics, by tracker:**

- **YouTrack:**
  - Saved-query ID (digits-hyphen-digits, e.g. `--filter 11-0`) — looks the saved query up at `/api/savedQueries/<id>`, uses its `query` text. Symmetric with Jira's saved-filter shortcut.
  - Raw query fragment (e.g. `--filter "state:Open assignee:me"`, or `--filter "#Unresolved"`) — ANDed with the project clause.
- **Jira:**
  - Saved filter ID (all-digit, e.g. `--filter 10363`) — JQL becomes `filter = 10363`.
  - Raw JQL fragment (e.g. `--filter "assignee = currentUser()"`) — ANDed with the project.

**Filter resolution order** (when `--filter` is *not* given on the command line):

1. **Per-project memory** — read `default_filters.md` from the project memory directory. Look up `<tracker>:<project>` (e.g. `jira:PSG`). If found, pass that value to the list hook as if the user had typed `--filter <value>`.
2. **Stop with an error.** No hardcoded fallback. Tell the user: *"No filter specified and no entry for `<tracker>:<project>` in `default_filters.md`. Pass `--filter <value>` or seed the memory file."*

An explicit `--filter <value>` always wins.

## Tracker routing

| Tracker | List hook | Council fetch | Council comment | State transition |
|---|---|---|---|---|
| `youtrack` / `yt` | `~/.claude/hooks/glorfindel-youtrack-list.sh` | `~/.claude/hooks/council-youtrack-fetch.sh` | `~/.claude/hooks/council-youtrack-comment.sh` | `~/.claude/hooks/youtrack-state.sh` |
| `jira` | `~/.claude/hooks/glorfindel-jira-list.sh` | `~/.claude/hooks/council-jira-fetch.sh` | `~/.claude/hooks/council-jira-comment.sh` | `~/.claude/hooks/jira-state.sh` |

## State mapping

When the per-ticket action settles to `forth` (and only `forth` in v1), Glorfindel looks up the project's state mapping in `state_mapping.md` and asks the state hook to move the ticket. The mapping is per `<tracker>:<project>`. Format:

```
- youtrack:SKA → forth=To Do, forged=In Review
- jira:PSG     → forth=10006, forged=10007
```

YouTrack values are state names (the State field's value, e.g. `To Do`). Jira values are transition IDs (numeric, project-specific — see `GET /rest/api/3/issue/<key>/transitions`). The same file is read by `/celebrimbor` for its `forged` action.

**Lazy bootstrap.** The first time the action would fire for a `<tracker>:<project>` whose row is absent or missing the `forth` key, ask via AskUserQuestion *once* per sweep:

- For YouTrack: offer the project's common State names if known, otherwise an "Other" affordance for free text. Add a `(skip — never transition on FORTH for this project)` option which seeds `forth=` (empty) so the prompt does not return.
- For Jira: prompt for a transition ID with the same skip option, and remind the user to fetch it via `GET /rest/api/3/issue/<key>/transitions` if unknown.

Save the answer to `state_mapping.md`, then proceed. Future sweeps consult the file silently.

## Workflow

### 1. Pre-flight checks

**a. Resolve the repo path and acquire a workspace.** Same rule as `/council` — see the council skill's "Working-directory contract" section, including its single-repo / multi-repo split. The acquire strategy follows which kind the project is:

- **Single-repo project (bare key).** Resolution happens **once for the whole sweep**. Look up `<tracker>:<project>` in `repo_routing.md`; if absent, ask once, save, proceed. If the resolved value is a real path (not `(no repo)`), acquire **one** isolated workspace for the entire ride via the shared helper:

  ```bash
  ~/.claude/hooks/skadi-worktree.sh acquire <source-repo>
  ```

  Every ticket in the sweep hands the same workspace path to its Erestor subagent — one acquire per sweep, not per ticket, since worktree setup carries a non-trivial cost and Glorfindel may visit dozens of tickets. If the resolved value is `(no repo)`, skip the acquire — Erestor drafts from ticket text alone on every ticket.

- **Multi-repo project (sub-keyed).** The repo depends on each ticket's summary tag, so resolution is **per ticket**, deferred into the sweep loop. For each ticket, derive its layer tag and resolve `<tracker>:<project>:<tag>` per the council contract. Acquire that repo's workspace lazily, **caching by source-repo path** so each distinct tree is acquired at most once per sweep — a sweep touching ten `[APP]` and three `[WEB]` tickets acquires two workspaces, not thirteen. A ticket whose summary bears no matching sub-key resolves to `(no repo)` — its Erestor drafts from ticket text alone.

All workspaces acquired — the one sweep-wide tree, or the several cached multi-repo trees — are released in step 4 (after the aggregate report) on the success path.

**b. Jira post-safety warning.** If `<tracker>` is `jira` and none of `--auto`, `--dry-run`, or `--confirm` is set: warn the user via AskUserQuestion that Glorfindel is about to sweep Jira and may post automatically to many real tickets. Offer three options:
- Proceed unattended (risky on Jira).
- Re-run with `--confirm` (recommended).
- Re-run with `--dry-run` (safest).

If the user picks "proceed unattended" explicitly, continue. Otherwise stop and tell them how to re-invoke. **`--auto` skips this prompt** — the flag *is* the deliberate intent the warning exists to confirm, given in advance (e.g. when Glorfindel rides under an unattended `/anduin` / `/amon-sul` watch). YouTrack never reaches this gate.

### 2. List the open tickets

Resolve the filter argument per the **Filter resolution order** above (explicit `--filter` > `default_filters.md` > hook default). Then invoke the chosen list hook:

```bash
<list-hook> <PROJECT> [<FILTER>]
```

The hook output takes one of three shapes:

- **Flat array** `[{id, summary}, ...]` — the normal case. Iterate it.
- **Wrapped truncation object** `{"tickets": [...], "truncated": true, "cap": 1000}` — emitted when the hook hit its safety cap (1000 tickets in 20 pages of 50). Tell the user the cap fired (*"The road runs longer than the eye can see — N tickets returned, more remain"*) and ask whether to proceed with the truncated list or to narrow the filter and re-run. On "proceed", iterate `.tickets`.
- **Error object** `{"error": "...", "response": "..."}` — surface and stop.

If the iterable list is empty, tell the user *"The road lies empty — no tickets matching the scope."* and stop.

### 3. For each ticket — run the council

Iterate the list (newest-first as the hook returns it). For each ticket, follow the **council workflow** (see `skills/council/SKILL.md` steps 1 through 6) with three glorfindel-specific shifts:

- **Engagement gate.** A ticket is enrolled in the sweep iff *one* of these holds:
  - The thread already contains any `[COUNSEL v…]` / `[PLAN v…]` (alias) or `[PARLEY]` / `[AGENT-ASK]` (alias) — already in the council, OR
  - Any non-bot comment carries `[MELLON]` or its alias `[FRIEND]` (Elrond's summons; case-insensitive, anywhere in the body).

  Tickets with neither gate satisfied are *untouched* — the sweep does not draft on them, even though they are open. Record action `untouched` with detail "no `[MELLON]` summons yet" and move on. This keeps `/glorfindel` from flooding a fresh project with `[COUNSEL v1]`s on its first run; Elrond enrolls each ticket explicitly. The gate applies only to `/glorfindel` — direct `/council MET-2` is itself the summons and runs without `[MELLON]`.

  **This skill-level gate governs the Jira path only.** On YouTrack, `skeleton-rung.py`'s decider owns enrollment in its own right — a planless, un-summoned ticket yields `await_start`, which this step records as `untouched` the same way, but the check itself lives in the decider, not here (see Rules, below).

- **Loop-safe is mandatory.** Once a ticket is past the engagement gate, skip silently any whose state classifies as "no fresh counsel". Do not draft, do not post — they are at rest. Record action `quiet` and move on.
- **Posting gate** — applies any time the per-ticket flow would invoke the comment hook:
  - If `--dry-run` is on: do *not* invoke the comment hook. Record what *would* have been posted (token, body length).
  - If `--confirm` is on: ask the user via AskUserQuestion (one ticket per question, with the proposed token and a 2-line excerpt). On rejection: skip the post; record `skipped`. On approval: post.
  - Otherwise: post.

Erestor's draft is per-ticket — each ticket gets its own subagent dispatch with its own thread context. Every dispatch reuses the workspace resolved for this ticket per step 1a — the single sweep-wide tree for a single-repo project, or the ticket's cached layer-tagged tree for a multi-repo one; the workspace is detached, read-only from Erestor's vantage, and shared across every ticket that resolves to the same tree.

If a hook fails mid-sweep (auth, network, server error), record the ticket as `error` with the message and continue with the rest. Do not let one ticket's failure halt the sweep.

- **State transition on `forth`** — when the per-ticket action settles to `forth`, look up the project's `forth` value in `state_mapping.md`. Bootstrap if missing (see "State mapping"). If the value is empty or `--dry-run` is on, do not transition; otherwise invoke the state hook:

  ```bash
  <state-hook> <ticket-id> <forth-value>
  ```

  Append the hook's outcome to the ticket's `Detail` cell:
  - `transitioned: ...` → suffix becomes `; state <from>->\<to\>`.
  - `noop: ...` → suffix becomes `; state already <state>`.
  - JSON error → suffix becomes `; state error: <message>` (the action stays `forth`; the comment / verdict was untouched).

### 4. Aggregate the report

Print one markdown table summarizing the ride. Example shape:

```
**Glorfindel — sweep of youtrack:MET**

| Ticket | Action     | Detail                              |
|--------|------------|-------------------------------------|
| MET-3  | drafted    | [COUNSEL v1] posted (id 7-22)       |
| MET-2  | dry-run    | [COUNSEL v2] would post (412 chars) |
| MET-1  | quiet      | awaiting reply on [COUNSEL v4]      |

Total: 3 tickets — 1 drafted, 1 dry-run, 1 quiet, 0 untouched, 0 answered, 0 forth, 0 forged, 0 nay, 0 farewell, 0 talked-out, 0 skipped, 0 errors.
```

Action vocabulary:

| Action | Meaning |
|---|---|
| `untouched` | No `[COUNSEL vN]`/`[PLAN vN]` exists yet, no `[PARLEY]`/`[AGENT-ASK]` stands, AND no `[MELLON]`/`[FRIEND]` summons in the thread. Skipped to avoid mass-drafting on first sweeps. |
| `quiet` | Loop-safe no-op — bot's last word stands; no fresh Elrond counsel. |
| `drafted` | Erestor wrote a `[COUNSEL vN]` or `[PARLEY]` and the post landed. |
| `answered` | Elrond asked a question (`[CEIST]`/`[ASK]`, or bare prose); Erestor posted a `[PEDO]` answer and the plan stands unchanged. |
| `dry-run` | Erestor's draft prepared; not posted per `--dry-run`. |
| `forth` | `[FORTH]` (or alias `[APPROVE]`) found — plan stands. Council adjourned with approval. |
| `forged` | `[GWAITH]` (or alias `[FORGED]` / `[SHIPPED]`) found — Celebrimbor has opened the PR/MR; the deed is wrought. Detail carries the PR/MR URL. Takes precedence over `forth` and `quiet` when `[GWAITH]` is present in the thread. |
| `nay` | `[NAY]` (or alias `[REJECT]`) found — plan abandoned. Council adjourned without approval. |
| `farewell` | `[NAMARIE]` (or alias `[FAREWELL]`) found — council adjourned without verdict (resolved out-of-band, subsumed, etc.). |
| `talked-out` | Five-counsel turn limit hit; canned `[PARLEY]` posted (or would-post under dry-run). |
| `skipped` | User declined the `--confirm` prompt for this ticket. |
| `error` | A hook failed for this ticket. Include the error message in Detail. |

Do not reproduce Erestor's full drafts in the report — they live on the tickets (or stayed in dry-run memory). Print one URL per ticket only when the action carries an id (drafted / talked-out).

After the report, release every workspace acquired in step 1a — the single sweep-wide tree for a single-repo project, or each cached multi-repo tree:

```bash
~/.claude/hooks/skadi-worktree.sh release <workspace-path>
```

A mid-sweep crash that bypasses this step leaves the workspace under `$TMPDIR` for inspection; the next sweep acquires a fresh one, and the OS clears `$TMPDIR` on reboot.

## Rules

- **YouTrack path is modify-only.** On YouTrack, Glorfindel drives the converted
  `/council` (one living `[PLAN]` comment, no `[COUNSEL vN]` versions). Loop-safety
  comes from `~/.claude/hooks/skeleton-rung.py` returning `await_plan` (nothing new
  since the last edit) rather than the old append "no fresh counsel" check. The Jira
  path keeps the append behavior.
  On the YouTrack path the enrolment gate (step 3) is the decider's own work: a
  planless ticket with no `[MELLON]`/`[FRIEND]` summons yields `await_start`, which
  Glorfindel records as `untouched` — the same outcome the skill-level gate gave,
  now derived in one place. The Jira path keeps its skill-level engagement gate.

- Glorfindel never posts more than the council would. Per-ticket behavior matches `/council` exactly.
- `--dry-run` overrides `--confirm` — nothing to confirm if nothing is posted.
- Errors on one ticket do not stop the sweep. Record and continue.
- Sweep order is the order returned by the list hook.
- **Jira sweeps require deliberate intent.** When tracker is `jira` without `--dry-run`, `--confirm`, or `--auto`, prompt before proceeding (step 1b). `--auto` skips the prompt — the flag is the deliberate intent it exists to confirm.
- Do not surface tracker tokens in logs, responses, or saved files.
- Do not invent ticket IDs not returned by the list hook. The list is the authoritative scope.
