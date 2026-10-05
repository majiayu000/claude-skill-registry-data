---
name: cyber-tiered-intel
description: "Tiered cyber intelligence system — automated scanning, tier classification, and auto-implementation of security findings. Mirrors the PIM enhancement detection pattern."
version: 1.2.0
author: Hermes Agent (Pulse)
platforms: [windows]
metadata:
  hermes:
    tags: [cyber, intel, tiered, auto-action, scanner, phantom, dark-web, threat-intel]
    triggers: [cyber-tiered, cyber-intel-scanner, cyber-auto-actions, phantom-tiered]
    related_skills: [cyber-intel-workflow, pim-ingestion-pipeline, osint-threat]
---

# Cyber Tiered Intelligence System

## Architecture

```
Cron Chain (Nightly):
  22:00 ── Cyber Night Research (Phantom — LLM-driven)
            ├── Scans CISA KEV, PoC-in-GitHub, BleepingComputer, THN, Packet Storm
            ├── Classifies: TIER 1 (critical) / TIER 2 (high) / TIER 3 (info)
            └── Delivers formatted report to #cyber

  05:00 ── deep-spider-sweep (no_agent script)
            ├── Dark web sweep via Tor (Ahmia + OnionLand)
            ├── Breach/cred/financial keyword searches
            └── Saves JSON results to ~/deep-spider/results/

  06:30 ── cyber-intel-scanner (no_agent script)
            ├── Reads deep-spider results + gateway logs
            ├── Scores findings using keyword + LLM analysis
            └── Writes to trumpian-accounting-kb/monitoring/findings/
                cyber_intel_findings.json (Tier 1/2/3)

  07:00 ── auto_action_handler.py (every 6h — no_agent)
            ├── Reads cyber + PIM + AI ecosystem findings
            ├── Tier 1 → auto-implement (clone POC, hardening notes, log intel)
            ├── Tier 2 → research note
            └── Tier 3 → ignore

  07:01 ── Cyber Morning Briefing (Phantom — LLM-driven)
            └── Consumes night research + overnight developments + scanner findings
```

## Tier Classification

| Tier | Score | Action |
|------|-------|--------|
| 1 | ≥ 0.40 | Auto-implement — clone PoC, log hardening note, track intel, block IP |
| 2 | ≥ 0.20 | Research note — logged to cyber_intel_log.md |
| 3 | < 0.20 | Ignored |

### Tier 1 Triggers (keyword-based scoring)
- CVE affecting our stack (Firefox, Linux, Python, Node, Nginx, Tor)
- Active exploits/PoC for our tech stack
- Breach data that may include our credentials
- Authentication/bypass affecting our platforms
- Infrastructure vulnerabilities (proxies, VPNs, browsers)
- Supply chain attacks on dependencies
- Gateway log threats (auth failures, crashes, timeouts, segfaults, panics)
- **AI-agent-specific threats** — attacks targeting AI agents: image prompt injection (Ghostcommit pattern), agent supply chain poisoning, session/cookie theft from agent processes, weaponized model outputs, or any technique that compromises AI agent decision surfaces

## Files

### Scripts (canonical: `_project/scripts/`)
| File | Purpose |
|------|---------|
| `cyber_intel_scanner.py` | Scans dark web results + logs, scores findings |
| `cyber_auto_actions.py` | Executes Tier 1 cyber actions |
| `auto_action_handler.py` | Central auto-action handler (reads all sources) |

### Runtime (~/AppData/Local/hermes/scripts/)
- Same files mirrored from `_project/scripts/`

### Data Files
| File | Purpose |
|------|---------|
| `~/trumpian-accounting-kb/monitoring/findings/cyber_intel_findings.json` | Latest scored findings |
| `~/trumpian-accounting-kb/monitoring/findings/cyber_intel_history.jsonl` | Historical findings |
| `~/trumpian-accounting-kb/monitoring/findings/cyber_actions_log.jsonl` | Auto-action audit trail |
| `${MY_REPOS}/Documents/research/cyber_hardening_notes.md` | Hardening recommendations |
| `${MY_REPOS}/Documents/research/cyber_intel_log.md` | Tracked intelligence items |
| `~/deep-spider/banned_ips.txt` | Blocklisted IPs |

