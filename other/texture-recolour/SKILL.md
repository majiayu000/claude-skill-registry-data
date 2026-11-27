---
name: texture-recolour
description: "Use when changing the colour of a garment, hair or skin texture: hue shift on an ID mask or keep the original. Never multiply a black and white texture."
---

# Texture recolour

yskills 2026-11-12: a flat recolour of a black and white shirt texture (multiply) killed shirt and tie under pullovers. Run by the Character TD
(`claude-setup/.claude/skills/operator/roles/character-td.md`), also after step 4 of [`asset-intake`](../asset-intake/SKILL.md).

## Rule

1. **Keep the original** when the download's colour already fits the cast sheet palette. A recolour needs a reason in the plan.
2. **Otherwise shift the hue on a mask**, not the whole texture: Hue/Saturation node (or the texture painted in HSV) with the part's
   ID mask as the factor, so skin, white shirt and tie, buttons and metal keep their colour.
   Tool: `scripts/recolour.py` (numpy and Pillow): `--list` prints the UV islands of an exported `.obj`, `--islands 0,2 --hue 120 --out <dir>` shifts the hue
   only inside those islands, keeps value and alpha, writes `before_after.png` and exits 1 if one byte of the saved file outside the mask differs from the source. `--grow` (default 1) widens the mask by pixels so seam texels are covered. Feathered island edges are not covered: add them with a test if a seam shows. Tests: `scripts/test_recolour.py`, run in CI.
3. **Never multiply** a black and white or greyscale texture with a colour: black stays black, white takes the whole tint, details die.
   A recolour that has to start from grey uses a colour ramp on the mask or a Color blend at low strength, then check it per step 5.
4. **Where the mask comes from:** the material slots or UV islands of the garment first (one slot per part is the usual case); only if
   neither separates the parts the TD paints an ID mask once, saved beside the texture as `<name>_id.png`, and the catalog entry names it.
   Patterns stay on UVs or object coordinates, never "Generated" (`docs/clothing-pipeline.md`, Lessons).
5. **Check before and after per base:** one render per body key set in `asset-intake` step 6, original left and recolour right, under the
   layers it is worn with (pullover over shirt and tie). A part that lost detail or contrast is reverted at once, not patched.
6. The source texture is never overwritten; the recolour is a new file in `files/` and the node setup is saved in the asset.
