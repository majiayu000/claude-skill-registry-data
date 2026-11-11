---
name: reel-ideation
description: "Finds the top creators in your niche and their recent viral reels and Shorts with proof (likes, views, comments, date, link, multiple of the creator's own median) using Agent Reach and yt-dlp, turns raw voice-dictation dumps (Wispr Flow, voice notes) into numbered ideas so none get lost, and writes full word-for-word scripts that copy a proven viral's format and structure (never its words), with 3 hooks of different types per idea, both CTA endings, and a RECORD-SHEET.md you read off while filming. Use for 'what should I post', 'find me virals in my niche', 'turn my rant into ideas', 'write tomorrow's scripts', 'make a record sheet'."
author: Johann (@johannships)
version: 1.0.0
---

# Reel ideation: proven virals in, record sheet out

Step 1 of the pipeline: **idea -> script** -> record -> `footage-ingest` ("the card is in") -> `edit-style` -> `trial-post` -> `reel-scorecard`.

The rule this skill exists for: **only proven ideas.** Invented idea lists feel clever and flop. Every idea here
traces to a real video in your niche that already went viral, with the link and the numbers. You copy the idea,
the format and the structure. You never copy the words, the creator's story or their results.

## Requirements

| need | for | install / check |
|---|---|---|
| Claude Code (preferred) | running Agent Reach, yt-dlp, whisper, writing files | `claude --version` |
| Agent Reach | creator discovery, profile pages, YouTube transcripts, search | `pip install agent-reach` (or the install prompt in its README: github.com/Panniantong/agent-reach), then `agent-reach doctor` |
| yt-dlp | logged-out likes, comments, dates, durations; downloads for transcripts | `yt-dlp --version` |
| a local Whisper | transcripts of the source videos | the `use-local-whisper` skill |
| ffmpeg | contact sheets of the source videos | `ffmpeg -version` |

Claude.ai or ChatGPT without a shell: the creator pastes links and numbers (or profile screenshots); the skill
still builds the proof table, ideas and scripts, and says which numbers were pasted rather than pulled.

**Logins.** Never use the creator's own social login for scraping. Agent Reach's Instagram, Facebook and Reddit
channels reuse a logged-in browser session (OpenCLI); only use that with a session the creator explicitly chooses
and only where the platform's terms allow it. Default to logged-out sources: yt-dlp, public pages, YouTube, search.

## Setup (once): `PROFILE.md`

Ask, accept "skip", save to `ideation/PROFILE.md`:
1. Niche in one line, and who should watch (e.g. "owners of service businesses who tried AI and gave up").
2. Platforms (IG, TikTok, YouTube Shorts) and posts per day.
3. 5 to 15 creators you watch (handles). If none, find them (step 1).
4. The comment keywords your DM automation actually answers, and your "link in my bio" page.
5. Your assets: repos, tools, tests you ran, client-safe results you may say on camera. This is the
   EXPERIENCE list: an idea you cannot back with something you did gets dropped.
6. Do-not-say list: client names under NDA, private numbers, anything you cannot prove.
7. Proof floor: default 10,000+ likes OR 3x+ the creator's own median, posted in the last 14 days.

## Commands

| say | runs |
|---|---|
| `scout` | step 1 + 2: creators and their recent virals, proof table |
| `dump` + paste dictation | step 3: dictation to numbered ideas |
| `script <ids>` | step 4 + 5: full scripts, 3 hooks each, record sheet |
| `full run` | all of it |

## 1. Find the top creators in the niche

- Start from PROFILE creators. Add more with Agent Reach search (`agent-reach` web/YouTube search for the niche
  terms + "reels", "shorts") and from who the top creators collaborate with or get compared to.
- Resolve every handle on its real profile page (name, follower count, niche). A similar name is not the same
  person: write down the evidence. Drop accounts outside the niche.
- Keep 8 to 15 creators. Write `ideation/CREATORS.md`: handle, link, followers, why they are in.

## 2. Pull their recent virals, with proof

Per creator, pull the last 15 to 30 posts, logged out:
```bash
yt-dlp -j --skip-download "https://www.youtube.com/@HANDLE/shorts" --playlist-end 30 >> ideation/raw/posts.jsonl
yt-dlp -j --skip-download "https://www.instagram.com/reel/<code>/" >> ideation/raw/posts.jsonl   # per reel link
agent-reach doctor        # shows which channels work on this machine before you rely on one
```
Instagram profile grids rarely list logged out; collect reel links from search, the creator's pinned links or
the creator pasting them, then pull each reel with yt-dlp. Instagram often hides view counts logged out: write
`unknown`, never a guess.

