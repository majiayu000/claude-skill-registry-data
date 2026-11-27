---
name: board
description: Use when the user asks where things stand, what is waiting on them, what is blocked, to start, plan or implement a ticket from the master session, to roll the daily board to a new day, or at the start of a master-session day.
---

# Board

One place to see all active work. State lives in a Notion database with one row per day. Each day row holds the human-readable "Your view"; a child page "Claude scratchpad" holds machine notes and the work registry. External gathering (tracker, GitHub, Slack) and ticket work run in sub-agents; the main session coordinates, reads local files like `MEMORY.md` inline, and reports.

## Sub-commands

| Command | Does | Steps in |
|---|---|---|
| `/board` or `/board sync [--sessions]` | Rebuild today's row from every source and print Your view | SKILL.md |
| `/board rollover` | Close yesterday's row, create today's, carry open items forward | rollover.md |
| `/board start <TICKET or short name> [repo]` | Worktree, planner, approval, implementer, reviewer, `/pr` | start.md |
| `/board resume <key>` | Restart a stream from its registry row after a session restart | start.md |
| `/board status [<key>]` | Stage of one or all streams, from files first, agents second | start.md |
| `/board access` | Run the morning access check alone and list what still needs the user | SKILL.md |
| `/board wrap` | End of day: verify today's drafts went out, clean merged worktrees and branches, stop strays and the Slack poll, list temporary permission rules, write the handoff, ask for `/clear`; pickup checks after any `/clear` | wrap.md |
| `/board tidy` | Run the `tidy` skill's weekly mode now | SKILL.md |
| `/board done <text>` / `/board defer <text>` | Tick or move one line on Your view. `done oncall: <text>` appends `- [x] oncall: <text>` to Done today, which the next standup puts under Oncall | SKILL.md |

Read only the file for the mode being run.

## Config

