---
name: doc-sync
description: |
  Rewrite stale sections of existing docs so they match the code. Edit-only:
  never creates, splits, moves or renames files. Manual-only; run it when asked
  to "sync the docs" or "fix doc drift".
compatibility: |
  Requires: git, ripgrep
disable-model-invocation: true
---

# doc-sync: make existing docs match the code

Sync means rewriting sections of files that already exist until they say what
the code does. Code wins; the order is in `AGENTS.md` ("Where truth lives").

## Find drift

Diff `origin/main...HEAD`; on `main`, diff from the last commit that touched the
doc. Note routes (`REGISTERED_PATHS`), shim `ACTIONS`, config keys, CLI flags,
exit codes, gate names and moved paths. Grep the docs for each changed name and
fix only the sections that mention it.

## Rules

- Edit in place. Never create, split, move or rename a file.
- Delete stale text. Do not label it "historical"; git history keeps it.
- One home per fact: fix the section that owns it and link to it from
  elsewhere instead of restating it.
- Never fan an edit out to mirrors. A stale copy elsewhere is a duplicate:
  replace it with a link, or name it in your report.
- Quote code and config values from `rg`, never from memory or a report. Grep it.
- Leave dependency version numbers to `dep-sync`.
- If `tests/invariant_guard.rs` has a `DOCS_BUDGET`, it is the tripwire. Make
  the edit fit by cutting words; adding a row or raising a cap is the
  operator's call.

## Verify and report

```bash
cargo test --test invariant_guard
```

Re-grep every name you wrote and check that every link you touched resolves.
Report each file and section you changed, and name the docs you did not check
instead of claiming everything is in sync.
