---
name: tidy
description: Use when the user asks to clean up, tidy, prune or archive leftovers (branches, worktrees, agents, plans, handoffs, stale board lines), at board wrap or rollover, or for the weekly deep clean.
---

# Tidy

Cleanup on a schedule instead of when someone notices. Three modes, one script (`~/bin/tidy`), one log. The rule behind all of it: remove only what is provably dead, ask once per category about anything that loses content, and keep an undo command for every action.

## Config

Read `~/.claude/config/tidy.md` (its `### Tidy` section; older installs keep it in `~/.claude/CLAUDE.md`; `~/bin/tidy` reads both): `Weekly` (day whose wrap runs the weekly clean), `Extra repos`, `Report folders`, `Branch age`, `Plan age`, `Handoff age`, `Memory age`, `Loose ends`, `Loose ends max`, `Loose ends age`, `Never touch`. The handoff folder comes from `## Handoffs`; the worktree config, memory dir, Projects data source and `carry_flag_days` from `~/.claude/config/board.md` (`### Work board`); the Slack poll files from `~/.claude/config/watch.md` (`### Watches`); older installs keep both sections in `~/.claude/CLAUDE.md`. Archive, log and state live in `~/.claude/tidy/`.

Without tidy config (`~/.claude/config/tidy.md` or a `### Tidy` section in CLAUDE.md), tidy is list-only: run `scan`, print the findings, change nothing (`apply` refuses).

## Modes

| Mode | When | Does |
|---|---|---|
| `daily` | Every board wrap | Tier 1 only: merged worktrees and branches, finished processes and agents, empty plan and handoff files, old poll events. One line out unless something needs the user |
| `stale` | Every rollover, after today's row exists | Flags old board lines and old local items (plans, handoffs, memories) into the board's Open questions queue. One line out |
| `weekly` | Wrap when the scan says `weekly_today` or `weekly_due` (it reads the real date, never assume the weekday), or rollover's answer was "at wrap"; `/tidy weekly` or `/board tidy` any time | Everything: Tier 1 without asking, one question per Tier 2 category, the report-only list, Loose ends review |

Every mode takes `--dry-run`: run `scan --no-fetch` and `apply --dry-run`, print the report, change nothing and write no state. `stale` mode never fetches.

Steps for any mode:

1. `~/bin/tidy scan --mode <mode> --json`. It is read-only except `git fetch --prune` per repo (`--no-fetch` skips that). A non-empty `errors` list (for example an unreadable worktree config; the command exits 2) stops the run: report it and fix the config before cleaning anything.
2. For `stale` and `weekly`, dispatch the board's `tidy-board-check` (sonnet, read-only; see the board skill's Dispatching agents) for board lines and Projects rows.
3. Agents first: `ListAgents`, then `TaskStop` every idle agent whose work is done (read anything still needed from it first). Background shells the session started: stop those whose log says done. A worktree that any live process still works in is never removed (scan and apply both check).
4. Pipe the Tier 1 findings, as a JSON list, to `~/bin/tidy apply --mode <mode>`. No question. Never pipe the scan output itself: `apply` refuses anything but a list.
5. Tier 2: one grouped question per category (below). On a yes, add `"approved": true` to exactly the approved findings and pipe them as a JSON list to `apply`. `apply` refuses any Tier 2 item without that marker.
6. Print the report (shape below) and append it to the day's handoff.

## Merged, defined once

After `git fetch --prune`, a branch is merged when (a) its tip is an ancestor of `origin/<default>` and not on its first-parent line (the branch had commits of its own that a merge brought in), or (b) its PR merged into the default branch and the PR's head sha equals the branch tip (squash merges). A branch cut from the default tip with no commits of its own is never "merged": its worktree may be waiting on a plan. Only a proven-merged branch is deleted without asking, with `git branch -D` and its sha logged. Before deleting any branch whose commits are not in the default branch (squash-merged or unmerged), `apply` keeps them at `refs/tidy-archive/<sha>`. Never use `git branch -d` as the check: it compares to the local upstream or HEAD and refuses squash merges.

## Safety tiers

