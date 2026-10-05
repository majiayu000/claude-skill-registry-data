---
name: doctor
user-invocable: true
description: Diagnose and repair a broken or degraded skill-concierge install. Use this skill when the skill-search MCP won't connect, search_skills returns nothing or stale results, skills have gone dark, the MCP seems to run old code after a plugin update, or anything about skill-concierge misbehaves after setup or a plugin update. Runs scripts/doctor.py to check the deployment layer (engine venv, engine freshness, the local index owner, MCP wiring, settings overrides, ledger) and delegates retrieval health to the engine; with --fix it applies safe repairs (start the index owner, reindex, re-apply overrides).
argument-hint: "[--fix]"
next-skills: skill-concierge:flywheel
license: MIT
metadata:
  version: 0.2.2
---

# skill-concierge doctor

A deployment-layer health check with safe auto-fixes. It diagnoses what `setup.sh`
provisions and delegates the retrieval diagnostic (embedder, index, dark/stale skills) to
the engine's own `skill-search --health`, so the two never drift.

## Steps

1. **Diagnose (read-only)** from the plugin root:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/doctor.py"
   ```

   It prints a check matrix and an overall `status: OK | WARN | FAIL` (exit `1` on FAIL).

2. **Read the matrix.** Each row is `[✓|!|✗] <check>  <detail>`:

   | Check | What it verifies |
   |-------|------------------|
   | Python 3.10-3.12 | a usable interpreter (only when the venv is missing) |
   | Engine venv | the stable venv + `skill-search` bin exist |
   | Engine freshness | the venv's COPIED engine matches the deployed vendored source — catches a **stale MCP serving old code after `/plugin update`** (the venv is built once by setup.sh and never refreshed by an update); WARN → rerun setup.sh |
   | MCP wiring | `.mcp.json` is valid + `bin/skill-search-mcp` is executable |
   | Index owner | the local index owner (ADR-0070; replaces the Qdrant container and the Docker embed shim) answers its Qdrant-compatible REST port + `/health`, its `code_version`, and its SQLite file's integrity/point counts |
   | Retrieval health | engine `--health`: embedder reachable, no dark/stale skills, index fresh |
   | Multi-vector layer | trigger points present (MAX-pool retrieval, ADR-0012); WARNs if `SKILL_MULTIVECTOR` is on but none exist |
   | Corpus health | per-skill calibration `ok`/`weak`/`no-signal` counts from `eval/thresholds.json` |
   | Retrieval flywheel | is the utterance-generation LLM configured + reachable, per-skill utterance coverage (which skills lack utterances), and the **last flywheel run** from the global manifest (`~/.claude/skill-concierge/flywheel-manifest.json`). Read-only, **fail-open** (never FAIL — the flywheel is optional). [ADR-0027](../../docs/adr/0027-flywheel-first-class-multi-provider.md) |
   | Trigger hygiene | junk **already stored** in the utterance layer — empty / one-char / repeated phrases a degraded model wrote. Coverage only measures *presence*, so such a skill still counts as "covered" and the generator then skips it forever; this row is what catches it. WARN + auto-fix (purge). Read-only, fail-open |
   | Settings overrides | `skillOverrides` applied to `~/.claude/settings.json`; now **detects drift** from the installed catalogue (`apply-overrides.py --check`) → WARN + auto-fix (ADR-0025) |
   | Ledger dir | the telemetry log directory is writable |
   | Duplicate MCP | warns if a leftover user-scope `skill-search` MCP also exists |
   | MCP reachable | warns when the skill-search MCP is installed but **not connected here** — disabled for the project via `/mcp`, pending approval, or failed. Every other row answers *is the index healthy*; this one answers *can the agent reach it*, and the two come apart: a project-disabled MCP leaves the engine fully green while `search_skills` / `get_skill` do not exist for that session. The enforcer's per-turn offer is unaffected (it queries Qdrant over REST), so WARN not FAIL. Read-only, fail-open, no auto-fix — re-enabling is a user action |

3. **Auto-fix the safe failures:**

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/doctor.py" --fix
   ```

   `--fix` applies only fast, safe repairs, then re-checks: start a stopped index owner
   (also stopping + disabling a revived `skill-search-qdrant`/`skill-concierge-embed-shim`
   container if an old harness copy brought Docker back onto the owner's ports),
   `--reindex` a stale/dark index, re-apply the settings overrides, purge
   junk utterance layers. It never builds or refreshes the keep-off map — that is consent-only
   (ADR-0077); the `Keep-off` row only reports.

   > **Heads-up:** the overrides fix writes `~/.claude/settings.json` (backed up first) via
   > `scripts/apply-overrides.py`. The user invoking doctor is consent for that; mention it
   > before running `--fix` so the change isn't a surprise.
   >
   > **The `Trigger hygiene` fix DELETES data** — it drops each junk utterance layer from
   > the canonical corpus `~/.claude/skill-concierge/triggers.json` (backed up to `triggers.json.bak-junk-<ts>` first) and clears that
   > skill's generation-cache key, then reindexes. It does **not** regenerate: doctor never
   > calls the LLM. A purged skill falls back to description+body retrieval (no worse than
   > junk phrases pointing the wrong way) until the next flywheel run rewrites it — which it
   > now will, because the cleared cache key stops the generator skipping it as "covered".

4. **Handle what `--fix` can't.** doctor never auto-builds the venv or the container
   (slow, heavyweight). If `Engine venv` is FAIL **or `Engine freshness` is WARN**, run the
   **`skill-concierge:setup`** skill (or `./setup.sh`) — that rebuilds/refreshes the stable
   venv from the deployed source. For a duplicate MCP, run the printed `claude mcp remove`
   command. After any fix, **restart Claude Code** if the MCP wiring or engine changed.

## Symptom → check shortcuts

- **`/mcp` shows skill-search not connected** → `Engine venv` / `MCP wiring`. Fix: run setup.
- **search behaves like an OLD version after a plugin update** → `Engine freshness`. The MCP venv
  is stale (copied engine, not refreshed by `/plugin update`). Fix: rerun setup.sh, then restart.
- **search returns nothing or stale** → `Index owner` / `Retrieval health`. Fix: `--fix` (reindex)
  — note the SessionStart `auto_reindex` hook now self-heals index staleness in the background.
- **`Keep-off` row** only reports; `--fix` never touches the map (ADR-0077). No map, or a map
  without `"approved_by_user": true`, hides nothing and is OK (an unapproved map's names are
  reported as ignored). WARN means the file is invalid JSON or has no `keep_off` list. To get
  suppression, run `python3 scripts/build_keep_off.py` to see a proposal and `--apply` only after
  Thinh says yes. A skill you take inline that gets dropped → add it to keep-on (exempt).
- **skills you expect aren't offered / a new skill leaks its full description** → `Settings overrides`
  (now flags override **drift**). Fix: `--fix` (re-apply) — or nothing: the SessionStart
  `auto_overrides` hook self-heals the budget on drift (ADR-0025).

Full landmine reference: `docs/caveats.md`.
