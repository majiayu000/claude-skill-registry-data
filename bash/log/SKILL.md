---
name: log
description: Writes one day's work log as a file — what moved in the tracker, what was on the calendar, what was decided, what other people said about your work, and links to the evidence. Built to run unattended on a schedule, so it never asks and never invents; a source it cannot reach is reported as missing rather than filled in. It also looks back a few days and fills the gaps an earlier run left. Turning these files into accomplishment statements is /pm:log-review. Triggers - explicit invocation only - "/pm:log", "write the log for today", "fill in the days that were missed", "일지 써줘", "업무 일지 작성", "빠진 날 채워줘".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-query-data-sources, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-get-users, mcp__claude_ai_Slack__slack_read_channel, mcp__claude_ai_Slack__slack_read_thread, mcp__claude_ai_Slack__slack_search_public_and_private, mcp__claude_ai_Google_Calendar__list_events, mcp__plugin_github_github__issue_read, mcp__claude_ai_Slack__slack_read_user_profile
---

# log — one day, one file

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

Assembles a day's work log from the tracker the task skills already use, plus a calendar and chat where you name them, and writes it as a single markdown file. Reads everywhere, writes one place: a file under `log.out.dir`. Nothing is written back to the tracker.

Built for a scheduler. It runs with nobody watching, so the rules below lean hard on *say what you could not do* rather than *fill it in anyway*.

**It records; it does not appraise.** These files are the raw material a later review turns into accomplishment statements — that is `/pm:log-review`. This skill's job is to capture, on the day, the things that cannot be reconstructed months later: who said what about your work, what was decided and why, and the link that proves a piece of work existed. It never rates the importance of anything, and it never writes a sentence a source did not supply.

## Principles

- **Never ask.** There is no one to answer. A missing value is skipped and named in the closing summary.
- **Never invent.** Every line traces to something a source returned. An empty section gets `log.empty_line`, not a plausible sentence.
- **Quote, do not characterise.** Praise, criticism and decisions are recorded in the words they were said in, with a link. Do not summarise someone's opinion into your own phrasing — a later review needs the original.
- **Read the tracker's schema before querying it.** Property names drift and differ per workspace. Fetch the data source and use the names it currently has. Never trust names pinned in this document or in config.
- **A source that fails does not stop the run.** Write the log from what did come back, and record what did not.
- **The file is the output.** No preview gate — the target is a file in the user's own log directory, and every other system is read-only here.
- **Yesterday is still fixable.** Every run re-checks the recent past and repairs what an earlier run missed.

## Configuration

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml
```

`log.enabled: false` means stop immediately and say so — that is a correct outcome, not an error. `task.record` gives the tracker; `log` gives everything else. A `null` source is skipped and named in the summary.

## 1. Settle the date

Get today in the local timezone from the shell, not from memory. Everything downstream keys off this one value.

```bash
date +%Y-%m-%d
```

## 2. Learn the tracker's shape

**The calls live per tracker, not in this document.** Read the record's adapter before querying anything; a `type` of `none` means there is no tracker — skip section 3 and say so in the summary.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.record.type} --role record
```

It prints the file to read — the bundled one, or yours from `adapters.dirs` where you drafted one. **Exit 3 means no adapter exists for that type.** Stop and say so; `/pm:setup` drafts one from the tools connected on this machine. Do not improvise the calls, and do not fall back to a tracker the config did not name. **Exit 4 means the adapter exists but answers for the other side** — a mirror-only file asked for the record, say. Stop the same way; 3b drafts the side that is missing. Say what it means in the person's words — "this tool isn't supported yet; `/pm:setup` can add it from what's connected here" — never the exit code or the file path.

Whatever the tracker, read its **current** schema or field names immediately before querying, and use what it has now — the title, status, assignee, project, grouping, priority, due-date and progress equivalents, and the exact spellings a query needs. Names drift and differ per workspace. A name pinned in a document or in config returns nothing, and nothing looks exactly like a quiet day.

If that read fails, skip section 3 and say so. Do not fall back to guessed names.

## 3. Collect what moved

Query rows the day actually touched, split by whether they are yours.

- **Mine** — assignee contains `log.me.tracker_user_id`, last-edited on the date.
- **The team's** — assignee is anyone else or empty, last-edited on the date.

Query on **last edited or last updated**, never on created. Work in progress was created weeks ago; a created-date filter returns a nearly empty day and looks like a correct answer.

How the day filter is applied is the tracker's business. A store that can be queried exhaustively takes it as a condition; one that can only be searched needs the filter applied after the fetch, and its adapter says so. **Where the exhaustive read is gated or missing, say so in the summary** — an under-covered day must never read as a quiet one.

