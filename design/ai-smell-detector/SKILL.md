---
name: ai-smell-detector
description: Use to audit a generated or heavily templated interface for generic AI aesthetics, unjustified trend patterns, component-registry residue, vague copy, repetitive motion, novelty theater, or visual decisions that lack brand/UX rationale.
metadata:
  short-description: Detect generic AI design patterns and visual slop
---

# AI Smell Detector

## Detect patterns, not forbidden shapes

The following are smells when repeated without a project-specific reason:
- centered hero + generic eyebrow + two CTAs;
- arbitrary bento/three-card feature grids;
- gradient text and blue/purple glow as default “premium” styling;
- glassmorphism with no material concept;
- excessive pills/badges;
- identical corner radius on every surface;
- icon + heading + paragraph card repetition;
- every section using the same fade-up reveal;
- oversized vague claims with no evidence;
- stock imagery with inconsistent lighting/crop;
- generic font pairing with no typographic character;
- floating decorative objects with no composition role;
- 3D cursor/particles/parallax that communicate nothing.

## Test each suspicious decision

Ask:
1. What user/brand/content purpose does this serve?
2. Would the design lose meaning if it were removed?
3. Is this repeated because of a system or because it was an easy default?
4. Does the choice appear in the references as a principle or as a copied fashion cue?
5. Is there a more specific expression of the same intent?

## Output

Classify each smell as: `keep`, `adapt`, `replace`, or `remove`, with the reason. Avoid redesigning merely to be unusual.
