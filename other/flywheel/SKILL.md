---
name: flywheel
user-invocable: true
description: See the retrieval-flywheel status and trigger an incremental utterance-generation run. Use this skill when the user asks about the flywheel, "how many skills have utterances / triggers", "flywheel coverage", "which skills are missing utterances", "is the LLM endpoint configured/reachable", or wants to "generate triggers", "run the flywheel", "refresh utterances", or "index the new skills' utterances". The flywheel is the utterance layer (ADR-0026) that teaches the retriever how users actually ask for a skill (EN+VN), lifting recall. Runs scripts/flywheel.py — status mode (default, read-only) prints endpoint config + reachability and per-skill utterance coverage (N/M covered, and the missing skills by name); --generate runs the incremental generator (only new/changed skills hit the LLM) then reindexes so the new points go live, printing before/after coverage. Generation fails loud if the LLM endpoint is unreachable.
argument-hint: "[--generate] [--rate <seconds>] [--catalog <alias>] [--workers <N>]"
license: MIT
metadata:
  version: 0.1.2
---

# skill-concierge flywheel

Surface and drive the **retrieval flywheel** — the utterance layer (ADR-0026). For each
indexed skill the flywheel stores short, LLM-generated "how a user actually asks for this"
phrases (English + Vietnamese) under `llm_triggers` in the canonical corpus
`~/.claude/skill-concierge/triggers.json` (operator home — personal data, kept out of the
public repo since 0.37.0); those phrases
lift retrieval recall. Generation is **offline and incremental** — the generator
content-hashes each skill, so only new or changed skills ever hit the LLM. Skills with no
utterances still work (graceful fallback to description+body retrieval); the flywheel just
makes them easier to find.

This skill is the seamless surface for two things: **seeing** where the flywheel stands, and
**running** an incremental generation pass.

## Steps

1. **Status (default, read-only)** — endpoint config + reachability and per-skill coverage:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/flywheel.py"
   ```

   It prints the full observability card:
   - **Endpoint** — the configured `FLYWHEEL_LLM_ENDPOINT` + model, whether an API key is
     set, the schema mode, and a live `ping()` reachability result.
   - **Coverage** — installed `N/M` plus one line per configured external catalog
     (`antigravity: N/M`), with missing skills by name. Indexed names come from the live
     Qdrant `claude_skills` index; covered = a non-empty `llm_triggers.triggers` in
     the canonical corpus at `~/.claude/skill-concierge/triggers.json`.
   - **State** — lock free vs `IN PROGRESS`; while a run holds the lock (including the
     detached auto-flywheel pass) status samples coverage twice (5s) and prints live
     throughput + ETA — the only way to observe a detached run's progress.
   - **Auto-flywheel** — gate value, workers/cap/throttle config, throttle-window
     countdown from the machine stamp, and the last hook log line.
   - **Recent runs** — the last 3 manifest runs (model, generated/error/skipped,
     coverage, last_error) plus per-skill error detail from the most recent run.

2. **Generate (`--generate`)** — fill utterances for new/changed skills, then reindex:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/flywheel.py" --generate
   ```

   It preflights the endpoint with `ping()` and **fails loud** if unreachable (pointing at
   the provider-setup doc — do not generate against a dead endpoint). On success it runs BOTH
   incremental generators — the eval scenarios (`llm_eval_gen.py`) and the utterance triggers
   (`llm_triggers.py`), under the engine venv — then `skill-search --reindex` so the new
   utterance points land live, and prints before/after coverage. Only new/changed skills call
   the LLM (each generator content-hashes the description), so re-running when nothing changed
   is cheap and safe. Every run is recorded to the global manifest (below).

   Flags: `--triggers-only` skips the measurement-only scenario pass (triggers are what serve
   retrieval); `--limit <N>` caps how many skills are processed in one pass; `--rate <seconds>`
   spaces out LLM calls when sharing a busy endpoint; `--catalog <alias>` runs generation
   against ONE external catalog's `<alias>:*` skills instead of installed skills (the
   ADR-0031 D10 deferral, owner-commissioned — default coverage counts stay installed-only);
   `--workers <N>` fans the LLM network phase out over N concurrent calls while all file
   writes stay single-threaded (default 1 = sequential; effective gateway load scales with
   N). Full rationale: [ADR-0043](../../docs/adr/0043-catalog-flywheel-generation-and-bounded-parallel-workers.md).

## Auto-flywheel (background, default ON) + the run manifest

You usually do **not** need to run `--generate` by hand. The **`auto_flywheel`** SessionStart
hook (ADR-0027, gated `SKILL_AUTO_FLYWHEEL`, **default ON**) does it for you: when an endpoint is
configured **and** reachable, on session start it detects skills missing utterances, generates for
just those, and reindexes — **detached and non-blocking** (it never delays the session), throttled
(`AUTO_FLYWHEEL_THROTTLE_S`, default 6h) and capped per run (`AUTO_FLYWHEEL_MAX_PER_RUN`, default 25).
If no endpoint is configured or it's unreachable, the hook is a **silent no-op** — the graceful
description+body fallback is untouched.

Because the run is a background process, its results are written to a **global manifest** at
`~/.claude/skill-concierge/flywheel-manifest.json` — timestamp, endpoint+model, per-skill status,
totals, coverage, last error (last 20 runs). Any agent or the user can read it to verify what the
flywheel did, without watching a live process. Status mode (above) prints the last run from it, and
`doctor` reports it too.

## When it can't run

- **Endpoint unreachable** → `--generate` fails loud. Configure a provider first; the three
  documented setups (LM-Studio, Ollama, OpenAI-compatible gateway) live in
  `references/flywheel-llm-providers.md`. The four `FLYWHEEL_LLM_*` env vars belong in the
  machine's cross-harness env file `~/.config/harness-env.sh` (sourced by `~/.zshenv` +
  the bash entry files), NOT in `~/.claude/settings.json` env — the settings env block
  reaches Claude sessions only, so a Codex session's doctor reported "not configured"
  against a fully configured machine and its auto_flywheel silently no-opped
  ([caveats §20](../../docs/caveats.md)). Status mode still works — it just reports NO.
- **Engine venv missing** → `--generate` points you at the **`skill-concierge:setup`** skill,
  which builds the venv. After a reindex, retrieval picks up the new points immediately (no
  restart needed).

Doctor's `check_flywheel()` reports the same coverage + reachability inside the normal health
workflow; this skill is the place to **act** on it.
