---
name: dev-bump-zudo-deps
description: "Bump every `@takazudo/*` registry dependency in the current project to its newest version, resolving each by the channel it currently tracks. Use when: (1) User says '/dev-bump-zudo-deps', 'bump zudo deps', 'bump the @takazudo packages', 'update zfb', 'update zudo-doc', or 'update the takazudo toolchain to latest', (2) A new `@takazudo/*` prerelease or release has shipped and this project should adopt it, (3) Routine first-party dependency-update rounds. Resolution rule: a dep currently on the `next` prerelease line (`0.1.0-next.N`) → newest `next` release; a dep on the literal `latest` tag → `dist-tags.latest`; a plain stable semver → newest stable. Skips `workspace:`/`file:`/`link:` specs and leaves operator style (exact / `^` / `~`) and prerelease channel intact. Beyond the version math, the skill assesses upstream impact per bump (changelog slice + code diff between the pinned and target versions) and also syncs vendored/generated artifacts tracked in a ZUDO_DEPS_PINS.md file (e.g. a zudo-doc scaffold or copied template HTML/CSS with no package.json pin). A bundled script does the discovery + semver resolution; this skill drives impact assessment + install + verify + report."
user-invocable: true
argument-hint: "[package-name... | all (default)] [--dry-run]"
---

# dev-bump-zudo-deps — Bump all `@takazudo/*` deps to latest

Discover every `@takazudo/*` dependency that resolves to the npm registry across **all**
`package.json` files in the project, bump each to the newest version on the channel it already
tracks, install, and verify the project still builds.

The fragile part — finding the deps, classifying each spec's channel, and computing the target
with correct prerelease semver — is done deterministically by **`scripts/resolve-bumps.mjs`**, so
it never depends on the model recomputing version math by hand.

## Resolution rule (what "bump" means per dep)

The dep's **current spec decides the channel**, and only deps pinned to a concrete version get
rewritten — specs that float are reported but left alone, because rewriting them would silently
turn a deliberate choice into a hard pin:

| Current spec                                   | Resolved to                            | Action     |
| ---------------------------------------------- | -------------------------------------- | ---------- |
| `0.1.0-next.58` (a `-next.*` prerelease pin)   | newest release on the `next` line      | ✏ `bump`   |
| `^1.2.0-beta.3` (any other prerelease line)    | newest release on that line            | ✏ `bump`   |
| `1.2.3` / `^1.2.3` / `~1.2.3` (stable semver)  | newest stable (`dist-tags.latest`)     | ✏ `bump`   |
| `next` / `latest` / `beta` (a dist-tag string) | reported (what the tag points at now)  | `tag`      |
| `*` / `x` / empty (floating)                   | —                                      | `skip`     |
| `workspace:` / `file:` / `link:` / git / url   | —                                      | `skip`     |

Write-back preserves what was there: an exact pin stays exact, `^`/`~` operators are kept, and a
prerelease-pinned dep stays on its own line. A dep declared via a **dist-tag string** (`next`,
`latest`, …) is intentionally **not** rewritten — it already floats to that tag on install, so the
script just reports what the tag currently resolves to (with a stale-tag/graduation note) and
leaves the pinning decision to you. Non-registry specs (`workspace:*`, `file:`, `link:`,
`portal:`, `catalog:`, `npm:` aliases, git/url) are left untouched — bumping a `workspace:*` dep
would break the monorepo.

### The one gotcha worth knowing: the `next` dist-tag can be stale

For prerelease lines, the npm `next` dist-tag sometimes points at an _older_ version than what's
actually published (or than `latest`). "Newest `next`" means the highest published `-next.*`
version, not whatever the `next` tag literally says. The script already resolves this by scanning
the full version list and flags two cases in its report:

- **stale tag** — `next` dist-tag < newest published `next` version (script uses the newest).
- **graduation** — `latest` is higher than the newest `next` (the line may have moved to stable); this is a human call, so surface it instead of silently switching channels.

## Step 1 — Resolve the plan (dry-run)

From the project root (running without `--write` is a dry-run):

```bash
node "$HOME/.claude/skills/dev-bump-zudo-deps/scripts/resolve-bumps.mjs"
```

**`--dry-run` is a top-level contract for the whole skill**: resolve + assess + report only — no
`package.json` writes, no installs, no vendored-artifact copies, no `ZUDO_DEPS_PINS.md` updates.

