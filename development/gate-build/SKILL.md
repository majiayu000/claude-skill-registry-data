---
name: gate-build
description: Gate 6 — the module passes the full `zbb gate` and the resulting `gate-stamp.json` is committed. Use as the last step before opening a PR.
---

# Gate 6: Build & gate-stamp

After Gates 1–5 pass piecemeal, Gate 6 runs the full lifecycle from cold and stamps the result. The committed `gate-stamp.json` is what CI checks; without it, publish fails.

## What to run

```bash
cd package/<vendor>/[<suite>/]<service>

zbb gate --slot local
```

This drives the gradle `:gate` task under the hood, which has these direct dependencies (each runs once, in dependency order; the gradle daemon parallelizes where it can):

1. `:validate` (chains assembleSpec → bundleSpec)
2. `:lint` (eslint)
3. `:compile` (chains :generate → tsc)
4. `:test` (unit + in-process integration via mocha)
5. `:testDirect` (e2e in-process, live API)
6. `:testDocker` (e2e in container — `onlyIf` `buildImage` produced one; effectively skips for interface-only modules)
7. `:buildArtifacts` (chains :buildHubSdk + :buildOpenApiSdk + :buildImage)
8. Writes `gate-stamp.json` in the module directory

Note: `zbb build` is the alias for `:buildArtifacts` and does NOT depend on `:test` — `zbb gate` does. So `zbb build` alone gets you everything *up to and including artifact production* but not the test suite; for the full picture, use `zbb gate`.

## What to check

```bash
# 1. Gate succeeded
zbb gate --slot local
# Exit code must be 0.

# 2. gate-stamp.json exists and is recent
test -f gate-stamp.json || { echo "✗ gate-stamp.json missing"; exit 1; }
jq -r '.timestamp // .createdAt // empty' gate-stamp.json
# Should be recent (today).

# 3. gateCheck agrees with what's on disk
zbb gateCheck
# Exit code 0 = stamp matches current source.
# Exit code != 0 = source has been edited since the stamp was written; re-run zbb gate.

# 4. Build outputs exist and match what package.json publishes
test -d dist                                  || echo "✗ dist/ missing"
test -f dist/src/index.js                     || echo "✗ dist/src/index.js missing"
test -f dist/src/index.d.ts                   || echo "✗ dist/src/index.d.ts missing"
test -f generated/api/manifest.json           || echo "✗ generated/api/manifest.json missing"
ls dist/module-*.yml >/dev/null               || echo "✗ no bundled module-*.yml in dist/"

# 5. No npm-shrinkwrap.json (legacy artifact)
test -f npm-shrinkwrap.json \
  && { echo "✗ npm-shrinkwrap.json present — delete it; CI uses package-lock.json"; exit 1; }
test -f package-lock.json \
  || echo "warn: no package-lock.json — run npm install once to create it"

# 6. files[] in package.json matches what's actually on disk
for f in $(jq -r '.files[]' package.json); do
  [ -e "$f" ] || { glob_match=$(ls $f 2>/dev/null | head -1); [ -n "$glob_match" ] || echo "✗ package.json files entry '$f' has no match"; }
done

# 7. ESM marker present
[ "$(jq -r '.type' package.json)" = "module" ] \
  || { echo "✗ package.json missing \"type\": \"module\""; exit 1; }

# 8. zerobias metadata key present
jq -e '.zerobias.package // empty' package.json >/dev/null \
  || { echo "✗ package.json missing zerobias.package"; exit 1; }
```

## Pass criteria

- `zbb gate --slot local` exits 0
- `gate-stamp.json` exists in the module directory and is up to date with the current source (`zbb gateCheck` exits 0)
- `dist/src/index.js`, `dist/src/index.d.ts`, `generated/api/manifest.json`, `dist/module-<name>.yml` all present
- `package.json.type === "module"` and `.zerobias.package` is set
- No `npm-shrinkwrap.json`; `package-lock.json` exists
- For connectors: a Docker image was built (`buildImage` is part of `:gate`)

## What gets committed

Once `:gate` passes, stage and commit only files inside the module directory plus the stamp:

```
package/<vendor>/[<suite>/]<service>/
├── api.yml
├── connectionProfile.yml          # connector only
├── connectionState.yml            # only if you created one in Phase 3
├── build.gradle.kts
├── package.json
├── package-lock.json
├── tsconfig.json
├── .mocharc.json
├── .gitignore
├── README.md
├── hub-sdk/package.json
├── src/**
├── test/unit/**
├── test/e2e/**
└── gate-stamp.json                # the CI signal
```

Do **not** commit: `dist/`, `generated/`, `hub-sdk/generated/`, `hub-sdk/dist/`, `build/`, `node_modules/`, `module-*.yml` at module root (the published one lives in `dist/`).

## On failure

- **Gate failed at `:bundleSpec`** — go back to Gate 1
- **Gate failed at `:generate*`** — Gate 2
- **Gate failed at `:compile` / `:lint`** — Gate 3
- **Gate failed at `:test`** — Gate 4a + 5
- **Gate failed at `:testDirect` / `:testDocker`** — Gate 4b + 5
- **`buildImage` failed** — Docker daemon, base image pull, or one of `installServerDeps` rejected something. Surface the Docker log.
- **`zbb gateCheck` returns 1 after a successful `zbb gate`** — you edited a source file (or `api.yml`, etc.) after running `zbb gate`. Re-run `zbb gate`.

CI's failure message — `gate-stamp.json is missing or invalid — run zbb gate locally and commit the stamp before publishing` — almost always means: stamp not committed, or stamp committed and then a file was edited.

## Related

- @.claude/skills/build-quality/SKILL.md — full lifecycle diagram
- @.claude/skills/gate-test-execution/SKILL.md — Gate 5 (just before this)
- @.claude/skills/tool-requirements/SKILL.md — zbb command surface
- @.claude/skills/git-workflow/SKILL.md — what to stage / what to ignore
- @.claude/skills/production-readiness/SKILL.md — final cross-cutting checks
