---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: napi
description: >
  Build native Node.js addons in Rust with napi-rs. Covers the napi config,
  #[napi] attributes, ThreadsafeFunction callbacks, what `napi build` generates
  and which inputs control it, cross-compiling, the multi-platform publish
  pipeline, and the loader contract. ALWAYS load this skill when a repo has a
  build.rs calling napi_build::setup(), a "napi" key in package.json, a
  @napi-rs/cli dependency, or any .node binary. Load it before editing
  Cargo.toml, package.json, or CI for a native addon, and before debugging why
  a binding fails to load or why the published package is huge.
---

# napi-rs

Write a Node.js native addon in Rust. `#[napi]` attributes describe the
JavaScript surface, `napi build` compiles one target and emits the loader and
the types, and CI fans the binaries out into one npm package per platform.

## Read the docs first

Run this before writing any napi config, CI, or publish step. The CLI renamed
several commands between v2 and v3, and half the packaging behaviour is not
guessable.

```bash
npx napi --help          # read the FULL output, never pipe to head or tail
npx napi build --help    # per-command help is much richer than the top level
```

The full documentation is a separate repo. Fetch it once and grep it locally
instead of making dozens of web requests:

```bash
bunx opensrc path napi-rs/website
# ► ~/.opensrc/repos/github.com/napi-rs/website/main/content/docs/**/*.en.mdx
```

The pages that matter most: `cli/napi-config`, `cli/build`, `cli/artifacts`,
`cli/pre-publish`, `deep-dive/release`, `cross-build`, `more/integrations`,
`more/troubleshooting`.

Reference projects:

- <https://github.com/napi-rs/package-template> — the canonical layout and CI
- <https://github.com/Brooooooklyn/Image> — a large real addon
- <https://github.com/napi-rs/napi-rs> — read `cli/` source when the docs are thin

## Requirements

napi-rs v3 needs **Rust 1.88+**. The CLI needs **Node `^20.17 || ^22.13 || >=23.5`**;
that is a build-time requirement and is unrelated to what the addon supports at
runtime.

## Scaffold, or set up by hand

```bash
npx @napi-rs/cli new my-addon --name @scope/my-addon --no-interactive
```

`napi new` copies the maintained Yarn or pnpm template, applies the name and
target selection, and can emit a working CI workflow. Prefer it for a new
standalone package. For an existing crate or a monorepo, add the four input
files below by hand.

Rename later through the CLI so Cargo, the napi config, CI, and the generated
binding names stay aligned:

```bash
npx napi rename --name @scope/my-addon --binary-name my-addon \
  --repository https://github.com/you/my-addon.git
```

## What the build generates, and what controls it

`napi build` is a code generator. **Never hand-edit its output and never commit
it.** To change any of it, change the input and rebuild.

| Generated | Controlled by |
|---|---|
| `<binaryName>.<platform-arch-abi>.node` | `napi.binaryName`, `--target`, `--platform`, `--release`, `--profile`, `--strip` |
| `index.js` — the loader | `--platform` (without it there is **no loader**), `--js <path>`, `--no-js`, `--esm`, `--js-package-name`, `napi.packageName` |
| `index.d.ts` — the types | `napi-derive`'s `type-def` feature, `--dts <path>`, `napi.dtsHeader` / `napi.dtsHeaderFile` / `--no-dts-header`, `--const-enum`, and per-item `#[napi(skip_typescript)]`, `ts_args_type`, `ts_return_type` |
| `npm/<platform-arch-abi>/` | `napi.targets`, then `napi create-npm-dirs` |
| root `optionalDependencies` | `napi pre-publish`, one exact-version entry per configured target |
| WASI loaders and workers | a WASI entry in `napi.targets`, plus `napi.wasm.*` |

Two consequences people get wrong:

**`napi.targets` is a packaging list, not a build command.** Each `napi build`
compiles exactly one target, chosen by `--target`, `CARGO_BUILD_TARGET`, or the
host. Adding a triple to `targets` creates a package directory and an optional
dependency; it does not create a CI job or a binary.

