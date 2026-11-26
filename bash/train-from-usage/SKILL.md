---
name: train-from-usage
description: Use when building the session-to-brain training pipeline.
version: 1.4.0
author: OpenAmer Agent
license: MIT
metadata:
  openamer:
    tags: [training, brain-data, a2a, self-improvement, sessions, trajectories]
    related_skills: [capture-thinking, self-modify, openamer-agent]
---

# Train from Usage — Session Data Pipeline

## Overview

OpenAmer captures **every session, every response, every tool result** as a
training trajectory. This is the "provably improves with use" axis made
concrete: the more you use OpenAmer, the more data exists to fine-tune the next
generation of the model.

The pipeline works automatically — no manual setup, no cron job required since
commit 77c34917f (v1.3):

1. **Background daemon** (`session_to_brain.py --watch`) — spawned at every
   `openamer` startup. Polls the state DB every 60 seconds and writes NEW
   session trajectories to a **staging file** at
   `~/.openamer/trajectories/daemon-trajectories.jsonl` (rich format with
   ``_fingerprint`` for dedup).
2. **Periodic consolidation** — every 5 cycles (~5 min) the daemon runs
   ``openamer a2a brain collect`` as a subprocess. This reads ALL trajectory
   files + mesh memory and writes the canonical **ChatML-format** brain dataset
   at `~/.openamer/a2a/openamer-brain.jsonl`.
3. **Manual run** — `python scripts/session_to_brain.py` also triggers
   ``brain collect`` after export if new records were found.
4. **Manual insights** — the agent saves key decisions via `a2a meshlearn auto`.

**Format isolation:** The staging file (daemon-trajectories.jsonl) uses a rich
format with ``_fingerprint``, ``_session_id``, ``stats`` etc. for reliable
dedup. The brain dataset (openamer-brain.jsonl) uses a minimal ChatML format
(``messages`` + ``engine`` only). `brain collect` is the **sole producer** of
the ChatML file — the daemon never writes to it directly. This prevents the
pre-v1.3 bug where daemon + brain collect wrote incompatible formats to the
same file, causing data loss every time `brain collect` overwrote the daemon's
rich-format records.

## When to Use

- The user asks about training data, brain fine-tuning, or self-improvement.
- You set up a new OpenAmer and need to enable the data pipeline.
- You need to check whether session data is being captured correctly.
- The user asks "why hasn't anything been saved?" — this is the skill to
  diagnose the problem.

## Quickstart (new install)

Nothing to do. The daemon starts automatically. Verify:

```bash
# Check autolog is ON (default):
openamer a2a brain autolog status

# Check existing brain data:
wc -l ~/.openamer/a2a/openamer-brain.jsonl

# Manually trigger an export (if daemon hasn't polled yet):
python scripts/session_to_brain.py
```

## The Pipeline

### Layer 1: Background Daemon (REAL mechanism — since commit 77c34917f)

The daemon (`openamer_cli/session_to_brain_daemon.py`) is spawned in
`openamer_cli/main.py` at startup (line 15146-15148). It runs
`scripts/session_to_brain.py --watch` as a silent subprocess.

```
state.db (SQLite, sessions)  →  session_to_brain.py --watch (every 60s)
                                ↓
  ~/.openamer/trajectories/daemon-trajectories.jsonl   (staging, rich format)
                                ↓
  every 5 cycles: openamer a2a brain collect           (consolidation)
                                ↓
  ~/.openamer/a2a/openamer-brain.jsonl                 (canonical, ChatML)
```

**No cron job needed. No user action needed.** The daemon is non-fatal — if
the script is missing or fails, the rest of OpenAmer works fine.

The daemon:
- Writes to a STAGING file in `~/.openamer/trajectories/` — NOT directly to
  the brain dataset. This prevents format conflicts with `brain collect`.
- Every 5 cycles (~5 min), runs ``openamer a2a brain collect`` as a subprocess
  to consolidate staging data + mesh memory into the canonical ChatML brain
  dataset.
- On manual run (non-watch mode), triggers `brain collect` immediately after
  export if new records were found.
