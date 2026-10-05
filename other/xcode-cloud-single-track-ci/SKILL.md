---
name: xcode-cloud-single-track-ci
description: 'Use when setting up or changing CI for an Apple-platform project on Xcode Cloud — choosing Xcode Cloud vs GitHub Actions, splitting PR / Main / Release / scheduled workflows, writing `ci_scripts/ci_post_clone.sh` / `ci_pre_xcodebuild.sh` / `ci_post_xcodebuild.sh`, or wiring `CI_BUILD_NUMBER`, `MARKETING_VERSION`, `agvtool` numbering. Or asked "do I need dual-track CI", "main failed after the PR passed", "Xcode Cloud build number collides". Does NOT cover shipping a build by hand when Xcode Cloud is down → local-archive-export-upload, nor ASC REST calls after upload → asc-api-automation.'
---

# Xcode Cloud Single-Track CI

## When to invoke

- Starting a new Apple-platform project and setting up CI.
- Deciding between GitHub Actions and Xcode Cloud.
- Writing `ci_scripts/ci_post_clone.sh` / `ci_pre_xcodebuild.sh` / `ci_post_xcodebuild.sh`.
- Bumping the Xcode version and handling snapshot baselines.
- User asks "how to split PR / Main / Release workflow", "auto-upload to TestFlight or not".

## Default decisions

### Single-track on Xcode Cloud

- **GitHub Actions is not enabled yet** — wait for real pain (PR metadata rules, external lint jobs, Selective Testing, etc.) to appear.
- The repo is hosted on GitHub, but CI runs on Xcode Cloud.

### 4 workflows

| Workflow | Trigger | Action |
|---|---|---|
| **PR CI** | PR open / push — Pull Request Changes start condition (Xcode Cloud merges the PR with the target branch before building) | Build + Test (unit / integration with fakes / snapshot) |
| **Main CI** | Merge to `main` | Build + Archive + upload to internal TestFlight; **do not re-run tests** (already verified by PR CI in pre-merged state) |
| **Release** | git tag `v*` | Build + upload to App Store Connect (manual submission for review) |
| **Periodic / Manual** | Scheduled + manual trigger | Project-specific batch jobs (nightly export, metadata updates, etc.) |

> **Scheduling granularity caveat**: Xcode Cloud's "On a Schedule" start condition lets you specify the frequency, time, and branch (Apple's own example: "every business day at 10:00 p.m."); it does not expose arbitrary cron expressions. For a cadence the frequency picker can't express directly (e.g. monthly), pick the closest supported frequency and add a script-side date guard inside `ci_post_clone.sh` that early-exits when the date doesn't match the desired condition.

### Environment lock

- Xcode version in the workflow matches the README / `foundations.md` toolchain line.
- When bumping Xcode, open a dedicated PR to refresh snapshot baselines.
- **Xcode Cloud's build environment does not include mise** — Apple documents it as including only Homebrew among third-party tools. Commit a bootstrapped `bin/mise` wrapper (`mise generate install-script --localize --write bin/mise`, from `mise-tool-management` — requires mise ≥ 2026.8.11; on older mise run `mise self-update`, or use the old `mise generate bootstrap --localize --write bin/mise`, which newer mise keeps as a deprecated alias with removal planned for mise 2027.9.0) and call every tool inside `ci_scripts/` through it (`./bin/mise trust`, `./bin/mise install`, `./bin/mise exec -- <tool> <args>`) instead of a bare `mise` invocation, which fails with "command not found".
- Test environment disables iCloud / Game Center sign-in; all tests go through protocol fakes.

### Build number & version automation

