---
name: create-music
description: Create and deliver original songs, vocal tracks, instrumentals, theme songs, jingles, and other requested music audio with HeartMuLa on the local ROCm GPU. ALWAYS load and prioritize this skill whenever a request looks like it may involve making, composing, generating, producing, or turning lyrics/ideas into a song or music—even if the user does not explicitly say “AI music” or provide lyrics yet. Also use for /create-music. Do not use for merely discussing music or restyling an existing recording.
version: 1.1.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [ffmpeg]
  paths: [~/src/heartlib]
metadata:
  hermes:
    tags: [music, song, generation, ai, heartmula, lyrics, genre, suno, audio]
    related_skills: [heartmula, mock-voice]
---

# Create Music — HeartMuLa song generation (lyrics + genre, GPU)

Generate a full song from **lyrics** and **genre/style tags** using HeartMuLa (`heartlib`),
an open-source Suno-like model, on the local AMD GPU (ROCm). Deployed at `~/src/heartlib`.

## Mandatory trigger policy

**Prioritize and load this skill first whenever the request appears to involve producing music.** This includes:

- Writing, making, composing, generating, or producing a song from even a vague idea.
- Theme songs, character songs, jingles, background music, beats, vocal songs, and instrumentals.
- Turning lyrics, a story, mood, genre, image, or concept into playable music audio.
- Requests such as「做一首歌」「幫我寫歌」「製作音樂」「配樂」「角色歌」even when no duration, tags, or lyrics were supplied.

Do not wait for the user to name HeartMuLa. Load this skill before choosing tools or commands. It is not needed when the user only asks for music facts, lyrical analysis, playback/search, or to restyle an existing audio recording.

## Required execution workflow

1. Search for factual genre/reference characteristics as required below, then prepare tags and structured lyrics.
2. Choose an absolute output path ending in `.mp3`, `.wav`, or `.flac`. Default to high-quality MP3 unless the user requests otherwise.
3. Run the canonical wrapper below. **Do not use a remembered manual command and do not use a `~/.claude/...` path.** The wrapper sets the required working directory, ROCm environment, BF16 codec, AOTriton, lossless intermediate, and MP3 bitrate.
4. Allow enough execution time. Use at least `max(180, 60 + 2.2 × requested_seconds)` seconds; add extra time when using `-S` or `-C`. Do not impose a 600-second timeout on songs longer than about four minutes.
5. Confirm the output exists and inspect it with `ffprobe` before claiming success.
6. Deliver it in chat with `[[file: /absolute/path/song.mp3]]`. Never claim generation succeeded when the output file is absent.

## Canonical command

The skill is discovered through `~/.pi`, which resolves to the shared Hermes skill directory on this machine:

```bash
~/.pi/agent/skills/media/create-music/create_music.sh \
  -t "piano,happy,lofi" \
  -l /absolute/path/my_lyrics.txt \
  -d 90 \
  -Q high \
  -o /absolute/path/song.mp3
```

Inline lyrics (`\n` becomes a line break):

```bash
~/.pi/agent/skills/media/create-music/create_music.sh \
  -t "jazz,piano,relaxing" \
  -L "[Verse]\nMidnight city lights are glowing\n[Chorus]\nWe are dreaming, we are flowing" \
  -d 60 -Q high -o /absolute/path/mysong.mp3
```

Required output verification:

```bash
test -s /absolute/path/song.mp3
ffprobe -v error -show_entries format=duration,bit_rate \
  -of default=noprint_wrappers=1 /absolute/path/song.mp3
```

Options:
- `-t TAGS` — genre/style, **comma-separated** (e.g. `"rock,energetic,guitar"`). Drives the vibe.
- `-l FILE` — lyrics file path (structured, see format below).
- `-L TEXT` — inline lyrics string (overrides `-l`).
- `-o OUT` — output path. `.mp3` is auto-encoded at **320kbps** (generated lossless then ffmpeg);
  `.wav`/`.flac` = lossless. Default `./assets/output.mp3`.
- `-d SEC` — max length in seconds. Default **90** (1:30). Use larger for full songs.
- `-T TEMP` — temperature (default 1.0; higher = more variation).
- `-c CFG` — guidance scale (default 1.5; higher = follow tags/lyrics more strictly).
- `-k TOPK` — top-k sampling (default 50).
- `-Q LEVEL` — **quality preset** (default `high`):
  - `high` — 320kbps mp3 + codec_steps 16 (best fidelity).
  - `low` — 128kbps mp3 + codec_steps 8 (faster, smaller — drafts/quick previews).
- `-q STEPS` — override the preset's HeartCodec decode steps (higher = better fidelity, slower).
- `-C` — compile the MuLa model using TorchDynamo (recommended for long runs, e.g., > 3 minutes).

### Audio quality

- **`-Q high` (default)** = 320kbps mp3; **`-Q low`** = 128kbps mp3 (faster). The wrapper renders
  the model's audio to a lossless wav then ffmpeg-encodes at the preset bitrate (avoids
  soundfile's low default mp3 bitrate and double-lossy).
- For lossless, use `-o name.flac` or `-o name.wav` (bitrate preset is ignored for those).
- `-q` overrides codec decode steps (reconstruction fidelity); `-Q high` already uses 16.
- Codec runs in bfloat16 for a massive 4.25x speedup on ROCm with negligible quality difference.

### Clarity Repair (audio-separator post-processing, `-S`)

Pass `-S` to run the finished song through **audio-separator** (UVR-MDX-NET-Inst_HQ_4) on the
ROCm GPU as a clarity-repair pass. It splits the song into vocals + instrumental stems and sums
the cleaned stems back into one mix — the MDX model only passes through learned musical content,
so the reconstruction drops broadband noise / muddiness it treats as non-music. **Keeps vocals**
(it is not a karaoke/instrumental-only extraction).

