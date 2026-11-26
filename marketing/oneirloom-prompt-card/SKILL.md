---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-prompt-card
description: "Create a 3:4 vertical card from an existing image and complete prompt. Crop the image to fill the upper third, and typeset the prompt in the lower two thirds. Use for image-and-prompt collages, prompt cards, or Oneirloom prompt sharing layouts."
triggers:
  - oneirloom-prompt-card
  - oneirloom
  - prompt
  - card

---

# Image and prompt card

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available.

把已有成品图与完整提示词排成一张可分享卡片的渲染技能。本技能只渲染既有内容；写作新提示词仍归摄影与设计方法。

## When to use

Use this Oneirloom child skill when the user asks to combine an existing image and prompt into one shareable graphic. Recognize requests for a prompt card or an image paired with its prompt. This skill renders existing content; the photography and design methods remain responsible for writing new image prompts.

## Fixed layout

- The output is one 3:4 portrait PNG. Use a 1800 by 2400 logical canvas and render at 1.5 scale for a 2700 by 3600 PNG.
- The image region is the full-width upper third, from the top edge to exactly one third of the total height. Fill it with a proportional `object-fit: cover` crop. Crop the image to fit this region, retaining an identifiable focal point. For a mirror selfie, prioritize the face, camera and upper outfit when the wide crop cannot include the whole body.
- The prompt region is the full-width lower two thirds. Place any modest title and all text padding inside this region. Typeset the complete selected prompt here. Keep the region split fixed while fitting the text.
- Use a plain light text background, dark type and clear paragraph spacing. Keep decorative labels subordinate to the prompt. Preserve the source image's colors and geometry apart from the proportional crop and an explicitly requested watermark.

## Optional watermark and private brand identity

- The free public package renders an unbranded card by default. It contains no private Oneirloom mascot, logo, or standalone signature asset. Do not search for, recreate, or require those assets to render a card.
- Add a watermark only when the user authorizes its use and supplies an accessible local PNG. Pass that file explicitly with `--watermark`. Preserve the original bytes and aspect ratio. Supplying a private asset for a local card does not authorize publishing that asset or adding it to the public package.
- For an authorized local Oneirloom card, the approved identity is a woven creature behind overlapping white Chinese lettering "织梦师", with "Oneirloom Skill" beneath it and blue threads woven into the strokes. Both language lines and the long calligraphic flourishes have black outlines. Use the approved local PNG without redrawing it. Prefer this white-letter version on light and dark backgrounds. A black-letter version requires white outlines around its Chinese text, English caption, and flourishes. A gray-background preview is not a transparent watermark. Older text-only white or black versions remain explicit local choices only when the corresponding file is supplied.
- Set a supplied watermark to 20 percent of the card width, with 36 logical pixels at the top and right. A square PNG occupies 360 by 360 logical pixels, or 540 by 540 pixels with 54-pixel margins in the final export. Other aspect ratios retain their proportional height and must fit inside the image region.
- Use 90 percent opacity and no added shadow, panel, or border. Keep the complete overlay inside the image region. Inspect readability and subject overlap; report a conflict that the fixed placement cannot resolve. These placement defaults apply only when a watermark is supplied.

## Workflow

1. Select the latest confirmed image and prompt from the conversation. A new attachment replaces the previous picture for the card unless its role is explicitly different. When the user refers to a known template, use its current prompt rather than a superseded archive. Use the requested language; otherwise use the complete Chinese version for a Chinese conversation.
2. Inspect the image and choose the crop position. Read the actual prompt file. Preserve its wording, paragraph order and values, including any generation aspect ratio. Card composition does not authorize rewriting or shortening the prompt. An output image paired with a prompt does not establish which exact prompt or model generated it.
3. Render with [scripts/render_card.py](scripts/render_card.py) using local HTML, Playwright and an available Chromium browser. Omit `--watermark` for the default unbranded card. The renderer copies the original image and, when supplied, the exact watermark PNG into the output folder beside editable HTML and prompt text. Rendering requires Python Playwright and Pillow; use an installed browser executable when available.
4. Check the actual rendered geometry: 3:4 canvas, cropped upper image region exactly one third high, lower text region exactly two thirds high, every prompt paragraph inside that lower region, and rendered prompt text equal to the selected source. For a supplied watermark, verify its upper-right position, proportional size, margins, opacity and source hash. For an unbranded card, verify that no watermark is present. Fit the font within the text region; an inability to fit the complete text is a gap to report, not permission to shorten it or enlarge the image region.
5. Inspect the PNG for crop focus, legible text, paragraph order and clipping. Inspect any supplied watermark for readability and subject overlap. Fix the crop or text fitting within the fixed split when required. Deliver the PNG inline with a clickable file link. State material omissions or unverified outcomes only when present.

## Renderer

```powershell
python '<skill directory>/scripts/render_card.py' --image '<source image>' --prompt '<current prompt text file>' --output '<new output directory>' --title '<short title>' --image-y 6 --browser 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
```

`--image-y` sets vertical `object-position` as a percentage from 0 to 100. Choose it from the inspected image; 6 is the crop used for the current hotel-selfie case, not a universal portrait setting. Horizontal positioning stays centered. Omit `--browser` to use Playwright's installed Chromium. Output folders must be new so previous versions remain intact.

To add an authorized local PNG, append `--watermark '<user-supplied PNG>'`. Omitting the option performs no private-asset lookup.

The renderer saves `prompt-card-3x4.png`, `card.html`, `photo` with the original extension, `prompt.txt` and `render-checks.json`. It saves `watermark.png` only when a watermark is supplied, and the HTML then references that archived file. The checks record the actual geometry, source-image hash, prompt match and watermark presence. When present, watermark checks include placement and source hash. These checks do not prove visual quality until the PNG is inspected. Keep an output folder containing a private watermark local unless its publication has separate authorization.
