---
name: vibe
description: >
  Delegate a coding task to Mistral Vibe and supervise the result via git diff.
  Trigger: /vibe <instruction>. Claude orchestrates, Vibe codes.
  Also handles /vibe-report [--since N] [--project NAME] [--fails] — token/cost/failure report.
license: MIT
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Vibe Orchestrator

## /vibeon | /vibeoff | /vibestatus

Toggle auto-delegate mode — Vibe automatically handles coding tasks without requiring `/vibe` each time.

| Command | Action |
|---------|--------|
| `/vibeon` | `touch ~/.local/share/vibe-auto.flag` → confirm "Auto-vibe ON" |
| `/vibeoff` | `rm -f ~/.local/share/vibe-auto.flag` → confirm "Auto-vibe OFF" |
| `/vibestatus` | report auto-mode (ON/OFF) **and** active model override |

For `/vibestatus`, run both checks and print two lines:
```
Auto-vibe: ON | OFF
Model: <alias>  (override)  OR  Model: <default from ~/.vibe/config.toml>  (config default)
```

### Auto-mode pre-filter (when flag is set)

When `vibe-auto.flag` exists, apply this gate **before** loading the full skill:

| Task signal | Action |
|---|---|
| 1 file, ≤10 lines, exact location already known | Edit directly — do NOT invoke the skill |
| Logic non-trivial, location unclear, multiple files, HTML/JS content, or >1 change | Invoke `/vibe` as normal |

---

## /vibe-report

If the user invokes `/vibe-report`, run `~/tools/delegate-report` with any flags
extracted from the arguments, display output verbatim, and stop.

| User says | Flag |
|-----------|------|
| "last 7 days", "7d" | `--since 7` |
| "last 30 days", "30d" | `--since 30` |
| "project foo" | `--project foo` |
| "only failures", "fails", "bugs" | `--fails` |
| "adapt", "adaptations", "by adaptation" | `--adapt` |
| "all delegates", "everything", "compare delegates" | `--all` |
| "delegate foo", "only opencode" | `--delegate foo` |
| (nothing) | (no flags — vibe runs only) |

The report defaults to **vibe runs only**. The log is shared across delegate
tools (vibe, opencode, gemini); use `--all` for the cross-delegate comparison
or `--delegate NAME` to scope to a different one.

---

## /vibe-model-pick | /vibe-model-clear

Override the Vibe model for all subsequent delegations without touching `~/.vibe/config.toml`.

| Command | Action |
|---------|--------|
| `/vibe-model-pick <alias>` | `echo <alias> > ~/.local/share/vibe-model.flag` → confirm |
| `/vibe-model-clear` | `rm -f ~/.local/share/vibe-model.flag` → confirm "back to config default" |

**Aliases are machine-specific** — read the actual list (and the default) from
`[[model]]` entries in `~/.vibe/config.toml` before suggesting one; never assume
an alias from this table exists. Example snapshot from one machine:

| Alias | Model | Provider | Notes |
|-------|-------|----------|-------|
| `deepseek-flash` | deepseek-v4-flash | DeepSeek | Default — fast, cheap; solid for inline edits |
| `mistral-medium-3.5` | mistral-vibe-cli-latest | Mistral | Stronger reasoning; reliable for inline edits |
| `devstral-small` | devstral-small-latest | Mistral | Agent-mode — read/explore only, weak at inline edits |
| `local` | devstral (llamacpp) | Local | Requires local server on :8080 |

Run the bash command, print one confirmation line showing the active model, and stop.

---

When the user invokes `/vibe <instruction>`, Claude delegates the implementation
to Mistral Vibe via its programmatic mode, supervises in real time, and reports.

---

## Known Limits

Hard constraints — not config options. Full details in `SKILL-reference.md`.

