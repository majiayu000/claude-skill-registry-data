---
name: statusline-doctor
description: >-
  Diagnose a blank, empty, or broken Claude Code statusline and suggest fixes.
  Invoke when the user says things like "my statusline is blank", "the statusline
  isn't showing", "statusline broken", "troubleshoot the statusline", "why is my
  bar empty", "nothing renders in my status bar", or "statusline not working on
  Windows". Mostly read-only: it inspects config, runtime, and settings, then
  test-renders. It only changes files on explicit user confirmation.
---

# statusline-doctor

Figure out why the usage-aware statusline is blank or wrong, then suggest concrete
fixes. This skill is **mostly read-only**. You inspect things and report a PASS/FAIL
table. You do **not** edit `statusline_config.json`, `settings.json`, or anything else
unless the user explicitly confirms a specific change. When a fix means editing the
config or the install command, point them at `/statusline-config` and
`/statusline-install` rather than doing it yourself.

This whole project is **English only**. Everything you write or report stays in English.

## How to run the diagnosis

Work through the seven checks below **in order**. For each one, determine PASS or FAIL,
and on FAIL note the concrete fix. Use the real tools to gather facts (Read the files,
run the runtime probes, run the test-render) — do not guess. At the end, print a tidy
report (see "Final report" at the bottom).

**Diagnose the ACTIVE statusline, not the repo copy.** The bar that Claude Code is really
running is usually the **deployed** copy (e.g. `~/.claude/statusline.py`), not the copy in
this repo. Every check below operates on the *resolved active* `statusline.py` and its
config — never a hardcoded repo path. Check 1 resolves them once, via the shared helper,
and the rest of the diagnosis reuses what it found.

First, establish the two base paths you will reuse:

