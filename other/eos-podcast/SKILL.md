---
name: eos-podcast
description: Generate NotebookLM-style two-host podcasts via the EmptyOS Podcast app (port 9000). Use when the user asks to make a podcast, generate an episode, turn a topic or vault content into audio, or schedule recurring podcasts. NOT for slideshow/MV video assembly (use creative-mv-generator) or publishing an episode to a channel (use creative-youtube-ai-engineering).
---

# EmptyOS Podcast

Generate two-host conversational podcasts via the EmptyOS Podcast app on `localhost:9000/podcast`. Output MP3s land in the vault podcast folder (`30_Resources/EmptyOS/podcast/`) and are indexed automatically — playable at `http://localhost:9000/podcast/`.

## When to Use

| User says | Mode |
|-----------|------|
| "make a podcast about X", "generate podcast on Y" | Topic — Mode 1 or Mode 2 |
| "podcast with this briefing…", "use this exact context" | Rich context — **Mode 2 (two-step)** |
| "daily podcast", "podcast from today's journal" | Vault-auto — Mode 3 |
| "list podcasts", "what episodes do I have" | `GET /podcast/api/files` |

## Pre-flight

EmptyOS daemon must be running:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9000/podcast/
# Expect 200. If not, ask Kevin to run restart.bat — never start :9000 from a
# session (.claude/rules/daemon-handling.md).
```

Voice pairs, duration presets, and image styles are discoverable:

```bash
curl -s http://localhost:9000/podcast/api/voice-pairs | python -m json.tool
```

Current presets:
- **Voice pairs**: `en_mf`, `en_ff`, `en_mm`, `zh_mf`, `zh_ff`, `zh_mm`, `bi_mf` (bilingual), plus custom XTTS clones (e.g. `kevin_f`)
- **Durations**: `short` (6 segments, ~3 min), `medium` (12 segments, ~6 min), `long` (20 segments, ~12 min)

## Mode 1 — Topic Only (simple, one-shot)

Use when the LLM can freely research / invent the content from the topic string.

```bash
curl -s -X POST http://localhost:9000/podcast/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "TOPIC HERE",
    "voice_pair": "en_mf",
    "duration": "medium",
    "language": "en",
    "cover": true,
    "video": false
  }'
```

Returns either `{"job_id": "...", "mode": "async"}` (worker pool queued) or `{"mode": "sync", "result": {...}}` (inline).

For async, poll: `GET /podcast/api/job/{job_id}` until `status: "completed"`.

## Mode 2 — Rich Context (two-step) — **use for prep/briefing podcasts**

**Why two steps**: `/api/generate` alone doesn't accept a `context` field (the web route strips it). If the LLM must be grounded in specific facts (interview prep, factual briefings, named people/projects, exact phrasings to reuse), generate the script first with `/api/script` which DOES accept `context`, then submit that script to `/api/generate`.

This also lets you (or the user) review and edit the script before burning TTS time.

### Step A — Script with grounded context

```bash
curl -s -X POST http://localhost:9000/podcast/api/script \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Short title, used for the filename slug",
    "context": "FULL BRIEFING THE LLM MUST USE VERBATIM — names, facts, quotes, constraints, what NOT to say.",
    "duration": "long",
    "language": "en"
  }' > /tmp/script.json
```

Response: `{"topic": "...", "script": [{"speaker": "A", "text": "..."}, ...], "duration": "long", "language": "en"}`

### Step B — Generate audio from the script

```bash
SCRIPT=$(python -c "import json; d=json.load(open('/tmp/script.json')); print(json.dumps(d['script']))")

curl -s -X POST http://localhost:9000/podcast/api/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"topic\": \"Short title\",
    \"script\": $SCRIPT,
    \"voice_pair\": \"en_mf\",
    \"duration\": \"long\",
    \"cover\": true,
    \"video\": false
  }"
```

### Context-field best practices (lessons from real failures)

1. **Name the domain explicitly and disambiguate homonyms.** If the topic contains a word that collides with something famous, say so. Example: "This is about Endeavour Energy, the Australian electricity distributor — NOT Endeavor Global the entrepreneur network. NEVER talk about founders, scale 10x, or pitch decks."
2. **List proper nouns the script must use**: people, projects, tools, standards. The LLM will anchor on them.
3. **Say what NOT to do.** Negative examples are highest-leverage for keeping the LLM on-topic.
4. **Give verbatim phrasings** when the user should be able to reuse lines from the podcast.
5. **End the context with a CLOSE line** the hosts should say, so episodes thread together.

### Splitting long content

`long` = ~12 min. For 30–60 min of content, split into **N episodes × long** rather than one "extra long" request. One episode per coherent theme. Fire sequentially — the Claude CLI script-gen has a global lock. Chain in a single bash script running in background.

## Mode 3 — Vault Auto-Generate

```bash
curl -s -X POST http://localhost:9000/podcast/api/auto \
  -H "Content-Type: application/json" \
  -d '{
    "source": "vault_daily",
    "language": "en",
    "duration": "short",
    "cover": true,
    "video": false
  }'
```

Sources: `vault_daily` (today's journal + frogs + tasks), `vault_random` (discovery across vault), `vault_dictionary` (word-of-the-day deep dive).

## Listing & Playback

| What | How |
|------|-----|
| All episodes (JSON) | `GET /podcast/api/files` — `{files: [...], dir, count}` |
| Episode history (metadata only) | `GET /podcast/api/history` |
| Single episode metadata | `GET /podcast/api/history/{id}` |
| Stream MP3 | `GET /podcast/api/audio/{filename}` |
| Web UI | `http://localhost:9000/podcast/` |

Audio directory resolves via:
1. `podcast.audio_dir` setting if present and exists
2. Else `self.vault_dir` — typically `{vault}/30_Resources/EmptyOS/podcast/`

## After Generation

1. Report filename, segment count, duration, and the UI URL: `http://localhost:9000/podcast/`.
2. If the user asked for a standalone copy outside the vault podcast folder, `cp` after generation.
3. All episodes belong in the vault podcast folder — never scatter copies into ad-hoc directories.

## Common Failure Modes

- **HTTP 500 with a long `topic` field**: the topic is slugged for the filename and hits length limits. Keep `topic` short (< 80 chars); put detail in `context`.
- **LLM hallucinates a wrong interpretation of the domain**: Mode 1 + an ambiguous topic = confident nonsense. Switch to Mode 2 with an explicit disambiguation line in `context`.
- **Script comes back empty or JSON parse fails**: retry. If repeated, `eos health` and check the `think` capability (Claude CLI or OpenAI/Ollama).
- **Files written but not visible in UI**: check `GET /podcast/api/files` — the UI is a thin shell over that endpoint.

Legacy pre-EmptyOS episodes (retired 2026-07): one-time import via `POST /podcast/api/import-hp` (reads old JSON sidecars into EOS history), or copy MP3 + `.json` sidecar + `_cover.png` into the vault podcast folder.

## Known Gaps

- `POST /api/generate` does not currently forward a top-level `context` field to `_full_generate` — that is why Mode 2 requires the two-step flow. If you want a single-call rich-context generate, patch `apps/personal/podcast/app.py` `api_generate` to pass `context=data.get("context", "")` into `_full_generate` and through to `_generate_script`.