- **UTF-8 / special chars** → silent `search_replace` match failure. Use `python3 str.replace()` for accented chars or emoji.
- **Code duplication** → Vibe may re-insert a block already written. Grep for duplicate definitions after every run.
- **HTML in prompt** → tags like `<div>` are shell redirects (exit 127). Write HTML content to a temp file; reference the path in the prompt.
- **Source code in bash heredoc** → quotes/backslashes mangle. Use `search_replace` directly; never a helper script that replaces code.
- **Large files are NOT a blocker** (measured 2026-10-01, `docs/harness-audit-2026-10-01.md` H8). One `read_file` call returns the first 51,200 bytes with `was_truncated: true` and the real `file_size_bytes`; `offset`/`limit` page the rest, `grep -n` finds anchors. Never tell the user "Vibe can't read files over 50 KB". The real risk is Vibe reasoning on the first window only, so for big files the harness injects a grep → read offset/limit → edit instruction. Handing it a big *diff to understand* is still a bad idea: split by area.
- **Calling `vibe -p` directly hangs** without a TTY (it waits for stdin EOF; no session is even created). Always go through `vibe-delegate` (pty), or add `< /dev/null`.
- **Tool names differ by view.** The model sees `edit` (`old_string`/`new_string`); the runtime and the stream log `file_system.search_replace`. In prompts say **"the edit tool"** — asking for "search_replace" makes Vibe waste turns on `search_tool_functions`.
- **A turn = one model call, not one tool call.** Vibe can issue several independent tool calls per turn (6 reads + 6 edits took 5 turns). For repetitive edits across many files, ask for **one `run_typescript` call that loops with `tools.file_system.edit`** (verified 2026-10-01: 6 files in one call, 4 turns, ~18 % fewer tokens; each edit is still journaled as `search_replace`, so the WRITE AUDIT stays exact). Otherwise ask for parallel independent calls. Never forbid other tools in the same prompt — a "use the edit tool" line was enough to stop Vibe from batching.
- **Never trust Vibe's description of itself** — check the session store (H11).
- **Files outside the workdir are unreadable** → `--trust` does NOT cover them. Any path outside `workdir` raises an `outside_directory` approval that is auto-denied headlessly: the run exits **0** with 0 tool calls and, before the 2026-08-02 parser fix, said nothing at all. **Any file the prompt points Vibe at must live inside the workdir.** Stage temp inputs in a gitignored dir in the repo, not `/tmp`.
- **Orchestration chain** → 6 failure points in order: CLI auth → pseudo-TTY → stream parser → TOML pricing → git diff → JSON log. When a run produces unexpected results, work down this list. Full details in `SKILL-reference.md`.

---

## Step 1 — Detect workdir

1. `git rev-parse --show-toplevel` in the current directory.
2. If ambiguous or no git repo → ask with `AskUserQuestion`.

---

## Step 2 — Decompose the task

**Critical rule**: keep tasks **atomic and focused** — one objective, one prompt.

| Size | Definition | Max turns | Approach |
|------|-----------|-----------|----------|
| **Trivial** | 1 file, change is obvious and located | — | **Skip delegation — edit directly** |
| **Simple** | 1 file, non-trivial logic or unknown location | 5–8 | 1 vibe call |
| **Medium** | 2–3 related files, 1 objective | 8–12 | 1 structured vibe call |
| **Complex** | >3 files OR business logic OR DB migrations | — | **Break into sub-tasks** |

**Decomposition for complex tasks:**
```
Sub-task 1: Explore / read relevant files (read-only, 5 turns)
Sub-task 2: Implement change A in file X (8 turns)
Sub-task 3: Implement change B in file Y (8 turns)
Sub-task 4: Verify / test (5 turns)
```
→ Check git diff between each sub-task before launching the next.

---

## Step 3 — Write the Vibe prompt

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
- Language: English (better Mistral performance)

**Prompt adaptations:**
- **Any task that defines or calls a specific function**: include the exact signature — `def validate(data: dict) -> tuple[bool, list[str]]:`.
- **No fixed signature, but conventions matter**: point at the file to read first ("read app.py, follow its route/jsonify style") instead — don't do both, they're substitutes.
- **Write/modify tasks**: append an output format block:
  ```
  OUTPUT FORMAT:
  Modified: <file>
  Does: <one line>
  No other prose.
  ```

