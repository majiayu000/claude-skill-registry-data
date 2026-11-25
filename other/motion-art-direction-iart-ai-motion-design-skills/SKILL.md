---
name: motion-art-direction
description: This skill should be used when the user asks to "direct a motion graphics video", "do creative/art direction for a video", "define a motion language", "set the tone and pacing", "make the animation feel consistent", "decide what to animate (and what not to)", "turn a brief/brand into motion choices", or needs the senior creative judgment that sits above specific techniques (gsap/lottie/shader). Covers motion language, tone & energy, pacing/rhythm, motion hierarchy, restraint, and cross-shot consistency.
version: 0.1.0
---

# Motion Direction

Make the creative decisions for a motion piece before anyone animates a frame. Direction is the judgment layer: it turns a brief and a brand into a small, repeatable set of motion rules — one easing vocabulary, one timing scale, one transition family — so every shot feels like it came from the same hand. Good direction is mostly subtraction: deciding what NOT to move.

## When to use

- Starting any piece — explainer, launch film, UI demo, data story, loop — and the look/feel isn't decided yet.
- Animation feels "busy", "cheap", or "inconsistent" and the cause is decisions, not craft.
- Orchestrating other skills (gsap/lottie/shader/three.js): direction sets the rules they execute.
- Translating a brand or brief into directable, written choices a team (or an agent) can follow.

## The one rule

**Define the motion language first, then animate to it.** A motion language is a short spec — pick *one* of each: easing family, base timing unit, transition family, stagger rhythm, motion intensity. Everything in the piece obeys it. Consistency reads as confidence; variety reads as noise. When in doubt, reuse, don't invent.

## Direction workflow

| Step | Decision | Output |
|---|---|---|
| 1. Brief | Audience, one message, platform, duration, mood (3 adjectives) | One-line creative intent |
| 2. Tone & energy | Where it sits on calm↔kinetic and soft↔sharp | A point on the matrix below |
| 3. Motion language | Lock the spec table | The motion-language spec (filled) |
| 4. Hierarchy | Rank what moves: hero / support / texture | Motion hierarchy list |
| 5. Restraint pass | Cut motion that doesn't carry meaning | List of what stays static |
| 6. Shot direction | Note intent per shot, not keyframes | Direction notes (see template) |
| 7. Consistency check | Audit against the spec | Pass/fail per shot |

## Tone & energy matrix

Place the piece on two axes; the cell dictates the motion language defaults.

| | Soft (organic, eased) | Sharp (precise, snappy) |
|---|---|---|
| **Calm** | Luxury, wellness, editorial — slow, long eases, generous holds, minimal stagger | Premium tech, fintech — deliberate, clean linear-ish moves, tight but unhurried |
| **Kinetic** | Playful, lifestyle, kids — bouncy/overshoot, springy, loose timing | Sports, hype, gaming — fast cuts, hard snaps, aggressive overshoot on beats |

Pick one cell and commit. Mixing cells within a piece is the most common cause of "inconsistent" motion.

## Motion personality (named presets)

The tone matrix tells you *where* the piece sits; a **motion personality** is the named, numeric preset you hand to whoever animates. Pick ONE per project and apply it everywhere. This is shared vocabulary — other skills (e.g. `gsap-web`, `micro-interaction`, the video packs) can just say "use the Premium personality."

| Personality | Duration | Signature easing | Overshoot | Reads as |
|---|---|---|---|---|
| **Playful** | 150–300ms | `ease-out-back` / `cubic-bezier(0.34,1.56,0.64,1)` | 10–20% | fun, bouncy, whimsical |
| **Premium** | 350–600ms | `cubic-bezier(0.4,0,0.2,1)` | 0% | elegant, minimal, luxury |
| **Corporate** | 200–400ms | `cubic-bezier(0.2,0,0,1)` | 0–3% | clean, professional, trustworthy |
| **Energetic** | 100–250ms | `ease-out-expo` | 15–30% | bold, dynamic, hype |

Default: **Corporate** for UI/product, **Playful** for illustration/lifestyle. Maps onto the matrix — Premium≈calm-soft, Corporate≈calm-sharp, Playful≈kinetic-soft, Energetic≈kinetic-sharp. The personality fills the "easing family / base timing unit / motion intensity" rows of the spec below.

## The motion-language spec

The core artifact. Fill every row with ONE choice and reuse it everywhere.

| Property | Choose one | Example (calm-sharp / premium tech) |
|---|---|---|
| Easing family | The signature curve for ~90% of moves | `cubic-bezier(0.22, 1, 0.36, 1)` (decelerate, soft landing) |
| Base timing unit | The atomic duration; build others as multiples | 0.4s (enters 0.4s, big moves 0.8s, micro 0.2s) |
| Transition family | How shots connect | Match-cut + crossfade only; no wipes/spins |
| Stagger rhythm | Delay between grouped elements | 60ms cascade, top-to-bottom |
| Motion intensity | Distance/scale/overshoot budget | Travel ≤ 24px, scale 0.96→1.0, overshoot ≤ 2% |
| Hold discipline | Minimum rest between moves | ≥ 0.3s of stillness after each beat |

Two eases maximum: one "in" (exits) and one "out" (entrances/landings). A third curve must justify its existence.

## Motion hierarchy

Not everything earns motion. Rank every element, then animate down the list — and stop early. These three tiers are the universal **three motion layers** (see `animation-principles`): Hero = **Primary**, Support = **Secondary**, Texture = **Ambient**.

| Tier | What it is | How it moves |
|---|---|---|
| Hero | The one thing the shot is about | Gets the boldest, slowest, most-eased move; lands on the beat |
| Support | Context that helps the hero land | Smaller, faster, eased *out* of the way; never competes |
| Texture | Background, grain, ambient drift | Subliminal only — slow loops, low contrast, no hard cuts |

If two elements compete for the eye in one frame, the direction has failed. Demote one to support.

## Restraint — what NOT to animate

The senior move. For each element ask: *does the motion carry meaning?* If not, hold it still.

- Don't animate the entire frame at once — stagger or hold a anchor so the eye has a home.
- Don't transition the transition (no animated wipe *and* a spin *and* a fade).
- Don't loop-animate text the viewer is still reading.
- Don't add overshoot to serious/financial content — it reads as toy-like.
- One "wow" moment per piece. A second one cancels the first.

## Pacing & rhythm

Pacing is the edit's heartbeat. Vary it on purpose: tension (faster, tighter) → release (a hold). Map energy across the timeline before timing individual moves — most pieces want a low-energy open, a build, a peak, and a settled end card. Cut and land key moments on the audio (see launch-video for beat-syncing); silence and stillness are pacing tools, not gaps to fill.

## Consistency check

Before sign-off, audit every shot against the spec table:

- Same easing family on comparable moves? (No stray `linear` or `ease`.)
- All durations are multiples of the base unit?
- Only the chosen transition family between shots?
- Stagger rhythm identical across grouped reveals?
- Hold discipline respected — no two moves stacked without rest?
- Exactly one hero per frame?

Any "no" is a direction defect, not a craft preference — fix it before polishing.

## Reference files

- `references/direction-playbook.md` — worked examples of the motion-language spec for five tone cells, a full brief template, a shot-by-shot direction-notes template with example entries, brand→motion translation tables, an easing-vocabulary cheat sheet, and a complete pre-render direction checklist.
