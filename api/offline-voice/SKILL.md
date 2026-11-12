---
name: offline-voice
description: How the on-device narration engine (VieNeu-TTS) and voice cloning work in this system - install tiers, the worker protocol, and the verified traps around torchaudio, voice metadata parsing and duration. Read when working on Text to video narration, the Voices page, the /api/voices or /api/tts endpoints, or when a user reports that offline voices or voice cloning fail to install or sound wrong.
---

# Offline voice - VieNeu-TTS and voice cloning

The system has **two narration engines running side by side**. They are deliberately not merged.

| | `gemini` | `vieneu` |
|---|---|---|
| Where it runs | Google API | The user's own machine |
| Cost | Per call | Free |
| Needs network | Yes | No |
| Voices | 30 preset | 14 Vietnamese preset + unlimited cloned |
| Voice cloning | **No** (API only accepts preset names) | **Yes** |
| Speed | A few seconds | RTF ~1.0 (about real time) |
| Setup | `GEMINI_API_KEY` | `pip install vieneu` |

Keep both. Do not "simplify" by deleting one: a weak machine reads at roughly real time, which is unacceptable for a long script, while Gemini costs money on every preview click.

## Why VieNeu and not F5-TTS / XTTS / Chatterbox

Checked against the requirement "Vietnamese + English, cloning, and shippable in an open-source repo":

- **Chatterbox** (MIT, excellent English) has **no Vietnamese**. Disqualified on language.
- **F5-TTS** code is MIT but the **weights are CC-BY-NC**, and every Vietnamese finetune is CC-BY-NC-SA. Disqualified on licence.
- **viXTTS / XTTS-v2** inherit Coqui's CPML non-commercial licence. Disqualified on licence.
- **VietTTS** (dangvansam) is Apache-2.0 code but the installer is Linux-only, and its weights are CC-BY-NC too.
- **VieNeu-TTS** is Apache 2.0 on the code and on the **v3 Turbo weights** (`pnnbao-ump/VieNeu-TTS-v3-Turbo`, trained from scratch on ~10k hours, not a finetune), plus Apache 2.0 on its codec dependency `OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano`. Vietnamese-first with English code-switching, torch-free on CPU via ONNX, clones from 3-8 seconds of reference audio.

If a future engine is evaluated, check the **weights** licence separately from the code licence. That is where every other candidate failed.

**Licence trap inside the package itself.** `vieneu/assets/voices.json` carries `"license": "CC BY-NC 4.0"` and `"Model and voices are for non-commercial use only"`. That notice is scoped to **that file**, which is the **v2** preset pack: 6 voices named `Binh, Tuyen, Vinh, Doan, Ly, Ngoc`, default `Binh`. We run `mode="v3turbo"`, which reads `voices_v3_turbo.json` (14 Vietnamese voices, default `Phạm Tuyên`). The two sets have **zero overlap** - verified by comparing the key sets - so nothing on our path is NC-licensed. If anyone ever switches the engine mode away from `v3turbo`, or a preset named `Binh`/`Tuyen`/`Vinh`/`Doan`/`Ly`/`Ngoc` shows up in the picker, the commercial position changes and must be rechecked.

## Install tiers - keep them separate

Two independent levels. Never collapse them into one check:

1. **Speech only**: `pip install vieneu`. Torch-free (ONNX Runtime), ~30 MB of wheels. This is enough for all 14 preset voices.
2. **Cloning**: additionally `pip install torch torchaudio`, 2-3 GB.

`start/doctor.mjs` reports these as `vieneu` and `vieneu-clone`, and only asks about torch once `vieneu` is present. Forcing a 2-3 GB torch download on someone who only wants offline narration is the mistake to avoid.

The first synthesis after a server start downloads ~1 GB of model from HuggingFace and takes 30s; subsequent process starts take ~15s to load. Always surface this in the UI, otherwise the first click looks like a hang.

## Known issues

**Symptom:** every transcription (video projects, Text to video, narration) fails with `TypeError: open() got an unexpected keyword argument 'metadata_errors'` from `faster_whisper/audio.py`.
**Cause:** PyAV 17+ dropped `metadata_errors`, but faster-whisper 1.2.x still passes it to `av.open()` (verified 2026-10: `av` 19.0.1 + `faster-whisper` 1.2.1). An unpinned `pip install faster-whisper` pulls the newest `av`.
**Fix:** `.runtime/venv/Scripts/python.exe -m pip install "av>=11,<17"` (16.1.0 verified). `start/doctor.mjs` now pins it in the faster-whisper fix, but a venv that already has av 19 must be downgraded by hand - the doctor's probe only checks `import faster_whisper`, which still succeeds.