> ⚠️ **Shell safety**: if the prompt contains UTF-8 accented chars, emojis,
> `:` in Python/YAML code, or typographic apostrophes — the vibe-delegate script
> passes them safely via a temp file (`printf %q`). Never interpolate such a prompt
> directly into a bash heredoc.

**Verification — always use grep, not file re-read:**
```
VERIFY: grep for "def extract_labels" in app.py and confirm it exists.
```

---

## Step 4 — Launch Vibe

```bash
~/tools/vibe-delegate "<workdir>" "<prompt>" [max-turns] [agent] [timeout-secs]
```

| Argument       | Default  | Notes                                           |
|----------------|----------|-------------------------------------------------|
| `workdir`      | —        | Absolute path, must exist                       |
| `prompt`       | —        | Self-contained task description                 |
| `max-turns`    | `10`     | Mistral turn limit — hard cap at 12, never more |
| `agent`        | *(none)* | See agent table below                           |
| `timeout-secs` | `180`    | Wall-clock kill timer                           |
| `--require STR` | *(none)* | Repeatable. Abort before launch if STR is absent in the workdir — pass the `search_replace` anchor here |
| `--with-review N` | *(none)* | After Vibe finishes, Claude reviews the diff and re-delegates fixes up to N times (see Step 8) |
| `--verbose` | *(off)* | Print per-token-type cost breakdown (input/output tokens × pricing) instead of the compact summary line |
| `--no-ghostwrite` | *(off)* | Disable the ghostwrite fallback — after 3 failed Vibe attempts, halt and ask instead of finishing (see Step 6) |

**Available agents:**

These are Vibe's **built-in** agents. Custom agents can add to this list, but
nothing outside it is guaranteed to exist — an unknown name aborts the run in
~1.5s with `Error: Agent 'X' not found`.

| Agent | Type | Use |
|-------|------|-----|
| *(default → `auto-approve`)* | agent | General implementation — all tools run without approval |
| `plan` | agent | **Read-only** — reviews, analysis, planning. The right pick for any "look, don't touch" task |
| `default` | agent | Standard loop, prompts for approval (needs a TTY — avoid headless) |
| `accept-edits` | agent | Auto-approves edits but not other tools |
| `lean` | agent | Reduced tool surface |
| `explore` | **subagent** | Read-only exploration — **cannot** be passed to `--agent`; usable only as a sub-agent from within a run |

> ⚠️ `code-reviewer`, `planner`, and `code-architect` were listed here until
> 2026-08-02 but **do not exist** in current Vibe. Use `plan` for review and
> planning work. Verify against `BUILTIN_AGENTS` in
> `vibe/core/agents/models.py` if a name is ever in doubt.

**Read-only runs write nothing by design** — that is success, not `WROTE_NOTHING`.
Do not apply the Step 6 retry/ghostwrite ladder to a `plan`/`explore` run.

**Recommended max turns:**
- Read/explore: `5`
- Simple change (1 file): `8`
- Medium change (2–3 files): `12`
- Never exceed `12` — decompose instead

**Background launch:**
```bash
~/tools/vibe-delegate "<workdir>" "<prompt>" 10 > /tmp/vibe_out.txt 2>&1 &
# Monitor with: tail -f /tmp/vibe_out.txt
```

---

## Step 5 — Supervise in real time

The script prints live:
```
=== VIBE START ===
Workdir : /path/to/project
Agent   : default
Turns   : 10
Timeout : 180s
Prompt  : Stack: Python/Flask. File: app.py ...
===================
  [read]  app.py
  [tool]  file: app.py
  [tool]  search_replace [OK] ...
  [vibe]  Done. Converted date to datetime.date in fetch_data().
Tool calls: 5
Delegate tokens (run): 4,800  (last turn: 4,600+200)  |  cost ~$0.0086
Claude Sonnet 4.6 eq: same tokens would cost ~$0.0168  (ratio x2.0)
=== VIBE DONE (exit: 0) ===
=== SYNTAX OK (1 check(s)) ===

=== UNCOMMITTED CHANGES ===
 app.py | 4 ++--
[log] → ~/.local/share/delegate-runs.jsonl  (4800 tokens, exit 0, 34.2s)
```

