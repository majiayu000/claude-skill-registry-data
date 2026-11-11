---
name: idea-bank
description: "Replaces a creator's ideas meeting: takes five creators in the user's niche, finds their videos that beat their own normal views by 3x or more, explains the topic, hook or format behind each, rewrites the best in the user's own experience with the original named, drops any idea the user cannot speak to from real experience, and ends with a month of video ideas in filming order, each with a hook. Use when a creator wants a month of content ideas, a calendar built from proven videos, or asks \"what should I film this month\". Public data and pasted numbers only; never logs in to any account."
---

# Idea Bank

Five agents: scout outliers in your niche, explain why they worked, make your version, drop what you cannot back with real experience, and plan the month in filming order.

Unlike a one-off viral breakdown, this keeps an EXPERIENCE list of what you have actually done, filters every idea against it, and always ends in a month CALENDAR.

## What you need

| Data | Claude Code | Claude.ai |
|---|---|---|
| YouTube views and dates | YouTube Data API v3 with your key in `.env` as `YOUTUBE_API_KEY` (public data only; setup in `agents/01-scout.md`) | Pasted list or screenshots of the channel's Videos tab |
| Instagram / TikTok views | Pasted numbers or profile-grid screenshots | Same |
| Transcripts | `yt-dlp --write-auto-subs --skip-download <url>` for public YouTube videos (the Data API cannot download other channels' captions) | "Show transcript" on the video page, pasted |
| Filming days (optional) | Google Calendar connector, read only | Same, or typed |

Missing numbers become a question or NOT ENOUGH DATA, never an estimate.

## Setup (`start`, or when PROFILE is empty)

Three rounds, accept "skip", show PROFILE and EXPERIENCE back, then suggest `full run`.

Round 1, niche
1. Your niche and viewer, in one sentence.
2. Platforms and formats (shorts, reels, TikTok, long-form).
3. Five creators you watch in your niche, with platform for each.

Round 2, what you have actually done
4. Things you have built, tested, sold, fixed or failed at in this niche. Rough notes are fine.
5. Which numbers can go on camera? Which stay private?
6. Topics you never cover.

Round 3, the month
7. Videos per week, filming days.
8. Fixed dates this month (launch, event, travel).
9. YouTube API key in Claude Code, or pasting numbers?

## Commands and routing

| Command | Runs |
|---|---|
| `full run` | 1 > 2 > 3 > 4 > 5, one summary |
| `scout` / `patterns` / `adapt` / `filter` / `plan month` | 1 / 2 / 3 / 4 / 5 |
| `add experience: <what you did>` | appends a dated line to EXPERIENCE, re-runs 4 on ASK and DROPPED ideas |
| `swap <date>` | replaces one calendar slot with the top backup |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-scout.md`: baseline = median of last 20 to 30 same-format videos; outlier = 3x+
- `agents/02-pattern-finder.md`: topic, hook or format driver; cross-creator patterns
- `agents/03-make-it-yours.md`: your angle on each pattern, original named
- `agents/04-honesty-filter.md`: KEEP / ASK / DROPPED against EXPERIENCE
- `agents/05-month-planner.md`: slots, ordering rules, batched filming days

## Safety rules (every agent)

- Outliers are judged against each creator's own baseline, never raw views across creators.
- Every view count, date and baseline names its source and capture date.
- Adapt, never copy: no reused footage, script lines, graphics, thumbnails or title wording. Every idea carries "Inspired by: <creator>, <video title>".
- Never write "I did X" for anything not in EXPERIENCE. Missing facts go in [brackets].
- Never ask for passwords or log in to any account. Keys stay in `.env`. Nothing is posted, scheduled, commented or messaged.

## Shared files

Claude Code: files in `ideas/`. Claude.ai: print updated tables at the end so the user can save them to Project knowledge.

- `PROFILE`: niche, viewer, platforms, formats, filming days, tone, private list
- `CREATORS`: creator | platform | handle | baseline | window | captured
- `OUTLIERS`, `PATTERNS`: agent 1 and 2 tables
- `EXPERIENCE`: one line per real thing done, dated where given
- `IDEAS`: idea | status KEEP / ASK / DROPPED (reason)
- `CALENDAR`: the month plan

## End of every run

1. One line per agent that ran.
2. CALENDAR (or the changed part).
3. ASK questions only the user can answer.
4. Data gaps (NOT ENOUGH DATA creators, TITLE ONLY breakdowns) and how to fill them.
5. "Nothing has been posted or scheduled."

Example (fake data):

```
Ran: Scout (5 creators, 4 with data, 11 outliers), Patterns (3), Adapt (14 ideas), Filter (8 KEEP, 3 ASK, 3 DROPPED), Plan (Nov, 12 slots, 8 filled, 4 OPEN).
Calendar: Tue 3 Nov "I tested 3 cold email tools for 30 days" (head-to-head, inspired by Creator B, "Tool X vs Tool Y") ...
ASK: 1) Did the 30-day test book 4 calls or 5?
Gaps: Creator E has 6 videos (NOT ENOUGH DATA); 3 outliers TITLE ONLY.
Nothing has been posted or scheduled.
```
