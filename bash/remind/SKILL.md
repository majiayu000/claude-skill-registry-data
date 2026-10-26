---
name: remind
description: Set a reminder for when an account's session or weekly limit resets, when its usage drops under a percentage, or at a time; list or cancel them.
argument-hint: "when <account>'s session|weekly limit resets | when <account> is under <N>% | in <2h> <text> | at <3pm> <text> | list | cancel <id>"
disable-model-invocation: true
allowed-tools:
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/remind.py" add:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/remind.py" list:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/remind.py" cancel:*)
---

Turn `$ARGUMENTS` into exactly one command below, run it with the Bash tool, and show its output as is. `R` stands for `"${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/remind.py"`.

| Request | Command |
|---|---|
| `list` | `R list` |
| `cancel 3` | `R cancel 3` |
| when the session / 5-hour limit resets | `R add reset [--account NAME] -- ['TEXT']` |
| when the weekly limit resets | `R add weekly [--account NAME] -- ['TEXT']` |
| when an account is under N% | `R add under [--account NAME] -- N ['TEXT']` |
| in a duration (`2h`, `90m`, `1h30m`, `1d`) | `R add in -- DURATION 'TEXT'` |
| at a time (`15:00`, `3pm`, `3:30pm`, `tomorrow 9am`, `2026-10-18 09:00`) | `R add at -- 'WHEN' 'TEXT'` |

- `--account` only when the user names one (`alex's` → `--account alex`); without it the script uses the account this session runs on. A plain "usage limit" means the session limit.
- `TEXT` is what to remind about, without the time words, in single quotes (`'` → `'\''`); always keep the `--`. Account reminders may leave it out.
- Other days than today or tomorrow: give `WHEN` as `YYYY-MM-DD HH:MM`. Weekday names or vague times ("later", "tonight") → ask for a time instead of guessing.
- Nothing fits (or no request): show the table's left column as the usage and run nothing.
- A `remind: ...` error (unknown account, no usage cached yet, window already reset, already under) is the answer: show it and stop. Never pick a time for an account reminder yourself.
- `python3` not found (Windows): run the same command with `python`.
