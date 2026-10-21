---
name: ambience-and-sound-for-stills
description: >
  Ambience beds, gap fill and spot effects for narrated documentaries, especially films built
  from photographs and silent archive: bed levels and coverage (never dead air), the gap lift,
  the layer hierarchy (bed / texture / spot / designed transition), density and timing rules
  for spot effects, no-sound classes (portraits, details, weak pictures), worldizing and
  era-matching so generated effects do not sound like a cartoon, and the witness test. Uses
  the opendubstage foley CLI (analyze, plan, check, generate, render). Use when someone asks
  "what should play under these stills", "there is dead air between lines", "should this
  photo have a sound", "the effects sound cheesy / like a stinger", is generating or placing
  sound effects from image descriptions, or is laying ambience under narration. Do NOT use
  for music (music-under-narration) or chapter joins (scene-transitions).
---

# ambience-and-sound-for-stills

A pause in a narrated film must sound like a place, not a dropout. A photograph gets a sound
only when something visible would make one, placed further away than the narrator. OpenDubStage
tool: `opendubstage foley` (`opendubstage.foley`: `plan`, `check`, `Rules`, `levels`,
`prompts.lint`, `post.ERA_EQ`, `post.ROOMS`).

## 1. Beds: never dead air

| Rule | Number | Source |
|---|---|---|
| A bed runs under every narrated stretch | per-cue target −40 LUFS at a −24 dialogue anchor (−16 LU); duck −3 dB under speech | Torcoli et al. 2019: ambience ≥ 15 LU under commentary |
| Not inaudible | −44 LUFS with a −5 duck (−49 under speech) is inaudible on a TV at living-room level; beds are the room the voice lives in, not a safety net against the silence detector | NPR §5 "what pros would say"; measured in practice |
| Gap lift | +5 dB over any stretch > 3 s with no speech and no music, eased 2 s; never above −33 LUFS short-term | measured in practice (45 accidental holes in one mix) |
| Gaps are air, not holes | momentary loudness (400 ms) in every speech gap ≥ −46 LUFS; ambience in the clear −38…−42 LUFS | Torcoli; EBU Tech 3341 |
| Dead-air detector | no span below −60 dBFS sample peak for > 3 s between first and last cue (strict: −50 dBFS / 2 s); programme head and tail exempt | `opendubstage qc` `dead_air`; ffmpeg `silencedetect` |
| **Coverage check** | the union of bed cues (target ≤ −38) covers [0, total] with no hole; dead air usually comes from beds shorter than their scenes, so check every bed's source length against the scene it must cover before mixing | measured in practice |
| Designed silence | at most two per film, chosen by hand, listed in an explicit whitelist that the dead-air check reads; inside one, nothing plays, not even the bed | Albrechtsen (total silence once or twice per film); Burns |
| Bed joins | successive beds crossfade 5 s (start 5 s early), never fade from silence at a chapter start; one bed per scene, chosen from the scene's pictures (time of day, place), not per still | `foley.Rules.bed_crossfade_s`; TSNGO (distance per scene) |
| Loops | 3–5 s equal-power; lengths that are not multiples of each other (41 s / 67 s) | Pixflow; rule of thumb |
| Nature beds under voice | low-pass 8 kHz so pines and crickets sit behind the voice and do not read as "nature documentary" | measured in practice |
| Room-tone floor | a learned floor from the narration's own gaps at −46 LUFS under the whole dialogue stem (see `dialogue-editing-and-restoration` §3) | NPR room-tone practice |
| Perspective | on a few hero stills only, ±1–2 dB of bed top end following a push-in or pull-out; nothing else follows the picture move | Milano on *Apollo 11* ("sweep the treble and go with the motion") |

## 2. Layers and levels (relative to dialogue)

| Layer | What | Level vs dialogue | At −24 |
|---|---|---|---|
| Bed | continuous scene ambience | −16 LU | −40 |
| Texture | semi-continuous and placeable: distant voices, water, birds, a far train; 10–40 s, 3 s fades; one at a time, changes with the scene | −12 LU | −36 |
| Spot | one-shot matched to a visible source | −8 LU (hero still −4) | −32 (−28) |
| Designed transition | a door, a car passing, applause, a shutter that *is* the cut; hand-requested, ≤ 1 per chapter | −2 LU | −26 |

Nothing in the effects stem ever reaches dialogue level (`levels.MAX_OFFSET_LU = −2`).
**Distance is the dial**: the narrator is present; the photograph is a memory; a sound that
comes across nearer than the narrator is wrong (Heywood, TSNGO: distance, not level, keeps a
long film from becoming monotonous). Murch's two-and-a-half layers: dialogue + bed leaves half a
layer for spots and music together.

## 3. Density and timing (`foley.Rules` defaults)

