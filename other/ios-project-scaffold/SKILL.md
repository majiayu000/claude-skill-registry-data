---
name: ios-project-scaffold
description: "Scaffold a new iOS project with a pinned Xcode toolchain, Tuist manifest, repo-owned worktree execution helper, simprofile-driven simulator policy, Makefile targets for build/test/run/trace/release, Fastlane lanes for TestFlight and the App Store, and GitHub Actions workflows for CI. Also audits existing projects against the same conventions and reports drift with concrete fix commands. Use when the user asks to start or bootstrap an iOS app, set up Tuist and Makefile automation, add worktree-local simulator/build structure, or audit an iOS repo's scaffold and agent-facing build hygiene. Two modes: init for scaffolding, audit for checking drift."
---

# iOS Project Scaffold

Use this skill to create a new iOS project with a consistent local workflow or to check an existing project against that workflow. Choose `init` when creating the scaffold and `audit` when checking for drift.

The generated repo has one clear ownership contract:

- `make` is the public interface for local builds, tests, screenshots, cleanup, and trace collection.
- The repo-owned worktree helper manages simulators, ownership locks, and mutable state under `build/`.
- `Project.swift` defines targets, schemes, and suite metadata tags.
- `TestPlans/<App>.simprofile.toml` defines runtime classes and preferred devices only.
- `AGENTS.md` and the worktree runbook direct future agents to use the helper when it owns the requested state, instead of issuing freehand `xcodebuild`, `simctl`, `tuist`, or `fastlane` commands.
- Generated hooks stay fast: they may format staged files and run lightweight lint, but they do not run simulator tests, `xcodebuild`, or deep analysis.

## Init: scaffold a project

1. Run the scaffold script with the target directory, app name, bundle ID, and team ID:

   ```bash
   bash ~/.agents/plugins/plugins/ios/skills/ios-project-scaffold/scripts/scaffold.sh \
     --target /path/to/new/app \
     --name MyApp \
     --bundle-id com.example.MyApp \
     --team-id ABCD123456
   ```

2. Add `--with-analysis` when the project should include Periphery configuration and a `make analyze` target. The script also accepts `--force` to overwrite existing generated files.
3. In the generated project, follow the script's printed next steps: read `README.bootstrap.md`, run `git init`, then `make bootstrap-local`, `make generate`, `make build`, `make run-iphone`, and `make test-matrix`. The script creates the scaffold; it does not install Xcode.

The scaffold includes:

- Tool pins: `.xcode-version`, `.tuist-version`, `mise.toml`, and `.envrc`
- Tuist source of truth: `Project.swift` and `Tuist/Package.swift`
- Agent and test guidance: `AGENTS.md`, `docs/operations/runbooks/worktree-execution.md`, and `TestPlans/README.md`
- Runtime policy: `TestPlans/<App>.simprofile.toml`
- Helper-driven automation: `Makefile`, `scripts/<app>_worktree.py`, and `scripts/trace_execution.py`
- Local hygiene: `.swiftlint.yml`, `.swiftformat`, `.typos.toml`, and `.githooks/pre-commit`
- Release configuration: `fastlane/Fastfile`, `fastlane/Appfile`, and `fastlane/.env.example`
- CI workflows: `.github/workflows/ci.yml`, `.github/workflows/beta.yml`, and `.github/workflows/security.yml`
- A minimal SwiftUI app under `<App>/`

With `--with-analysis`, the scaffold also adds `.periphery.yml`, pins Periphery, and wires `make analyze`.

## Audit: check an existing project

1. Run the deterministic convention checks:

   ```bash
   bash ~/.agents/plugins/plugins/ios/skills/ios-project-scaffold/scripts/audit.sh --target /path/to/app
   ```

2. Add `--json` for machine-readable results:

   ```bash
   bash ~/.agents/plugins/plugins/ios/skills/ios-project-scaffold/scripts/audit.sh --target /path/to/app --json
   ```

3. Read the flagged files and assess the judgment calls below. Report concrete drift and applicable fix commands; the script's output alone does not assess these qualitative points.

The audit exits with `0` when all checks pass and `1` when at least one check fails.

## Audit judgment calls

### Repo contract

- Does `AGENTS.md` clearly identify `make` as the public command surface?
- Does the runbook explain ownership, simulator reuse, cleanup, and the `build/` artifact layout?
- Does the repo keep mutable generated state under `build/`, rather than `/tmp` or global DerivedData paths?

### `Project.swift` and Tuist

- Does `Project.swift` define shared schemes and suite topology directly, without depending on generated scheme edits?
- Do targets carry metadata tags for role, suite kind, runtime class, device support, and data mode?
- Is `Project.swift` the only place that encodes target and suite topology?
- Does `Tuist/Package.swift` include the external package dependencies expected by the manifest?

### Worktree helper

- Does the helper infer topology from `tuist dump project` and target metadata instead of handwritten lane maps?
- Does it own one reusable iPhone simulator and one reusable iPad simulator per worktree?
- Does it keep locks in `build/state/` and simulator metadata in `build/simulators/`?
- Does it expose `doctor-state`, `clean-build`, `clean-simulators`, `reset-simulators`, `release-owner`, and `clean`?

### Makefile

- Do `build`, `run`, `test-*`, `record-snapshots-*`, and screenshot targets use the helper?
- Does `generate` use the helper so ownership and state remain consistent?
- Does the Makefile consume helper-exported environment such as derived-data paths, simulator names, and result-bundle paths?
- Do build and test commands still flow through `xcbeautify`?
- Are grouped targets split by device family so an agent can intentionally run one lane?

### Simprofile

- Does `TestPlans/<App>.simprofile.toml` define runtime classes and preferred device identifiers only?
- Does it leave task names, suite topology, and scheme names to their source of truth?

### Local hygiene

- Is `.githooks/pre-commit` limited to staged-file operations?
- Does it avoid `xcodebuild`, simulator work, and deep analysis?
- Do `setup-tools` and `bootstrap-local` remain local-only rather than mixing in CI concerns?

### CI and release

- Does `ci.yml` run through `make` instead of hand-rolled `xcodebuild` commands?
- Do macOS jobs have `timeout-minutes`?
- Does `ci.yml` cancel stale runs while `beta.yml` preserves in-flight releases?
- Does the beta/TestFlight workflow use an approval-gated environment?

## References

Load the relevant reference when you need implementation details for that area:

- [Tuist](./references/tuist.md)
- [CI](./references/ci.md)
- [Release](./references/release.md)

## Requirements

The scaffold assumes Xcode 26.3 is installed and selected, with `xcodes`, `mise`, `jq`, and `perl` available. Run `make bootstrap-local` once after `git init`. Xcode installation is outside this skill's scope.

## Related skill

Use `ios-audit` for a broader engineering and UX audit. This skill checks scaffold and repo-hygiene conventions.

The scaffold does not create an App Store Connect app record, design product architecture or feature modules, define backend contracts, choose app design or HIG-specific UX, or replace project-specific release, secrets, and API workflows beyond the scaffold baseline.
