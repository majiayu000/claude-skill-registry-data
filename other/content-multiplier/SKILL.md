---
name: content-multiplier
description: "Turns one published long-form video or podcast transcript into up to thirty pieces: 10 clips with new hooks and exact timestamps, 8 X posts, 4 LinkedIn posts, 3 carousels, 2 threads, a newsletter, a community post and a blog post, laid out on a two-week plan, all built only from what was said. In Claude Code it also cuts, reframes and captions the clips with ffmpeg. Use when someone wants to repurpose a long video, find clips, or write social posts from a transcript. Never posts or schedules."
---

# Content Multiplier

Five agents pull every usable moment out of a video the creator already made. Everything comes from what was said. The creator reviews and posts.

## Where it runs

- **Claude.ai:** paste the transcript (timestamped; word level if possible). All five agents run; the Clip Cutter outputs in/out points and one SRT per clip instead of video files.
- **Claude Code:** same, plus the Clip Cutter cuts vertical captioned clips from the final video file with ffmpeg, whisper.cpp and OpenCV (see `agents/03-clip-cutter.md` for the tool check).
- **No social connectors.** It never posts, schedules or logs in anywhere. The plan is a table (and CSV) the creator loads into their own scheduler.
- **Getting a transcript:** YouTube Studio > Subtitles > download .srt or .vtt for your own video; podcast hosts usually export one; or in Claude Code run whisper.cpp on the file. It must be the transcript of the PUBLISHED edit, or clip timestamps will be wrong.

## Setup (`start`, two rounds, "skip" allowed)

1. What is the video about, and who is it for?
2. Which platforms do you post on, and how many posts per week on each?
3. One CTA per platform (comment a keyword, join the newsletter, book a call).
4. Start date and time zone for the plan.
5. 5 to 10 of your own posts that sound like you; words you never use.
6. Names, products and terms that must be spelled exactly (SPELLING).
7. Anything that must NOT be used (private details, a client, a misspoken line).

## Commands

| Command | Runs | Result |
|---|---|---|
| `start` | setup | PROFILE, SPELLING |
| `multiply` + transcript (and video path in Claude Code) | 1 to 5 in order | 30 pieces + plan |
| `moments` | 1 | MOMENTS |
| `clips` | 2 (needs MOMENTS) | CLIPS |
| `cut` | 3 | clips or cut list + SRTs |
| `write` | 4 | POSTS |
| `plan` | 5 | PLAN |

## The fixed mix of 30

10 clips, 8 X posts, 4 LinkedIn posts, 3 carousels, 2 threads, 1 newsletter, 1 community post, 1 blog post. If the material is not there for a piece, leave it out and say so. Never pad to reach 30.

## Agents

Read the agent file before running that step; its rules live only there.

1. `agents/01-moment-finder.md`: splits the transcript into one-idea moments with exact times; ranks how well each stands alone.
2. `agents/02-clip-picker.md`: picks up to 10 standalone clips, tightens in/out, writes a hook for the first 2 seconds.
3. `agents/03-clip-cutter.md`: cuts, reframes to 1080x1920 and captions each clip (Claude Code), or cut list + SRT (Claude.ai).
4. `agents/04-text-writer.md`: the 20 written pieces in the creator's voice.
5. `agents/05-planner.md`: 14-day calendar, one CTA per piece, overflow listed.

## Shared files (project notes in Claude.ai, `work/` in Claude Code)

- `PROFILE`, `SPELLING`
- `MOMENTS` (M1...), `CLIPS` (CL1 to CL10), `POSTS` (X1-X8, L1-L4, C1-C3, T1-T2, N1, CP1, B1), `PLAN`
- Claude Code only: `input/final.mp4`, `out/clip-NN-*.mp4`, `out/clip-NN.srt`, `out/CHECKS.md`

## Safety rules (every agent)

- Only what was said. Quotes word for word. A missing fact becomes `[ADD SOURCE: what is needed]`.
- Nothing from the do-not-use list, ever, even at a clip boundary.
- Timestamps in `HH:MM:SS.mmm`, snapped to word boundaries. Never cut mid-word.
- SPELLING applied to every caption and post. No em dashes; no emoji or hashtags unless the creator's samples use them.
- Never post, schedule or connect to a social account. Never upload a clip.

## End-of-run output

```
MULTIPLIED: "How I plan a week" (42 min)
Moments  31 found, 14 stand alone, 3 AVOID (private)
Clips    10 picked (24 to 58 s), 8 hook KEEP, 2 hook CARD
Cutter   10 clips in out/, 9 FACE crop, 1 CENTRE-CROP (screen share), all checks PASS
Posts    8 X, 4 LinkedIn, 3 carousels, 2 threads, N1, CP1, B1 written; 2 [ADD SOURCE] gaps
Left out none
Plan     Day 1 Mon: CL3 Reels/Shorts/TikTok + X2; N1 on Day 6; 2 pieces overflow to week 3
Nothing has been posted or scheduled. Review every clip and post before it goes out.
```
