---
name: plan-comic-storyboard
description: Turn a story idea, synopsis, or finished script into a production-ready comic storyboard manifest with a character bible, visual style, exact page count, panel beats, dialogue, and layout logic. Use before rendering a multipage comic or revising its narrative structure; do not use for generating final comic artwork, film shot lists, animation storyboards, or one standalone illustration.
---
# Plan Comic Storyboard

## Catalog

- Display name: Plan Comic Storyboard
- Text category: yes
- Categories: Text
- Status: Ready
- Route label: Agent-authored structured storyboard
- Tone: blue
- Short description: Convert a story into a validated page-by-page comic production manifest.

- Similar skills: develop-story, render-comic-page, plan-film-storyboard
## What this skill does

- Expands a thin premise only when requested, then preserves its characters, causal spine, tone, and ending.
- Extracts a concise visual character bible and one reusable English art-style description.
- Plans the exact requested number of pages with panel-level action, dialogue, composition, and continuity anchors.

## How to use

Provide the story or premise, page count, reading direction, page ratio, language, audience, style, and any fixed characters or ending.

#### Example

```text
Plan a six-page vertical Chinese comic from this premise: a night-shift courier discovers that every undelivered parcel contains a forgotten memory. Keep the ending bittersweet and use no more than four panels per page.
```

## Workflow

1. Separate fixed facts from gaps. Ask only when a missing answer would change the ending, audience rating, page count, reading direction, or required character.
2. If the input is only a premise and expansion is requested, write a compact story with setup, escalation, turn, climax, and resolution. Do not add unrelated subplots merely to fill pages.
3. Extract only recurring or plot-critical characters. Give each a stable identity block: name, role, species, apparent age, body and face anchors, hair, outfit construction, palette, signature feature, personality, and change restrictions.
4. Choose one English visual-style prompt describing medium, linework, color, lighting, background density, and mood. Do not imitate a living artist or copy protected characters.
5. Allocate one narrative beat per page before choosing panels. Use panel count to serve pacing; default to 1–4 panels per page unless the user asks otherwise.
6. Write each panel as an observable shot: participating character IDs, action, setting, shot size, camera angle, expression, continuity locks, exact dialogue or caption, and bubble speaker. Never replace visible action with literary summary.
7. Validate the manifest against [storyboard-schema.md](references/storyboard-schema.md). The pages array must equal the requested page count, page numbers must be contiguous, every character ID must exist, and every line of dialogue must have a speaker or be marked narration.
8. If structural validation fails, revise only the invalid fields. Do not silently change the requested page count, ending, language, or fixed characters.

This is a planning Atom. It does not submit a WeShop generation run. Hand its complete manifest to `$render-comic-page` one page at a time; create each missing canonical character sheet with `$create-character` first and bind the accepted sheet into page rendering. The optional seven-asset character expansion is not required for comic-page rendering unless the user confirms it after reviewing the sheet.

## User-facing output

- Media type: Structured comic storyboard manifest
- Default quantity: One manifest containing the requested pages
- Content per artifact: Project brief, style prompt, character bible, pages, panels, dialogue, layout, and continuity locks
- Default layout: Validated Markdown or JSON following the bundled schema
- Model policy: Agent-authored planning; no paid image generation
- Downstream use: Character reference creation and independent comic-page rendering
