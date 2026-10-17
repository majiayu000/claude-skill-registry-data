---
name: test-discovery
description: Explains the prescribed __test__/ directory layout, test file naming conventions, and how source coverage is derived from the adjacent src/ folder.
paths:
  - "**/__test__/**/*"
  - "**/__fixtures__/**/*"
  - "**/__snapshots__/**/*"
---

# Test Layout — `__test__/` Conventions

Projects using this layout place tests in a `__test__/` directory that sits adjacent to `src/`. Coverage is calculated from that `src/` directory. Auto-discovery tools (like `AgentPlugin.discover()`) may generate Vitest projects from this structure automatically, but custom project configurations are also possible.

```text
<project-root>/
├── src/            source code — coverage is calculated from here
└── __test__/       tests and test support files
```

Discovery recognises these two locations and no others. A `__test__/` directory anywhere else in the package tree — `lib/scripts/__test__/`, for example — is not a valid test location: Vitest will not collect it, and the tests inside it will never run. The walker also stops at a nested `package.json` boundary, so a sibling package's tests are never double-counted in a monorepo scan.

## `__test__/` Directory Structure

Test files sit flat at the top level of `__test__/`; helper files go in reserved subdirectories organised by test kind.

```text
__test__/
├── *.test.ts | *.unit.test.ts  unit test files
├── fixtures/                   static files needed by unit tests
├── snapshots/                  Vitest snapshot files for unit tests
├── utils/                      shared helpers for unit tests
├── integration/
│   ├── *.int.test.ts           integration test files
│   ├── fixtures/               static files needed by integration tests
│   ├── snapshots/              Vitest snapshot files for integration tests
│   └── utils/                  shared helpers for integration tests
└── e2e/
    ├── *.e2e.test.ts           e2e test files
    ├── fixtures/               static files needed by e2e tests
    ├── snapshots/              Vitest snapshot files for e2e tests
    └── utils/                  shared helpers for e2e tests
```

## Subdirectory Rules

| Subdirectory | Coverage | Lint | Typecheck | Purpose |
| --- | :---: | :---: | :---: | --- |
| `fixtures/` | excluded | excluded | excluded | Static files consumed by tests (JSON, TOML, binary, etc.) |
| `snapshots/` | excluded | excluded | excluded | Vitest snapshot output (managed automatically) |
| `utils/` | excluded | required | required | Shared helpers — mocks, extended `expect`, shared types |

Fixtures and snapshots are fully excluded; place arbitrary static content there without concern for linting or types. Utils files must be valid TypeScript and pass the linter — treat them as first-class support code, just not counted toward coverage.

These three columns describe coverage, linting, and typechecking — not Vitest
discovery, which is a separate mechanism. Discovery only ever collects
`*.test.ts` files, so a helper in any of these directories is never collected
wherever it sits. What discovery does exclude is a *test* file under a helper
directory named directly beneath `__test__/` — `__test__/utils/a.test.ts` is
not collected, while `__test__/integration/utils/a.test.ts` is an ordinary
suite. That boundary is anchored at the test root deliberately: matching the
helper name at any depth silently swallowed real suites (issue #251).

## Escape Hatch — `__fixtures__` and `__snapshots__` Anywhere

Directories named `__fixtures__` or `__snapshots__` (double-underscore wrapping) are recognised and excluded from coverage, linting, and typechecking wherever they appear inside a project — not just under `__test__/`. This can be useful when a fixture needs to live close to the source file it supports.

Prefer the prescribed locations (`__test__/fixtures/`, `__test__/integration/fixtures/`, etc.) over this escape hatch. Scattering `__fixtures__` directories through `src/` makes test support files harder to find and the project harder to navigate.

## Test File Classification

The scanner classifies files by suffix; first match wins:

| Suffix | Kind | Lives in |
| --- | --- | --- |
| `*.e2e.test.ts` | e2e | `__test__/e2e/` |
| `*.int.test.ts` | int | `__test__/integration/` |
| `*.test.ts` or `*.unit.test.ts` | unit | `__test__/` (top level) |

## Limitation — the PreToolUse Hook Only Knows the Default Layout

The `test-location.sh` PreToolUse hook and its backing `vitest-agent agent
check-test-path` CLI subcommand classify a test path against the **default**
layout described above — `classifyTestPath` is purely lexical and never loads
a project's actual Vitest config. Most workspaces use the default layout
`AgentPlugin.discover()` produces, so this is right almost always. It is
**not** aware of a consumer who changes discovery via:

- a custom `discoverStrategy` passed to `AgentPlugin({ discoverStrategy })`
  (including `discoverStrategy: false` to disable discovery entirely),
- `AgentPlugin.discover().addProject({ name, path })` registering a
  non-package folder as an extra project, or
- a class extending `DefaultDiscoverStrategy` / implementing
  `DiscoverStrategy` directly.

For such a workspace, the default-layout rule can be wrong about a path the
consumer's actual config collects fine. Because a denial is the strongest
action the hook can take, `check-test-path` **fails open** (exits 1 with no
stdout — the hook then no-ops) whenever it detects one of those markers in
the workspace's `vitest.config.*` / `vitest.workspace.*` / `vite.config.*`
source text, or whenever that config file cannot be found or read at all. A
missing or unreadable config is treated exactly like a detected marker: no
verdict is safer than a confidently wrong one. The detector
(`detectNonDefaultDiscoverStrategy` in `@vitest-agent/sdk`) is a lexical scan
with a best-effort comment strip, so a marker string that only appears inside
a comment can still register as a false positive — that direction (failing
open) is the safe one, so it is accepted rather than built out further.

If you hit a wrong deny anyway — or just want the check off — set
`VITEST_AGENT_TEST_LOCATION_HOOK=off` (`0` and `false` also work) in your
environment. The hook checks this before doing anything else and emits a
silent noop without ever invoking the CLI.
