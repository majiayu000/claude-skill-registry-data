---
name: tool-requirements
description: CLI command reference for ESM/gradle Hub module development. Use when running build, test, validation, or scaffolding commands.
---

# Tool & Command Reference

Quick reference for the commands an agent runs against a target module. Everything below assumes the prerequisites in `@.claude/skills/prerequisites/SKILL.md` are in place.

## Module command surface

All module-level work happens through **one of two drivers**:

1. **`zbb`** — full lifecycle, test modes, gate, secrets, slots (run from the module dir)
2. **`yo @zerobias-org/module`** — initial scaffold only (run from repo root)

The only `npm` command run inside a module's directory is `npm` itself for things like `npm view` or `npm ls`. No more `npm run …` lifecycle scripts.

## Build lifecycle via zbb

zbb proxies every gradle task; run from the module directory (`cd package/<vendor>/[<suite>/]<service>` first):

```bash
# Full lifecycle: assembleSpec → bundleSpec → generate → compile → lint → test → buildImage → buildArtifacts
zbb build

# Individual tasks
zbb syncMeta                    # sync package.json metadata into api.yml info block
zbb assembleSpec                # build full.yml from api.yml + connectionProfile/State
zbb bundleSpec                  # inline all $refs into a self-contained spec
zbb generate                    # codegen → generated/api, generated/model, hub-sdk/generated/
zbb compile                     # tsc → dist/
zbb lint                        # eslint via @zerobias-org/eslint-config
zbb test --slot local           # in-process tests (unit + integration)
zbb testDirect --slot local     # e2e direct (in-process, live API)
zbb testDocker --slot local     # e2e docker (container, wire protocol)
zbb buildImage                  # Docker image (requires Docker)
zbb gate --slot local           # full CI gate — writes gate-stamp.json
zbb gateCheck                   # validate existing gate-stamp.json (cheap, no rebuild)

# Useful diagnostics
zbb tasks                       # list available tasks for this project
zbb dependencies                # dependency tree
zbb clean                       # wipe build outputs
```

**Always** run zbb from the module directory. zbb resolves the matching gradle subproject automatically.

## zbb test modes (run from the module directory)

```bash
cd package/<vendor>/[<suite>/]<service>

zbb test       --slot local   # unit tests (test/unit/) — fastest
zbb testDirect --slot local   # e2e direct: <Class>Impl in-process — proves the impl works
zbb testDocker --slot local   # e2e docker: <Class>Client → containerized impl — proves packaging works
# zbb testHub  --slot local   # e2e full stack — currently blocked, skip
```

Each mode runs the **same `test/e2e/<name>.test.ts`** via `describeModule<T>` — that's the whole point of the layout. Only the impl behind `client` differs.

```bash
zbb gate       --slot local   # full preflight: validate + generate + test + testDirect + testDocker + buildImage
                              # writes gate-stamp.json (commit it)
zbb preflight  --slot local   # gate + publish readiness checks (signing, version, deps)
```

## zbb slot / secret / env

```bash
zbb slot create local                                  # one-time per slot
zbb slot list

# Provide credentials for e2e
zbb secret create <name> \
  --module @zerobias-org/module-<vendor>-[<suite>-]<service> \
  --slot local                                         # interactive — pasted credentials never hit disk in plaintext

# Env vars for testDirect / testDocker (defaults declared in test/e2e/constants.ts)
zbb env set GITHUB_ORG zerobias-com --slot local
zbb env get GITHUB_ORG --slot local
zbb env list --slot local
```

## Scaffold a new module

```bash
# From repo root (package.json.name must end with /module)
yo @zerobias-org/module \
  --productPackage '@zerobias-org/product-<vendor>-[<suite>-]<service>' \
  --modulePackage  '@zerobias-org/module-<vendor>-[<suite>-]<service>' \
  --packageVersion '0.0.0' \
  --description    '<Display name>' \
  --repository     "$(git config remote.origin.url)" \
  --author         "$(git config user.email)" \
  --moduleType     'connector'   # or 'plain'

# Generator runs `zbb build` automatically.
# Pass --no-install to skip the build, --no-links to skip the .nvmrc/.npmrc symlinks.
```

