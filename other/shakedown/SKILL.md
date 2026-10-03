---
name: shakedown
description: Audit a script-calling skill for CWD-sensitive path-resolution bugs — bundled `.sh` scripts that run in the session that wrote them but come back "not found" in another session, repo, or install — then write a graded report with a proposed fix. Runs a read-only static path audit plus a live scenario matrix (foreign CWD, nested dirs, spaces-in-path, project vs user install, stripped exec bit). Use when the user says "test this skill", "shake out the path bugs", "why can't Claude find my skill's scripts", "the bash script isn't being located", "harden this skill before I ship it", "audit the skill's script paths", or points at a script-calling skill that behaves unreliably across sessions or installs.
---

# Shakedown

Shake the faults out of a script-calling skill. The signature failure this targets: a skill whose bundled `.sh` scripts run fine in the session that wrote them but come back **"No such file or directory"** in a *different* session. That is almost always a path that resolves against the **current working directory** or one **hardcoded install location** instead of the skill's own folder. Shakedown proves it, then proves the fix.

Two layers, both **read-only** against the target:
1. **Static audit** — grade every script path in the target's `SKILL.md`, check each bundled script's shebang / exec bit / self-location.
2. **Live harness** — copy the skill into throwaway installs and actually run its documented command from a matrix of conditions, recording found / exit / stderr per scenario.

## Read-only contract

- Never edit, stage, commit, or mutate the target skill or any of the user's repos.
- All live tests run in `mktemp` sandboxes that are deleted on exit.
- The **only** things written to the user's repo are the dated report under `SHAKEDOWN/` and the newest-first index entry in `SHAKEDOWN/INDEX.md` — and by default the report *proposes* a patch rather than applying it (see Defaults).

## Locate this skill, then call its scripts by absolute path

This skill practices what it checks. When it triggers, Claude Code provides this skill's directory — run the bundled scripts by that **absolute** path, never by a CWD-relative path. If the directory isn't obvious, discover it once — preferring the install roots, traversing symlinked installs (`find -L`), anchoring the project root to the repo top (not the CWD), and requiring a real match so an empty result can't collapse to `.` (`dirname ""` is `.` — the exact bug this skill hunts):

```bash
SK=""
# Search the user-install root, the project-level .claude/skills, and this skill's
# canonical in-repo home (skills/). `find -L` so a SYMLINKED install (the common
# case, e.g. ~/.claude/skills/shakedown -> .../skills/4-occasional/shakedown) is actually
# traversed — bare `find` will not descend a symlinked dir and the locator comes back empty.
for root in "$HOME/.claude/skills" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/skills"; do
  [ -d "$root" ] || continue
  hit=$(find -L "$root" -path '*shakedown/SKILL.md' 2>/dev/null | head -n1)
  [ -n "$hit" ] && { SK=$(dirname "$hit"); break; }
done
[ -n "$SK" ] || { echo "shakedown: skill dir not found — pass it by absolute path" >&2; exit 1; }
```

Then every call below is `bash "$SK/scripts/<name>.sh"`. The scripts self-locate internally (`SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`), so they source their own helpers correctly no matter where you invoke them from.

## The run

### 1 — Static audit
```bash
bash "$SK/scripts/audit.sh" --target <path-to-target-skill-dir>
```
Prints a header block (target, target git HEAD, host) and graded findings. Exit code: `0` clean · `1` warnings · `2` blockers. Lift its output straight into the report.

### 2 — Read the target and extract the invocation
Open the target's `SKILL.md` and find the command(s) it tells a user to run for its scripts — **verbatim**, exactly as written (e.g. `bash scripts/relay_init.sh`). If a script needs arguments to start, supply a minimal safe example. You need two strings:
- **as-documented**: the literal command from the SKILL.md (this is what reproduces the bug).
- **proposed**: the same command with the script path anchored, using `{SKILL}` as the install-dir token (e.g. `bash {SKILL}/scripts/relay_init.sh demo`).

### 3 — Live harness
```bash
bash "$SK/scripts/harness.sh" \
  --target <target-skill-dir> \
  --as-documented '<verbatim command>' \
  --proposed '<command using {SKILL}>'
```
Run A runs the documented command across: control (CWD = skill dir), foreign CWD, nested CWD, spaces-in-path, project-level install, user-level install, and stripped exec bit. Run B re-runs the anchored command to confirm it survives every condition. Exit `0` = no discovery bug; `1` = bug reproduced. (`--keep` retains the sandbox for debugging.)

