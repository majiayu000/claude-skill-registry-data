---
name: restyle-music
description: Change the style/genre of an existing song while keeping its original melody and structure, using ACE-Step 1.5 "cover" mode on the local ROCm GPU. Use when the user provides an audio file and asks to convert/restyle/re-arrange it into another genre or instrumentation (e.g. "make this song traditional Japanese", "turn this into lofi jazz", "orchestral version of this track").
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [ffmpeg, yt-dlp]
  paths: [~/src/ACE-Step-1.5, ~/src/audio-separator]
metadata:
  hermes:
    tags: [music, cover, restyle, genre, style-transfer, ace-step, audio, gpu, rocm]
    related_skills: [create-music, mock-voice]
---

# Restyle Music — change a song's style, keep its melody (ACE-Step 1.5 cover, GPU)

Take an **existing audio file** + a **target style description** and re-render the song in that
style while preserving the original melody/structure, via ACE-Step 1.5's `cover` task on the
local AMD GPU (ROCm, gfx1151). Deployed at `~/src/ACE-Step-1.5`.

## ⚠️ MANDATORY: Web search FIRST — NEVER guess

**This skill REQUIRES searching the web before writing ANY caption. No exceptions.**

**Mandatory workflow (agent MUST follow each step):**
1. **Take the user's requested style** (genre name, artist, band, song reference, or vibe).
2. **Web-search it** — e.g. `"<genre> instruments musical style"` or `"<artist> band instruments
   genre"` or `"<song title> BPM arrangement"`. **You MUST find real data.**
3. **Collect facts** — specific instruments, BPM/tempo, vocal type, arrangement style, what it avoids.
   (Example: Wagakki Band search revealed shamisen/koto/shakuhachi/taiko + rock band.)
4. **Compose the `-s` caption** from those ACTUAL findings — not from memory or guessing.
5. **Run the wrapper** with the researched caption.

**What happens if you skip the search:**
- You will write wrong instruments (e.g. "guqin" instead of "大三弦" for 京韵大鼓)
- You will get wrong tempo (e.g. "170 BPM" instead of "130 BPM" for only my railgun)
- The output will sound "wrong" and users will call you out on it
- **This skill has been broken by this exact mistake multiple times**

**Skip the search ONLY when:** genre is extremely generic with no specific references (e.g. "lofi", "orchestral").
When in doubt, ALWAYS search.

## Caption format — how to write `-s` correctly

**The `-s` caption MUST follow ACE-Step's official format.** Never just comma-separate tags.
Write it as a **descriptive paragraph** using this four-part structure:

```
[1. Big genre label] + [2. Specific instruments/arrangement] + [3. Mood/atmosphere/scene] + [4. Exclusions]
```

This is based on the **official** `cover_wagaku.py` example from the ACE-Step repo:

```
Traditional Japanese wagaku arrangement (和樂). Replace all modern instruments with classical
Japanese ones: plucked shamisen and koto, breathy shakuhachi bamboo flute, deep taiko drums,
kotsuzumi hand drums, biwa, suzu bells and wind chimes. Pentatonic min'yo / gagaku folk feel,
elegant and ceremonial, slower contemplative tempo, acoustic and organic, evoking a Japanese
festival under cherry blossoms. No electric guitar, no synthesizer, no drum machine.
```

### Structure breakdown

| Part | What to include | Example |
|---|---|---|
| **1. Genre label** | The big genre/style name | `Taiwan 8+9 komedya pop` |
| **2. Instruments** | Name specific instruments/arrangement | `bright brass with trombone and trumpet, synth bass, gong and drum` |
| **3. Mood/scene** | Describe the vibe/atmosphere | `festive party atmosphere reminiscent of Taiwanese wedding band` |
| **4. Exclusions** | Explicit `No X, No Y` | `No acoustic instruments, no jazz elements` |

### ✅ vs ❌ examples

```bash
# ❌ BAD — tag soup, comma-separated gibberish
-s "lofi jazz, chill, mellow, piano, beats, instrumental"

# ✅ GOOD — descriptive paragraph following official format
-s "lofi jazz: mellow Rhodes electric piano over a relaxed hip-hop drum beat with brushed snare,
upright bass walking the root notes, warm vinyl crackle texture, relaxed and contemplative mood
for late-night study sessions. No heavy bass, no synth leads, no fast tempo."
```

