---
name: cron-watchdog
description: >-
  Monitor all Hermes cron jobs, detect missed runs (reboot, scheduler
  skip), and auto-re-fire them. Stays silent when healthy, reports when
  it catches something. Companion watchdog for the Hermes scheduler.
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, scheduler, watchdog, monitoring, recovery, hermessystem]
    triggers:
      - watch cron jobs
      - missed cron
      - cron not firing
      - schedule watchdog
      - auto re-fire
      - monitor cron health
      - cron watchdog
      - cron monitor
      - restart recovery
      - catch up missed jobs
      - guardian angel
      - process health
      - failed cron job messages
      - discord cron spam
      - purge discord cron messages
    related_skills:
      - hermes-nightly-watchdog
      - infrastructure-self-healing-pulse
      - webhook-subscriptions
      - guardian-angel
---

# Cron Watchdog

A proactive watchdog that ensures every enabled Hermes cron job runs when it should, even after restarts, scheduler hiccups, or brief downtime. Runs as a high-frequency cron job itself that inspects all other jobs and re-fires any that missed their window.

## Core Pattern

Create a single cron job (interval: 15-30 min) that:

1. Lists all cron jobs via `cronjob(action='list')`
2. Parses each job's schedule to compute the expected run interval
3. If the time since `last_run_at` exceeds ~1.5x the expected interval, the job was missed
4. Re-fires the missed job with `cronjob(action='run', job_id='...')`
5. Reports only when action is taken (silent when healthy)

## Detection Heuristics

Parse the `schedule` field from `cronjob(action='list')`:

| Schedule Pattern | Expected Interval | Mis Fire Threshold |
|---|---|---|
| `every Xm` | X minutes | 1.5 × X minutes |
| `every Xh` | X hours | 1.5 × X hours |
| `0 H * * *` (daily at H:00) | 24 hours | 26 hours |
| `0 H1,H2 * * *` (twice daily) | ~12 hours (gap between H1-H2) | 16 hours |
| `0 H * * D` (weekly on day D) | 7 days | 8 days |
| ISO timestamp (one-shot) | N/A — skip, never re-fire | N/A |

For **daily-at-time** cron expressions (`0 6 * * *`), compute whether the job should have fired today. If `last_run_at` is from yesterday (or earlier) and the current time is past the scheduled hour, it was missed.

### Timezone Awareness

