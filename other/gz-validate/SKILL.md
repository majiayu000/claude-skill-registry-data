---
name: gz-validate
description: Use to check manifest, ledger, document or surface validity against schema rules.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "0.2.1"
model: haiku
---

# gz validate

## Overview

Run gzkit's governance validators. Each `--<scope>` flag is one validator, and
`VALIDATOR_REGISTRY` in `src/gzkit/commands/validate_cmd.py` is the authority
for which scopes exist and their tier; `uv run gz validate --help` lists the
flags and `docs/user/manpages/validate.md` says what each checks.

- A bare `gz validate` runs every **default-tier** scope. This is the
  `Validate` step of `uv run gz check`.
- An **explicit-tier** scope runs only when its flag is named. `gz check`
  enrolls some of them as their own steps; the rest run on no commit path
  (GHI #1063), so a green `gz check` says nothing about them.
- Flags combine, except a **solo-only** scope, which refuses to run with any
  other scope (exit 1) and must be run alone (GHI #704).
- `--json` changes the rendering, never the exit status (GHI #995).
- In an open MX hangar (`gz mx`), ERROR-level scopes report without failing;
  CRITICAL-level scopes still fail. The run says so when it demotes one.

Exit codes: 0 clean; 3 when every finding is a policy breach; 1 when any
finding is an ordinary error, or on a refused combination. Each finding names
the artifact, the rule it breaks and the recovery.

## Workflow

1. Run the scope the question needs, `uv run gz validate --<scope>`, or bare
   `uv run gz validate` for the default tier. Capture output to a file and read
   `$?` straight after it: the verifier-pipe gate refuses a piped verifier or
   one followed by another statement (GHI #589).
2. For each finding, fix the named surface as its message directs, then re-run
   the same scope until it exits 0.
3. Report the scopes run, the exit code and each finding fixed or still open.

## Example

```bash
uv run gz validate
uv run gz validate --deprecated-verb-prescription
uv run gz validate --briefs --json
```
