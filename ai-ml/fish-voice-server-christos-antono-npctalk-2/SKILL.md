---
name: fish-voice-server
description: Host Fish Audio's open-weights voice models (Drama 3 and S2 Pro) on a serverless GPU (Modal, or fal) behind one small HTTP API a game can call. POST /speak takes text and a voice and streams 16-bit PCM back with first audio in ~0.4 s, cloned zero-shot from a reference clip, with [tags] like [angry] or [laughing] for delivery. Covers deploying with SGLang-Omni, the API, preparing voices at startup, keep-warm and cold starts, scaling to zero and cost, sampling settings that measurably help likeness, picking the best of several takes for pre-rendered lines, an optional S2 Pro fine-tune, and the setup gotchas. Use when a game, mod or app needs realtime cloned character voices, the user mentions Fish Audio, Fish Speech, S2 Pro, Drama 3 or a self-hosted TTS server, or a voice server is slow, cold or failing.
---

# A Fish Audio voice server for games

`server/drama3.py` (default) and `server/s2pro.py` are Modal apps with the same API, so a game switches models by
changing one URL. Both run Fish Audio's open weights through SGLang-Omni on one H100 and stream audio as it's
generated.

## Pick the model
| | **Drama 3** (`fishaudio/drama-3`) | **S2 Pro** (`fishaudio/s2-pro`) |
|---|---|---|
| Size | 35B mixture of experts, 3B active, FP8 (~37 GB) | Smaller; leaves room for fine-tuned voices on the same GPU |
| First audio from a PC | ~0.33-0.5 s warm | ~0.5 s warm |
| Acting `[tags]` | Better (crying, laughing, whispering) | Good |
| Voice likeness, zero-shot (Lamar, below) | 0.643 at defaults, 0.660 tuned, **0.704 best of 8** | 0.680 with the same clip, 0.707 with its best clip |
| Fine-tuning | Not done here | LoRA in `server/finetune/` (**0.785**, the best result, but it needs training) |

## Deploy (Modal)
```bash
uv tool install modal && modal setup
modal secret create npcvoice-auth NPCVOICE_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
modal run server/drama3.py::download_weights        # once: ~40 GB into the npcvoice-models volume
npctalk voice make --name Narrator --audio narrator.wav && npctalk voice upload voices/Narrator
modal deploy server/drama3.py                       # prints https://<workspace>--npcvoice-drama.modal.run
export NPCVOICE_URL=https://<workspace>--npcvoice-drama.modal.run NPCVOICE_TOKEN=<the token>
npctalk health                                      # waits through a cold start (1-3 min)
npctalk say "[laughing] Nah, you trippin'." --voice Narrator/clone --out test.wav
```
Everything is named `npcvoice-*` (apps, volumes, secrets) so it stays apart from the rest of a Modal workspace.
Keep the URL private: `/health` needs no token and wakes the GPU.

## The API
```
POST /speak    Authorization: Bearer <NPCVOICE_TOKEN>
  {"text": "[angry] Get out of my face!", "voice": "Trevor/clone"}            a voice prepared on the server
  {"text": "...", "reference_audio_url": "https://.../me.wav", "reference_text": "what me.wav says"}
  optional: "temperature", "top_p", "multi" (all clips in the voice's folder), "best_of" (1-8, drama3.py)
→ 200, X-Sample-Rate: 44100, body: 16-bit mono PCM, streamed as it's generated
  (with best_of > 1: the whole line at once, and X-Takes: per-take likeness / word error / length)
GET /health    no auth → {"ok": true, "model": "drama-3", "voices": 21}
```
- **Voices** live in the volume at `/voices/<Name>/clone.wav` + `clone.lab` (transcript), plus `ref_0..2` and mood
  folders (`/voices/<Name>/angry/ref_0.wav`). The server encodes every clip when it starts, so a named voice
  costs nothing per request; a clip sent by URL costs ~9 s the first time. Restart the server after uploading
  voices (`modal app stop npcvoice-drama`).
- **Tags** go where they happen in the text: `"[sigh] Man... [laughing] nah."`. Drama 3 and S2 Pro both voice
  them; other engines treat them as hints.
- **Client:** `examples/gta-v/mod/Tts.cs` (`ModalTts`, C#) and `npctalk/server.py` (Python) both read the stream
  in 4 KB chunks and start playing at the first chunk.

## Settings that were measured (Lamar, 10 lines, voice match = ECAPA similarity to 60 real clips)
| Change | Result |
|---|---|
| Sampling `temperature 0.7, top_p 0.8` instead of Drama 3's defaults (1.0 / 0.9) | 0.660 (10 runs) vs 0.643, better on 8 of 10 lines (t = 2.5) |
| Temperature 0.5 or 0.3 | Worse (0.609, 0.628) and more rambling takes |
| The ~30 s `clone.wav` vs one 6-10 s clip | 0.680 vs 0.610-0.630: clone the long clip |
| All four clips as references at once | No better (0.641 vs 0.637) |
| **`best_of: 8`** with checks (below) | **0.704** vs 0.660 for one take, better on 9 of 10 lines (t = 3.9) |

So `SAMPLING = {"temperature": 0.7, "top_p": 0.8}` is the server default, and pre-rendered lines use best of 8.

## best_of: for lines made ahead
About 1 take in 10 rambles to the token limit (47.6 s for a 15-word line) or trails off into noises. For lines
that don't need streaming (cutscenes, a director's clips) `best_of: N` renders N takes in one batch and:
1. stops each take just past the longest the words could take (`1.5 + 0.45 s per word`, + 1 s);
2. drops takes that are too long or that a small ASR (Whisper base, on the GPU) can't hear the line in
   (word error above the clearest take's + 0.1, or above 0.5);
3. keeps the one most like the reference by ECAPA plus WavLM similarity, each scaled across the takes.

Picking by one model alone over-fits it: WavLM-only picks scored 0.692 at 4 takes; ECAPA-only raised ECAPA a lot
but WavLM less; both together kept most of each. An unchecked pick scored 0.708 but let a 14-second whimper
through. Best of 8 takes ~4-6 s per line with the scoring models on the GPU.

## Keep-warm, cold starts, cost
- `MIN_CONTAINERS = 0`, `SCALEDOWN = 300`: the H100 (about $4/hour) stops 5 minutes after the last request; the
  next request waits 1-3 minutes (weights load, kernels warm up, every voice is encoded).
- A game should ping while it runs (the GTA mod sends a one-word line every 90 s of silence) and fall back to
  a no-GPU engine (MiniMax on fal) while the GPU wakes.
- For a demo without the game: `modal deploy server/keepwarm.py`, then
  `modal run server/keepwarm.py --url $NPCVOICE_URL --hours 12` (it says what that costs: ~$45-50).

## Fine-tuning S2 Pro (optional, needs training)
`server/finetune/`: `prepare_dataset.py` (Demucs → Whisper word timings → 2-15 s clips → speaker filter →
loudness), `train.py` (LoRA r8, α16, lr 1e-4; step 250 was best), `fish_finetune.py` (two fixes fish-speech
needed for S2 Pro). Read `references/finetune.md` before starting.

Gotchas for all of this: `references/gotchas.md`.
