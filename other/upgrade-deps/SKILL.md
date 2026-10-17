---
name: upgrade-deps
description: >
  Upgrade a Node repo's dependencies in three rounds (patch → minor → major)
  using npm-check-updates, respecting the project's release-age cooldown.
  Researches each update's changelog in parallel, bumps the uneventful ones
  silently, runs the tests, commits, and surfaces only the packages that need a
  human decision -- a few at a time, most severe first. Works in monorepos
  (--workspaces, syncpack). Use when the user runs /upgrade-deps, or asks to
  "upgrade deps", "bump dependencies", "update packages", or "run ncu".
---

# Upgrade deps

Get a repo's dependencies current with the least possible human attention.
The user's attention is the scarce resource: spend it only on packages that
genuinely need a decision. Everything that Just Works™ gets bumped, tested,
committed, and mentioned in a single line at the end.

The user can override the plan at any point ("skip majors today", "leave
`zod` alone", "just try them all"). Their instruction beats this document.

## Setup (once per run)

1. **Clean tree required.** If `git status --porcelain` shows changes, stop
   and ask. Never stash or discard anything.
2. **Package manager.** Detect from the lockfile (`pnpm-lock.yaml`,
   `yarn.lock`, `package-lock.json`, `bun.lock*`). Pass it to ncu as
   `-p <pm>`, and use it for installs.
3. **Monorepo?** If the root `package.json` has `workspaces`, or there's a
   `pnpm-workspace.yaml`, add `--workspaces` (root stays included by default).
   Bump a package to the same version everywhere it appears.
4. **Cooldown.** Only if the project configures one:
   - pnpm: `minimumReleaseAge` (minutes) in `pnpm-workspace.yaml` → `--cooldown <N>m`
   - yarn: `npmMinimalAgeGate` in `.yarnrc.yml` → convert to ncu's units
     (`d`/`h`/`m`)
   - npm/bun: check `.npmrc` / `bunfig.toml` for a release-age setting
   If none is configured, use no cooldown. If a setting exists but its unit is
   ambiguous, ask rather than guess.
5. **Verification command(s).** From the root `package.json` scripts (via
   `turbo run` if the repo uses turbo): `test` and `test:types`, whichever
   exist. No build, no lint. If the repo uses syncpack (dependency or config
   file present), add `syncpack lint` (or whatever syncpack script the repo
   defines).
6. **Baseline.** Run verification once before touching anything. Record
   pre-existing failures so they're never blamed on an upgrade. If the
   baseline is red, tell the user in one line and ask whether to proceed.

Keep a session-local **reject list**: packages the user decided not to
upgrade. Pass them as `--reject` to every later ncu call so they don't
resurface.

## A round

Rounds run in order: `-t patch`, then `-t minor`, then `-t latest` (majors).
Each round:

### 1. List

```
npx npm-check-updates -t <target> -p <pm> [--workspaces] [--cooldown X] [--reject a,b] --jsonUpgraded
```

Nothing to upgrade → say so in one line, move to the next round.

### 2. Research (parallel)

First grep the repo for each package's usage (imports, config files, CLI
invocations in scripts) so research is grounded in what *we* use.

Then spawn one subagent per package (general-purpose), all in a single
message. Each gets: package name, from → to, and our usage sites. Each must:

- Read the changelog for every version in the range: GitHub releases
  (`gh release view`), `CHANGELOG.md` in the repo (`npm view <pkg>
  repository.url`), or the npm page.
- Only if the changelog is vague or missing and our usage is non-trivial:
  inspect `npm diff --diff=<pkg>@<from> --diff=<pkg>@<to>`.
