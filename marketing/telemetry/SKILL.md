---
name: telemetry
description: >-
  Internal utility for the skills library itself — opt-in, local-first,
  privacy-respecting usage telemetry and update checks. Provides version
  checking, usage logging, and usage reporting for the skills in this repo.
  Use only when asked to view skill usage stats, configure telemetry
  opt-in/out, wire a skill to log its own runs, or check for skill updates.
when_to_use: |
  Use when the user wants to instrument or inspect the skills library's own usage: viewing local skill-usage stats, configuring telemetry opt-in/opt-out, wiring a skill's preamble to log its runs, or checking whether a newer release of the skills repo is available.

  Not when: the task is product or event analytics in an application — capturing user events, feature flags, A/B tests, or API lifecycle telemetry with PostHog — use typescript-analytics. This skill instruments the skill library, not your app and not your infrastructure.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Telemetry

Internal, opt-in, local-first telemetry for the skills in this repository. It answers two questions: *which skills get used (and how reliably)?* and *is a newer version of the library available?* Every run is logged to a local file regardless of opt-in; data only leaves the machine if the user has explicitly opted in. No PII is ever collected — see [README.md](README.md) for the full field list and privacy commitment.

## Where data lives

All state lives under the telemetry data directory — by default `~/.ai-marketing-skills/`, the upstream location, which can differ per install:

| Path | Written by | Contents |
|------|-----------|----------|
| `telemetry-config.json` | `telemetry_init.py` | `opted_in` (bool), `device_id` (random UUID), `created` |
| `analytics/skill-usage.jsonl` | `telemetry_log.py` | one JSON object per skill run (append-only) |
| `version-cache.json` | `version_check.py` | last GitHub release seen + check timestamp (24h TTL) |

Each line in `skill-usage.jsonl` records only anonymous fields: skill name, duration (ms), success, version, OS, arch, Python version, UTC timestamp, and the random `device_id`. Never code, paths, repo names, or content.

## Tools

| Script | Purpose | Invocation |
|--------|---------|------------|
| `telemetry_init.py` | Configure opt-in/out (interactive on first run) | `python3 telemetry/scripts/telemetry_init.py` (or `--yes` / `--no`) |
| `telemetry_log.py` | Log one skill run (called by a skill's preamble) | see integration pattern below |
| `telemetry_report.py` | View local usage stats | `python3 telemetry/scripts/telemetry_report.py` (`--json`, `--skill <name>`) |
| `version_check.py` | Check for a newer library release | `python3 telemetry/scripts/version_check.py` |

## Logging a skill's runs

A skill opts into telemetry by calling `telemetry_log.py` once at the end of its run. The script always appends to the local JSONL log, and additionally POSTs to the analytics endpoint only if the user opted in. It fails silently and never blocks execution. All four flags are required:

```bash
python3 telemetry/scripts/telemetry_log.py \
  --skill my-skill-name \
  --duration 4500 \
  --success true \
  --version 1.0.0
```

Capture a start time before the work, compute `--duration` in milliseconds after, and pass `--success false` if the run errored. The endpoint in `telemetry_log.py` is a stub (`ANALYTICS_ENDPOINT`) — replace it with a real URL before remote send does anything.

## Reading the stats

```bash
python3 telemetry/scripts/telemetry_report.py            # human-readable summary
python3 telemetry/scripts/telemetry_report.py --json      # machine-readable
python3 telemetry/scripts/telemetry_report.py --skill seo-ops   # filter to one skill
```

Reports total runs, runs in the last 7/30 days, per-skill success rates and average durations, and the most-used skill. Reads only the local log — works the same whether or not you opted in.

## Checking for updates

```bash
python3 telemetry/scripts/version_check.py
```

Compares a local `VERSION` file against the latest GitHub release, caches the result for 24h, and stays silent unless a newer version exists. **It needs a `VERSION` file at the repo's skills root (`.claude/skills/VERSION`) containing the current version** (e.g. `1.0.0`). If that file is absent the script has no baseline and stays silent rather than reporting a false update — create the file to enable update notices.

## Privacy

- **Opt-in only** — nothing is sent without explicit consent.
- **Local-first** — usage is always stored locally for your own inspection.
- **No PII** — no names, emails, paths, repo names, or content.
- **Revocable** — delete `telemetry-config.json` from the telemetry data directory (by default `~/.ai-marketing-skills/`) and re-run `telemetry_init.py`.
