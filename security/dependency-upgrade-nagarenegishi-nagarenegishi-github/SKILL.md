---
name: dependency-upgrade
description: >
  Upgrade outdated dependencies one package at a time, with a changelog check
  for breaking changes and a test run between upgrades. Invoke with
  /dependency-upgrade; pass package names to limit scope.
disable-model-invocation: true
---

# Dependency Upgrade

Walk outdated dependencies up to current versions without breaking the project: one package at a time, tests between every step, stop on the first failure.

Upgrade workflow only. Vulnerability detection belongs to the `owasp-*` skills; do not scan for or report vulnerabilities beyond what the package manager prints on its own.

## Commands

<Fill in for this project's package manager(s). A project can have more than one, e.g. backend + frontend.>

- List outdated: `<outdated command, e.g. npm outdated, dotnet list package --outdated, pip list --outdated>`
- Upgrade one package: `<upgrade command, e.g. npm install <pkg>@<version>>`
- Test suite: `<test command>`

If these are still placeholders, detect the package manager from the project's manifest and lock files, take the test command from `CLAUDE.md`, and state the commands before using them.

## Workflow

1. **Survey.** Run the outdated-list command and show the result. If the user passed package names as arguments, limit the list to those. Propose an order: patch and minor bumps first, major bumps last, and within that, leaf dependencies before widely-used ones.
2. **Baseline.** Run the test suite once before the first upgrade. If it is not green, stop and report — a failure after an upgrade cannot be pinned on the upgrade otherwise.
3. **Per package, one at a time:**
   a. Read the changelog or release notes for the versions being jumped, looking specifically for breaking changes and migration steps. Check the package's repository or registry page.
   b. If the changelog cannot be fetched (container firewall may block registry and changelog domains), say which URL failed and continue with extra caution: prefer the smallest version step and rely on the test suite. Never silently skip the check.
   c. Apply the upgrade. If breaking changes require code updates, make them in the same step and say what was changed and why.
   d. Run the test suite.
   e. On green: report the package, old → new version, and any code changes, then move to the next package.
   f. On failure: stop the loop. Report which package broke what, with the failing output. Offer the options — fix forward, pin to an intermediate version, or revert this upgrade — and wait for the user's choice before touching the next package.
4. **Wrap up.** Summarize upgraded packages (old → new), skipped ones and why, and any that need a decision. Do not commit; suggest a commit message per coherent group of upgrades.

## Rules

- Never upgrade more than one package per test run. If two packages must move together (peer dependency), treat the pair as one step and say so. Transitive updates the package manager resolves along with the one package belong to that same step.
- Lock-file-only refreshes count as upgrades too: run the tests.
- If the test suite does not exist or cannot run, stop and report that upgrades cannot be verified — do not continue blind unless the user explicitly accepts the risk.