| Rule | Value |
|---|---|
| spots per still | ≤ 1; only visible sources (Kwok, TSNGO) |
| spots per minute | ≤ 4 under narration; ≤ 6 in a narration-free montage; 0 under music-up; 0 under live or sync sound |
| spacing | ≥ 5 s between spots; ≥ 30 s before the same class repeats; the same sample never within 600 s; 3 variants per class, rotated |
| placement | `cut + 0.8 s ± 0.3 s`, never within 0.4 s of the cut (a sound on the cut reads as a stinger); if blocked, the still's midpoint once |
| end | 0.1 s before the next cut; a spot belongs to its picture |
| spot fades | in 0.03 s, out 0.3 s |
| narration guard | nothing in the 0.5 s before a narration onset, nor on its first 0.3 s |
| key lines | bed only from 4 s before to 3 s after; textures end before the window |
| textures | one at a time, 10–40 s, 3 s fades |
| designed transitions | ≤ 1 per chapter, by hand |
| picture moves | spots never follow the Ken Burns move; no whooshes, risers or stingers (the lint rejects them) |

Natural density is low: measured on a large set of captioned photographs, roughly one spot-worthy
object per 5–6 stills. Do not invent sounds for most pictures.

## 4. When not to add sound

- Portraits, close-ups, posed pictures, smiles (a face ≥ 3 % of the frame counts as a portrait).
- Details and documents: cake, rings, dress, letters, maps, certificates.
- Technically weak pictures (blurry, dark, overexposed): the picture is already asking for forgiveness.
- Objects that make no sound: a lantern does not tick; a padlock being clicked shut does, only if the hand is in the picture.
- Anything with real sync sound (speeches, performances, interviews on camera): the camera already heard it (*Apollo 11* left the EVA audio alone).
- 360° spheres and wide empty landscapes: bed plus one slow directional wind texture, no spots (*Fire of Love*: "winds give it a sense of direction").
- Inside a key line, and inside a designed silence.

## 5. Avoiding the cartoon feel

1. **One action, one material, one place, one distance** per prompt; tail "no music, no voices" (Spiegel: a Panzer "in snow", "on wet road", "on dry road").
2. **Lint** (`foley.prompts.lint`) rejects whooshes, swooshes, risers, swells, braams, impact hits, stingers, comedic sounds, music, intelligible speech, "epic" or "cinematic" scale.
3. **Match the era and the mic** (`post.ERA_EQ`): `highpass=f=80,lowpass=f=9000,equalizer=f=3500:t=q:w=1.2:g=-3`, 30 ms fades, then loudness-normalise to the layer table. Libraries and generators "sound too modern" (TSNGO; Burns' team); Albrechtsen records foley "badly" on purpose to match rough production sound.
4. **Worldize** (`post.ROOMS`): a short room matched to the bed: trees / open land (early reflections only, ~0.4 s), street, small room (~0.5 s), hall (~1.1 s). The narrator's own room is never applied to the photograph's sounds.
5. **Prefer textures to hits**: laughter as a distant group, not a sitcom laugh; a few steps on pine needles, not a march; one glass at a table, not a toast cascade.
6. **Keep source artefacts**: handling noise, the maker's breath, interjections are texture (*Cameraperson*, *Fire of Love*).
7. **Witness test**: play a viewer five stills with and without the effects. If they cannot say which is which but prefer "with", the level is right; if they can point at the effect, lower it 3 dB or remove it (Burns' veterans: "Yes, that's the way it was").
8. **Invent only from evidence, then age it** (*Apollo 11*'s 1202 alarm built from the NASA spec and dirtied).
9. **Textures and beds**: `loop=true`, 22–30 s, low prompt influence (0.3) for natural variation; spots 1–3 s at higher influence (0.6); three variants each; keep a manifest with prompt, parameters and date so generation is reproducible.

Prompt template and keyword → class map: `references/prompts-and-classes.md`.

## 6. Workflow with `opendubstage foley`

```
opendubstage foley analyze SEQUENCE.json [--vision]           # scene analysis per still (keywords, or Apple Vision labels)
opendubstage foley plan SEQUENCE.json -o cuesheet.json [--vision]   # analysis -> cue sheet under the rules; rejected candidates are listed in "decisions"
opendubstage foley check SEQUENCE.json cuesheet.json          # re-verify a (hand-edited) cue sheet; exit 1 on any violation
opendubstage foley generate SEQUENCE.json cuesheet.json --backend library|woosh -o fx
opendubstage foley render cuesheet.json -o stems               # per-layer stems with ffmpeg
```

`plan` always passes `check` (property-based tests assert it). Hand edits go through `check`.
Resolution order when choosing a cue: the picture's moment type wins (speeches, performances, portraits →
none); then the no-sound classes; then the first matching spot; then texture; the bed from the
scene's median time of day and the majority bed selector among its pictures.

## 7. Verify

| Check | Threshold |
|---|---|
| bed coverage | union of bed cues covers [0, total]; every bed source ≥ its scene length (or looped) |
| gaps | momentary ≥ −46 LUFS in every speech gap; no `dead_air` outside the designed-silence whitelist |
| effects stem | short-term never above −28 LUFS; spot count per 60 s window ≤ 4 under narration |
| placement | no spot within 0.4 s of a cut, within 0.5 s before a narration onset, or inside a key-line window |
| anti-cartoon | every generated file passed the lint, `ERA_EQ` and a room; the witness test was run on ≥ 5 stills |
| textures | ≤ 1 at a time; 10–40 s |
