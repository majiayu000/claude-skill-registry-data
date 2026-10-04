---
name: h3-game-sprites
description: Build 2D game sprite sheets by generating motion with MiniMax H3 (Hailuo) video, then cutting the footage into validated chroma-keyed sprite frames - the Mortal Kombat method with a video model instead of filmed actors. Covers the character-still recipe, the idle-pin trick that keeps every move on-model and loopable, per-move clip briefs, frame extraction with keying and numeric QC, seamless walk-cycle detection, and the atlas/render math that keeps a character planted and correctly sized in an engine. Use this whenever the user wants game sprites, a sprite sheet, an animated 2D game character, a fighting/platformer/beat-em-up character, wants to turn AI video into game animation frames, or wants a character animated for a game - even if they never say H3, Hailuo, or "sprite". Also use it for chroma-keying generated video to transparent frames, choosing keyframes from footage, and debugging sprites that jitter, float, sink, or change size between animations.
license: MIT
compatibility: Requires ffmpeg, Python 3 with Pillow and numpy, and an OPENROUTER_API_KEY with credit for video and image generation.
---

# H3 → Game Sprites

Mortal Kombat filmed actors and digitized the footage into sprites. Do the same
with H3 as the actor: one 5 s clip per move (~$0.64), cut down to 8–16 pose
extremes, keyed to transparency, validated with numbers rather than vibes.

Read the **`h3-video`** skill for H3 API mechanics (submitting, polling, frame
pinning, the parallel runner). This skill is the sprite layer on top of it.

## Why a 5-second clip becomes a quarter-second move

The video is source footage, not gameplay. 5 s at 24 fps is ~120 frames; a game
move needs 8–16. H3's slow, deliberate performance is an advantage — more
in-betweens to choose from, less blur per frame. Game timing (startup, active,
recovery) is authored separately in frame data and never inherited from the clip.

## 1. The character still

Generate with `scripts/gen_still.py` (Nano Banana, ~$0.07, `--batch` for parallel
style probes). The prompt must nail four things:

- **Side view facing right, full body including feet, centered, feet planted on
  an invisible ground line.** Cropped feet make a character you cannot anchor.
- **Flat solid magenta `#FF00FF`, edge to edge, no gradient, no cast shadow, no
  ground line.** This is your chroma key.
- **Clean cel: no film grain, no dust, no scratches, no paper texture, no
  vignette.** Beautiful grain destroys the key — say so explicitly, because
  style prompts tend to add it.
- Bold outlines and flat fills survive downscaling to sprite size.

Style choice is a motion question, not a taste question: some styles H3 simply
won't animate. Probe several looks, then spend one clip motion-testing the
finalist before committing to a full move set. Ink wash, claymation, rubber-hose
and photoreal move well; flat vector and paper cutouts risk freezing.

Extra end-pose stills (KO, downed) are generated from the idle as a reference
image. Say **"EXACTLY ONE character, completely alone, no second figure, no
duplicate"** — asking for "knocked out" while showing a standing reference
reliably returns both a standing and a lying character in one frame.

## 2. Clip briefs, one per move

**The idle pin.** Every move clip sets `first_frame = last_frame = the idle
still`. This buys three things at once: the character cannot drift off-model
(H3 keeps identity only when it is anchored in a locked frame), the animation
returns exactly to neutral so it loops, and moves chain cleanly in a state
machine. Moves that end elsewhere (KO) pin their own end frame instead.

Use the beat structure from `h3-video`, plus these sprite-specific guards —
each one was learned by getting the opposite:

```
The character's hands and feet stay their normal size at all times - NO
ballooning, NO growing fists; limbs may stretch but hands and feet keep
constant scale.
Camera locked on a tripod, no zoom, no pan, no cut.
The background stays a perfectly flat uniform solid magenta at all times - no
gradient, no cast shadow, no ground line, nothing else enters the frame.
The character stays centered on the same ground level and does not travel
across the frame; everything not described stays static.
Audio: SFX only. NEVER generate music, melody, score or musical tones.
```

- **Walks are briefed in place** ("as if on a treadmill") — the engine moves the
  transform, so a sprite that travels fights the engine.
- Hit-stun and KO react to "an invisible blow", since no opponent is in frame.
- Cartoon models love exaggeration. Unforbidden, fists balloon on impact frames.

A basic set — idle, walk forward, walk back, jump, crouch, punch, kick, block,
hit-stun, KO — is ~$6.50 and submits as one parallel batch. Consider skipping
the back-walk clip and playing the forward cycle in reverse (a classic 2D
fighter trick): asked for a backward stride, H3 tends to give a wary sway.

## 3. Decompose and validate

