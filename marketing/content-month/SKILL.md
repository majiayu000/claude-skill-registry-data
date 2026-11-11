---
name: content-month
description: "Plans and writes a creator's or brand's whole month of Instagram posts before the month starts. Sets three or four content pillars from an export of their top posts, lays out a post for every day mixed across pillars, writes each caption and hook and the text for every carousel slide, flags anything off brand, unsupported or AI-sounding, and loads the month into a scheduler such as Metricool or Buffer as drafts (or a ready-to-load file) that only go live when the user approves them in that tool. Use when a user asks for a content calendar, a month of posts, content pillars, carousel copy for a month, or to fill their scheduler. Never publishes."
---

# Content Month

A whole month of posts planned, written and checked before the month starts, then waiting in your scheduler as drafts until you approve them. From the reel "Claude just killed your content calendar".

You are the coordinator. Each role's full steps live in `agents/`; read the file before acting as that agent. In Claude Code you can copy `agents/*.md` into `.claude/agents/` to run them as subagents.

| # | Agent | File | Does |
|---|---|---|---|
| 1 | Pillar Setter | `agents/01-pillar-setter.md` | 3 or 4 pillars from your posts that beat your normal by 3x |
| 2 | Calendar Planner | `agents/02-calendar-planner.md` | A post per posting day, pillars and formats rotated |
| 3 | Post Writer | `agents/03-post-writer.md` | Hook, caption, CTA, carousel slide text, in your voice |
| 4 | Post Checker | `agents/04-post-checker.md` | PASS / FIX / NEEDS YOU on brand, proof, AI tells, platform limits |
| 5 | Scheduler | `agents/05-scheduler.md` | Approved posts into your scheduler as drafts, or a ready-to-load file |

## Inputs and connections (be honest about each)

- **Your past posts with numbers** (needed for pillars): Meta Business Suite, Insights, Content, Export data (CSV), or screenshots. Claude never logs in to Instagram.
- **Voice samples**: 10 captions you wrote.
- **Scheduler**: Claude can only write to Metricool, Buffer or similar if you have set up a connector (MCP server) or API access in Claude Code that can save drafts. Without that, the Scheduler writes a file you load yourself (Metricool's CSV bulk upload, or copy-paste). Claude.ai without a scheduler connector = file only.
- **Google Calendar** (optional, read only): launches and events in the month.

Missing input: ask for that exact export or paste, run what can run, and say which parts used partial data.

## Setup (`start`, or when PROFILE is empty)

Ask in one message, accept "skip":
1. What you post about and who for (one sentence). Platforms and formats.
2. Your post export for the last 90 days.
3. 10 captions that sound like you; words, claims or topics you never use.
4. Proof you can use (results, testimonials, numbers) and what stays private.
5. Which month, posts per week, which days; fixed dates (launches, offers, events).
6. Your scheduler, and whether Claude has a draft-capable connection to it.

Show PROFILE back, then suggest `pillars`.

## Commands

- `full run`: agents 1 to 4, then stop and show the month for approval. Agent 5 never runs inside `full run`.
- `pillars`, `plan month`, `write <week or IDs>`, `check`, `rewrite <ID>`.
- `approve <IDs>` or `approve all passed`: marks posts approved in chat.
- `load`: agent 5, approved posts only.

## Shared files

Claude Code: `content/`. Claude.ai: print the tables at the end of each run for the user to save to Project knowledge.

| File | Written by | Holds |
|---|---|---|
| PROFILE | setup | Brand, audience, formats, voice samples, banned words, never-post list, scheduler |
| PILLARS | 1 | Pillars with evidence, PROVEN or UNPROVEN |
| CALENDAR | 2 | ID, date, pillar, format, angle |
| POSTS | 3, 4 | Full text and status (draft, fix, needs you, approved, loaded) |
| LOAD-LOG | 5 | What went where, as draft or file row, with the tool's IDs |

## Safety rules

1. Never publish. Agent 5 creates drafts only, in a tool confirmed to support drafts, or writes a file. The user approves again inside the scheduler.
2. Two approval gates: `approve` in chat, then approval in the scheduler.
3. Never invent a number, result, quote, testimonial or customer story. Unknown facts go in [brackets]; a post with open brackets cannot PASS.
4. Health, legal, money advice, competitors, private details, or the never-post list: NEEDS YOU.
5. Never ask for passwords. API keys live in `.env` in Claude Code, never in chat.

## End of every run

1. One line per agent that ran.
2. CALENDAR with status per post.
3. NEEDS YOU items, one line each.
4. What was loaded (drafts or file) and what to approve in the scheduler.
5. "Nothing has been published."

Example:

```
Ran: Calendar Planner (22 posts), Post Writer (week 1, P1-P5), Post Checker.
ID | Date   | Pillar         | Format   | Status
P1 | 01 Mar | Tool tutorials | carousel | PASS
P2 | 02 Mar | Client stories | reel     | NEEDS YOU: result [x% faster] has no source
P3 | 04 Mar | Behind the build | photo  | FIX: hook rewritten (was a generic question)
Loaded: nothing yet. Type approve P1 P3 then load.
Nothing has been published.
```
