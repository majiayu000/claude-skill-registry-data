---
name: nix-ci
description: Use this when setting up CI for a GitHub repository — offers GitHub Actions or Vira depending on the project
---

# GitHub Actions CI Setup

Use the [install-nix](https://github.com/nixbuild/nix-quick-install-action) action (avoid DetSys actions) and invoke Nix to build:

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: nixbuild/nix-quick-install-action@v34
      - run: nix build # Or, better, build *all* flake outputs
```

## Caching the Nix store (plain `nix build`, no Vira)

When building directly with `nix build` on GitHub runners (instead of `vira ci`), cache `/nix/store` across runs with [`cache-nix-action`](https://github.com/nix-community/cache-nix-action). Otherwise every run re-fetches all dependency tarballs and rebuilds the whole closure — easily 30 min for a large app. With a warm cache the build job drops to ~1 min (dominated by the restore).

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      actions: write          # REQUIRED — see gotcha 2 below
    steps:
      - uses: actions/checkout@v4
      - uses: nixbuild/nix-quick-install-action@v34
      - uses: nix-community/cache-nix-action@v6
        with:
          primary-key: nix-${{ runner.os }}-${{ hashFiles('flake.lock', '**/flake.nix') }}
          restore-prefixes-first-match: nix-${{ runner.os }}-
          gc-max-store-size-linux: 5G   # keep under the 10 GB repo cache limit
          purge: true
          purge-prefixes: nix-${{ runner.os }}-
          purge-last-accessed: 604800
          purge-primary-key: never
      - run: nix build -L
```

Two gotchas, each of which makes the cache **silently no-op** (save/restore complete in ~1s and nothing is cached):

1. **`cache-nix-action` must pair with `nix-quick-install-action`, not the DeterminateSystems installer.** The DetSys daemon-based store layout isn't snapshotted by the cache action. (This is the concrete reason for "avoid DetSys actions" above.)
2. **`purge: true` requires `actions: write` permission.** Without it the save aborts with `Resource not accessible by integration` (it calls the REST cache API to purge stale entries) and no `nix-*` cache is ever created.

Verify it worked: `gh cache list` should show a `nix-*` entry sized in the hundreds-of-MB-to-GB range — not just the installer's own ~40 MB cache.


