---
name: 3dicon
description: Turn a prompt or a still image into a looping animated icon with real transparency — GPT Image / Nano Banana for the art, Seedance via OpenRouter for the motion, exact-unpremultiply matting for the alpha, animated WebP out. Use when asked to animate an app icon, make a 3D icon loop, produce a transparent animated asset, or add motion to flat icon art.
---

# 3dicon

Generate a still, animate it into a seamless loop, key the background out
properly, and encode it as an animated WebP with true soft alpha — the format
`expo-image`, Chrome and Safari all render natively, with no Lottie conversion
and no new native dependency.

## Before anything

1. `pip install -r requirements.txt` (or `uv pip install -r requirements.txt`).
2. `cp .env.example .env` and fill in the keys for the backend you want.
3. `ffmpeg` must be on PATH.

Check the keys are present *before* running — `animate` costs money, and a run
that dies halfway has already spent it.

## Always stop after the still

One still, then ask. Never generate several takes to choose from, and never
run through to the animation without the user seeing the art first.

1. Generate exactly ONE still.
2. **Show it to the user** and ask plainly whether they are happy with the
   static design before anything else happens.
3. Only on a yes, animate it.

Why this is a hard rule, not a nicety: the still is 13 cents and the full run is
48 cents and four minutes, and every later stage inherits the still's object,
colour and weight. Animating art the user has not approved means paying twice.
`run` therefore stops after the still on purpose.

If they are not happy, adjust the prompt and generate one replacement — not a
grid of options. Variants exist behind `--variants` but are off by default and
should stay that way unless the user asks to compare.

## How to report back

Keep the chat almost empty. The user is looking at an image, not reading a
report — everything they need is either in the picture or in one line under it.

**After the still**, say only this, then stop and wait:

> **Still ready.**
> *(show the image)*
> Happy with it, or change something?

Do not explain the prompt, list what you did, or describe the image back to
them. They can see it.

**Then propose the motion and stop again.** Do not animate on the strength of
the still being approved — the motion is the second decision and it is the one
that costs four minutes. Propose exactly one:

> **Motion** — *(one plain sentence: what actually happens, in physical terms)*
> `event` · `lively` · `--emit`
>
> Agree, or describe the motion you want?

One sentence and the flags. No reasoning, no alternatives, no explanation of
what the flags mean.

**If they describe their own motion, translate it.** They will use ordinary
words; your job is to turn those into the flags and one physical sentence, not
to pass their phrasing through. Work out:

- *what does this object do when left alone?* → `--strategy`
- *how much should the object itself move?* → `--energy`
- *would the action throw something off?* → `--emit`
- *what literally happens to the material?* → `--motion`

Then show the translated proposal in the same format and confirm before
running. If what they asked for is not supported — a camera move, something
entering the frame, the object travelling away — say so in one line and offer
the nearest thing that is.

`animate --dry-run` composes the full prompt and spends nothing. Use it if you
need to check what the flags expand to; do not paste the result into the chat.

**After the animation**, one line of numbers and the file:

> **Done** — `flame.webp` · 857 KB · 122f @ 24fps
> *(show the contact sheet)*

**If `verify` fails**, one line on what failed and one on what you propose:

> **Motion too weak** — step 0.9, needs 1.0.
> Retry as `event` with `--emit`?

**Never** paste raw CLI output, stage-by-stage progress, the composed motion
prompt, or a summary of the pipeline. If a stage succeeds, its output is the
file — say the filename and move on. Save the detail for when something breaks
and the user has to choose what to do next.

## The pipeline

```bash
python -m iconloop --out out still   --prompt "a 3D stopwatch, sage green and cream, soft matte plastic"
python -m iconloop --out out animate --motion "the stopwatch rocks gently while its hand sweeps clockwise"
python -m iconloop --out out matte
python -m iconloop --out out encode  --sweep
python -m iconloop --out out encode  --size 288 --name timer
python -m iconloop --out out verify
```

`run` is just `still` plus the reminder to stop and ask. The stages are
separate because each one is a place to look before spending the next thing.

## Choosing the motion

Before animating, answer one question: **what does this object do when left
alone?** The answer picks the strategy, and picking it wrong is the main cause
of a dull or generic result.

| answer | strategy | what you get |
|---|---|---|
| It moves by itself — flows, burns, breathes, ticks | `native` | continuous motion from its own physics |
| Nothing. It is inert until used | `event` | it performs its function once, then rests |
| Nothing, but part of it is loose, hinged or light | `part` | the body anchors, one small piece moves |
| Nothing, and it has no moving parts at all | `surface` | light or material travels across a fixed form |

Most objects people ask for are **inert**. Asking an inert object to move
naturally is what produces a turntable spin or an aimless bob — it has no
natural motion, so the model supplies a generic one. Reach for `event` first
unless the thing genuinely moves on its own.

