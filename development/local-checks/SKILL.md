---
name: local-checks
description: How to compile and test a change locally in Kaeri before pushing (Rust, Android, Apple, website), under the HOME guard with the shared caches. Use before any push, and whenever running tests or builds.
---

# Local checks

Compile and run the touched area's tests before every push. CI is slow; never push uncompiled code.

## The HOME guard

Tests must never see the real HOME or the real app data. Run checks in a subshell like this, and
commit **outside** it (the temporary HOME hides `~/.gitconfig`, so commits come out unsigned):

```bash
(
  real=$HOME
  export CARGO_HOME=$real/.cargo RUSTUP_HOME=$real/.rustup GRADLE_USER_HOME=$real/.gradle
  export ANDROID_HOME=$real/Library/Android/sdk
  export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
  export RUSTC_WRAPPER=sccache SCCACHE_DIR=$real/.cache/sccache CARGO_BUILD_JOBS=4 CARGO_INCREMENTAL=0
  export CARGO_TARGET_DIR=$real/kaeri-target-<your-task>   # your own; delete when done
  export KAERI_ENGINE_CACHE=$real/.cache/kaeri-engine  # without it engine.sh rebuilds from scratch
  guard=$(mktemp -d) && trap 'rm -rf "$guard"' EXIT          # each run cleans up its own HOME
  export HOME=$guard KAERI_TOKEN_STORAGE=file KAERI_PLAYER_NATIVE=off
  [ "$HOME" != "$real" ] || exit 1
  # checks go here
)
```

## By area (run what the change touches)

- **Rust:** `cargo check --workspace --all-targets --locked`; tests for touched crates
  (`cargo test -p <crate>`); `cargo clippy --workspace --all-targets -- -D warnings`, plus
  `-p kaeri-engine --no-default-features` and `-p kaeri-model --features ffi`;
  `cargo fmt --check`; `tools/check-boundaries.sh`; `tools/check-plugins.sh`. Store crates: `deploy/sync.sh --check`.
  Dependencies: `cargo audit`. Goldens: look at the diff before re-blessing.
- **FFI:** `cargo test -p kaeri-ffi --features testing,cli`.
- **Android:** `android/scripts/engine.sh testing`, then from `android/`:
  `./gradlew --max-workers=3 :store:testFixturesDebugUnitTest :ui:testFixturesDebugUnitTest :app:assembleFixturesDebug`
  (add `:player`, `:widgets`, `:app` tests and `:app:minifyFixturesReleaseWithR8` when touched).
  Re-record scenes with `android/scripts/scenes.sh` after engine record changes.
- **Apple:** `apple/scripts/engine.sh testing`, then per touched package `swift test` and
  `swift build -c release` (Release catches concurrency errors). iPhone-only code: build the
  Fixtures app for the iOS Simulator. Mac Release app: build with signing off, then
  `apple/scripts/signing-keychain.sh sign $real/.kaeri-signing/mac <app>` must verify. It signs
  with Kaeri's certificate through a throwaway keychain, as a release is signed, so a review
  build keeps its keychain access; `apple/scripts/adhoc-sign.sh <app>` alone signs ad hoc.
- **Website:** `cd website && bun install --frozen-lockfile && bun run build`.

## Output and disk

- Pipe long output through `grep -E 'error|warning: unused|FAILED|panicked|✘'` or `tail`; don't
  read whole logs.
- Keep free disk above 10 GB (`df -h /`). Each Swift package's `.build` holds all its
  dependencies; delete it once that package's checks pass. Delete your target dir when done.
- Xcode keeps a DerivedData folder per project path, which outlives a removed worktree. Before
  `git worktree remove`, delete the ones for your worktree, and erase or delete the Simulators
  you created:

  ```bash
  for d in ~/Library/Developer/Xcode/DerivedData/*/; do
    p=$(/usr/libexec/PlistBuddy -c 'Print :WorkspacePath' "$d/info.plist" 2>/dev/null)
    [[ "$p" == "$PWD"/* ]] && rm -rf "$d"
  done
  ```
- The engine cache keeps the newest four builds per slice (`KAERI_ENGINE_CACHE_KEEP`), so
  don't prune it by hand while other builds run.
