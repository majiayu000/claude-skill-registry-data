---
name: thumbnail-generator
description: "Make a 1280x720 YouTube thumbnail (or a banner/cover) that reads at phone size: a text-free background plate (generated or from a real frame), a real cutout of the person, 1 to 3 words in tight colour blocks, an official logo, composed by a script that checks overlaps and frame edges and renders the 320px and 168px views you must look at. Use when asked for a thumbnail, cover, banner, 'make this clickable', or to fix a thumbnail that looks cluttered or small."
author: Johann (@johannships)
version: 2.0.0
---

# Thumbnail generator

The method: **image models make the plate, code makes the words.** Generated
text comes out misspelled and generated faces come out as somebody else, so
text, logos and the person's real face are composited by
`scripts/compose_thumbnail.py`, which then checks the layout.

Sibling skills: `longform-edit` and `edit-style` produce the video and its
frames; this skill turns a frame into the cover.

## Requirements

- Python 3.9+ with Pillow (`pip install pillow`). Required.
- Cutouts: `pip install "rembg[cli]"` then `rembg i photo.jpg cutout.png`, or any background remover that outputs a transparent PNG.
- Plates (optional): any image model you have access to (an image-generation
  tool in your agent, an image API with an edit endpoint, or none: a blurred,
  darkened real frame is a fine plate).
- Claude.ai works for planning and prompts; composing needs Claude Code (a shell).

## Inputs

- The video's title and its one-sentence promise.
- A real photo or video frame of the person, ideally 1500 px tall or more,
  with the emotion the video needs (pick the frame; do not invent the face).
- Official logos for any named tool (brand press page or the site's own SVG).
- Optional: a reference thumbnail the user wants matched. Find and study that
  exact image first (see `references/reference-matching.md`).

## Steps

1. **Concept in one line**: what the viewer sees + the 1 to 3 words. If it
   needs more than 3 words, the concept is wrong. Show the result, hide the how.
2. **Make the plate** (1280x720 or larger, 16:9). Prompt rules for any model:
   - "no people, no faces, no text, no letters, no logos" (always)
   - topic-relevant scene that tells the story, not "dark room with screens"
   - high contrast, one dominant colour, empty space where the text goes
   - avoid the default blue/purple AI gradient look
   Alternative: a real frame from the video, `gblur` + darkened 20 to 40%.
3. **Cut out the person** from the chosen real frame (`rembg`). Never generate
   the person from text. If you use an image model to restyle the person, feed
   it the real frame as the input image and reject any result that changes the
   face, teeth, or clothes.
4. **Write `layout.json`** (format in the script's header). Starting values:
   cutout `height` 0.85 to 0.95 on one side, flush with the bottom; headline
   `size` 110 to 140; second line 60 to 80; logo `width` 180 to 260.
5. **Compose**: `python3 scripts/compose_thumbnail.py layout.json --out thumb.png`.
   Fix every FAIL (overlap, out of frame, cutout under 70% height, over 5 words).
6. **Look at `thumb.preview.png`**, the 168 px view first. Run the checklist
   below. Adjust the layout, not the plate: re-generate only when the concept changes.
7. **Optional single polish pass**: if your image model has an edit mode, run
   the FINISHED composite through it once at low strength (0.3 to 0.5) for
   lighting and saturation. Then re-check that every word is still spelled
   right and the face is still the same person. If not, ship the un-polished one.

## Rules (from rejected thumbnails)

- **Hierarchy: face > headline > logo > background.**
- **Everything is too small.** Make elements 30 to 50% bigger than feels right; most people see 168 px wide.
- **Text in solid colour blocks, padding that hugs the letters** (about 8 px
  at 1280 wide), drop shadow. Yellow = attention, green = positive, red =
  danger (white text), white = neutral. Heavy condensed sans (Impact, Bebas Neue).
- Nothing covers the face. Text never crosses the face.
- One plate fills the frame edge to edge: no voids, no visible seams.
- Duplicated or mirrored elements look cheap: each repeated element is its own image.
- Each new thumbnail looks different from the channel's last few.
- Do not upscale a cutout more than about 1.15x (the script warns): find a bigger source.
- Logos: official, unaltered colours and proportions, never AI-redrawn.

## QA checklist (write the answers in your reply)

- [ ] 168 px view: can you read every word and recognise the face?
- [ ] 1 to 3 words (5 max), spelled right
- [ ] face fully visible, not cropped at the chin or forehead, no UI badges from the source frame
- [ ] no overlaps, nothing cut at the frame edge (script PASS)
- [ ] high contrast, one clear focal point, no clutter
- [ ] would you click it next to the channel's other thumbnails?

## Output

```
thumb.png            1280x720 final
thumb.preview.png    full size + 320 px + 168 px side by side
layout.json          so the next tweak is a re-run, not a redo
```

Example reply:

```
thumb.png PASS (compose checks). 168px: "IT'S FREE" readable, face clear.
Concept: shocked face + "IT'S FREE" + tool logo; plate = blurred frame at 03:12, darkened 30%.
Kept all versions in thumbs/v1..v3.
```

## Failure handling

| problem | do |
|---|---|
| no image model | use a blurred, darkened real frame as the plate |
| no good real photo of the person | ask for one; never generate a stand-in face |
| model put text or faces in the plate | regenerate with the "no text, no people" line first in the prompt, or crop that area out |
| cutout has halos or missing hair | try `rembg -m isnet-general-use`, or pick a frame with a plainer background |
| font missing (tiny or fallback text) | set `"font"` in layout.json to a real bold .ttf |

Keep every version until the user picks one. Depth:
`references/composition.md` (sizes, text, layer order) and
`references/reference-matching.md` (matching a reference image, banners, square ads).
