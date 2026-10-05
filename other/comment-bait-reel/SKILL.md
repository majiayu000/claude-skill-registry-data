---
name: comment-bait-reel
description: >
  Build a "Comment X for the links" lead-magnet reel (9:16, ~14s) from the
  creator's OWN clips + REAL YouTube tutorial thumbnails. Proven format:
  [b-roll + "POV: you want X" caption] -> [black + "Watch this" + a real
  YouTube card] xN -> CTA "Comment KEYWORD / it's free". Single-ffmpeg-per-
  segment then concat. NVENC not needed (fast at this length). Pairs with a
  ManyChat/GHL keyword funnel that DMs the actual link list. Distilled from the
  SkynetLabs Claude link-drop reel (2026-06-09, critic-passed).
  Trigger: "comment bait reel", "/comment-bait-reel", "comment X for links reel",
  "link-drop reel", "lead magnet reel", "make a reel like this" + a reference
  showing the POV->Watch this->Comment format, or "watch this YouTube card reel".
---

# comment-bait-reel

A lead-magnet reel that converts a scroll into a **comment**, then a comment into
a **DM**. The on-screen video is only half the system — the other half is the
keyword funnel that delivers the promised links.

## The format (decoded from the viral reference)

```
[B-ROLL + POV caption]  →  [BLACK + "Watch this" + real YouTube card]   ×3
                                                                         ↓
                              [CTA: Comment "KEYWORD" / it's free]
```

- Each beat is **short**: b-roll ~1.6–1.8s, card ~2.0s, CTA ~3.3s. Total ~14s.
- B-roll = the **creator** (face/desk), graded, with a top dark bar + white
  "POV: you want X" caption. First b-roll is the **HOOK** — highest-stakes line,
  most cinematic frame. The hook frame decides reach; spend the most effort here.
- Card = pure black, big "Watch this", a **real** YouTube thumbnail framed white,
  real title + real channel name. NO invented stats (see hard rules).
- CTA = black, "Comment \"KEYWORD\"" + a punchy 2-word promise ("It's free") +
  one subline + a pulsing "comment below" nudge near the bottom.
- Cuts are **hard**, each segment opens with a 0.07s white flash (flash-cut) and
  cards get a slow zoom-in. That reads as "transitions" without fragile xfades.

## Inputs you need before building

1. **Creator clips** — 1–2 clean, caption-free vertical windows of the creator
   (a tight intense close-up = best hook; a talking-head or desk shot = body).
   Probe with `cropdetect` (see gotchas) to find caption-free seconds. Letter-
   boxed clips with burned captions: crop the clean video band and blur-fill.
2. **3 real YouTube tutorials** on the topic — get real `video_id`s (research
   agent). Thumbnail = `https://i.ytimg.com/vi/<id>/maxresdefault.jpg`
   (fallback `hqdefault.jpg`). VERIFY each id resolves and the thumb downloads
   (>3KB). Reject dead/private/tiny.
3. **Keyword + lead magnet** — the exact comment word (keep it the topic, e.g.
   CLAUDE) and what gets DM'd. Wire the DM via ManyChat keyword or GHL.

## Build

The engine is `assets/build.template.sh`. Copy it into a working dir next to the
source clips, edit the 3 b-roll blocks (clip path + `-ss`/`-t` + POV text), the
3 `make_card` lines (thumb + title + channel), and the CTA keyword. Then:

```bash
bash build.sh        # writes reel.mp4, regenerates everything idempotently
```

It builds 7 segments → concats with the concat demuxer (stream-copy, instant).
Output is **silent by design** — add trending platform audio at upload (boosts
reach + you avoid shipping unlicensed music).

## HARD RULES (learned the hard way)

- **No fake stats.** Do NOT put invented view counts / "X weeks ago" / durations
  on the cards. The videos are real but the numbers aren't — fabricating stats
  about real third-party channels is a no-fake-claims violation AND collapses
  credibility the moment a viewer clicks through. Card = real title + real
  channel name only. (This was the #1 critic ship-blocker.)
- **Hook is the whole ballgame.** A bright low-effort selfie as frame 1 = scrolled.
  Lead with the most cinematic/intense creator frame + a high-stakes caption
  ("POV: you're scared AI will replace you" > "POV: you want to learn X").
- **Keyword = the topic.** The comment word should match what's delivered
  (CLAUDE for Claude links). One unambiguous word.
- **Real thumbnails > designed cards.** Real recs look like genuine tips. Verify
  each thumbnail visually before building (Read the jpg).
- **Creator continuity.** Carry at least the first two b-roll beats with the
  actual creator, not a stranger/stock — continuity sells the "I'll send you MY
  list" promise.

## ffmpeg gotchas on Windows (gyan build)

- **Font path colon breaks the filtergraph.** `C\:/Windows/Fonts/...` does NOT
  escape on this build, and fontconfig has no default config. FIX: copy the TTFs
  to a **relative, colon-free** dir (`fonts/arialbd.ttf`) and reference that.
  `assets/fonts/` ships arial / arialbd / ariblk.
- **Colons inside `text=` break parsing even when single-quoted.** "POV:" / clock
  values die. FIX: escape the colon as `\:` inside the text value.
- **`zoompan` `d` is frames-PER-input-frame.** Feeding a looped image with `-t 2`
  (=60 input frames) × `d=60` = 3600 frames = a 2-MINUTE clip. FIX: feed ONE
  frame (`-loop 1 ... -frames:v 60`) and let `d=60` generate the 2s.
- **concat demuxer paths are relative to the list file.** If `list.txt` lives in
  `segments/`, entries must be `s1.mp4`, NOT `segments/s1.mp4`.
- **Always pass `-y`** (engine bakes it into `$ENC` + does a clean `rm` first) or
  ffmpeg blocks on the overwrite prompt in non-interactive shells.
- Find the clean video band in a caption-burned letterboxed clip:
  `ffmpeg -i in.mp4 -vf cropdetect=20:2:0 -f null -` (run at default loglevel —
  `-v error` HIDES cropdetect output). Note: burned caption text counts as
  content, so the reported top edge includes the caption; the clean video is the
  lower sub-band — eyeball a frame to split them, then blur-fill the band.

## Ship checklist

1. Build → extract a frame per beat → **Read them** (visual QA).
2. Independent critic pass (no self-grading): hook strength, card realism,
   caption legibility, CTA pull, topic coherence, no-fake-claims. Threshold 80.
3. Wire the keyword funnel (ManyChat/GHL) BEFORE posting — the DM must fire.
4. Post silent; add trending audio in-app. Pin a first comment with the keyword.

```

```
