---
name: completion-checklist
description: Positive checklist for finishing a /create-module or /add-operation task. Use right before declaring done or opening a PR.
---

# Completion checklist

A task is done when every box below is checked. This is the positive form of `@.claude/skills/failure-conditions/SKILL.md`.

## Spec & codegen

- [ ] `api.yml` design final, follows the 12 critical rules
- [ ] `connectionProfile.yml` final (connector modules only)
- [ ] `connectionState.yml` final if the module tracks token expiry (optional otherwise)
- [ ] `zbb bundleSpec` exits 0
- [ ] `zbb generate` exits 0
- [ ] `generated/api/manifest.json` reflects every operationId
- [ ] `hub-sdk/generated/api/index.ts` is populated
- [ ] No `Inline*Response` / `Inline*RequestBody` types anywhere in `generated/`

## Implementation

- [ ] `<Class>Impl` implements the generated `<Class>Connector` interface
- [ ] Connector lifecycle methods present and async: `connect`, `disconnect`, `isConnected`, `metadata`, `isSupported`
- [ ] One `<Tag>ProducerImpl` per tag in `api.yml`
- [ ] Mappers in `src/mappers/` (or `src/Mappers.ts`) use `map()` from `@zerobias-org/util-hub-module-utils`
- [ ] `src/index.ts` re-exports `generated/api/index.js` + `generated/model/index.js` and exports `new<Class>()`
- [ ] All relative imports end in `.js`
- [ ] No `Promise<any>`, no `process.env` in `src/`
- [ ] `zbb compile` exits 0
- [ ] `zbb lint` exits 0

## Tests

- [ ] `test/unit/ConnectionTest.test.ts` covers all lifecycle methods (connectors)
- [ ] `test/unit/<Tag>ProducerTest.test.ts` per producer, with happy + error paths
- [ ] Unit tests use `import nock from 'nock'` (default import) and `nock.cleanAll()` in `afterEach`
- [ ] `test/e2e/constants.ts` declares env-backed constants with sensible defaults
- [ ] `test/e2e/<name>.test.ts` uses `describeModule<T>` with `CoreError.deserialize` as the 3rd arg
- [ ] Module type imported as `type` from `../../hub-sdk/generated/api/index.js`
- [ ] No `dotenv`, no `test/integration/`, no nock in `test/e2e/`
- [ ] `zbb test --slot local` exits 0 (unit)
- [ ] `zbb testDirect --slot local` exits 0 (e2e direct)
- [ ] `zbb testDocker --slot local` exits 0 (e2e docker, connectors only)
- [ ] Mapper runtime validation pass green — zero missing fields per `@.claude/skills/mapper-runtime/SKILL.md`

## Build & gate

- [ ] `zbb gate --slot local` exits 0
- [ ] `gate-stamp.json` present in the module dir
- [ ] `zbb gateCheck` exits 0 (stamp matches current source)
- [ ] `dist/src/index.js`, `dist/src/index.d.ts`, `dist/module-<name>.yml`, `generated/api/manifest.json` all present
- [ ] No `npm-shrinkwrap.json` in the module dir
- [ ] `package-lock.json` present
- [ ] `package.json.type === "module"`
- [ ] `package.json.zerobias.package` set
- [ ] For connectors: Docker image built (part of `zbb gate`)

## Docs

- [ ] `README.md` documents how to connect (credential acquisition) and at least one operation
- [ ] Any non-obvious decisions (e.g. why a custom `connectionState.yml`) explained in the PR description, not in code comments

## Repo scope

- [ ] Only files inside `package/<vendor>/[<suite>/]<service>/` (plus that path's `gate-stamp.json`) were modified
- [ ] No sibling-module files touched
- [ ] Branch is a feature branch (not `main`)
- [ ] Commit message follows conventional commits
- [ ] PR description summarizes what's in the module + how to test

## Completion signal

When all boxes check, the right summary is one or two lines:

> Gates 1–6 green. `gate-stamp.json` written and staged. Ready to commit.

## Validation script

```bash
#!/usr/bin/env bash
set -u
cd "$1" || exit 1   # pass the module dir as first arg
fail=0
note=$(printf '\033[33m')
err=$(printf '\033[31m')
ok=$(printf '\033[32m')
rst=$(printf '\033[0m')

# Spec
grep -E "describe[A-Z]|nullable:|'40[0-9]'|'50[0-9]'" api.yml \
  && { echo "${err}✗ forbidden tokens in api.yml${rst}"; fail=1; }

# package.json shape
[ "$(jq -r .type package.json)" = "module" ] || { echo "${err}✗ package.json missing type=module${rst}"; fail=1; }
jq -e '.zerobias.package' package.json >/dev/null || { echo "${err}✗ package.json missing zerobias.package${rst}"; fail=1; }
[ -f npm-shrinkwrap.json ] && { echo "${err}✗ npm-shrinkwrap.json present${rst}"; fail=1; }

# src/
grep -rn "Promise<any>" src/ \
  && { echo "${err}✗ Promise<any> in src/${rst}"; fail=1; }
grep -rn "process\.env" src/ \
  && { echo "${err}✗ process.env in src/${rst}"; fail=1; }
grep -rnE "from '\.\.?\/[^']*'" src/ test/ | grep -v "\.js'" \
  && { echo "${err}✗ relative imports missing .js${rst}"; fail=1; }

# Tests
grep -rn "import \* as nock" test/unit/ \
  && { echo "${err}✗ wildcard nock import${rst}"; fail=1; }
grep -rnE "jest\.mock|from 'sinon'|fetch-mock|from 'msw'" test/ \
  && { echo "${err}✗ forbidden mock library${rst}"; fail=1; }
[ -d test/integration ] \
  && { echo "${err}✗ test/integration/ exists (use test/e2e/)${rst}"; fail=1; }
grep -rn "process\.env" test/e2e/ 2>/dev/null | grep -v "/constants.ts:" \
  && { echo "${err}✗ process.env outside constants.ts${rst}"; fail=1; }
grep -rn "from 'dotenv'" . --include='*.ts' --include='*.json' 2>/dev/null \
  && { echo "${err}✗ dotenv import${rst}"; fail=1; }

# Build outputs (require zbb gate to have been run)
[ -f gate-stamp.json ] || { echo "${err}✗ gate-stamp.json missing — run zbb gate --slot local${rst}"; fail=1; }
[ -f dist/src/index.js ] || { echo "${note}note: dist/ not present — run zbb gate first${rst}"; }
[ -f generated/api/manifest.json ] || { echo "${note}note: generated/ not present — run zbb generate first${rst}"; }

[ $fail -eq 0 ] && echo "${ok}✓ static checks pass${rst}"
exit $fail
```

## Related

- @.claude/skills/failure-conditions/SKILL.md — the negative form
- @.claude/skills/gate-build/SKILL.md — Gate 6 (last step)
- @.claude/skills/production-readiness/SKILL.md — extra checks before publishing
