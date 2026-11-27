---
name: blender-body
description: "Use for any 3D character body, rig or review work in Blender: picking a base, shape keys, posed tests, hand-in sheets, grading a body. Born from 13 failed Luna rounds and 15 Miss Galaxy rounds."
---

# Blender body: build and review a rigged character body

Why this exists: Luna's body took 13 rounds (lc1 to lc13, 2026-10-18) and ended with yskills
asking what had been learned. The rounds stacked edits on a mesh nobody
owned, graded outlines instead of looking, and never posed the body. This skill is the answer.
Every 3D builder and reviewer thread loads it. Blender setup and views: [`studio`](../studio/SKILL.md);
the character order (reference, brief, sheet, gate): `docs/character-workflow.md` (`claude-setup/docs/character-workflow.md`).
The per-round lists live in [`checklists.md`](checklists.md): builder checklist, reviewer checklist,
hand-in sheet contract.
How a professional game avatar is built (mesh split, naming, rig and physics bones, clothes,
face keys, Unity and Mixamo mapping), and **rule 0: test every built-in shape key at 0 and 1
before building**: [`pro-avatars.md`](pro-avatars.md).

**Where the know-how lives:** this skill (method, rules, technique), [`pro-avatars.md`](pro-avatars.md)
(how pro avatars are laid out), [`checklists.md`](checklists.md), and `docs/game-pipeline.md` (laptop paths,
characters, animation, scenes, Ren'Py and the latest lessons). Project specifics (file paths, slider values,
scene slots) live in the private game repo and the studio's `START.md` (root of `STUDIO_ROOT`).

## Order of attack: pick the best source, then model (2026-10-24)

