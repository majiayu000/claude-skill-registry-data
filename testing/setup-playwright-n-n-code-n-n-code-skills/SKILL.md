---
name: setup-playwright
description: Use when adding, extending, or repairing a repo-owned Playwright test harness across Node Playwright Test, Playwright Pytest, or .NET/Java test frameworks. Also use when explicitly persisting `@playwright/cli` developer tooling, or adding or regenerating Playwright Test Agent definitions for a compatible Node Playwright Test harness. Not for live CLI exploration or ordinary spec work in a working harness; use `playwright-testing`.
---

# Setup Playwright

Build the smallest reliable repo-owned Playwright setup that fits the
repository's language, package boundaries, test runner, developer-tool, and CI
conventions.

This is a system skill: it leaves behind a repo-owned harness or an explicitly
requested Playwright developer-tool artifact. Day-to-day test authoring and
live browser investigation belong to `playwright-testing`.

## Ownership Boundary

Use this skill when the main artifact is one or more of:

- Playwright dependencies or browser binaries
- runner config, package placement, or monorepo wiring
- app startup through `webServer` or an ecosystem-native equivalent
- browser, device, environment, retry, reporter, or artifact configuration
- reusable-auth setup and ignored state files
- a minimal smoke check that proves the harness works
- CI install, smoke, sharding, or report-merge plumbing
- an explicitly requested repo-owned `@playwright/cli` developer dependency or
  script
- host-targeted Playwright Test Agent definitions for a compatible Node
  Playwright Test harness

Use `playwright-testing` when the harness works and the task is a spec, test
review, flake diagnosis, locator change, mock decision, visual check, or
standalone `playwright-cli` investigation. If an environment-dependent install,
startup, container, or CI failure has no established cause, start with
`project-platform-diagnose` and return here once the repair is known.

## Choose The Existing Ecosystem

Follow the strongest repository signal:

- Node/TypeScript/JavaScript: `@playwright/test` unless another runner is
  already intentional.
- Python with pytest: the official Playwright Pytest plugin and pytest-native
  fixtures/config.
- .NET: the repo's MSTest, NUnit, xUnit, or xUnit v3 project and Playwright .NET
  integration.
- Java: the repo's JUnit or TestNG module with its Maven or Gradle build.

Do not create a Node sidecar in a Python, .NET, or Java repo merely because its
examples are more familiar. Load
[references/ecosystem-patterns.md](references/ecosystem-patterns.md) before
editing a non-Node harness.

If multiple ecosystems are equally plausible and package ownership cannot be
derived from the repo, ask before adding dependencies.

## Repo-Owned CLI Tooling

Use this lane only when the user explicitly wants Playwright CLI tooling
persisted in the repository. Agent-side investigation alone belongs to
`playwright-testing` and does not justify a dependency.

1. Inspect package ownership, the installed command surface, and whether the
   repo's existing Playwright version already exposes `npx playwright cli`.
2. Record the existing runner and CLI package versions, dependency resolution,
   lockfile state, and browser-command ownership before changing dependencies.
3. If standalone `@playwright/cli` is still wanted, add it only as developer
   tooling under the repo's version and lockfile policy.
4. Compare dependency resolution afterward and verify both the existing runner
   and the persisted CLI command. Do not upgrade or align a stable
   `@playwright/test` harness to an alpha Playwright dependency pulled by the
   CLI. If the package manager cannot keep the surfaces compatible, report the
   conflict instead of forcing installation.
5. Report the before/after versions, lockfile impact, commands verified, and
   any browser-download or update commitment introduced.

## Playwright Test Agent Extension

Treat Playwright Test Agents as a Node Playwright Test harness extension, not
as standalone generic agent tooling.

1. Inspect the worktree and existing agent definitions, then require a
   compatible Node Playwright Test harness and an explicit target host or
   `--loop` value supported by the installed `init-agents` command. Identify an
   existing seed when the repo has one and check the installed version's
   default-seed behavior when it does not.
2. If the harness or target host is missing, do not generate unusable
   definitions. Use the Harness Workflow only when the request authorizes that
   additional setup; otherwise report the missing prerequisite. A missing seed
   alone is not a blocker: the current planner can create a default. Prefer an
   explicit seed when custom fixtures, hooks, project dependencies, or startup
   make that bootstrap contract material. Do not create a Node sidecar in a
   Python, .NET, or Java repo solely to enable Test Agents.
3. Generate only the requested host definitions using current runtime help.
   Review the complete diff and preserve the documented regeneration path
   rather than casually hand-editing generated files.
4. Validate agent-file discovery and the existing or generated seed's
   compatibility with the active config, fixtures, project dependencies,
   hooks, and startup contract. Do not claim operational success when required
   app access, accounts, or secrets were unavailable.
5. `setup-playwright` owns generation, placement, version compatibility, and
   regeneration. Add `prompt-engineering` only when the user asks to evaluate
   or change agent instructions, tool boundaries, or prompt behavior, not for
   routine generation or structural diff review. Do not add
   `agent-skill-generator` merely because the artifacts are called agents; they
   are not reusable `SKILL.md` packages.

