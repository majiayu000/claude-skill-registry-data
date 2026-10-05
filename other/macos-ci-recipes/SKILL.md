---
name: macos-ci-recipes
description: >
  Copy-in CI recipes for adding macOS build/test/lint to a project on the ios
  profile — either a macOS-only app with no iOS target, or a hybrid app that
  also ships a separate macOS scheme sharing code with an iOS target. Use
  when scaffolding CI for a new macOS app, or adding a macOS target/scheme to
  an existing iOS project. The lacquer does not auto-sync macOS CI (only two
  fleet projects have needed it so far — not enough signal to justify
  conditional asset sync yet); these are reference recipes you copy into your
  project's own workflow files, adapted from two real, working
  implementations (a macOS-only app and an iOS+macOS hybrid).
---

# macOS CI Recipes

Two shapes, depending on whether an iOS target coexists in the same project.
Both reuse the lacquer's existing iOS CI conventions (dedicated runner,
`CODE_SIGNING_ALLOWED=NO` for non-release jobs, the exit-65 spurious-failure
handling, the error-tail grep on real failures) — nothing here is a new
pattern, just the iOS pattern applied to `-destination 'platform=macOS'`.

**Why the dedicated runner, not a GitHub-hosted macOS one:** these jobs (and
any other Xcode-touching job you add) must run on
`runs-on: [self-hosted, macOS, ARM64, dedicated]` — never `macos-latest` or a
stray label like `mac-mini`. Release jobs hold App Store Connect keys and
unlock the login keychain, so signing must only ever happen on infrastructure
you control; the pinned Xcode + simulator runtime lives only on the dedicated
runner (GitHub-hosted macOS images drift); and GitHub-hosted macOS minutes are
billed while the dedicated runner isn't. A pure script/REST-call job with no
Xcode dependency uses `blacksmith-4vcpu-ubuntu-2404` instead, and the
`if: always()` `ci-ok` merge gate uses `[self-hosted, Linux, pi-gate]` — see
the `runs-on` note under the hybrid recipe below.

## Which recipe

- **No iOS target at all** (a macOS-only app on the `ios` profile): use
  "macOS-only app" below. It replaces the synced `ios-ci.yml` outright —
  `exclude` it in `.lacquer.toml` and add this file to your project's `root/`
  tree instead (the lacquer already supports excluding a synced file; this
  is that mechanism, just pointed at CI instead of release/testflight).
- **An iOS target plus a separate macOS scheme sharing code** (e.g. a shared
  `Core/`+`Shared/` compiled into both an iOS app and a `MenuBarExtra`/full
  macOS app): use "Hybrid" below. It adds one job to your project's *own
  copy* of the synced `ios-ci.yml` — see "Living with a hand-edited managed
  file" for what that costs on future syncs.

## macOS-only app

Lint, build, and test jobs mirroring the lacquer's iOS shape, with no
simulator involved anywhere:

```yaml
name: macOS CI

on:
  workflow_dispatch:
  pull_request:
    branches: [main, develop, 'feat/*', 'fix/*']
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: swiftformat + swiftlint (strict)
    runs-on: [self-hosted, macOS, ARM64, dedicated]
    steps:
      - uses: actions/checkout@v7.0.1
      - name: swiftformat --lint
        run: swiftformat --lint {{COMPONENT_PREFIX}}.
      - name: swiftlint --strict
        run: swiftlint --strict --config {{COMPONENT_PREFIX}}.swiftlint.yml {{COMPONENT_PREFIX}}.

  build:
    name: xcodebuild build (macOS)
    runs-on: [self-hosted, macOS, ARM64, dedicated]
    steps:
      - uses: actions/checkout@v7.0.1
      # No actions/cache for SPM here: on a persistent dedicated runner,
      # DerivedData/SourcePackages already survives between runs on local
      # disk. actions/cache still tars+uploads+downloads on every run
      # regardless of whether anything changed — one fleet project measured
      # this at ~25 minutes of overhead against a 16-second compile. This is
      # an open question for the lacquer's OWN iOS ci.yml too (it still uses
      # actions/cache on the same runner class) — verify your runner is
      # actually the same persistent box across runs before dropping the
      # cache step; if it's ephemeral/rotating, keep it.
      - name: xcodebuild build
        run: |
          set -o pipefail
          xcodebuild build \
            -project "{{XCODEPROJ}}" \
            -scheme "{{SCHEME}}" \
            -destination 'platform=macOS' \
            -configuration Debug \
            CODE_SIGNING_ALLOWED=NO \
            | xcpretty --color || xcodebuild build \
              -project "{{XCODEPROJ}}" \
              -scheme "{{SCHEME}}" \
              -destination 'platform=macOS' \
              -configuration Debug \
              CODE_SIGNING_ALLOWED=NO

      - name: xcodebuild test
        run: |
          set -o pipefail
          xcodebuild test \
            -project "{{XCODEPROJ}}" \
            -scheme "{{SCHEME}}" \
            -destination 'platform=macOS' \
            -configuration Debug \
            CODE_SIGNING_ALLOWED=NO \
            -only-testing:<YourTestTarget> \
            | xcpretty --color || xcodebuild test \
              -project "{{XCODEPROJ}}" \
              -scheme "{{SCHEME}}" \
              -destination 'platform=macOS' \
              -configuration Debug \
              CODE_SIGNING_ALLOWED=NO \
              -only-testing:<YourTestTarget>

  ci-ok:
    name: CI OK
    runs-on: [self-hosted, Linux, pi-gate]
    needs: [lint, build]
    if: always()
    timeout-minutes: 2
    steps:
      - name: Verify required jobs passed (or were skipped)
        run: |
          for r in "${{ needs.lint.result }}" "${{ needs.build.result }}"; do
            if [ "$r" = "failure" ] || [ "$r" = "cancelled" ]; then
              echo "::error::A required job did not pass (result=$r)"
              exit 1
            fi
          done
```

