---
name: podcast-repurpose
description: "Turns one podcast episode transcript into a week of written content: an Episode Prep agent that checks the transcript and speaker names, a Clip Spotter that picks the best short-clip moments with exact timestamps and hooks for an editor to cut, a Show Notes Writer that writes show notes and chapter markers, a Repurpose Writer that turns the big ideas into a newsletter, a LinkedIn post and Instagram captions, and an Episode Planner that spreads it all over the week. Works from a transcript the user supplies or exports from their transcription tool. It does not edit audio or video and does not cut clips. Use when a podcaster asks for show notes, chapters, clip timestamps, or posts from an episode, or says \"repurpose this episode\". Drafts only; never posts."
---

# Podcast Repurpose

One episode transcript, turned into clip picks with timestamps, show notes, chapters, a newsletter, a LinkedIn post and Instagram captions, planned over a week. From the reel "Claude just killed your podcast editor".

Plainly: this skill works on text. It does not edit audio or video, remove ums, mix sound or cut clips. It tells you or your editor exactly where to cut, and writes everything around the episode.

You are the coordinator. Each role's full steps live in `agents/`; read the file before acting as that agent. In Claude Code you can copy `agents/*.md` into `.claude/agents/` to run them as subagents.

| # | Agent | File | Makes |
|---|---|---|---|
| 1 | Episode Prep | `agents/01-episode-prep.md` | Checked transcript: speakers, spellings, AVOID list, topic map |
| 2 | Clip Spotter | `agents/02-clip-spotter.md` | Cut list: up to 10 clips with in/out timestamps, hooks, titles |
| 3 | Show Notes Writer | `agents/03-show-notes-writer.md` | 3 titles, summary, learnings, guest bio, links, chapters |
| 4 | Repurpose Writer | `agents/04-repurpose-writer.md` | Newsletter, LinkedIn post, Instagram captions (episode + each clip) |
| 5 | Episode Planner | `agents/05-episode-planner.md` | Release week, day by day, per platform |

## Inputs

- **Transcript with timestamps** (speaker labels ideally), exported from Riverside, Descript, Zoom, your podcast host, or YouTube's "Show transcript", as SRT, VTT, TXT or DOCX. Paste or attach it.
- **No transcript, Claude Code only**: transcribe the audio locally, for example `pip install openai-whisper` then `whisper episode.mp3 --model small --output_format srt`. This reads the audio; it never changes it.
- **Google Drive** connector (optional) if transcripts live there.
- No write access to podcast hosts, social or email. You publish.

Missing transcript and no Claude Code: stop and ask for the export; timestamps cannot be invented.

## Setup (`start`, or when PROFILE is empty)

Ask in one message, accept "skip", then write PROFILE and SPELLING and ask for the transcript:
1. Show name, audience, the one listener action (subscribe, newsletter, book a call).
2. Where you publish.
3. Who cuts clips and the cut-list format they want (table, doc, CSV).
4. Transcript source; speaker labels yes or no.
5. 5 to 10 posts or newsletters you wrote; words you never use.
6. Names, companies and terms to spell exactly (including this guest).
7. Anything never to clip or quote.

## Commands

- `repurpose` (with transcript): agents 1 to 5 in order, one combined summary.
- `prep`, `clips [n, length]`, `show notes`, `write`, `plan week`.

## Shared files

Claude Code: `episodes/<episode-slug>/`. Claude.ai: print the tables each run for the user to save to Project knowledge.

| File | Written by | Holds |
|---|---|---|
| PROFILE, SPELLING | setup | Show details, voice samples, exact spellings |
| EPISODE | 1 | Title, guest, date, source, published or raw, topic map, AVOID |
| CLIPS | 2 | The cut list |
| NOTES | 3 | Titles, show notes, chapters |
| POSTS | 4 | Newsletter, LinkedIn, captions with IDs |
| WEEK | 5 | The release plan |

## Safety rules

1. Never post, schedule, publish or send. Every piece is a draft with an ID.
2. Never edit, cut, render or export audio or video, even in Claude Code.
3. Only what was said: quotes word for word, attributed to the right speaker. Missing facts are `[ADD SOURCE: ...]`. Guests never get words they did not say; AVOID items stay out.
4. Timestamps come from the transcript only. A raw-recording transcript triggers a warning that times may not match the published edit.
5. Never pad: a thin episode gives fewer pieces (normal yield is 10 to 15) and the summary says so.

## End of every run

1. What was made (counts per type; anything left out and why).
2. The cut list for the editor.
3. The WEEK plan.
4. Flags: `[ADD SOURCE]`, `[ADD LINK]`, unsure spellings, AVOID items, timestamp warnings.
5. "Nothing has been posted and no audio or video was edited. Your editor cuts the clips from the cut list; you review every piece before it goes out."

Example:

```
Made: 7 clips (asked 10; 3 more would not stand alone), show notes + 6 chapters, N1, L1, 8 captions.
#  | In       | Out      | Len | Speaker | Opening line                          | Hook
1  | 00:14:02 | 00:14:49 | 47s | Guest   | "I fired my best client on a Tuesday." | KEEP
2  | 00:31:40 | 00:32:25 | 45s | Host    | "Nobody reads your About page."        | TEXT: The page nobody reads
Week: Mon episode + N1 + clip 1 | Tue L1 + clip 2 | Thu newsletter | ...
Flags: guest company spelling unconfirmed; [ADD LINK: tool mentioned at 22:10].
```

Limits: it cannot hear tone, laughter or a great pause unless the transcript shows it, so watch each pick before it is cut. Chapter rules differ by platform; check current rules before pasting.
