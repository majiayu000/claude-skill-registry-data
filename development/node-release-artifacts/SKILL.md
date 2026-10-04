---
name: node-release-artifacts
description: Choosing and building the release artifact for a Node Web Only project - a single self-contained binary or a runtime-bundled tarball. Use when deciding what a Node project ships, compiling with Bun or Node SEA, writing the bundle script or its launcher, or proving a bundle runs without a system Node. Triggers on bun build --compile, node --build-sea, sea-config.json, postject, scripts/bundle.sh, a runtime/bin/node layout, and a .tar.gz release asset.
user-invocable: false
---

# Node Release Artifacts

**Two shapes. A native addon decides which one, and a project ships one of them, never both.**

| Situation | Artifact |
|---|---|
| Pure JS, no native addons, and one file is wanted | a compiled binary |
| Any native addon present, or neither binary path fits cleanly | a runtime-bundled tarball |

Compiled `.node` addons are the deciding factor, because the embedder bundles JavaScript into its own virtual filesystem and a native module has to be a real file the dynamic loader can open. Bun does not embed one. Node SEA carries it as an entry in the config's `assets` map, which the entry script then writes to a temp file and loads with `process.dlopen()`, so the addon is unpacked on every start and a blob produced by `postject` inside a Linux arm64 container crashes on that call.

The tarball keeps the addon a real file on disk with no unpacking step, so it stays the choice whenever one is present and the fallback whenever the answer is unclear.

## Path 1: A Compiled Binary

Two toolchains produce one executable carrying a JS runtime, the server, and the embedded frontend.

### Bun

```bash
bun build ./bin/[APP_NAME].js --compile --minify \
  --target=bun-linux-x64-musl \
  --outfile dist/[APP_NAME]-linux-x64
```

Every target cross-compiles from one host by changing `--target`, so the whole matrix builds on a single runner.

| Platform | Target |
|---|---|
| Linux x64, static | `bun-linux-x64-musl` |
| Linux arm64, static | `bun-linux-arm64-musl` |
| macOS x64 | `bun-darwin-x64` |
| macOS arm64 | `bun-darwin-arm64` |

Frontend assets are folded in by importing them:

```js
import index from '../public/index.html' with { type: 'file' };
```

The resulting binary runs on JavaScriptCore rather than V8, so behavior can differ from `node`. Development and unit tests stay on real Node, and the compiled binary is smoke-tested on its own before release. Testing only the source leaves the engine difference to be discovered by a user.

### Node SEA

Stays on V8, which removes the engine question entirely.

`--build-sea=config` generates the executable in one step, but it arrived in Node v25.5.0 at stability 1.1 and is absent from the Node 24 baseline these projects pin:

```bash
node --build-sea=sea-config.json
```

On Node 24 the same result takes the older two-step sequence, writing the preparation blob and injecting it with `postject`:

```bash
node --experimental-sea-config sea-config.json
cp "$(command -v node)" dist/[APP_NAME]
codesign --remove-signature dist/[APP_NAME]   # macOS only
npx postject dist/[APP_NAME] NODE_SEA_BLOB sea-prep.blob \
  --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2 \
  --macho-segment-name NODE_SEA               # macOS only
```

The signature is removed before injection and the segment name is passed on macOS only. Skipping either produces a binary that builds and then refuses to run.

SEA takes a single CommonJS entry, so an ESM project bundles first:

```bash
esbuild bin/[APP_NAME].js --bundle --platform=node --format=cjs \
  --outfile build/[APP_NAME].cjs
```

Assets are declared in the `assets` map of `sea-config.json` and read back at run time:

```js
import { getAsset } from 'node:sea';
const html = getAsset('index.html', 'utf8');
```

SEA does not cross-compile, so each target builds on a matching runner.

Bun cross-compiles from one host but changes engine; SEA keeps the engine but needs a runner per platform and a bundling step. Pick on which of those two costs the project can absorb.

## Path 2: A Runtime-Bundled Tarball

