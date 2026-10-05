---
name: scaffolding
description: Module scaffolding via the @zerobias-org/module Yeoman generator. The generator emits a fully ESM/gradle-ready module and auto-runs the gradle build. No `npm run sync-meta`, no `npm install`, no manual symlinks.
---

# Module Scaffolding

The generator is the single source of truth for what a fresh module looks like. This skill documents *how to invoke it* and *how to verify its output* — not what files it produces, since the generator owns that.

## Generator

- **Package:** `@zerobias-org/generator-module` (registered name `module`, invoked as `yo @zerobias-org/module`)
- **Source:** https://github.com/zerobias-org/util/tree/main/packages/generator-module (read-only reference for what's scaffolded)
- **Install:** `npm i -g @zerobias-org/generator-module@0.25.2`

## Preconditions

The generator will throw if any of these are missing:

1. CWD is a directory whose `package.json.name` ends with `/module` (the module repo root)
2. `gradlew` exists at that root (otherwise the auto-build step has nothing to run)
3. Docker Desktop is running (`docker info` must return 0) — gradle's `buildImage` task needs it. Use `--no-install` to skip the auto-build if scaffolding offline.
4. Node 22.21.x is active

## Invocation

The generator takes seven inputs. Two are essential and best-derived from product research; the rest should be pre-filled from repo context to keep prompts minimal.

```bash
yo @zerobias-org/module \
  --productPackage '@zerobias-org/product-<vendor>-[<suite>-]<service>' \
  --modulePackage  '@zerobias-org/module-<vendor>-[<suite>-]<service>' \
  --packageVersion '0.0.0' \
  --description    '<Display name>' \
  --repository     "$(git config remote.origin.url)" \
  --author         "$(git config user.email)" \
  --moduleType     'connector'   # or 'plain'
```

Argument rules:
- `productPackage` — **required**. Must be in `@zerobias-org/` and contain `/product-`. Comes from @product-specialist.
- `modulePackage` — **required**. Must be in `@zerobias-org/` (module packages never move scopes) and contain `/module-`. Derived from `productPackage` by replacing `product-` with `module-` and switching scope.
- `packageVersion` — always `0.0.0` for a new module. Gradle/zbb owns versioning afterwards.
- `description` — human-readable display name. Pull from the product package's `index.yml` (`displayName`) when available.
- `repository` — derive from `git config remote.origin.url` (always `git@github.com:zerobias-org/module.git` for this repo, but reading from git config keeps it future-proof).
- `author` — derive from `git config user.email`. Do **not** read from `~/.claude/CLAUDE.md` — the global file no longer carries an email line; it has a directory-scoped table.
- `moduleType` — `connector` if the API needs credentials, `plain` otherwise. `plain` skips `connectionProfile.yml`.

The generator derives the destination path from `modulePackage`:
- `@zerobias-org/module-github-github` → `package/github/github/`
- `@zerobias-org/module-amazon-aws-s3` → `package/amazon/aws/s3/`

It will throw if the destination directory already exists.

## What the generator does for you

