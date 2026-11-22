---
name: registry-publish
description: Publish a package to a registry safely — prepare, check, dry-run, confirm, publish, then verify the published artifact actually installs and works. Use when shipping a new version of a package. npm first. No publish happens without the user's explicit written confirmation. Only invoke via the orcinus router.
license: MIT
user-invocable: false
---

# REGISTRY-PUBLISH — ship the package, and prove the shipped one works

Publishing is the one step in the lifecycle that cannot be undone cleanly. You cannot reliably unpublish: npm allows unpublishing only within 72 hours and only under restrictions, and a version number, once published, can never be reused. So all the safety lives before the publish, not after it. Release tooling does not do this step for you: release-please writes release notes and tags, it does not publish to a registry. This skill is the missing step.

## Rules

- No publish without the user's explicit written confirmation. A version bump is not a confirmation.
- Never publish from a dirty tree. Commit first, then publish from the commit.
- Never publish a version that already exists on the registry. Check first.
- The pack list is the contract: read it before publishing, not after. If it contains a test, a secret, or source that should not ship, stop.
- Verify the published artifact after publishing: install it in a clean directory and run it. A publish that nobody verified is a rumour.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Prepare

- Bump the version (semver: breaking change = major, new feature = minor, fix = patch). The version in `package.json` is the version that ships.
- Write the changelog entry for this version: what changed, in the user's words.
- `package.json` must declare: `name`, `version`, `license`, entry points (`main` and/or `exports`), and a `files` allowlist of exactly what ships (for example `["dist/src", "README.md", "LICENSE"]`). No `files` field means everything not ignored ships — including tests.
- No secrets in the package. Run `security-review` on the pack list.

### 2. Check

- The four commands are green (build, lint, typecheck, test).
- Pin the registry explicitly (`--registry https://registry.npmjs.org`, or the project's `.npmrc` — never rely on the ambient default), then check whether the exact version exists. Query the exact version, not the latest, or a different version's existence will mislead you. Capture the exit code AND stderr: the three empty-stdout cases are different.
  - `E404` (version not found) = free to publish.
  - `FETCH_ERROR` / timeout / `E401` / `E403` = INCOMPLETE, stop — the registry is unreachable or the credentials are wrong, and an empty answer proves nothing. Do not read it as "free to publish".
- Build the exact artifact once: `npm pack`. Record its sha256, install THAT tarball in a clean directory and smoke-test it (Step 6 verifies the published one the same way). Publish that exact artifact, never a second build.
- The git tree is clean and the version bump is committed.

### 3. Dry-run

```bash
npm pack --dry-run
```

Read the file list. It must contain exactly the built output, the README, the LICENSE, and `package.json` — and nothing else. No tests, no source, no `.env`, no config.

### 4. Human gate

Show the user the version, the changelog entry, the dry-run file list, and the tarball sha256 from Step 2. Publish only after their explicit written confirmation.

### 5. Publish

```bash
npm publish ./<name>-<version>.tgz
```

Publish the exact tarball built and smoke-tested in Step 2, never a fresh build. Use `--provenance` where the registry and CI support it, so the published artifact is tied to its build.

### 6. Verify after publish

In a clean directory, with nothing from the project in it:

```bash
npm install <name>@<version>
node -e "import('<name>/<entry>').then(m => console.log(m))"
```

Import the package's public entry points and run them against known inputs. The outputs must match the expected values. If they do not, the publish is broken — say so immediately, do not wait for a user to find it.

## Report

Return the report in this form:

- Name, version, changelog entry.
- The four commands and their results.
- The registry check (version does not exist yet) and its output.
- The dry-run file list, in full.
- Who confirmed the publish, and when.
- The publish command and its output.
- The post-publish verification: install output and the smoke-test results.

## Scope

npm first. Other registries (PyPI, Maven, crates.io) are out of scope for v1 — the checklist is the same shape, but the commands differ, and this skill does not guess them. This skill publishes a package; it does not cut the release (that is `finalize` with release-please) and it does not monitor the package afterwards (that is `monitoring-observability`).

## Sources

Written from scratch for ORCINUS. No ready skill was found for this in the 0–100 research: release-please explicitly does not publish to package registries, and no verified candidate for registry publishing was found. The npm commands used here are the registry's own documented commands, verified by running them in the eval.
