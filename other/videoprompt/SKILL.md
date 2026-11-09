---
name: videoprompt
description: Write production-grade prompts for AI video generation in the Seedance 2.5 shot-memo style. Use whenever the user wants to write, revise, extend, or break down a video-generation prompt or shot description for any shot-based model (Seedance, Veo, Kling, Sora, Hailuo) — character beats, dialogue scenes, aerial/VFX shots, scene extensions/continuations — even if they don't name the tool. Also use when converting a scene, beat, or storyboard frame into a prompt a video model will consume.
---

# Videoprompt — Seedance 2.5 shot-memo prompts

Turn a shot idea into a production-grade video prompt: fixed sections in a fixed order, beat-level timing, locked character identity, motivated lighting, and a hard must-hit checklist. Everything here is reverse-engineered from three working Seedance 2.5 production templates, stored verbatim in `references/seedance-examples.md`. Read the example closest to your shot type before writing:

- **Example 1** — short character beat, 3–5s, night exterior, one dialogue line
- **Example 2** — aerial/VFX arrival, scene extension of a previous clip
- **Example 3** — interior dialogue one-shot, ~16s, multiple beats and exits

## Core principles

These are why the templates work. Apply all of them, every time.

1. **Write a shot memo, not a pitch.** The model is a literal-minded film crew. Every section answers exactly one question a department head would ask (who, where, what light, what lens, what happens when). Never merge sections, and never narrate story context beyond what the camera can see in this one clip.

2. **Positive constraints.** The must-hit list states what WILL be true ("Oscar must sit on the upper edge with legs dangling"), not warnings. Reserve "no X" for naming a specific known AI failure mode (see the antidote table below). Generic negatives ("not boring", "not weird") do nothing.

3. **Redundancy on load-bearing facts.** Anything that must survive generation gets stated 2–3 times in different sections: dialogue appears in ACTION TIMING, AUDIO, and POSITIVE CONSTRAINTS; hero staging appears in LOCATION MAP, CAMERA, and POSITIVE CONSTRAINTS. Single-mentioned facts get dropped — repetition is the feature, not a flaw.

4. **Lock identity twice.** Every recurring character, prop, or location gets both its @reference tag AND a full physical description in the body. Tags alone drift; prose alone drifts. Tag names carry the variant (`@char_ruth-noglasses` = the no-glasses version). Only use @tags that exist in the user's project — never invent them; ask which assets exist if not stated. Continuity micro-props get named where they live ("the @watch- on the left wrist while she drives").

5. **Screen-space directions + metric anchoring.** Give directions relative to the FRAME ("to the LEFT of FOOD", "exits to the LEFT", "ENTERS FRAME from ABOVE") — the model cannot take direction from a character's point of view. Give sizes and distances in real units ("around 5 meters in diameter", "about 50 meters in front") and by comparison ("clearly smaller than the observatory").

6. **Name the failure mode, not the fear.** "No postcard drone look", "no opening freeze shot", "no aggressive sci-fi laser sound" work because they name the exact artifact. Before writing, ask: what is the default cheesy version of this shot? Then write its antidote into the prompt.

## Section skeleton — fill in this order

**0. Title + setup.** Scene name and 2–3 sentences: where we are, what is already true, what happens in this clip. For continuations, open with "Direct continuation of/from @Video N" (see "Extending a previous clip" below). Reference @images/@videos/@chars inline.

**1. PACING.** One line, 2–4 words of rhythm: "Fast, funny, character-driven."

**2. ENERGY.** The kinetic-emotional arc. A beat-chain is ideal: "slow approach → realization → cute confirmation → abrupt stop → quiet exit."

**3. EMOTION.** One line per character, as attitude: "Ruth is grumpy but committed. Oscar is delighted."

**4. COLOR** (longer shots). `60:30:10 — [dominant] / [secondary] / [accent]` with a named palette: "pale desert morning / dusty interior browns / faint cool metallic accent."

**5. CHARACTERS / HERO LOCKS.** One block per character: age, build, face, hair in concrete visual terms; wardrobe; skin or material texture; plus a one-line attitude. This is the identity lock — write the full physical description even when an @tag exists. Make characters distinguishable by silhouette alone (floral nightgown + sleep bonnet; charcoal glistening amphibian skin with three wet eyes).

