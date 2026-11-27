---
name: garment-fit
description: "Use when fitting, refitting or moving a garment onto a body base: sleeves, shrinkwrap, follow keys, clearance. Adds the rules that clipping and false-clip sheets taught."
---

# Garment fit

The pipeline (fit once per base, follow keys, hide mask, dress script, the Done report numbers) is
`claude-setup/docs/clothing-pipeline.md`; this skill adds only what it lacks. Run by the Character TD
(`claude-setup/.claude/skills/operator/roles/character-td.md`), also as step 5 of [`asset-intake`](../asset-intake/SKILL.md).

## The loop (GameDev 2026-11-15)

- **Proven route, not tinkering.** The route is the passed garment recipe of the project's proven list, quoted in the pre-gate file. A material change (alpha, emission, offsets in mm) does not fix skin showing through; if the piece shows skin, the geometry or the fit is wrong.
- **Self-loop:** change, render front, back, left, right and close-ups, score yourself against the table below, change again, without closing or reporting each step. Call a fresh gate only at a self-score of 4.8 or more with every hard check green, and hand it all of these views with the pre-gate file, not one front and one back image.

## Before the fit

- **Search first:** library, catalog, `clothes_dupe.py`; refit a gate-passed piece before building one (`docs/clothing-pipeline.md`, Reuse first).
- **Rebind sleeves to the arm pose before Shrinkwrap.** A sleeve fitted on a rest or T-pose arm clips the moment the arm is down. Pose the arm
  to the pose the garment is worn in, bind the sleeve to that pose's weights, then Shrinkwrap, then return to rest. Check the sleeve axis
  (centre line of the sleeve against the arm bone) in the pose and at rest.
- **Sheets bind what `dress.py` binds.** A fit or sheet script uses the same `FIT_SW` shrinkwrap setup as `dress.py`; another setup shows
  clips that the dressed character does not have, and hides ones it does. One definition, imported, never copied.
- A hidden object is not evaluated: unhide what you measure (`docs/clothing-pipeline.md`, Lessons).

## Criteria (all in 4 views against the MAIN reference, front, side, back, three-quarter)

| Check | Pass |
|---|---|
| Sleeve axis | sleeve centre line within the arm bone's line at rest and in the pose; cuff ends where the reference ends |
| Shoulder | seam on the shoulder, no pull or bridge across the collar bone |
| Bust | cup shape follows the body key at 0 and 1, no gap above, no pinch under |
| Hem | length and line as in the reference, no clipping at sit or bend |
| Foot | sole or hem clears the floor and the shoe, no poke-through at heel |
| Silhouette | outline in each view within the reference outline (the gate's silhouette row, `gate.md`) |
| Clearance | per piece: smallest mm and share of vertices below 0 at rest, in the big pose and at each key's extreme (`scripts/blender/clearance.py`, `faces`); 0 mm or more, 0 % inside |

Run it on **every base**: `pipeline-gates.mjs fit` needs a state per `BT_` preset and a `char_<name>` per `CH_` key, and the measuring run
runs without the `save` argument, so the character file is never written. The report lists the numbers per piece and the 4-view sheet per base; a view that was not looked at is "not checked".