**Why `ci-ok` is on `pi-gate` and not a hosted Linux runner.** GitHub bills
**per job started, with a one-minute minimum**, so the cost of a job tracks its
*count*, not its duration. `ci-ok` is `if: always()` and does nothing but read
`needs.*.result`, so it starts on every single run and finishes in seconds —
the one-minute minimum was the entire bill. Moving it to a box we own makes it
free. `pi-gate` is a **role** label, carried by both the Raspberry Pi and the
Synology: `runs-on` label matching is AND, so any box carrying the full set can
serve the job, and the gate fails over instead of putting the whole fleet
behind one runner. Ordinary Linux jobs stay on
`blacksmith-4vcpu-ubuntu-2404`, which bills separately from the GitHub Actions
allowance.

**UI tests are deliberately absent.** macOS UI tests need a real
WindowServer/GUI login session on the runner — there's no simulator escape
hatch like iOS has. One fleet project's UI tests hung with "test runner hung
before establishing connection" on their dedicated runner and were dropped
rather than fought. If your macOS app has UI tests, expect to need a runner
with an active GUI session (not a headless/SSH-only box) before they'll run
at all — don't assume the same runner that handles iOS simulator UI tests
can run macOS ones for free.

## Hybrid: add a macOS job to an existing `ios-ci.yml`

For a project that already syncs the lacquer's `ios-ci.yml` for its iOS
target and adds a macOS scheme alongside it (shared `Core`/`Shared` code,
`PRODUCT_MODULE_NAME` matching so `@testable import` resolves to whichever
target owns the test bundle). Add this job to your project's copy of
`ios-ci.yml`:

