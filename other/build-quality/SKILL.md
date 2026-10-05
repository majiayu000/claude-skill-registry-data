---
name: build-quality
description: What gradle's lifecycle actually verifies, and where each gate checkpoint sits inside it. Use when running a build, diagnosing failures, or scoping a checkpoint validation.
---

# Build & quality

The build is gradle, driven through `zbb` from the module directory. The driver is `zbb build` (or `zbb gate` for the full CI gate). Everything below is either part of that lifecycle or a cheap pre-check before invoking it.

## The full lifecycle

```
syncMeta
   ↓
assembleSpec         # merge api.yml + connectionProfile.yml + connectionState.yml → full.yml
   ↓
bundleSpec           # inline every $ref → self-contained spec
   ↓
dereferenceProductInfos
   ↓
generateApi          # → generated/api, generated/model
generateServerApi
generateServerEntry
buildHubSdk          # → hub-sdk/generated/
   ↓
copyDistributionSpec # module-<name>.yml into dist/
   ↓
compile              # tsc → dist/
compileServer
compileHubSdkExec    # tsc inside hub-sdk/ → hub-sdk/dist/
   ↓
lint                 # eslint via @zerobias-org/eslint-config
   ↓
test                 # mocha (unit + integration in-process)
   ↓
buildImage           # Docker image (if buildable)
   ↓
buildArtifacts (alias: build)
```

`zbb build` runs all of that. Failing at any step stops the rest. Each step's outputs are cacheable, so re-runs are cheap.

`zbb gate` adds e2e on top:

```
build
   ↓
testDirect
   ↓
testDocker
   ↓
gate-stamp.json      # written
```

`gate` is what produces the artifact CI validates. CI never runs the build itself.

## Where the six gates sit

The numbered gates from the workflow checklist map to specific points inside this lifecycle:

| Gate | Concept                | Verified by                                  |
|------|------------------------|----------------------------------------------|
| 1    | API spec               | `assembleSpec` + `bundleSpec` (succeed = spec is well-formed and all refs resolve) |
| 2    | Type generation        | `generate*` chain (succeed = TS types written to `generated/` + `hub-sdk/generated/`) |
| 3    | Implementation         | `compile` + `lint` (succeed = source compiles cleanly under strict TS + eslint) |
| 4    | Unit tests             | `test` filtered to `test/unit/**/*.test.ts` |
| 5    | Integration / e2e tests | `testDirect` (+ `testDocker` for connectors); `test` covers in-process integration |
| 6    | Build                  | `buildImage` + `buildArtifacts`; final stamp via `gate` |

Each gate's skill file (`gate-api-spec`, `gate-type-generation`, etc.) describes its specific checklist; this file describes the lifecycle they live inside.

## Cheap pre-checks

Before invoking the full `zbb build` you can run cheaper checks. Useful when iterating quickly:

```bash
# Just regenerate types after a spec edit
zbb generate

# Just compile after a source edit
zbb compile

# Just run unit tests
zbb test --slot local

# Validate an existing gate-stamp.json without rebuilding
zbb gateCheck
```

`zbb gateCheck` is the cheap "is the committed stamp still valid?" check. CI uses it. Locally, run it before pushing to confirm nothing has drifted since you last ran `zbb gate`.

## What artifacts exist on disk after `zbb build`

| Path                                  | Purpose                                      | Tracked? |
|---------------------------------------|----------------------------------------------|----------|
| `dist/src/`                           | Compiled module JS + `.d.ts`                 | No       |
| `dist/test/`                          | Compiled tests                               | No       |
| `dist/module-<name>.yml`              | Bundled spec for publishing                  | No       |
| `generated/api/`                      | Generated API interfaces + `manifest.json`   | No (except `manifest.json` is in `files`) |
| `generated/model/`                    | Generated model types                        | No       |
| `hub-sdk/generated/`                  | Typed client source                          | No       |
| `hub-sdk/dist/`                       | Compiled hub-sdk                             | No       |
| `gate-stamp.json`                     | CI signal; commit this                       | **Yes**  |
| `build/`                              | Gradle internals                             | No       |

The committed `gate-stamp.json` is the only build artifact that lives in git. Everything else is reproducible.

## When the build fails

The failing task tells you which gate broke:

- `assembleSpec` / `bundleSpec` — Gate 1 (API spec). Check unresolved `$refs`, malformed YAML, missing dependencies in `node_modules/`.
- `generate*` — Gate 2 (type generation). Spec parses but codegen rejects it. Read the codegen error; the fix is in the spec, not in `generated/`.
- `compile` / `compileHubSdkExec` — Gate 3 (implementation). TypeScript errors. Fix `src/` (or the consumer code if the type shape changed). Never edit `generated/`.
- `lint` — Gate 3 still. ESLint violations. Auto-fix where possible; otherwise update the source to satisfy the rule.
- `test` — Gate 4 (unit) or part of Gate 5 (in-process integration). Look at the mocha output.
- `testDirect` / `testDocker` — Gate 5 (e2e). Iterate with `zbb test*` directly.
- `buildImage` — Gate 6. Docker daemon is off, base image pull failed, or `installServerDeps` rejected a dep. Surface the Docker output.
- `gate` — Gate 6 final. Re-runs everything; usually fails the same way `build` does, with extra e2e on top.

For each failure, the working directory's `build/` folder has a detailed log. Don't paste the log into the spec or source as a comment; read it, fix the upstream cause.

## Cleaning state

```bash
zbb clean                   # wipes dist/, generated/, build/ for this project
```

After `zbb clean`, the next `zbb build` is from cold. Useful when you suspect cached state is hiding a real failure (e.g. a `$ref` you removed is still resolving from a cached `full.yml`).

## Quality bar at each checkpoint

- TypeScript compiles under `strict: true` with the canonical `tsconfig.json`. No `// @ts-ignore` without a referenced bug.
- ESLint passes. Disables (`// eslint-disable-next-line …`) carry a comment with the reason.
- Spec is round-trip clean: `bundleSpec` produces a self-contained YAML; the bundled spec is the artifact published in the npm tarball.
- No `Promise<any>` in `src/`. No `process.env` in `src/`.
- `gate-stamp.json` matches the working tree. If you've edited a file that's part of the stamp inputs and not re-run `zbb gate`, `zbb gateCheck` exits non-zero.

## Related

- @.claude/skills/api-regeneration/SKILL.md — regenerating after spec edits
- @.claude/skills/tool-requirements/SKILL.md — full zbb command surface
- @.claude/skills/gate-api-spec/SKILL.md — Gate 1 checklist
- @.claude/skills/gate-type-generation/SKILL.md — Gate 2 checklist
- @.claude/skills/gate-implementation/SKILL.md — Gate 3 checklist
- @.claude/skills/gate-unit-tests/SKILL.md — Gate 4 checklist
- @.claude/skills/gate-integration-tests/SKILL.md — Gate 5 checklist
- @.claude/skills/gate-build/SKILL.md — Gate 6 checklist
