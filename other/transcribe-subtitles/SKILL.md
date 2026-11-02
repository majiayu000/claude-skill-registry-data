---
name: transcribe-subtitles
description: Produce finished SRT/VTT subtitles locally from audio or video; automatically prepare whisper.cpp, FFmpeg and the base multilingual model when needed.
priority: P1
category: media
status: builtin-guidance
---

# Transcribe & Subtitles

Transcribe on the user's own computer using whisper.cpp + FFmpeg. Keep recordings, extracted audio, inference and results on that device. Deliver actual .srt/.vtt files, and a subtitled video if requested.

## Device and permission gates

Use an online user device with read_file, write_file and start_process inside an authorized Trusted Write Location. A transcription task authorizes ordinary task-local dependency preparation within those permissions. Automatically download/install missing FFmpeg, whisper.cpp and the multilingual base model; announce the source, approximate size and destination, then continue. Do not stop to ask the user to install them manually. No system/admin installation, cloud transcription, paid API or input-media upload is authorized by this skill.

## Prepare the local helper

Use scripts/local-media.mjs packaged with this skill. Arc prepare_skill {id:"transcribe-subtitles",deviceId,workspace} stages it. Connect read_skill {id:"transcribe-subtitles",path:"scripts/local-media.mjs",offset:0} returns exact chunks; follow nextOffset to null, write them locally and compare SHA-256 with the manifest. Resource-only clients can read remotearc://skills/transcribe-subtitles/scripts/local-media.mjs.

Use Node.js 22.2+ and npm. If missing, prepare a portable Node distribution from nodejs.org/dist inside .ra-media-tools/node and verify the published release SHASUMS256.txt; no administrator/global installation. Read video-creator for that preparation method if needed.

    node "<helper>/scripts/local-media.mjs" ensure --workspace "<workspace>" --components whisper

The helper reuses working binaries, otherwise downloads checksum-verified pinned releases, or builds pinned whisper.cpp locally with a portable CMake. macOS/Linux require an existing C++ compiler and git; if an OS developer-tools dialog is necessary, report that specific blocker without bypassing OS consent. Windows x64 uses the CPU binary with its DLLs. GPU is optional; no CUDA/PyTorch download by default.

**Default model:** `ggml-base.bin` (multilingual, ~148 MB / 141 MiB), pinned to a Hugging Face revision and SHA-256. Keep caches under <workspace>/.ra-media-tools. Initial setup may also need tens or hundreds of MB for FFmpeg/build tools. Check free disk first and reuse verified caches on later runs. ggml-small.bin (~466 MB) or ggml-large-v3-turbo.bin (~1.6 GB) require explicit size-aware consent before a larger download; do not silently substitute them after poor recognition. Qwen TTS and ACE-Step installation always follows their size-aware confirmation gate.

## Produce and verify subtitles

1. Inspect the input duration and audio track with ffprobe. For long recordings, disclose likely CPU runtime; run as a managed background process so it can finish and retain logs.
2. Execute:
       node "<helper>/scripts/local-media.mjs" transcribe --workspace "<workspace>" --input "<audio or video>" --output "<new subtitle prefix>" --language auto
   Use zh/en when the language is known. The helper prepares dependencies, extracts 16 kHz mono WAV, runs whisper-cli, reads generated SRT/VTT and validates nonempty timed cues, ordering and source-duration bounds. It refuses to overwrite existing output files and writes an artifact receipt. Silence/no speech is reported explicitly.
3. Read the output, review a sample against the original audio, correct observed mistakes and verify names/terminology. Never invent dialogue or speaker identities. Timed files alone do not establish recognition accuracy.
4. For burned-in subtitles, use local FFmpeg with the correct installed font (CJK for Chinese), fit subtitles inside safe margins, then ffprobe and decode the resulting MP4. Inspect frames and audio sync. For OpenFilm, put a matching .vtt beside its clip.
5. Deliver .srt and .vtt (and the MP4 if asked), absolute local paths, model name, covered duration and unverified portions. A temporary create_file_resource link is optional; keep the local durable copy and state link expiry.

## Evidence of completion

Do not claim subtitles exist before reading both files. Distinguish engine readiness, transcription completion, timing validation and human-language accuracy. Downloads contact official dependency/model hosts; user recordings never leave the selected device.