**Vibe never commits.** All changes are left unstaged — `git checkout .` reverts everything if needed.

**Verdict lines (since 2026-09-30) — read these before anything else:**

- Last line is `=== RESULT: OK ... ===` or `=== RESULT: FAILED [reason] ... ===` (or `READ-ONLY`). `FAILED` means nothing usable landed, whatever stdout narrated: never report success, run `git diff`.
- Exit code **3** = vibe exited 0 but the run failed (`wrote_nothing`, `write_mismatch`, `syntax_error`, `sr_fail`, ...). A `vibe-delegate ... && next` chain now stops there.
- `FAILED [turn_cap]` (since 2026-10-01) = Vibe used every `--max-turns` model call and never gave a final answer. Vibe 2.25 exits **0** on this, so before the check it was logged `ok`. Files may be changed but the task is likely partial: diff against the task list, then delegate only the missing part.
- `=== VIBE FINAL ANSWER ===` (since 2026-10-01) = Vibe's complete closing message, read from the session checkpoint. The `[vibe]` stream lines are cut at 400 chars — quote this block, not them.
- `=== WRITE AUDIT (journal vs disk) ===` lists every edit/write call with its **own outcome** (`call: ok` / `call: FAILED (reason)`) and the disk state. `MISMATCH` = a successful call that did not land. A failed edit followed by a successful one on the same file is marked `recovered` and does **not** make the run FAILED (it used to, wrongly). `0 write attempts` = Vibe only explored.
- `[PREFLIGHT] large file(s)` = a file named in the prompt is >40 KB; the harness appended a grep → read offset/limit → edit instruction. Still pass the anchor with `--require`.
- Every prompt also gets a `RUN BUDGET` line (turn count, "use the edit tool", "keep the last turn for a summary"): Vibe has no other way to know its `--max-turns`.
- `VIBE_HARNESS=legacy|unified` forces a backend. Benchmarked 2026-10-01: both 4/4 correct; unified faster (19–21 s vs 24–29 s), legacy ~15–30 % fewer tokens. Default (unset) = unified.
- Sessions live in `~/.vibe/logs/session/unified/<uuid>/{journal,chunks}` (compact JSON; tool `file_system.search_replace`, input `{file_path, content:[{old_str,new_str}]}`). That layout's `meta.json` has no token stats; vibe-delegate reads them from `generations/<CURRENT>/projection-state.json` (`tokenUsage`) and the model from `runtime-state.json`. `0 tokens` / `Model: unknown` on a new run is a bug, not expected.

**Red flags to act on immediately:**

| Flag | Meaning | Action |
|------|---------|--------|
| `[WARN]` | Vibe encountered an error | Read the error, fix manually |
| `[ERROR]` | Vibe refused to start (bad agent name, bad flag) — run died in ~1.5s | Fix the argument named in the message; do NOT retry verbatim |
| `[DENIED]` | A tool call was auto-denied. Almost always a path **outside the workdir** | Move the file inside the workdir and re-run. `--trust` will not fix it |
| `[APPROVAL]` | Vibe needed a permission it did not have | Same as `[DENIED]` — check the `outside workdir` label |
| `[tool]  search_replace [FAIL]` | UTF-8 match failure | Edit manually with Python `str.replace()` |
| `exit: 1` or non-zero | Vibe failed / did not complete verification | Read diff, correct prompt |
| No `[tool]  file:` lines, or `0 files changed` | Looks like `WROTE_NOTHING` — **but this is stdout, not proof.** The harness only prints what its stream parser recognized; it does not print what Vibe actually submitted to `write_file`. Do the journal check below before treating this as a failure. | See **mandatory pre-check** below. Only once that check comes back genuinely empty: revise prompt and retry; ghostwrite fallback after 3 attempts. Follow Step 6. **Not applicable to `plan`/`explore`** — writing nothing is correct there. |
| Mangled tool name in output (e.g. `write_filecepte`) | Vibe produced a garbled tool call — write never executed | Same journal check as above before assuming the content is gone. |
| `=== SYNTAX ERRORS ===` | Post-run syntax check failed | **Fix before committing** |
| Same file read 5+ times | Vibe is looping — run likely lost | Abort, check diff, try again |

