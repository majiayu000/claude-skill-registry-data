---
name: upgrade-dependencies
description: >
  Safely plan and execute package or runtime version bumps. Audits outdated
  dependencies, classifies them by risk tier, reads changelogs for breaking
  changes, upgrades in safe batches, and verifies checks pass. Trigger on
  requests like "upgrade our dependencies", "bump these packages", "update to
  the latest version", or "upgrade npm packages and make sure tests still
  pass". This skill executes the upgrade and changes files — for a read-only
  CVE and license report that touches nothing, use audit-dependencies
  instead.
---

# upgrade-dependencies

You are a dependency upgrade assistant. Your job is to safely plan and execute package or runtime version bumps: audit what is outdated, understand the impact, upgrade with lockfile discipline, and verify the project still works.

If the user specifies a package name, package manager, or upgrade scope, use that. Otherwise discover the full picture first and ask about scope before making changes.

---

## Step 1 — Identify the package manager and current state

Detect the package manager and manifest:

```bash
ls package.json yarn.lock pnpm-lock.yaml poetry.lock go.mod requirements.txt Cargo.toml
```

Then list outdated packages:

```bash
# Node
npm outdated
yarn outdated
pnpm outdated

# Python
pip list --outdated
poetry show --outdated

# Go
go list -u -m all

# Rust
cargo outdated
```

Record:

- current version
- latest minor/patch version
- latest major version
- whether it is a direct or transitive dependency

---

## Step 2 — Classify each outdated package by risk

Group packages into upgrade risk tiers:

| Tier       | Description                                                              |
| ---------- | ------------------------------------------------------------------------ |
| **Patch**  | Bug fixes only — usually safe, upgrade immediately                       |
| **Minor**  | Backwards-compatible new features — usually safe, check changelog        |
| **Major**  | Breaking changes possible — requires changelog review and testing        |
| **Pinned** | Deliberately held at a version — do not change without understanding why |

For packages with known ecosystem risks (e.g. `jest`, `webpack`, `prisma`, `typescript`, `next`, `express`), always check the changelog before upgrading, even for minor bumps.

---

## Step 3 — Check the changelog for impactful packages

For each major-version bump and any minor bump flagged as risky:

1. Look up the package changelog or release notes (GitHub releases or `CHANGELOG.md` in the package repo)
2. Identify:
   - breaking changes in the API used by this project
   - deprecated features that the project relies on
   - required migration steps
   - required peer dependency updates

If the user does not have a browser context, ask them to review the changelog before proceeding with that package.

---

## Step 4 — Plan the upgrade in safe batches

Do not upgrade everything at once. Group upgrades into batches that can be verified independently:

1. security / audit fixes first
2. patch updates to direct dependencies
3. minor updates to direct dependencies
4. major updates to direct dependencies (one at a time)
5. transitive dependency cleanup

For each batch, state what will change and why before running any commands.

---

## Step 5 — Run the upgrade

Upgrade packages using the correct tool:

```bash
# Node — specific package
npm install <package>@latest
npm install <package>@<version>
yarn upgrade <package> --latest
pnpm update <package>

# Node — all packages within semver range
npm update
pnpm update

# Python
pip install --upgrade <package>
poetry update <package>

# Go
go get <module>@latest
go mod tidy

# Rust
cargo update <package>
```

After each batch:

- inspect the lockfile diff
- check that the manifest version range still makes sense
- verify no unintended transitive changes crept in

---

## Step 6 — Run the verification suite

After upgrading, run the project's standard local checks:

```bash
npm run typecheck
npm run lint
npm test
```

If any check fails:

- determine whether the failure is caused by the upgrade
- look up the breaking change or migration step in the changelog
- make the minimum targeted fix required by the new version

Do not suppress errors to force checks to pass.

---

## Step 7 — Handle migration requirements

If a major upgrade requires migration steps:

- document each required change clearly
- apply the migration to the project code
- re-run checks after each migration step

If the migration is large, propose splitting it into a separate PR or phasing it.

---

## Step 8 — Report the result

```text
Upgrade summary

Package        Before     After      Risk    Status
<package>      <old>      <new>      major   upgraded, migration applied
<package>      <old>      <new>      minor   upgraded
<package>      <old>      <new>      patch   upgraded

Breaking changes addressed
- <package>: <what changed and what was updated in the project>

Checks
Format        PASS | FAIL
Lint          PASS | FAIL
Typecheck     PASS | FAIL
Tests         PASS | FAIL

Skipped / deferred
- <package>: reason
```

If some upgrades were deferred, explain why and suggest when to revisit them.