**6. LOCATION MAP.** Spatial staging in frame terms: who and what is where, relative positions, distances. For extends, also stage what is NOT yet visible: "The alien craft is not yet in frame at the start."

**7. FORMAT MODE.** Shot law #1: "One single continuous shot. No cuts." Add "No opening freeze shot" — a common AI default — whenever it could occur.

**8. OPTICS.** FOV in degrees plus lens character: `47° FOV. Physical cine lens.` for human-scale character work; `29° FOV` for telephoto compression and distant/aerial elegance. Camera personality belongs here too: "far away and elegant, not close or documentary."

**9. CAMERA.** Position, shot size, movement style ("static or only very subtly shaky from vehicle vibration"; "subtle floating camera or tiny handheld drift only"), plus a frame-content checklist: "The frame must clearly show: A, B, C, D." Hard camera laws go here: "The camera never leaves the cabin."

**10. ACTION TIMING.** The beat sheet. Time ranges that sum to the clip length; each beat is one dramatic event with concrete physical action, verbatim dialogue in screenplay format, and reactions. Example beat:

   ```
   0:04–0:09

   Ruth keeps driving, eyes forward, skeptical and dry:

   RUTH:
   "The alien compass brought us here."
   She glances toward Oscar.
   "Is that right, Oscar?"
   ```

   The end-state belongs to the last beat: "End with the UFO hovering in perfect alignment over the observatory." / "Hold one small beat on the empty view. CUT." See beat math below.

**11. PHYSICS.** How mass and contact behave: suspension and jolt, believable balance corrections, prop weight, "mass has real weight, correct contact shadows", scale caps ("No oversized mothership scale — it is medium-sized and clearly smaller than the observatory").

**12. LIGHTING.** Time of day, then every light source by name, all diegetic: night sky ambience, warm spill from trailer windows, beam glow, diffuse daylight through the windshield. Craft terms that land: rim light, fill, catchlights, bloom, atmospheric haze for separation. Add caveats where the model could fail: "subtle reflections on the windshield are allowed, but the observatory must remain clearly visible."

**13. AUDIO.** Open with "Environmental SFX only. No music. No subtitles." Then enumerate SFX sources (spray can hiss, cabin rattle, tires on gravel), repeat the dialogue verbatim in character-name-colon format, and give restraint rules per event ("a smooth, restrained, otherworldly descending resonance. No aggressive sci-fi laser sound."). Creature sounds are onomatopoeia: "Prrrp!"

**14. CHARACTER ACTING.** One block per character: subtext and micro-behavior, not adjectives. "'That's it?' is not a joke line played big — it is quiet, real disbelief." / "one restrained micro-expression of: how did I end up here?"

**15. STYLE** (plus **QUALITY** for longer shots). The register in one or two lines, including where the feeling comes from: "The humor comes from the seriousness of the filmmaking applied to this very strange little trio." QUALITY adds acceptance criteria: "emotionally legible in one take."

**16. POSITIVE CONSTRAINTS.** The hard checklist, 6–12 one-line items, harvested from everything above: duration ("Exactly 3 seconds"), single-shot law, wardrobe and prop facts, hero positions, exact dialogue ("VACE says exactly: 'That's it?'"), end-state. Every item must be checkable by watching the clip once.

**17. Boilerplate footer.** Copy verbatim — see below.

## The boilerplate footer (append verbatim)

Every prompt ends with this fixed quality block. Copy it exactly; per-shot behavior lives in the sections above, never in the footer.

