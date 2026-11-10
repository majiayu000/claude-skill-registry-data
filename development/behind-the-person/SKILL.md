---
name: behind-the-person
description: Edits a talking-head clip so the graphics sit BEHIND the speaker. The speaker is cut out and stays in front of a panel (a grid of posts, a bar chart or a screenshot), big words land on the chest as they are said, and a profile card counts a number up. Use when the user runs /behind-the-person or asks for "visuals behind me", "graphs behind the person" or a professional depth effect on a 9:16 clip.
---

# /behind-the-person

```
┌──────────────────────┐
│ ╭──────────────────╮ │
│ │ grid / chart /   │ │  the panel, BEHIND the head
│ │ screenshot  head │ │
│ ╰──────── ( ) ─────╯ │
│        10,000        │  big chest words, one beat at a time
│  (o) Name  +10,000 [Follow] │  profile card, counts up, button flips
└──────────────────────┘
```

## First use
This skill's folder is the "Base directory" Claude Code shows when it loads it.
```bash
SKILL_DIR="<base directory of this skill>"   # the path Claude Code printed as "Base directory for this skill"
KIT=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","..","kit")))' "$SKILL_DIR")
PY="$KIT/.venv/bin/python"; [ -x "$PY" ] || bash "$KIT/setup.sh" --cutout
```
`GROQ_API_KEY` must be set to transcribe. Needs ffmpeg and Node.

## Steps
1. **Clip.** The user's 9:16 talking head. The cutout works best on one person, waist up, on a plain background.
2. **Words.** Run `"$PY" "$KIT/reel.py" words <video>`. It prints one sentence per line with `[ends …]` (when its last word ends). Pick a 3 to 6 second stretch of whole sentences with a concrete claim: `start` is the first word's time and `end` is the `[ends …]` time. A claim that holds a number works best ("this post alone got me over 10,000 followers").
3. **Framing.** Run `"$PY" "$KIT/reel.py" frame <video> <t> frame.jpg` and look at it.
   - The panel spans y 150 to 1020 by default. The head should cover its lower middle.
   - The chest words sit at `chest_top` (1105) and the card at `card_top` (1235). Both should land on the torso, under the chin.
4. **Spec.** Write `<clip>.behind-the-person.json` (below). Paths in a spec are relative to the spec file. Times are seconds from `start`, or spoken words (`"followers"`, `"this#2"`, `"over+0.2"`).
5. **Build.** Run `"$PY" "$SKILL_DIR/build.py" <spec.json>`. The cutout takes about 0.1 s per frame.
6. **Check.** Look at `<out>.sheet.jpg`:
   - The chest words don't cover the mouth.
   - The panel reads around the head.
   - The card is fully visible.
   - Nothing sits in the red zones.
7. **Hand over** the mp4 path.

## Spec
```json
{
  "video": "my-clip.mp4", "start": 9.4, "end": 13.1,
  "panel": {
    "type": "grid", "images": "my-posts/*.jpg", "tabs": ["Posts", "Reels", "Tagged"],
    "highlight": {"index": 0, "at": "this", "slides": ["post-2.jpg", "post-3.jpg"], "swipe_at": ["carousel", "alone+0.2"],
                  "label": "10K+ followers", "label_at": "10,000"}
  },
  "chest": [
    {"text": "for example", "at": 0.24}, {"text": "this carousel", "at": "this"}, {"text": "alone", "at": "alone"},
    {"text": "got me over", "at": "got"}, {"text": "{count}", "at": "10,000"}, {"text": "followers", "at": "followers"}
  ],
  "card": {"avatar": "me.jpg", "name": "Your Name", "label": "new followers", "count": "10,000", "at": "got",
           "count_at": "10,000", "button": "Follow", "pressed": "Following", "press_at": "followers"}
}
```
The panel takes one of three `type`s:
- **`grid`**: an Instagram-style profile grid with 12 cells, filled with your images on repeat, that scrolls slowly. `highlight` outlines one cell, swipes through its `slides` and pops a `label` chip.
- **`bars`**: `{"type": "bars", "title": "Views per post", "bars": [{"label": "Reels", "value": 12000, "show": "12K"}, ...], "highlight": 2, "at": 0.3}`. The bars grow in turn. Put the bar that matters at the side, because the middle sits behind the head.
- **`image`**: `{"type": "image", "src": "screenshot.png", "scroll": 200}`, a screenshot that pans upward.

The other fields:
- **`chest`**: the big words, each shown from its `at` until the next one. `{count}` counts up to `card.count` (`"10,000"`, `"4:12"` or `"250"`).
- **`card`**: optional. It counts up with the chest and the button flips at `press_at`.

## Taste
- Chest words are 1 to 3 words: the beat, not the sentence. Land each one on its word.
- The panel's content must be real: the user's own posts, analytics or screenshots. Never invent their numbers. The count must be one they said.
- Keep it calm. One panel, one highlight and one card is enough. The motion comes from the speaker standing in front of it.