**Symptom:** every VieNeu call (narration, Text to video, voice preview) returns `503 LOAD_FAILED` for the rest of the server's life, yet the same Python loads `Vieneu()` and synthesizes fine from the command line.
**Cause:** one failed model load (seen once as `External data path escapes model directory` while the ~1GB model was still being fetched on first use) set `loadFailure` in `ttsLocal.ts`. That flag overrode every later probe, and the only way to clear it was `probeLocalEngine(true)` - which no route called. An agent mid-edit had no way out but asking the user to restart the backend.
**Fix:** the flag now expires after 2 minutes (the next call retries the real load), and `GET /api/tts/engines?refresh=1` - the Voices page "Kiểm tra lại" button - clears it immediately. To check a machine by hand, run the worker with the server's env (`HF_HOME` and `HUGGINGFACE_HUB_CACHE` both = `.runtime/models`) and send `{"id":1,"cmd":"synth","text":"Xin chào","voice":"Mai Anh","out":"<abs path>.wav"}` on stdin.

**Symptom:** Cloning fails with `ImportError: TorchCodec is required for load_with_torchcodec`, or `RuntimeError: Could not load libtorchcodec`.
**Cause:** `add_voice()` reads the reference through `torchaudio.load()`. From torchaudio 2.9 every backend routes through `torchcodec`, which needs FFmpeg **shared libraries** - the usual Windows FFmpeg builds are static, so it can never load. Installing `torchcodec` does not fix it. Passing `backend="soundfile"` does not fix it either (verified: all three backends raise the same error).
**Fix:** monkeypatch `torchaudio.load` to use `soundfile` **before importing vieneu**. `soundfile` is already a vieneu dependency, so this adds nothing to install. Guard it in try/except so that a machine without torch still gets preset voices.

```python
import torch, torchaudio, soundfile as sf
def _load(uri, *a, **kw):
    data, sr = sf.read(str(uri), dtype="float32", always_2d=True)
    return torch.from_numpy(data.T).contiguous(), sr
torchaudio.load = _load
```

**Symptom:** Voices are filed under the wrong region, or every male voice looks southern.
**Cause:** `list_preset_voices()` returns labels shaped `Name — <Nam|Nữ> · <Bắc|Trung|Nam> · Phong cách <...>`. Field 1 is **gender**, field 2 is **region**, and the word **"Nam" means both "male" and "southern"**.
**Fix:** parse strictly by position, never by searching for the substring "Nam". Regression cases: `Thái Sơn` = gender nam / region nam; `Mai Anh` = gender nu / region bac.

**Symptom:** Cloned voices vanish after a restart, or a stray voice appears in the preset list and leaks into vieneu's own error messages.
**Cause:** `tts.save_voices()` (and `add_voice(..., save=True)`) rewrites `vieneu/assets/voices_v3_turbo.json` inside site-packages, permanently adding your test voice as a 15th "preset". This happened for real during development.
**Fix:** never call either. The store lives at `assets/voices/` (`library.json` plus `<id>/ref.wav`) and voices are re-registered into the worker on demand with `add_voice(..., save=False)`. Registration costs ~3s and is lost whenever the worker restarts, so track what the live process actually has. As defence in depth the worker drops any preset whose description does not parse into `gender · region · style`, and `listLocalVoices()` drops presets colliding with a store id - a contaminated install still yields a clean 14. To repair one by hand, delete the offending key from `voices_v3_turbo.json` or `pip install --force-reinstall vieneu`.

**Symptom:** A storytelling voice reads like a newsreader.
**Cause:** `infer()` has its own `style=` argument defaulting to `"tu_nhien"`, which is independent of the voice you picked.
**Fix:** look up each preset's own `style` (`get_preset_voice(name)` returns `{gender, style, description, ...}` as real fields) and pass it into `infer()`. Only **region** has to be parsed out of the description string.

**Symptom:** Timeline drifts against the narration.
**Cause:** estimating duration from character count.
**Fix:** every duration is measured with ffprobe, exactly as on the Gemini path. This is not engine-specific advice - see the `video-pipeline` skill.

## Architecture notes

- `apps/server/python/vieneu_worker.py` is a long-lived worker speaking JSON-lines on stdin/stdout. **stdout is protocol only**; all logging goes to stderr. It must `sys.stdout.reconfigure(encoding="utf-8")` first thing or Vietnamese corrupts on the Windows cp1252 console.
- `ping` must answer **without loading the model** - it backs the availability check.
- One worker, requests serialised (the model is not re-entrant), 10-minute idle shutdown because it holds ~1 GB of RAM.
- Output is already **48 kHz mono**, which equals the pipeline's `OUT_SAMPLE_RATE`, so no resampling. It still goes through the same `TRIM_FILTER` and gap-insertion path as Gemini in `synthScript()` - two engines with two joining strategies would drift audibly at the seams.
- The Perth watermark is left at its default (on). It is inaudible and is the responsible default for cloned speech.

## Reference audio guidance for users

3-8 seconds, clean speech, no background music, no noise. Longer is **not** better - the model only uses the head, so anything past ~8s is discarded. Below 3s the embedding is too weak and the clone stops resembling the speaker.