```bash
~/.pi/agent/skills/media/create-music/create_music.sh -t "lofi,chill,jazz" -L "[Verse]\n..." -d 60 -S -o /absolute/path/song.mp3
```

- Runs on GPU via the onnx2torch→torch-ROCm path (no onnxruntime EP needed; gfx1151-safe).
- Deployed at `~/src/audio-separator` (uv venv, torch 2.11+rocm7.2). Wrapper:
  `~/src/audio-separator/enhance_clarity.sh -i in.mp3 -o out.mp3` (standalone use on any audio).
- First run JITs MIOpen kernels (~30s extra); the kernel cache persists, then it's ~RTF 1 on GPU
  (a 6s clip ≈ 3s separation). A full 4-min song ≈ ~2 min.
- Caveat: MDX works at **44.1kHz**, so the repaired output is 44.1kHz (HeartMuLa natively outputs
  48kHz). It's a clarity/de-noise pass, not bandwidth extension.

## Lyrics format

Use section headers in square brackets. Lines under each become the sung lyrics. For an
**instrumental**, use only structural tags with empty sections (e.g. just `[Intro]`).

```txt
[Intro]

[Verse]
The sun creeps in across the floor
I hear the traffic outside the door

[Prechorus]
The world keeps spinning round and round

[Chorus]
Every day the light returns
Every day the fire burns

[Bridge]
It is not always easy, not always bright

[Outro]
```

Supported sections: `[Intro] [Verse] [Prechorus] [Chorus] [Bridge] [Outro]` (multilingual lyrics
are supported — HeartMuLa covers most languages).

## ⚠️ MANDATORY: Search online BEFORE generating tags

**NEVER write tags from memory or guess.** When the user specifies a genre, artist, song, or style:

1. **Search the web** — e.g. `"<artist> instruments tempo BPM"` or `"<genre> musical style characteristics"`
2. **Find real data** — BPM, specific instruments, arrangement style, vocal type, tempo
3. **Write tags from actual findings** — not from guessing or generic assumptions
4. **If no search results found**, tell the user and ask for clarification

**Examples of things you MUST search:**
- Artist-specific requests: "like Only My Railgun" → search for fripSide's actual instruments, BPM (130-143), synth+rock fusion
- Genre requests: "京韵大鼓" → search for real instruments (大三弦、四胡、琵琶), ban shuo ban chang style
- Song references: "like <song title>" → search the actual song's musical characteristics

**What NOT to do:**
- ❌ Write tags like "rock, energetic, guitar" for only my railgun (too vague, wrong BPM)
- ❌ Write "Beijing opera, guqin" for 京韵大鼓 (wrong instruments entirely)
- ❌ Guess what a genre sounds like without checking

### Genre / tags ideas (for reference only — still search first)

Comma-separated descriptors of instrument, mood, genre, tempo, vocals. Examples:
- `piano, happy, upbeat`
- `lofi, chill, mellow, jazz`
- `rock, energetic, electric guitar, male vocals`
- `orchestral, epic, cinematic`
- `electronic, synth, dance, female vocals`
- `acoustic, folk, soft, warm`

## Manual fallback (only if the wrapper is unavailable)

The wrapper is authoritative. Use this only after verifying it is missing or broken. These settings are required for the optimized ROCm path; generate WAV first and encode MP3 afterward.

```bash
cd "$HOME/src/heartlib"
export PYTHONUTF8=1
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1

.venv/bin/python ./examples/run_music_generation.py \
  --model_path ./ckpt --version 3B \
  --lazy_load false --codec_dtype bfloat16 \
  --tags /absolute/path/tags.txt \
  --lyrics /absolute/path/lyrics.txt \
  --max_audio_length_ms 90000 \
  --temperature 1.0 --cfg_scale 1.5 --topk 50 \
  --codec_steps 16 --compile false \
  --save_path /tmp/song.wav

ffmpeg -y -i /tmp/song.wav -b:a 320k /absolute/path/song.mp3
```

Change `--max_audio_length_ms` to exactly `requested_seconds × 1000`; never copy a stale hard-coded 240000 value. Key flags are `--tags`, `--lyrics`, `--max_audio_length_ms`, `--temperature`, `--cfg_scale`, `--topk`, `--codec_steps`, and `--save_path`.

## Performance & hardware (Strix Halo gfx1151, ROCm 7.2)

- The wrapper enables AOTriton memory-efficient attention with `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1`; generation sustains about **7.3 iterations/second**.
- Measured high-quality end-to-end wall times: **10s audio ≈ 32s, 20s ≈ 54s, 30s ≈ 76s**. MuLa autoregressive generation accounts for roughly 71–77% of runtime.
- HeartCodec decodes fixed 29.76-second windows. Going from 29.x to 30 seconds crosses into a second window, so codec time rises discontinuously rather than perfectly linearly.
- Compiling via `-C` can increase generation to about **7.8 iterations/second**, but adds startup overhead. Reserve it for songs longer than roughly three minutes.

## Notes / gotchas

- Must use **torch 2.11+rocm7.2** in `~/src/heartlib/.venv`. The `rocm7.1` torch wheel SIGSEGVs
  in `libhsa-runtime64.so` on this gfx1151 (even a bare GPU matmul) — do not downgrade to it.
- Output saving is patched to use `soundfile` (torch 2.11's `torchaudio.save` needs torchcodec).
- Models live in `~/src/heartlib/ckpt` (HeartMuLaGen + HeartMuLa-oss-3B + HeartCodec-oss, ~21G).
- If the box's qwen `llama-server` (:8001) is also running, there's still ~40GB GTT free — both
  fit, but if you hit a true OOM, lower its context (`-c`) rather than `-np`.
