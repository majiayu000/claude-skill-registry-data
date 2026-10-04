---
name: "HUD: Prose Health"
description: "Check every layer of the prose-gating suite is still wired and report how Claude's own output is trending against the house rules"
when_to_use: "When Jason asks whether the writing-style setup is working, whether em dashes are creeping back, how often the commit-msg hook fires or after editing settings, hooks, the output style or the commit and prose skills; also as a periodic check."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: hud
disable-model-invocation: true
allowed-tools: ["Bash(~/.claude/library/scripts/prose-health.py:*)", "Bash(~/.claude/library/scripts/prose-metrics.py:*)", "Read"]
arguments: ["scope"]
argument-hint: "[metrics] (no args = full check; metrics = the output trend only)"
---

# HUD: Prose Health

The prose-gating suite has five layers: the output style and CLAUDE.md in the system prompt, the `commit-msg` git hook, the strict scan the prose skills run before their approval gates, the rejection contract in the commit skills and the scanner that backs all of it. Any one of them can silently come unwired (a settings file rewritten, a hook losing its executable bit, a skill edited without its gate text). This skill runs the deterministic check and turns the result into a fix list.

## Step 1: Run the check

Full check (default):

```bash
~/.claude/library/scripts/prose-health.py
```

`metrics` only:

```bash
~/.claude/library/scripts/prose-metrics.py --days 28
```

The full check records today's output metrics into `library/state/prose-metrics.json` as a side effect, so the trend survives transcript pruning.

## Step 2: Relay the report verbatim

Print the script's output as it came: the status lines, any `tree hits` list and the metrics table. Do not summarise the numbers away; the table is the point.

## Step 3: Turn every WARN and FAIL into a next action

One line per non-PASS check, naming the file to open or the command to run:

| Check         | Fix |
|---------------|-----|
| `settings`    | Edit `~/.claude/settings.json`: `outputStyle` and the `attribution` block (see `docs/reference/configuration.md`) |
| `style`       | Edit `output-styles/british-dev-goblin.md` frontmatter, or run the strict scan on it and fix the hits |
| `hook`        | `git config --global core.hooksPath ~/.claude/hooks`, `chmod +x ~/.claude/hooks/commit-msg`, or reinstall python3 |
| `hook-log`    | Informational; a rejection rate above about 20% over a week means the commit skills are not pre-checking their messages |
| `skills`      | Open the named skill; the gate text or the `allowed-tools` entry was removed. Restore it from git history |
| `frontmatter` | Open the named file; usually an unquoted colon in a `description:` value |
| `tree`        | Run `~/.claude/library/scripts/slop-scan.py --strict` on the listed files and fix them, or raise `RESIDUAL_TOLERANCE` in `prose-health.py` if the new hits are clause-joining commas (the tolerance carries headroom above the audited count, so tripping it means several have accumulated) |
| `tests`       | Run `python3 -m pytest library/scripts/test_slop_scan.py library/scripts/test_prose_metrics.py library/scripts/test_commit_msg_hook.py` and read the failure |
| `index`       | `python3 ~/.claude/library/scripts/gen-skills-index.py` |
| `output`      | The system-prompt layer is not holding. Check `settings` and `style` first; if both pass and the rate stays above 3 per 1k words for a week, the next structural step is a `MessageDisplay` hook, which nothing here builds |

Never apply a fix in this skill; it reports. Offer the fix and stop.

## Red flags

**Never:** edit `RESIDUAL_TOLERANCE` to make `tree` pass without reading the hits; suppress a FAIL by editing the check; read the metrics as a verdict on one session (the window is seven days for a reason).

<raw-arguments value="$ARGUMENTS" />
