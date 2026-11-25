---
name: dependency-update
description: Checks after `pnpm update`, `josh latest`, `josh adopt`, `pnpm josh overrides` or any dependency update — `overrides` kept, one expected `devEngines` change. Read it before reporting the pins or pinning a bump back.
---

# After a dependency-update command

`CLAUDE.md` → "Decision autonomy" keeps both prohibitions resident as Tier C: never touch `overrides`,
never touch `devEngines`, without explicit user approval. This skill is the single source of how to check
whether a command touched them, after `pnpm update`, `josh latest`, `josh adopt` (which runs
`josh latest`), `pnpm josh overrides`, a Dependabot merge, or any command that rewrites dependency
versions. Overrides exist on purpose (e.g. `"esbuild@<=0.24.2": ">=0.25.0"` for Workers builds).

## 1. Effective overrides live in the workspace — inspect both files

**pnpm 11 and 12 read effective overrides only from `pnpm-workspace.yaml`.** `pnpm.overrides` in
**`package.json` is ignored** (verified with pnpm 12.6.0). Inspect both to preserve existing
declarations, but an absent package field says nothing about workspace overrides.

## 2. Quote the printed overrides verdict

`josh latest`, `josh adopt` and `josh latest:if-required` print it after §3's line and a
`✖ <file> overrides changed` heading per moved block. `overrides: keep` — keep. `overrides: restore (…)`
(non-zero exit) — restore the moved entries, investigate, report. `overrides: not judged (…)` — run
the check below.

**No verdict printed** (`pnpm update`, a Dependabot merge) — run `pnpm josh overrides --diff HEAD`
(`<default>...<branch>` once committed) and quote its `✔` / `✖` lines the same way.

It covers the overrides blocks only: confirm overridden packages' `devDependencies` still respect them.

## 3. `devEngines` — the one expected change

**Read the verdict line, never compare by eye.** `pnpm josh overrides` prints it first — against
`HEAD`, or the `--diff` range's base — and `josh latest` prints it after its pnpm bump
(`scripts/version/development-engines-verdict.ts`). Quote it:

- `devEngines: unchanged` / `devEngines: kept` — keep. `kept` is the lockstep pnpm bump (the version
  byte-identical to the `packageManager` pin, `+sha512…` suffix included) or `josh sync` moving
  `onFail` from `"error"` to `"download"`.
- `devEngines: restore (<reason>)` — restore + ask. Also restore when something other than
  `josh latest` / `josh sync` touched it.

## 4. When the bump breaks something — fix forward

Single source: `prompts/collaboration-workflow/principles.md` → "latest-first". Fix-forward never
authorizes a silent edit to a protected pin; sections 1–3 still apply.
