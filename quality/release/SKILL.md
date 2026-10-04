---
name: release
description: >-
    Cut a release of the plainworks monorepo with Changesets — verify pending changesets, run the
    full pre-release gates, version the affected packages, and publish the @plainworks/* packages to
    npm in dependency order. Use when preparing or publishing a plainworks release or checking
    release readiness.
---

# Releasing plainworks

plainworks is a bun-workspace monorepo of independently-versioned `@plainworks/*` packages published to **npm** under the `@plainworks` scope. Releases are **Changesets-driven**: each change carries a changeset (its release-note + semver-bump intent), and Changesets aggregates them into version bumps and a generated changelog. There is no hand-maintained CHANGELOG. Distribution is npm only.

## Alpha stage — pre-release line

plainworks is **pre-stable**, shipping on the `0.1.0-alpha.x` line (matching gokit/rskit's `v0.1.0-alpha.1`). New packages are born at `0.1.0-alpha.1` (the golden generator seeds this).

- **Pre mode is on.** `.changeset/pre.json` is committed with the `alpha` tag, so `changeset version` emits `0.1.0-alpha.N` and Changesets owns the counter. Never hand-edit `pre.json`.
- **The release line is guarded.** `bun run check-versions` (part of `verify`) runs `plainworks-release check-line`. It fails when pre mode is on and a package is off the `-alpha.N` line, or when pre mode is off while a version still carries a prerelease suffix — the case where the next bump would publish a stable version by accident.
- **Publish under the `alpha` dist-tag**, never `latest`, so `npm install @plainworks/<name>` does not pull a prerelease by default. The workflow refuses to publish a prerelease under `latest`.
- **Graduating to stable `0.1.0`** is a deliberate step: run `bun x changeset pre exit`, commit the `exit` state, and version as usual. The guard allows prerelease versions in `exit` mode, and the graduating `changeset version` removes `pre.json`. Publish that release under `latest`.

## Prerequisites

- Push access to `github.com/kbukum/plainworks`, and trusted publishing configured for the `@plainworks` npm scope (see Step 5).
- On `main`, clean working tree, `bun install` current.
- Access to run the `release.yml` workflow and approve the protected `release` environment.

## Step 1 — Confirm there is something to release

```bash
ls .changeset/*.md            # pending changesets (excluding README.md/config.json)
bun run changeset status      # what would be versioned, and at what bump
```

If there are no pending changesets, **refuse to release** — nothing to ship. Every merged change should have arrived with a changeset (the `create-pr` / `validate` gates require one); if one is missing, add it now with `bun run changeset` before versioning — written in the plain, benefit-first release-note voice (what a consumer gains, not internal mechanics; see the Documentation baseline in `copilot-instructions.md`).

## Step 2 — Full pre-release gate

A release is the one time to run the **complete** gates rather than the affected set:

```bash
bun run verify                # every Definition-of-Done gate, in order (`--list` shows them)
(cd packages/create-plainworks && bun run smoke)   # a fresh starter passes its own gates
```

The smoke packs every package the way it will publish, scaffolds a starter against those tarballs, and runs the starter's typecheck, build, boot, and e2e. A red smoke means a published package or the starter breaks outside the monorepo.

Also run the [`review`](../review/SKILL.md) project audit in a fresh agent before a release. Treat green gates as necessary but not sufficient. The packaging gate already lints each built tarball's `exports`/`types` resolution; still sanity-check the artifacts before publishing:

```bash
plainworks-release pack packages/<name>   # inspect the npm-shaped tarball
```

Confirm `packages/elements/shadcn.lock.json` records the same shadcn CLI version as the `shadcn` catalog pin in the root `package.json`. The lock stores the version that last ran `registry:update`, so a mismatch means atoms were not refreshed after a CLI bump — run [`update-atoms`](../update-atoms/SKILL.md) before releasing. Never edit the lock by hand.

Confirm each publishable package's `tsdown.config.ts` exports a typed build description for its public entries, and `bun run check-shape` is green so the derived `package.json` fields match it. Packages publish `dist` plus `src` (tests excluded) so source maps and declaration maps land on real TypeScript source.

## Step 3 — Version the packages

Let Changesets consume the pending changesets, bump the affected packages (and their internal dependents), and write the generated changelog entries:

```bash
bun run version:packages      # changeset version + release-line check + create-plainworks versions + lockfile
```

Review the diff: the version bumps (`-alpha.N` while in pre mode), the consumed `.changeset/*.md`, and the changelog additions. This is the release commit content. While in `0.x`, a breaking change bumps **minor**, otherwise **patch** — Changesets handles this from each changeset's declared bump.

## Step 4 — Land the version bump through a reviewed PR

`main` is protected — the version bump lands like any other change, on a branch, reviewed:

```bash
git switch -c kbukum/release-<date>
git add -A
git commit -m "chore(release): version packages"
git push -u origin kbukum/release-<date>
gh pr create --draft --base main --title "chore(release): version packages" --body-file <path>
```

Per repo workflow the maintainer reviews and merges. Do not push the bump directly to `main`.

## Step 5 — Publish and tag (after merge)

Publishing has **one path**: the [`release.yml`](../../workflows/release.yml) workflow. It publishes with npm **provenance** (a signed SLSA attestation linking each tarball to the exact CI build), which needs npm **trusted publishing (OIDC)** — an ambient CI identity, never a long-lived token. There is no local publish path, because a local publish cannot carry provenance.

What the workflow does, in order:

1. Runs only on `main`, in the protected `release` environment.
2. Runs `bun run verify`, so a commit that never passed CI cannot publish.
3. Checks the publish set with `plainworks-release publish-set --check`, then walks it in dependency order (lowest layer first), derived from the workspace graph.
4. Packs each package with `plainworks-release pack`, which resolves `catalog:` and `workspace:*` into concrete versions, applies `publishConfig`, and removes the repo-only source condition. `bun publish` cannot use OIDC or emit provenance yet ([oven-sh/bun#24855](https://github.com/oven-sh/bun/issues/24855)), and `npm publish` alone would ship the raw protocols.
5. Publishes each tarball with `npm publish <tarball> --provenance --tag <dist-tag>`, skipping versions already on npm, so a re-run is safe. It refuses to publish a prerelease under `latest`.

One-time setup (out of band): configure a **trusted publisher** for each `@plainworks/*` package and `create-plainworks` on npmjs.com, pointing at this repo's `release.yml`. The workflow requests `id-token: write` and installs npm ≥ 11.5.1.

After the version-bump PR merges, trigger the workflow from the Actions tab (`Run workflow`, `dist-tag` = `alpha` while in pre mode). When it succeeds, tag the release on merged `main` and push the tags:

```bash
git switch main && git pull --ff-only
bun x changeset git-tag       # per-package tags for the published versions
git push --follow-tags
```

Never publish anything `"private": true` (apps, `internal/*`); the publish set already excludes them. Then draft the GitHub Release from the generated changelog if desired.

## Guardrails

- **Never** run destructive git commands (`reset --hard`, `checkout -- .`, `clean`) on uncommitted work without explicit permission.
- **Never** publish from a dirty tree or an unbuilt `dist/`.
- Per repo workflow, the agent prepares the branch/version bump; **the maintainer merges the PR, tags, and triggers the publish** unless explicitly asked otherwise. Open a PR only when explicitly requested, in **draft**, following the PR template.
- All CI actions must be SHA-pinned; the `release.yml` publish workflow carries minimum permissions (`contents: read`, `id-token: write`) and uses OIDC trusted publishing rather than a stored token.
- Reference other-repo items with full URLs, never bare `#123`.
