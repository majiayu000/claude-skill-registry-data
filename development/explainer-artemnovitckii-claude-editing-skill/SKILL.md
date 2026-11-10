---
name: explainer
description: Edits a talking-head clip into an explainer reel. The speaker sits low in a rounded panel on a light backdrop with their head breaking out over its top edge, and the top of the frame explains the point with visuals (a before-to-after comparison with an arrow, or a numbered list). White captions set the key words in a serif. Use when the user runs /explainer or asks for "me at the bottom, visuals on top" on a 9:16 clip.
---

# /explainer

```
┌──────────────────────┐
│   Steal what works   │  title, one word in serif italic
│ [before] ⟶ [after]   │  compare: card, drawn arrow, reveal  (or a numbered list)
│      ╭──head──╮      │  the head breaks out over the panel
│ ╭────┴────────┴────╮ │
│ │  speaker, captions│ │  rounded panel, eye line = its top edge
│ ╰──────────────────╯ │
└──────────────────────┘
```

## First use
This skill's folder is the "Base directory" Claude Code shows when it loads it. Resolve the kit from it (works through symlinks), and set up once:
```bash
SKILL_DIR="<base directory of this skill>"   # the path Claude Code printed as "Base directory for this skill"
KIT=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","..","kit")))' "$SKILL_DIR")
PY="$KIT/.venv/bin/python"; [ -x "$PY" ] || bash "$KIT/setup.sh" --cutout
```
`GROQ_API_KEY` must be set to transcribe (free at console.groq.com). Needs ffmpeg and Node.

## Steps
1. **Clip.** Use the 9:16 clip the user gave (any size; it is cropped to 1080x1920). Ask for it only if none was given.
2. **Words.** `"$PY" "$KIT/reel.py" words <video>` prints every word with its time (it transcribes on first use). It prints one sentence per line with `[ends …]`, the time its last word ends. Pick one stretch of 3 to 8 seconds that makes ONE point, made of whole sentences: `start` is the first word's time and `end` is the last sentence's `[ends …]` (source seconds).
3. **Eye line.** `"$PY" "$KIT/reel.py" frame <video> <a time in the stretch> frame.jpg`, then look at the image. The red ruler is in 1080x1920 pixels; read the y of the eyes. That is `eye_y` (about 700 to 800 for a normal framing).
4. **Spec.** Write `<clip name>.explainer.json` next to the clip (fields below). Paths in a spec are relative to the spec file. Every time is either seconds from `start` or a spoken word to anchor on (`"viral"`, `"viral#2"` for its second time, `"viral+0.2"`). Prefer words: they stay right when you move `start`.
5. **Build.** `"$PY" "$SKILL_DIR/build.py" <spec.json>`. It cuts the stretch, cuts the speaker out (about 0.1 s per frame), renders with HyperFrames and writes `<out>.sheet.jpg`.
6. **Check.** Look at the sheet. Red is what Instagram covers. Fix the spec and rebuild if:
   - the title or visuals sit in the red
   - a caption covers the mouth, or sits within 80 px of the red bottom zone (move `caption_top`)
   - a caption shows a word from outside the stretch (move `start` or `end` to the sentence edges)
   - the head doesn't break out over the panel (move `eye_y`)
   - an image is missing or squashed
7. **Hand over** the mp4 path and say in one line what each visual shows.

## Spec
```json
{
  "video": "my-clip.mp4", "start": 21.4, "end": 25.66, "out": "my-clip.explainer.mp4",
  "title": "Steal what *works*",
  "eye_y": 750,
  "visual": {
    "type": "compare",
    "left":  {"label": "Another niche", "images": ["theirs-1.jpg", "theirs-2.jpg", "theirs-3.jpg"], "at": 0.3,
              "chip": "14× viral", "chip_at": "viral", "swipe_at": ["carousel", 2.3]},
    "right": {"label": "Your niche", "at": "outside", "reveal_at": "recreate",
              "image": "my-photo.jpg", "text": "the best *ai tools*\nto use when\nyou're *young and broke*"},
    "arrow_at": "and"
  },
  "keys": ["viral", "outside", "recreate"],
  "caption_top": 1420
}
```
- `title`: 1 to 4 words. Wrap ONE word in `*...*` for the serif accent.
- `visual.type: "compare"` is a before and after:
  - The left card shows 1 to 3 images and swipes between them at `swipe_at`.
  - The right card starts as a dashed "?". The arrow draws at `arrow_at`, then the card reveals at `reveal_at`.
  - The right card is either a plain `image`, or a carousel cover made from `image` plus `text` (`*word*` turns yellow, `\n` breaks the line).
- Either card can be a **text card** instead of images: `"big": "*Pro*\ntools", "small": "what pros use"`. Use it when the user has no images. It is the right choice for a left/right comparison the speaker points at.
- `visual.type: "list"`: `{"type": "list", "items": [{"text": "Find a *viral* post", "at": "find"}, ...]}`. Up to 4 numbered rows, each landing as it is said.
- `keys`: caption words to set in the serif. Pick 2 to 4 that carry the meaning. Every time the word is said, it is set in the serif.
- `caption_top`: the y of the top of the captions, 1420 by default. Keep it under the mouth, and its bottom (`caption_top` + 80) above 1500.

## Taste
- One point per clip. If the stretch makes two points, make two explainers.
- Land each visual on the word that names it. Nothing should appear before it is said. The title is the exception: it is there from the first frame.
- Keep the top visuals between y 330 and 760 (the title sits above them, at about 210). Text and graphics stay out of the top 220 px, the bottom 420 px and 100 px at each side. The speaker's panel may run into them.
- If the speaker points left and right, use `compare`. Its cards sit where they point.
- Use the user's own images. Never invent numbers or results about someone else's post. A chip like "14× viral" must be something the user said or gave you.
