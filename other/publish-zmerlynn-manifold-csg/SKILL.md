---
name: publish
description: Publish crates to crates.io with pre-flight checks
user-invocable: true
---

# Publish

Publish our 4 crates to crates.io with pre-flight validation. The workspace
has two canonical crates (`manifold-csg-sys`, `manifold-csg`) and two thin
facade re-exports (`manifold3d-sys`, `manifold3d`) under the same version
numbers. Facades always ship in lockstep with their canonical counterparts
via `=` version pins.

## Arguments

- No arguments: publish all 4 crates in dependency order
- `--dry-run`: run all checks but don't actually publish

## Pre-flight checks

Run all checks before publishing. Stop on first failure.

### 1. Clean working tree

```
git status
```

Must be on `main` with no uncommitted changes. Refuse to publish from a feature branch.

### 2. Build and test

```
cargo test --features nalgebra
cargo clippy --all-targets --all-features -- -D warnings
```

### 3. Version bump

Version bumps happen at publish time, not in feature PRs. Read CLAUDE.md for the versioning scheme, then:

- **Check if versions have already been bumped** by comparing the workspace + sys crate versions against what's actually published on crates.io:
  ```sh
  # crates.io rejects curl's default User-Agent; it wants one that identifies the caller
  UA="manifold-csg-publish (+https://github.com/$(gh api user --jq .login))"
  curl -sS -A "$UA" https://crates.io/api/v1/crates/manifold-csg     | python3 -c "import json,sys; print(json.load(sys.stdin)['crate']['max_version'])"
  curl -sS -A "$UA" https://crates.io/api/v1/crates/manifold-csg-sys | python3 -c "import json,sys; print(json.load(sys.stdin)['crate']['max_version'])"
  ```
  Without the `-A`, crates.io returns an error body and the `['crate']` lookup dies with a `KeyError`, which reads like a network blip, not a blocked request. If it fails anyway, the sparse index needs no User-Agent: `curl -sS https://index.crates.io/ma/ni/manifold-csg` (one JSON object per line, last is newest).
  If the in-repo version is already ahead of the published version, it's pre-bumped — DO NOT bump again. Subsequent feature PRs ride into the pre-bumped version. (Pitfall: assuming the workspace version is the published version. They diverge whenever a PR includes its own bump, which CLAUDE.md says PRs "usually should" do.)
- If not already bumped:
  - **`manifold-csg-sys`**: bump the patch component (e.g., `3.4.102` → `3.4.103`) whenever the upstream contents differ from the last publish — pinned commit changed, carry-patches added/removed, or FFI declarations changed. If the upstream major.minor changed (new manifold3d release), update major.minor accordingly.
  - **`manifold-csg`** (workspace version): bump patch for additive changes, minor for breaking changes (pre-1.0, minor bumps can break).
  - **`manifold3d-sys`** version must match the new `manifold-csg-sys` version exactly (= pin).
  - **`manifold3d`** inherits the workspace version, so bumps automatically. Its `manifold-csg` dependency `=` pin must be updated to the new workspace version.
  - Update `manifold-csg`'s `manifold-csg-sys` dependency version to match. Update `manifold3d-sys`'s `manifold-csg-sys` `=` pin and `manifold3d`'s `manifold-csg` `=` pin.
- Commit the version bumps on a branch, open a PR, and get it merged before proceeding. Branch protection requires this — you cannot push version bumps directly to main.

### 4. Carry-patch audit

For each patch in `crates/manifold-csg-sys/patches/`:
- Check if the upstream PR has been merged (use `gh api`)
- If merged AND included in our pinned commit, warn that the patch can be removed
- If the patch fails to apply during build, stop — the pin and patches are inconsistent

### 5. Release notes

`crates/manifold-csg/CHANGELOG.md` must have an entry for the version being published. It ships inside the tarball, so it is the only release note a vendored consumer ever sees. See CLAUDE.md for what belongs in it, especially the rule about flagging silent behavioral changes.

If the entry is missing, add it in the same PR as the version bump (step 3). Do not publish without it.

Tagging and the GitHub Release happen after publishing, in Post-publish.

### 6. Dry run

Run a dry run for each crate in publish order:

```
cargo publish --dry-run -p manifold-csg-sys
cargo publish --dry-run -p manifold3d-sys
cargo publish --dry-run -p manifold-csg
cargo publish --dry-run -p manifold3d
```

Facade dry runs will fail if their canonical counterparts aren't already on crates.io at the expected version — this is expected for first publish and version bumps. The real dry-run validation for facades happens after their canonical is published.

