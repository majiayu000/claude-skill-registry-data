---
name: definition-of-done
description: "The ordered finish-line runner for any change in this repo — generators, then the asset-integrity refresh last on its own, then the full gate suite, then commit and push; use before declaring any change finished or whenever the stop hook reports uncommitted or untracked changes."
allowed-tools: ["Bash", "Read", "Agent"]
---

# Definition of Done

## Doctrine

The order is load-bearing. The integrity manifest must hash the settled tree, so
`asset-integrity:write` always runs last, on its own, from the repo root — never folded into a
parallel generator batch, never run from a subdirectory.

## Trigger

- Before declaring any change in this repo finished.
- Whenever the stop hook reports uncommitted or untracked changes.

## Input

The list of paths you touched in this change.

## Decision matrix

Pick the steps that apply based on what changed — most changes trigger more than one row.

- **catalog / agents / skills / roles / providers changed** → `npm run manifest:write:all`,
  then re-run asset-integrity LAST on its own (the parallel-generator ordering caveat in
  `CLAUDE.md`).
- **`skills/**` changed** → `npm run manifest:write`.
- **`catalog/model-policy.json` or `model-registry.json` changed** → `npm run
  model-policy:check` (and `model-policy:apply` if the projection changed).
- **`tools/vfa-tui/**` changed** → `cd tools/vfa-tui && cargo fmt --check && cargo clippy
  --all-targets -- -D warnings && cargo test`. Return to the repo root afterwards — a
  persisted `cd` has broken integrity runs before.
- **any root file / `agents/` / `plugins/` / `package.json` changed** → asset-integrity
  refresh required.

## The invariant sequence

Always, in this order:

1. Applicable generators from the decision matrix above.
2. `python3 tests/validate-asset-integrity.py --write` from the REPO ROOT, last, on its own.
3. `npm run validate` — zero failures.
4. `npm run lint:spell` and `npx --yes markdownlint-cli2 "**/*.md" "#node_modules"` — zero
   failures.
5. `git status` clean after committing with a scoped conventional-commit message.
6. `git push -u origin <branch>` (retry with backoff on network errors only).

## Footguns

- `grep -cE 'FAIL|ERROR'` exits 1 on a count of 0 — do not chain it with `&&` before the
  commit, or a clean gate run looks like a failure and blocks you.
- Run integrity from the repo root — a leftover `cd` into `tools/vfa-tui` makes the write
  silently target a nonexistent path.
- Warnings from model-policy are exit-0 by design — read them, don't treat them as failures.
- Never edit `catalog/asset-integrity.json` by hand.

## Output

The checklist above with pass evidence per step, then the commit hash and push confirmation.

## Delegation note

Gate runs may be delegated to a Haiku subagent per `agentic-delegation`'s "Gate run" workflow
template, but the orchestrator reads the results and owns the commit — a delegate's self-report
that gates passed is not verification.