```bash
python3 scripts/sprite_cut.py clips/v_punch.mp4 sprites/punch --frames 12
python3 scripts/sprite_cut.py clips/v_walk.mp4  sprites/walk  --frames 8 --loop
```

Writes `keyed/*.png` (RGBA), `strip.png`, `anim.gif` (pose preview at source
pacing) and `report.json`.

**Keyframes are picked by cumulative motion arc-length** — equal steps of
accumulated frame-to-frame change, so frames concentrate where the action is.
Uniform sampling looks mushy, and picking local motion maxima over-samples the
idle bounce at the head of the clip.

**`--loop` for cycles.** Whole-clip picks include the start-up and the settle
back to idle, which is exactly why a walk visibly resets instead of looping.
Loop mode finds the closest-matching frame pair inside the sustained middle of
the clip and samples between them, giving a true seam.

Read the summary before trusting anything:

| metric | what it tells you |
|---|---|
| `worst_bg_purity` | ~1.0 means every pixel is confidently background or character; lower means key leak |
| `loop_diff` | move returns to its start pose (or, in loop mode, the cycle seam) |
| `first_vs_last_baseline` | feet end where they began, in px |
| `baseline_drift_px` | feet wandering — large is right for a jump, suspicious for a stance |

Despill note: do not blend the fringe toward the off-channel, which visibly
tints the character. Clamp the key channels against the off-channel instead, as
the script does.

## 4. Atlas: one global scale

**The trap.** Scaling each frame to a fixed on-screen height is the obvious
thing and it is wrong: a crouch or jump tuck has a *smaller* bounding box, so
per-frame normalization renders it **bigger** than standing. Derive one scale
from the idle frame and apply it to every frame of every move.

```bash
python3 scripts/build_atlas.py sprites/ atlas.json \
    --moves idle,walk,jump,crouch,punch,kick,block --ref idle --height 340
```

Frames are stored trimmed, at global scale, with offsets to a shared anchor:
`footOffset` (feet vs the ground line), `anchorOffset` (stance-center column
inside the crop), `driftX` (this frame's drift from the canonical center).

**The anchor X comes from the ankle-region centroid, not the bbox center** — a
big arm or tail swing moves the bbox, and centering on it makes the character
slide sideways between poses.

The script prints per-move on-screen heights. Crouch and jump-tuck must be
*shorter* than idle; if they are taller, per-frame scaling has crept back in.

## 5. Render

```js
ctx.translate(x + f.driftX, GROUND_Y + jumpY);
ctx.scale(facing, 1);              // player 2 is a flip, never a generative mirror
const foot = state === 'jump' ? 0 : f.footOffset;   // engine arc supplies the lift
ctx.drawImage(img, -f.anchorOffset, foot - img.height, f.w, f.h);
```

Two real bugs live in those four lines. `drawImage`'s y is the **top** edge
while `footOffset` positions the **feet**, so dropping `- img.height` sinks the
character through the floor. And if the engine authors a jump arc, adding the
frame's baked-in air offset on top double-lifts it.

Frame data stays separate from pixels — durations per frame, a loop flag, and
for held states an enter/hold/release split so a key can be held:

```js
punch:  { frames:[0..11], durations:[35,35,45,50,...], loop:false }
crouch: { enterFrames:[0,1,2], holdFrame:3, releaseFrames:[4..7], hold:true }
```

Roughly 35–70 ms per frame for attacks (fast startup, slower recovery) against
~150 ms for idle. Tune feel here; never regenerate video for timing.

## 6. Verify with pixels, in a browser

Asserting on atlas metadata is not verification — it passes happily while the
render is broken. Measure the character on the actual canvas:

```js
// drive the loop deterministically: requestAnimationFrame freezes in unfocused tabs
const drive = (n, codes) => {
  for (const c in keys) delete keys[c];
  for (const c of codes) keys[c] = true;
  for (let i = 0; i < n; i++) tick(g, keys, 16.7);
  draw();
};
// then getImageData, find the non-background bbox, compare against GROUND_Y
```

Confirm: idle feet sit on the ground line, crouch is shorter *and still
planted*, jump lifts without resizing, landing returns to exactly idle.

Chrome extensions cannot open `file://` URLs — serve the page with
`python3 -m http.server` and drive localhost.

## Costs and habits

Still ~$0.07, 5 s clip $0.64, a 10-move fighter ~$7, failed jobs free. Retakes
are per-move, never the whole set, so diagnose before rerolling: a wrong-looking
character means the locked frames were wrong, not the prompt. Keep superseded
assets rather than deleting them — an earlier take is often the only surviving
copy of a pose you end up wanting back.
