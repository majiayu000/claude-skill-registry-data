---
name: seedance
description: >
  Expert guide for prompting ByteDance's Seedance 2.0 AI video model (text-to-video,
  image-to-video, first/last-frame, multi-reference, and multi-shot generation with
  native synchronized audio). Use when the user wants to write, improve, or debug a
  Seedance 2.0 prompt; plan a shot; work with reference images/videos/audio; animate a
  start frame or interpolate first-and-last frames; direct camera moves, motion, and
  cinematic style; generate dialogue, sound effects, or music; keep a character
  consistent across shots; or understand Seedance 2.0's capabilities, specs, API model
  IDs, limits, and access routes (Dreamina, Volcano Ark, BytePlus, fal.ai, Replicate).
  Triggers on "Seedance", "Seedance 2.0", "ByteDance video model", "Dreamina video",
  "seedance prompt", "reference-to-video", "first and last frame video".
---

# Seedance 2.0 — Prompting & Capabilities

Seedance 2.0 (ByteDance Seed team, launched Feb 2026) is a **multimodal audio-video model**: it takes text, images, audio, and video in a single call and generates a 4–15s clip with **native synchronized audio** (dialogue + lip-sync, sound effects, ambient, music) in the same pass.

**Core mental model — this drives every decision below:** Seedance 2.0 is a *physics and cinematography simulator you direct like a film crew*, not a mood board you brainstorm with adjectives. It renders physical interactions ("tires smoke as the car pivots on wet asphalt") and directorial language ("slow dolly-in", "golden-hour rim light"). It does **not** render vague adjectives ("cinematic", "epic", "amazing"). Write shot directions, not vibes.

## Capabilities at a glance

| Mode | Input | Use it for |
|------|-------|-----------|
| **Text-to-video (T2V)** | prompt only | Generating a scene from scratch |
| **Image-to-video (I2V)** | 1 start image + prompt | Animating an existing still |
| **First-and-last frame** | 2 images (`first_frame`+`last_frame`) + prompt | Controlled transitions / reveals / before-after |
| **Reference-to-video (R2V)** | 1–9 images + ≤3 videos + ≤3 audio (max 12 files) + prompt | Character/style/motion/object consistency, voice, "omni" composition |
| **Multi-shot** | prompt with a shot list / timeline | A short narrative (up to ~6 shots) in one 15s generation |
| **Video-extend** | prior clip + prompt | Continuing past 15s by chaining |

**Native specs:** 480p/720p native (1080p and native 4K on hosting platforms), 4–15s, 24 fps, aspect ratios `auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16`. Audio is on by default (`generate_audio: true`), at no extra cost. Full specs, access routes, model IDs, pricing, and the raw API request shape are in **`references/access-and-specs.md`** — read it when the user asks how to call/access the model or needs exact limits.

## The universal prompt formula

Order matters: the model reads left-to-right and weights the front most heavily. The first 2–3 instructions land reliably; adherence drops after ~8 requirements. Front-load subject and action.

```
[Subject] + [Action] + [Environment] + [Camera] + [Lighting] + [Style] + [Constraints]
```

- **Subject** — who/what, with concrete material/age/wardrobe detail
- **Action** — ONE clear action, present tense (compound choreography causes "melting")
- **Environment** — where, time of day, weather
- **Camera** — ONE primary move + shot size (see rules below)
- **Lighting** — the single highest-leverage element; always name it explicitly
- **Style** — 2–3 named anchors (director/film-stock/movement), never vague adjectives
- **Constraints** — what to keep fixed, plus duration & aspect ratio

Target **60–100 words** for a single shot (hard ceiling ~3000 characters; the model starts averaging past ~150 words). Write natural, directorial prose — not a keyword list.

**Worked example:**
> "A weathered fisherman in a yellow raincoat hauls a net over the side of a small wooden boat. Grey choppy sea, dawn, light drizzle. Camera slow tracking shot from the water's surface, gentle rise. Hard rim light through overcast sky, desaturated teal grade, 35mm film grain. Realistic water weight and rope tension, feet planted. 8 seconds, 16:9. Avoid jitter and bent limbs."

## Non-negotiable rules (the highest-leverage ones)