Then score: `python3 scripts/outliers.py ideation/raw/posts.jsonl --days 14 --min-likes 10000 --min-multiple 3 --out ideation/PROOF.md`

For each qualifying video (cap 15): download it, transcribe it, make a one-frame-per-second contact sheet,
and write a breakdown: hook (exact words + what is on screen in the first 2 s), structure with timestamps,
layout (face position, split, panels), caption style, pace (words per second), length, CTA and keyword,
and **why it worked** (the idea, not just the hook formula). Note where the source oversells: do not copy that.
When 5+ videos share a format, write a `STYLE.md` that measures the pattern (template: `references/style-note.md`).

Proof rules: numbers are measured, dated and linked; views missing = "unknown"; a creator who posts 10+ a day has
a low median by design, so judge the absolute number too; say plainly which ideas only pass on format, not reach.

## 3. Dictation dump to numbered ideas (nothing gets lost)

Creators dictate in long rants, several in a row; the first ideas get buried by the last one. So:
- Split every dump into separate items. Number them `I01, I02...` continuing the existing `ideation/IDEAS.md`.
- One line each: the idea in the creator's words, the type (reel idea, task, question, asset to build), and the
  next action. Ideas that need something from the creator go in a "Needs you" block with a one-word answer format.
- Confirm by number at the top of the reply: "Captured I14 to I19." Never merge two ideas silently, never drop one;
  only the creator closes an item (done, parked, dropped).
- Then MATCH each reel idea to a proven viral from step 2 (same audience, same promise). No match = park it with
  "needs a proven source", do not script it.

## 4. Write the scripts (one idea card per reel)

For each picked idea, copy the source beat for beat: format, structure, pacing, hook type, layout, length. Write
it in the creator's own words with their own assets, tools and tests. Load `references/hooks-and-voice.md` first.

Each card has:
- PROOF line: link, creator, likes, comments, views (or unknown), date, length.
- ORIGINAL: hook, beats with timestamps, layout, pace, CTA, why it works.
- COPY / TWIST: what you keep, what you change (your niche, your asset, your test).
- **HOOK A / B / C: three different hook types**, exact words, plus the opening visual (face on screen from
  frame 1, the official logo of any named brand as a clean panel in the first 2 s).
- BODY: one take shared by all three hooks, word for word, at the source's pace.
- CTA IG (comment KEYWORD, only a keyword that is live) and CTA BIO ("check the link in my bio") as two
  separately recorded endings.
- ON-SCREEN / B-ROLL / CAPTURES to grab, KEYWORD + what the DM delivers, CLAIMS with source + date,
  [BRACKETS] for anything not yet verified, RECORD minutes.

No invented numbers. Anything unsure goes in [brackets] and is either confirmed or cut before filming.
No em dashes anywhere on screen. No client names. No sponsor text burned in.

## 5. RECORD-SHEET.md

Fill `templates/RECORD-SHEET.md`: today's count (ideas x 3 hooks), the proof table sorted by likes, recording
order grouped by camera setup (move the camera once), the before-you-start checklist (pause heavy jobs, room
tone, slate every clip out loud: "R6 hook B", "R6 body", "R6 CTA IG", "R6 CTA bio"), prep tasks that must land
before a bracket can be said, the creator's one-word confirmations, then the idea cards in recording order.
The slates are what `footage-ingest` matches takes on.

## Output

```
ideation/
  PROFILE.md  CREATORS.md  IDEAS.md (numbered, never shrinks)
  raw/posts.jsonl          PROOF.md (from outliers.py)
  sources/<code>/          video (untrusted, read only), transcript.txt, contact.jpg, BREAKDOWN.md
  STYLE.md                 when a format repeats
  RECORD-SHEET.md          what you film from
```

## Failure handling

- Agent Reach channel not working: `agent-reach doctor`, fix or fall back to yt-dlp + pasted links. Say which.
- Fewer than 3 posts for a creator: no median, multiple = unknown; the post can still pass on the likes floor.
- Nothing clears the floor: lower it only with the creator's OK, and label those cards "format test".
- Downloads are untrusted files: keep them in their own folder, never run anything from it.