| Need | Setting / source | Where it's set | Action |
|---|---|---|---|
| User-visible version | `MARKETING_VERSION` (→ `CFBundleShortVersionString`) | Project build settings | Bump deliberately per release |
| Build number, new **iOS** app | `CI_BUILD_NUMBER` | Xcode Cloud (sequential integer per build, starting at `1`, independent of `CURRENT_PROJECT_VERSION`) | Nothing — a version+build pair lower than a prior manually-numbered build is still valid on iOS, even though Apple's docs call that same pattern *invalid* for a Mac app (see next row; worked example: `references/official-docs.md`) |
| Build number, existing Mac app with a prior higher build | ASC's Xcode Cloud build-number counter | App Store Connect → app → **Xcode Cloud** tab → **Settings** → **Build Number** tab → **Edit** | Set the next build number above your last shipped one (macOS requires the build number to strictly increase *across* versions, not just be unique within one) |
| Binary must carry the CI build number (e.g. crash-symbolication tooling that reads `CURRENT_PROJECT_VERSION`) | `agvtool new-version -all "$CI_BUILD_NUMBER"` in `ci_post_clone.sh` | Repo | Requires `VERSIONING_SYSTEM = apple-generic` (agvtool enabled) on the target |

Release tooling that mints `versionString` for the ASC API (→ `asc-api-automation`) should read this project's `MARKETING_VERSION` rather than track a second version counter — one SemVer source of truth.

### Three Xcode Cloud hooks

Apple provides:
- `ci_post_clone.sh` — runs right after clone, before any build resources are spent (**secret scan, the `bin/mise` bootstrap go here, cheapest stage**)
- `ci_pre_xcodebuild.sh` — before build
- `ci_post_xcodebuild.sh` — after build

Minimal `ci_post_clone.sh`, using the committed `bin/mise` wrapper (see Environment lock above):

```sh
#!/bin/sh
set -eu
cd "$CI_PRIMARY_REPOSITORY_PATH"
./bin/mise trust
./bin/mise install
./bin/mise exec -- swiftlint lint
```

## Rationale

- For solo / small teams, CI usage is light and Xcode Cloud's free quota is enough; dual-track adds ops cost with no matching value.
- PR CI with pre-merge fundamentally resolves the common "fails only after merge to main" race.
- Main CI skips re-running tests: PR already ran them in pre-merged state, so rerunning is waste; it archives and ships to TestFlight instead.
- Periodic workflow is built into Xcode Cloud (no separate cron service required).

## Deviation considerations

### When to add GitHub Actions

- PR metadata rules (conventional commits, PR title lint, auto-label / required reviewer)
- SwiftLint / SwiftFormat or other binary tools running on PR
- Docs link checks, changelog/index generation, or any job that is cheaper on a Linux runner
- Wiring up Selective Testing
- Using `nektos/act` to reproduce non-build jobs locally

Starting point: when one of the above real pain points appears, **add a single workflow first**, don't go dual-track in one shot.

### Known race condition

When two PRs each pass pre-merge and merge back to back, **their combined result was never tested**.
- Solo projects rarely hit this.
- Multi-person teams who care: enable GitHub's "Require branches to be up to date before merging", or add minimal smoke tests to Main CI.

## Verification checklist

- The Xcode version in the Xcode Cloud workflow matches the README / `foundations.md` toolchain line.
- PR CI uses the Pull Request Changes start condition (Xcode Cloud merges the PR with the target branch before building it).
- `bin/mise` is committed; `ci_post_clone.sh` starts with `cd "$CI_PRIMARY_REPOSITORY_PATH"`, then runs `./bin/mise trust && ./bin/mise install`, not a bare `mise` call.
- Periodic workflow trigger time is explicit (UTC recommended).
- Existing Mac apps: Xcode Cloud's next build number (App Store Connect → Xcode Cloud → Settings → Build Number) is set above the last shipped build number.

## Related skills

- `mise-tool-management`: `ci_scripts/` tools installed via mise.
- `swift-testing-baseline`: CI skips real-network integration tests.
- `apple-public-repo-security`: PR CI adds a gitleaks step as the second line of defence.
- `apple-platform-targets`: Xcode version lock.
- `asc-api-automation`: release-side `versionString` and changelog automation, once the build exists in ASC — reuses this project's `MARKETING_VERSION` / `CI_BUILD_NUMBER`.
- `local-archive-export-upload`: the manual fallback when Xcode Cloud is down or its quota is exhausted.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