**Known bugs and workarounds:**

| Bug | Cause | Fix |
|-----|-------|-----|
| Variable declared twice | Vibe doesn't check scope | Grep the variable before relaunching |
| Truncated prompt | Special chars in inline prompt | Script uses temp file — should be fixed |
| Wrote a Python helper just to replace code | Misdiagnosed search_replace limit | Use search_replace directly for ASCII code; write_file only if new content is too long for the prompt |
| Empty run — 0 files changed despite ≥3 tool calls | Multi-edit prompt: first `search_replace` target not found byte-for-byte | Split into sequential single-change runs; grep target string locally before delegating |
| `Tool calls: 0` on a run that clearly did work; no `[vibe]` answer line | **Fixed 2026-08-02.** The stream parser only understood the legacy `role`-keyed schema; current Vibe emits tool calls as `type: effect` and message content as a **list** of blocks. `content.lower()` on that list threw `AttributeError`, killing the parser and discarding the whole run output | Already patched. If it reappears, the run output is still recoverable from `~/.vibe/logs/session/<newest>/messages.jsonl` — nothing is lost, only unprinted |

**If exit non-zero:** do not relaunch immediately. Read the diff, understand what was done, fix the prompt.

**Mandatory pre-check before declaring WROTE_NOTHING.** stdout is a filtered
stream, not a record of what Vibe did — the parser can drop or mislabel a
write it doesn't recognize the shape of. The session journal is not filtered:
`~/.vibe/logs/session/session_<ts>_<id>/messages.jsonl` records the exact
arguments of every `write_file`/`search_replace` call, whether or not the
write later succeeded. vibe-delegate already runs this check for you — when
the filesystem shows 0 changed files, it scans the journal for the *newest*
session and prints an `[RECOVERY]` block listing every write attempt found,
with char counts, before the syntax-check section. **Read that block before
concluding the run failed.** A run that "wrote nothing" per stdout but shows
a few-KB `write_file` in `[RECOVERY]` did not fail — the content exists and
is very likely usable; treat it as a formatting/parsing problem, not an empty
run, and inspect the content in the journal directly:

```bash
JOURNAL=$(ls -t ~/.vibe/logs/session/*/messages.jsonl 2>/dev/null | head -1)   # legacy layout only; for unified sessions read WRITE AUDIT
python3 -c "
import json
for line in open('$JOURNAL'):
    m = json.loads(line)
    if m.get('role') != 'assistant': continue
    for tc in (m.get('tool_calls') or []):
        fn = tc.get('function') or {}
        if 'write' in fn.get('name',''):
            print(json.loads(fn['arguments'])['content'])
"
```

Confirmed case (2026-08-11, a delegated Python project): stdout showed `0 files changed` and a
turn-limit stop on a `temperature.py` delegation. The journal held a complete,
correct 5,706-char module from the *first* `write_file` call — Vibe had simply
wrapped it as `{"module_docstring": """...."""}\n<real source>` instead of
emitting raw source, the write step rejected the shape, and Vibe burned the
rest of the turn budget on write→rm→write instead of on the actual task.
Stripping the one-line JSON envelope recovered the module outright — no
retry needed. The retry that *was* run cost ~180k tokens for a result no
better than turn 1's output already sitting in the journal.

If, after reading the journal, there is genuinely no `write_file`/`edit` call
for the target file at all — that's the real WROTE_NOTHING, and Step 6 applies.

---

## Step 6 — Iteration

- **Max 3 attempts** per sub-task before escalating to the user.
- Between attempts, **read the git diff** to avoid doubling partial work.

### WROTE_NOTHING / failed write — auto-retry then ghostwrite (default)

When a run produces any of the following:
- No `[tool]  file:` lines (WROTE_NOTHING)
- Mangled tool call output (e.g. `write_filecepte`, `search_replacecepte`)
- Non-zero exit with 0 files changed