For each crate, check:
- **Crate size** — warn if over 500KB (we don't vendor C++ source, so it should be small)
- **File list** — `cargo package --list -p <crate>` — verify no secrets, build artifacts, or unnecessary files are included
- **License files** — `LICENSE-APACHE` and `LICENSE-MIT` must be present

### 7. docs.rs build simulation

```
DOCS_RS=1 cargo doc --no-deps --features nalgebra \
  -p manifold-csg-sys -p manifold-csg -p manifold3d-sys -p manifold3d
```

Must build without errors. docs.rs runs with `--network=none`, so `build.rs` must detect `DOCS_RS` and skip the C clone/build.

### 8. API stability check

Before first publish or any version where the public API changed:
- List all `pub` items in `manifold-csg` — are any provisional or likely to change?
- Flag return types that lock us in (e.g., `Vec<f64>` vs a newtype)
- Remind: once published, the API is semver-locked. For pre-1.0 crates (`0.x.y`), minor bumps (`0.1.0` → `0.2.0`) can contain breaking changes, but patch bumps (`0.1.0` → `0.1.1`) must be backwards-compatible. Post-1.0, breaking changes require a major bump.

### 9. Documentation

```
cargo doc --features nalgebra --no-deps
```

Must build without warnings. Spot-check that crate-level docs render correctly.

## Publish

Only after all checks pass. **Always get explicit user confirmation before running `cargo publish`.**

### Order matters

Dependencies must reach crates.io before their dependents:

1. `manifold-csg-sys` (no internal deps)
2. `manifold3d-sys` (facade of `manifold-csg-sys`)
3. `manifold-csg` (depends on `manifold-csg-sys`)
4. `manifold3d` (facade of `manifold-csg`)

Between each publish, crates.io may take a moment to index the new version. If the next publish fails with "no matching package", wait and retry.

```
cargo publish -p manifold-csg-sys
cargo publish -p manifold3d-sys
cargo publish -p manifold-csg
cargo publish -p manifold3d
```

### Post-publish

A publish is not finished when `cargo publish` returns. Users watching the repo see the Releases page, not crates.io, so skipping the release step means the feature looks unshipped no matter what is on crates.io. This has actually happened here: v0.3.1 through v0.3.3 were published and tagged but had no GitHub Release for two months, and the reporter on #49 asked for a "release bump" for a feature that had been live since 0.3.1.

**1. Tag.** Use the `manifold-csg` version number; facades share the workspace version.

```
git tag -a v<version> -m "Release <version>"
git push origin v<version>
```

The tag must be annotated (`-a`). A GitHub Release inherits its `created_at` from the annotated tag's tagger date, and the Releases page sorts on `created_at`. A lightweight tag loses that.

**2. GitHub Release.** Write the notes to a file first, then create it. Get user confirmation before creating, since this is an externally visible write.

```
gh release create v<version> --verify-tag --latest --title v<version> --notes-file <file>
```

- `--verify-tag` fails if the tag does not exist rather than silently creating one.
- Pass `--latest` explicitly. When backfilling several releases, the older ones need `--latest=false` so the newest keeps the marker.
- Write the notes rather than relying on `--generate-notes`. Source them from the CHANGELOG entry and the merged PR bodies. Cover: what changed and whether it is additive or breaking, a usage snippet for anything with a non-obvious entry point (env vars, build levers), and credit by @handle to anyone who filed the issue or sent the fix.
- Link migration guides by absolute URL, and match the existing releases' section layout (`### Additions`, `### Fixes`, `### Raw sys (...)`, `### Credit`, then the compare link).

**3. Verify.**

- All 4 crates appear on crates.io at the new version, and docs.rs builds succeed for all 4.
- Every tag has a release: compare `git tag` against `gh release list`. Any tag missing a release is a backfill to cut.
- If any issues were closed by this release, comment on them with the version and a link (ask before posting).

## Rules

- **NEVER publish without explicit user confirmation** — dry run is the default mindset
- **A release is not done until the GitHub Release exists.** crates.io and the tag are two of three steps; report the publish as incomplete until the release is cut.
- Do NOT publish from a dirty working tree or a non-main branch
- Do NOT publish if tests or clippy fail
- If any publish succeeds but a later one fails, report this clearly — published versions can only be yanked, not deleted. Common failure: facade fails because its canonical isn't indexed yet; retry after a delay.
- Sys crate patch bumps must be semver-compatible (additions only)
- Facade crates must always share the exact version of their canonical counterpart (`=` pin in Cargo.toml enforces this)
