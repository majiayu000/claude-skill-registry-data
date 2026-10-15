---
name: nix-bun
description: Use this when building a Bun (bun.lock) project with Nix. Covers bun2nix, the bun.nix dependency workflow, the bun --compile top-level-await pitfall, and a CI drift check.
---

# Bun + Nix with bun2nix

For Bun projects (those with a `bun.lock`), use [bun2nix](https://github.com/nix-community/bun2nix) — it converts the lockfile into a `bun.nix` expression so Nix installs dependencies deterministically and offline. Keep nixpkgs pinned via npins (see `nix-for-dev`) and add bun2nix as the single flake input.

## Dependency workflow

`bun.nix` is generated and must track `bun.lock`. Regenerate it whenever dependencies change:

```bash
nix run github:nix-community/bun2nix -- -o bun.nix
```

Pin the same bun2nix version in `flake.nix` (`?ref=2.1.0`) and in CI so generation is reproducible.

## Building

Idiomatic usage compiles a standalone binary:

```nix
# default.nix
{ bun2nix, ... }:
bun2nix.mkDerivation {
  pname = "myapp";
  version = "1.0.0";
  src = ./.;
  bunDeps = bun2nix.fetchBunDeps { bunNix = ./bun.nix; };
  module = "src/index.ts";   # entrypoint compiled into `bin/myapp`
}
```

`bun2nix.packages.<system>.default` carries `mkDerivation`, `fetchBunDeps`, and `hook` as passthru attrs, so you can use it without a flake-parts overlay.

### Pitfall: `bun build --compile` is fragile

`mkDerivation { module = ...; }` runs `bun build --compile`, which **fails on top-level `await`** (`error: "await" can only be used inside an "async" function`) and can produce a broken binary for apps with **native addons or workers**. (`bun run` handles all of these — only the bundler chokes.)

When `--compile` doesn't work, build a wrapper that runs the entrypoint with `bun` instead, using bun2nix only for deterministic deps:

```nix
{ pkgs, bun2nix, ... }:
pkgs.stdenv.mkDerivation {
  pname = "myapp"; version = "1.0.0"; src = ./.;
  nativeBuildInputs = [ bun2nix.hook pkgs.makeWrapper ];  # hook populates node_modules offline
  bunDeps = bun2nix.fetchBunDeps { bunNix = ./bun.nix; };
  # buildPhase: build any workspace deps (tsc) the entrypoint imports
  installPhase = ''
    appdir=$out/share/myapp
    mkdir -p $appdir $out/bin
    cp -R src package.json node_modules $appdir/
    makeWrapper ${pkgs.bun}/bin/bun $out/bin/myapp --add-flags "run $appdir/src/index.ts"
  '';
  dontFixup = true;
}
```

The bun2nix hook runs `patchShebangs`, but tsc's `/usr/bin/env node` shebang still breaks in the sandbox — invoke it as `bun ./node_modules/typescript/bin/tsc` instead of via the `.bin` symlink.

## CI: keep bun.nix from drifting

Add a check that fails when `bun.nix` is out of sync with `bun.lock`:

```yaml
- run: |
    nix run github:nix-community/bun2nix/2.1.0 -- --lock-file ./bun.lock --output-file ./bun.nix
    git diff --exit-code -- bun.nix \
      || { echo "::error::bun.nix is stale — run: nix run github:nix-community/bun2nix -- -o bun.nix"; exit 1; }
```

This check is fast; run it as a separate job from the (slow) `nix build` so PRs get quick feedback. For the build job, cache `/nix/store` — see `nix-ci`.
