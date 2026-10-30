---
name: release
description: >-
  Prepare a named version: preflight, version consistency, build/package, smoke
  test, checksums and notes, and release readiness. Covers both our own projects
  (subtree publication) and external packages. Publishing, tagging and deploying
  need separate authorization. Explicit-only.
invocation: explicit-only
---

# Release

Loading this part is not publish authority. It prepares; the owner releases.

## Which path applies

| Target | Path |
|---|---|
| One of our projects (`projects/<name>/`) | the project's own publish procedure splits the folder by subtree into its own repository — `BOOT.md` §6 owns the rules |
| A package published to a registry (npm, PyPI, crates) | The project's own release script and registry flow |
| A deploy (Workers, Vercel, host) | The deploy part (`cloudflare-deploy`, `vercel-deploy`), not this one |

Name the path in the readiness report. A version number that is not in the request
is a question, not an assumption.

## Workflow

1. **Preflight** — working tree clean and on the intended branch, version numbers
   consistent across manifest, lockfile, changelog and any badge, changelog entry
   present, dependency lock untouched unless the change is the dependency itself.
2. **Build/package** — the project's locked commands only, no ad-hoc flags.
3. **Smoke test** — install or run the artifact the way a consumer would; the
   tests that pass in the repo do not prove the package starts.
4. **Checksums and notes** — hashes for artifacts, notes written for the reader.
5. **Readiness report** — version, path, artifacts, checks run, and the exact
   command the owner would run to publish. Then stop.

## Non-goals

- No tag, push, publish or deploy without separate authorization, one action each.
- No invented version numbers, no skipping the smoke test because tests are green,
  no secrets in notes or artifacts.