**No `.d.ts` means `type-def` is off.** It ships in `napi-derive`'s default
features. If default features are disabled, add it back:

```toml
napi-derive = { version = "3", default-features = false, features = ["strict", "type-def"] }
```

Generated does not mean untracked. The official template **commits `index.js`
and `index.d.ts`** so the JavaScript surface shows up in review and consumers of
the repo can typecheck without a Rust build. It **gitignores `*.node`** and
`npm/`. Committing `npm/` leaves stale versions that publish over good ones; the
release job recreates it with `napi create-npm-dirs`.

Committed or not, they are still output. A hand edit is lost on the next build
and silently disagrees with the Rust source.

## Input files

### `Cargo.toml`

`crate-type` must include `cdylib`; Node loads a shared library. Add `rlib` too
when `examples/` or benches need to link the crate normally.

```toml
[package]
name = "my-addon-native"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
napi = { version = "3", features = ["napi8", "serde-json"] }
napi-derive = "3"

[build-dependencies]
napi-build = "2"

[profile.release]
lto = true
strip = "symbols"
```

`napi-build` stays on **2** even for napi-rs v3. The v2-to-v3 migration guide
says `3`; it is wrong, and the crate has no 3.x. Copy the template.

When the same crate also builds for `wasm32-unknown-unknown`, gate the napi
dependency, because `napi` does not compile for that target:

```toml
[target.'cfg(not(all(target_arch = "wasm32", target_os = "unknown")))'.dependencies]
napi = { version = "3", features = ["napi8", "serde-json"] }
napi-derive = "3"
```

### `build.rs`

Must sit at the crate root.

```rust
fn main() {
    napi_build::setup();
}
```

### `package.json`

```json
{
  "name": "@scope/my-addon",
  "version": "0.1.0",
  "main": "index.js",
  "types": "index.d.ts",
  "repository": { "type": "git", "url": "https://github.com/you/my-addon" },
  "napi": {
    "binaryName": "my-addon",
    "targets": [
      "aarch64-apple-darwin",
      "x86_64-apple-darwin",
      "x86_64-unknown-linux-gnu",
      "aarch64-unknown-linux-gnu",
      "x86_64-pc-windows-msvc",
      "aarch64-pc-windows-msvc"
    ]
  },
  "publishConfig": { "registry": "https://registry.npmjs.org/", "access": "public" },
  "scripts": {
    "build": "napi build --platform --release",
    "build:debug": "napi build --platform",
    "artifacts": "napi artifacts",
    "version": "napi version",
    "universalize": "napi universalize",
    "prepublishOnly": "napi pre-publish -t npm"
  },
  "devDependencies": { "@napi-rs/cli": "^3" },
  "files": ["index.js", "index.d.ts"]
}
```

`repository` must be the real repository. npm provenance validates it, so a
leftover template URL fails the release.

v3 config field names, and the v2 names they replaced:

| v3 | v2 |
|---|---|
| `napi.binaryName` | `napi.name` |
| `napi.targets` (flat array) | `napi.triples.defaults` and `.additional` |
| `napi.packageName` | `napi.package.name` — **not read by v3**, move it yourself |

### `.gitignore`

```
npm/
*.node
```

`index.js` and `index.d.ts` stay tracked, like the template does. Regenerate
them with a build; never edit them by hand.

### `src/lib.rs`

```rust
#![deny(clippy::all)]

use napi::bindgen_prelude::*;
use napi_derive::napi;

/// `#[napi(object)]` is a value shape. It becomes a TypeScript interface and
/// converts to and from a plain object. Every field must be public.
#[napi(object)]
pub struct EventPayload {
    pub element_id: f64,
    pub event_type: String,
    pub x: Option<f64>,
}

/// `#[napi]` on a struct gives it JavaScript class identity.
#[napi]
pub struct Renderer {
    count: u32,
}

#[napi]
impl Renderer {
    #[napi(constructor)]
    pub fn new() -> Self {
        Self { count: 0 }
    }

