---
name: create-gif
description: Produce consistent pixel-art character animations (idle/walk sprite sheets) and preview GIFs from the local create-image pipeline. Use when asked to animate a game character, build a sprite sheet with multiple poses/frames, or make a GIF of a sprite or an in-engine animation. Covers identity-consistent multi-frame generation, semantic matting, figure splitting, sheet assembly, and both sprite-frame and in-engine GIF capture.
---

# Create GIF — character animation & preview GIFs

Turn the local `create-image` pixel pipeline into **animation frames** and **GIF previews**. The hard part is not drawing — it is keeping the character's identity from morphing between frames, and showing motion that is often too subtle to see. This skill is the distilled know-how.

## The core trick: generate every frame in ONE image

Identity consistency does **not** come from a reference image, img2img, or a fixed seed. It comes from drawing **all the poses/frames inside a single generation** — one canvas keeps one character coherent. Generating frames as separate images morphs the face/outfit every time (and matching the seed does not help, because a different prompt = a different image).

```bash
cd /home/chihmin/models-work/flux2 && source .venv-rocm72/bin/activate
FLUX2_BIG_WMMA_LINEAR=1 python ~/.hermes/skills/create-image/scripts/create_image.py \
  "pixel art chibi character sprite sheet in 二次元像素風 style, EXACTLY THREE large full-body figures of the very same <CHARACTER DESIGN>, arranged in ONE single horizontal row, wide even spacing, identical hair outfit and colors in every pose, front view, pure solid white background, <PER-POSE ACTIONS>, no grid, no extra copies, not more than three figures, no text" \
  --anime --aspect-ratio 16:9
```

Key points:
- **`二次元像素風`** triggers the chibi Elin pixel-sprite LoRA (matches the game's map sprites). Drop it and use plain `--anime` for detailed (non-chibi) art.
- **Pin the design in the prompt** (hair colour/length, outfit, palette, props) so all figures share identity.
- **Constrain count + layout hard.** The model loves to make grids or extra duplicates. Spell out `EXACTLY THREE … ONE single horizontal row … no grid … no extra copies … not more than three figures`. If it still misfires (5–6 tiny figures, 2 rows), just regenerate — that is what the **seed** is for (a reroll knob, recorded in the output `timing.json`), not consistency.
- Use `--aspect-ratio 16:9` for a row of 3; widen for more frames.

## Matting: pick the right model

- **Characters → `isnet-anime`** (anime-person segmentation).
- **Objects / props → `birefnet-general`** — `isnet-anime` erases inanimate objects to nothing.

```bash
uv tool run --python 3.13 --with 'numba>=0.61' --from 'rembg[cpu,cli]>=2.0.70' \
  rembg i -m isnet-anime  in.png out.png    # characters
uv tool run --python 3.13 --with 'numba>=0.61' --from 'rembg[cpu,cli]>=2.0.70' \
  rembg i -m birefnet-general in.png out.png # objects
```

Never derive alpha from white/colour thresholds — always a semantic model.

## Split the multi-figure sheet into frames

Segment figures by **transparent vertical gaps** (column alpha projection), not fixed thirds — this survives uneven spacing. Keep the widest N segments, crop each to its bbox.

```python
import numpy as np
def split_figures(im, keep=3):
    a = np.array(im)[:, :, 3]
    colmask = (a > 24).sum(axis=0) > 2
    segs, run = [], None
    for x, on in enumerate(colmask):
        if on and run is None: run = [x, x]
        elif on: run[1] = x
        elif run is not None: segs.append(run); run = None
    if run is not None: segs.append(run)
    merged = []
    for s in segs:                       # merge gaps < 8px
        if merged and s[0]-merged[-1][1] < 8: merged[-1][1] = s[1]
        else: merged.append(list(s))
    merged = [s for s in merged if s[1]-s[0] > 20]
    merged.sort(key=lambda s: s[1]-s[0], reverse=True)
    merged = sorted(merged[:keep], key=lambda s: s[0])   # widest N, left→right
    return [im.crop((s[0],0,s[1]+1,im.height)).crop(im.crop((s[0],0,s[1]+1,im.height)).getbbox()) for s in merged]
```

## Assemble a runtime sprite sheet

Two rules keep the animation from jittering:
1. **One shared scale factor** for all frames of a character — base it on the resting/standing frame's height, then clamp so the widest/tallest frame still fits the cell budget. Never scale each frame to fill its cell independently (the body would grow/shrink).
2. **Feet-baseline alignment** — align every frame's bbox **bottom** to a common baseline `y` so the character never bobs its feet.

```python
FW, FH, TARGET_H, BASE_Y = 96, 128, 112, 123   # cell + resting height + feet line
h0 = figs[0].height; scale = TARGET_H/h0
maxw, maxh = max(f.width for f in figs), max(f.height for f in figs)
scale = min(scale, (FW-6)/maxw, (FH-3)/maxh)
sheet = Image.new('RGBA', (FW*len(figs), FH), (0,0,0,0))
for i, f in enumerate(figs):
    nw, nh = round(f.width*scale), round(f.height*scale)
    fr = f.resize((nw, nh), Image.LANCZOS)
    sheet.alpha_composite(fr, (i*FW + (FW-nw)//2, BASE_Y-nh))
```

Match the game's existing sheet dimensions exactly (e.g. this project's NPC idle = `288×128`, 3×`96×128`; hero walk = `288×512`, 3 cols × 4 rows) so the swap is drop-in and needs no engine change. Verify a matte over a checkerboard — no white box, colour fringe, neighbouring-figure fragment, or clipped limbs.

