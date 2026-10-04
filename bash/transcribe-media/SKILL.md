---
name: transcribe-media
description: Transcribe local audio or video files into timestamped JSON and readable Markdown with resumable processing and source provenance. Use when a user asks to transcribe, extract spoken content, create subtitles or text from local media, or passes a supported video URL for transcription. For URLs, invoke $download-video first and consume its verified artifact manifest. After a non-empty transcript is complete, ask whether the user wants to invoke $ingest-knowledge; never write to a knowledge base without confirmation.
---

# Transcribe media

Turn one verified local media input into a traceable transcript artifact. Do not combine transcription with summarization or knowledge-base writes.

## Platform boundary

- Mutating and file-verifying operations support Python 3.11–3.14 on macOS
  and Linux.
- They require POSIX `fcntl`, `dir_fd`, `O_NOFOLLOW`, `O_DIRECTORY`, directory
  `fsync`, atomic no-replace rename, and atomic exchange rename. Missing
  capabilities fail closed with
  `UNSUPPORTED_PLATFORM`; there is no weaker fallback.
- Input, model, adapter, output, state, and chunk paths must not traverse
  arbitrary symlinks. Managed files must be current-user-owned regular files
  with one link.

## CLI protocol

Success prints exactly one JSON object to stdout, leaves stderr empty, and
exits 0. An expected failure leaves stdout empty and prints exactly one
redacted JSON error to stderr. Repository-wide failure codes are: 2 for
arguments, schemas, or unsafe inputs/paths; 3 for unavailable dependencies,
models, or platform capabilities; 4 for locks, conflicts, recovery conflicts,
or stale plans; 5 for external-tool, network, or runtime I/O failures; 7 for
contract, identity, or file-evidence integrity failures; and 130 for
interruption.

## Workflow

1. Determine whether the input is a URL or a local path.
   - For a URL, invoke `$download-video`, require a complete
     `awesome-capture.artifact/v2` video artifact, and retain both the artifact
     path and `media.path`.
   - For a local path, inspect it directly. Do not invent or guess an adjacent
     artifact path.
2. Check the environment:

   ```bash
   python3 scripts/transcribe_media.py doctor \
     --model "<absolute-local-ggml-model-path>" \
     --whisper-cpp-bin "<absolute-whisper-cli-path>"
   ```

   `--engine auto` requires both this explicit binary path and the explicit
   local model path. An explicit `--engine whisper-cpp` may still discover
   `whisper-cli` on `PATH` when the binary option is omitted.
   For speech recognition without a sidecar subtitle, require
   `ready_for_asr: true`; `status: ok` only means the diagnostic command itself
   completed.

3. Inspect the media and confirm it has an audio stream:

   ```bash
   python3 scripts/transcribe_media.py inspect "<absolute-media-path>"
   ```

4. Prefer an exact-basename `.srt` or `.vtt` sidecar when present. Otherwise select an engine:
   - `auto`: whisper.cpp only when both `--whisper-cpp-bin` and `--model`
     explicitly name existing local files. It never discovers the binary from
     `PATH` or selects a Python engine.
   - `whisper-cpp`: first-class local engine. It requires an explicit local `--model` file and optionally `--whisper-cpp-bin`.
   - `faster-whisper`: explicit only; requires a fully local model directory.
   - `mlx-whisper`: explicit only; requires a fully local model directory and
     a compatible local MLX installation.
   - `external`: explicit only; requires `--adapter`, a local `--model`, and
     `--trust-external-adapter`.
5. For a local file, run:

   ```bash
   python3 scripts/transcribe_media.py transcribe "<absolute-media-path>" \
     --output-dir "<absolute-dir>" \
     --engine auto \
     --model "<absolute-local-ggml-model-path>"
   ```

   For a video produced by `$download-video`, pass the handoff explicitly:

   ```bash
   python3 scripts/transcribe_media.py transcribe \
     "<video-artifact.media.path>" \
     --source-artifact "<absolute-video-artifact-v2-path>" \
     --output-dir "<absolute-dir>" \
     --engine auto \
     --model "<absolute-local-ggml-model-path>"
   ```

   `--source-artifact` is never inferred. When present, its schema, contract
   digest, media path, bytes, SHA-256, duration, stream counts, and current
   ffprobe evidence are all revalidated.

   Other transcription options are:

   - `--language <code>` to request a language;
   - `--ignore-sidecar` to force ASR despite an exact-basename subtitle;
   - `--chunk-seconds <n>` (default `600`, minimum `30`);
   - `--timeout <seconds>` for each external process (default `3600`);
   - `--lock-timeout <seconds>` for the persistent job lock (default `30`).

   To bypass the initial whisper.cpp GPU subprocess, add `--whisper-cpp-cpu-only`. Normally leave it off: the first GPU failure is recorded, retried with `-ng`, and cached so the remaining chunks in that task go directly to CPU.