    #[napi]
    pub fn set_text(&mut self, id: u32, content: String) -> Result<()> {
        if content.is_empty() {
            return Err(Error::from_reason("content must not be empty"));
        }
        self.count += 1;
        Ok(())
    }

    /// `get_count` becomes the property `count`.
    #[napi(getter)]
    pub fn get_count(&self) -> u32 {
        self.count
    }
}

/// A free function becomes a named export. `Option<T>` becomes `arg?: T | null`.
#[napi]
pub fn parse_json(input: String, pretty: Option<bool>) -> Result<serde_json::Value> {
    serde_json::from_str(&input).map_err(|error| Error::from_reason(error.to_string()))
}
```

`snake_case` becomes `camelCase`, struct names become `PascalCase`. Override
with `#[napi(js_name = "…")]`.

Useful attributes: `object`, `array`, `transparent`, `constructor`, `factory`,
`getter`, `setter`, `strict`, `catch_unwind`, `namespace`, `skip_typescript`.
`catch_unwind` is **not** a safety boundary; return `Result` for expected
failures.

### Calling JavaScript from another thread

`ThreadsafeFunction<Arg, Return>` is the only safe way. It queues on the Node
event loop.

```rust
use napi::threadsafe_function::{ThreadsafeFunction, ThreadsafeFunctionCallMode};

#[napi]
pub struct Renderer {
    on_event: Option<Arc<ThreadsafeFunction<EventPayload, ()>>>,
}

#[napi]
impl Renderer {
    #[napi(constructor)]
    pub fn new(event_callback: Option<ThreadsafeFunction<EventPayload, ()>>) -> Self {
        Self { on_event: event_callback.map(Arc::new) }
    }

    fn emit(&self, payload: EventPayload) {
        if let Some(tsf) = &self.on_event {
            tsf.call(Ok(payload), ThreadsafeFunctionCallMode::NonBlocking);
        }
    }
}
```

The generated type carries the Node error-first shape:

```ts
constructor(eventCallback?: ((err: Error | null, arg: EventPayload) => any) | null)
```

Prefer `NonBlocking`. Everything a `ThreadsafeFunction` stores must be
`'static`, so convert scoped JS values (`Object<'env>`, `Function<'env, …>`) to
owned Rust data before crossing the thread boundary, or you get `E0521`.

## Build

```bash
npx napi build --platform --release
npx napi build --platform                       # debug
npx napi build --platform --release -t aarch64-apple-darwin
npx napi build --platform -- --locked           # flags after -- go to cargo build
```

Always ship and benchmark the **release** build. A debug `.node` is many times
slower and looks like an application bug.

A `.node` cannot be unloaded. `require()` calls `process.dlopen` and Node has no
unload, so **there is no hot reload for native code**. Restart the process after
a rebuild; a watcher that only remounts JavaScript keeps the old binary.

In a split workspace, make every path explicit. `--package` is required when
the manifest is a virtual workspace:

```bash
npx napi build --platform \
  --cwd packages/addon \
  --manifest-path ../../Cargo.toml \
  --package my-addon-native \
  --package-json-path package.json \
  --output-dir .
```

Keep the loader and its local `.node` together. Moving only `index.js` breaks
its relative lookup.

## Cross-compiling

Pick **exactly one** flag; any pair is a hard error. Full matrix in
`docs/cross-build`.

| Flag | Use for | Mechanism |
|---|---|---|
| `--use-napi-cross` | Linux glibc targets from a Linux x64/arm64 host | downloads a gcc toolchain, glibc 2.17 floor, still `cargo build` |
| `--cross-compile` / `-x` | Windows MSVC from a non-Windows host, musl, and as the zig fallback | swaps in `cargo xwin build` or `cargo zigbuild` |
| `--use-cross` | legacy, avoid | runs `cross build` in Docker |

`rustup target add <triple>` first. macOS and Windows targets are far easier on
a native runner; copy what the generated CI does.

## CI: one job per target, then one collection job