### Cron Jobs
| Job ID | Name | Schedule | Type | Status |
|--------|------|----------|------|--------|
| `030d0a516a7e` | Cyber Night Research | 22:00 daily | LLM-driven | ✅ |
| `9c3bcff4956e` | deep-spider-sweep | 05:00 daily | no_agent script | ✅ |
| `8b5378a8abe8` | cyber-intel-scanner | 06:30 daily | no_agent script | ⚠️ needs pin |
| `9843a00bd786` | Auto-Action Handler | every 6h | no_agent script | ⚠️ has bug |
| *MISSING* | cyber-auto-actions (`cyber_auto_actions.py`) | 07:00 (desired) | no_agent script | 🔴 not created |
| `5cfe9f93ed65` | cyber-morning-briefing | 07:00 daily | LLM-driven | ✅ |

**Note:** `cyber_auto_actions.py` has NO cron job entry as of Jul 2026. It exists at `~/AppData/Local/hermes/scripts/cyber_auto_actions.py` but is never scheduled. The pipeline architecture assumes it runs at 07:00 but it does not. Create a cron entry to enable cyber-specific hardening actions (PoC cloning, IP blocklisting, hardening notes). See Pitfalls below.

## Reference Files
- `references/auto-action-gaps.md` — concrete transcript of the keyword router and dedup gaps discovered during the 2026-07-11 briefing cycle, with fix code and audit trail
- `references/ai-agent-threats.md` — AI-agent-specific threats (Ghostcommit image injection, agent supply chain, session theft) for Tier 1 classification and red team feeding
- `references/pipeline-health-overview.md` — systemic pipeline health issues: config drift on unpinned cron jobs, auto_action_handler.py UnboundLocalError bug, missing cyber_auto_actions.py cron entry, and the full file-timestamp verification methodology

## Manual Usage
```bash
# Force-run scanner
cd ~/AppData/Local/hermes/scripts
python cyber_intel_scanner.py

# Force-run auto-actions
python cyber_auto_actions.py

# Check current findings
cat ~/trumpian-accounting-kb/monitoring/findings/cyber_intel_findings.json

# View hardening backlog
cat "${MY_REPOS}/Documents/research/cyber_hardening_notes.md"
```

## Pitfalls

### resolve_actions() Keyword Router Gaps (cyber_auto_actions.py)

- **Missing infrastructure crash/panic keywords.** The `resolve_actions()` function checks for `breach|leak|dump|patch|cve|vulnerability|exploit|ransomware` but does NOT check for `crash|segfault|panic|watchdog|timeout`. Tier 1 findings like "Gateway crash detected in watchdog.log (63 occurrences)" get logged to the intel log but never trigger a hardening note. **Fix:** Add a new detection block for infra signals matching these keywords and route them to `action_create_hardening_note()` + `action_apply_patch()`.

- **Duplicate finding dedup gap.** The fingerprint-based `actioned_fps` state works per `action_type:fingerprint`, but `cyber_intel_findings.json` can contain the same fingerprint multiple times (same content, different scan timestamps). Each entry is processed independently, creating duplicate hardening notes and intel log entries. **Fix:** Before the routing loop, deduplicate findings by `fingerprint` keeping only the latest entry per unique fingerprint.

### Briefing Verification (Morning Check)

When producing the morning briefing, always:
1. **Read `cyber_actions_log.jsonl` directly** to verify what was actually auto-implemented. Do not fabricate or assume actions — read the log.
2. **Check for type gaps** — did Tier 1 infrastructure warnings (watchdog crashes, connection timeouts) get a `hardening_note`, or only `intel_logged`? If only logged, flag the gap.
3. **Check for duplicates** — does the same finding fingerprint appear multiple times in `cyber_intel_findings.json`? If so, note the duplication in the briefing and suppress redundant action entries.
4. **Cross-reference against `auto_action_state.json`** to see what `actioned_fps` contains. The central `auto_action_handler.py` and `cyber_auto_actions.py` track state separately.

### Auto-Action Handler Execution Verification (Pipeline Health)

**Critical: verify the auto-action handler actually ran.** The handler is a no_agent script, so it can silently fail (script error, cron miss, dependency issue) without producing an error message in the briefing output.

**Verification methodology — correlate three file timestamps:**

