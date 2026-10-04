---
name: i18n-subtitle
version: 1.0.0
description: Create subtitles or captions with correct timing, line breaks, and reading-speed limits.
author: matrixx0070
tags: [subtitles, captions, timing, srt]
capabilities: []
---

## When to use

Use this when producing subtitles or captions from a transcript or translation — turning dialogue into time-coded cues that stay on screen long enough to read and never overflow the frame. Applies to translated subtitles, same-language captions (SDH), and accessibility captions with sound cues.

**Not for:** untimed prose translation (use `i18n-translate`), locale formatting of documents (use `i18n-localize`), glossaries (use `i18n-glossary`), or tone-only passes (use `i18n-tone-adapt`).

## Method

1. Segment by sense, not by sentence length. Break at natural pauses/clauses so each cue is a readable unit.
2. Enforce reading speed. Target ≤17 chars/sec for adults (≤12 for children). Decision point: if text exceeds the limit for its duration, condense the wording rather than shorten the display time below ~1s.
3. Limit layout: max 2 lines per cue, ~42 characters per line. Balance line lengths; break before conjunctions/prepositions, never mid-word or mid-name.
4. Set timing: minimum ~1s, maximum ~7s on screen; leave ≥2 frames (~83ms) gap between consecutive cues; sync in-points to speech onset.
5. Decision point: for captions (SDH), add speaker labels and bracketed sound cues `[door slams]`; for plain translation subtitles, omit them.
6. Validate: no overlaps, no negative durations, monotonically increasing timecodes, and every cue passes the CPS limit.

## Example

Line to caption: "I told you yesterday that the shipment would arrive on Monday morning." (~68 chars, spoken over 3.0s → ~23 CPS, too fast).

Split into two cues:

```
1
00:00:04,000 --> 00:00:06,000
I told you yesterday

2
00:00:06,100 --> 00:00:08,600
the shipment arrives Monday morning.
```

Each cue now sits under 17 CPS, 2-frame gap between them, condensed "would arrive on" → "arrives".

## Pitfalls

- **Reading speed too fast.** Cramming full sentences into short cues; viewers can't finish reading — condense instead.
- **Bad line breaks.** Splitting "New / York" or breaking after an article strands words and slows reading.
- **Overlapping or gapless timecodes.** Cues that collide or touch flicker; keep a minimum gap and no overlaps.
- **Under-minimum flashes.** Cues under ~1s register as a flash even if the text is short.

## Output format

SubRip (`.srt`): sequential index, `HH:MM:SS,mmm --> HH:MM:SS,mmm`, then 1–2 text lines, blank line between cues.

```
<n>
HH:MM:SS,mmm --> HH:MM:SS,mmm
<line 1 (≤42 chars)>
<line 2 optional (≤42 chars)>

```