6. Require zero exit status and a complete
   `awesome-capture.artifact/v2` transcript. Read output paths from
   `artifact.outputs`; do not derive them from filenames. Report the engine,
   detected language, duration, segment count, transcript Markdown path, and
   any empty/silent result.
7. If the transcript contains speech, ask exactly one follow-up: “是否需要把这份内容写入本地 Obsidian 知识库？” If yes, invoke `$ingest-knowledge` with `transcript.json`. If no, stop.

## Recovery

Transcription uses a persistent job lock and private managed layout:

```text
<output>/.awesome-capture-media/v2/
  locks/
  staging/
  transcriptions/<64-hex-job-id>/
  quarantine/
```

The source is copied to a private content-verified snapshot before ffmpeg or
ASR reads it. Managed directories use mode `0700`; locks, snapshots, chunks,
state, outputs, pending artifacts, and final artifacts use `0600`.

Re-running the same command acquires the same lock and either resumes a valid
`running` state, publishes a verified pending artifact, or returns `reused`.
For an explicit recovery pass:

```bash
python3 scripts/transcribe_media.py recover \
  --output-dir "<absolute-dir>" \
  --lock-timeout 30
```

Recovery never overwrites an existing artifact. Unknown workspace files,
unsafe links, conflicting identities, or invalid hashes produce
`RECOVERY_CONFLICT` or an integrity error.

## Reliability rules

- Preserve source timestamps; never invent missing speech.
- Keep `awesome-capture.transcription-state/v1`, the complete
  `awesome-capture.chunk-set/v1` manifest, and per-chunk results so an
  interrupted run can resume.
- Reject missing or extra chunks, filename gaps, changed hashes, non-mono
  16 kHz PCM16 WAVs, inconsistent cumulative timing, foreign state entries,
  and incomplete result sets.
- Offset each chunk by the cumulative duration measured from the normalized WAV sample counts. Never multiply the nominal `--chunk-seconds` value by the chunk index.
- Do not download models. Every ASR engine requires an explicit local model.
  Record and bind the model, engine executable or adapter, package versions,
  settings, and source to the job identity.
- Re-hash the private source snapshot, model, executable/adapter, and the
  versioned content identity of the standalone transcription implementation
  before publishing. Also compare the execution metadata guard so a component
  changed and then restored to the same bytes still aborts with
  `IDENTITY_CHANGED`. Once the private
  snapshot is durably verified, recovery does not require the original source
  path or upstream video artifact to remain present.
- Write chunk results and derivative outputs while state remains `running`.
  After validating every result and output hash, durably write
  `transcript.pending.json`; only then advance state to `ready_to_publish`.
  Promotion revalidates source/model/adapter/chunks, advances state to
  `complete`, and refreshes the pending artifact's state descriptor.
  Publish `transcript.json` last without clobbering an existing entry.
- Reject artifact/v1, unversioned or unknown state, duplicate JSON keys,
  non-finite numbers, and unknown contract properties. Do not migrate or
  silently fall back.
- Treat a platform title, description, chapter summary, or LLM-generated reconstruction as metadata, not transcription.
- Do not summarize before the transcript artifact is complete.
- `external` executes explicitly trusted local code. It is not selected
  automatically and is not an OS-level network sandbox.
- External media tools run with a working directory pinned by directory FD;
  regular media/model-file inputs are passed through inherited read-only FDs
  where supported. Local model directories are still re-hashed before and
  after execution and are not an OS sandbox.
- Read [engines.md](references/engines.md) before choosing models, handling long files, or adding an engine.
- Read [artifact-contract.md](references/artifact-contract.md) when composing with another skill.
