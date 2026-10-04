---
name: clean-audio
description: Voice/audio cleanup step of the AI Video Editor pipeline — diagnose a video's background noise, pick the right denoise method, and produce a cleaned master (voice isolated, levels preserved, video stream copied). Use when the user wants to "clean the audio / voice", "remove background noise", "denoise", "isolate voice", fix outdoor/room/water/hum/hiss noise, run ElevenLabs Voice Isolator or local RNNoise, A/B denoise methods, or produce a cleaned master for a video-N in this repo. Covers diagnosing the noise (spectrogram + levels), choosing eleven vs rnnoise by noise type, the sample A/B, tools/clean_voice.py, preserving levels (RMS-match, not LUFS), and rewiring the pipeline to the clean master. Not the SFX/music mix (that is /suggest-sfx + the final-mix step) and not the cut (that is /clean-cut).
---

# clean-audio — voice cleanup

Take a locked master cut and remove its background noise, producing a **cleaned master** whose voice
sounds natural and whose visuals are untouched. Runs early (once the cut is locked) so everything
downstream — TSX bake, SFX mix, final assemble — sits on the clean voice. Work with the user; the
final loudness/limiting is the final-mix step's job, this step is "denoise only, levels preserved."

The engine is **`tools/clean_voice.py`**; this skill is the judgment around it: diagnose → pick method
→ A/B → clean → rewire.

## The two methods (pick by NOISE TYPE — this is the core decision)

| Method | What it is | Use when | Cost |
|---|---|---|---|
| **`--method eleven`** | ElevenLabs Voice Isolator (cloud ML voice/noise separation) | **Dynamic, broadband noise in the voice band** — outdoor running water, wind, traffic, crowd, cafe. Local tools CANNOT remove these. | ~1000 credits/min (~$1 for a 5.5-min video); needs `ELEVENLABS_API_KEY` |
| **`--method rnnoise --model sh`** (or `cb`) | Local RNNoise via ffmpeg `arnndn` (models in `tools/models/rnnoise/`) | **Stationary / mild** noise (steady hiss, fan, some room tone). Free/offline. Only PARTIALLY removes dynamic noise. | free |

Proven on video-1 (shot outdoors with a stream): `afftdn` did ~nothing, RNNoise only partially darkened
the water bed, **ElevenLabs removed it near-completely** (pauses to near-silence, voice + breaths intact).
Rule of thumb: **stationary noise → try local first; dynamic broadband (water/wind/traffic) → ElevenLabs.**

## Inputs (read/measure first, every time)

- **The master** — `videos/video-N/reference/<cut>.mp4` (or the locked cut). Original is NEVER modified;
  output is a new `-clean` / `-clean-<model>` file.
- **The composited preview** (if it exists) — `videos/video-N/output/video-N-preview.mp4`, to make a clean
  in-context preview by swapping audio (its video is identical — no re-bake needed).
- **`videos/video-N/work/timeline.json`** — its `master` field; you rewire this to the clean master on approval.

## Workflow

1. **Diagnose the noise BEFORE choosing a method.** Measure and look:
   - Levels: `ffmpeg -i M -vn -af astats` (RMS, peak, noise floor) + `ebur128` (integrated LUFS, true peak).
   - Find speech-free gaps (grep `edited-transcript.json` for the biggest inter-word gaps) and measure
     the pure-noise RMS there vs speech RMS → the real SNR.
   - Spectrogram: `ffmpeg -i M -vn -lavfi showspectrumpic=s=1500x600:legend=1:scale=log out.png` and
     LOOK at it. Hum = steady horizontal lines (50/60Hz) → notch. Rumble = low band → high-pass. Broadband
     bed that fills the voice band and fluctuates = dynamic (water/wind) → ElevenLabs. HF hiss = bright top band.
   - Note if the export is already produced (compressed/normalized/peak-maxed) — it limits what's recoverable.
2. **Decide the method with the user** from the diagnosis (table above). If unsure, A/B both.
3. **A/B on a short sample FIRST** (prove before spending / committing): cut a ~15s pause-rich sample,
   run each candidate method, level-match them to each other, and compare — by ear (the real test) AND by
   spectrogram (pauses going dark = noise removed) and residual level. Let the user pick.
4. **Clean the full master:** `python tools/clean_voice.py videos/video-N/reference/<cut>.mp4 --method <chosen> [--model sh]`
   → `<cut>-clean.mp4` (or `-clean-<model>.mp4`). Video stream COPIED (fast, non-destructive, keeps 4K60).
5. **Levels are preserved by RMS-match, not LUFS** (the tool does this). Never match integrated LUFS —
   it is gated and inflated by the removed noise, and over-boosts the voice into clipping. The clean file
   will read a lower integrated LUFS than the noisy original; that is expected (the noise was padding the
   number), the voice RMS is unchanged. Final loudness to -14 LUFS is the final-mix step's job.
6. **Give the user an in-context preview** (optional but recommended): swap the clean audio onto the
   composited preview — `ffmpeg -i preview.mp4 -i <cut>-clean.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -shortest preview-clean.mp4`
   (video identical, no re-bake). For a full A/B, also export `FULL_*.mp3` scrub files.
7. **On approval, rewire the pipeline:** point `timeline.json` `"master"` at the clean file so every future
   bake/mix uses the clean voice; re-bake the preview if needed.

## Decisions to surface to the user

- **Method** (from the diagnosis) — and A/B if unsure.
- **Dead-silent gaps vs a faint ambience bed.** Voice isolation removes ALL background; on an outdoor shot
  the dead-silent gaps can feel vacuum-sealed. Offer to add back a low-level neutral ambience if wanted.
- **Cost** for ElevenLabs (~1000 credits/min) — confirm before running on the full master.

## Principles (the house style)

- **Least processing that works.** The goal is to remove distraction, not to make the voice sound
  processed. Prefer the gentlest method that clears the noise; don't over-strip a clean track.
- **Diagnose, then choose.** The right tool depends on the noise type — never crank a denoiser blind.
  Local spectral/RNNoise can't separate dynamic broadband noise; that's ElevenLabs' job.
- **A/B before you commit** (and before you spend). Prove on a sample; the user's ears decide.
- **Preserve levels; loudness is the final-mix step's.** RMS-match with a peak ceiling, no compression here.
- **Non-destructive.** Original master untouched; video stream copied; output is a new file.

## Tooling quick reference

- Clean: `python tools/clean_voice.py IN.mp4 [--method eleven|rnnoise] [--model sh|cb] [-o OUT.mp4] [--no-preserve-loudness] [--keep]`
- Diagnose: `ffmpeg -i M -vn -af astats -f null -` · `ffmpeg -i M -vn -lavfi showspectrumpic=... out.png` (then Read the png).
- RNNoise models: `tools/models/rnnoise/<model>.rnnn` (`sh`, `cb`).
- Scratch samples/spectrograms go in the scratchpad, not the project.

Done = the noise is diagnosed, the method is chosen (A/B'd if needed), the full master is cleaned with
levels preserved, the user has approved by ear, and — on approval — `timeline.json` points at the clean
master. Update memory if a noise-type → method lesson emerges.