Carry each row's **stable url** alongside its title. Titles get rewritten; urls do not, and a later review stitches months of entries together by url. A row recorded without its url cannot be stitched.

Where the previous entry for the same url shows a different status, note the transition rather than the state alone — `in progress → done` says something `done` does not. Rows that reached a terminal status today go into the front matter's `completed` list as title and url.

Resolve assignee ids to names through `log.people`. An id that is not there is looked up once against the tracker's user directory and used as found. Never guess a name from an id, and never infer one from an adjacent mapping — say the id was unresolved instead.

## 4. Collect the day around it

- **Calendar** — `log.sources.calendar`, the day in local time, ordered by start. Drop working-location, birthday and out-of-office entries. Each event becomes time, title, and one or two key attendees. The calls are in the adapter for `sources.calendar_type` (`adapter.py --kind sources --role calendar`); `none` skips the calendar and says so.
- **Chat** — `log.sources.chat_channels` for the day, plus messages the user sent or was mentioned in. Keep decisions, questions and answers, feedback, shared material, and open threads. Drop chatter, bots and reactions. The calls are in the adapter for `sources.chat_type` (`--role chat`); `none` skips chat and says so, and exit 3 means the tool has no adapter yet — skip the section, and name that in the summary rather than reading a tool the config did not name.

From the same pass, pull out two things that are cheap now and unrecoverable later.

- **What others said** — messages *about* the user's work: thanks, praise, criticism, an accepted proposal, a request that names them as the one to do it. Record the sender, the quote as written, and the permalink. Do not include something merely because the user was mentioned in it, and do not soften or sharpen the wording.
- **Decisions** — a decision the user made or took part in, with the reason **as the source states it**. No reason in the source means no reason in the file. Do not reconstruct rationale.

- **Your own notes** — `log.sources.notes_channel` is a channel only you write in, so everything
  there is yours by definition and nothing needs tagging. Read the day's messages and drop the
  ones an app posted on your behalf: the workspace attributes those to the app, and the ids to
  ignore are in `log.sources.notes_exclude_apps`. Nothing you did not type belongs here.

  **Carry the text across, not a link to it.** Chat retention expires; this file does not, and
  a log that points at a message nobody can open years later has not recorded anything. Keep the
  time, the body as written, and the permalink alongside it.

Chat search tools cap their response size. Ask for concise output without surrounding context, and page rather than widening a single call — an over-large request fails outright and returns nothing, which reads as silence.

## 5. Assemble

Write `log.out.dir/YYYY/MM/YYYY-MM-DD.md`. Front matter carries `log.out.front_matter`; counts are counts and `completed` is an index of title and url, never a second copy of the body. Sections follow `log.sections` in order, and a section with nothing in it gets `log.empty_line`.

What belongs where, given the default section names:

| Section | What goes in |
|---|---|
| What I did | Three to six lines. Your own work and the discussions you personally drove |
| Meetings | One line per event, with the decision or the point of it |
| My tasks | Rows from section 3, mine. Title with url, priority, status transition, progress, project, grouping, due |
| Team tasks (reference) | Rows from section 3, the team's, each with its owner. Plus items discussed today that have no row yet |
| Decisions | What was decided, and the stated reason. One line each |
| What others said | Sender, quote, permalink. Verbatim |
| Evidence | Links to what the day produced — a change request, a design node, a document, a release announcement |
| Notes | What you typed to yourself that day — meeting notes, memos, things to look into. Body as written, with time and permalink |
| Follow-ups | Threads still open, each with the action it is waiting on |
| Tomorrow | One to three unchecked boxes, drawn from what is unresolved |

Where the file already exists with a body, update it rather than replacing it — preserve anything a human added by hand.

Prose follows whatever writing standard applies in `meta.language`.

## 6. Fill the gaps behind you

Look back `log.backfill.business_days` business days. For each one, check the file exists and its sections are not all empty. A day whose file is missing is written now, from the same sources scoped to that date. A day whose file exists but has an empty section the sources can now fill gets that section filled — nothing else on the page is touched.

Limit the look-back to the configured window so a long absence does not turn one run into a backfill of the whole quarter. Say in the summary how far back you went and what you repaired.

## 7. Summarise

Close with a few lines: the file path, the counts that went in, what the gap check repaired or that it found nothing, and any source that was skipped along with why. This summary is the only thing a scheduled run leaves in its own log, so it has to be enough to diagnose a bad day from.

## When NOT to invoke

- Turning these files into accomplishment statements → `/pm:log-review`
- Writing a task record's context table → `/pm:task-draft`
- Filing a task in an engineering tracker → `/pm:task-publish`
- Reconciling two trackers → `/pm:task-sync`
- Writing requirements → `/pm:prd`