It prints one row per `@takazudo/*` dep — `bump` / `up-to-date` / `tag` / `skip` / `error` — with
current → target and any stale-tag/graduation notes, plus a `Scanned N package.json` line. Pass
exact package names to limit scope (`… resolve-bumps.mjs @takazudo/zfb @takazudo/zfb-runtime`);
`--json` adds a machine-readable plan.

- If every dep is `up-to-date` (or only `tag`/`skip` rows remain), skip to Step 7 — a project can still have vendored artifacts to sync even with zero registry bumps. Only after that check report "already on latest" and stop.
- An `error` row can mean the package is genuinely unpublished **or** a registry/auth/offline issue — if every lookup errored the script says so; confirm `npm view @takazudo/<pkg>` works from this shell before concluding a package is missing.
- `tag`/`skip` rows are deliberately not rewritten — surface them so the user can pin or update those manually if they want.
- The scan does not follow symlinks, so a symlinked nested workspace won't be found; sanity-check the `Scanned N` count against the project.
- The scan skips nested checkouts — any directory below the root that itself has a `.git` entry (dir, file, or symlink), such as a linked worktree or a vendored clone — so `--write` never touches another checkout's `package.json`.

Read the table before writing and **act on any flagged note** — a graduation warning means asking
the user whether to follow the line to stable rather than silently staying on the prerelease channel.

## Step 2 — Assess upstream changes (changelog + code diff)

For each `bump` row, find out **what actually changed upstream** between the pinned and target
versions before touching the consumer project. Full procedure:
[`references/upstream-impact.md`](references/upstream-impact.md). The short of it:

1. **Resolve the upstream repo** — `npm view <pkg> repository.url` (+ `repository.directory` for the monorepo package dir). Follow only first-party orgs (`Takazudo/*`, `zudolab/*`).
2. **Resolve both commits** — `npm view <pkg>@<ver> gitHead` for old and new, **verifying each hash exists in the repo** (`gh api repos/<o>/<r>/commits/<sha>`); fall back to matching git tags (`<pkg>@<ver>` changesets convention, `v<ver>`, `<ver>`). Unresolvable → changelog-only mode, stated in the report — never guess a commit.
3. **Read the changelog slice** first (package-dir `CHANGELOG.md` at the new ref, or GitHub releases) — highest signal, cheapest.
4. **Diff the published tarballs** — `npm diff --diff=<pkg>@<old> --diff=<pkg>@<new>` (name-only survey, then targeted files). This is the primary technical check: it is what consumers actually receive, and needs no repo/commit resolution at all.
5. **Repository diff only when source context is needed** — `gh api repos/<o>/<r>/compare/<old>...<new>` by default (no clone; watch the 300-file truncation cap and non-linear histories), blobless clone into the session scratchpad as the fallback. Scope to the package dir; look at the public surface: `exports`, `peerDependencies`, config schema/options, template markup and CSS classes.
6. **Write a per-package impact note** — breaking changes, renamed options, new required config, or "none found — plain bump". These notes drive the consumer-side edits and make any later verify failure diagnosable against a known diff.

For a ranged spec (`^`/`~`), "old" is the **lockfile's installed version**, not the spec's lower
bound — comparing from the manifest floor overstates the upgrade.

This step is timeboxed hints-gathering, not an audit — changelog + surface diff, then move on.
All of it is read-only recon: no edits, installs, or commits happen here, and never inside an
upstream clone.

## Step 3 — Apply the bumps

```bash
node "$HOME/.claude/skills/dev-bump-zudo-deps/scripts/resolve-bumps.mjs" --write
```

`--write` does a minimal in-place string edit per dep (it preserves each file's formatting). The
same package appearing in several `package.json` files is moved to the **same** target everywhere;
the script warns (`⚠ … multiple targets`) if anything would diverge.

## Step 4 — Check peer coupling

First-party families often pin each other. Before installing, confirm a bumped package's peers are
satisfied by the other targets — bump coupled packages together so the install resolves:

```bash
npm view <bumped-pkg>@<target> peerDependencies
```

If a peer requires a version the plan didn't reach (common with exact-pinned prerelease lines
where `^x-next.40` does NOT satisfy `next.41`), re-run Step 1/3 including that peer so the whole
family lands on a mutually compatible set.

