---
name: render-comic-page
description: Render one finished comic page from an approved page storyboard, character references, exact dialogue, and a visual-style contract. Use for one manga, webcomic, graphic-novel, or illustrated-story page and for targeted regeneration of one failed page; do not use for planning the whole story, character sheets, film storyboards, photo collages, or adding bubbles to an already accepted image.
---
# Render Comic Page

## Catalog

- Display name: Render Comic Page
- Categories: Comic
- Status: Ready
- Route label: GPT Image 2 reference-aware comic page
- Tone: purple
- Short description: Render one storyboarded comic page with character, style, panel, and dialogue continuity.
- Similar skills: develop-story, plan-comic-storyboard, plan-film-storyboard
## What this skill does

- Converts one approved page manifest into one intentional multi-panel comic page.
- Binds named characters to canonical reference images and carries observable continuity from adjacent pages.
- Keeps exact dialogue separate enough to repair typography without discarding accepted artwork.

## How to use

Provide one storyboard page, page ratio, reading direction, visual-style prompt, exact dialogue, canonical character references, and any previous-page continuity reference.

#### Example

```text
Render page 3 from this approved storyboard as a 3:4 Chinese webcomic page. Use the attached Lin and Momo sheets as canonical identity references, keep the red parcel in Lin's left hand, and render the three exact dialogue lines in reading order.
```

## Input and page contract

1. Accept exactly one page per invocation. Require its page number, panel count, ordered panel instructions, layout logic, ratio, reading direction, style, dialogue, and continuity locks.
2. Bind each character ID to one canonical reference asset. State which image owns face, hair, body, wardrobe, and palette. Never inherit an unrelated reference background, pose, action, or layout.
3. Use a previous accepted page only as a style, atmosphere, and state reference. Never copy its action or panel arrangement. If no previous page exists, use the project style contract and character sheets.
4. Compile the image Prompt with [page-prompt.md](references/page-prompt.md). Keep the requested panel count and reading order explicit. Assign every dialogue line to its speaker and target panel.

## Route and execution

Use `gpt-image` v1.0 / GPT Image 2 with every required reference in `images`, one `textDescription`, `quality: "medium"`, `imageSize: "2K"`, the requested supported `aspectRatio`, and `batchCount: 1`. Do not use Midjourney or Z-Image because page rendering is reference- and layout-sensitive.

Persist one stable `operationKey` for the page before submission, require a non-empty `executionId`, and poll that run to terminal state. Each page is an independent planned slot. A failed or unknown page never increases the planned page count and never causes accepted pages to regenerate.

Render different pages sequentially when the later page depends on the previous page's visible state or style. Independent page generation is allowed only when the storyboard and canonical references fully define continuity; do not parallelize merely for speed.

## Acceptance and repair

Check the returned page for panel count and order, character identity and wardrobe, required props and state, action legibility, style continuity, subject count, dialogue assignment, and readable exact copy. Do not reject intentional crops or stylized anatomy that match the approved style.

- Terminal provider failure: diagnose the returned error and make at most one new linked run with a materially revised request when retry is allowed.
- Visual continuity or layout failure: regenerate only this page with the failed property strengthened; never regenerate accepted neighbors.
- Missing, garbled, or long dialogue: preserve the accepted artwork. If the user permits compositing, render a text-free or cleared-bubble page and hand it to `$add-speech-bubble` with exact copy and tail targets instead of repeatedly redrawing the page.
- Unknown create outcome: reconcile the existing operation key; never submit a duplicate page.

Record page number, reference bindings, parameters, exact Prompt, operation key, execution ID, terminal state, acceptance failures, and any repair handoff.

## User-facing output

- Media type: One finished comic-page image plus execution receipt
- Default quantity: 1
- Content per image: One page containing the approved ordered panels and dialogue
- Default layout: Storyboard-defined page ratio and reading direction
- Model policy: GPT Image 2 Medium/2K with canonical character references
- Downstream use: Multipage comic assembly, targeted page revision, translation, or deterministic bubble repair