All Hermes cron timestamps are in the configured timezone (ET for the operator's setup). Use the current time consistently when computing gaps. Account for DST changes — cron uses local wall-clock time, so a daily-at-6AM job always means 6AM local regardless of DST.

## What to Skip (Never Re-Fire)

| Job Type | Reason |
|---|---|
| Your own watchdog job | Infinite loop |
| State != `scheduled` | Paused, completed, cancelled intentionally |
| No `last_run_at` | New/never ran; not a miss |
| `no_agent=true` script jobs | Scripts run on their own schedule via the scheduler's timer; the watchdog lacks the script context and re-running could cause duplicates |
| Jobs with `state=completed` | One-shot jobs that already finished |
| Jobs with `state=paused` | User intentionally stopped them |

### NEVER_PAUSE Blacklist (for Cron Guardian)

When a model-outage watchdog auto-pauses jobs, it must NEVER pause infrastructure
jobs or the system deadlocks:

```python
NEVER_PAUSE = [
    "Cron Guardian", "Guardian Angel", "Cron Watchdog",
    "Hermes Self-Healer", "model-health-watchdog", "welcome-back-briefing",
    "tor-circuit-rotation", "Hermes System Backup", "PIM Ingestion",
    "PIM Ingestion & Sync", "refresh-firefox-cookies",
]
```

This blacklist is shared between the Cron Watchdog and the Cron Guardian. If you're
building a cron-based auto-pause system, always include this check.

## Re-Fire Process

```python
# Pseudocode for the detection + re-fire loop
for job in all_jobs:
    if not should_skip(job) and is_missed(job):
        cronjob(action='run', job_id=job.job_id)
        log(f"Re-fired {job.name} — missed because {reason}")
```

When re-firing:
- Use `cronjob(action='run', job_id='...')` to trigger an immediate run
- The job runs in a fresh agent session exactly like a scheduled tick
- If the job has attached skills, they're loaded automatically
- If the job has a `workdir`, it runs from that directory

## Reporting

- **STAY SILENT** when everything is on track (no missed jobs detected)
- **REPORT** when you re-fire one or more jobs:

> **Cron Watchdog — Missed Jobs Detected**
>
| Job | Missed Since | Reason | Action |
|---|---|---|---|
| website-landlord-daily-build | Jun 22 → Jun 23 (6AM) | Computer restart — missed 6AM window | ✅ Re-fired |
| morning-brief | Jun 23 (6AM) | Computer restart | ✅ Re-fired |
>
> *Next check in 15 min.*

## Initial Setup

```yaml
# Create the watchdog cron job
# Run: cronjob(action='create', schedule='every 15m', ...)
# Or use the Hermes CLI:
#   hermes cron create --name "Cron Watchdog" --schedule "every 15m" --prompt "..."

name: Cron Watchdog — detect & re-fire missed jobs
schedule: every 15m
prompt: |-
  [Self-contained watchdog prompt with detection logic]
enabled_toolsets: ["cronjob"]
deliver: origin  # Deliver back to the chat where it was set up
```

## Pitfalls

- **Watchdog itself is skipped** — the watchdog must skip re-firing itself by name or by detecting it's the current running job.
- **No-agent script jobs are skipped** — these run via script execution, not the LLM loop. The scheduler handles them on its own timer. Re-running them without the full context could cause duplicates or race conditions.
- **Computer restart gap** — when the computer is off during a scheduled window, the Hermes scheduler does not auto-catch-up missed jobs. The watchdog handles this.
- **next_run_at can be misleading** — after a miss, the scheduler reschedules `next_run_at` to the *next* future slot, not "right now." Don't rely on `next_run_at` being in the past as the sole detector.
- **Stale hardcoded date in prompt** — If the watchdog prompt has a literal date string like "Current time: approximately June 23, 2026", it will blind the watchdog to all future misses. The prompt MUST reference the current time dynamically. If the watchdog stops detecting misses, check for hardcoded dates in the prompt and the watchdog's reference prompt file. Fix by replacing the literal date with a statement like "Use the current system time — do NOT use a hardcoded date."
- **"No model configured" cascade** — When all cron jobs fail simultaneously with "no model configured", the root cause is usually one of: (a) `config.yaml` has `model.default: ''` (empty string), (b) `HERMES_MODEL` env var is empty, (c) the default model provider config is broken. Jobs that DO have explicit per-job models (`model=deepseek-v4-flash` in the job record) will still fail if the prompt references a stale date or the job record's model was set after the failed run (the error output reflects state-at-run-time, not current state). Fix: set `model.default` in config.yaml, or add explicit per-job models via `cronjob action=update job_id=<id> model=<name> provider=<provider>`.
- **Don't over-fire** — if a job missed 2 cycles (e.g., 48h gap for a daily job), only re-fire once. A single re-fire handles the catch-up; the next scheduled tick covers the rest.
- **Output noise** — if the watchdog fires every 15 minutes and repeatedly detects the same missed job (because re-running it is still failing), it'll spam. Add a cooldown: skip jobs that were re-fired in the last N hours.
- **Schedule string parsing** — cron expressions can be complex. Use simple regex heuristics for known patterns rather than a full cron parser. The `every Xm/h` format is trivial; `0 H * * *` is the common cron format.

### Corruption: guardian_state.json contains invalid data

The Cron Guardian state file `~/AppData/Local/hermes/cron/guardian_state.json` can
become corrupted — containing just `0` instead of valid JSON. This happens after
force-kills or crashes during file writes.

**Symptoms:** Cron Guardian reports `Error loading guardian state` in its log.
State transitions (pause/resume) are lost. The guardian starts fresh with
`state: WAITING`, potentially re-pausing jobs unnecessarily.

**Detection:** `cat ~/AppData/Local/hermes/cron/guardian_state.json` shows
just `0` instead of `{"state": "WAITING", ...}`.

**Fix:** Reinitialize the state file:
```python
import json
from pathlib import Path
state = Path.home() / "AppData/Local/hermes/cron/guardian_state.json"
state.write_text(json.dumps({
    "state": "WAITING",
    "last_healthy": "2026-01-01T00:00:00",
    "consecutive_failures": 0,
    "last_transition": "repaired"
}))
```

### Corruption: UTF-8 BOM in jobs.json

The cron database file `~/AppData/Local/hermes/cron/jobs.json` can get a UTF-8 BOM (`\\xef\\xbb\\xbf`) prepended, causing all cron jobs to stop firing.

**Symptoms:** `cronjob(action='list')` errors with `Cron database corrupted and unrepairable: Unexpected UTF-8 BOM`. Gateway log shows repeated `ERROR cron.jobs: Failed to auto-repair jobs.json: Unexpected UTF-8 BOM` and `Cron tick error`.

**Detection:** `file ~/AppData/Local/hermes/cron/jobs.json` reports `Unicode text, UTF-8 (with BOM) text` instead of `JSON text`. Or `xxd` shows `efbb bf` at offset 0.

**Fix:** Strip the BOM bytes from the file:
```bash
python -c "
path=r'C:\\Users\\<you>\\AppData\\Local\\hermes\\cron\\jobs.json'
with open(path,'rb') as f: d=f.read()
if d[:3]==b'\\xef\\xbb\\xbf':
    with open(path,'wb') as f: f.write(d[3:])
    import json
    with open(path) as f: json.load(f)
    print('BOM stripped, file valid')
"
```

### Duplicate Dist-Info Corruption

If SQLAlchemy-dependent cron jobs suddenly fail with:
```
ImportError: cannot import name 'getcurrent' from 'greenlet' (unknown location)
```
See `references/python-duplicate-distinfo.md` for diagnosis and fix.
This is a common issue after pip upgrades that install duplicate
package metadata without cleaning up old versions.

## Finding a Cron Job's Output Directory (Self-Discovery)

When a cron agent needs to read its own output or a sibling's (e.g., for dedup or error verification) but doesn't know the job ID, search all output directories for your task title. Each output file's first line is `# Cron Job: <Title>`:

```bash
# Search the latest file in each output dir for a unique title keyword
for dir in ~/AppData/Local/hermes/cron/output/*/; do
  f=$(ls -t "$dir" 2>/dev/null | head -1)
  [ -n "$f" ] && head -1 "$dir/$f" 2>/dev/null | grep -q "C2C\|YourTask" && echo "${dir##*/}"
done
```

Replace the grep pattern with a distinctive word from your own cron task title. Once found, the directory name (e.g., `582ca95572a2`) is the job ID for all subsequent `read_file` or `tail` calls against that job's output tree. Cache it in a cron environment variable to skip discovery on future runs.

## Handling Stale `state: error` Jobs

Cron jobs can get stuck in `state: error` even after the underlying issue is resolved. This prevents them from running on schedule. The error state persists in the job record and must be explicitly cleared.

**Detection:** Look for jobs where `state: error` appears in the `cronjob(action='list')` output. These jobs may have `last_status: error` or `last_status: ok` with `state: error` (a stale flag).

**Recovery (pause/resume):**
```python
# Pause clears the error flag, resume re-enables
cronjob(action='pause', job_id='<job-id>')   # state → paused
cronjob(action='resume', job_id='<job-id>')  # state → scheduled
```

This is the only way to clear `state: error` on a job that no longer has the root cause present. The pause/resume cycle resets the scheduler's state machine for that job.

**Pitfall — "OK but error":** A job can have `last_status: ok` (last run succeeded) but `state: error` (a stale flag). This happens when the error occurred on a *different* run than the most recent one. Don't confuse `state` (scheduler state machine) with `last_status` (most recent run outcome). Pause/resume fixes both.

**Pitfall — Don't re-fire errored jobs blindly:** Before clearing the error state, verify the job's output to understand why it errored. Read its most recent output file from `~/AppData/Local/hermes/cron/output/<job_id>/`. If the error was transient (network blip, timeout), pause/resume is safe. If the error is structural (missing script, bad config), fix that first, then pause/resume.

**Pitfall — Run vs resume semantics:** `cronjob(action='run')` triggers an immediate run but does NOT clear `state: error`. The job remains in error state even after a successful `run`. Always use pause/resume to clear the state flag.

## Discord Failure Spam: Prevention + Retroactive Purge

Failing cron jobs with `deliver: discord:*` (or `origin` on a Discord-bound session) post an error message to the channel on EVERY tick — a broken every-4h job spams 6 messages/day per job indefinitely. the operator's standing rule: **zero failed-cron messages in Discord, ever** — jobs must work and only report back when there's something actionable.

### Triage (do this first)

1. `cronjob(action='list')` — find jobs where `last_status: error` or `last_delivery_error` is non-null.
2. Remove junk/test jobs outright (`cronjob action=remove`): one-letter names, `echo hi`/`say hello` prompts, smoke-test leftovers.
3. For real jobs you want to keep, stop the spam immediately by switching delivery to local: `cronjob(action='update', job_id='<id>', deliver='local')`. The job keeps running and reporting locally; Discord stays clean.
4. Fix the root cause (missing script, bad model config, dead API key, adapter down) before ever restoring Discord delivery.

Common `last_delivery_error` values and what they mean:

| Error | Meaning | Fix |
|---|---|---|
| `platform 'discord' not configured/enabled` | Job targets a Discord channel but the gateway's Discord adapter is down/not enabled | Switch to `local` until the adapter is fixed |
| `Discord API error (429)` | Rate limited — too many jobs posting to the same channel | Consolidate jobs or local-deliver |
| `'charmap' codec can't encode character '\u2705'` | Report contains emoji the delivery path can't encode | Strip emoji from the report template or local-deliver |

### Proactive Delivery Management (Prevent Spam Before It Starts)

The most effective way to keep Discord clean is to set the right delivery target BEFORE jobs start spamming. Classify every cron job on creation or during audits:

| Job Category | Deliver Setting | Examples |
|---|---|---|
| Revenue/actionable output | `origin` | C2C Hunter, Land Sales, AI Sharp picks, options |
| Pulse/heartbeat/monitor | `local` | the operator's Pulse, Morning Brief, Flash Intel, Weekly Strategy |
| Error-prone jobs | `local` | Any job with `last_status: error` |
| no_agent script jobs | Auto-silent | Empty stdout = no delivery; output only when there's data |

### Running an Audit

1. List all jobs: `cronjob(action='list')`
2. Group them by type (revenue vs heartbeat vs monitor)
3. For each LLM-driven job with `deliver: origin`:
   - Is this revenue or actionable? → keep `origin`
   - Is this a routine status check / pulse / heartbeat? → switch to `local`
   - Has it ever errored? → switch to `local`
4. Set delivery: `cronjob(action='update', job_id='<id>', deliver='local')`

### no_agent Script Rule

`no_agent=True` script jobs ALREADY self-suppress — empty stdout = absolutely no delivery. Only non-empty output triggers delivery. This is the most efficient pattern for watchdog and data-collection jobs. When creating a new cron job that checks for something periodically, prefer `no_agent=True` with a script that outputs nothing when there's nothing to report.

### Audit Results Reference

In the operator's setup (Jul 2026), the audit classified 88 jobs into:
- **59 local** — pulses, heartbeats, monitors, errored jobs, background services
- **11 origin** — revenue jobs (C2C Hunter, Land Sales, AI Sharp picks, options, strategy bots)
- **14 channel-specific** — pulses that go to specific Discord channels (dev-lead-pulse, skills-lead-pulse, etc.)
- **4 errored → local** — stopped immediately

Prevention doesn't remove the backlog of error messages already sitting in channels. Use `scripts/cleanup_discord_cron_messages.py` (packaged with this skill): a discord.py bot script that scans every text channel's history (last 30 days), matches bot-authored messages against failure patterns (cron keywords + error keywords, ❌/🔴/⚠️ markers, HTTP error codes, `Cronjob Response:` headers), and deletes them.

```bash
python "${USER_HOME}/AppData/Local/hermes/skills/devops/cron-watchdog/scripts/cleanup_discord_cron_messages.py"
```

- Requires `DISCORD_BOT_TOKEN` in `~/.hermes/.env` or `~/AppData/Local/hermes/.env`, with `message_content` + `guilds` intents.
- Expect heavy 429 rate limiting — discord.py auto-retries; a full-server purge of hundreds of messages takes 5+ minutes. Run with a long timeout or in the background. **It's resumable** — already-deleted messages stay deleted, so re-running continues where it left off.
- Only deletes bot-authored messages; user messages are never touched.

## Verification

After creating the watchdog:

1. Wait for its first run (should be within 15 min)
2. Check that it lists all enabled jobs
3. Confirm it correctly identifies recently missed jobs (like the daily website build)
4. Verify re-firing actually triggers the job (check the job's last_run_at updates)
5. Confirm the watchdog stays silent when no jobs are missed

To test manually:

```python
# Simulate: run the watchdog immediately
cronjob(action='run', job_id='<watchdog-job-id>')
```

## References

- `references/production-watchdog-prompt.md` — the exact prompt used in the operator's production cron watchdog, with full detection heuristics and edge cases.
- `references/model-aware-cron-guardian.md` — model availability watchdog that auto-pauses/resumes cron jobs during API outages. Complementary to this skill: Guardian prevents error spam (pauses before jobs fail), Watchdog catches missed runs (re-fires after recovery).
- **Guardian Angel** (`guardian-angel` skill) — companion process-health watchdog that monitors the Hermes Agent and Gateway processes. While cron-watchdog handles schedule-level monitoring (missed jobs), Guardian Angel handles process-level monitoring (crash, hang, error burst). The two are complementary: cron-watchdog re-fires jobs, Guardian Angel restarts the gateway.
- **Model Provider Routing** (`model-provider-routing` skill) — centralized model configuration that supplies API endpoints and keys to cron-guardian.py and all other scripts. All model provider settings (base URL, API key env var, model name) now flow through this one config.
