---
name: build-toolchain
description: Designs and maintains build tooling — bundlers (Vite, Webpack, Rollup, esbuild, Parcel, tsup), package managers (npm, pnpm, yarn, Pipenv, Poetry, uv), lockfile hygiene, pre-commit hooks, runtime pinning, build cache, module resolution, monorepo workspaces, reproducibility. Audits for non-deterministic builds, lockfile drift, mixed package managers, unpinned runtimes, broken caches, and hooks that mutate without staging. Use when adding a bundler, switching package managers, debugging slow or non-reproducible builds, configuring pre-commit, or laying out a monorepo. Triggers on "build", "bundler", "vite", "webpack", "rollup", "esbuild", "parcel", "tsup", "swc", "babel", "npm", "pnpm", "yarn", "pipenv", "poetry", "uv", "pip-tools", "lockfile", "pre-commit", "husky", "lefthook", "build cache", "slow build", "hmr", "tree shaking", "code splitting", "monorepo", "workspace", "turborepo", "nx", "reproducible build", ".nvmrc", ".python-version", "engines field", "build toolchain".
---

# Build / Toolchain Engineer

Owns the path from source on disk to a runnable artifact. Optimises for reproducibility first, feedback latency second, output size and runtime cost third.

## Investigation order

Apply to any build problem before changing the config.

1. **Reproduce.** Pin the exact command, working directory, lockfile state, runtime version, and OS. A build that "works on CI but not locally" is two builds; describe both.
2. **Measure.** Wall time per stage (resolve, compile, bundle, emit), cache hit ratio, peak memory, output size. Profilers: `--profile`, `--analyze`, `--metafile`, `--debug-resolve`, language-specific timers.
3. **Hypothesise.** Name the suspected cause in one sentence: stale cache, unhashed input, lockfile mismatch, dual transformer, plugin order, runtime drift.
4. **Verify.** Change one variable in isolation — wipe the cache, pin the runtime, regenerate the lockfile in a clean checkout, swap one plugin out. Re-measure.
5. **Apply.** Smallest config diff that proves the fix.
6. **Re-measure.** Cold build, warm rebuild, dev start, and output size all return to or beat baseline before closing.

Skipping step 2 is the most common error — build problems look obvious and almost always aren't.

## Mode router

Pick one per invocation. If ambiguous, ask.

| Mode | Use when | Output |
|------|----------|--------|
| **Design** | A new bundler, package manager, or monorepo layout is being introduced | Config spec (entry points, outputs, transformers, plugins, cache strategy, lockfile and runtime pinning) |
| **Audit** | Existing config needs review | Tiered findings (Blocker / High / Medium) with the rule each violates |
| **Diagnose** | Build is slow, flaky, non-deterministic, or producing the wrong output | Root cause traced through resolver → transformer → bundler → emitter |
| **Optimise** | Build works but is too slow or too large | Ranked changes by measured impact, smallest first |

## This project's build — a published dual-format library

Most of this skill is about building an *application*. `react-basics-ui` builds a
**package other people install**, which changes what "correct" means: the output
is a public contract, not a deploy artifact.

### Shape

`tsup.config.ts` exports an **array of two configs**:

| Config | Entry | Emits |
|---|---|---|
| JS | `src/index.ts` | `index.js` (ESM) · `index.cjs` · `index.d.ts` / `.d.cts` · sourcemaps |
| CSS | `src/global.css` | `index.css` (~293 KB, Tailwind + the token system) |

`package.json` publishes them via the `exports` map (`.` and `./styles.css`),
ships only `dist` via `files`, and marks
`sideEffects: ["**/*.css"]` so bundlers may tree-shake the JS but never drop the
stylesheet.

### Two gotchas that cost real time here

1. **The stylesheet needs its own config.** The declaration pass refuses a `.css` root file (`TS6054`), so a combined config fails the whole build. The CSS config also sets `clean: false`, or it wipes the JS build that ran before it.
2. **The entry key must be exactly `index`.** Naming it `'index.css'` produces `dist/index.css.css`, which the exports map does not point at — and nothing warns you.

### Externals — verify, don't assume

tsup externalises `dependencies` and `peerDependencies` by default, which is what
you want: bundling `react` would give consumers two Reacts. Confirm after any
build change:

```bash
grep -oE 'from ?"[^"./][^"]*"' dist/index.js | sort -u
```

Expect exactly: `clsx`, `react`, `react-dom`, `react/jsx-runtime`,
`react-icons/*`, `tailwind-merge`. Anything else appearing means a dependency got
inlined; anything *missing* means it got bundled. `dist/index.js` is ~540 KB of
this library's own components — that number should track component count, not
dependency count.

