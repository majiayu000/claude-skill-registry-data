---
name: skillcheck
description: Measure whether the user's Claude Code or Codex skills actually trigger in their real setup, next to all their other installed skills and plugins. Use when the user says a skill "doesn't fire", "isn't being used", "gets ignored", "the wrong skill runs", asks to test, audit or debug skill triggering or descriptions, wants to check a skill before publishing it, or is about to install a new skill and wants to know whether it will break or take over existing ones. Not for writing a new skill from scratch or for general code review.
---

# skillcheck

Runs prompts through the user's real `claude -p` / `codex exec` with everything installed, records which skill actually loaded, and compares before/after a description fix.

## Find the script

1. `../../skillcheck.py` relative to this skill's base directory (plugin install).
2. Otherwise download a pinned copy into a temp folder and run it from there:
   `curl -fsSL -o /tmp/skillcheck.py https://raw.githubusercontent.com/Noem836/skillcheck/v0.1.2/skillcheck.py`

Run it with `python3`. It needs only the standard library.

## Workflow

1. `python3 skillcheck.py scan`. These are static checks with no model calls. Fix any `error` lines first (missing frontmatter, name/folder mismatch, skill turned off by `skillOverrides`, nested SKILL.md).
2. `python3 skillcheck.py gen --skills <names> --out suite.json` drafts should-fire and near-miss prompts. Show the suite to the user and let them edit it. Their real phrasings beat generated ones.
3. `python3 skillcheck.py run --agent claude --suite suite.json --tag before --runs 3`. Each run takes about a minute, so tell the user the estimate (skills × prompts × runs) before starting, and run it in the background.
4. `python3 skillcheck.py report --tag before`. Read the "taken by" column: a miss is usually another skill winning, not a broken skill.
5. Edit the description (see below), run again with `--tag after`, then `compare --before before --after after`.
6. Optional: `html --tag before,after` for a local report, or `upload --tag before,after` for a share link (sends no prompt texts).

## Before installing a skill

`python3 skillcheck.py preflight <path to the downloaded skill or pack>` lists name clashes and the installed skills it most likely competes with. Add `--measure --runs 2` (and `--skills a,b` for the user's skills that matter most; word overlap misses narrow rivals) to run those skills' prompts with and without the new skill (installed only inside a temp folder). Report each skill's fire rate before → after, and "taken by the new skill". Tell the user the run estimate first (suspects × 3 prompts × runs × 2, about a minute each).

## Description fixes that worked in measurements

- Remove wording that reads as slash-only ("use as /name <topic>"). It stopped one skill from firing at all (0/4 → 4/4 after removal).
- List the user's literal trigger phrases ("explain simply", "can I conclude that …?") instead of abstract categories.
- When two skills compete, state the boundary in both descriptions ("single-field use-case lists go to X, not Y").
- Re-measure with prompts written before the edit, so the fix isn't just fitted to the test.

Runs are locked down (Claude: Skill tool only; Codex: no user config, MCP, web or plugins). Even so, don't run suites from untrusted sources without reading them first.
