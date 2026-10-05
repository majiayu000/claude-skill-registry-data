---
name: opencode
description: >
  Delegate a coding task to OpenCode CLI and supervise the result via git diff.
  Trigger: /opencode <instruction>. Claude orchestrates, OpenCode codes.
  Also handles /opencodeon, /opencodeoff, /opencodestatus, /opencode-report,
  /opencode-model-pick, /opencode-model-clear.
license: MIT
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Grep
---

## /opencodeon | /opencodeoff | /opencodestatus

Toggle auto-delegate mode — OpenCode automatically handles coding tasks without
requiring `/opencode` each time.

| Command | Action |
|---------|--------|
| `/opencodeon` | `touch ~/.local/share/opencode-auto.flag` → confirm "Auto-opencode ON" |
| `/opencodeoff` | `rm -f ~/.local/share/opencode-auto.flag` → confirm "Auto-opencode OFF" |
| `/opencodestatus` | run `test -f ~/.local/share/opencode-auto.flag && echo ON \|\| echo OFF` |

Run the bash command, print one confirmation line, and stop.

---

## /opencode-report

If the user invokes /opencode-report, run ~/tools/delegate-report with any flags extracted from the arguments, display output verbatim, and stop.

| User says | Flag |
|-----------|------|
| last 7 days, 7d | --since 7 |
| last 30 days, 30d | --since 30 |
| project foo | --project foo |
| only failures, fails | --fails |
| (nothing) | (no flags, full report) |

---

## /opencode-model-pick | /opencode-model-clear

Override the model for all subsequent delegations without editing the script.

| Command | Action |
|---------|--------|
| /opencode-model-pick model | echo model > ~/.local/share/opencode-model.flag, confirm |
| /opencode-model-clear | rm -f ~/.local/share/opencode-model.flag, confirm back to default |

Run the bash command, print one confirmation line, and stop.

---

# OpenCode Orchestrator

When the user invokes `/opencode <instruction>`, Claude delegates the implementation
to OpenCode CLI via its headless `run` mode (`opencode run <prompt> --format json`),
monitors in real time, and reports.

---

## Known Limits

Hard constraints — not config options.

### 1. No `--max-turns` flag
**Timeout is the only runaway-control lever.** Set timeouts conservatively and decompose tasks.

### 2. `--dangerously-skip-permissions`
Passed automatically by the delegate script — all tool calls auto-approved. Review the git diff afterwards.

### 3. `--dir` flag
Passed automatically by the delegate script. Sets the working directory for OpenCode.

### 4. No pseudo-TTY needed
Plain pipe — no `script -q -c` wrapper required.

### 5. Free model queue delays
`opencode/deepseek-v4-flash-free` — no API key cost; may queue during peak usage.

### 6. Orchestration chain — 5 failure points

| Link | Failure mode | Symptom |
|------|-------------|---------|
| OpenCode CLI | Auth expired, quota hit, network | Immediate exit or silent hang |
| Stream parser | OpenCode changes JSON event schema | Tool calls not detected |
| Token aggregation | step_finish missing or malformed | Tokens logged as 0 |
| git diff | Not a git repo, or OpenCode committed mid-run | Wrong file count |
| JSON log | `~/.local/share/` not writable | Silent log skip |

When a run produces unexpected results, check these links top to bottom.

---

## Step 1 — Detect workdir

1. `git rev-parse --show-toplevel` in the current directory.
2. If ambiguous or no git repo → ask with `AskUserQuestion`.

---

## Step 2 — Decompose the task

**Critical rule**: keep tasks **atomic and focused** — one objective, one prompt.

| Signal | Action |
|--------|--------|
| 1 file, ≤ ~10 lines to change, location already known | **Do it directly** — don't delegate |
| 1 file, logic non-trivial OR location unclear | Delegate |
| 2–3 files, single objective | Delegate |
| >3 files OR multi-step logic OR migrations | Delegate, broken into sub-tasks |

| Size | Definition | Timeout | Approach |
|------|-----------|---------|----------|
| **Trivial** | 1 file, change is obvious and located | — | **Skip delegation — edit directly** |
| **Simple** | 1 file, non-trivial logic or unknown location | 180s | 1 opencode call |
| **Medium** | 2–3 related files, 1 goal | 300s | 1 opencode call with structured prompt |
| **Complex** | >3 files OR multi-step logic | — | **Decompose** |