Add `--emit` when the action would realistically throw something off — a
fragment, a droplet, a spark, a glint. For an inert object that emission is
often the entire reason the animation reads at icon size.

`event` and `part` also permit the object to be **temporarily altered** —
something removed, opened, split, filled — as long as it returns to its
opening state so the loop closes. Without that permission an object can only
ever jiggle.

## How much it moves

`--energy` decides whether the object itself moves, separately from what it is
doing. Body motion is not the enemy — aimless body motion is. A squash, a
recoil, a quick shake, an anticipation before an action: that is most of the
vocabulary that makes something feel alive, and forbidding it to avoid a
turntable spin throws away the whole language.

| energy | the object |
|---|---|
| `still` | holds completely rigid |
| `calm` | leans, settles, breathes a little |
| `lively` | squashes, tilts, recoils, shakes, springs back |
| `playful` | anticipates, overshoots, wobbles, hops in place |

Defaults follow the strategy — `native` and `event` get `lively`, `part` gets
`calm`, `surface` gets `still` — and an explicit `--energy` always wins. If a
result feels lifeless, raise it before changing anything else.

Only two things stay forbidden at every level: rotating as a whole, and
drifting. Everything else is available.

**Small and many beats large and one.** A single big motion of the whole object
is the obvious choice and the worst one: it risks the frame edge, it reads as
generic, and it says nothing about what the object is. Motion distributed over
the object's own details cannot leave the frame and is specific to that object
by construction. Where it has several of the same element, they must move out
of step with each other — unison is the loudest tell that something was
animated rather than observed.

**Everything that goes out comes back.** Anything that extends, rises, spreads
or is thrown off must retract, settle, be reabsorbed or fade. Stated as physics
rather than as a boundary, because a boundary is something the model can cross
without noticing — and a round trip is what the seamless loop needs anyway.

**Animate the effect, not its cause.** The commonest way a good result still
comes out wrong: the model reaches for whatever would normally *cause* the
motion, and that cause is usually the object being moved by something. The
physics ends up correct and the icon ends up bobbing, because at icon size the
cause is invisible and only the displacement reads. Describe the effect by
itself and let gravity, heat, air, tension or the object's own forces drive it.

Then say in `--motion` what the specific action is, in plain physical language.
Describe what happens to the material, not what the animation should feel like.

## Rules that matter

**Resolution is the quality lever, not the WebP quality setting.** Measured on
one icon: quality 50 to 90 cut colour error from 2.96 to 1.84 out of 255 and
added 500KB — nothing you can see. The visible loss is the downscale from a
1440px render. Defaults are now a 512px master and a 384px output; raise
`--size` before you touch `--quality`, and never above the master, which only
upscales.

**Encode at the source frame rate.** Kling returns 24fps. Sampling down to 8fps
to hit a size target is the single most common way to ruin one of these — it
produces judder that looks like a bad render, bad matting, or a bad player, and
is none of those. `--sweep` prints what each rate actually costs; choose with
the numbers in front of you. Smooth, slow motion suffers worst, so the icons
that most want animating are the ones a low frame rate hurts most.

**The last frame is set to the first frame.** That is what makes the model
return to its opening pose and the loop close. It is handled for you in
`kling.py` on both backends; do not remove it and try to cross-fade instead.

**Motion runs through OpenRouter on Seedance 2.0 by default.** `--model` picks
another — Seedance 2.5, Veo 3.1, Hailuo 3 and Wan 2.7 all accept a first and
last frame. Not Kling 3.0: it caps prompts at 2500 characters and the composed
motion clause is longer, so it rejects the request outright. `--via replicate`
is the fallback and stops at Kling 2.5.

**The backing colour is load-bearing.** The still is flattened onto a known
mid-grey before it is sent. Because the colour is known exactly, the matte
stage solves `C = (F - (1-a)*BG)/a` for the true foreground rather than
estimating it — measured, that cut edge colour error from 26.9 to 15.9. Do not
switch it to chroma-key green or magenta: those spill onto glossy edges.

**Believe the verifier, not the contact sheet.** A render can look animated in
stills and be almost entirely static — it has happened, 1 moving frame out of
121. `verify` measures motion inside the object and exits non-zero. If it says
the render is static, re-prompt; do not encode it.

**Never temporally smooth alpha.** It seems like the obvious anti-flicker move
and it smears a ghost ring around anything that moves.

## What it cannot do

See `docs/limitations.md`. The short version: the soft contact shadow does not
survive matting, file size scales with frame count, transparent MP4 needs an
x265 build most distros do not ship, and an animated WebP cannot honour
reduced-motion — ship the still alongside it.