If a CLI or Test Agent request also changes the test harness, use the Harness
Workflow for that portion.

## Harness Workflow

1. **Inspect before installing.** Read repository instructions, package and
   lock files, test projects, existing Playwright artifacts, scripts, ignore
   rules, app startup commands, ports, and CI workflows. Check the installed
   version before relying on current flags or config fields.
2. **Define the harness contract.** Name the owning package, runner, target URL,
   startup owner, browser scope, auth strategy, output paths, local command, and
   CI command. Distinguish a broken harness from an environment-only failure.
3. **Make the smallest coherent change.** Use the repo's package manager and
   pinning policy. Install only required browsers. Preserve existing config and
   scripts; do not run a scaffold over a non-trivial harness blindly.
4. **Configure for local and CI use.** Set base URL/startup, projects or runner
   equivalents, timeouts, retries, workers, reporters, and artifacts only when
   the repository needs them. Prefer project dependencies over Node
   `globalSetup` when setup should be visible and traceable in the runner.
5. **Wire auth deliberately.** Use UI login, API login, or per-worker accounts
   according to the claim and mutation model. Verify authentication succeeded
   before saving state. Ignore saved state and treat it as a credential.
6. **Add one meaningful smoke check.** Prove that startup, navigation, locator,
   assertion, browser binary, and output path cooperate. Keep broader product
   coverage for `playwright-testing`.
7. **Validate in layers.** Verify config/listing first, run one smoke target,
   repeat if the repair involved state or startup, then run the smallest
   relevant CI-shaped command. Inspect generated output rather than assuming
   command success proves correct placement.
8. **Report exact evidence.** State changed files, commands and results,
   browsers not installed or run, CI not executed, secrets required, and any
   remaining environment assumptions.

## Setup Rules

- Preserve package-manager and lockfile ownership. Do not mix npm, pnpm, yarn,
  Python managers, NuGet conventions, Maven, or Gradle without repo evidence.
- Keep Playwright package and browser binaries aligned. Install the smallest
  browser set that proves the stated matrix; broader defaults must be an
  explicit choice.
- Prefer one clear config owner per package. Reuse existing test and artifact
  directories unless relocation is part of the request.
- Keep local server reuse local; CI should start from a controlled build and
  process. Use a readiness URL and a startup timeout that reflects app boot,
  not an inflated global test timeout.
- Default CI concurrency conservatively when shared state is not proven safe.
  Add parallelism or sharding only with an isolation model and report merging.
- Configure traces, screenshots, or video for actionable failure evidence,
  while controlling retention and excluding secrets.
- Use a Node setup project for reusable auth when applicable. In other
  ecosystems, preserve native fixtures/helpers instead of inventing
  `auth.setup.ts`, project dependencies, or `test.use()`.
- Saved browser state may contain cookies, tokens, IndexedDB data, and—in newer
  versions when requested—credential material. Keep it ignored and out of
  logs/artifacts unless explicitly sanitized.
- `storageState` does not persist `sessionStorage`; wire a deliberate restore
  only when the application requires it.
- Test generated config against the installed version. Features such as
  isolated retry strategies, credential-state capture, component-test models,
  and bundled CLI commands are version-sensitive.

## Tooling Boundaries

- `playwright-cli` and Playwright's installable CLI skill are agent-side
  exploration aids, not automatically repo dependencies. Do not add a local
  third Playwright skill or a production dependency merely to run an agent
  investigation.
- Component testing, browser extensions, WebView2, and raw Playwright library
  automation use different lifecycle/config models. Treat them as specialized
  setups rather than silently applying the default web E2E template.

## Harness Validation Evidence

Choose commands from the active ecosystem and existing scripts. Typical Node
layers are:

```console
npx playwright --version
npx playwright test --list
npx playwright test <smoke-target> --project=<project>
```

For Python, .NET, and Java, use the native runner and browser-install commands
from [references/ecosystem-patterns.md](references/ecosystem-patterns.md).
Validate command availability against the installed version rather than
copying a current-doc flag into an older harness.

Resource execution and test execution are separate evidence: a valid config
does not prove browsers are installed, and a passing smoke does not prove every
browser, shard, or CI environment. Repo-owned CLI and Test Agent validation are
defined in their lanes above; do not substitute unrelated harness commands.

## Reference Map

- [references/ecosystem-patterns.md](references/ecosystem-patterns.md) —
  package, runner, install, and auth boundaries across Node, Python, .NET, and
  Java.
- [references/browser-and-config-patterns.md](references/browser-and-config-patterns.md)
  — Node config scope, projects, browsers, reporters, timeouts, `webServer`,
  and specialized modes.
- [references/auth-and-ci-patterns.md](references/auth-and-ci-patterns.md) —
  Node setup-project auth, API login, worker accounts, CI, and sharded reports.
- [references/pressure-tests.md](references/pressure-tests.md) — shortcut
  rationalizations and expected responses; load only when those pressures are
  present or when maintaining the skill.

For maintainer provenance and routing fixtures, use
[references/coverage-and-validation.md](references/coverage-and-validation.md).