**Decomposition for complex tasks:**
```
Sub-task 1: Explore relevant files (180s)
Sub-task 2: Implement change A in file X (300s)
Sub-task 3: Implement change B in file Y (300s)
Sub-task 4: Verify / test (180s)
```
→ Check git diff between sub-tasks before launching the next.

---

## Step 3 — Write the OpenCode prompt

The prompt must be **self-contained**.

**Structure:**
```
Stack: Python/Flask, SQLAlchemy, SQLite
Key files: app.py (routes + fetch), models.py (Entry)

TASK: [one single thing to do, stated as an imperative]

CONSTRAINTS:
- [what must not break]
- [expected format if relevant]

VERIFY: grep for "def function_name" in file.py and confirm it exists.
```

**Formulation rules:**
- One task per prompt — never "also do X and Y"
- Name the exact files to modify
- Include a grep-based verification criterion (not a file re-read)
- Language: English (best model performance)

**Prompt adaptations:**
- **Any task that defines or calls a specific function**: include the exact signature — `def validate(data: dict) -> tuple[bool, list[str]]:`.
- **No fixed signature, but conventions matter**: point at the file to read first ("read app.py, follow its route/jsonify style") instead — don't do both, they're substitutes.

**Verification — always use grep, not file re-read:**
```
VERIFY: grep for "def extract_labels" in app.py and confirm it exists.
```

**Examples:**

❌ Bad (too vague, too wide):
```
Fix the API, add a signal classifier, update the UI with colored badges
```

✅ Good (atomic, verifiable):
```
Stack: Python/Flask. Files: app.py, templates/index.html

TASK: In fetch_data(), convert the date string (format "YYYY-MM-DD")
to datetime.date before returning.

CONSTRAINTS:
- Keep the existing route structure
- Use the same import style as the rest of the file

VERIFY: grep for "datetime.date" in app.py and confirm it exists.
```

---

## Step 4 — Launch OpenCode

```bash
~/tools/opencode-delegate "<workdir>" "<prompt>" [timeout-secs] [model]
```

| Argument       | Default | Notes |
|----------------|---------|-------|
| `workdir`      | —       | Absolute path, must exist |
| `prompt`       | —       | Self-contained task description |
| `timeout-secs` | `300`   | Wall-clock kill timer |
| `model`        | `opencode/deepseek-v4-flash-free` | OpenCode model string |

**Recommended timeouts:**
- Explore only: `120`
- Simple change (1 file): `180`
- Medium change (2–3 files): `300`

**Model selection:**
- `opencode/deepseek-v4-flash-free` (default) — free, no API key needed, may have queue delays
- `google/gemini-2.5-flash` — cheap, fast (requires `GOOGLE_GENERATIVE_AI_API_KEY`)

**Examples:**
```bash
# Simple change
~/tools/opencode-delegate "/path/to/project" "Stack: Flask. File: app.py. TASK: ..." 180

# Background run
~/tools/opencode-delegate "/path/to/project" "..." 300 > /tmp/opencode_out.txt 2>&1 &
# Monitor with: tail -f /tmp/opencode_out.txt
```

---

## Step 5 — Supervise in real time

The script prints live:
```
=== OPENCODE START ===
Workdir : /path/to/project
Model   : opencode/deepseek-v4-flash-free
Timeout : 300s
Prompt  : Stack: Python/Flask. File: app.py ...
======================
  [read]   app.py
  [edit]   app.py  (+2/-1)
  [opencode] Done. Converted date to datetime.date in fetch_data().
Tool calls: 3
OpenCode tokens: 4,800  (4,600 in + 200 out)  |  ~$0.000000
=== OPENCODE DONE (exit: 0) ===
=== SYNTAX OK (1 file(s) checked) ===

=== UNCOMMITTED CHANGES ===
 app.py | 4 ++--
[log] → ~/.local/share/delegate-runs.jsonl  (4800 tokens, exit 0, 42.1s)
```

**Event types emitted by the parser:**

| Event | Meaning |
|-------|---------|
| `[read]` | File read |
| `[edit]` | File edited (+additions/-deletions) |
| `[write]` | File created |
| `[search]` | Grep / search tool called |
| `[shell]` | Shell command executed |
| `[opencode]` | Assistant text response |
| `[WARN]` | Tool error detected |
| `[ERROR]` | OpenCode runtime error |

**OpenCode never commits.** All changes are left unstaged — `git checkout .` reverts everything if needed.

**Red flags to act on immediately:**

