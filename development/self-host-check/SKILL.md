---
name: self-host-check
description: Run a single test file under both native and self-hosted
  cx and compare outputs. Use when diagnosing a self-host-only
  regression — it's faster than the full 45-test suite and shows the
  divergence directly.
allowed-tools: Bash, Read, Write
---

# self-host-check

Diff a single test between the native and self-hosted paths. A
mismatch is the smoking gun for a cx.c bug.

## The two commands

    build/cx <file>              # native path
    build/cx cx.c <file>         # self-hosted path

Run both, capture stdout and exit code for each, and diff them.

## What to report

1. Native exit code and a few lines of output.
2. Self-host exit code and a few lines of output.
3. First divergence — the earliest line that differs, or the earliest
   assert that fails only in the self-host column.
4. A guess at which `.claude/rules/cx-constraints.md` pattern this
   looks like.

## Bisecting a self-host-only failure

Once you have a minimal failing file, shrink it:

- Delete functions until the failure disappears — the last removed
  function (or its dependency) is the culprit.
- Inside that function, comment statements. The smallest still-failing
  body is the reproducer you want.
- Cross-reference the cx-constraints rules — one of them almost
  certainly names the pattern you just hit.

Keep the shrunken reproducer in `tmp/` (gitignored) while you work.
Don't add it to `tests/` unless the fix lands alongside it.

## Don't

- Don't check in shrunk reproducers without a fix — they become
  confusing failing tests nobody understands later.
- Don't conclude "self-host is broken for this language feature"
  without having tried a minimal repro first. Almost every time it
  turns out to be one of the documented patterns.
