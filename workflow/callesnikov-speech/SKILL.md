---
name: callesnikov-speech
description: Use this skill when the user wants to prepare or run a local speech-to-text workflow for long audio files with ffmpeg and whisper.cpp. Trigger for local audio transcription tasks involving mp3, wav, m4a, ogg, chunking into short files, checking or bootstrapping whisper.cpp runtime/model files inside the skill folder, transcribing chunks to json/srt/txt, and merging text chunks without prematurely running later stages.
---

# Callesnikov Speech

Use this skill to process long local audio incrementally through an offline-friendly `ffmpeg` and `whisper.cpp` pipeline.

Only perform the stage the user asked for. Do not advance to later stages unless the user explicitly asks to continue.

## Core Rules

- Keep every runtime asset self-contained in this skill directory: `C:\Users\User333\.codex\skills\callesnikov-speech`.
- Put `whisper.cpp`, build outputs, model files, helper downloads, temporary files, and generated skill-owned metadata under this skill folder only. Do not install models or binaries globally.
- Prefer the model at `runtime/whisper.cpp/models/ggml-large-v3-turbo.bin` when it exists.
- Use official sources when checking freshness or downloading runtime assets:
  `https://github.com/ggml-org/whisper.cpp` for runtime, `https://huggingface.co/ggerganov/whisper.cpp/tree/main` for pre-converted GGML model files, and official OpenAI Whisper references for model lineage.
- If a needed codec, audio format dependency, or system package is outside the bundled skill runtime, ask the user where to install or download it.
- Work in the current task directory for audio chunks and transcript outputs.
- Use the scripts in `scripts/` for repeatable stages when possible.
- Treat `runtime/whisper.cpp/models/` as the only model directory unless the user explicitly provides another model path for a one-off run.
- Never accept a generic `main` executable from PATH on Windows; use a local `whisper-cli.exe`, local `main.exe`, or an explicit user-provided binary path.

## Runtime And Model Sources

Expected local layout:

```text
C:\Users\User333\.codex\skills\callesnikov-speech\
  runtime\
    whisper.cpp\
      build\
      models\
        ggml-large-v3-turbo.bin
```

Use these upstream sources when bootstrapping or updating:

- Runtime repository: `https://github.com/ggml-org/whisper.cpp`
- GGML model repository: `https://huggingface.co/ggerganov/whisper.cpp/tree/main`
- Default model file: `ggml-large-v3-turbo.bin`
- whisper.cpp model downloader after cloning/building: `runtime\whisper.cpp\models\download-ggml-model.cmd large-v3-turbo`

When assets are missing, explain the missing pieces and offer a local skill-folder bootstrap. Do not download the large model or clone/build whisper.cpp unless the user explicitly asks.

Bootstrap command, only after explicit user approval:

```powershell
C:\Users\User333\.codex\skills\callesnikov-speech\scripts\bootstrap_whisper_cpp.ps1 -Model large-v3-turbo
```

This script clones/updates `whisper.cpp`, builds it with CMake, downloads the selected GGML model, and then runs preflight. It writes only under `C:\Users\User333\.codex\skills\callesnikov-speech\runtime`.

## Stage 0: Bootstrap And Preflight

On the first user message in the current chat, run one preflight for local tooling and the default model:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-speech\scripts\preflight.py"
```

Check `ffmpeg`, `python`, `cmake`, a runnable local `whisper.cpp` binary, and at least one usable `ggml` model under `runtime/whisper.cpp/models/`.

If files are missing, explain exactly what is absent. Downloads and builds must be placed inside this skill folder. Do not start transcription until the user explicitly asks.

## Stage 1: Split Source Audio

When the user provides a source audio file, split it into short chunks:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-speech\scripts\split_audio.py" "C:\path\to\audio.mp3"
```

Default to `60` second chunks unless the user asks for another value in the `50-70` range. Write chunks into `splitted_records` as `audioChunk_XXX.wav`.

After success, tell the user the source audio was split and point to `splitted_records`.

## Stage 2: Prepare Output Directories

After splitting, create transcript output directories next to `splitted_records`:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-speech\scripts\prepare_dirs.py"
```

This creates `transferred` and `low_merged`. Continue to stage 3 only when the user asks.

## Stage 3: Transcribe Audio Chunks

Transcribe prepared chunks from `splitted_records`, not the original long recording:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-speech\scripts\transcribe_chunks.py"
```

Use the model requested by the user, or default to `runtime/whisper.cpp/models/ggml-large-v3-turbo.bin`. If that model is missing, stop and request permission to bootstrap/download it into the skill folder. Save `json`, `srt`, and `txt` artifacts for every processed chunk into `transferred`.

After success, tell the user each chunk was converted and the results are in `transferred`.

## Stage 4: Merge TXT Chunks

Merge only the `txt` outputs from `transferred`:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-speech\scripts\merge_txt_chunks.py"
```

Default to `20` text chunks per merged file unless the user asks for another value in the `20-30` range. Write merged files to `low_merged` using `mergedFromXToY.txt`, where `X` and `Y` are the included chunk numbers.
