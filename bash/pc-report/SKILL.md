---
name: pc-report
description: >-
  Host monitoring report (uptime, CPU/RAM, disk, top processes) for Linux,
  macOS, and Windows. Use when the user asks for a machine report, sysstat/sar
  summary, or invokes /pc-report_*.
disable-model-invocation: true
---

### TO COPY

# pc-report

Per-workspace registration slice. No credentials.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
```

##### END TO COPY

# pc-report

## When to use

Use for host health summaries on Linux, macOS, or Windows. Trigger phrases:
"machine report", "host report", "rapport machine", "sar CPU RAM", `/pc-report_*`.

Scripts live in `~/.meta-skills/skills/productivity/pc/pc-report/`. Run the script for your OS from that directory (see [slash commands](#slash-commands)).

## Layout

Scripts are split by language: French in `FR/`, English in `en/`. Each folder has
a Linux (`.sh`), macOS (`-mac.sh`) and Windows (`.ps1`) variant.

## Slash commands

| Slash | CLI | Description |
|-------|-----|-------------|
| `/pc-report_run` | `./FR/pc-daily-report.sh` | French report (Linux) |
| `/pc-report_run-en` | `./en/pc-daily-report.sh` | English report (Linux) |
| `/pc-report_run-mac` | `./FR/pc-daily-report-mac.sh` | French report (macOS) |
| `/pc-report_run-mac-en` | `./en/pc-daily-report-mac.sh` | English report (macOS) |
| `/pc-report_run-win` | `pwsh -File ./FR/pc-daily-report.ps1` | French report (Windows) |
| `/pc-report_run-win-en` | `pwsh -File ./en/pc-daily-report.ps1` | English report (Windows) |

## How to run

1. `cd` to `~/.meta-skills/skills/productivity/pc/pc-report`.
2. Pick the script for language + OS (see slash table).
3. On Linux, ensure `sysstat` / `sar` data is available (`SADIR` defaults to `/var/log/sysstat`).
4. Run the script and return the full stdout to the user.

## Notes

- Bash / PowerShell scripts (no Python CLI).
- See `dependencies.md` for packages (Linux: `sysstat`).
- No per-workspace OAuth tokens; host metrics only.
- Docs: [`README.md`](README.md) (EN), [`README-FR.md`](README-FR.md) (FR).