### After any build change, check all four

```bash
npm run build
ls dist/index.js dist/index.cjs dist/index.d.ts dist/index.css   # all four exist
grep -c 'import\.meta' dist/index.cjs                            # must be 0 — syntax error in CJS
```

The `import.meta` check matters: it is valid in ESM and fatal in CommonJS, so a
Vite-style idiom slipping into source breaks only the CJS consumers, and only at
their build time.

## Optimisation priority

In order. Never invert.

1. **Correctness.** The output matches source semantics. Tree-shaking must not drop side-effectful imports; minifiers must not rename across module boundaries; transforms must preserve `this`, decorators, and async semantics.
2. **Reproducibility.** Same inputs → same outputs, on any machine, any day.
3. **Cold build time.** First build from a clean checkout.
4. **Warm rebuild time.** Incremental build during development.
5. **Dev server start.** Time from `start` to first interactive request.
6. **Bundle size.** Compressed size of shipped artifacts.
7. **Memory footprint.** Peak RSS during build.

A faster build that emits subtly wrong output is a regression, not a win.

## Reproducibility

The default question: *can this exact artifact be rebuilt in six months from the committed state of the repo alone?*

### Inputs that must be pinned

- **Runtime.** Node, Python, Bun, Deno version, declared in a version file (`.nvmrc`, `.tool-versions`, `.python-version`, `engines` field) and enforced in CI.
- **Package manager.** Version pinned (`packageManager` field, `pipenv --python`, `poetry env use`). Mixing `npm install` with a `pnpm-lock.yaml` corrupts the lockfile silently.
- **Direct dependencies.** Exact versions in the manifest *and* a lockfile committed to VCS.
- **Transitive dependencies.** Resolved versions in the lockfile, with integrity hashes.
- **Native toolchain.** Compiler, linker, system libraries — declare in a base image or devcontainer when they affect output.

### Lockfile rules

- Always committed. A repo with `package.json` but no `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` has no reproducibility guarantee.
- Regenerated only by a manifest change. A lockfile churn in a PR that did not touch the manifest is a smell — investigate before merging.
- Frozen in CI. Use the install mode that fails on drift (`npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`, `pipenv install --deploy`, `poetry install --no-update`). Plain `install` mutates the lockfile and hides drift.
- One lockfile format per repo. Two installers writing to the same `node_modules` produces ghost dependencies.

### Determinism gotchas

| Source | Symptom | Fix |
|---|---|---|
| `Date.now()` baked into output | New hash on every build | Inject build date at runtime, not build time |
| Filesystem iteration order | Chunk hashes shuffle across machines | Sort glob results before consumption |
| Parallel emitter race | Source maps mis-aligned with chunks | Pin emitter concurrency or pin output filenames |
| Postinstall scripts touching the network | Build differs by region or DNS state | Vendor or remove the postinstall |
| Untracked env vars (`NODE_ENV`, `CI`, locale) | Output diverges by environment | Snapshot the env in the build manifest |

## Bundler configuration

### Entry, output, target

- **Entry**: enumerate explicitly. Glob entries hide which files ship.
- **Output**: content-hash filenames (`[name].[contenthash].js`) for cacheable assets; stable names only for the HTML or manifest that points at them.
- **Target**: pin to a concrete set of browsers, a Node version, or a runtime spec. `latest` is not a target.

### Transformer pipeline

Order matters and is rarely commutative.

1. Resolve (path → file)
2. Load (file → source string + maps)
3. Transform (source → source; runs N times)
4. Bundle (graph → chunks)
5. Optimise (minify, tree-shake, scope-hoist)
6. Emit (chunks → disk)

A common bug: two transformers claim the same extension and run in the wrong order. Symptoms — works in dev, breaks in prod, or vice versa. Make the order explicit in config.

### Tree shaking

- Requires ESM sources. CJS is opaque to the bundler.
- Requires `sideEffects: false` in `package.json` (or a precise array) for any package whose modules can be safely dropped when unused.
- Breaks silently on:
  - Re-export barrels that re-export everything (`export * from './x'`) without `sideEffects`.
  - Property access on namespace imports (`import * as X`).
  - Polyfills imported for side effect (must be listed in `sideEffects`).

### Code splitting

- **Route-level**: dynamic `import()` at the route boundary. Default for SPAs.
- **Vendor split**: separate chunk for stable third-party deps. Inverts cache invalidation pressure from application changes.
- **Shared chunks**: extract code referenced by ≥2 entries. Configure the minimum reuse threshold; the default is often too aggressive and produces dozens of tiny chunks.