```yaml
jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        settings:
          - host: macos-latest
            target: aarch64-apple-darwin
            build: napi build --platform --release --target aarch64-apple-darwin
          - host: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            build: napi build --platform --release --target x86_64-unknown-linux-gnu --use-napi-cross
          - host: windows-latest
            target: x86_64-pc-windows-msvc
            build: napi build --platform --release --target x86_64-pc-windows-msvc
    runs-on: ${{ matrix.settings.host }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          target: ${{ matrix.settings.target }}
          cache: false
          # the action defaults to RUSTFLAGS="-D warnings"; keep lint policy in
          # the crate instead of letting CI deny every warning
          rustflags: ""
      - run: npx ${{ matrix.settings.build }}
      - uses: actions/upload-artifact@v4
        with:
          name: bindings-${{ matrix.settings.target }}
          path: my-addon.*.node
          if-no-files-found: error
```

Set `if-no-files-found: error`. Without it a target that silently produced no
binary publishes a broken platform package.

## Publish

The pipeline, in order. Each command does one thing and none of them covers for
another:

```
napi build (once per matrix row)   ►  upload artifacts
        ▼
napi create-npm-dirs               ►  npm/<target>/package.json, from napi.targets
        ▼
download-artifact                  ►  artifacts/**/my-addon.<target>.node
        ▼
napi artifacts                     ►  copies each binary into npm/<target>/ AND the package root
        ▼
napi pre-publish -t npm            ►  syncs versions, writes optionalDependencies,
                                      publishes every platform package, uploads GH assets
        ▼
npm publish                        ►  the root package
```

`napi pre-publish` (alias `napi prepublish`) never publishes the root package.
It runs as `prepublishOnly`, so the surrounding `npm publish` does that after it
returns. Order is forced: **platform packages, then the root, then anything that
depends on the root.** If the root lands first, an install in that window cannot
resolve a binary.

**A multi-platform release is not atomic.** npm versions are immutable and the
CLI cannot roll back. A missing target file is a *warning*, not an error, so add
an explicit CI gate that every configured target directory holds exactly its
expected `.node` before the publish step runs.

To inspect the tarball safely:

```bash
npm pack --dry-run --ignore-scripts
```

**Never use `npm publish --dry-run` as a safety check.** npm can still run
lifecycle scripts, and a `prepublishOnly` containing `napi pre-publish` will
publish the real platform packages with real credentials.

Guard local publishing:

```json
"prepublishOnly": "node -e \"if (!process.env.CI) { console.error('CI is the only release path'); process.exit(1) }\" && napi pre-publish -t npm --no-gh-release"
```

After a partial failure, do **not** bump the version. Inventory what exists
with `npm view <pkg>@<version> version`, keep the same artifacts, and re-run the
same version; already-published packages are skipped.

## Never ship every binary in the main package

The most common napi packaging bug. It costs users a multiple-times-larger
install and nothing fails, so nobody notices.

`napi artifacts` writes each collected binary **twice**, by design. From the
official docs:

> Native files are also copied to the root package directory so the generated
> loader can resolve a local binding.

```
artifacts/bindings-*/my-addon.<target>.node
        │
        ├──► npm/<target>/my-addon.<target>.node   the per-platform package
        └──► ./my-addon.<target>.node              local require, and napi universalize
```

The root copy is what lets a CI job smoke-test the addon without installing
anything:

```yaml
- run: node -e "require('./packages/native'); console.log('binding OK')"
```

Then one glob publishes all of them:

```json
"files": ["index.js", "index.d.ts", "*.node"]
```

```
node_modules                       254M
├── @scope/addon                   185M   ◄── all six binaries, from the glob
├── @scope/addon-darwin-arm64       23M   ◄── the one that actually loads
└── consumer package               544K
```

Nothing breaks because the loader tries the **local file before** the optional
dependency, so the root copies silently shadow the per-platform packages.

**The rule: never put `*.node` in `files`.** The official template does not:

```json
"files": ["index.d.ts", "index.js", "browser.js"]
```

