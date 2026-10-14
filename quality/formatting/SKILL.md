---
name: formatting
description: "Formatting: use repo formatter; no unrelated reformats in diffs."
---

# formatting

The repo's formatter is the law; diffs stay minimal.
## Inspection

Read the repo formatter config; check whether the diff contains unrelated reformats.

## Decision rules

Repo formatter always wins; format only touched files; config disputes resolved by config change, not per-file exceptions.


## Activate when

- Formatting code, adopting a formatter, or reviewing diffs with style noise.

## Do NOT activate for

- Lint findings that are defects (see linting, core/code-review).

## Procedure

1. Detect the repo formatter and config first (Prettier, Ruff format, gofmt, rustfmt, Standard); never introduce a competing formatter.
2. Format only files the change touches; no drive-by reformats of unrelated code.
3. Formatter disagreements are resolved by config change + team note, not per-file exceptions.
4. Verify: formatter check green, diff contains no unrelated hunks.

## Failure modes

Second formatter introduced alongside the first; drive-by reformats polluting diffs; formatting fights in review.

## Escalation

Real defects found while formatting → core/code-review or linting as appropriate.
