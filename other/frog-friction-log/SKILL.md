---
name: frog-friction-log
description: Log friction with `frog` the moment you hit a workaround, confusing error, misleading docs, or a bug in a dependency — not just in this repo's own code. Use when you notice yourself working around something broken rather than fixing it directly.
---

# Frog Friction Log

Friction noticed and not recorded is lost the moment the session ends. Log it the moment you hit it, before finishing the task it interrupted.

## When it's friction

A missing env var producing a silent `"undefined"`, a flag that doesn't do what its help text says, a test runner ignoring a filter, a type that lies about what it accepts, docs contradicting behavior — anything you had to work around instead of just using.

Not friction: your own mistakes, or things you fixed cleanly with no workaround.

## Process

1. If this repo has no `.agents/friction-log/` yet, run `frog init` once before the first `frog log`.
2. Check it isn't already recorded: `frog list --state pending`.
3. Record it:
   ```
   frog log "<specific, searchable title>" --body "<what happened, what you expected, how to reproduce>" --severity <blocker|major|minor>
   ```
4. If the friction is in a dependency rather than this repo, target it instead of filing locally: `frog targets` to check it accepts reports, then `frog log ... --target <owner/repo or npm-package>`.
5. Keep working — don't let logging interrupt the fix. Publishing (`frog publish`) and repository automation setup are separate, deliberate steps a human decides on a per-repo basis, not something to do unprompted.