- Return exactly:
  - `verdict`: `trivial` or `attention`
  - `risk` (if attention), meaning how much harm it can do to the product if
    it's shipped or ignored:
    - `critical`: security fix we're exposed to, or possible data loss/corruption
    - `high`: silent behavior change in code we use, or breaks runtime code
    - `medium`: breaks tests/types/tooling (loud, so caught before it ships),
      or needs a decision
    - `low`: cosmetic, opt-in, or tooling-only consistency issues
  - `reason` (if attention): one line, citing our usage site if relevant

`trivial` = no change touches API surface we use, or only additive/fix
changes. Anything ambiguous about code we use is `attention`. Never pad a
trivial verdict with an explanation.

### 3. Bump the trivial ones

Upgrade all `trivial` packages together (`ncu -u --filter a,b,c ...`), install,
verify.

- **Green** → commit via `gcm --yolo "<round>-level dependency upgrades"`.
- **Red** → bisect: revert half the batch (restore `package.json` files +
  lockfile from `HEAD`, re-apply the other half, reinstall), verify, narrow
  down until the culprit(s) are isolated. Commit the green remainder.
  Culprits move to the attention list, with their risk re-assessed in light
  of what broke.

### 4. Report

Sort attention items by risk, then by how much of our code they touch.
Output, and nothing else:

```
Patch round: 3 need you.

| name        | from    | to      | reason                                                      | risk   |
|-------------|---------|---------|-------------------------------------------------------------|--------|
| zod         | 3.23.8  | 3.23.11 | `z.string().email()` regex tightened; we validate signup     | high   |
|             |         |         | emails with it (src/auth/schema.ts:14). Tests pass, but      |        |
|             |         |         | existing users with odd emails could fail re-validation      |        |
| vitest      | 2.1.3   | 2.1.5   | bumped → 4 tests in packages/core fail (fake timers)         | medium |
| @types/node | 22.7.4  | 22.7.9  | syncpack mismatch: apps/web pins 22.7.4 exactly              | low    |

Pick one (default: zod), or "all" to batch-try + bisect.

Upgraded patch-level: react, react-dom, tsup, prettier, eslint-plugin-react, typescript-eslint (+9 more)
```

Rules:

- **At most ~8 table rows** (half a terminal screen). If more items exist,
  the last row is `| …and msw, undici, hono (3 more) | | | next message | |`.
- Reasons are one line where possible; wrap only when the reason truly needs
  it. No mention of trivial packages beyond the final line.
- The final line lists everything committed this round. If it'd exceed one
  line, name the first few and `(+N more)`.
- Zero attention items → just the final line, then continue to the next
  round. (Still pause before majors if the user said so.)

### 5. Iterate

Work through items with the user, one at a time, their pick. Typical moves:

- They ask questions → answer tersely, from changelog/diff evidence.
- They say "try it" → bump, verify, report the result in a line or two.
- They say "all" → bump every attention item, verify, bisect on red,
  report only what broke.
- A fix on our side is needed → make it, verify, commit the upgrade + fix
  together via `gcm --yolo "<pkg> <from> → <to>"`.
- They decline → add to the reject list, move on.

**Formatter upgrades** (any formatter: prettier, biome, dprint, oxfmt,
prettier/biome plugins, …): never ask, always do
this as three separate commits:

1. the version bump
2. the reformat the new version causes in files that were already formatted
3. a reformat of files that already failed the format check before the bump

Skip any step that has no changes. Mention commits 2 and 3 in a line each
only if something in them deserves a look (e.g. a rewrap inside a code
block or formula). Otherwise they go on the final line like any other
upgrade.

Each green upgrade is committed as it lands. Pause only when something needs
the user. When the attention list is empty, the round is done → next round.

## Ground rules

- Never push. Never rewrite history. Commits only via `gcm --yolo`.
- Never leave the tree half-upgraded when pausing for the user: either
  committed or reverted to `HEAD`.
- Never claim a package is safe without having read its changelog (or diff).
  No changelog found and non-trivial usage → `attention`, reason "no changelog".
- Majors are almost never `trivial` unless our usage is clearly unaffected by
  every listed breaking change.
