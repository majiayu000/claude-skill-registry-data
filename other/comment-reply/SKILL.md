---
name: comment-reply
description: "Works through a YouTube channel's comments: pulls new public comments since the last check with the YouTube Data API (commentThreads.list) and the user's API key in Claude Code, or takes pasted comments, labels each, drafts short replies in the creator's voice that answer the actual question, turns repeat questions into video ideas, and puts anyone asking to buy, hire or work together at the top. Use when a creator asks to check comments, draft comment replies, find leads or find video ideas in comments. Drafts only; never posts a reply."
---

# Comment Reply

Five agents that pull your new comments, label them, draft replies, find repeat questions worth a video, and put real leads at the top. You review the drafts and post the ones you like.

## What you need (be clear which path you are on)

| Path | How comments get in | What works |
|---|---|---|
| Claude Code + API key | YouTube Data API v3, `commentThreads.list`, key in a local `.env` as `YOUTUBE_API_KEY` (setup in `agents/01-comment-puller.md`) | Everything. Pulls only public comments; cannot see comments held for review |
| Claude.ai, or no key | Paste or export comments (YouTube Studio > Comments, or Instagram/TikTok copy or data download) | Agents 2 to 5 work the same on pasted text |

Posting replies needs a separate OAuth sign-in with write scope (`comments.insert`). This skill does not set that up: the creator copies approved drafts into YouTube Studio.

## Setup (`start`, or when PROFILE is empty)

Two rounds, accept "skip", show PROFILE back, then suggest `sweep`.

1. Channel ID (starts with `UC`; YouTube Settings > Advanced settings) or handle.
2. Claude Code with an API key, or pasting? No key yet: walk through agent 1's setup.
3. How far back on the first run? Default 7 days.
4. Paste 5 to 10 comment replies you wrote, for voice.
5. Answers to your most common questions (FAQ), and links you are happy to share.
6. What counts as a lead (sponsors, clients, buyers, collabs), and where they go (email, form, `<your booking link>`)?

## Commands and routing

| Command | Runs |
|---|---|
| `sweep` | 1 to 5, one summary |
| `pull` / `sort` / `drafts` / `ideas` / `priority` | 1 / 2 / 3 / 4 / 5 alone |

Runs when you run it. For a daily sweep, `/schedule` a routine in Claude Code with the prompt `sweep`; it still only writes drafts.

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-comment-puller.md`: key setup, API call, paging, STATE
- `agents/02-comment-sorter.md`: five labels and tie-break order
- `agents/03-reply-drafter.md`: under 40 words, answer first
- `agents/04-idea-finder.md`: 3+ asks = idea
- `agents/05-priority-list.md`: leads, unreplied and oldest first

## Safety rules (every agent)

- Never post, like, heart, pin, hide, delete or report. Replies are drafts with IDs (D1, D2...).
- API key lives in a local `.env` (in `.gitignore`), restricted to YouTube Data API v3. Never print it, never put it in a skill file or chat.
- Never click links in comments.
- No invented answers, links, prices, dates or promises. Unknown answer = NEEDS YOU.
- Complaints, criticism of the creator, safety, legal or medical questions, anything upsetting: NEEDS YOU, no auto-written comeback.
- Commenter names stay in the creator's own files. Never look up a commenter's private details.

## Shared files

Claude Code: files in `comments/`. Claude.ai: print updated tables at the end so the creator can save them to Project knowledge.

- `PROFILE`: setup answers
- `STATE`: channel ID, last-checked time
- `COMMENTS`: id | video | author | date | text | label
- `FAQ`: approved answers
- `DRAFTS`: replies awaiting approval
- `IDEAS`: question groups with running counts
- `LEADS`: lead | status (NEW, REPLIED, MOVED TO EMAIL, NOT A FIT; only the creator changes status)

## End of every run

1. One line per agent, with period covered and comment count.
2. Priority leads.
3. Drafts awaiting approval: ID | video | one line.
4. NEEDS YOU items.
5. New video ideas.
6. "Nothing has been posted. Copy approved replies into YouTube Studio to post them."

Example (fake data):

```
Ran: Puller (4 to 11 Oct, 212 comments, 4 API calls), Sorter, Drafter (38), Ideas, Priority.
Leads: 1) "do you build these for agencies?" (5 days, no reply) D1  2) sponsor ask from a tools brand, D2
Drafts: D1-D38. NEEDS YOU: 3 (2 criticism, 1 question with no FAQ answer).
Ideas: "How do you back up the automations?" asked 7x on 3 videos.
Nothing has been posted. Copy approved replies into YouTube Studio to post them.
```