> 💡 Write the `-s` caption like a **brief for a music producer** — a complete descriptive
> paragraph, not a tag cloud.

**Two hard rules:**
- **Write the caption in English.** The model's text encoder is English-centric, so English gives
  the most reliable results. A native-script genre name in parentheses is fine (the official
  example uses `(和樂)`), but keep the instrument/mood description in English.
- **Keep it under ~512 characters** (ACE-Step's caption limit; longer is silently truncated).
  The official example above is ~330 chars — aim for that ballpark, not an essay.

## ACE-Step constraints (the skill validates these)

Stay within what ACE-Step actually supports — don't invent free-form values for the bounded
fields. From `acestep/constants.py` + `inference.py`:

- **Caption (`-s`)**: free text (Qwen3-Embedding encoder — there is **no fixed tag list**), but
  **≤ 512 chars** (the skill errors if longer). Ground the instruments you name in ACE's
  recognised families for reliable results: **woodwinds, brass, strings, keyboard, guitar, bass,
  drums, percussion, synth, fx, vocals/backing_vocals**. Obscure/very specific instruments may be
  hit-or-miss; describe them in those terms (e.g. "shamisen → plucked strings", "sax → woodwinds").
- **Vocal language (`-g`)** must be one of ACE's `VALID_LANGUAGES`: `ar az bg bn ca cs da de el
  en es fa fi fr he hi hr ht hu id is it ja ko la lt ms ne nl no pa pl pt ro ru sa sk sr sv sw ta
  te th tl tr uk ur vi yue zh unknown`. (No 台語 token — use `zh` or `yue`.) The skill warns and
  falls back to `en` for anything else.
- **BPM (`-B`)**: 30–300 (auto-detected value is clamped to this).
- **Lyrics (`-l`/`-L`)**: ≤ 4096 chars; `[Instrumental]` = no vocals.
- **Duration**: 10–600 s; for cover it's locked to the source length.
- Other metadata ACE accepts (not exposed as flags): keyscale (A–G + ♯/♭, major/minor),
  time-signature ∈ {2,3,4,6}.

## When to use

- "Change this song into <genre>" / "make this traditional Japanese / lofi / orchestral / metal"
- "Re-arrange / cover this track in another style", "swap the instrumentation"
- User gives an input audio file and a vibe; wants a restyled audio file out.

This is **cover** (melody-preserving style transfer), not text-to-music from scratch — for
generating a brand-new song from lyrics+tags use the `create-music` skill instead.

## Keep the ORIGINAL singing voice (`-k`)

Cover mode **re-synthesizes the whole song, vocals included** — so on its own it cannot keep the
real original voice (it renders a new singer over the kept melody). To genuinely preserve the
original voice, pass `-k`. The `-k` pipeline:

1. **Separate** the song into vocals + instrumental with `audio-separator` (UVR-MDX-NET, GPU).
2. Feed the **isolated vocal** to ACE as the cover source (with `[Instrumental]`), so ACE
   **composes a fresh new-genre backing that follows the sung melody** — rather than trying to
   bend the old-genre instrumental into the new style (which sounded forced). 
3. **Separate ACE's output** again to drop any vocal it generated, keeping the clean new backing.
4. **Mix the original vocal stem** back over that backing (boosted + loudness-normalised).

Result = your original singer over a freshly-composed new-genre backing that fits the melody.
(Costs two separation passes; that's why `-k` is a bit slower, but the backing fits far better.)

```bash
~/.claude/skills/restyle-music/restyle_music.sh \
  -i ./song.mp3 -k \
  -s "lofi jazz: mellow Rhodes electric piano over relaxed hip-hop drums with brushed snare and upright bass, warm and contemplative mood for late-night listening. No heavy bass, no synth leads." \
  -V 1.0 -o ./lofi_keepvocals.mp3
```

- `-k` skips lyrics automatically (so the restyled backing stays instrumental). When using `-k`, the `-s` caption should describe an **instrumental** style (no vocal descriptions).
- The remix defaults are tuned to keep the **backing loud and the lead/melody prominent**: the
  instrumental is boosted (`-M`, default `1.25`) and the whole mix is loudness-normalised to a
  punchy `-13` LUFS (`-N`). Adjust the balance with `-V` (vocal) / `-M` (music) / `-N` (loudness).
- `-V GAIN` balances the kept voice against the new backing (default `1.0`; `1.2`–`1.4` if the
  vocal sits too low, `0.8` if it's too hot). Describe an **instrumental** style in `-s`.
- Needs `~/src/audio-separator` (already deployed; set `AUDIO_SEPARATOR_DIR` to override).
- Caveat: separation isn't perfect — faint bleed/reverb tails of the old backing can remain in
  the vocal stem. For a totally fresh (new) voice instead, run the normal mode without `-k`.
- Want the *vocal itself* re-sung in the new style instead of kept? Omit `-k` and pass the song's
  lyrics with `-l`/`-L` — normal cover re-synthesizes the vocal (a new singer) in the target genre.

## Quick start (one-shot wrapper)

```bash
~/.claude/skills/restyle-music/restyle_music.sh \
  -i ./input_song.mp3 \
  -s "Traditional Japanese wagaku arrangement (和樂). Plucked shamisen and koto, breathy shakuhachi bamboo flute, deep taiko drums, elegant ceremonial feel with pentatonic min'yo folk atmosphere, slower contemplative tempo, acoustic and organic. No electric guitar, no synthesizer, no drum machine." \
  -o ./restyled.mp3
```

With more control (looser style transfer + keep the vocal by supplying lyrics):
```bash
~/.claude/skills/restyle-music/restyle_music.sh \
  -i song.wav -s "lofi jazz: mellow Rhodes electric piano over relaxed hip-hop drums with brushed snare and upright bass, warm and contemplative mood for late-night listening. No heavy bass, no synth leads." \
  -S 0.45 -l ./lyrics.txt -o lofi.mp3
```

### From YouTube / a URL

`-i` also accepts a **URL** (YouTube, etc.) — the wrapper runs `yt-dlp` to download the audio
first, then proceeds exactly as for a local file. No need to download by hand.

```bash
~/.claude/skills/restyle-music/restyle_music.sh \
  -i "https://youtu.be/XXXXXXXXXXX" -k \
  -s "Traditional Japanese wagaku arrangement (和樂). Plucked shamisen and koto, breathy shakuhachi flute, deep taiko drums, elegant ceremonial pentatonic folk feel, acoustic and organic atmosphere. No electric instruments, no synthesizer, no drum machine." \
  -S 0.5 -o ./wagaku.mp3
```

(Equivalent manual step if you'd rather: `yt-dlp -x --audio-format wav -o song.wav "<url>"`,
then pass `-i song.wav`.)

Options:
- `-i FILE|URL` — **input audio**: a local file (any ffmpeg-readable: mp3/wav/flac/m4a…) **or** a
  YouTube/other URL (auto-downloaded via `yt-dlp`). Required.
- `-s TEXT` — **target style description** (required). Must follow the official four-part
  format: `[Genre label]. [Specific instruments/arrangement]. [Mood/atmosphere/scene]. No X, No Y.`
  Write a complete descriptive paragraph **in English**, never just comma-separated tags, and keep
  it **under ~512 chars** (longer is truncated). See **Caption format** section above for examples.
- `-o OUT`  — output path. `.mp3` re-encoded (default `256k`); `.wav`/`.flac` = lossless. Default `./restyled.mp3`.
- `-S NUM`  — `audio_cover_strength` 0.0–1.0 (default **0.5**). **Lower = freer / more style change**;
  **higher = stays closer to the source**. Guidance:
  - **Plain cover** (no `-k`, restyling the whole mix): ACE-Step officially recommends **~0.2 for
    style transfer**. Going higher (0.4–0.6) keeps it too close to the original and can produce
    *forced/weird instruments*. Use 0.2–0.3 for a clean genre swap.
  - **`-k` (vocal-as-source)**: the source is just the vocal, so **~0.5** works well — enough
    freedom to compose a new-genre backing while still following the sung melody. Lower if the
    backing drifts off the melody; this is the main knob to tune.
- `-l FILE` / `-L "inline"` — lyrics (file or inline, `\n` = line break). Optional; supplying the
  song's lyrics helps keep clean vocals on vocal tracks. Omit for instrumental-ish sources.
- `-g LANG` — vocal language hint (`en`,`zh`,`ja`,…; default `auto`→en).
- `-q N`    — diffusion steps (default 8, turbo). More = slightly cleaner, slower.
- `-m NAME` — LM checkpoint (default `acestep-5Hz-lm-0.6B`; cover skips the LM so this rarely matters).
- `-b RATE` — mp3 bitrate (default `256k`).
- `-k`      — **keep the original singing voice** (separate → restyle instrumental → remix vocal). See above.
- `-V GAIN` — vocal gain for the `-k` remix (default `1.0`).
- `-M GAIN` — **music/instrumental gain** for the `-k` remix (default `1.25`, so the new backing &
  lead melody sit forward). Raise for a louder/more prominent backing, lower to favour the vocal.
- `-N LUFS` — final loudness target for the `-k` mix (default `-13`, true-peak −1 dB; louder/punchier).
  Less negative = louder (e.g. `-11`); more negative = quieter (e.g. `-16`).
- `-B BPM` — lock the new backing's tempo to this BPM (conditions ACE's `bpm`). For `-k` the
  original tempo is **auto-detected** (librosa, separator venv) and passed automatically so the
  backing's beat grid matches the song; `-B N` overrides, `-B 0` disables (ACE auto-estimates).
  Note: this locks *tempo*, not downbeat *phase* — if drums feel offset from the vocal groove,
  tempo matching alone won't fix it.

The wrapper normalizes the input to 48kHz stereo wav, runs the cover on GPU, and encodes the result.
It prints `[restyle] done -> <path>`.

## Tuning — "I want to change X" → use this option

Every adjustment a user is likely to ask for maps to a specific option. Pick the matching row;
the wrapper is fast (cover skips LM planning), so iterating on `-S` / the `-s` caption is cheap.

| If the user wants to… | Use | How |
|---|---|---|
| **Change the genre/instrumentation** | `-s "…"` | The core control. Write a full descriptive paragraph: `[Genre]. [Instruments]. [Mood]. No X, No Y.` |
| **Remove a specific instrument** (e.g. drop the guitar/synth) | `-s "…"` | End with `"No electric guitar, no synthesizer, no drum machine."` |
| **Write a better caption** | — | Follow the official four-part format: genre → instruments → mood → exclusions. Never tag-soup. |
| **More style change / "it still sounds like the original"** | `-S` ↓ | Lower it. Plain cover: down to **0.2** (ACE's style-transfer sweet spot); `-k`: ~0.4. |
| **Instruments sound forced / weird** | `-S` ↓ | Too high keeps it glued to the source — lower toward 0.2 (plain cover) for a cleaner render. |
| **Less style change / "it drifted too far, keep the original feel"** | `-S` ↑ | Raise it: `-S 0.75`–`0.9` for a light re-skin. |
| **Lost / mangled the original melody** | `-S` ↑ | Raise `-S`; higher = closer to the source structure. |
| **Keep the ORIGINAL singing voice** | `-k` | Splits vocals out, restyles only the backing, remixes the real voice back. Use an instrumental `-s`. |
| **A brand-new singer (don't keep the voice)** | *(omit `-k`)* | Normal cover re-synthesizes the vocal; pass `-l`/`-L` lyrics for clean diction. |
| **Kept vocal too quiet** (with `-k`) | `-V` ↑ | `-V 1.2`–`1.4`. |
| **Kept vocal too loud / drowns the backing** (with `-k`) | `-V` ↓ | `-V 0.8`–`0.9`. |
| **Garbled / mushy vocals** (without `-k`) | `-l` / `-L` | Supply the real lyrics (file or inline), or describe an instrumental style in `-s`. |
| **Wrong vocal language / accent** | `-g` | `-g ja` / `-g zh` / `-g en` … (default `auto`→en). |
| **Higher audio quality / cleaner result** | `-q` ↑ | More diffusion steps, e.g. `-q 16` (slower). |
| **Faster generation** | `-q` ↓ or `ACESTEP_ROCM_DTYPE=bfloat16` | Fewer steps, or `export ACESTEP_ROCM_DTYPE=bfloat16` (~2× diffusion). |
| **Lossless output** | `-o name.wav` / `.flac` | Any non-mp3 extension = lossless copy (may exceed Discord's 25MB). |
| **Different mp3 quality / file size** | `-b` | e.g. `-b 320k` (higher) or `-b 192k` (smaller). |
| **Use a different ACE-Step repo / models dir** | `ACE_ROOT=…` | Export before the call; `AUDIO_SEPARATOR_DIR=…` for the `-k` separator. |
| **Pin a specific GPU** | `HIP_VISIBLE_DEVICES=N` | Export before the call (default `0`). |
| **Out-of-memory during VAE decode** | `ACESTEP_ROCM_DTYPE=bfloat16` | Halves activation memory; alloc already uses `expandable_segments`. |

Anything not in this table (the LM checkpoint via `-m`, etc.) rarely affects cover output — `-S`
and the `-s` caption do almost all the work.

## Manual run (equivalent)

```bash
cd ~/src/ACE-Step-1.5
ffmpeg -y -i input.mp3 -ac 2 -ar 48000 /tmp/src.wav
# Full ROCm/gfx1151 env the wrapper now fills in automatically (ACE_ENV array in restyle_music.sh):
env -u HSA_OVERRIDE_GFX_VERSION \
  HIP_VISIBLE_DEVICES=0 \
  MIOPEN_FIND_MODE=FAST \
  MIOPEN_USER_DB_PATH=~/.claude/skills/restyle-music/.cache/miopen \
  MIOPEN_CUSTOM_CACHE_DIR=~/.claude/skills/restyle-music/.cache/miopen \
  PYTORCH_HIP_ALLOC_CONF=expandable_segments:True \
  TOKENIZERS_PARALLELISM=false \
  ACESTEP_LM_BACKEND=pt \
  ACESTEP_ROCM_DTYPE=float32 \
  ACE_ROOT=$PWD .venv/bin/python ~/.claude/skills/restyle-music/cover_runner.py \
    --src /tmp/src.wav \
    --caption "lofi jazz: mellow Rhodes electric piano over relaxed hip-hop drums, warm contemplative mood. No heavy bass, no synth leads." \
    --out-dir ./output/restyle --strength 0.6 --steps 8
```

The wrapper sets all of these for you (and for the `-k` separator step too), so a bare
`restyle_music.sh -i … -s …` runs on this box with no extra setup. Override any of them by
exporting it before the call (e.g. `ACESTEP_ROCM_DTYPE=bfloat16` for ~2× faster diffusion).
The pinned `MIOPEN_*` cache means MIOpen only JITs its kernels once; later runs skip the ~JIT.

`cover_runner.py` loads the DiT (turbo) + 0.6B LM (pt backend) and calls
`generate_music(..., task_type="cover", src_audio=..., audio_cover_strength=...)`.

## Performance & hardware (Strix Halo gfx1151, ROCm 7.2)

- Runs on the AMD GPU (AMD Radeon 8060S, 96GB GTT). dtype float32 by default; set
  `ACESTEP_ROCM_DTYPE=bfloat16` for ~2x faster diffusion if needed.
- A ~160s song: model load ~30–60s + **cover generation ~65s** (8 steps; cover skips LM planning,
  so it's faster than text2music's ~141s). Peak VRAM ~21GB.

## Notes / gotchas

- **Never set `HSA_OVERRIDE_GFX_VERSION`** on this box — the repo's stock ROCm launchers default it
  to `11.0.0`, which makes the GPU vanish ("No CUDA GPUs available"). rocm7.2 torch supports gfx1151
  natively; the wrapper already passes `env -u HSA_OVERRIDE_GFX_VERSION`.
- Requires `~/src/ACE-Step-1.5/.venv` with **torch 2.11+rocm7.2** and models in `checkpoints/`
  (DiT `acestep-v15-turbo` + VAE + Qwen3-Embedding + LM `acestep-5Hz-lm-0.6B`). Set `ACE_ROOT` to
  override the repo location.
- Output is 48kHz stereo. A full song's lossless wav can exceed Discord's 25MB limit — send the mp3.
- Harmless startup warnings: torchao CUTLASS `.so` load fail (CUDA-only), LyCORIS/bitsandbytes/
  pytorch_wavelets missing (training/DCW only).