- Deduplicates by fingerprint (session_id + first-5-messages content hash)
- Runs silently (stdout/stderr to DEVNULL)
- Persists its PID to `~/.openamer/session_to_brain.pid` and checks it on
  spawn to avoid duplicates

**Diagnostic commands:**

```bash
# Check if daemon is running:
cat ~/.openamer/session_to_brain.pid
```

### Layer 2: Thinking Insights (Manual)

Thinking blocks are **not** in the state DB — only the final assistant message
is. Use `a2a meshlearn auto` to save key decisions:

```bash
openamer a2a meshlearn auto "<lesson>" --topic "<category>"
```

**CRITICAL PITFALL — Windows npm timeout:**
On Windows, `meshlearn auto` with a long insight text triggers a full
`npm install` (desktop app dependencies). If the insight text is > 200
characters, the command can timeout (20-25s) while npm resolves deps.
**Keep insight text under 200 characters** or the insight is still adopted
(verified) but the command appears to fail.

If timeout occurs, the insight is usually still saved — verify with:

```bash
grep "<topic>" ~/.openamer/MEMORY-official-mesh.md
```

### Layer 3: Brain Dataset

```bash
openamer a2a brain collect
```

Merges trajectories + mesh insights into `~/.openamer/a2a/openamer-brain.jsonl`.
Two record types:
- `trajectory` (engine: trajectory) — full session transcript, signed
- `insight` (engine: learn) — signed distilled lesson

**Dual-brain-file pitfall:** `brain collect` writes to `~/.openamer/a2a/` (user
home directory). There is ALSO a stale copy at
`$OPENAMER_HOME/a2a/openamer-brain.jsonl` (app-data dir) that is NOT updated by
`brain collect`. Always read the home-dir copy. The app-data copy is an artifact
from pre-v1.1.

## Real-World Sizing

| Usage Time | Brain Records | File Size |
|---|---|---|
| ~12h (1 heavy day, BEFORE daemon fix) | 9-10 (bulk-exported at 02:44) | ~900 KB |
| ~20h (AFTER daemon fix, 35 total) | 35 (34 trajectory + 1 insight) | ~9 MB |
| ~48h (active use) | ~40-50 | ~10-15 MB |
| ~1 week | ~150-200 | ~20-30 MB |
| ~1 month (daily use) | ~600-800 | ~80-120 MB |

Target for a useful LoRA fine-tuning: **200-500 sessions** (~2-6 weeks).

## Verification

```bash
# Brain dataset (ChatML format — should NEVER contain _fingerprint):
wc -l ~/.openamer/a2a/openamer-brain.jsonl

# Record types:
python3 -c "
import json
with open(r'~/.openamer/a2a/openamer-brain.jsonl') as f:
    types={}
    for l in f:
        d=json.loads(l); t=d.get('engine','?')
        types[t]=types.get(t,0)+1
    print(types)
"

# Format validation (must NOT be rich-format with _fingerprint):
python3 -c "
import json
with open(r'~/.openamer/a2a/openamer-brain.jsonl') as f:
    for i,l in enumerate(f,1):
        d=json.loads(l)
        assert 'messages' in d, f'Row {i}: missing messages'
        assert 'engine' in d, f'Row {i}: missing engine'
        assert '_fingerprint' not in d, f'Row {i}: ChatML must not have _fingerprint'
    print(f'All {i} rows valid ChatML')
"

# Staging file (should be in trajectories/, may have _fingerprint):
wc -l ~/.openamer/trajectories/daemon-trajectories.jsonl 2>/dev/null || echo "No staging file yet"

# Insights in memory:
grep "source :" ~/.openamer/MEMORY-official-mesh.md

# Daemon running:
cat ~/.openamer/session_to_brain.pid 2>/dev/null && echo "Daemon PID exists"

# Full pipeline test (dry-run — no writes):
python /path/to/scripts/session_to_brain.py --dry-run
```

## References