**Tier 1, do without asking (the scan marks these `tier: 1`):**
- Worktree on a merged branch, with no running process working inside it, whose status shows nothing but setup copies that are byte-identical to the main checkout, and no other git-ignored files. Removed, branch deleted, main fast-forwarded. A worktree that also holds ignored files (an `.env.local`, a data export, a cache) is Tier 2 with the file list, weekly only; on a yes those files are moved to the archive before the worktree is removed.
- Worktree on a merged branch whose folder was deleted by hand (`prune_worktree`): `git worktree remove <path>` drops that one entry (never a repo-wide `git worktree prune`), then the branch is deleted.
- Merged local branch, not checked out anywhere, not the default branch, no open PR.
- `wait-for pr` processes whose PR is merged or closed; idle finished agents; finished background shells.
- Empty files and folders in the plans and handoff folders.
- Slack poll event files older than 7 days (archived). The triage log trim to its last 500 lines runs only after wrap stops the poll; `apply` skips it while the poll runs.

**Tier 2, ask once per category.** File and branch questions offer "archive or remove all (Recommended)", "keep all", "show me the list". Board lines and Loose ends never get a blanket yes: list each line with a proposed home, date or drop, and the user confirms or changes each one. Questions go through the board's Open questions queue (grouped `AskUserQuestion`, up to 4 per call), never one per item.
- `branch_gone`: unmerged branches whose upstream is gone or whose PR closed, older than `Branch age`.
- `worktree_gone`: a worktree on such a branch, with its `edits` and `ignored` file lists. On a yes, both lists are moved to the archive (staged changes too, as a patch beside it), then the worktree is removed and the branch deleted (commits kept under `refs/tidy-archive/`). If any listed file cannot be moved, the worktree is not removed.
- `branch_no_pr`: old branches with no PR and no upstream, in batches of 30 (the `batch` field), oldest first. One batch per week.
- Plans older than `Plan age`: drop any the Work registry still points at, then offer the rest.
- Handoffs older than `Handoff age`: archived to `<handoff folder>/archive/YYYY-MM/`. The newest handoff and today's `-files` folder are never offered.
- Finished-work memories not edited in `Memory age`: only `project` memories whose description or first body line starts with a finished word (DONE, ENDED, closed, shipped). Feedback, user and reference memories are never offered. Moved to `<memory dir>/archive/`, index line removed. Memory text is never edited.
- Unlinked entries in `~/.claude/commands` and `~/.claude/skills` that shadow a repo item. The rest are report-only; name any that mention a retired feature in the report. `.bak` files are `update.sh`'s job.
- Board lines (from `tidy-board-check`): Deferred lines and dateless Blocked watch rows older than `carry_flag_days` x 3, In-flight rows that are not in flight, Projects rows with a past Next milestone and no update in 14 days, Loose ends items older than `Loose ends age`. Each gets a home, a date, or is dropped. Edits to today's row are single-line `update_content` edits after the yes.
- Permission rules: the scan's `permission_rules` finding, grouped by tool, shown as a list once a week. The user names which to drop; edit the settings file only for those.