## Making the GIF

**Case A — the animation lives in the frames** (pose swaps, walk cycles): build the GIF straight from the sprite frames.

```python
frames=[Image.open(...).convert('P',palette=Image.ADAPTIVE) for ...]
frames[0].save('out.gif', save_all=True, append_images=frames[1:], duration=150, loop=0, disposal=2)
```

**Case B — the animation is procedural** (breathing, sway, scaling, shader/transform done in-engine): a sprite-frame GIF shows nothing. You **must capture the running app** frame by frame with headless Chrome, then assemble.

```js
// puppeteer-core: /home/chihmin/src/LazyGravity/node_modules/puppeteer-core
const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome-stable',headless:'new',
  args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const p=await b.newPage(); await p.setViewport({width:1400,height:646,deviceScaleFactor:1});
await p.goto(url,{waitUntil:'networkidle2'}); await new Promise(r=>setTimeout(r,3800)); // let assets load
for(let i=0;i<18;i++){ await p.screenshot({path:`f${i}.png`}); await new Promise(r=>setTimeout(r,150)); }
```

Then **crop to the subject and upscale (Image.NEAREST)** before making the GIF — subtle motion (a ~2% breathing) is invisible at full-frame but reads once zoomed 2–3×. Confirm motion objectively with a pixel diff between frames (`ImageChops.difference(...).mean()` should be clearly > 0); don't ship a GIF you haven't verified actually moves.

## Animation gotchas (learned the hard way)

- **Static NPCs?** Check the engine actually cycles frames each render tick — a one-time `setSpriteFrame` leaves them frozen no matter how many frames the sheet has.
- **Framerate independence:** drive animation timing from **wall-clock** (`performance.now()/1000`), not an accumulated `dt` that is capped for movement stability — a capped dt makes the clock lag at low FPS.
- **Feet planted while scaling:** when you breathe a billboard with `scaling.y`, compensate `position.y = baseCenterY * scaling.y` so the bottom edge stays fixed.
- **Desync** identical loopers with a per-instance phase so a crowd doesn't move in lockstep.
- **Keep idles subtle** unless asked — a held pose + gentle breathing/cloth sway usually reads better than swapping big poses.

## Checklist

1. One-image multi-pose/frame generation with the design pinned + count/layout constrained.
2. Matte (`isnet-anime` characters / `birefnet-general` objects).
3. Split by transparent gaps → crop.
4. Assemble with one shared scale + feet baseline into the game's exact sheet dims.
5. GIF from frames (Case A) or from in-engine capture, zoomed (Case B) — verify it moves.