Read `~/.claude/config/board.md` (its `### Work board` section); on older installs the same section is in `~/.claude/CLAUDE.md`. It holds every machine-specific value (the list and formats are in claude-setup's `config/board.example.md`); access checks live in `~/.claude/auth-checks.json` (the `daily-auth` skill). Nothing in this skill names a company, person, channel, ticket or path.

If the section or the Notion page line is missing, stop with: "Add ~/.claude/config/board.md (copy config/board.example.md from claude-setup) and set the board page."

The watch steps below (the Slack poll and `wait-for pr`) run only when `~/.claude/config/watch.md` exists (or, on older installs, a `### Watches` section in `~/.claude/CLAUDE.md`); without it, skip them. The Slack poll (`~/bin/wait-for slack`, see the `watch` skill) runs only when that section says `Slack poll: on`. Start it at rollover and again whenever the session resumes after `/clear`, if it is not already running.

Notion setup happens on every run, so any empty page works: fetch the page, find its inline database and that database's `collection://` data source, and add any schema column from `page-template.md` that is missing (`notion-update-data-source`, add only). Cache the data source url in the scratchpad for the day.

## Dispatching agents

The main session never reads `dispatch-prompts.md` or `page-template.md`. Each agent reads its own section. Dispatch with a short prompt in this shape:

    Read the section "## <name>" of ~/.claude/skills/board/dispatch-prompts.md in full: its fenced block, which ends at the closing fence (headings inside the block are part of it), is your task. Replace each {{placeholder}} with the value given below.
    Values:
    <key>: <value>
    ...

Pass `model` and `subagent_type` as the section heading says. Give every key in that section's "needs" list below; the agent stops with BLOCKED naming any needed key that is missing, rather than guessing. Values that are long (gatherer reports for the standup) are pasted under their key. Values that live on the scratchpad page (registry rows, outreach threads, drafts today) are not pasted: pass `scratchpad_url` and the agent reads the section it needs. `standup-builder` is the one exception to "uses no tools": it reads its own section, then uses no other tool.

Needs, per section:
- tracker-status: user_name, today, tracker_site, tracker_mcp_prefix, tracker_project, tracker_epics, since_date
- github-status: user_name, today, github_org, worktree_config, worktree_script, since_date, scratchpad_url, epic_child_keys, running_waits, declined
- slack-status: user_name, today, slack_user_id, slack_channels, since_date, oncall, scratchpad_url, declined
- email-status: user_name, today, email_address, email_mcp_prefix, since_date, scratchpad_url
- drafts-check: user_name, today, slack_user_id, email_address, scratchpad_url
- tidy-board-check: user_name, today, today_row, projects, carry_flag_days, loose_ends, loose_ends_age
- standup-builder: user_name, tracker_epics, prev_rollover_time, projects, prev_done_today, tracker_report, github_report, slack_report, email_report, confirmed_goal, carried_needs_you, blocked_rows
- board-writer: user_name, today, mode, row_url, scratchpad_url, board_page, poll_files, writer_inputs
- Planner, Implementer, Reviewer, PR agent: ticket, worktree_path, repo, plus ticket_url (Reviewer), approval_notes (Implementer), approved_files (PR agent)

Placeholder sources (board config means `~/.claude/config/board.md`, or on older installs the `### Work board` section of CLAUDE.md):

| Placeholder | Comes from |
|---|---|
| `user_name` | `git config user.name`, or a name line in `~/.claude/CLAUDE.md` if present |
| `tracker_site`, `tracker_mcp_prefix` | the `### Issue Tracker` section of `~/.claude/CLAUDE.md` |
| `ticket_url` | that section's ticket URL format |
| `master_session_name` | this session's name from `ListAgents` |
| `since_date` | the previous row's Date, else 7 days ago |
| `today` | local `date +%F` |
| `approved_files` | the user's ship-it turn |
| `epic_child_keys` | the child keys under `tracker_epics` listed under those epics in the previous scratchpad's "Epic rollups" section, never from the project fallback (empty on the first run or when `tracker_epics` is empty; the GitHub gatherer then skips step 4) |
| `registry_rows`, `outreach_threads`, `drafts_today` | read by the agent from `scratchpad_url`; empty on the first run, which the prompts tolerate |
| peer answers | the Session state block or the previous scratchpad |
| `oncall` | the `Oncall` line of board config (`yes` or `no`) |
| `email_mcp_prefix`, `email_address` | the `Email` line of board config; when absent, skip the email gatherer |
| `slack_user_id`, `slack_channels`, `tracker_project`, `tracker_epics`, `github_org`, `worktree_config`, `worktree_script` | board config |
| `prev_done_today`, `prev_rollover_time` | the previous row's Done today section, and the `Rollover started:` line in its scratchpad's Rollover log (else its Date at 00:00 UTC) |
| `declined` | the `declined` keys in the watch-slack state file (board config), dropping any older than 7 days; `none` when the file is missing |
| `running_waits` | the main session's list of running `~/bin/wait-for` commands; `none` when there are none |
| `tracker_report`, `github_report`, `slack_report`, `email_report` | this rollover's gatherer replies, verbatim |
| `confirmed_goal`, `carried_needs_you`, `blocked_rows` | the new row's Today's goal, Needs you and Blocked sections after the carry |
| `projects` | the Projects data source when configured: one line per row with name, Priority and the ticket keys named on its page |
| `today_row`, `carry_flag_days`, `loose_ends`, `loose_ends_age` | today's row url, the WIP limits line of board config, the `Loose ends` lines of `~/.claude/config/tidy.md` |
| `scratchpad_url`, `row_url`, `board_page` | today's scratchpad page, today's row, the `Board page` config line |
| `mode` | sync, rollover or edit |
| `poll_files` | paths of `slack-poll-triage.jsonl`, `slack-poll-held.jsonl` and `slack-poll-digest.jsonl` next to the poll state file, or `none` |
| `writer_inputs` | gatherer replies plus the main session's decisions (sync step 3), or the exact edits (edit mode) |
| `ticket`, `worktree_path`, `repo` | the registry row or the start command; `ticket` is the ticket key, or the short name in a no-ticket repo |


## Event log

Every landed fact is written once to the event log, and the board and the status page are rebuilt from it at checkpoints.

- Append: `~/bin/board-event add <kind> <key> "<one plain line>" [--link URL] [--field k=v]`, the moment a fact lands: a `wait-for` event, a registry stage change, a decision or approval, an answered ask, a reply that clears or adds a wait, a draft made or sent, a long-job count. `<key>` is the ticket key or project short name. Kinds: `merged`, `deployed`, `run-started`, `run-finished`, `failed`, `job-progress` (`--field job=<label> --field done=N --field total=N`), `job-done`, `decision`, `draft-created`, `draft-sent`, `waiting-on`, `needs-you`, `cleared`, `goal-tick`, `note`. The same event twice (today or yesterday) prints `exists <id>` and writes nothing; for a fact that may be re-reported later, pass a stable `--dedupe <run or thread id>`.
- Sub-agents append the same way, with `--by <agent name>`.
- `add` prints a second line `URGENT <id> ...` for `failed` and `needs-you` (or `--urgent`): run a checkpoint now.
- Read: `~/bin/board-event since <id>` or `today` (`--json` for raw lines).
- Checkpoint rule: Between checkpoints the session only appends events (`~/bin/board-event add ...`). Views are rebuilt at checkpoints: a sync, the wrap, when the user turns to the board (a status ask, "what's next", `/board`), and right away for an event `add` printed as `URGENT`. A checkpoint does one board-writer dispatch and one status publish for everything since their cursors. No writer dispatch or publish happens for a single non-urgent event.
- At a checkpoint, paste `~/bin/board-event since <Events through>` (from the Session state block; after `/clear`, from the scratchpad through the one-shot reader below; `today` only when the scratchpad has none) into `writer_inputs`, and hand the status publisher the checkpoint (it reads the log itself).
- Fallback: if `~/bin/board-event` is missing or `add` exits 1 with `warning: event not logged`, pass the fact in `writer_inputs` and hand the publisher one line, as before.

## Where facts go

- Dated progress (what merged, ran, was decided or sent) goes to the event log, the board and the ticket.
- Memory holds rules and pointers, never progress or run status.

## access (morning access check)

Runs once per day, before the first gatherer dispatch: at rollover, on the first sync of a day whose scratchpad has no `## Access check` section, or on `/board access`. It runs on its own: the user never has to ask for it or remember a login. Its job is to make sure the session holds every credential the day's work needs up front, so nothing stalls on the user later if they step away.

1. Read `~/.claude/daily-auth-last-run.json`; if it is not today's, run the `daily-auth` skill. Its `needs_user` lines go to the top of the row's `## Your TODOs` section through the next board-writer dispatch. Then run only the extra checks step 2 adds.
2. Anticipate: scan Today's goal, Needs you, the In-flight table and the Work registry for environments, hosts, repos or services they name (a prod health check needs the prod profile; an SFTP push needs that key; a database question needs that env file). Add a check for each one `~/.claude/auth-checks.json` already knows; name any it does not know as a gap. Run those extra checks and their fixes the way `daily-auth` does (fix right away, interactive fixes with a long timeout, anything the session cannot run goes to `## Your TODOs` as `! <fix>` marked "blocks: <what work waits on it>").
3. Record the results (through the same writer) in the scratchpad as `## Access check (<HH:MMZ>)`, one line per check with pass / fixed / needs user / gap. Before dispatching any agent that needs a failed credential, re-run that one check; if it still fails, tell the user which TODO line unblocks it instead of dispatching.

## sync

1. Read config and do the Notion setup above. Find the row with `Status = Open` (query the data source; fall back to fetching it). If none, or its Date is not local `date +%F`, run rollover first. If more than one row is Open, keep the newest and close the rest.
2. Run the access check if it has not run today. Then in ONE message dispatch four Explore gatherers (see Dispatching agents): `tracker-status` (opus), `slack-status` (opus), `github-status` (sonnet), `email-status` (sonnet; skipped when config has no `Email` line). Fill `{{oncall}}` from config; when it is `no`, the slack gatherer skips alert channels and nothing alert-shaped (monitors, error-tracker issues, alert tickets) goes on the page. Read `MEMORY.md` inline. Message idle peer sessions with the handoff ask only on rollover or `--sessions`; otherwise reuse the scratchpad's last answer marked "as of <time>". Never wait on a peer reply to write the page.
   Watch jobs ride on these gatherers (only with watch config): `slack-status` reports `NUDGE?` lines for the user's own asks with no reply after 3 business days, and `github-status` reports `PROPOSE` lines for the user's open PRs with no running wait. Pass both the declined keys from the watch-slack state file (drop any older than 7 days) and `github-status` the running waits. Drop any line a rule, a declined entry or an earlier answer settles, then ask the rest in one multi-select question, up to 4. A yes on PROPOSE starts the matching `wait-for`; a yes on NUDGE? drafts the nudge for approval; a no goes into `declined` with today's date (the main session writes the state file).
3. Write. Dispatch `board-writer` (sonnet, general-purpose, see Dispatching agents) once, with this run's gatherer replies, the events since the Session state block's `Events through` (see Event log), the decisions the main session made this run (answers, goal swaps the user confirmed, new drafts for the Drafts table, open questions to queue), and `poll_files`. It reads the stored `Row last edited after sync` from the scratchpad itself, reads the Slack poll files (the triage log's `not-now` lines, the held file and the digest, each since the last sync), merges and writes the row and the scratchpad by `writer.md`, and returns Your view plus a short "Session state" block (see writer.md). The main session keeps that block in the conversation as its working copy of the scratchpad and never fetches the scratchpad itself. Any goal swap it would propose comes back as a proposal, never written without the user.
4. On a sync run by rollover: if the writer reports no `## Standup` on the row, dispatch `standup-builder` (sonnet) with the gatherer replies and insert its output with a one-shot writer in edit mode (insert at the top of the row); if one exists, leave it and say so.
5. Print only Your view plus one pacing line that starts with goal progress (`goal 1/3`), then "Memory corrections to apply" if any. Apply memory edits and report them in one line.

Between syncs (start, resume, status, a single Projects edit), the main session uses the Session state block from the last writer reply. When it needs a scratchpad section it does not have (after `/clear`, or a section the block leaves out), it dispatches a one-shot reader (sonnet, Explore, read-only) that returns that one named section, never the whole page.

## Delivered, not confirmed

Shipping is not the finish line: a delivery is done when the person who asked has what they need. When a send or release lands, append a `draft-sent` (`--field delivers=true`) or `deployed` event; the writer keeps the row's `## Delivered, not confirmed` section by writer.md, including the Friday check. A nudge it flags goes under Needs you as a draft, never sent directly.

## Projects database

When config names a `Projects` data source, each long-lived workstream has one row there; its schema, page body and sync edits are in writer.md and `page-template.md`, applied by the writer.

- Decisions: when the user says something was decided, append a row to that project's Decisions table the same day. The public hub (if any) gets the team-facing version; the project page gets the private one.
- Memory files keep pointers and how-to-apply rules; project narrative moves to the project page. Propose, under "Memory corrections to apply", trimming any memory file whose facts now live on a project page.
- New workstream: propose a row in chat; create it only after the user says yes.
- Slack places: when a channel, a long-running thread or a DM turns out to belong to a project, record it the same day in four places: the project's notes (channel id, thread ts, who posts there), a `Slack:` line in the project page's `## Links`, the project's `links[]` on the status page, and, for channels, the `Watched channels` line in config.
- Finding a message "from" a partner or project: read its recorded places directly first. Search is the fallback; it lags a few minutes on fresh messages and `from:` misses external (shared-channel) authors.
- This is record-keeping, not a watch: it does not change what wakes the session.

## Project status page

When `~/.claude/project-status/config.json` exists (the `project-status` skill), the board keeps that page linked and current. Without the file, skip this whole section.

- Link: the first line of `## Your TODOs` on every daily row is `**Project status page:** <artifact_url>`. Rollover writes it on the new row; sync puts it back if it is missing. It is a link, not a TODO, and is never ticked or carried as an open item.
- Full refresh: rollover's sync runs the `project-status` skill's Refresh (gather, build, publish) after the Your view write, feeding its gather agent this run's gatherer replies so nothing is fetched twice.
- Keep it in sync at checkpoints, without being asked (see Event log): between checkpoints every landed fact is only appended as an event. At each checkpoint, hand the project-status skill's one-shot publisher (sonnet) one dispatch (its "Small updates"): it reads the events since `events_cursor` in `projects.json`, changes only the affected lines, builds and publishes. No gather for these. One-offs added or finished by hand still go to the publisher at the next checkpoint.
- Inbox mirror: on every sync, before the build, write the session-owned inbox items with `python3 ~/.claude/skills/project-status/inbox.py sync --origin board --file <scratchpad>/inbox-items.json`. The list holds: each unticked `## Your TODOs` line except the status page link (`todo`, logins `effort 2m`); each Needs-you line held by a sub-agent (`approve-agent`); each `## Drafts today` row with status `pending` (`send-draft`, link to the target thread); each `## Delivered, not confirmed` line (`confirm`, `since` = its delivered date, `due` = its confirm-by date). Other Needs-you lines are not mirrored: project asks reach the page through `projects.json` `needs_me`, and Slack not-now asks through the feed. Every item carries a stable id: `ref` from the line's link when it has one, else `id` built from the line's own key (draft id, ticket key plus kind, agent name plus ticket), never from its wording. Items no longer listed are marked done by the command. Between syncs, when one of these lands (an approval given, a draft sent), append an event; the next checkpoint runs `inbox.py done <id>` before the rebuild. At rollover, set the next meeting with `inbox.py meeting` only when the session knows it.
- Long jobs: when a long job reports progress (a backfill chunk lands), append a `job-progress` event (`--field job=<label> --field done=N --field total=N`); `job-done` when it finishes. The checkpoint's publisher applies them with `apply_events.py`.
- Every inbox mirror item carries its source link (`ref` or `link`) when the board line has one; fix any unlinked-mention warning from the build before publishing.
- Say it in one line per checkpoint ("status page updated: <what changed>"), never as a question. A failed publish is reported once and retried at the next checkpoint.

## Open questions (grouped interviews)

Questions for the user that surface mid-work (a seeding agent unsure of an owner, a conflicting fact, a choice between two shapes, a stale credential) are never left inside a long report or dropped. They queue and get asked in batches.

- Gate first. A question reaches the queue only when all three hold: (1) no source the session can read answers it (Slack, GitHub, the tracker, Dagster, files, a database); (2) no memory rule, Decisions row or earlier answer in this session settles it; (3) it is the user's call: a send to a person, a merge, a prod run or re-run, money, scope, a timeline, or anything outward-facing or hard to undo. Anything that fails a check is checked or applied, then reported in one line ("both review asks went out, 11:06 and 13:00"). "Interview me" and "anything pending?" mean ask what passes the gate, not everything pending.
- Queue: every open question goes to the scratchpad's `## Open questions for the user (not yet asked)` as one line: `- <project or ticket>: <question> | options: <a> / <b> | recommended: <x> | source: <agent or sync, HH:MMZ>`. Agent reports are scanned for them on arrival ("unsure", "left out", "conflict", "may be stale", "needs a decision").
- Ask with `AskUserQuestion`, up to four questions per call, each with the recommended option first and marked `(Recommended)`, grouped by project. Ask when any of these is true: the queue holds 3 or more; a queued question blocks work the user is waiting on (ask that one now, with whatever else is queued); the user turns to the board (a sync, a status ask, a "what's next"); or the oldest queued question is older than 60 minutes. Never ask one question at a time outside those moments, and never ask the same question twice. A call with a single question is allowed only when it blocks work the user is waiting on right now.
- Record each answer the same turn: a Decisions row on the project page (date, decision, why), a Needs-you or TODO line if it creates work, and remove the line from the queue. An answer of "later" moves the line to Deferred with the date.
- Questions the user has already answered in chat count as answered: check the conversation and the Decisions tables before queuing.

## Keeping facts current

The board's notes (scratchpad, memory, the user's own tracker comments) are snapshots. Other people's work keeps moving between syncs.

- A draft or page line that states a fact about someone else's work (their PR merged, a blocker still open, a report still failing) must be checked against the primary source on the same day: the GitHub report's "Epic PRs by others" section, `gh pr view`, or the Slack thread. If it cannot be checked, write it as a question to that person or mark it `as of <date>`.
- When a sync proves a note wrong, the correction goes to "Memory corrections to apply" and, for tracker comments, to Needs you as a one-line refresh for the user to approve.

## Notion write rules

The main session never fetches a board row, scratchpad or project page to edit it. Every write goes to a one-shot writer agent (board-writer, edit mode): give it the page, the exact lines and the heading each goes under; it returns one line per edit. One batch per agent, then it ends; a later edit is a new dispatch. Full rules: writer.md.

## Model discipline

Pass `model` on every dispatch. Planner, implementer, reviewer, pr agent, tracker and slack gatherers: opus. GitHub gatherer, standup-builder, board-writer and other mechanical work: sonnet. The main session never runs the external gathering (tracker, GitHub, Slack) itself; reading local files like `MEMORY.md` inline is fine.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing inbox items by editing `inbox.json` or putting GitHub review requests in it | Use `inbox.py`; GitHub and Slack not-now items come from `status-feeds` |
| Treating Explore as read-only | It still has Bash and every MCP write tool. The read-only rule is a prompt rule; every gatherer prompt carries it |
| Calling `/babysit-pr` from sync | It makes fixes. Sync reuses only its `gh pr list` query |
| Blocking the page write on a peer session reply | Replies can be held or expire. Write with the last known answer |
| Firing board edits with `allow_async: true` | They can fail silently and leave the page stale. Always `allow_async: false`, and re-fetch before a `replace_content` |
| Asking before a memory correction | Apply it and report it in one line |
| Creating an hourly Slack sweep cron | Retired. Rollover starts `~/bin/wait-for slack`; sync carries the NUDGE? and PROPOSE jobs |
| Drafting a reply that asserts the state of someone else's PRs or blockers from the board's own notes | Check the primary source first (Epic PRs by others, `gh pr view`, the thread) or ask them; notes older than a business day are snapshots |
| Tracking alerts, monitors or error-tracker issues when the user is not on call | Read the `Oncall` flag; `no` means alert channels are not read and alert items never reach the page |
| Asking the user for a login or VPN mid-day, or listing a login as a TODO instead of running it | The access check runs the `daily-auth` skill at the start of the day, which runs every fix itself (the user approves the prompt); the board adds checks for the day's environments. Only fixes that cannot run from the session go under Your TODOs |
| Dispatching a writer or publisher for each landed fact, or regathering everything for one change | Append an event; one writer dispatch and one publish per checkpoint (an `URGENT` event is one); full gather only at rollover |
| Treating a shipped or merged item as finished while the consumer has not confirmed | Put it in `## Delivered, not confirmed` with a confirm-by date; it leaves only on the consumer's confirmation or a recorded nudge after 5 business days |
| Leaving a sub-agent's "unsure" or "left out" items inside its report, or asking the user one question at a time as each one appears | Queue them in the scratchpad and ask in one grouped `AskUserQuestion` at the next trigger (3+ queued, blocking, the user turns to the board, or 60 minutes) |
| Asking "did that draft go out?", "delete this draft?" or "merge the PR you said to ship?" | Each fails the gate: Slack says whether it went out, a rule covers the draft, and the ship-it already covers the merge. Check or apply, then report in one line |
| Reading dispatch-prompts.md or page-template.md in the main session | Agents read their own section; see Dispatching agents |
| Fetching a Notion page in the main session to add one line | Hand the line to a one-shot writer |