| Flag | Meaning | Action |
|------|---------|--------|
| `[WARN]` | Tool error | Read the error, fix manually |
| `[ERROR]` | Runtime error | Check auth, model availability |
| `exit: 1` or non-zero | OpenCode failed | Read diff, correct prompt |
| No `[edit]` after 60s | Looping or queue delay | Abort if persists |
| exit 0 + no `[edit]` events | `WROTE_NOTHING` — OpenCode ran but wrote nothing | Do not compensate — fix prompt and relaunch |
| `=== SYNTAX ERRORS ===` | Post-run syntax check failed | **Fix before committing** |
| `=== OPENCODE TIMEOUT ===` | Timed out | Check what was done before retrying |
| Same file read 5+ times | OpenCode is circling — run likely lost | Abort, check diff, try again |

**Common issues and workarounds:**

| Issue | Cause | Fix |
|-------|-------|-----|
| No tool calls, empty response | Model overloaded or queue delay | Retry; increase timeout to 300 |
| Timeout with no writes | Model not responding | Try a different model |
| File not modified despite "done" | OpenCode described but didn't edit | Add "make the edit now, do not describe it" |
| `[ERROR] API key missing` | Provider not configured | Check `opencode auth list` |
| Exit 124 (timeout) | Task too large for given timeout | Decompose or increase timeout |

---

## Step 6 — Iteration

- **Max 3 attempts** per sub-task before escalating to the user.
- Between attempts, **read the git diff** to avoid doubling partial work.
- If OpenCode completed ≥50% and timed out: finish the rest manually rather than relaunching.

## Step 6b — Log manual completion

When you finish a task manually (after OpenCode failures), run this:

```bash
python3 -c "
import json, datetime, subprocess, os
workdir = subprocess.run(['git','rev-parse','--show-toplevel'], capture_output=True, text=True).stdout.strip() or os.getcwd()
project = os.path.basename(workdir.rstrip('/'))
stat = subprocess.run(['git','-C',workdir,'diff','--stat'], capture_output=True, text=True).stdout
lines_added = sum(int(l.split('+')[1].split()[0]) for l in stat.splitlines() if '|' in l and '+' in l) if stat else 0
files_changed = len([l for l in stat.splitlines() if '|' in l])
tokens_out = lines_added * 10
tokens_in  = lines_added * 40
cost = (tokens_in * 3.0 + tokens_out * 15.0) / 1_000_000
entry = {'ts': datetime.datetime.utcnow().isoformat() + 'Z', 'delegate': 'claude-manual', 'workdir': workdir, 'project': project, 'exit_code': 0, 'files_changed': files_changed, 'tokens_in': tokens_in, 'tokens_out': tokens_out, 'tokens_total': tokens_in + tokens_out, 'cost_usd': round(cost, 6), 'cost_estimated': True, 'lines_added': lines_added}
log = os.path.expanduser('~/.local/share/delegate-runs.jsonl')
open(log, 'a').write(json.dumps(entry) + '\n')
print(f'[log] claude-manual -> {project}  ~{lines_added} lines  est. cost \${cost:.4f}')
"
```

Run from anywhere inside the project. Flagged `cost_estimated: true` in the log.

---

## Step 7 — Report to the user

```
✓ OpenCode finished — <1-line summary>

Files modified:
  - path/to/file.ext (+X / -Y lines)

[If problem]:
⚠ <description> — completing manually / retrying?

Ready to commit?
```

---

## Orchestration rules

- **Decompose before delegating** — one task, one prompt.
- **Check diff between sub-tasks** — never launch the next step blind.
- **Don't code in OpenCode's place** unless OpenCode did ≥50% and timed out.
- **Timeout is the only turn limit** — decompose rather than extending.
- **VERIFY with grep, not re-read** — `grep -n "def foo" file.py`.

---

## Run Log

Every run appends one JSON entry to `~/.local/share/delegate-runs.jsonl`.
The shared `~/tools/delegate-report` script can query all runs across delegates.

```bash
~/tools/delegate-report                  # full report
~/tools/delegate-report --since 7        # last 7 days
~/tools/delegate-report --project myapp  # filter by project
~/tools/delegate-report --fails          # failures only
```

**Useful queries:**
```bash
# All recent runs
cat ~/.local/share/delegate-runs.jsonl | python3 -m json.tool | less

# Total cost
jq -r '.cost_usd' ~/.local/share/delegate-runs.jsonl \
  | awk '{sum+=$1} END {printf "Total: $%.4f\n", sum}'
```

---

This skill is improved regularly — run [update-skills](https://github.com/pcx-wave/update-skills) to pull the latest version of this skill, as well as all your other skills!