## Step 5 — Install

Use the project's package manager (check `packageManager` in `package.json` / the lockfile —
`pnpm-lock.yaml` → pnpm, `package-lock.json` → npm, `yarn.lock` → yarn). Prefer a project-provided
safe-install script if one exists (e.g. `pnpm install:safe`).

```bash
pnpm install        # or: npm install / yarn install
```

**Independent nested workspaces install separately.** After `--write`, the script prints the
distinct directories it edited — install in each one that has its own lockfile (a nested workspace
with an independent lockfile is **not** covered by the root install), and commit every changed
lockfile:

```bash
pnpm install             # root workspace
cd doc && pnpm install   # any printed dir that has its own lockfile
```

## Step 6 — Verify

Run the project's checks and build to prove the bump didn't break anything. Use whatever the
project defines:

```bash
pnpm typecheck && pnpm build      # or: pnpm check, pnpm test, per the project's scripts
```

For a monorepo, build each workspace the bump touched, not just the root. Read the output — a
green typecheck/build is the bar. If a build breaks, the new version likely changed an API or a
peer; report the failure with the offending package rather than forcing the bump through.

## Step 7 — Sync vendored / generated artifacts (ZUDO_DEPS_PINS.md)

**Always check for `ZUDO_DEPS_PINS.md` at the project root — even when Step 1 found zero registry
deps.** Some projects consume a first-party package without any `package.json` pin: a doc site
generated by zudo-doc, template HTML/CSS copied and adapted from an upstream. Provenance for those
lives in `ZUDO_DEPS_PINS.md`; full format + workflow:
[`references/zudo-deps-pins.md`](references/zudo-deps-pins.md). The short of it:

- **File exists** → for each entry: resolve the upstream latest, diff `pinned..latest` scoped to the entry's `source:` paths (same mechanics as Step 2), and sync by the preferred strategy — regenerate, re-copy, or manual merge — **re-applying the local customizations listed in `notes:`** and re-diffing to confirm none were lost. Then update `pinned:`/`updated:` and commit the pins file **in the same commit as the synced artifacts**.
- **File missing, but this run touches vendored artifacts** → create it: one entry per upstream with best-effort provenance, using the honest-unknown convention (`pinned: unknown — recorded <date>, upstream HEAD was <hash>`) when the true origin is lost. Never state a guessed pin as fact.
- **File missing and nothing vendored** → skip; do not create an empty pins file.

## Step 8 — Report

Summarize for the user:

- **Bumped**: `pkg` old → new (note next-channel vs stable)
- **Upstream impact**: the Step 2 per-package notes — consumer-side edits made, or "none found"; call out any package where the code diff was skipped (changelog-only) and why
- **Up-to-date / skipped**: counts (and which were skipped as `workspace:`/non-registry)
- **Flags**: any stale-tag or graduation warnings from Step 1, and the decision taken
- **Vendored artifacts**: pins-file entries synced / already current / created (or "no ZUDO_DEPS_PINS.md, nothing vendored")
- **Verify result**: typecheck/build status per workspace
- **Lockfiles changed**: which ones (so they get committed)

Leave committing to the user / `/co` unless they asked otherwise.

## Step 9 — File upstream reports for anything the bump surfaced

The bump is the moment first-party problems show up — a stale/misleading dist-tag, a removed or
broken export, a regression in the new version, or a consumer-side fix that should have shipped as
a package change. File these on the **source repo** so they get fixed at the root instead of
worked around forever, via the `/dev-upstream-report` skill:

```
Skill tool: skill="dev-upstream-report"  args="<concise description + evidence>"
```

**Privacy guardrail — this skill runs in arbitrary repos, some of them private client work.** When
writing an upstream report (or any external artifact), describe the problem in terms of the
**public package** (name + version + a minimal repro), and:

- Name the source repo only when it is one of the first-party accounts — `Takazudo/*` or `zudolab/*` (e.g. `Takazudo/zudo-front-builder`, `zudolab/zudo-doc`). If the upstream is not one of those, do not assume a repo.
- **Never** include the consuming project's name, directory paths, internal URLs, or any client/company identifiers. A private client project must not be named or hinted at in a public issue. Strip paths down to the package-relevant minimum.