```yaml
  macos:
    name: macOS (Build + Test)
    runs-on: [self-hosted, macOS, ARM64, dedicated]
    needs: [lint, changes]
    # Skip on push-to-main (squash-merged tree == tested tree) and on
    # docs-only PRs. No simulator for macOS, so this is one xcodebuild that
    # builds + runs the macOS test bundle against the host Mac.
    # SECURITY: same-repo guard — fork-PR code must not build/test on the
    # self-hosted runner.
    if: (github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository) && github.event_name != 'push' && needs.changes.outputs.code == 'true'
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v7.0.1

      - name: Create Secrets.xcconfig (build-time placeholder)
        run: |
          if [ -f "{{COMPONENT_PREFIX}}Secrets.xcconfig.example" ]; then
            cp "{{COMPONENT_PREFIX}}Secrets.xcconfig.example" "{{COMPONENT_PREFIX}}Secrets.xcconfig"
          fi

      - name: Clean stale build intermediates
        run: |
          # Gitignored DerivedData persists between runs on the dedicated
          # runner. Stale .o files from a prior failed/interrupted build cause
          # Swift incremental compilation crashes (exit 65).
          rm -rf {{COMPONENT_PREFIX}}DerivedData/Build

      - name: Install xcpretty
        run: |
          gem install xcpretty -v 0.4.1 --user-install --no-document
          echo "XCPRETTY=$(ruby -e 'puts File.join(Gem.user_dir, "bin", "xcpretty")')" >> $GITHUB_ENV

      - name: Build + Test (macOS)
        id: tests
        timeout-minutes: 12
        run: |
          set -o pipefail
          rm -rf TestResults-macos.xcresult

          EXIT_CODE=0
          xcodebuild test \
            -project "{{XCODEPROJ}}" \
            -scheme <YourMacOSScheme> \
            -destination 'platform=macOS' \
            -derivedDataPath {{COMPONENT_PREFIX}}DerivedData \
            -only-testing:<YourMacOSTestTarget> \
            -parallel-testing-enabled NO \
            -resultBundlePath TestResults-macos.xcresult \
            CODE_SIGNING_ALLOWED=NO \
            CODE_SIGNING_REQUIRED=NO \
          2>&1 | tee xcodebuild-macos.log | $XCPRETTY --color --test || EXIT_CODE=$?

          # Exit code 65 is a known spurious Swift Testing failure. Confirm via
          # xcresulttool before trusting it — never assume pass on a code we
          # can't explain.
          if [ $EXIT_CODE -eq 65 ]; then
            if [ ! -d "TestResults-macos.xcresult" ]; then
              echo "::error::No test results found — tests may not have run"
              grep -iE 'error:|fatal|failed|ld:|actool|CodeSign' xcodebuild-macos.log | tail -60
              exit 1
            fi
            # Modern `get test-results summary`. The legacy `get --format json`
            # form this recipe used is refused by current Xcode ("--legacy flag
            # is required"), so XCRESULT_JSON came back empty, ALL_SUCCEEDED was
            # always "false", and every spurious exit-65 was reported as a
            # failure — fail-closed, but it defeated the entire point of the
            # workaround. ios-ci.yml had the same call in a fail-OPEN position;
            # see its "Run Tests" step.
            set +e
            SUMMARY_JSON=$(xcrun xcresulttool get test-results summary --path TestResults-macos.xcresult 2>/dev/null)
            SUMMARY_EXIT=$?
            set -e
            RESULT=$(echo "$SUMMARY_JSON" | jq -r '.result // empty' 2>/dev/null)
            FAILED_COUNT=$(echo "$SUMMARY_JSON" | jq -r '.failedTests // empty' 2>/dev/null)
            if [ $SUMMARY_EXIT -eq 0 ] && [ "$RESULT" = "Passed" ] && [ "$FAILED_COUNT" = "0" ]; then
              echo "All tests passed (0 failed). Exit code 65 was spurious."
              exit 0
            fi
            echo "::error::Test failures detected via xcresult (or inconclusive: exit=$SUMMARY_EXIT result=$RESULT failed=$FAILED_COUNT)"
            grep -iE 'error:|fatal|failed|ld:|actool|CodeSign' xcodebuild-macos.log | tail -60
            exit 65
          elif [ $EXIT_CODE -ne 0 ]; then
            echo "::error::xcodebuild failed with exit code $EXIT_CODE — raw tail:"
            grep -iE 'error:|fatal|failed|ld:|actool|CodeSign' xcodebuild-macos.log | tail -60
            exit $EXIT_CODE
          fi

      - name: Upload Test Results
        uses: actions/upload-artifact@v7.0.1
        if: always()
        continue-on-error: true
        with:
          name: macos-test-results
          path: TestResults-macos.xcresult
          if-no-files-found: ignore
          retention-days: 1
```

Then add `macos` to the `ci-ok` job's `needs:` list so it's part of the
single required check, not a separate unenforced job.

The source implementation this recipe is adapted from also validates its SPM
cache for corruption (a cache saved mid-download from a cancelled run can be
missing inner `.framework` bundles inside an `.xcframework`) before trusting
a cache hit — worth adding if you keep `actions/cache` for SPM on this job
(see the SPM-cache note in the macOS-only recipe above; the same open
question applies here).

### Living with a hand-edited managed file

`ios-ci.yml` is a lacquer-managed asset — normally synced verbatim. Adding a
job to your own copy means `lacquer audit` will show it as
`locally-modified` from then on, and a plain `lacquer sync` will refuse to
overwrite it (the clobber guard) rather than silently dropping your job.
When you want to pull in a lacquer update to the rest of the file, either
re-apply the `macos` job after `sync --force`, or promote this pattern into
the lacquer properly once a third project needs it (see
`skill-authoring-standard`'s placement guidance) so it stops being a
per-project patch.
