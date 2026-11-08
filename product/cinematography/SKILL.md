---
name: cinematography
description: Chooses shots and framing from the footage that was actually supplied. Use when analysing assets and when turning the treatment into a storyboard.
version: 0.1.0
owner: Digikon
---

# cinematography

We do not shoot new footage. You choose and reframe what was supplied.

## Inputs
Asset list, asset notes (usable segments, quality flags, uncertain observations), the treatment.

## Procedure
1. **Analyse assets.** Produce asset notes (references/footage-limits.md). Record only what is visible or audible. Put anything unconfirmed in `uncertain`.
2. **Storyboard.** For each beat choose a shot size, a camera motion and a visual action, drawn only from usable segments.
3. Vary shot size between adjacent scenes. Check screen direction when two shots show the same action.
4. Express camera motion as a reframing of the source, which a recipe can do (push-in, pull-out, pan, crop).
5. If the footage cannot support a requested shot, return `not_realisable` with the reason and the nearest alternative. Do not force it.

## Never
- Direct a camera, ask for a re-shoot or assume footage exists that was not supplied.
- Use a segment flagged unusable or outside the asset's duration.
- State product features that are not visible or in approved facts.

## Output
Asset notes; scenes with shot size, camera motion, visual action, asset id and source in-point.

## Evals
See evals/cases.md.