Hand-modelling a body round after round caused the 22-round loop of 2026-10-23. Pick the best source for the job with the criteria and table in [`game-3d/refs/asset-sources.md`](../game-3d/refs/asset-sources.md) (licence first, free first), and say which step you are on:
1. An existing base from the best source: a free CC0 or VRM base, or a paid pro base after yskills' word ([`pro-avatars.md`](pro-avatars.md)). Props and rooms: free CC0 libraries first (Poly Haven; list in [`game-3d/starter/models.md`](../game-3d/starter/models.md)).
2. A generator (open-weight image-to-3D, licence read for our country, or the Blender connector's asset tools), then clean up. Order (3d-route, 2026-10-18): TRELLIS.2 (MIT; free Hugging Face Space or a laptop GPU such as an RTX 4060) first, then Blender cleanup (decimate, UV, scale) through the `studio` skill; test Meshy's free tier only if TRELLIS quality is too low; Autodesk Fusion makes no game bases. Not Hunyuan3D 2.1: Tencent's community licence excludes the EU, UK and South Korea. Open-source AI 3D output (TRELLIS, Hunyuan) needs retopology and UV cleanup and has weak hands and faces: concept props and background clutter only, never hero or rigged characters (low-poly-and-sources, 2026-10-24).
   Cleaning a generated or downloaded mesh: merge by distance, fill holes, recalculate normals outward, cut in half and mirror for true symmetry, then scale to real size. Paid or API-key options (only listed, never signed up for without yskills' OK): Tripo, Meshy paid, Hyper3D Rodin and Sketchfab (the community Blender MCP has Rodin and Sketchfab toggles, both need a key).
3. bpy modelling, only for edits to what steps 1 and 2 gave. The `attempt-guard` hook blocks a command that fails 5 times without a `## Diagnosis` in `PROGRESS.md`.

## Method v2 (Miss Galaxy line, 2026-10-19): read this first

15 more rounds (mg1 to mg15) taught what the Luna rules did not. Details and the why:
[`references/method.md`](references/method.md) (build), [`references/gate.md`](references/gate.md)
(review), [`references/master-base.md`](references/master-base.md) (one mesh for every woman).

1. **Simplest method first, and say so before building.** Scale the base's own form before adding
   any shaping key. The bust finally worked (mg14, "way better") as the PURE original breast, every
   extra key and the nipple-ring key off, scaled evenly 1.4x and a bit fuller; the butt the same at
   1.25x. Nine rounds of extra shaping keys on top made the dent and the teardrop. If a simpler
   or better method exists, tell yskills before building; he lost two weeks to a method nobody
   proposed.
2. **One key per form, never stacked.** A bad key is switched off, never patched. No added loops:
   Subdivision Surface gives density. Subdivision runs after the rig; pose correctives are keys
   driven by bone angle. Subdivision needs quads. A bust key masked by arm weights leaves a step:
   fade it.
3. **The best round is the baseline.** Never regress from it (mg2-w9 stays as the untouched
   fallback). A new round shows ref | best | new on one canvas; anything worse fails.
4. **Never again** (ERROR-SEARCH, `references/method.md`): no head or neck tools once the base is
   chosen; no stacked fix keys; no global smoothing; no profile fit against a fresh trace; no base
   switch without a same-size sheet plus two gates; crown and soles in frame; same cameras every
   round; posed set every round; never a teardrop bust.
5. **Review: one standing reviewer, plus an independent check for 5/5.** The independent reviewer is blind: it gets the written requirements, the reference and the renders, never the builder's explanation. The same reviewer thread
   re-grades every round (it holds the best-round history); do not start a fresh one per round. A
   5/5 counts only after the reviewer re-ran all views itself AND a fresh, independent reviewer
   with the checklist agreed. Gates: [`references/gate.md`](references/gate.md).
6. **Tracking.** The dense tracker and overlay bands were Luna's outline tool. With a good base the
   gate is `tools/review/review_mg.py` (frame contract, bust apex, bow, butt shelf) plus the eye.
   Numbers are hints; yskills' eye on the reference picture beats every number.
7. **Builders keep state on disk.** Update the handoff note after every finished version, so a
   compaction loses nothing (handoff only at a trigger, `docs/WORKFLOW.md`).

## The rules (each one cost a round)

1. **Pick a base that already looks right, then shape it.** Take a rigged body that is close to the
   target (our own best old model, or a licence-clean rigged body such as the CC0 MakeHuman/MPFB2
   one) and move it with shape keys. Never grow a body out of stacked edits on a mesh no one owns
   (Luna lc3 to lc11). Decide the base in the first hour, write it in LIVE STATE, say which build it
   is. Once head and neck are right, they are **locked**: no tool touches vertices above the
   collarbone again (lc3 head x0.95 and +2.5 cm, lc4 head back, lc11 chest trim at the neck base
   turned a slim neck into a short thick one).
2. **One named shape key per region** (bust, waist, hips, butt, back, thighs), authored from
   parameters (a json next to the blend), mirrored. A bad key is switched off or regenerated from
   its parameters, **never patched** with a second tool. Keep a **band-ownership map** in LIVE STATE
   (which key owns which z band); two keys never own the same band. Fillets and smooth passes are
   not keys: they were what made the Luna neck ring and the bust seam (see rule 7).
3. **Body and rig together.** Every body change is a shape key on the rigged mesh; the rig and its
   weights stay fixed; after each key the weights around it (neck, armpit, bust root, groin, knee)
   are re-checked. Shape on an unrigged mesh shows its deformation errors only when the animator
   plays a clip (Luna: tube neck, groin flap, knee pinch, found in the Rika test clip, the lock-in rule came at lc12). The **pose test runs every
   round**: from-below frame (camera low, her above it), sway mid-frame, arm up plus head tilt.
   Fail = no tube neck, no groin fold, no knee pinch, bust root stays on the chest.
4. **Grade by eye first, numbers last.** Order: bust front crop at full
   resolution vs best round and ref (the standing gate), neck crop old|new vs ref, zoom triples REF|best|new at 2x, raking raw renders in five
   views (front, side, back, back 3/4, posed). Overlay and tracker numbers are builder hints. A
   reviewer who graded on numbers let two bust regressions through (lc10, lc11) and the user caught
   them. The user's pins outrank any reviewer number. Bust and upper chest: fill, never cut.
5. **Never hand in a regression.** The builder runs every gate (neck, bust, zoom, poses) before
   anyone else sees the round. A failed gate is said in one line and the round is not handed in.
   The best round so far is always the baseline to beat, shown beside the new one.
6. **Reference hygiene.** Profile and silhouette fits run only on the verified ref trace. A
   re-trace is compared to the original by eye before any tool uses it (a hand-traced edge sat
   6 to 21 mm behind the ref skin and sent a round the wrong way). Registration (chin and sole, or
   skeleton points) is the same for ref, best and new. Judge the model itself, overlays second.
7. **Tool hygiene.**
   - Every mesh tool prints its **max vertex move** and stops over 5 cm.
   - Edits go to Basis **and every shape key**. Face expression keys stay in sync with body edits
     (`luna_facekeysync.py`: stored Face key values 0.3 to 0.45 inverted every edit in renders for
     five rounds). When an edit does not show in a render, evaluate the depsgraph mesh with and
     without the keys before blaming the tool.
   - Smoothing is local: fillets of about 2 to 3 cm radius in the problem band (under-butt, thigh
     ring over 6 cm, neck join), never one global pass (a 1.3 mm Taubin did not move cm-scale
     lumps; lc11's 400-iteration pass on z 1.33 to 1.40 left the neck ring visible). Contact tools
     never push vertices through the body (lc11 pulled 96 deep chest verts up to 20 cm and the
     stretched sheets drew a hand shape on the back). A groove needs width (rx) at least 2x its depth
     and at least 3 cm (rx 1.6 to 1.8 cm read as dark trenches, 3 cm with 3.5 to 6 mm is soft); no
     region key above 3x, 15 mm.
   - Never name a script `bisect.py` or `inspect.py` in the work folder (shadows the stdlib).
8. **Thread hygiene.** One builder and one reviewer until the score rule picks a version (`operator/gate.md`, Scored gates); a thread stays on its job
   until done, lets its context compact and keeps its LIVE STATE block on disk (yskills: no handoff
   threads, no new thread per round). A brief names **only** the LIVE STATE block, the contract
   blocks and the top 3 items of the current plan; a builder that reads whole study libraries fills
   its context on one item (a Luna builder stopped at its 210k context budget with nothing handed in). Hand-in comes
   first in the plan, research second. Cloud Blender setup is about two minutes (also in `references/method.md`):
   `apt-get update && apt-get install -y libegl1 libgl1-mesa-dri libegl-mesa0 libgles2 libtbb12`,
   `python3.13 -m pip install bpy scipy pillow numpy matplotlib`.
9. **Same size, every sheet.** The blobcg reference is the only shape target (other models, and
   other characters liked for one feature, are bases to shape toward it, never goals; the base keeps its
   neck, bust and rig, the reference decides everything else). Every sheet shows the body next to the reference on one canvas at the
   same height, registered by chin and sole (side view: chin and knee), crown inside the frame. A sheet
   with a clipped head, stray objects, cut hands, hidden hair or no figure frame (the body in the
   hinata-v1 scene with hair and shader, like the dance video) fails before scoring.
10. **Render truth.** Before trusting a picture, check the renderer shows the edit: Face keys at
   0.4/0.3/0.45 invert every tool that skips them (run `luna_facekeysync zero` last); `drender4`
   zeroes non-Face keys, so bake keys; sync `me.vertices` to Basis before building masks; a wrongly
   registered base (Hinata 1.743 m vs 1.598 m) breaks `slicefit`, fit by chin and sole.
11. **Content line.** Adult characters only, adult face and proportions, no minors ever. Check every reference set for
    the source character's canonical age before use and write the checked age and version in LIVE STATE; frames of a canonically underage character never
    enter it, whatever the art style. A thread that declines part of a job says so in one line and hands
    the rest back. Nude
   bodies and explicit poses live on the private side behind the 18+ gate; public files and the
   hand-in sheets that go to public places stay clean; his references never go into git.

## Rig conventions for every figure (2026-10-26, from the night scenes)

Same for every character and the man, so one script poses all of them:

- **Fingers:** bone +y points along the finger, -z is the palm, **+x on a finger bone bends toward the palm**
  (set `Armature["rig_version"] = 2`). A rig whose +x bends to the back of the hand looks "turned 180°"; fix it with
  a 180° bone roll plus converting the F-curves (pose identical to 0.001 mm), then old scenes with
  `migrate_rig_v2.py`. Check every new figure: fingertip offset · palm normal must be negative.
- **IK:** hand and foot IK bones with pole targets in a bone collection "IK", and the switches (`ik_arm_L/R`,
  `ik_leg_L/R`, `wrist_limit`, `toe_auto`, `skirt_follow`) as properties on the armature object. Put the constraints
  in the figure file: they survive a library override, constraints added in the scene do not. Wrist limits are
  anatomical (flex 75°, extend 70°, radial 20°, ulnar 30°).
- **Openings:** each opening (lips, vulva, anus) is a ring vertex group (`Lips_Ring`, ...) plus a path, so contact
  depth is measured from the group, not guessed. A test script reports full depth and zero skin hits after every
  body change.
- **Vertex groups:** one per body part, without `_NNN` suffixes; POV groups per part (`POV_Hips/Belly/Chest/Arms/
  Legs/Head/Penis/Hands`) so a camera hides only what it must. Lock the location of `Penis_1` so the base stays
  on the body.
- **Normals point out** on every body mesh (inward normals made the solver shove figures 25 cm); scale 1.
- **Soft parts:** dent keys driven by the distance of a probe object; talking is the viseme keys at 0.3-0.5, not
  the wide expression keys.
- **Files:** one `.blend` per figure; every old state (backups, `_before-*`, wip, `.blend1`) goes in one zip archive
  (`characters\_archive\modelle_vorher_<date>.zip` plus a list), so no thread opens a stale file.

## Technique (how the pros do it, what we copy)

Research: `/mnt/project-files/companyxy/patches/base-body/library/agent-3d-study/PRO-ADULT-BODY.md`
(sources, numbers) and `APPLY-LC14.md` (ordered rounds A to E). Read the sections you need, not
the file. Every pro pipeline (Daz, Virt-a-Mate, Koikatsu, CBBE/BodySlide, MetaHuman) is one fixed
topology, **independent morph sliders** (deltas from the base, so two sliders add and never
re-shape each other), corrective morphs on joints, grafted openings, spring bones for soft parts,
normal maps for fine anatomy.

| Part | Method | Gate (after the eye) |
|---|---|---|
| Bust | `breast_flat` key (Laplacian fill of the chest wall) + ONE generator: an ellipsoid dome per breast, ray-height smooth union, k per direction (under 10, inner 14, upper 22, outer 30 mm), nipple and areola primitive on the apex; all from a json | ellipsoid RMS under 1.5 mm; mirror error under 0.5 mm; no concave window collarbone to apex; gap between domes 0 to 6 mm; pole ratio 48:52 to 52:48; apex and internipple per the ref |
| Joints | half-angle helper bones (`knee_help`, `groin_help`, `neck_help`, Copy Rotation 0.5), twist on the 02 bones, JCM-style corrective keys per joint, direction and angle (neck back 30 / fwd 35 / twist 45; hip flex 57, 115, abduct 85, back 35; knee 90, 155), driver SWING_TWIST local space | ring cross-section 0.92 to 1.05x rest at neck, thigh root, knee; no self-overlap in the 6 cm band; no fold deeper than 3 mm on raking light |
| Openings | a welded graft: hole, ring patch, inner tube, cap, bridge, weight transfer, open and spread keys | vulva open 6 +-1 mm, spread 20 to 25 mm across the crest, anus open 10 to 14 mm, tube depth 6 / 3 cm; no back faces in the key 0 and key 1 renders (backface-red debug material, SAMPLES 3); no shading seam at the bridge on raking light; round lips |
| Bust and butt motion | 1 to 3 bones per side, weight from the dome height (root 0, apex 1), spring bones | sway clip: apex travel 8 to 15 mm, root under 2 mm, no arm interpenetration |
| Back detail | calm geometry plus a baked normal map for blades, groove, dimples, lat edge | silhouette bands unchanged within 0.5 mm |
| Neck | clean tapered cylinder on the neck bones, 20 mm fillets into trapezius and jaw, nothing else touches it | crop vs ref: long and slim, no ring, no shelf, plus a bent head frame (new base only; a locked neck is not touched) |

### Contact deformation (hands, shafts, tight clothes; 2026-10-28)

Our numbers and files: the product's `docs/LESSONS.md`.

- **Shape keys keep no volume.** A key that pulls tissue sideways around an object also pulls it toward the
  middle and pinches the front. Blend two size keys steeply or push the tissue forward on purpose; check the
  front view, not only the side.
- **Contact beats distance.** A squeeze driven by the distance hand to breast point fits one size and floats
  or sinks at the others. Use a collider (palm and fingers as probes) that pushes the skin out with a
  Shrinkwrap (Outside, a few mm offset) and then smooths; it works at every size and from every side.
- **Soft body and cloth fail on an open shell** (no volume: it folds and crumples whatever the pressure). Only a
  closed proxy volume with a pin to the chest wall would work; for loops, keyed contact is cheaper and stable.
- **Openings:** a contact layer of Shrinkwrap (Outside) -> Smooth -> Shrinkwrap on a soft mask (ring group, moved
  vertices, falloff) removes nearly all skin hits at small cost per frame and opening, with no pull on the body.
  Smooth alone pushes the skin back into the object; Outside Surface drags the whole canal. Cap depth by canal
  length (deeper needs deeper canal keys) and tilt only a little at depth.
- **Build it in the figure file, not in the scene:** modifiers added to library overrides do not survive a
  reload. Keep the layer in the base (modifiers off until a target is set) and sync it to every character.
- **Jiggle:** Wiggle 2 does not run headless; key it (lag 3 frames, one overshoot).
- **Proofs use the real character** (head, hair, skin, her own shape values), not the bare base, and several
  sizes (smallest, real, largest) from front, side and above.

**Licence.** Ship only our CC0 MakeHuman-derived body and the output of our own scripts (plus
Blender/GPL tool output; MB-Lab only via the official build with CC BY 4.0 and credit). Daz, VaM,
Illusion/Koikatsu, CBBE/BodySlide, MetaHuman, Wild Life and Subverse assets are **study only**: look
and measure, never copy a mesh; his private reference pictures are never uploaded anywhere.

## Worked example: where Luna went wrong and what fixed it

| Round | Mistake | Rule |
|---|---|---|
| lc3 to lc4 | head scaled and moved, trapezius cut | 1 |
| lc6 to lc10 | Face keys inverted every hand and smooth edit in renders | 7 |
| lc10, lc11 | tilt, contact, cleavage, forms and profile stacked on the bust; reviewer let both through on numbers | 2, 4 |
| lc11 | chest trim at the neck base, 400-iteration smooth | 1, 7 |
| lc12 | side fit on a wrong trace plus lumbar fill forms | 6 |
| lc1 to lc13 | no posed frame until the animator's clip showed 11 errors | 3 |
| 2026-10-18 14:29 | user's decision: Hinata rigged base; its neck, bust shape and rig stay, shape keys on top (waist, hips, butt; bust scaled from Hinata's own breast mesh, no stuck-on spheres) | 1, 2 |

The full story, root causes, tool gotchas and his taste: `patches/base-body/LESSONS.md`.
Files: `characters/luna/REVIEWER-TO-BUILDER.md` (contract and verdicts), `BUILDER-HANDOFF.md` (LIVE
STATE blocks), `REVIEWER-HANDOFF.md`, `proof/rika-test/ERRORS.md` (the 11 posed errors), tools
`characters/luna/tools/handin-cloud.sh`, `quickcheck.sh`, `luna_facekeysync.py`, and `tools/ref-tracker/trk2/t3/zoom5.py`, all under
`/mnt/project-files/companyxy/patches/base-body/`.