- **Renderer dir** = the folder that holds the **active** `statusline.py` — as resolved by
  Check 1 (the helper's `statusline_py`). The user's *live* deploy is usually `~/.claude`
  (i.e. `C:/Users/<you>/.claude` on Windows, `/Users/<you>/.claude` or
  `/home/<you>/.claude` elsewhere); the repo root (e.g. `F:/ai/statusline`) is only the
  active one if the install actually points there. Do not assume — let Check 1 tell you.
- **Home** = `~` expanded (`C:/Users/<you>` on Windows, `/Users/<you>` or
  `/home/<you>` otherwise).

---

### Check 1 — Locate the ACTIVE statusline, then parse its config

**Resolve the active install with the shared helper first — do not guess paths.** All
skills share one resolver that lives in the `statusline-config` skill. From this
(`statusline-doctor`) skill it is a sibling:

```
<skills-dir>/statusline-config/statusline_io.py
```

i.e. relative to this skill's own directory: `../statusline-config/statusline_io.py`.
Run its `locate` subcommand and read the JSON it prints to stdout (it always exits 0 and
always prints valid JSON, even on error):

**PowerShell:**

```powershell
python <skills-dir>/statusline-config/statusline_io.py locate
```

**bash:**

```bash
python <skills-dir>/statusline-config/statusline_io.py locate
```

It prints one JSON object:

```json
{"statusline_py": "...", "config_path": "...", "settings_json": "...",
 "launcher": "...", "source": "pointer|settings|none",
 "pointer_path": "...", "notes": "..."}
```

How `locate` resolved it (so you can explain it): (a) a gitignored **pointer** file
`<.claude>/.statusline-active.json` next to the skills' `.claude` dir, else (b) parse the
active **settings.json** (`.claude/settings.json` found upward from CWD takes precedence
over `~/.claude/settings.json`) and read `statusLine.command`, else (c) **none**.

**Report the resolution up front**, because every later check depends on it:

- **`source`** — `pointer` (a saved pointer was used), `settings` (parsed from the active
  `settings.json`), or `none`.
- The resolved **`statusline_py`** (the active renderer) and **`config_path`** (the active
  config) — these are the paths the rest of this report diagnoses.
- **Which `settings.json` was read** (`settings_json`) and the **`launcher`** (e.g.
  `uv run`, `python3`, `powershell -NoProfile -File`).
- If `source == "settings"`, mention you *can* save a pointer for instant future runs via
  `python <skills-dir>/statusline-config/statusline_io.py save-pointer ...` — but as a
  read-only doctor, only do so on explicit user confirmation.

**If `source == "none"`:** no active statusline could be located — neither a pointer nor a
`statusLine` block in any settings.json. Report this as the headline finding (it alone
explains a blank bar: there is nothing wired up to render). Suggest **`/statusline-install`**
to deploy and wire it. You can still ask the user where their `statusline.py` is if they
believe one exists, but do not invent a path. Skip the JSON parse below (there is no
resolved `config_path`) and carry the "none" status into the final report.

The renderer itself resolves *its* config path in this order (the helper's `config_path`
already reflects it — this is just the underlying rule):

1. The `STATUSLINE_CONFIG` environment variable / `STATUSLINE_CONFIG=` set in the launch
   command, if present.
2. Otherwise `statusline_config.json` **next to the active `statusline.py`** (same
   directory).
3. There is no separate `~/.claude` fallback inside the code — but in practice the live
   `statusline.py` lives in `~/.claude`, so its sibling config is
   `~/.claude/statusline_config.json`.

Then, on the **resolved active `config_path`**:

- Report whether the config file **exists**.
- If it exists, Read it and confirm it **parses as JSON**. A trailing comma, a smart
  quote, or an unclosed brace makes the whole file invalid.

Important nuance to tell the user: **a missing or invalid config is NOT itself the cause
of a blank bar.** `load_config()` wraps the whole read-and-parse in `try/except` and on
*any* error falls back to built-in defaults, so the bar still renders with the default
layout. If the bar is blank *and* the config is invalid, the invalid config only means
"your customizations are being ignored, you're seeing the default bar", not "the bar is
empty". Keep looking for the real cause (Checks 4–6, especially Check 2's crash case and
Check 5's launcher).

- **PASS:** the active install was located (`source` is `pointer` or `settings`) and its
  config exists and parses (or is intentionally absent → defaults apply).
- **FAIL (not located):** `source == "none"` → no active statusline found. Headline cause
  of a blank bar; fix is `/statusline-install`.
- **FAIL (parse error):** report the exact JSON error and line. Fix: correct the JSON
  (or let `/statusline-config` rewrite it cleanly). Note the bar is using the built-in
  default layout until then.

Then list the template lines:

- **Active lines** = keys under `templates` that start with `line` **and whose value is a
  string** (e.g. `line1`, `line2`, …), in order. These are what get printed.
- **Inactive keys** = anything under `templates` that does **not** start with `line`:
  `_disabled_*`, `_comment`, or any other name. These are deliberately ignored — that is
  the supported way to keep a line turned off. Report them as "ignored (not active)", not
  as errors.

If there are **zero active `line*` keys** (e.g. every line has been renamed to
`_disabled_*`), this is **NOT a cause of a blank bar** — and getting this right matters,
because it's easy to misdiagnose. Here is exactly what the code does: `load_config()`
builds `file_lines = {k: v for k, v in t.items() if k.startswith("line") and
isinstance(v, str)}` and then `if file_lines: templates = file_lines`. When every line is
disabled, `file_lines` is an empty dict, which is falsy, so the assignment is skipped and
the renderer **keeps `DEFAULT_TEMPLATES` and renders the full built-in default bar**
(verified empirically: exit 0, complete colored default output — not a blank bar).

So flag zero active lines as **INFO**, not FAIL: "No active `line*` keys — your custom
lines are all turned off, so the renderer is falling back to the built-in DEFAULT layout.
If the default bar is what you're seeing, that's why. To use your own lines instead,
rename a `_disabled_*` key back to `lineN` (or run `/statusline-config`)." Do **not** tell
the user this is why the bar is empty — it isn't.

---

### Check 2 — Every placeholder is known (a typo here blanks the WHOLE bar)

For each **active** line, scan for `{...}` placeholders and confirm each is in the known
set below. This is one of the strongest findings a doctor can produce, because the
failure mode is severe: an unknown placeholder makes `template.format(**values)` raise
`KeyError`. That call (statusline.py line 1108) is **NOT** wrapped in try/except, so the
`KeyError` propagates out of `main()` and **crashes the entire renderer** — non-zero exit,
a traceback on stderr, and **nothing on stdout, so the WHOLE bar goes blank** (not just
the one bad line). Verified empirically: a config with `{usd}` on a line produced
`KeyError: 'usd'` and exit 1 with zero output. **A typo'd or invented placeholder is a
real, common cause of a completely empty bar** — check this carefully whenever the bar is
blank.

Known placeholders (the complete set — there is no other):

- Color / format: `{c.NAME}` (any color key, see Check 3 list), `{r}`
- Session: `{time}` `{version}` `{model}` `{effort}`
- Context: `{ctx}` `{ctx_percent}` `{ctx_bar}` `{ctx_bar:N}` (N = integer cell count)
  `{ctx_micro}` `{align_pad}`
- Tokens: `{total}` `{input}` `{output}` `{cached}`
- Usage gauges: `{usage_bars}` `{usage_resets}` `{usage_micro}` `{compact_usage_micro}`
- Path / git: `{path}` `{branch}` `{added}` `{removed}`
- Weather: `{weather}` `{sun}`
- Status: `{status}` `{status:N}` (N = integer char cap, 0 = unlimited) `{status_icon}`
  `{status_header}`
- Legacy (back-compat only — do **not** suggest adding it): `{peak_label}`

Notes while scanning:

- `{ctx_bar:N}` with a numeric `N` is valid (fixed-width bar). `{ctx_bar:foo}` (non-numeric
  spec) is tolerated by the code (falls back to a default width) but is sloppy — mention it.
- `{status:N}` with a numeric `N` is valid (char cap for that line). `{status:foo}`
  (non-numeric spec) is sloppy — mention it.
- A bare `{c.something_not_in_colors}` does not crash (unknown color keys resolve to white),
  but flag it as "color key not recognized — will render white".
- Common typos that DO crash the whole bar (they aren't keys in the values dict):
  `{cxt}`, `{ctx_pct}`, `{usage_bar}` (singular), `{branchname}`, `{commit}`, `{cost}`,
  and `{usd}` — there is no `{usd}` placeholder; `usd` is only a *color* key (`{c.usd}`).
  Flag any of these as a fatal placeholder that blanks the entire bar.

- **PASS:** all placeholders on every active line are known.
- **FAIL:** list each unknown placeholder and the line it's on, and warn that it crashes
  the whole renderer (blank bar) — not just that line. Fix: remove or correct it (or run
  `/statusline-config`).

---

### Check 3 — `emoji_width` sanity

`emoji_width` controls only the **alignment math** between line1 and the big `{ctx_bar}` /
the usage bars — it never blanks the bar. Valid values are `1` or `2`; the code treats
anything that is not exactly `1` as `2`.

- If the user reports the bar "looks shifted", "is offset", or "doesn't line up under
  line1", suggest **flipping** `emoji_width` (1↔2) to match how their terminal draws
  emoji. Windows Terminal / iTerm2 usually render emoji 2 columns wide (`2`); some
  terminals render them 1 wide (`1`).
- Only relevant when a line uses the auto-aligned big `{ctx_bar}` (with `{align_pad}`) or
  `{usage_bars}`. The inline `{ctx_micro}` and fixed `{ctx_bar:N}` do not depend on it.

- **PASS:** `emoji_width` is `1` or `2` (or absent → default `2`).
- **FAIL / hint:** value present but odd, or the user reports misalignment → suggest the flip.

---

### Check 4 — Runtime on PATH

The statusline is launched as a shell command by Claude Code. The command needs a working
Python (≥ 3.7, because the code uses `datetime.fromisoformat`). `uv` is an optional
convenience launcher; plain `python`/`python3` works just as well since there are zero
third-party dependencies.

Probe (report what is found):

- `python --version` and/or `python3 --version` — is it ≥ 3.7?
- `uv --version` — present or not? (Not required, just report.)

On Windows, also be aware the "App execution alias" stub for `python` can intercept the
command and do nothing — if `python --version` prints nothing or opens the Microsoft Store,
that is the culprit; tell the user to install real Python (or use `uv`) and disable the
alias.

- **PASS:** at least one of `python`/`python3`/`uv` resolves to Python ≥ 3.7.
- **FAIL:** none resolve. Fix: install Python 3.7+ (or `uv`), and make sure the launcher
  named in `settings.json` (Check 5) is the one that actually exists on PATH.

---

### Check 5 — `settings.json` `statusLine.command` (the #1 Windows cause)

Read the Claude Code settings file — prefer the **`settings_json`** that Check 1's helper
already reported it read (project-level `.claude/settings.json` takes precedence over the
user-level `~/.claude/settings.json`). Find the `statusLine` block:

```json
"statusLine": { "type": "command", "command": "uv run ~/.claude/statusline.py", "padding": 0 }
```

Verify all of:

1. **A `statusLine` block exists** with `"type": "command"`. If it is missing entirely,
   that alone explains a blank bar — there is nothing configured to render. Fix: run
   `/statusline-install`.
2. **The script path in `command` points at a file that exists.** Extract the path
   argument (after `uv run`, `python`, `python3`, `powershell -File`, …), expand `~`, and
   confirm `statusline.py` (or the `.ps1` wrapper) is really there.
3. **WINDOWS PATH RULE — check this carefully, it is the single most common cause of a
   blank bar on Windows.** The path must use **forward slashes** (`C:/Users/you/.claude/
   statusline.py`) or `~` (`~/.claude/statusline.py`) — **never backslashes**. On Windows,
   Claude Code runs the command through Git Bash when it is installed; Git Bash treats `\`
   as an escape character, so `C:\Users\you\.claude\statusline.py` is mangled and the
   command fails **silently** → blank bar. Fixes:
   - Best: rewrite the path with forward slashes or `~`
     (e.g. `"uv run ~/.claude/statusline.py"`).
   - The Git-Bash drive form also works: `uv run /c/Users/you/.claude/statusline.py`.
   - If there is **no Git Bash** installed, Claude Code uses PowerShell; then a PowerShell
     wrapper is the robust option:
     `"powershell -NoProfile -File C:/Users/you/.claude/statusline.ps1"`.
4. **The launcher resolves.** If the command starts with `uv run`, `uv` must be on PATH
   (Check 4). If it starts with `python`/`python3`, that must resolve. A command of
   `uv run ...` on a machine without `uv` → blank bar. Fix: switch the launcher to one that
   exists, or install the missing launcher.
5. **The command path matches the ACTIVE `statusline.py` from Check 1.** Normalize both
   (expand `~`, forward slashes, absolute) and compare the script path inside
   `statusLine.command` against the helper's resolved `statusline_py`. They should be the
   same file. **Caveat for the PowerShell-wrapper install (sub-check 2's `.ps1` case):**
   when `command` names a `.ps1` wrapper, the helper deliberately resolves `statusline_py`
   to the sibling `statusline.py` in the **same directory**, not to the `.ps1` itself — so a
   literal `.ps1`-vs-`.py` compare will *always* look different even though it's a perfectly
   valid deploy. In that case compare the **directory** of the wrapper (or the sibling
   `statusline.py` in it) against the resolved `statusline_py`: they match when the wrapper
   sits next to that renderer. Only flag a mismatch when the directories (real renderers)
   actually differ, or when the script the command names does not exist on disk. A genuine
   **mismatch** is a likely cause of a **stale or blank bar**: Claude Code is launching a
   different (or non-existent) script than the one you are diagnosing — e.g. the pointer
   points at `~/.claude/statusline.py` but `command` still runs the old repo copy, or
   vice-versa, or the script that `command` names does not exist on disk. Report the two
   paths side by side and call out the discrepancy. Note: if Check 1's `source` was
   `pointer`, the pointer may simply be stale relative to a since-changed `settings.json` —
   re-running with a fresh pointer (or `save-pointer` after `/statusline-install`) realigns
   them.

Flag every problem you find separately. Backslashes in the path are the headline check —
call it out explicitly even if everything else passes.

- **PASS:** block exists, path exists, path uses `/` or `~` (no backslashes), launcher
  resolves, and the command path matches the active `statusline.py` from Check 1.
- **FAIL:** report exactly which of the five sub-checks failed and the fix. Editing
  `settings.json` is what `/statusline-install` does — recommend it rather than hand-editing.

---

### Check 6 — Usage token source (for `{usage_*}` segments)

Only relevant if an active line uses `{usage_bars}`, `{usage_resets}`, `{usage_micro}`, or
`{compact_usage_micro}`. If none of those appear, **skip this check** and say so.

`claude_usage.py` resolves the OAuth token in this order (the token is never written to disk):

1. **`CLAUDE_CODE_OAUTH_TOKEN`** environment variable (any OS). Check if it is set.
2. **macOS login Keychain** (`Claude Code-credentials`), read via `/usr/bin/security` —
   **macOS only**, auto-detected, no prompt when launched by Claude Code. (On Windows/Linux
   this step is skipped.)
3. **`~/.claude/.credentials.json`** with `claudeAiOauth.accessToken` — the Linux / Windows
   / headless path. On Windows that file is `C:/Users/<you>/.claude/.credentials.json`.
   Check it exists and contains a `claudeAiOauth.accessToken` (do **not** print the token
   value — just confirm presence).

Report which source (if any) is available. **Crucial framing:** if no token is found, the
usage segments simply render **empty** and every other segment still works — **this is not
a bug**, it is the documented graceful degradation. Only call it a problem if the user
specifically expects the session/weekly usage gauges to show and they are blank.

If a token *is* present but usage is still blank, possible causes to mention: no network
(the fetch times out → empty), an expired access token (start Claude Code to refresh it, or
run `claude setup-token`), or `~/.claude/usage_cache.json` holding a stale empty result
(it refreshes within ~60s).

- **PASS:** a token source is available, **or** no usage placeholders are used (N/A).
- **INFO/FAIL:** no token → usage segments will be empty by design; explain how to enable
  them (set `CLAUDE_CODE_OAUTH_TOKEN`, or sign in with Claude Code so
  `~/.claude/.credentials.json` exists).

---

### Check 7 — Test-render with the sample input

Run the **real renderer** against the bundled canonical sample so you can see exactly which
segments come out and which are empty. Use the **active `statusline_py` and `config_path`
from Check 1** — point `STATUSLINE_CONFIG` at the active config so you reproduce their
layout, and run the active renderer — but do **not** modify either file.

The sample input ships next to this skill as `assets/sample_input.json`. Use it.

**PowerShell:**

```powershell
$env:STATUSLINE_CONFIG="<config_path-from-Check-1>"; Get-Content <skill-dir>/assets/sample_input.json | uv run <statusline_py-from-Check-1>
```

(fallback if `uv` is absent: replace `uv run <statusline_py-from-Check-1>` with
`python <statusline_py-from-Check-1>`.)

**bash:**

```bash
STATUSLINE_CONFIG=<config_path-from-Check-1> uv run <statusline_py-from-Check-1> < <skill-dir>/assets/sample_input.json
```

(fallback: `python3` instead of `uv run`.)

Run the active `statusline.py` resolved by Check 1 (the live one is usually
`~/.claude/statusline.py`), not a hardcoded repo path. A **non-empty colored line is success** — that means the
renderer itself works and any blank bar is environmental (Check 5 launcher/path, or the bar
was never invoked).

Then explain **why** each empty segment is empty — most "broken" segments are expected:

| Segment | Why it can be empty (expected) |
| --- | --- |
| `{weather}` / `{sun}` | Weather is only fetched when an active line uses them; empty if offline with no cache, or the city/coords aren't set. Not a bug. |
| `{usage_*}` | No OAuth token (Check 6) or no network → usage data unavailable → renders empty. Not a bug. |
| `{branch}` / `{added}` / `{removed}` | If the cwd is not a git repo, **any line that contains `{branch}` is replaced by the bare path** — it does not matter what else is on that line, so `{added}`/`{removed}` and any surrounding text on that line disappear too. The sample `cwd` is not a real git repo, so this is expected. Not a bug. |
| `{effort}` | Empty when the model doesn't support effort; the sample sets `high`, so it should show `(high)`. |
| `{status}` / `{status_icon}` / `{status_header}` | No active incidents currently reported on the Claude status page, or the RSS fetch failed (falls back to `[]`). Both outcomes render the placeholder empty and the entire line is hidden — this is correct behavior, not a bug. |
| Whole line missing | A line that renders to only whitespace/color codes is intentionally skipped (so usage/weather lines vanish when they're empty). |

If the test-render produces a full colored line but the user's real bar is blank, the
conclusion is: **the renderer is fine — the problem is how Claude Code launches it** (Check
5: backslash path, missing launcher, or missing `statusLine` block). Say so explicitly.

If the test-render itself **errors with a traceback and prints nothing** (non-zero exit),
capture the error and trace it:

- `KeyError: '<name>'` from `template.format(**values)` → an **unknown placeholder**
  (Check 2). This crashes the whole renderer and is exactly what a user's typo'd line does
  to their live bar — a strong root-cause finding for a blank bar.
- A JSON / config error → trace to Check 1 (though note `load_config` should swallow those
  and fall back to defaults, so a crash here usually means a placeholder issue instead).
- Any other traceback → trace to a runtime issue (Check 4) or report it verbatim.

---

## Final report

Produce a tidy summary the user can scan. Suggested shape:

```
Statusline doctor report
========================
Active install: source=settings (read ~/.claude/settings.json)
                statusline.py = ~/.claude/statusline.py
                config        = ~/.claude/statusline_config.json
                launcher      = uv run

1. Config file ......... PASS  (~/.claude/statusline_config.json, valid JSON; active: line1, line2, line3; ignored: _disabled_ctx_bar_line, _comment)
2. Placeholders ........ PASS  (all known)
3. emoji_width ......... PASS  (2)
4. Runtime ............. PASS  (python 3.12, uv 0.5.x)
5. settings.json ....... FAIL  -> command path uses backslashes: "C:\Users\you\.claude\statusline.py"
                                  Fix: change to forward slashes / ~  ->  "uv run ~/.claude/statusline.py"
6. Usage token ......... INFO  (no token; usage segments will be empty by design)
7. Test-render ......... PASS  (colored output; weather + usage empty as expected)

Most likely cause: Windows backslash path in settings.json (Check 5).
Suggested fix: run /statusline-install to rewrite the command with forward slashes,
or fix the path by hand. Run /statusline-config to adjust the layout/colors.
```

When `source == "none"`, lead the report with that instead of the path block, e.g.:

```
Active install: source=none — no active statusline could be located
                (no pointer, no statusLine block in any settings.json)

Most likely cause: nothing is wired up to render the bar.
Suggested fix: run /statusline-install to deploy statusline.py and add the
statusLine block to settings.json.
```

Rules for the report:

- Open with the **Active install** block: `source` (pointer/settings/none), the resolved
  `statusline.py` + `config` paths, which `settings.json` was read, and the launcher
  (from Check 1).
- Each of the 7 checks gets a PASS / FAIL / INFO / N/A line with a one-line reason.
- End with a single **"most likely cause"** line and the concrete next step. If
  `source == "none"`, the most likely cause is "nothing wired up" → `/statusline-install`.
- When the fix is a config change, recommend **`/statusline-config`**; when it's a
  settings/install change, recommend **`/statusline-install`**.
- **Do not change any file** unless the user explicitly confirms a specific edit. This skill
  diagnoses; the other two skills apply. English only.