Full invocation rules and verification in `@.claude/skills/scaffolding/SKILL.md`.

## Product discovery (read-only)

```bash
# Latest version of a product package
npm view @zerobias-org/product-<vendor>-[<suite>-]<service> version

# Read product metadata locally after install
cat node_modules/@zerobias-org/product-<vendor>-[<suite>-]<service>/index.yml | yq

# Discover the product bundle
npm view @zerobias-org/product-bundle --json | jq
```

## YAML / JSON helpers (used in agent validation scripts)

```bash
# Title/version of an api.yml
yq '.info.title, .info.version' api.yml

# Find all operationIds
yq '.paths.*.*.operationId' api.yml

# Schema names
yq '.components.schemas | keys' api.yml

# Spot wrapper schemas (response envelopes) — should be rare
yq '.paths.*.*.responses.*.content.*.schema | select(has("properties"))' api.yml

# Forbidden tokens in api.yml (these would block validate)
grep -E "nullable:|describe[A-Z]|'40[0-9]'|'50[0-9]'" api.yml   # should print nothing

# package.json shape
jq '.name, .version, .type, (.scripts // {})' package.json
```

## Static checks against module source

```bash
# No env vars in src (forbidden — credentials live in connectionProfile)
grep -rn "process.env" src/ && echo "✗ env access in src" || echo "✓ no env in src"

# No Promise<any> in src
grep -rn "Promise<any>" src/ && echo "✗ Promise<any>" || echo "✓ typed promises"

# All relative imports end in .js (ESM requirement)
grep -rnE "from '\.\.?\/[^']*'" src/ test/ | grep -v "\.js'" && echo "✗ missing .js extensions" || echo "✓ ESM imports OK"

# nock default-import (nock 14 / ESM)
grep -rn "import \* as nock" test/ && echo "✗ wildcard nock import" || echo "✓ nock import OK"

# No legacy scopes
# Verify the `zerobias` metadata block exists in package.json
jq -e '.zerobias' package.json >/dev/null && echo "✓ zerobias block present" || echo "✗ missing zerobias metadata block"
```

## Legacy → modern command translation

Old docs, PRs, in-conversation memory, and existing-module READMEs may reference commands that don't exist in this world. When you see one, translate it:

| Legacy command                          | Modern equivalent                                              |
|-----------------------------------------|----------------------------------------------------------------|
| `npm run sync-meta`                     | (no-op — gradle reads `package.json` directly)                 |
| `npm run generate`                      | `zbb generate`                                                 |
| `npm run transpile`                     | `zbb compile`                                                  |
| `npm run build`                         | `zbb build`                                                    |
| `npm run shrinkwrap`                    | (no-op — CI uses `npm ci` against `package-lock.json`)         |
| `npm run lint:src`                      | `zbb lint`                                                     |
| `npm run lint:api`                      | `zbb validate`                                                 |
| `npm run test`                          | `zbb test --slot local`                                        |
| `npm run test:integration`              | `zbb testDirect --slot local`                                  |
| `npx swagger-cli validate api.yml`      | `zbb validate`                                                 |
| `npx redocly bundle …`                  | `zbb generate`                                                 |
| `bash scripts/fixAllOfs/fixAllOfs.js …` | (no-op — gradle resolves $refs natively)                       |
| `bash scripts/link-hoisted-refs.sh`     | (no-op — no workspace hoisting)                                |

## Tool verification one-liner

```bash
node -v && npm -v && yo --version && zbb --version && docker info >/dev/null && echo OK
```

## Related

- @.claude/skills/prerequisites/SKILL.md — installing the tools above
- @.claude/skills/scaffolding/SKILL.md — generator invocation
- @.claude/skills/build-quality/SKILL.md — what `zbb build` and `zbb gate` actually verify