A bundle with 200 chunks is not split — it is shrapnel. Measure HTTP/2 push, prefetch budget, and parse cost before adding splits.

### Source maps

- **Dev**: inline or `eval-cheap-module-source-map` equivalent — fast, accurate to original line.
- **Prod**: `source-map` (separate file), uploaded to the error tracker, not served to clients. A public source map leaks original source.

### Dev server vs prod build

These are two different programs sharing a config file. Verify both:

- Dev: HMR works, module graph is correct, no stale modules after edit.
- Prod: tree-shaking applied, minification correct, output runs in the target runtime.

A green dev server is not evidence that prod builds correctly.

## Build performance

### Cache layers

| Layer | Keyed by | Invalidates when | Storage |
|---|---|---|---|
| Resolver cache | (specifier, conditions, importer dir) | Manifest or directory listing changes | In-memory per process |
| Transform cache | (file content hash, transformer version, options) | File or transformer changes | Disk, per project |
| Bundle cache | (module graph, options) | Any input module changes | Disk or runner cache |
| Dependency cache | (lockfile hash) | Lockfile changes | Runner cache |

Cache invalidation must depend on every input that affects output. A cache keyed on the file path but not the file content is a correctness bug, not a speed feature.

### Parallelism

- Worker pools help CPU-bound transforms (TypeScript, Babel, Sass).
- They hurt I/O-bound steps; the bottleneck becomes disk, not CPU.
- Saturate at `cpu - 1` workers. Above that, contention with the main thread wastes time.
- Measure before parallelising — a 4× speedup that costs 16× memory is not always worth it.

### Incremental builds

Required signals from the watcher:

- File added, removed, content-changed, renamed.
- Directory rescans on case-insensitive filesystems (macOS) when case changes.

A watcher that misses a rename produces a build that disagrees with source until restart. Symptom: tests pass but production fails on the renamed file.

## Package managers

### Selection criteria

- Match the ecosystem. Node monorepos: `pnpm` or `yarn` with workspaces. Python projects with native deps: `uv` or `poetry`. Python apps with simple deps: `pipenv` or `pip-tools`.
- Pick one per repo. Mixed package managers produce shadow dependency graphs that pass tests and fail in prod.
- Pin its version. Without `packageManager` (Node) or `[tool.poetry] version` constraint (Python), the runner installs whatever floats — lockfile semantics differ across major versions.

### Install modes

| Intent | Command pattern | Effect |
|---|---|---|
| Add a dep | `add <pkg>` / `poetry add` / `pipenv install` | Mutates manifest and lockfile |
| Sync from lockfile (CI) | `ci` / `install --frozen-lockfile` / `install --deploy` / `install --no-update` | Fails on drift |
| Sync from lockfile (local) | Same as CI, or `install` if drift is allowed | Local convention |
| Upgrade | `update <pkg>` / `poetry update` | Recomputes lockfile within manifest constraints |

The CI install must always be the frozen mode. Plain install in CI silently regenerates the lockfile and ships drifted deps.

### Workspace layout

- Hoisting models differ: `npm`/`yarn` flatten by default; `pnpm` symlinks. Code that assumes a flat `node_modules` (raw path imports, native module probes) breaks under `pnpm`. Test on the chosen layout.
- A package depending on a sibling must declare it. Cross-package imports that work only because hoisting flattened them are accidents.
- `workspace:*` and `path:` specifiers preserve local development across versions; replace with concrete versions only at publish time.

## Pre-commit orchestration

A pre-commit hook is code that runs on every commit. Treat it as production code on a hot path.

### What belongs in pre-commit

- **Fast checks**: format, lint, trailing whitespace, secret scan.
- **Localised checks**: each hook reads only the staged files it was passed.
- **Idempotent fixers**: a second run on the same input is a no-op.

### What does not belong

- Full test suites — too slow; push to CI.
- Build steps — too slow and changes output the developer did not intend.
- Hooks that touch unstaged files — silently widens the commit's blast radius.
- Network calls — break offline commits; non-deterministic on flaky networks.

### Hook configuration discipline

- Pin every hook to a tagged release (`rev:` in `.pre-commit-config.yaml`, an SHA or version in `husky`/`lefthook` scripts). Floating refs mean two developers run different versions.
- Pin `language_version` for any hook with a compiled language (Python, Node). Otherwise a developer's system runtime decides what runs.
- Scope `files:` and `exclude:` per hook. A linter pointed at the entire repo runs N× as long as the staged set.
- Auto-fixers must re-stage their writes or fail loudly. A hook that fixes a file without staging produces a commit that does not match what was checked.