`optionalDependencies` already delivers the right binary. Keep `*.node` in
`.gitignore` so a stray local build cannot be published either. Verify with
`npm pack --dry-run --ignore-scripts`: more than one `.node` in the list means
the glob is back.

## The loader contract

The generated loader is output, so debug it through its documented interface,
not by reading or editing it. In order it tries the explicit override, a local
`<binaryName>.<platform-arch-abi>.node`, the matching optional package, then a
configured WASI fallback.

| Environment variable | Effect |
|---|---|
| `NAPI_RS_NATIVE_LIBRARY_PATH=/abs/addon.node` | **Replaces** platform and package selection with one library. Never ship this as normal package config |
| `NAPI_RS_ENFORCE_VERSION_CHECK=1` | Rejects a platform package whose version differs from the root. Off by default, so a stale package otherwise loads silently |
| `NAPI_RS_FORCE_WASI=error` | Chains WASI failures into the thrown error; ordinary WASI fallback failures are not in the normal cause chain |

It throws **one** error whose `cause` chain holds every native candidate
failure. Print the chain instead of reporting "Cannot find native binding":

```js
try {
  require('./index.js')
} catch (error) {
  let current = error
  for (let depth = 0; current; depth++, current = current.cause) {
    console.error(`[cause ${depth}]`, current.stack || current)
  }
}
```

Then read the real cause:

| Message | Meaning |
|---|---|
| `wrong ELF class`, `Exec format error`, `not a valid Win32 application` | CPU or OS mismatch |
| `GLIBC_x.y not found` | built against newer glibc than the runtime; rebuild with a lower floor, do **not** switch to musl |
| `undefined symbol: napi_*` | the addon enabled a higher Node-API level than the runtime provides |
| optional package simply absent | `--no-optional`, a lockfile from another platform, or a deploy that dropped `.node` files |

The target suffix is a **selection contract, not a conversion**. Never rename a
musl binary to `-gnu` or an x64 binary to `arm64`.

Turn on both diagnostics when reproducing:

```bash
DEBUG='napi:*' RUST_BACKTRACE=full npx napi build --platform --verbose
DEBUG='napi:*' node ./repro.cjs
```

## Consuming an addon: externalize it

A `.node` is a shared library, not JavaScript. Never let a bundler transform,
hash, or inline it. Mark the addon **and** its platform packages external, then
make sure the deployment actually installs them.

```js
external: ['@scope/addon', '@scope/addon-*']         // esbuild
externals: { '@scope/addon': 'commonjs @scope/addon' } // webpack
serverExternalPackages: ['@scope/addon']              // next.config
ssr: { external: ['@scope/addon'] }                   // vite
```

Externalizing does not package anything. Copy or install the root package and
its matching optional dependency into the image, function, or layer, then smoke
test one export from the final artifact.

For CommonJS versus ESM, generate the wrapper you need rather than transforming
it: `--js index.cjs` for CJS, `--platform --esm --js index.js` for real ESM
named exports. A CJS wrapper inside a `"type": "module"` package must use
`.cjs`.

## Gotchas

**Command names changed in v3.** `create-npm-dir` → `create-npm-dirs`,
`napi universal` → `napi universalize`, `--cargo-cwd` → `--manifest-path`,
`--cargo-flags="--locked"` → `-- --locked`. A stale script fails with an
unknown-command error, so run `npx napi --help` after a CLI major bump.

**`--platform` is not optional in practice.** Without it the CLI copies a plain
`index.node` and generates **no loader**.

**`crate-type` must include `cdylib`,** or cargo builds an rlib and the CLI
finds nothing to copy.

**A stale `.d.ts`** usually means the export is behind a `#[cfg(...)]`, carries
`#[napi(skip_typescript)]`, or the dts cache is stale. Delete only
`target/napi-rs` and rebuild.

**Write user-facing docs in Rust.** Doc comments on `#[napi]` items become JSDoc
in the generated `.d.ts`, so that is the only place to put them.