First, **revise the prompt** (simpler target, explicit file path, shorter scope) and re-run. This counts against the 3-attempt limit.

If all 3 attempts still produce WROTE_NOTHING or a failed write, **the default is to finish the task, not halt.** Claude writes the content itself (ghostwrite) — either delegating only the file-write step to Vibe or writing the file directly — then continues the chain. The task always completes; a stubborn Vibe never strands the run.

**The Step 7 report must list ghostwritten files separately** from Vibe-authored files — never silently mix them:

```
Files ghostwritten (Claude-authored after 3 failed Vibe attempts):
  - path/to/file.ext
```

### `--no-ghostwrite` — opt out of the ghostwrite fallback

When the user passes `--no-ghostwrite` to `/vibe`, Claude must **not** ghostwrite. After 3 failed attempts, halt and ask instead:

```
⛔ Vibe wrote nothing after 3 attempts (--no-ghostwrite set).
  File expected : <path>
  Failure signal: <WROTE_NOTHING | mangled write | exit N, 0 files>
  Sub-task      : <description>

Options:
  (r) Revise prompt manually and retry
  (a) Abort
```

Do not proceed to subsequent sub-tasks until resolved.

---

## Step 7 — Report to the user

```
✓ Vibe finished — <1-line summary>

Files modified:
  - path/to/file.ext (+X / -Y lines)

[If problem]:
⚠ <description> — completing manually / relaunching?

Ready to commit?
```

**When `--verbose` was passed:** after the file list, quote the full token/cost block verbatim from the script output — the lines starting with `Model`, `  Input`, `  Output`, `  Total`, `  Claude`. Do not paraphrase or summarize them. Example:

```
Model               : mistral-medium-3.5
  Input  :     45,120  @  $1.50/M  = $0.0677
  Output :      1,280  @  $7.50/M  = $0.0096
  Total  :     46,400              = $0.0773
  Claude :     46,400  (@ $3/$15/M)  = $0.1531  (x1.98 cheaper)
```

---

## Step 8 — Review pass (`--with-review N`)

Triggered only when the user passes `--with-review N` to `/vibe`. Runs after Step 5 confirms exit 0.

### 8.1 — Read the diff

Run `git diff` (or `git diff HEAD` if changes are staged). Read the full output. This is Claude's review input — do not ask Vibe to review.

### 8.2 — Classify issues

Scan only for **fundamental issues**. Flag these:

| Category | Examples |
|----------|---------|
| Incorrect logic | off-by-one, wrong branch condition, inverted boolean |
| Crash-causing gap | unhandled None/null dereference, missing required field, index out of range |
| Broken contract | function signature changed without updating callers, return type mismatch |
| Wrong scope | change applied to wrong file/function/class |
| Security hole | unsanitized user input passed to shell/SQL/eval, credentials in plaintext |

**Do NOT flag:** style, naming, formatting, unused imports, performance, readability, or subjective preferences. If unsure whether an issue is fundamental, skip it.

### 8.3 — Re-delegate one issue per iteration

For each fundamental issue found (up to N):

1. Write one atomic Vibe prompt targeting that single issue (follow Step 3 rules).
2. Launch via `vibe-delegate` (same workdir, same model).
3. After Vibe finishes, re-read the diff and re-evaluate: did the issue get fixed?
4. Move to the next issue (or stop if N exhausted or no issues remain).

**Never bundle two fixes into one prompt.** One issue → one delegation → one diff check.

If N iterations are exhausted and issues remain, list them but do not attempt further fixes — report and stop.

### 8.4 — Tracking state across iterations

Maintain these counters locally (not persisted mid-run):

```
review_iterations_allowed  = N
review_iterations_used     = 0
review_issues_found        = <count from initial diff review>
review_issues_fixed        = 0
review_issues_remaining    = review_issues_found
```

Increment `review_iterations_used` and `review_issues_fixed` after each successful re-delegation. Update `review_issues_remaining` accordingly.

### 8.5 — Report

After all iterations or no issues remain, append to the Step 7 report:

```
Review pass (--with-review N):
  Issues found:     X
  Issues fixed:     Y
  Issues remaining: Z
  Iterations used:  A / N
```