```python
# 1. When did the scanner last produce findings?
#    File: cyber_intel_findings.json
#    If this file is fresh (today's 06:30 run), the scanner worked.
#
# 2. When did the auto-action handler last update its state?
#    File: cyber_auto_action_state.json (cyber-specific)
#    File: auto_action_state.json (central — cyber + PIM + AI ecosystem)
#    If these state files were last modified BEFORE today's findings
#    were created, the handler did NOT process today's findings yet.
#
# 3. When was the actions log last appended?
#    File: cyber_actions_log.jsonl
#    If this file's mtime matches the state file and is older than
#    the findings file, the handler missed this cycle.
```

**Recovery when handler missed a cycle:**
- Report the gap explicitly in the briefing (see flag below)
- Include a note that findings are queued but not yet actioned
- The handler runs every 6h — next window may catch it
- To verify the handler is alive: `python auto_action_handler.py --dry-run`

**State files to compare:**

| File | Tracks | Last updated |
|------|--------|-------------|
| `cyber_intel_findings.json` | Latest scored findings | After 06:30 scanner run |
| `cyber_auto_action_state.json` | Cyber-specific action fingerprints | After auto_action_handler run |
| `auto_action_state.json` | ALL action fingerprints (cyber + PIM + AI) | After each 6h cycle |
| `cyber_actions_log.jsonl` | Human-readable action log | After auto_action_handler run |

**The dual state file pattern matters:**
- `auto_action_state.json` is the CENTRAL handler — it processes ALL finding types (cyber breach intel + PIM enhancements + AI ecosystem papers). Its `actioned_fps` includes repo clones, paper downloads, and breed-specific cyber actions.
- `cyber_auto_action_state.json` is CYBER-SPECIFIC — only tracks cyber auto-actions. A mismatch between these two means one handler is lagging.
- If `cyber_auto_action_state.json` has stale timestamps but `auto_action_state.json` is fresh, the cyber-specific auto-actions may have been missed even though the central handler ran.

### Config Drift Protection for no_agent Script Cron Jobs

**Symptom:** A no_agent script cron job (e.g., `cyber-intel-scanner`) fails with:
```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since
this job was created (model 'X' -> 'Y'), and this job is unpinned. No inference call was made.
```

**Root Cause:** When the global inference provider or model changes (e.g., switching model snapshots or provider backends), unpinned cron jobs that were created under the old config are blocked from running. The job was created with a `model_snapshot`/`provider_snapshot` that no longer matches the current global config.

**Fix:** Pin the job explicitly to the desired provider and model:
```
cronjob action=update job_id=<ID> provider=<provider> model=<model>
```

**Affected jobs (July 13):**
- `cyber-intel-scanner` (ID: `8b5378a8abe8`) — failed at 2026-07-13T06:34 with `deepseek-v4-flash` -> `kimi-k2.7-code` drift

**Prevention:** Every no_agent script cron job with a `model_snapshot`/`provider_snapshot` should be pinned. Check for unpinned jobs when adding new ones or after a global config migration.

### auto_action_handler.py — UnboundLocalError in execute_actions() [RESOLVED]

**Status: RESOLVED** — The bug was fixed as of Jul 2026. The current `execute_actions()` correctly uses the `target` variable for all action dispatch calls, not an undefined `headline`:

```python
elif action_type == "enhance_soul":
    result = action_enhance_soul(target, finding)    # correct
elif action_type == "enhance_skill":
    result = action_enhance_skill(target, finding)   # correct
elif action_type == "enhance_config":
    result = action_enhance_config(target, finding)  # correct
```

**Historic symptom (before fix):** The handler crashed mid-cycle with `UnboundLocalError` when a finding matched the `change_type=="config"` route. The fix was replacing `headline` with `target` in the three dispatch lines.

**If the handler still produces no visible cyber actions despite running** (actions logged to `auto_actions_log.jsonl` but `auto_action_state.json` is empty), see the next section.

### auto_action_state.json Empty After Successful Handler Run

**Symptom:** The handler executes actions (visible in `auto_actions_log.jsonl`) but `auto_action_state.json` contains `{"actioned_fps": [], "noted_fps": []}` — empty arrays — despite a fresh timestamp.

**Observed (Jul 15, 2026):** The handler ran 37 actions (21 paper_skips, 2 enhance_skill, 2 enhance_soul, 2 kill_zombies, 1 remove_lock, 9 research_notes). `auto_action_state.json` was modified at ~11:08 UTC but contained empty arrays. Cause unknown — either a state-reset bug, a race condition with another process, or `dedup_actions()` returned empty before `save_state()`.

