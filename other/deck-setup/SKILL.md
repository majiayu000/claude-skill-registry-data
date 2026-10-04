---
name: deck-setup
description: Measures a team slide template into local deck assets — template-spec.md, template.js, and reference images. Canvas, type scale, colors, and the archetype catalog are read from actual nodes; anything the sample is too thin to settle is left empty rather than guessed. Run once before using /fig:deck in a new environment, or again after the template is revised. Triggers - "/fig:deck-setup", "extract the slide template", "set up the deck assets", "덱 템플릿 뽑아줘", "발표 템플릿 추출", "템플릿 다시 추출".
allowed-tools: Read, Write, Bash, AskUserQuestion, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__create_new_file, mcp__plugin_figma_figma__get_screenshot
---

# deck-setup — extracting a presentation template

`/fig:deck` uses the team template's coordinates, colours, and typography exactly as they are. Where those values come from is this skill. **It does not read a remote template on every run** — it reads local assets extracted here once.

**The premise**: never invent a value. Where an observation is ambiguous, leave it empty rather than fill it. An empty slot is read by `/fig:deck` as "that archetype does not exist", and it picks another. Mix up "not there" with "could not measure" and the deck quietly drifts away from the template.

**Prerequisites**: always load `figma:figma-use` and `figma:figma-use-slides` before calling `use_figma`. Step 2 (measure) is **zero writes** — the script only `return`s a report.

**Open with what this produces.** After this, `/fig:deck` builds slides from your own template's archetypes rather than a generic layout. Ten to fifteen minutes with the template to hand, and one thing is asked of you that MCP cannot do — applying the template. The template file itself is never touched. Name each step as it begins.

## When to invoke

- Using `/fig:deck` for the first time in a new environment, at a new company
- The team template has been revised and the values have moved
- The assets folder is missing, or `/fig:deck` has stopped with "no assets"

## When NOT to invoke

- Building the deck itself → `/fig:deck`
- Extracting design-file conventions → `/fig:setup` (a separate thing. This one is for Slides templates only)

## Configuration

`deck.assets_dir` is where the assets go. The default is `./deck-assets`; if several projects share one template, move it to `~/.claude/deck-assets`.

**The assets do not live inside the plugin.** Team template screenshots and background images carry company assets — a wordmark, an address — that must not ship in a distribution.

## 1. Reach the template

The source template file is usually outside MCP's reach. When it is, make a mirror.

1. Create an empty Slides file — `create_new_file`, editorType `slides`
2. **Ask the user to apply the team template from the Templates panel, and wait.** MCP cannot apply it
3. Applying it pulls in the sample slides wholesale. Those are the source for the catalog

Confirm it was applied before going on. Text still reading `Inter` or 'Pick a style' means it has not been.

## 2. Measure (read-only)

Measure every sample that came in. Read the values; do not eyeball them.

| What | How |
|---|---|
| Canvas | Width and height from a slide's `absoluteBoundingBox` |
| Margins | Min and max x of each slide's children — the mode is the left/right margin |
| Typography | The distribution of `fontSize`, `fontName`, `letterSpacing`, and `lineHeight` across every TEXT |
| Colour | The colour distribution across every `fills` and `strokes`. `getLocalPaintStyles` alongside |
| Text styles | `getLocalTextStylesAsync` — the named styles *are* the type scale |
| Archetypes | Per slide: name, child composition, title position, content top y |

Use the same criteria as `/fig:setup`. **Where the sample is thin or the values are split, do not fill it in.** A value becomes a convention only when it dominates 5 or more samples by more than 90%.

**Take the type scale from the named text styles.** The measured `fontSize` distribution has hand-tweaked exceptions mixed in, and a scale built from those is not a scale at all.

## 3. The archetype catalog

One slide is one archetype. For each, record:

    number · name · one line on what it is for
    title-position family (top / left title vertically centred / caption / no title)
    content top y · column count · column width · column gap
    slots (coordinates and size for title, subtitle, body, image, figure)

**Count the families and report them.** Four title positions and six distinct content-top y values is normal. A template is a menu, not a deck — a list of alternatives made to be chosen from. That count is the evidence the user picks fidelity from in step 3 of `/fig:deck`.

Where reference images help, screenshot each archetype into `template-assets/` named by number. It works without them, but they make the choosing accurate.

## 4. Write the assets

Create three things in `deck.assets_dir`. They are local files, so write them without a preview — but say so before overwriting anything already there.

**`template-spec.md`** — the human-readable spec.

```
canvas and grid    width · height · margin · column width · column gap
typography         family candidates · scale (size, weight, letter-spacing, line-height)
colour             name → hex. Only the ones that carry meaning
archetype catalog  all of them, in the 3-line form above
selection rules    content shape → archetype mapping
```

**`template.js`** — the constants and builders that attach to a build script. Written on the assumption that it is concatenated **after** `_common/scripts/deck-base.js`.

```js
const FAMS = ['<team font>', 'Inter'];        // in order of preference
const C = { bg: hx('#…'), text: hx('#…'), … };
const T = { title:{size:…,style:'Bold',ls:…,lh:…}, … };
const SW = …, SH = …, MARGIN = …, CELL_W = …, CELL_GAP = …;
// archetype builders — put the observed slot coordinates in as they are. Never invent new ones
function titleSlide({title, subtitle, bgImageHash}) { … }
```

Builders use `newSlide`, `addText`, `addRect`, `addImageRect`, and `addLine` from `deck-base.js`. Do not write element-creation code again — rules like `appendChild` ordering are baked into those.

**`template-assets/`** — images that cannot be reproduced with shapes, such as the cover and closing backgrounds. Where a wordmark or a mission statement is baked into the image, use the image itself rather than imitating it with shapes.

## 5. Verify

**Do not stop at writing the spec. Actually build one slide.**

1. Pick one archetype from the catalog and build a slide with the `template.js` builder
2. Compare coordinates, sizes, and colours against the original sample
3. A mismatch means the spec is wrong. Fix the spec, not the slide

Once one is right, build one per family — four families, four more slides. Title position is the family that goes wrong most often.

Report three things at the end.

- How many archetypes went into the catalog, and how many were **left empty for want of a measurement**
- How many title-position families there are, and how many distinct content-top y values
- Whether the team font exists in this environment — without it `/fig:deck` runs on a substitute and the letter-spacing changes