Inside the destination it writes:
- `build.gradle.kts` — single `plugins { id("zb.typescript-connector") }` (or `zb.typescript` for plain)
- `package.json` — ESM (`"type": "module"`), only the `clean` script, pinned deps, `zerobias` metadata key
- `tsconfig.json` — NodeNext, target ES2022, includes `src/**/*`, `test/**/*`, `generated/**/*`
- `.mocharc.json` — `{ "extension": ["ts"], "node-option": ["import=tsx/esm"] }`
- `.gitignore` — covers `dist/`, `generated/`, `hub-sdk/generated/`, `hub-sdk/dist/`, `build/`, ephemeral artifacts
- `api.yml` — minimal OpenAPI 3.0.3 stub with empty `paths`, product `$ref`
- `connectionProfile.yml` — stub with a single `apiToken` property (connector only)
- `hub-sdk/package.json` — wired to consume `dist/api/index.js` (populated by gradle's `generate`)
- `src/<Class>Impl.ts` — TODO-stub implementing the generated connector interface
- `src/index.ts` — re-exports the impl + a `new<Class>()` factory + generated types
- `test/e2e/constants.ts` — placeholder for env-backed constants
- `test/e2e/<name>.test.ts` — `describeModule<T>` skeleton
- `test/unit/.gitkeep` — placeholder so the dir exists
- `README.md` — short doc explaining how to build/test via gradle + zbb

It then:
- Symlinks `.nvmrc` and `.npmrc` to the repo root using a hardcoded `../../../{filename}` target. This works for two-segment module paths (`package/<vendor>/<service>/`) but **not for three-segment paths** (`package/<vendor>/<suite>/<service>/`) — those need `../../../../{filename}` and the generator does not yet adapt. If you scaffold a suite-nested module, the symlinks will be broken and need to be re-created by hand: `cd package/<vendor>/<suite>/<service> && rm .nvmrc .npmrc && ln -s ../../../../.nvmrc . && ln -s ../../../../.npmrc .`
- Runs `zbb build` (the full lifecycle: validate → generate → compile → test → buildImage)

You can pass `--no-install` to skip the auto-build, or `--no-links` to skip the symlinks (e.g. when Docker isn't running and you only want the file emission to inspect).

## Files the generator deliberately does NOT scaffold

These are *design-phase decisions* and are added later only if needed:
- `connectionState.yml` — only for modules that track token expiry (OAuth refresh, session lifetime)
- `Dockerfile` — gradle's `buildImage` task builds the image without one
- `.env.example` / `test-profiles/` — credentials are managed via `zbb secret create`
- Sample mappers, producer files, fixtures — implementation phase owns these

## Post-generator verification

After the generator returns, verify these exist (and only these — anything else means the generator drifted):

```bash
cd package/<vendor>/[<suite>/]<service>

# Scaffolded files
test -f build.gradle.kts
test -f package.json
test -f tsconfig.json
test -f .mocharc.json
test -f .gitignore
test -f api.yml
test -f README.md
test -f hub-sdk/package.json
test -f src/index.ts
ls src/*Impl.ts >/dev/null
test -f test/e2e/constants.ts
ls test/e2e/*.test.ts >/dev/null
test -f test/unit/.gitkeep
test -L .nvmrc
test -L .npmrc

# Connector-only
test -f connectionProfile.yml   # if --moduleType=connector

# Auto-build output (skip if --no-install was used)
test -d dist
test -d generated
test -d hub-sdk/generated
test -f generated/api/manifest.json
```

If `package.json` doesn't have exactly these top-level keys, the template drifted:
`name, version, description, type, moduleId, main, scripts, repository, license, author, publishConfig, files, zerobias, overrides, dependencies, peerDependencies, devDependencies`. The only script must be `clean`.

## When the generator fails

- **"You must run this generator from the root of a package"** — CWD's `package.json.name` doesn't end with `/module`. `cd` to the module repo root.
- **"Docker is not running"** — start Docker Desktop or rerun with `--no-install`.
- **"No gradlew at … — run the generator from a repo with gradle infrastructure"** — wrong repo.
- **"Path … already exists, aborting"** — module already scaffolded; delete and retry, or use the existing module.
- **"Product package must be in the format '@<scope>/product-…'"** — fix the `--productPackage` arg.
- **"Module package must be in the format '@<scope>/module-…'"** — fix `--modulePackage`.
- Gradle build step fails — read the gradle output, fix, then `zbb build` manually from the module dir (don't re-scaffold).

## Memory output

Phase 2 (Scaffold) writes its result to:

`${PROJECT_ROOT}/.claude/.localmemory/create-module-{moduleId}/phase-02-scaffolding.json`

Required shape:

```json
{
  "phase": 2,
  "name": "Module Scaffolding",
  "status": "completed",
  "timestamp": "<ISO-8601>",
  "modulePath": "package/<vendor>/[<suite>/]<service>",
  "gradleProject": ":<vendor>:[<suite>:]<service>",
  "moduleId": "<vendor>-[<suite>-]<service>",
  "moduleType": "connector | plain",
  "yeomanCommand": "<exact command run>",
  "generator": {
    "name": "@zerobias-org/module",
    "version": "<from npm view>"
  },
  "preconditions": {
    "dockerRunning": true,
    "nodeVersion": "v22.21.0",
    "gradlewPresent": true
  },
  "verification": {
    "scaffoldFiles": "passed | failed",
    "symlinks": "passed | failed",
    "autoBuild": "passed | skipped | failed",
    "details": []
  },
  "notes": "Build validation completed by generator's install() step."
}
```

