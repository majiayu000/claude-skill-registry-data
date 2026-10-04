---
name: scbe-manhwa-anchor-sheets
description: Build and maintain canon-locked character anchor sheets, expression packs, costume and prop locks, and environment swatch sheets for The Six Tongues Protocol and related SCBE webtoon/manhwa production. Use when preparing Senna, Bram, Alexander, or other cast for image generation, beat-expansion packets, reference atlas work, LoRA prep, or any render pass where character and environment continuity must be locked before prompts are scaled.
---

# SCBE Manhwa Anchor Sheets

Use this skill to lock visual canon before batch renders, chapter packet expansion, or style-system upgrades.

Do not let a lucky render become the source of truth. Make the sheet first, then generate from the sheet.

## Read Order

1. Read `references/anchor-sheet-spec.md`.
2. Read `references/six-tongues-foundation-cast.md` when working on current Six Tongues anchor packs.
3. Read only the specific manuscript chapter, episode packet, or act script needed to confirm new canon details.

## Core Rule

Lock canon at the sheet level, not by freezing every panel.

- `Arc Locks` stay stable: silhouette, posture logic, face read, core costume anchors, tools, companion creatures, palette logic, and environment identity.
- `Panel Flex` stays deliberate: expression exaggeration, chibi compression, painterly emphasis, memory haze, or impact simplification.
- Never rewrite canon because one model drifted into a better-looking but wrong version.

## Workflow

1. Resolve the scope.
- Name the active characters, arc, episode range, and target output.
- Default current pack: Senna, Bram, Alexander, plus `2-4` environment swatch sheets.

2. Build one character anchor sheet per character.
- Follow the exact required fields in `references/anchor-sheet-spec.md`.
- Separate immutable anchors from optional render flourishes.
- Record what absolutely must survive bridge panels, hero panels, and recap compression.

3. Build the environment swatch sheets.
- Create only the environments that control continuity for the active run.
- Lock palette, materials, lighting, geometry, weather or atmosphere, recurring props, and rule-bearing UI or magic overlays.
- Tie each environment to the characters and beats it supports.

4. Connect the sheets to the render lane.
- Use the same character and environment names in prompt packets, storyboards, and review notes.
- Mark hero-panel environments separately from bridge-panel environments.
- Call out which details belong in every prompt versus only in key panels.

5. Update only on canon change.
- Revise a sheet when the manuscript, approved storyboard, or canon note changes.
- Do not revise a sheet just because a generation lane improvised something attractive.

## Output Contract

Leave behind a compact packet that another lane can use without rediscovery:

- one character anchor sheet per named character
- one environment swatch sheet per required location
- a short cast and environment matrix for the active arc
- unresolved canon questions that still need source confirmation

Use Markdown unless the target pipeline explicitly needs JSON.

## Current Production Default

For the present Six Tongues webtoon lane, build these first:

1. Senna anchor sheet
2. Bram anchor sheet
3. Alexander anchor sheet
4. Archive continuity environment swatch
5. Maintenance war room or lower-vault swatch
6. Floating Shelves storm-platform swatch
7. World Tree memory-garden swatch if the episode uses family-history beats

## Quality Gate

Before approving a sheet, verify:

- the face read matches the manuscript mood, not just a generic fantasy archetype
- the posture and tool logic match the role
- the companion or prop logic is present where canon requires it
- the palette can survive both detailed panels and compressed recap usage
- each environment reads as a place with operational rules, not wallpaper
- every allowed style shift has a narrative reason

## References

- `references/anchor-sheet-spec.md`
- `references/six-tongues-foundation-cast.md`