**Diagnostic checklist when state is empty but actions are logged:**
1. Check if `auto_action_state.json` was overwritten by another process (e.g., another cron job that reinitializes state)
2. Check `self_healer_state.json` for `cron_failures:auto_action_handler` entries
3. Verify the handler is the only process writing to `auto_action_state.json` — if `cyber_auto_actions.py` also targets the same file, there could be a write race
4. Run `python auto_action_handler.py` with trace logging to see if `dedup_actions()` produces an empty list

**Impact:** Empty state means the handler will reprocess the same findings on every cycle, creating duplicate log entries. Findings that should be deduped never accumulate in the state file.

### `enhance_config` Dead End for Cyber Config Findings

**Observation:** When the auto_action_handler processes cyber intel findings with `change_type: "config"` (e.g., dark web breach sweeps, gateway crash spikes), it generates `enhance_config` actions. The `action_enhance_config()` function only logs "Config changes need review — logged for manual approval" to `auto_actions_log.jsonl`. It does NOT:
- Write to `cyber_hardening_notes.md`
- Update `cyber_actions_log.jsonl` (the cyber-specific log)
- Update `cyber_auto_action_state.json` (the cyber-specific state)
- Create any actual configuration change

The `enhance_config` action type is a placeholder — it flags config changes for review but produces no persistent artifact beyond the generic JSONL log. This is the ONLY route for cyber findings with `change_type: "config"` in the central handler. If you expect hardening notes or intel log entries for these findings, they will not appear.

**Mitigation:** Either (a) activate `cyber_auto_actions.py` as a cron job to handle cyber-specific Tier 1 actions, or (b) extend `action_enhance_config()` in the central handler to write to `cyber_hardening_notes.md` and `cyber_auto_action_state.json` in addition to the generic log.

### Missing Cron Job: cyber_auto_actions.py

**Symptom:** Cyber-specific Tier 1 actions (hardening notes, IP blocklisting, PoC cloning) documented in `cyber_auto_actions.py` never execute. The `cyber_actions_log.jsonl` and `cyber_auto_action_state.json` go stale.

**Root Cause:** `cyber_auto_actions.py` has NO cron job entry in `cron/jobs.json`. The architecture table in this skill shows it at `07:00`, but no actual cron object exists for it. The central `auto_action_handler.py` does NOT invoke `cyber_auto_actions.py` — they are independent scripts with separate state tracking.

**Impact:** All cyber-specific hardening actions (the `action_create_hardening_note()`, `action_block_ip()`, `action_clone_poc()` functions) are dead code. Only `intel_logged` entries appear because they also run as part of Tier 2 routing. The `auto_action_handler.py` processes the same findings but uses a different action router that may miss cyber-specific routes.

**Fix:** Create a cron job entry:
```
Job ID: (new)
Name: cyber-auto-actions
Script: cyber_auto_actions.py
No_agent: true
Schedule: 0 7 * * * (daily at 07:00 after scanner completes)
Deliver: origin (to #cyber)
```
Pin provider/model to current global config to prevent config drift.

### General

- Log scanning can produce false positives from legitimate watchdog restart messages. The `crash` pattern in `watchdog.log` should be reviewed manually before actioning.
- Dark web results vary by Tor exit node. Some nodes may have different source availability for Ahmia/OnionLand.
- The auto-action handler logs Tier 1 actions but does NOT auto-apply firewall rules or config changes — those require manual review of hardening notes.
- Script files in `~/AppData/Local/hermes/scripts/` are ephemeral. Always keep canonical versions in `_project/scripts/`.
- Cyber intel findings feed into the SAME auto_action_handler pipeline as PIM and AI ecosystem findings. Dedup state prevents re-execution.
- After any global provider/model migration (e.g., switching model snapshots), verify that all no_agent script cron jobs are pinned. Unpinned jobs created before the migration will silently fail. Check `last_status` and `last_error` on every job after migration.
- The pipeline has THREE action handler scripts that track state independently: `auto_action_handler.py` (central, every 6h), `cyber_auto_actions.py` (cyber-specific, NO cron entry as of Jul 13), and `auto_action_handler.py` processing of cyber findings via `analyze_scored_finding()`. When debugging gaps, check which handler is expected to run and verify its cron entry exists and its state file is fresh.