### 4 — Write the central report
Write one file per run to **`SHAKEDOWN/<YYYY-MM-DD>/<target-name>-<HHMM>.md`** at the repo root (use `user_time_v0` / system time — don't guess). This is the copy-paste-free deliverable: everything the user needs, including the patch, lives in the file. Also prepend a one-line entry to `SHAKEDOWN/INDEX.md` (newest-first) so the folder stays scannable. Confirm on screen with the file path and the one-line verdict — don't re-dump the whole report into chat.

## Report format

Use this structure exactly:

```markdown
# [SHAKEDOWN] <target-name> — <YYYY-MM-DD HH:MM>

**Target:** <name> (<path>)
**Target HEAD:** <short hash — subject, or "not a git repo">
**Env:** <uname -srm · bash version>
**Verdict:** <[path bug reproduced] | [warnings only] | [clean]> — <one line>

## Static audit
<graded findings from audit.sh: invocation paths, then bundled-script hygiene>

## Live harness
<Run A table (as documented) and Run B table (proposed fix) from harness.sh>

## Proposed patch
<a ready-to-apply diff for the target SKILL.md / scripts — the anchored invocation
 and, if needed, the BASH_SOURCE self-location block. Show it as a fenced diff.>

## What I could not verify
<honest limits — see below>
```

## Verdict & honesty rules

- **Anchor the verdict to the worst load-bearing finding**, not an average. One reproduced `[path bug reproduced]` discovery failure makes the whole skill's verdict `[path bug reproduced]`, even if everything else passes.
- **Separate "found" from "ran clean."** A script that is located but then errors on a missing argument still *passed discovery* — say so. Don't let a runtime error masquerade as a path bug, or vice-versa. The harness already splits these (exit 127 / "No such file" = not found; other non-zero = found-but-errored).
- **A green Run A is not nothing, but it is not proof of universality** — it means the bug didn't reproduce under *these* scenarios. If sessions still report failures, capture the exact failing command + CWD and add it as a scenario.
- Always fill **What I could not verify**. At minimum: shakedown tests the *documented command under varied CWD/install conditions* — it does **not** instrument Claude Code's internal skill resolver, so it can't certify how the runtime itself locates a skill; it tests whether the command as written is CWD-robust. Note any script you couldn't exercise (needs secrets, network, interactive input) and any arguments you had to guess.

## The fix shakedown recommends

When a discovery failure reproduces, the fix is two independent moves — apply whichever the findings call for:

1. **Anchor the invocation** in SKILL.md so it resolves against the skill's own dir, not CWD (absolute path via the discovery snippet above). Fixes "the script file itself isn't found."
2. **Self-locate inside each script** so its own sibling/`source`/data references resolve against the script, not CWD:
   ```bash
   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   source "$SCRIPT_DIR/lib.sh"
   ```
   Fixes "the script is found but can't find *its* files." These are separate bugs — a skill can need one, the other, or both. The harness's Run B confirms move 1; the static audit flags the need for move 2.

## When NOT to shake down

Calibration matters as much as coverage — don't run the full harness where there's nothing to find:

- **No bundled scripts.** A skill that ships only a `SKILL.md` (pure prose/process) has no script paths to grade — there is nothing to shake out. Say so and stop.
- **A runtime logic bug, not a discovery bug.** If the script is *found* and then misbehaves (wrong output, bad argument handling, a real exception), that's a normal code review — shakedown proves *location*, not the correctness of the logic.
- **A one-off you run by absolute path in a single session.** Shakedown hardens *distributed* skills against *cross-session* path drift; a local scratch script you always invoke by full path has no drift to harden.

## Defaults (state them, and offer to flip)

- **Propose, don't patch.** The report contains the diff; shakedown does not edit the target. Matches a review-gate workflow. Offer: "want me to apply this on a throwaway branch instead?"
- **Per-repo folder.** `SHAKEDOWN/` lives at the target repo root (mirrors the relay bus), not one global folder across all projects. Offer to centralize if the user prefers.

State both at the end of the first run so the user can redirect.
