---
name: fix-bug
description: >
  Fix a bug with a reproduce, root-cause, approve, fix, verify loop and a short write-up. Use when
  the user says "fix bug", "fix #N", "debug this", "this is broken", or picks up an issue labelled
  bug. Lighter than plan-feature: no interrogation, just a confirmed repro and proof the fix held.
argument-hint: "[issue number or description]"
---

# fix-bug

Read the project's `CLAUDE.md` **Skill settings** first: the tracker, the checks to run, where
notes go and what can only be verified on a device are there.

## 0. Size it

- **Mechanical** (stack trace or obviously wrong line): reproduce, fix, add a regression test,
  run checks, report. Skip steps 3–4's ceremony.
- **Everything else**: all steps.
- **Turns out to need design work** (new mechanism, data model change): stop and suggest
  `plan-feature`.

## 1. Load and guard

- Read the issue with comments. If it isn't a bug, say so.
- If you are on the default branch, create the issue branch using the project's naming rule
  before changing anything.

## 2. Reproduce

Read the code path first, then pick the first that works:

1. **Failing unit test** that shows the defect (preferred: it becomes the regression test).
2. **Browser / dev-server steps** you can run yourself.
3. **Device-only**: use the device route from Skill settings (logs, simulated input). If you
   can't run it, write exact steps for the user and wait for their result.

Can't reproduce and the report is vague? Ask for specifics instead of guessing. Also check the
default branch: `git log origin/<default> -- <paths>`. If it is already fixed there, say which
commit and stop.

## 3. Root cause

- 2–4 ranked, falsifiable hypotheses; test the cheapest first.
- Temporary logging gets a `[DEBUG-xxxx]` tag (random 4 hex) so cleanup is one grep.
- Write down the root cause in 2–4 sentences with `file:line`.

## 4. Propose and wait

Short message: what's wrong, why, and up to 3 fix options with trade-offs, recommended first.
Ask with `AskUserQuestion`. Don't edit shipping code before the user picks. If the diagnosis
shows it isn't a bug or is a duplicate, say so and ask whether to drop it.

## 5. Fix

- Implement the chosen option only. Minimal diff: no renames or clean-ups. Note anything you
  spot for later instead.
- New evidence that contradicts the diagnosis means going back to step 4, not quietly
  switching approach.
- Make sure there is a regression test that fails without the fix, where the bug allows one.

## 6. Verify

- Rerun the repro, then the project checks from Skill settings.
- `grep -rn "DEBUG-xxxx"` returns nothing.
- Visual, timing or device-only bugs: say plainly what you could not confirm and ask the user to
  check, with the exact steps.

## 7. Write-up and hand-off

Post this where Skill settings says (e.g. a comment on the issue), then open the PR the project's
way:

```markdown
**Problem:** <one line>
**Repro:** <test name or steps>
**Root cause:** <2–4 sentences, file:line>
**Fix:** <what changed and why this option>
**Verified:** <what ran and passed> · **Not verified:** <device/manual items, or "none">
**Follow-ups:** <optional>
```