1. **One primary camera move per shot.** "Slow push-in" ✅. Stacking pan + zoom + dolly + handheld ❌ → "soup".
2. **Never mix camera motion and subject motion in one clause.** ✅ "The dancer spins slowly. Camera holds a fixed frame." ❌ "spinning camera around a dancing person" → jitter.
3. **Name lighting explicitly.** If you add only one thing to improve a prompt, add a lighting description.
4. **Physics, not adjectives.** Describe weight, friction, impact, cloth/fluid behavior. Never write bare "fast" (the #1 quality-killer) — qualify pace ("slow, smooth, gradual") and apply speed to one element only.
5. **Named style anchors beat vague words.** "Wes Anderson symmetry, 35mm Kodak grain" ✅. "beautiful, cinematic, epic" ❌.
6. **State consistency locks** in any reference-based or multi-shot prompt, or characters/outfits drift.
7. **Scale beats to duration** (multi-shot): ~2–3 beats/5s, 4 beats/10s, 5–6 beats/15s. One action + one camera move per beat.

These plus the full camera/motion/style/multi-shot/negative-prompt vocabulary and 10 worked example prompts are in **`references/prompting.md`** — read it for any non-trivial prompt authoring, camera direction, multi-shot storyboard, or when the output has artifacts to debug.

## Reference tagging basics

When any image/video/audio is attached, bind it into the prose with `@Image1`, `@Video1`, `@Audio1` (numbered by input order) and **always state what each reference controls** — identity vs. camera-motion vs. style vs. audio. Vague "reference @Video1" is a top failure mode.

- ✅ "The woman in `@Image1` with dark curly hair walks down a neon street; reference `@Video1` for the camera movement only; background music from `@Audio1`."
- ❌ "Woman, @Image1, dancing, @Video1, sunset, 4k." (keyword soup + unattributed refs)

**Real human faces cannot be uploaded as direct references** (anti-deepfake policy) — use virtual portraits or the registered asset library (`asset://<ID>`). Reference modes, character-consistency workflow (reference packs), style transfer, image specs, start-frame/first-last-frame mechanics, and clip continuation are all in **`references/references-and-frames.md`** — read it whenever references, start frames, keyframes, or cross-shot consistency are involved.

## Audio basics

Audio generates natively and synced in the same pass. Steer it in the prose prompt (there are no volume parameters):

- **Dialogue** — wrap spoken lines in double quotes and keep them short (~12 words per 10s / ~20 per 15s or lip-sync drifts): `The man leans in and says: "Remember this moment."` Add delivery after: `dry, a little proud`.
- **Sound effects** — name source + material, optionally timestamped: `SFX: boots on wet cobblestone; thunder crack at 3s`.
- **Music/ambient** — write a short "sound brief": `Audio: low acoustic guitar, distant rain, no voiceover`.
- **Suppress unwanted score** — open prompts default to a "car-advert" music bed; write the literal phrase `no music` (or, for total silence, `silent, no dialogue, no ambient, no audio of any kind`).

Dialogue syntax, lip-sync conditions, reference-voice cloning (`@Audio`), supported languages, the `generate_audio` toggle, mix priority, and limitations are in **`references/audio.md`** — read it whenever the video needs spoken lines, SFX, music, or voice control.

## Workflow

1. **Clarify intent** — subject, motion, mood, duration, aspect ratio; are there reference images/frames/audio?
2. **Pick the mode** from the capabilities table.
3. **Draft the prompt** with the universal formula; apply the non-negotiable rules; read the relevant reference file for depth.
4. **Add references/audio** with `@` tags + explicit function, if any.
5. **Recommend an iteration path** — draft short (5s) in the Fast tier to test believability, then finalize longer in standard. Small prompt edits can cause large shifts, so change one thing at a time.
6. If the user is calling an API, pull exact model IDs / request shape from `references/access-and-specs.md`.

## Key limitations to set expectations

15s hard ceiling per generation; motion/physics can break in complex multi-person scenes; on-screen text renders poorly (add text in post); character identity drifts across long or crowded clips; non-English lip-sync is weaker; multi-speaker sync is an open problem; no LoRA/fine-tuning (closed, API-only). IP safeguards block realistic-face references and named-celebrity/trademark prompts. Details in `references/access-and-specs.md`.