### Bypass policy

`--no-verify` is a tool, not a workflow. If developers bypass routinely, the hook is wrong, not the developers. Investigate before tightening.

### Current state in this repo — configured but inert

`husky` is installed and `package.json` runs `prepare: husky`, and a `lint-staged`
block is configured (`eslint --fix` + `prettier --write` on `*.{ts,tsx}`). But
**`.husky/pre-commit` does not exist**, so nothing invokes lint-staged and no hook
runs on commit. `.husky/` contains only husky's internal `_/` directory.

This is dead configuration, and it is the failure mode this section warns about in
reverse: not a hook that does too much, but config that reads as protection while
providing none. Either wire it:

```bash
echo 'npx lint-staged' > .husky/pre-commit && chmod +x .husky/pre-commit
```

…or drop `husky`, `lint-staged`, and the `prepare` script so the repo does not
claim a guarantee it has not got. Do not leave it as-is — a reader reasonably
assumes staged files are linted.

## Monorepo concerns

### Task graph

A monorepo build is a DAG of (package, task) nodes. The runner (`turborepo`, `nx`, `bazel`, `make`) walks the graph and caches per node.

- Declare task inputs precisely. Anything not declared is invisible to the cache and produces stale hits.
- Declare task outputs precisely. Anything not declared is not restored from cache and looks like a miss.
- One node per `(package, task)` pair. A task that depends on "the whole repo" defeats the cache.

### Affected detection

- `since=<ref>` filters to packages whose inputs changed against the ref.
- Reliable only if every package's input set is complete. A missing input (e.g., a shared `tsconfig`) makes affected detection silently under-build.

### Versioning

- **Fixed**: all packages share a version; one publishes, all publish. Simple, coarse.
- **Independent**: each package versions on its own changes. Requires a changeset workflow or commit-message convention.

Pick one per repo. Half-and-half produces tag collisions.

## Red flags

Treat as bugs unless justified in writing.

- `package.json` without a committed lockfile.
- `npm install` (not `npm ci`) in CI.
- Two lockfile formats in the same repo (`package-lock.json` and `pnpm-lock.yaml`).
- A lockfile diff in a PR that did not touch the manifest.
- `latest`, `*`, or a floating major (`^1`, `~1`) on a runtime, a build tool, or a compiler.
- Postinstall scripts that fetch from the network or write outside the package.
- Bundler config that imports application source — config evaluation now depends on app correctness.
- Tree-shaking enabled with no `sideEffects` declaration on internal packages.
- Source maps emitted to a public output directory in prod.
- Pre-commit hook pinned to `main` or no rev at all.
- Pre-commit hook that runs the test suite.
- A watch script that calls a different bundler than the build script.
- A cache key that excludes the transformer's own version.
- `engines` field absent from any published package.
- A monorepo task whose declared inputs do not include the files it reads.
- Two developers reporting different build outputs from the same commit.

## Decision flowchart — "the build is broken"

```
Build is failing or wrong
  │
  ├─ Fails to resolve a module?
  │    ├─ Check the resolver:    extensions, conditions, exports field, tsconfig paths
  │    ├─ Check the manager:     lockfile in sync? frozen install passing? package manager pinned?
  │    └─ Check the workspace:   sibling declared as a dep? hoisting model assumed?
  │
  ├─ Resolves but transforms wrong?
  │    ├─ Two transformers claiming the same extension?  Pin order, drop one.
  │    ├─ Stale transform cache?                         Wipe; re-measure.
  │    └─ Transformer version drift across machines?     Pin runtime + lockfile.
  │
  ├─ Builds locally, fails in CI?
  │    ├─ Different runtime?           Compare .nvmrc / .python-version vs CI image.
  │    ├─ Different install mode?      CI must be frozen; local often is not.
  │    ├─ Case-sensitive paths?        Linux CI on a case-sensitive FS catches what macOS misses.
  │    └─ Missing env var?             Snapshot the env that affects the build.
  │
  ├─ Builds, but output is wrong?
  │    ├─ Tree-shake dropped a side effect?  Declare in sideEffects.
  │    ├─ Minifier renamed across modules?   Disable mangling for boundary symbols.
  │    └─ Source map mis-aligned?            Pin emitter concurrency.
  │
  └─ Builds, but is too slow?
       ├─ Measure stages first.   Optimise the slowest, not the most visible.
       ├─ Cache hit ratio low?    Check the key; one wrong input invalidates everything.
       └─ Parallelism saturated?  More workers will hurt.
```
