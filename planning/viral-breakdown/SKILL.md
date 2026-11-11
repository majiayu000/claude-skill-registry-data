---
name: viral-breakdown
description: "Researches a creator's niche: finds the creators actually winning, computes each creator's baseline views and keeps only videos that beat it by 3x or more, breaks down why each outlier worked from its transcript, adapts the best ideas into the user's own version with the source named, and once a week returns the top five ideas with hooks ready to film. Use when someone asks what to make next, wants competitor or niche research for short-form or YouTube, wants outlier videos in their niche, or wants a weekly idea radar. Uses public data and pasted numbers only."
---

# Viral Breakdown

Five agents study a niche so the user stops guessing what to post. Output of a normal week: five ideas that beat their own creator's normal by 3x or more, each with a hook ready to film. (For a month-long posting calendar, use a planning skill instead; this one ends at the weekly top five.)

## Where it runs and what each source can really do

| Source | Works in | Gives you |
|---|---|---|
| Web search | Claude.ai and Claude Code | creator discovery, public profile pages. NOT reliable view counts for Instagram or TikTok |
| `yt-dlp` (no login, no key) | Claude Code | YouTube and Shorts view counts, upload dates, auto captions |
| YouTube Data API key in `.env` (`YOUTUBE_API_KEY`) | Claude Code | the same YouTube numbers via the official API |
| User pastes numbers or a screenshot of the profile grid | both | Instagram, TikTok, LinkedIn view counts |
| User pastes transcripts | both | breakdowns for any platform |

The skill never logs in to any account and never asks for a password.

## Setup (`start`)

Ask in two short rounds, accept "skip", then save the answers as `PROFILE` and show it back.

1. Your niche in one or two lines, and who you want watching.
2. Platforms you post on, and how often.
3. What viewers should do after watching (follow, comment a keyword, buy, book).
4. Paste 3 to 5 of your past scripts or captions (best performer if you know it).
5. Creators you already watch or compete with (handles or links), and any to leave out.
6. Look-back window (default 90 days).
7. Claude Code: is `yt-dlp` installed (`yt-dlp --version`) or a YouTube API key set? Claude.ai: are you happy to paste Instagram/TikTok numbers?

## Commands

| Command | Runs |
|---|---|
| `start` | setup questions above |
| `full run` | agents 1, 2, 3, then 4 on the ideas the user picks |
| `outliers` / `breakdown <link>` / `adapt <idea>` | that single agent |
| `weekly radar` | agent 5 (which reruns 2 and 3 on new videos) |

## Agents

Read the agent file before running that step; it is the only home for that role's rules.

1. `agents/01-creator-scout.md`: 10 to 25 creators who post weekly to a similar audience.
2. `agents/02-outlier-finder.md`: baseline per creator, keeps videos at 3x or more.
3. `agents/03-breakdown.md`: hook, promise, structure and the idea underneath, from the transcript.
4. `agents/04-adapter.md`: the user's own version, source named, nothing copied.
5. `agents/05-weekly-radar.md`: the five best new ideas this week, each with a hook.

## Shared files

Claude Code: files in `research/`. Claude.ai: notes the user saves into the Project knowledge.

```
PROFILE.md      niche, audience, platforms, goal, voice samples
CREATORS.md     agent 1 table
OUTLIERS.md     agent 2 table, every row with source + capture date
BREAKDOWNS.md   agent 3, one entry per outlier
IDEAS.md        agent 4, status: new / picked / filmed / posted / skipped
RADAR-<date>.md agent 5 output
```

## Safety rules (every agent)

- Every view count, date and baseline names its source and capture date. Too little data = `NOT ENOUGH DATA`, never an estimate.
- Outliers are relative to the creator's own baseline, never raw views.
- Breakdowns come from transcripts; without one the entry is marked `TITLE ONLY`.
- Adapt, never copy: no reused footage, script lines, graphics, titles or thumbnails. The source is always named.
- API keys live in `.env`, never in chat.

## End-of-run output

```
VIRAL BREAKDOWN: weekly radar, captured 2026-01-12
Scout     14 creators on file, 2 quiet this week
Outliers  6 new at 3x+ (2 STAR), 3 TOO NEW rechecked
Breakdown 5 from transcripts, 1 TITLE ONLY (IG, ask user to paste captions)
Top five  RADAR-2026-01-12.md
Missing   @example_creator TikTok numbers: paste a grid screenshot
Next      "adapt 2" for a full draft of idea 2
```
