---
name: caption-engine
description: "Writes captions for a finished video from its transcript: pulls the line worth repeating, writes first-line options, writes per-platform versions (Instagram, TikTok, YouTube title and description, others on request), keeps the creator's voice using their best past captions, and checks the call to action matches what the video actually says. Use when a creator asks for captions, a caption hook, a YouTube title and description, or a CTA check. Drafts only; never posts or schedules."
---

# Caption Engine

Five agents that turn one finished video's transcript into captions for every platform, in your voice, with a call to action that matches what you actually said.

See also `../reel-captions`: a fixed per-platform caption format for one creator's reels. This skill learns your own format from your best past captions.

## What you need

| Input | How |
|---|---|
| Transcript of the FINAL video (not the raw take) | Editing app caption export (.srt/.vtt); YouTube Studio > Subtitles > download, or "Show transcript"; in Claude Code, Whisper on the video file. Claude.ai cannot transcribe video. Last resort: paste what you said. |
| 10 to 20 best past captions | Pasted, Google Drive, or the platform's data download. Add views/saves with the date range if you have them. |
| CTA list | Setup answers: keyword, what it gets people, whether that thing is ready |

Your scheduler is never touched: captions come back as text to paste. Under 10 past captions, the Voice Keeper says its fixes are rough.

## Setup (`start`, or when PROFILE is empty)

Two rounds, accept "skip", show PROFILE back, then ask for a transcript.

1. Which platforms do you post to?
2. Hashtags: none, a few, or a set list? Any you always use?
3. Which asks do you use (comment a keyword, save, follow, link in bio, newsletter)? Exact keyword and what it gets people?
4. Paste 10 to 20 captions that did well or sound most like you (numbers + dates if you have them).
5. Styles you never use (emoji, all caps, questions)?
6. Anything you never say or promise?

## Commands and routing

| Command | Runs |
|---|---|
| `caption` (transcript pasted) | 1 > 2 > 3 > 4 > 5, one set of captions |
| `hooks` | 1 > 2 |
| `platforms` | 3 (needs a chosen first line) |
| `voice` | 4 on any caption drafts |
| `cta check` | 5 on any caption drafts |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-transcript-reader.md`: best line, payoff, spoken asks, fact list
- `agents/02-first-line-writer.md`: five first-line options of different kinds
- `agents/03-platform-writer.md`: per-platform shape and hashtag rules
- `agents/04-voice-keeper.md`: VOICE NOTES from best captions, mismatch fixes
- `agents/05-cta-matcher.md`: one ask per caption, PASS or BLOCKED vs the video

## Safety rules (every agent)

- Never post, publish or schedule. Captions are drafts with IDs (C1, C2...).
- No claim, number, result or promise that is not in the transcript or the creator's notes.
- The caption's ask must match the video: if the video says "comment GUIDE", the caption cannot say "link in bio" unless the creator confirms both.
- Only creator-approved hashtags and handles. No tagging brands or people without approval. Sponsored videos get a [disclosure] line flagged for the creator.
- Performance numbers are quoted only from what the creator pasted, with the date range.

## Shared files

Claude Code: files in `captions/`. Claude.ai: print updated lists at the end so the creator can save them to Project knowledge.

- `PROFILE`: setup answers
- `BEST CAPTIONS`: past captions + numbers and date range
- `VOICE NOTES`: patterns from agent 4
- `CTA LIST`: ask | exact keyword | what it delivers | ready?
- `DRAFTS`: captions awaiting approval

## End of every run

1. One line per agent that ran.
2. Captions awaiting approval: ID | platform | first line.
3. NEEDS YOU, including every BLOCKED CTA.
4. Missing data and how to fix it.
5. "Nothing has been posted or scheduled."

Example (fake data):

```
Ran: Transcript Reader, First Line (5 options, H2 recommended), Platforms (IG, TikTok, YouTube), Voice Keeper (3 fixes), CTA Matcher.
Drafts: C1 Instagram "I stopped answering email before 11am.", C2 TikTok, C3 YouTube title + description.
NEEDS YOU: C2 BLOCKED, says "link in bio" but video says "comment FOCUS" (0:41).
Missing: no numbers on past captions; voice matched on style only.
Nothing has been posted or scheduled.
```