**Report only (listed, never changed):** dirty default checkouts and repos with uncommitted work, worktrees with real edits (merged or not), clean worktrees on a closed-PR or upstream-gone branch (until the weekly offers them), detached worktrees, worktrees whose `git status` fails (never removed), worktrees whose folder is gone on an unmerged branch or detached (the finding's `command` removes just that entry, keeping detached commits under `refs/tidy-archive/` first), stashes (count), published artifacts older than 30 days that a newer one replaces (the user deletes them, or says yes per artifact and it is logged `restore: none`), `~/.claude/tasks`, `teams`, `jobs` (count and size), transcripts (size), `Report folders`. Drafts belong to wrap's drafts check and tracker snapshots to the tracker gatherer: do not recheck them.

**Tier 3, never touch:** real edits anywhere, any stash, an open PR's branch, a checked-out branch, the default branch, closed daily rows, the scratchpad, Goals, the Standup section, settings file content (except the rules the user names), credentials, env files, `CLAUDE.md`, other people's PRs, tickets and threads, anything in `Never touch`, and any path outside the folders tidy knows. `apply` refuses these even when asked.

## Loose ends

The one home for things worth keeping that have no project, ticket or memory: a link to read later, a small idea, a file kept just in case, a question with no owner yet.

- With a Projects data source: one Projects row named by the `Loose ends` line, Status Parked, no Priority. Its page is a checklist: `- [ ] <item> (added YYYY-MM-DD) <link>`. Standup, the project status page and the stale check skip it.
- Without one: a `## Loose ends` section on the daily row, carried by rollover like Deferred.
- The daily row shows one Pacing line, `Loose ends: N items, oldest D days`, with a link. Never copy the list.
- Every item has an added date. At `Loose ends max` one item leaves before a new one comes in.
- Weekly: every item older than `Loose ends age` gets a home (project, ticket, memory), a date (moves to Blocked or Deferred with a re-check date), or is dropped and logged. Nothing stays by default.

## Log, archive and state

- `apply` takes a JSON list only, and acts on a Tier 2 item only when it carries `"approved": true`. It re-checks every item live (branch tip, PR state and base, worktree edits and ignored files, file mtime, process command, poll running) and skips anything that changed since the scan. It computes archive paths itself. One bad item is logged as failed (in the output and in `log.jsonl`) and the rest still run. Never hand it a list you edited by hand to "fix" a skip; re-scan.
- Every action writes two lines to `~/.claude/tidy/log.jsonl`: an `intent` line with the undo command before acting, then a `result` line (`ok` or `failed`). Fields: `ts`, `mode`, `tier`, `kind`, `target`, `phase`, `action`, `restore`. `restore` is the exact undo command (branch: `git -C <repo> branch <name> <sha>`; worktree: that plus `git worktree add <same path>` and a copy back of any archived edits and ignored files plus `git apply --cached` of the staged patch, without setup copies; file: `mv <archive> <original>`).
- Files are moved to `~/.claude/tidy/archive/YYYY-MM-DD/<path under home>` (worktree files to `archive/YYYY-MM-DD/worktrees/<repo>/<worktree>/`), never deleted, except empty files and folders with nothing inside.
- `state.json` holds `last_daily`, `last_stale`, `last_weekly`, written only by a real `apply` (pipe `[]` when there is nothing to apply). The scan's `weekly_due` is true when `last_weekly` is missing or older than 7 days, and `weekly_today` is false once `last_weekly` is today. When `weekly_due`, rollover asks "Run the weekly tidy now or at today's wrap?".

## Report

Weekly, in chat and appended to the handoff. Counts first, one line per heading:

```
Tidy weekly 2026-11-20: removed 41, archived 9, needs you 5 questions, left 3
Removed (no ask): 38 merged branches (app 30, infra 5, web 3), 2 empty plan folders, 1 finished task
Archived: 7 handoffs (to archive/2026-10), 2 plans
Questions: gone branches (21), finished-work memories (3), old board lines (7), Loose ends (2), permission rules (list)
Left alone: 3 dirty mains (app, web, api), listed since 2026-10-30
Skipped (changed since scan): 0
Log: ~/.claude/tidy/log.jsonl (each line has a restore command)
```

Daily and stale print one line (`tidy daily: removed 4 merged branches, 1 worktree; left 2 dirty`) unless something needs the user.

## Common mistakes

| Mistake | Fix |
|---|---|
| Deleting a branch with `git branch -d` and trusting it | Use the merged rule; `-d` checks the wrong base and refuses squash merges |
| Treating a worktree as clean because its only changes are setup copies | Copies count as clean only when byte-identical to the main checkout; `scan` checks this, including git-ignored copies |
| Trimming the poll's triage log while the poll runs | Trim after wrap stops the poll; `apply` skips it otherwise |
| One giant question, or one question per item | One question per category, through the board's queue |
| Acting on an old scan | `apply` re-checks live; a skip means re-scan, never force |
| Deleting handoffs, plans or memories | Archive them; only empty files are removed |
| Asking about Tier 1 items | They are provably dead. Do them and report the count |
| Offering all 100 old branches at once | One batch of 30 per week, oldest first |
| One "drop all" answer for old board lines | Each line gets its own home, date or drop |
| Deciding it is the weekly day from memory | Use the scan's `weekly_today` and `weekly_due`, which read the real date |
| Deleting an artifact because it looks old | Artifact deletion cannot be undone: report only, or a per-artifact yes logged `restore: none` |
