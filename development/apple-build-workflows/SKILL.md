---
name: apple-build-workflows
description: "Create or repair reproducible Xcode and SwiftPM build, test, debug, and simulator workflows with explicit destinations, raw logs, safe tooling, and truthful evidence."
---

# Reproducible Apple build and debug workflows

## Inputs

Identify project/workspace or package, scheme, configuration, SDK, destination, repo-owned generators, source state, requested actions, and available command-line tools.

## Rules

- **BUILD-001 — Discover before executing.** Read local instructions and list real schemes and destinations. A remembered device identifier or default workspace is not evidence.
- **BUILD-002 — Keep one build contract.** Make wrappers call the same reviewed command used in CI. Preserve project generator ownership and inspect effective settings.
- **BUILD-003 — Preserve failure.** Capture raw tool output and exit status. A log formatter, screenshot command, or successful install must not hide a failed prerequisite.
- **BUILD-004 — Separate actions.** Build, test, install, launch, reset, sign, and publish have different effects. A plan must not silently execute them.
- **BUILD-005 — Trust tools explicitly.** Build scripts, package plugins, generators, debugger expressions, and downloaded helpers can execute code. Inspect provenance and obtain scope before running untrusted content.

## Workflow

1. Resolve the actual build graph and record the toolchain.
2. Produce a command plan; state filesystem, device, network, and account effects.
3. Run only the authorized phase and retain structured results plus raw output.
4. Classify failures before changing source and repeat the affected phase against the final candidate.

## Verify

Check spaces in paths, missing tools, wrong destinations, failed tests, formatter failure, and fresh-clone behavior. Verify a wrapper returns the underlying failure.

## Output

Return reproducible commands, candidate identity, exit results, artifacts, and the strongest supported claim; list skipped destination gates.

## References

- [Bootstrap, CLI, and debugger contract](references/bootstrap-and-cli.md).
