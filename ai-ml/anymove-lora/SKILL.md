---
name: anymove-lora
description: Train and use a MiniMax H3 image-to-video LoRA on fal that keeps anymove's two-camera layout - split screen held, limb colours kept, both views in step. Builds the dataset by re-rendering clean captured motions (and their mirrors) from both cameras, packs it, runs a cheap debug pass, trains, and A/B tests against plain H3 with the same seeds. Use when plain video models keep swapping limb colours or breaking the split screen for a creature, or when someone asks about @Graalitoo's LoRA step, its cost or its training data.
license: Apache-2.0
compatibility: Needs a fal.ai key (FAL_KEY), Blender 5.x, and a creature with several good captures (anymove-capture). Training runs on fal, not locally.
---

# anymove-lora: teach the video model the layout

Graalitoo's addition to the method: a LoRA on MiniMax H3 (open weights) so two-camera clips come out right more
often. fal hosts both the trainer (`minimax/h3/i2v/trainer`, $0.01 a step) and LoRA inference
(`minimax/h3/image-to-video/lora`, about $0.375 a 5 s clip, about 200 s each). No local GPU needed for this part.

## The data, and what it is

Each training clip is one motion the pipeline already captured cleanly (paw agreement 0.8 or more), re-rendered in
Blender from both layout cameras on the painted rig, composed into the two-camera frame, and captioned with the prompt
that produced it. Each is also mirrored left to right (left/right and colour words swapped in the action sentence), so
19 motions give 38 clips. Every clip comes from one 3D motion, so the two halves are in sync by construction. The
motion itself is AI-made: it was solved from AI clips. Real animal mocap exists (for dogs, AI4Animation's data) but
its licence is non-commercial; say which you're using.

## Steps

1. Capture 15-20 good moves (anymove-film, anymove-capture). Prompts live in `prompts/<c>/<move>.txt` or
   `prompts/<c>/train/<move>.txt`; the wolf has 14 training and 4 held-out moves already written.
2. Build the set (Blender renders each clip and its mirror, 5 at a time):
   ```bash
   MOCAP_CREATURE=assets/<c> .venv/bin/python tools/build_lora_set.py runs/<c>/lora/data trot_s1 howl_s1 ...
   ```
   Clip names are folders under `runs/<c>/clips/`; the move is the name up to its last `_`. It was built and tested on
   the wolf, whose rig is symmetric; mirroring an asymmetric rig (the dragon's wings) needs checking.
3. Pack, then a 1-step debug run ($0.01) to see what fal's preprocessing does (768 x 448, 107 frames at 24 fps):
   ```bash
   .venv/bin/python -m mocap.lora pack runs/<c>/lora/data runs/<c>/lora/data.zip
   .venv/bin/python -m mocap.lora train runs/<c>/lora/data.zip runs/<c>/lora/debug 1 --debug
   ```
   Open `runs/<c>/lora/debug/debug_dataset.zip` and check the frames still show both views whole.
4. Train. Say the cost first: 1,200 steps is about $12 and about 2 h (rank 32, lr 2e-4, trigger word `TWOCAM`).
   ```bash
   setsid .venv/bin/python -m mocap.lora train runs/<c>/lora/data.zip runs/<c>/lora/v1 1200 > runs/<c>/lora/v1.log 2>&1 &
   ```
   If the session drops, the run keeps going on fal: `python -m mocap.lora resume runs/<c>/lora/v1` re-attaches.
5. Generate with it (the trigger word is added for you):
   ```bash
   .venv/bin/python -m mocap.lora generate runs/<c>/lora/v1 runs/<c>/ref/ref.png prompts/<c>/pounce.txt runs/<c>/videos/pounce/lora.mp4 1.0 42
   ```
   The wolf's trained LoRA is in the examples release, so it can be tried without training (about $0.38 a clip);
   fal loads it straight from the release:
   ```bash
   tools/fetch_examples.sh wolf --clips
   .venv/bin/python -m mocap.lora generate \
     https://github.com/Patch-gg/anymove/releases/download/examples-v1/lora-wolf-twocam-h3.safetensors \
     runs/wolf/ref/ref.png prompts/wolf/heldout/pounce.txt runs/wolf/videos/pounce/lora.mp4 1.0 42
   ```
   `tools/fetch_examples.sh wolf --lora` downloads the file itself (131 MB), to run H3 with it yourself.
6. A/B test on held-out moves against plain H3 with the same seed, then capture both and compare paw agreement and
   reprojection error (anymove-capture).

## What it did for the wolf (one seed per move: a first read, not a benchmark)

| move | plain H3 | H3 + LoRA |
|---|---|---|
| trot (in training set) | colours swapped, paws 0.15, fit 20.5 px | colours kept, paws 0.48, fit 6.0 px |
| gallop | colours swapped, fit 44 px | colours kept, paws -0.06, fit 21.6 px |
| pounce | one paw moves (-0.65), fit 6.0 px | all four move, paws 0.80, fit 6.2 px |
| dig | paws 0.75, fit 5.6 px | paws 0.87, fit 4.8 px |
| shake | paws 0.70, fit 9.1 px | paws 0.69, fit 6.9 px |

Plain H3 broke the colour code on 2 of 5 clips, the LoRA on 0 of 5. Sync improved on trot, pounce and dig, not on the
gallop. MiniMax H3's open weights carry a community licence (its page asks US, EU, UK and South Korea users to apply);
hosted use on fal goes through fal's terms. Check both before shipping anything made with it.
