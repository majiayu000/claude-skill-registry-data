---
name: text-to-speech
description: >-
  Use when you need to convert a text document to an audio file via a local TTS
  pipeline. Outputs MP3. Handles narrative rewrite, text normalization, prosody
  prep, and audio render. Backend is configurable. Triggers: text to speech,
  narrate document, make audio from text, synthesize speech, TTS, MP3 from
  document, convert to podcast, audio version of document.
globs: []
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "3.0.0"
---

# text-to-speech

Converts a text document to an MP3 audio file via a local TTS pipeline. The skill ships a wrapper script (`synth-audio.sh`) with a clean `text → audio-file` interface. The current backend is Kokoro-82M; swapping backends is a config change.

> **Does NOT install any TTS backend.** See [Backend Dependencies](#backend-dependencies).

> **v2.0.0 breaking change:** the narrative rewrite (L1) no longer runs
> automatically inside `synth-audio.sh`. If you're a driving Claude Code
> agent, dispatch a rewrite subagent first — see [L1 Narrative Rewrite](#l1-narrative-rewrite--dispatch-a-subagent-do-this-first)
> below — this is the normal way to use the skill now, not an edge case.
> A bare `synth-audio.sh input.md output.mp3` with no existing
> `narrative.txt` now fails loudly instead of silently shelling out to
> `claude --print` (that nested call could inherit your session's output
> style/CLAUDE.md and leak meta-commentary into the audio — see
> [L1 Narrative Rewrite](#l1-narrative-rewrite--dispatch-a-subagent-do-this-first)
> for why). For headless/standalone use, pass `--allow-inline-llm-rewrite`.

## Quick Start

```bash
${CLAUDE_SKILL_DIR}/scripts/synth-audio.sh input.md output.mp3 --skip-layer 1
# ^ requires <output.mp3>.workdir/narrative.txt to already exist — see
#   "L1 Narrative Rewrite" below for how to produce it (subagent dispatch)
```

Copy and configure backend settings (optional):

```bash
cp ${CLAUDE_SKILL_DIR}/templates/synth-backend.yaml.example ./synth-backend.yaml
# Edit synth-backend.yaml to match your setup
```

## Backend Config (`synth-backend.yaml`)

Place `synth-backend.yaml` in your project root to override CLI defaults:

```yaml
backend: kokoro        # current: kokoro | future: orpheus | ...

kokoro:
  voice: am_puck       # validated voice (R5, 5-round iteration)
  speed: 0.92          # validated speed — see Kokoro backend section
  phoneme_dict: ./phoneme-dict.yaml   # optional IPA overrides
  stress_hints: ./stress.yaml         # optional emphasis overrides
```

See `${CLAUDE_SKILL_DIR}/templates/synth-backend.yaml.example` for annotated defaults.

## Kokoro Backend

When `--backend kokoro` (default), the pipeline runs four layers:
**L1** narrative rewrite (LLM) → **L2** normalization → **L3** prosody prep → **render**

### L1 Narrative Rewrite — dispatch a subagent (do this first)

**If you are the driving Claude Code agent, do this before calling `synth-audio.sh`.**
Do NOT let `synth-audio.sh`/`pipeline.py` shell out to `claude --print` for you —
a nested `claude --print` launched from inside your own session inherits your
active output style, project `CLAUDE.md`, and any other session framing, and
can return meta-commentary instead of a rewrite (observed failure: a literal
`★ Insight` block rendered into the audio). Dispatching a subagent via the
`Agent`/Task tool gives a genuinely isolated context instead.

1. Determine `<workdir>` = `<output.mp3 path with .mp3 stripped>.workdir` and
   `mkdir -p` it (this matches the directory the backend itself creates).
2. Dispatch **one subagent** (general-purpose) with a self-contained prompt:
   - Read `${CLAUDE_SKILL_DIR}/scripts/backends/prompts/narrative-chapter-focused.md`
     and follow it exactly as the rewrite rules.
   - Read the input document.
   - Output ONLY the rewritten prose with `[[CHAPTER: ...]]` markers — no
     preamble, no explanation, no markdown fences, no commentary about the
     task itself.
   - Instruct it to **write the result directly to `<workdir>/narrative.txt`**
     (via Write) and return only a short status line — don't have it return
     multi-thousand-word prose through the tool result.
   - For documents >5000 words, either let the subagent chunk internally by
     H2, or dispatch one subagent per H2 section in parallel and concatenate
     — this replaces `chunk_and_rewrite.py`'s own `claude --print` calls when
     you're running inside a session.
3. Run:
   ```bash
   ${CLAUDE_SKILL_DIR}/scripts/synth-audio.sh input.md output.mp3 --skip-layer 1 [other flags]
   ```
   `pipeline.py` validates `narrative.txt` (chapter markers present, word
   count plausible vs. the source, no known contamination patterns) before
   continuing to L2/L3/render — if validation fails it exits loudly rather
   than rendering audio from a bad narrative. Re-dispatch the subagent and
   retry.

**Standalone / headless (no driving agent present):** pass
`--allow-inline-llm-rewrite` to `synth-audio.sh`. This falls back to an
isolated inline `claude --print --safe-mode` call inside the pipeline
(`--safe-mode` disables CLAUDE.md auto-discovery, output styles, hooks,
plugins, and custom agents/commands). It's a weaker guarantee than subagent
dispatch — there's no independent process boundary confirming isolation
beyond the flag itself — so `validate_narrative()` still runs as the
backstop either way. Prefer subagent dispatch whenever a driving agent is
available.

### Voice and Speed

- **Voice:** `am_puck` (validated across 5 rounds of iteration)
- **Speed:** `0.92×` — empirical: at 0.95+ the `/s/→/k/` transition in compound nouns like "Six key concepts" slurs to "Zik's"; 0.92 is the last clean value

### Phoneme Dictionary (L3a)

Place `phoneme-dict.yaml` in your project root for project-specific proper nouns:

```yaml
terms:
  MyProduct:
    ipa: "mˈaɪ pɹˈɒdʌkt"
    notes: "Default G2P stresses wrong syllable"
```

**MUST use `[word](/IPA/)` Markdown-link form.** Bare `/IPA/` is not reliably parsed — in Round 4 misaki voiced IPA characters as literal names ("slash D stress I slash"). The backend applies the link form automatically from your dict entries.

⚠️ **Do NOT add entries where default G2P is already correct.** misaki will voice the word twice ("Letta Letta"). Test with `--verify` before committing new entries.

See `${CLAUDE_SKILL_DIR}/templates/phoneme-dict.yaml.example` for format and warnings.

### Stress Hints (L3b)

Place `stress.yaml` in your project root:

```yaml
emphasize:
  - not
  - only
  - critical

deemphasize: []
```

⚠️ **`deemphasize` MUST stay empty.** Round 4 regression: ~650 `(-1)` wraps on articles, pronouns, and linking verbs produced a "timid, reserved" cadence that listeners flagged in review. Known-unsafe: articles (the, a, an), pronouns (I, you, it, they, we), be-forms (is, are, was, were), filler adverbs (just, really, very, quite). Do NOT re-add.

See `${CLAUDE_SKILL_DIR}/templates/stress.yaml.example` for safe examples with commentary.

### Em-Dash Chunking (L3c)

Kokoro only creates chunk boundaries at `.`, `!`, `?`. An em-dash does not force a breath pause. The pipeline converts `X — Y` to `X. — Y` — adding a pause while preserving the em-dash's intonation curve (removing the dash entirely produced flat, mechanical prosody).

### List Prosody (L1 prompt rules)

The narrative rewrite enforces a spoken-list structure:
- Announce list length up front ("Here are six requirements.")
- Period-terminate every item
- Ordinal words (First, Second… Tenth) — not numerals
- Sub-opener topic sentence for items >40 words
- Anchor + capstone for nested sub-lists ("So that is the first tier. Next, the second tier…")

## Whisper Self-Check (`--verify`)

```bash
${CLAUDE_SKILL_DIR}/scripts/synth-audio.sh input.md output.mp3 --verify
```

After render, transcribes the MP3 with Whisper and reports IPA regressions, missing ordinal patterns, and unexpected artefacts. Requires `mlx-whisper` (Apple Silicon; `uv pip install mlx-whisper`).

## ID3 Lyrics (USLT) — narrative debug artefact

The backend embeds the final `narrative.txt` (chapter markers stripped to
plain title lines) into the rendered MP3's ID3 `USLT` (lyrics) frame by
default — the spoken text travels inside the file, so you can compare it
against the source without a separate artefact. Pass `--no-lyrics` to
`synth-audio.sh` to skip it. Read it back with:

```bash
uv run --with mutagen --no-project python -c "
from mutagen.id3 import ID3
id3 = ID3('output.mp3')
for k, f in id3.items():
    if k.startswith('USLT'):
        print(str(f.text))
"
```

## Backend Dependencies

The skill does NOT install or configure backend software. Caller must provide:

- **Kokoro-82M:** `uv pip install kokoro` (hexgrad/kokoro)
- **Python 3.11+** with `uv`
- **ffmpeg:** `brew install ffmpeg`
- **espeak-ng:** conditional dependency — `brew install espeak-ng` as a
  fallback. Kokoro's `misaki` G2P depends on `espeakng_loader`, whose
  bundled `libespeak-ng.dylib` data-path resolution is not reliably correct
  on every install (observed: byte-identical dylib+data works fine from a
  normally-located venv, hard-aborts before Python can flush stdout from a
  venv nested under a long path — it's install-dependent, not universal).
  `kokoro.sh` runs a probe-first preflight (macOS): it actually exercises
  `misaki`'s G2P once, and only if that fails does it symlink the loader's
  dylibs to a Homebrew `espeak-ng` build — silent and a no-op when the
  bundled path already works. If TTS aborts with an `espeak-ng-data` path
  error and you don't have `espeak-ng` installed via Homebrew, that's the
  fallback you need.
- **`VIRTUAL_ENV` must be set** in the calling environment. `misaki`
  auto-installs the `en-core-web-sm` spaCy model via `uv pip install` on
  first use; under `uv run --no-project` with no active `VIRTUAL_ENV` this
  fails with an unhelpful "No virtual environment found" (exit 2, no
  traceback). `kokoro.sh` checks this upfront and fails loudly with the fix
  (`export VIRTUAL_ENV=/path/to/your/venv`) rather than letting the render
  fail deep inside misaki.
- **mutagen:** `uv pip install mutagen` (for ID3 chapter + lyrics injection)
- **mlx-whisper** (optional, for `--verify`): `uv pip install mlx-whisper`

## Known Kokoro Limitations

- **Phoneme doubling:** Adding a phoneme-dict entry where G2P is already correct renders the word twice. Drop the entry; test with `--verify`.
- **Whisper vocabulary gaps:** Novel compounds (atproto → "AppProto"). Gloss in prose on first mention.
- **Chunker edge cases:** `etc.`, `e.g.` may survive L2 normalization. Spot-check the Kokoro text output.
