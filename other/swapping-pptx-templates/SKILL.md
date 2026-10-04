---
name: swapping-pptx-templates
description: Use when re-rendering an existing .pptx deck's content into a different template/theme (PowerPoint, slides, brand swap, "use the template from X but content from Y"), especially with bilingual/CJK text or a template whose background is a baked-in image. For the underlying unpack/edit/pack mechanics, see the official pptx skill.
user-invocable: false
metadata:
  version: "1.0.0"
---

# Swapping PPTX Templates

## Overview

Moving a deck's *content* into a different template's *look*. PowerPoint has no
"reflow into another template" operation, so this is a slide-by-slide rebuild in raw
OOXML. This skill is the judgment layer on top of the mechanical workflow.

**REQUIRED BACKGROUND:** Use the official `pptx` skill (Anthropic document-skills plugin)
for the unpack → add_slide → edit → clean → pack mechanics and its scripts. This skill
covers the four things that skill does NOT warn about, each of which caused a real defect.

## The four non-obvious rules

### 1. Redesign, don't relocate
A "template" usually ships 3-5 generic layouts (title / banded-header / framed-card /
blank), not equivalents of the source's custom diagrams. Copy-pasting shapes drags the
*source's* colors and geometry into the new deck. Instead: extract each slide's content
(text, data, image refs) and rebuild the visual from scratch in the template's palette,
using its layouts only as background/chrome. Match content type to the closest layout;
layer plain text boxes + shapes on top for anything beyond title+body.

### 2. Never hand-type CJK (or any non-ASCII) as numeric XML entities
Deriving `&#20303;...` decimal codepoints from memory for Chinese/Japanese/Korean text is
the single highest-risk step. Each wrong codepoint decodes to a **valid but wrong**
character (圈→圭, 驗→鰓, 輪→載), so pack/validate never errors and the corruption is silent.

- Get ground truth: `python -m markitdown source.pptx > source_text.md`
- Insert CJK by **script substitution from that file** (`str.replace`), never by typing
  entities or characters into an edit by hand.
- Before packing, run the audit (path in Claude Code shown; elsewhere use the repo path):

```bash
AUDIT="$CLAUDE_PLUGIN_ROOT/skills/swapping-pptx-templates/scripts/audit_cjk.py"
python "$AUDIT" source_text.md <build_dir>   # exit 1 = suspicious chars, stop and fix
```
It flags any CJK char in the build absent from the source (near-zero false positives).

### 3. Template backgrounds are hazard zones
A template's `p:bg` is often a rasterized `blipFill`, not theme colors — so it can contain
baked-in text (a tagline) and a logo that your content must avoid. Detect their bounds
programmatically, don't eyeball a thumbnail:

```python
from PIL import Image
im = Image.open("ppt/media/image1.PNG").convert("RGB")  # the bg blip
# scan for tagline/logo pixels vs the known flat bg color; get px bbox, then:
# EMU_per_px = slide_width_emu / image_width_px   # e.g. 12192000/1280 = 9525
```
Convert the bbox to EMU and treat it as a keep-clear rectangle for every slide on that bg.

### 4. Visual QA is an adversarial pass by fresh eyes
After packing: `soffice --headless --convert-to pdf out.pptx && pdftoppm -jpeg -r 150 out.pdf slide`.
Then dispatch a **subagent** (no authoring context) told to *find* problems — overlaps with
the bg watermark/logo, text overflow, low-contrast label/fill pairings, lopsided whitespace.
You will not catch these yourself; you've been staring at the coordinates. Fix and re-render
until a pass is clean.

## Red flags — STOP

- About to type a Chinese/Japanese/Korean character or `&#NNNN;` entity into an edit → don't; substitute from the markitdown extraction instead.
- Packing without having run `audit_cjk.py` → run it first.
- Placing content in the top-right or a bottom band without checking the bg image's logo/tagline bbox.
- Declaring done after only self-review of the rendered slides → dispatch the fresh-eyes QA subagent.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Copy-paste source shapes into template | Old palette/geometry bleeds in | Rebuild visuals in template's colors |
| Hand-typed CJK codepoints | Silent wrong characters | Script-substitute from markitdown; run audit |
| Assume `<Default Extension>` covers new image types | Pack drops images / corrupt file | Add `jpg`/`png` defaults to `[Content_Types].xml` when copying source media |
| Eyeballing clearance from a thumbnail | Text collides with baked-in logo/tagline | Pixel-detect bbox → EMU keep-clear zone |
| Self-review only | Overlaps/whitespace shipped | Fresh-eyes subagent QA loop |