A per-platform `.tar.gz` carrying the Node runtime, the compiled native addon, the vendored frontend, and a launcher that injects the config path.

```
[APP_NAME]-<os>-<arch>/
├── bin/[APP_NAME]          # launcher shell script
├── runtime/bin/node        # the runtime for this os/arch
└── lib/
    ├── bin/                # bin/[APP_NAME].js, the entry
    ├── src/                # backend
    ├── public/             # vendored frontend
    └── node_modules/       # dependencies, including the compiled .node addon
```

`scripts/bundle.sh` downloads the matching runtime and assembles the tree. Node ships `.tar.xz` for Linux and `.tar.gz` for macOS, so the extension is chosen rather than assumed.

```bash
#!/usr/bin/env bash
set -euo pipefail
OS="$1"; ARCH="$2"
NODE_VERSION="24.20.0"
[ "$OS" = "darwin" ] && NODE_EXT="tar.gz" || NODE_EXT="tar.xz"
NODE_PKG="node-v${NODE_VERSION}-${OS}-${ARCH}"
BUNDLE="dist/[APP_NAME]-${OS}-${ARCH}"

curl -fL "https://nodejs.org/dist/v${NODE_VERSION}/${NODE_PKG}.${NODE_EXT}" -o "node.${NODE_EXT}"
tar -xf "node.${NODE_EXT}"

mkdir -p "$BUNDLE/runtime/bin" "$BUNDLE/lib" "$BUNDLE/bin"
cp "${NODE_PKG}/bin/node" "$BUNDLE/runtime/bin/node"

# The compiled .node addon and any helper binary ride along inside node_modules.
cp -R bin src public node_modules "$BUNDLE/lib/"
cp launcher/[APP_NAME] "$BUNDLE/bin/[APP_NAME]"
chmod +x "$BUNDLE/bin/[APP_NAME]"

tar -czf "${BUNDLE}.tar.gz" -C dist "$(basename "$BUNDLE")"
```

The launcher resolves its own location and runs the bundled runtime against the bundled entry, so an extracted tarball needs nothing on `PATH`:

```sh
#!/bin/sh
HERE="$(cd "$(dirname "$0")/.." && pwd)"
exec "$HERE/runtime/bin/node" "$HERE/lib/bin/[APP_NAME].js" --config "$HERE/lib/config.json" "$@"
```

`exec` replaces the shell rather than forking, so signals reach the Node process directly and a `docker stop` or a Ctrl+C triggers the graceful shutdown instead of killing a wrapper.

`"$@"` is forwarded last so a user-supplied `--config` overrides the injected default, since a later flag wins.

## Prove Self-Containment

The bundle is verified in CI by extracting it, removing every system `node` from `PATH`, starting the launcher, and requesting an endpoint. A bundle assembled on a machine that happens to have Node installed will run there and fail on a clean one, and only a scrubbed `PATH` catches that before a user does.

```bash
#!/usr/bin/env bash
set -euo pipefail
OS="$1"; ARCH="$2"
tar -xzf "dist/[APP_NAME]-${OS}-${ARCH}.tar.gz" -C /tmp

env -i PATH=/usr/bin:/bin HOME="$HOME" \
  "/tmp/[APP_NAME]-${OS}-${ARCH}/bin/[APP_NAME]" &
PID=$!
trap 'kill $PID' EXIT

sleep 2
curl -fsS http://127.0.0.1:8080/api/health
```

`env -i` clears the environment rather than editing `PATH`, which also catches a bundle that depends on an inherited `NODE_PATH` or a version manager's shims.

## Platforms

Linux x64 and arm64, macOS x64 and arm64. No Windows, because nothing here is tested on it and an untested artifact costs more in support than it delivers.

Native addons compile from source on architecture-native runners rather than cross-compiling, since `node-gyp` produces an object for the host toolchain and a cross-built addon fails to load rather than failing to build.

| Placeholder | Replace with |
|---|---|
| `[APP_NAME]` | the application name |
| `NODE_VERSION` | the pinned version, matching `.node-version` |