- `references/openamer-session-data-architecture.md` — Dokumentiert die
  tatsächlichen Datenquellen für Session-Analyse: `state.db:messages` (primär,
  241k Messages, 12k Sessions), `sessions.db` (leer), `sessions/*.json` (nur
  Error-Dumps). Enthält SQL-Query-Patterns und Metrik-Definitionen.
- `references/windows-a2a-pitfalls.md` — Windows-specific pitfalls observed in
  production (npm timeout, dual brain files, cron setup, real-world sizing)
- `references/format-conflict-fix.md` — Runtime debugging and fix for the
  daemon vs brain-collect format conflict (pre-v1.3)
- `references/cpu-finetune.md` — Proven CPU LoRA fine-tune pipeline
  (distill brain → SFT pairs → peft/Trainer → :8081 server; GGUF/Ollama
  blocker for Qwen3.5 hybrid arch documented). Includes `auto_retrain.py`
  nightly cron ops (guards: 24h interval, ≥10 new records, ≥8 GB free RAM,
  adapter hot-swap; restart server after swap) and the provider-registration
  note: patch tool refuses config.yaml — edit via python+PyYAML with a .bak,
  add provider under custom_providers only, never touch model.provider/default.
  Metric correction: usable SFT **pair yield** (~79 from 2,862 trajectories,
  ≈2.8%) is the progress metric, not raw session count.
- `references/energy-efficiency-2026-09-02.md` — The energy path to ASI:
  embedding cache (1381→10 ms), mini-server idle shutdown (~800 Wh/day saved),
  dream-weighted SFT (recurring nightmares 3x duplicated, Hebbian-style).
  Context: GPU-Backprop is ~14 Mio× the energy of biological learning —
  local+sparse+sleep-based is the strategic direction.

## Pitfalls

1. **meshlearn auto on Windows triggers npm install.** The insight text
   triggers a desktop-app dependency resolution. Keep text under 200 chars to
   avoid timeout. Command timeout does NOT mean the insight was lost — verify
   with `grep` in memory.
2. **brain collect overwrites the brain dataset.** It is a merge/rebuild, not
   an append. The daemon writes to a staging file
   (`~/.openamer/trajectories/daemon-trajectories.jsonl`) which `brain collect`
   reads — so the canonical file always reflects all data.
3. **Format conflict (pre-v1.3).** The daemon and `brain collect` wrote
   incompatible formats to the same file. Fixed in v1.3 by having the daemon
   write to a staging file. Verify the brain dataset is valid ChatML:
   ``python -c "import json; assert '_fingerprint' not in json.loads(open(r'~/.openamer/a2a/openamer-brain.jsonl').readline())"``.
4. **Thinking blocks are not captured.** Only the final assistant message
   lands in the state DB. Always use `a2a meshlearn auto` for key reasoning.
5. **Autolog must be ON.** Check with `openamer a2a brain autolog status`.
   Default is ON but can be toggled off.
6. **Daemon dies with the parent process.** When the desktop app is killed
   (e.g. via taskkill), the daemon dies too — it is a subprocess. On next
   `openamer` startup it respawns automatically.
7. **Windows: `session_to_brain.py` path.** For manual export, use the full
   Windows path to the script (not MSYS). The daemon (spawned from main.py)
   resolves the script relative to `openamer_cli/` and works regardless of
   shell.
8. **Windows `spawn()` UnicodeDecodeError = daemon never starts.** In
   `openamer_cli/session_to_brain_daemon.py`, the "already running" check runs
   `tasklist /FI "PID eq <old>"` with `text=True`. On a Windows codepage that
   emits bytes >= 0x80 (`0x81` etc.), `subprocess.run` raises
   `UnicodeDecodeError` — this makes `spawn()` CRASH *before* it can start the
   daemon, so the learning pipeline appears "down ~every hour" (each CLI start
   re-crashes at the stale-PID check). **Fix:** run `text=False` and decode the
   bytes with `errors="replace"`: `out = (r.stdout or b"").decode("utf-8",
   "replace")`. Distinct from pitfall #6 (parent-death): #8 is a hard crash at
   spawn. Verify with `python -c "... session_to_brain_daemon.spawn()"` — it
   must print a pid, not traceback.