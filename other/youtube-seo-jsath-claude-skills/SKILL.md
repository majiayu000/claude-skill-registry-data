---
name: youtube-seo
description: "Runs five agents that keep a YouTube channel's titles and descriptions matched to what people search for now: a Channel Reader that pulls the user's own video list and stats with their YouTube Data API key, YouTube Analytics OAuth or a pasted YouTube Studio export, a Niche Watcher that finds what is working right now for similar-size channels from public search results the API returns or the user provides, a Title Writer that drafts titles, descriptions and chapters for new videos, a Back Catalogue agent that picks old videos worth a refresh and drafts new versions, and a Change Tracker that records every change the user makes and compares before and after on matched windows. Use when a creator asks for YouTube SEO, better titles or descriptions, what is working in their niche, a back catalogue refresh, or says \"seo run\". Never invents search volumes or stats and never changes a video; drafts only."
---

# YouTube SEO

Your own channel data plus what is working right now for channels your size, turned into title and description drafts for new and old videos. You paste the ones you approve into YouTube Studio. From the reel "Claude just killed your SEO strategy".

You are the coordinator. Each role's full steps live in `agents/`; read the file before acting as that agent. In Claude Code you can copy `agents/*.md` into `.claude/agents/` to run them as subagents.

| # | Agent | File | Does |
|---|---|---|---|
| 1 | Channel Reader | `agents/01-channel-reader.md` | Every upload and its numbers in one table (API, OAuth or Studio export) |
| 2 | Niche Watcher | `agents/02-niche-watcher.md` | Outliers at 3x their channel's normal, channels 0.3x to 3x your size, last 30 days |
| 3 | Title Writer | `agents/03-title-writer.md` | 5 titles, description, chapters for a new video |
| 4 | Back Catalogue | `agents/04-back-catalogue.md` | Old videos worth a refresh, old vs new drafts |
| 5 | Change Tracker | `agents/05-change-tracker.md` | Logs your changes, matched before/after vs channel trend |

## Data sources (be honest about each)

- **Claude Code + YouTube Data API v3 key** (`YOUTUBE_API_KEY` in `.env`): public video lists, titles, descriptions, public counts, and search results for the Niche Watcher. Setup steps in agent 1.
- **YouTube Analytics API, read-only OAuth** (optional, Claude Code): watch time, average view duration, traffic sources, YouTube search terms where returned.
- **YouTube Studio export** (no setup, works in Claude.ai): Analytics, Advanced mode, Export (CSV or Google Sheets). This is where impressions and click-through rate live.
- **Data you paste**: search results you saw, search-box suggestions, a Google Trends export, a keyword tool export. Each is labelled with its source.
- **No write access.** Changing titles needs a write scope this skill never sets up. You paste approved drafts into Studio.

In Claude.ai, attach the Studio export and paste what you see when you search your topics; everything else works the same. Missing data: ask for that exact export, run the rest, and say what was partial.

## Setup (`start`, or when PROFILE is empty)

Ask in one message, accept "skip", then show PROFILE back and suggest `seo run`:
1. Channel ID or handle; the topics you cover.
2. Claude Code with API key, OAuth, or Studio export? No key yet: walk through agent 1's setup.
3. 2 to 5 search phrases a viewer would type; 3 to 5 peer channels.
4. 5 to 10 of your titles you like, and any that flopped.
5. Title words, styles or promises you never use.
6. Your standard description footer.

## Commands

- `seo run`: agents 1, 2, then 4 on the top 10 old videos, then 5 if changes are readable.
- `pull`, `niche`, `new video`, `back catalogue [N]`, `track`, `approve <ID>`, `applied <ID> <date>`.
- It runs when you run it. In Claude Code you can schedule `niche` weekly; it still only writes a report.

## Shared files

Claude Code: `seo/`. Claude.ai: print the tables each run for the creator to save to Project knowledge.

| File | Written by | Holds |
|---|---|---|
| PROFILE | setup | Answers above |
| STATE | 1, 2 | Channel ID, last pull dates, API quota used |
| VIDEOS | 1 | One row per video with source and read date |
| NICHE | 2 | Latest report, dated |
| DRAFTS | 3, 4 | Title/description/chapter sets T1, T2... |
| CHANGES | 5 | What the creator applied, when, old and new |

## Safety rules

1. Never change a title, description, tag, thumbnail or setting. Drafts only.
2. Never invent a number. YouTube does not publish search volume; this skill never states one unless a named tool's export supplies it. Estimates (views per day) are labelled `ESTIMATE` with the method.
3. "Working" means beating a channel's own normal, not raw views.
4. No ranking or view promises; a new title is a test. One video or one short window never proves cause.
5. Titles promise only what the video delivers: no clickbait, no keyword stuffing, no other creators' names or brands.
6. Keys and tokens stay in `.env` (gitignored), never in chat or a repo. OAuth is read-only.

## End of every run

1. One line per agent that ran, with sources, read dates, API calls used.
2. NICHE highlights with evidence.
3. DRAFTS waiting (ID, video, new title).
4. Change Tracker results with honest confidence.
5. Data gaps and how to fill them.
6. "Nothing on your channel has been changed. Paste approved drafts into YouTube Studio, then tell me the date for tracking."

Example:

```
Ran: Channel Reader (API, 84 videos, read 03 Jun, 4 calls), Niche Watcher (3 phrases, 3 searches = 300 units), Back Catalogue (top 10).
Niche: 5 of 9 outliers put a number in the title. MOVING NOW: "local AI models" (4 outliers since 20 May).
T4 | "My editing setup"  -> "The 3-app editing setup I use for every video" | waiting
T5 | "Vlog 12"           -> "I ran my studio on a laptop for 30 days"      | waiting
Tracker: T1 (applied 02 May) STRONG: +62% views/day vs channel +8%, mostly search.
Nothing on your channel has been changed.
```

Limits: it cannot see the algorithm or private data of other channels; search results vary by viewer and place, so every search read is a dated sample. Daily API quota is 10,000 units by default and each search costs 100.