If issues remain, list each one briefly (file:line — description). Do not re-attempt them.

### 8.6 — Log fields

After the review pass, the run log entry for the **original** Vibe run must include these additional fields in `~/.local/share/delegate-runs.jsonl`:

```json
"review_iterations_allowed": N,
"review_iterations_used": A,
"review_issues_found": X,
"review_issues_fixed": Y,
"review_issues_remaining": Z
```

When `--with-review` is not used, all five fields are omitted (do not write them as 0).

---

## Orchestration rules

- **Decompose before delegating** — one task, one prompt.
- **Streaming always** — never `--output text`.
- **Check diff between sub-tasks** — never launch the next one blind.
- **Ghostwrite only as a last resort** — always delegate to Vibe first; never write code yourself before 3 failed attempts. After 3 failures the default is to ghostwrite and finish (declare it in the Step 7 report). `--no-ghostwrite` disables the fallback and halts instead. See Step 6.
- **Max 12 turns per call** — decompose instead of extending.
- **Grep target before delegating** — `grep -n "exact_target" file.py` before any `search_replace` prompt. Pass that anchor as `--require "exact_target"` so the delegate aborts before launching if it's gone. Always use grep for VERIFY, not file re-read.
- **Match model to task** — inline-edit tasks → `deepseek-flash` or `mistral-medium-3.5`; never route edits to agent-mode `devstral-small` (read/explore only).
- **UTF-8 / emoji in the prompt** → the script handles it via temp file, but test with a short prompt first.
- **UTF-8 in OLD/NEW strings → mandate python3, no exceptions** — before writing any Vibe prompt, scan every OLD and NEW string for accented chars (é è à ç ù ô î û ñ...) or emoji. If ANY are present, the prompt MUST explicitly instruct Vibe to use `python3 -c` with `pathlib.Path.read_text/write_text(encoding='utf-8')` for those changes — never `search_replace`. A `search_replace [OK]` on UTF-8 content is a silent no-op: the tool call is accepted but the string is never found. This is the #1 cause of phantom successful runs that changed nothing.
- **Check string delimiters before delegating JS/JSON changes** — if a replacement value contains apostrophes (`'`) and the target JS property uses single-quote delimiters, the NEW string must switch to double-quotes (`"`) for that property. Scan OLD→NEW pairs for this conflict before writing the prompt; never leave it to Vibe to discover at runtime.
- **After any run that touches imports: grep the import line** — always run `grep "^from X import" file.py` before the next sub-task.
- **search_replace [OK] ≠ correct change** — always grep the specific changed line, not just check syntax.
- **Provide data structure context** — if a route accesses a DB payload, include the exact field paths (`payload['produit']['nom']`) in the prompt.
- **Reuse existing assets** — for UI tasks, tell Vibe to link existing CSS/JS files. "Use `/static/style.css` and CSS class `bar-row`" is always better than "generate a dark theme".

---

## Run Log

Every run appends one JSON entry to `~/.local/share/delegate-runs.jsonl`.
Log fields and jq queries → see `SKILL-reference.md`.

```bash
~/tools/delegate-report                  # vibe runs only (default)
~/tools/delegate-report --since 7        # last 7 days
~/tools/delegate-report --project myapp  # filter by project
~/tools/delegate-report --fails          # failures only
~/tools/delegate-report --adapt          # failure rates by prompt adaptation
~/tools/delegate-report --all            # all delegates (shared log)
~/tools/delegate-report --delegate opencode  # a specific delegate
```

Or via Claude Code: `/vibe-report [args]`. Log fields and jq queries → `SKILL-reference.md`.

**Review pass fields** — see §8.6 for log field definitions. Present only when `--with-review N` was used.

---

## See Also

A sister delegate using Gemini CLI exists: [gemini-skill](https://github.com/pcx-wave/gemini-skill).
Both write to the same `delegate-runs.jsonl` log, making runs comparable across delegates.

This skill is improved regularly — run [update-skills](https://github.com/pcx-wave/update-skills) to pull the latest version of this skill, as well as all your other skills!
