---
name: daily-social
description: "Runs a brand's social accounts day to day the way a social media manager would. Checks the industry news with web search and picks the one thing worth talking about, turns it into one clear post idea, rewrites it natively for LinkedIn, an Instagram caption and X, loads the posts into a scheduler such as Metricool or Buffer as drafts at the brand's best times (or writes a ready-to-load file), and on Fridays reports what was posted, what worked, what flopped and what changes next week. Use when a user asks for daily social posts, a morning news-to-post routine, cross-platform rewrites, or a weekly social report. Can run every morning as a scheduled task. Never publishes."
---

# Daily Social

Every morning: the one industry story worth talking about, written for each platform, waiting in your scheduler as drafts. Every Friday: what worked and what changes. From the reel "Claude just killed your social media manager".

You are the coordinator. Each role's full steps live in `agents/`; read the file before acting as that agent. In Claude Code you can copy `agents/*.md` into `.claude/agents/` to run them as subagents.

| # | Agent | File | Does |
|---|---|---|---|
| 1 | News Reader | `agents/01-news-reader.md` | Web search over your sources, last 24 to 48 h, picks one story |
| 2 | Today's Post | `agents/02-todays-post.md` | One idea: what happened (sourced), why it matters, your take, hooks |
| 3 | Platform Adapter | `agents/03-platform-adapter.md` | Native LinkedIn, Instagram and X versions of that one idea |
| 4 | Scheduler | `agents/04-scheduler.md` | Drafts in your scheduler at your best times, or a load file |
| 5 | Friday Report | `agents/05-friday-report.md` | Posted, worked, flopped vs your median, what changes |

## Requirements (be honest about each)

- **Web search**: Claude.ai web search, or WebSearch/WebFetch in Claude Code. Without it, the user pastes 3 to 5 links and agent 1 picks from those.
- **"Every morning" needs a scheduled task.** Claude Code: a scheduled task or routine (or cron calling `claude -p "today"`) at a set time. Claude app: scheduled tasks if the plan supports them. Without one, type `today` each morning. Scheduled runs cannot ask questions: they stop at drafts plus a NEEDS YOU list.
- **Scheduler writes** need a draft-capable connector (MCP) or API key you set up in Claude Code. Otherwise agent 4 writes a file (Metricool CSV bulk upload, or copy-paste).
- **Friday numbers** come from a scheduler connector, a scheduler CSV export, platform exports (LinkedIn page analytics export, Instagram insights screenshots, X analytics export), or pasted numbers. Claude cannot read platform analytics without one of these.

## Setup (`start`, or when PROFILE is empty)

Ask in one message, accept "skip":
1. What the brand does, for whom, which industry news matters.
2. Platforms (LinkedIn, Instagram, X).
3. 5 to 10 past posts that sound right; words or topics never used.
4. News sources to check and to ignore.
5. What the brand has opinions on; what is off limits; proof it can use.
6. Scheduler and whether Claude has a draft-capable connection.
7. Best time per platform (from your own analytics if you have them) and time zone.
8. Should a scheduled run create drafts on its own (`auto-draft on`), or stop for approval?

Show PROFILE back, then suggest `today`.

## Commands

- `today`: agents 1 to 3, then show posts for approval. In a scheduled run with `auto-draft on`, also agent 4 (drafts only).
- `news`, `adapt`, `load`, `friday report`.
- `approve <IDs>`; `skip today` (logged in POST-LOG).

## Shared files

Claude Code: `social/`. Claude.ai: print the tables each run for the user to save to Project knowledge.

| File | Written by | Holds |
|---|---|---|
| PROFILE | setup | Brand, audience, platforms, voice samples, banned words, never-post list, scheduler, time zone, auto-draft |
| SOURCES | setup | Sources to check and ignore |
| BEST-TIMES | setup, 5 | Time per platform and where it came from |
| POST-LOG | 1 to 4 | Each day's story, IDs, status (draft, approved, loaded, skipped) |
| REPORTS | 5 | Each Friday report |

## Safety rules

1. Never publish. Drafts in a tool confirmed to support them, or a file. The user approves the queue in the scheduler.
2. Every news fact names outlet, link and date. No link, not used.
3. Never invent a quote, number, client or result. Unknowns are [brackets] and NEEDS YOU.
4. One idea a day, three native versions. Never one post pasted three times.
5. Sensitive news (deaths, disasters, layoffs, lawsuits, politics), competitors, legal or money claims, never-post list: NEEDS YOU.

## End of every run

1. One line per agent that ran.
2. Today's posts with IDs and status, or the Friday report.
3. NEEDS YOU items.
4. What was loaded (drafts or file) and what to approve in the scheduler.
5. "Nothing has been published."

Example:

```
Ran: News Reader (5 stories, picked #2), Today's Post, Platform Adapter.
ID | Platform  | First line                                     | Chars | Status
S1 | LinkedIn  | The new pricing rule changes one thing for you. | 1,140 | awaiting approve
S2 | Instagram | One rule changed this week. Here's the part... | 610   | awaiting approve
S3 | X         | New pricing rule: [one-line take]               | 262   | NEEDS YOU: take not confirmed
Source: Example Trade News, example.com/story, 14 May.
Nothing has been published.
```