```
Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: floating immersive camera that lives with the actors; natural motivated light; painterly composed frames, strong silhouettes against the light.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with catch-lights, visible breath and chest rise.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

Variant: for natural-light day shots, the source templates insert this line after Cinematography:

```
Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze throughout. Key light from sky and windows only.
```

Note: the footer says "floating immersive camera" even when the shot is static — in the source templates it is an uncustomized fixed block. Keep it as-is; the CAMERA section governs actual behavior.

## Beat math

ACTION TIMING beats sum to the target duration, one dramatic event per beat:

- 3–5s → 1 beat; one action, at most one short line
- 6–10s → 2–3 beats
- 11–16s → 3–5 beats; can carry a short dialogue exchange, entrances/exits, and a closing hold

Keep dialogue lines short (≤ 8 words) — lip-sync degrades fast on longer lines.

FOV: 47° = human-scale character work; 29° = telephoto compression, distant or aerial elegance. Only these two appear in the source templates; wider (~65°) for tight interiors is a reasonable extension.

## Extending a previous clip

Continuation prompts carry extra rules:

1. Open with "SCENE extend @Video N" or "Direct continuation from ... @Video N" in the title/setup.
2. Declare the world state at frame one — the new clip's first frame equals the old clip's last frame: "It is already fully dark. The soft translucent beam is already rising from the observatory roof."
3. Explicitly stage what is NOT yet in frame: "The alien craft is not yet in frame at the start."
4. Specify the new clip's end-state ("End with the UFO hovering in perfect alignment over the observatory") — that final frame is the handle for the next extension.
5. Restate continuity anchors (the van's position, the painted words) even though the previous clip established them.

## Failure-mode antidotes

Known AI-video artifacts and the exact lines used against them. The "no" form is allowed ONLY here — each entry names a real artifact, not a vague fear.

| Artifact | Antidote line |
| --- | --- |
| 3D-render / game-cutscene look | "Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic." |
| Frozen opening frame | "No opening freeze shot." |
| Jittery motion | "24fps smooth motion. No jitter." |
| Identity drift between shots | "Characters, props, environment identical across every cut. No identity drift." |
| Weightless, floating props | "Mass has real weight, correct contact shadows. No floating props." |
| Plastic skin | "Pore-level realism — vellus hair, asymmetric moles, capillary flush." |
| Dead eyes | "Wet living eyes with catch-lights, visible breath and chest rise." |
| Postcard drone footage | "No postcard drone look." + "far away and elegant, not close or documentary" |
| Handheld creep | "No handheld feel." / "Subtle floating camera or tiny handheld drift only." |
| Stock sci-fi zaps | "No aggressive sci-fi laser sound." + describe the restrained sound you do want |
| Auto music / burned-in subtitles | "Environmental SFX only. No music. No subtitles." (appears 2–3× per prompt) |
| Scale inflation | Real measurements + comparison: "medium-sized, around 5 meters wide, clearly smaller than the observatory." |
| Static tableau open | "Every person moving from frame one." |

## Workflow

When asked to write or revise a video prompt:

1. **Collect shot facts first**: duration, shot type (character beat / dialogue scene / aerial-VFX / extension), which @reference assets exist (ask if not given — never invent tags), dialogue, and the must-hit list. Missing facts → ask the user; don't guess.
2. **Read the nearest example** in `references/seedance-examples.md`.
3. **Fill the skeleton** in order, applying the six core principles. Write POSITIVE CONSTRAINTS last — it is harvested from everything above.
4. **Append the boilerplate footer** verbatim.
5. **Run the pre-flight checklist.** Fix, then deliver the prompt as one copy-paste block: ALL-CAPS section headers, plain text, no markdown inside the prompt itself.
6. Write prompts in English regardless of the conversation language.

## Pre-flight checklist

Before delivering, verify every item:

- [ ] Beats sum to the target duration; each beat is one dramatic event.
- [ ] Every load-bearing fact (dialogue, hero staging, end-state) appears 2–3× across ACTION TIMING / AUDIO / POSITIVE CONSTRAINTS.
- [ ] Every recurring character, prop, and location has both its @tag (only if it exists in the project) and a full physical description.
- [ ] All directions are screen-space (LEFT / RIGHT / ABOVE / behind); all sizes and distances in real units.
- [ ] Dialogue is verbatim, screenplay-formatted, and marked "says exactly".
- [ ] Every light source is named and diegetic.
- [ ] POSITIVE CONSTRAINTS covers duration, single-shot law, wardrobe/prop facts, hero positions, exact dialogue, and end-state — each item checkable by watching the clip once.
- [ ] "No X" lines only name known failure modes from the antidote table.
- [ ] Boilerplate footer appended verbatim; per-shot behavior lives in the sections, not the footer.
