---
name: ceedling-build-runner
description: "Author and run the Ceedling build system for C unit testing - the canonical build orchestration on top of Unity (assertions) + CMock (mocks) + CException (exceptions). Covers ceedling new scaffolding, the project.yml schema (:project / :paths / :files / :defines / :flags / :tools / :test_runner / :cmock / :unity / :cexception / :gcov / :plugins), the task surface (test:all, test:{name}, test:pattern, test:path, release, clean / clobber, gcov:all, module:create, environment, dumpconfig), JUnit XML via the report_tests_* plugins, gcov integration, host vs cross-build flow, and CI wiring. CMock semantics - the generated Expect / Ignore / IgnoreArg / ReturnThruPtr / AddCallback / Stub / ExpectAndThrow family, cmock.yml :plugins, mock naming, tearDown verification, strict-vs-ignore matching - are in references/cmock.md. Use when a C project wants the ThrowTheSwitch trio bundled by one build command, or when authoring / reading CMock mocks. For the Unity assertion API see unity-test-framework-c."
metadata:
  keywords: "ceedling, unity, cmock, cexception, c, embedded, rake, throwtheswitch"
  version: "1.3.10"
---

# ceedling-build-runner

## Overview

This skill covers the Ceedling build orchestration - the
`ceedling` command-line tool, `project.yml` schema, and rake
tasks, per
[throwtheswitch.org/ceedling](https://www.throwtheswitch.org/ceedling).
For the Unity assertion API see `unity-test-framework-c`; for
CMock's generated mock API see [references/cmock.md](references/cmock.md);
for cross-target run see `qemu-system-test-runner`; for coverage see
`embedded-coverage-strategy-reference`.

## When to use

- C unit-test project - Ceedling is the canonical setup for the
  ThrowTheSwitch stack.
- Host-build-driven test loop (most embedded teams test on the
  host first, then cross-compile under
  `qemu-system-test-runner`) - Ceedling handles the host pipeline natively.
- Coverage required - the bundled gcov plugin produces LCOV /
  HTML / Cobertura without external glue.
- Mock-heavy module - CMock is integrated; no separate generator
  invocation needed.

If the unit-under-test is C++ instead of C, prefer
`googletest-embedded-arm`;
Ceedling does not target C++.

## Authoring

### Scaffolding a new project

Per the Ceedling README and the command-line reference at
[github.com/ThrowTheSwitch/Ceedling/.../getting-started/command-line.md](https://github.com/ThrowTheSwitch/Ceedling/blob/master/docs/mkdocs/getting-started/command-line.md):

```bash
gem install ceedling
ceedling new my-firmware --docs --local
cd my-firmware
```

`--docs` includes the documentation locally; `--local` vendors
Unity / CMock / CException into `vendor/ceedling/` so the build
doesn't need network at compile time. The generated layout:

```
my-firmware/
  project.yml          # the schema covered below
  src/                 # production code under test
  test/                # one test_<module>.c per module
  test/support/        # shared test helpers
  build/               # generated; gitignore'd
  vendor/ceedling/     # bundled Unity + CMock + CException
```

### project.yml

A minimal project.yml for a host test loop:

```yaml
:project:
  :build_root: build/
  :use_mocks: TRUE
  :test_file_prefix: test_
:paths:
  :test:
    - test/**
  :source:
    - src/**
  :include:
    - inc/**
:plugins:
  :enabled:
    - report_tests_pretty_stdout
    - report_tests_junit_xml
    - gcov
```

The full schema (every top-level section, test vs release
`:flags`, the `:cmock` / `:cexception` / `:gcov` blocks, per-section
notes, and the plugin list) is in
[references/project-yml-schema.md](references/project-yml-schema.md).

### Creating a module

```bash
ceedling module:create[ringbuffer]
# Creates src/ringbuffer.c, src/ringbuffer.h, test/test_ringbuffer.c
```

The generator emits the canonical skeleton - production header /
source with includes wired, test file with `setUp` / `tearDown` /
one `test_ringbuffer_NeedToImplement` placeholder.

## Running

```bash
ceedling test:all         # Run every test_*.c
ceedling test:ringbuffer  # Run only test_ringbuffer.c
ceedling gcov:all         # Run under gcov instrumentation + generate report
```

`ceedling test:all` returns non-zero on any test failure; CI
gates on the exit code. `gcov:all` writes
`build/artifacts/gcov/GcovCoverageResults.html` (HtmlDetailed) or
`GcovCoverageCobertura.xml` (Cobertura) - see
`embedded-coverage-strategy-reference`.

The canonical CI invocation chains tasks on one command line:

```bash
ceedling clobber test:all release gcov:all
# Clean -> run tests -> build release -> produce coverage report
```

The full task surface (`test:pattern`, `test:path`,
`--test-case`, `release`, `clean` / `clobber`, `environment`,
`dumpconfig`) is in
[references/task-reference.md](references/task-reference.md).

## Parsing results

### Pretty stdout output

```
-------------------
OVERALL TEST SUMMARY
-------------------
TESTED:  47
PASSED:  46
FAILED:   1
IGNORED:  0
```

Failures are reported per assertion with file:line:test:reason:

```
test/test_ringbuffer.c:48:test_overflow_returns_minus_one:FAIL: Expected -1 Was 0
```

### JUnit XML

With `report_tests_junit_xml` enabled, `ceedling test:all` writes
`build/artifacts/test/report.xml` in the canonical JUnit schema - 
the same one GoogleTest produces, so the same CI pipeline plugin
(GitHub `mikepenz/action-junit-report`, GitLab JUnit, Jenkins
JUnit) consumes both.

## CI integration

```yaml
jobs:
  ceedling-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Setup Ruby + Ceedling
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
      - run: gem install ceedling
      - name: Run tests + coverage
        run: ceedling clobber test:all gcov:all
      - name: Publish JUnit
        if: always()
        uses: mikepenz/action-junit-report@v4
        with:
          report_paths: 'build/artifacts/test/*.xml'
      - name: Publish coverage
        uses: codecov/codecov-action@v5
        with:
          files: build/artifacts/gcov/GcovCoverageCobertura.xml
```

For a cross-compile path (host build for CI, ARM build for
hardware-in-loop) the recipe is: keep two `project.yml` files
(`project.yml` for host, `project-arm.yml` for ARM) and pass
`--project=project-arm.yml` for the ARM build. The ARM build's
`:tools:` overrides the compiler to `arm-none-eabi-gcc` and the
results route through `qemu-system-test-runner`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Editing the generated `*_Runner.c` files | Regenerated on every build; edits lost | Edit the source `test_*.c`; the runner is derived |
| `:enforce_strict_ordering: FALSE` to "make tests pass" | Mock-call-order bugs become invisible | Keep `:enforce_strict_ordering: TRUE`; fix the SUT's call shape |
| Commit `build/` artifacts | Repo bloat; merges conflict on generated files | `.gitignore build/` always |
| Skipping `ceedling clobber` in CI | Stale mocks survive header changes; ghost test failures | Always `clobber` before the CI run |
| Mixing test compile flags with release flags | `--coverage` in release build inflates the binary | Keep `:flags: :test:` separate from `:flags: :release:` |
| Naming a test file `_test.c` instead of `test_*.c` | Default `:test_file_prefix: test_` won't pick it up | Match the prefix or change the project.yml setting |
| Using `:use_mocks: FALSE` then including a `Mock*.h` | CMock isn't invoked; link fails on the mock symbol | Either enable mocks globally or use Ceedling's `--mocks` runtime flag |
| Hardcoding the build directory in scripts | `:build_root` is project.yml-driven; scripts break on rename | Read it from `ceedling environment` |

## Limitations

- **Ruby dependency.** Ceedling runs on Ruby; embedded teams
  without a Ruby toolchain have an adoption cost.
- **C only.** No C++ support - for C++ pair
  `googletest-embedded-arm`
  with CMake.
- **Per-file flag overrides are verbose.** The `:flags` schema's
  glob keys are powerful but error-prone - `dumpconfig` is the
  only reliable verifier.
- **No native parallel test execution.** Each `test_*` runs
  serially. Parallelise across multiple `test:path[...]` jobs in
  CI if needed.
- **Plugin discovery is path-sensitive.** Custom plugins must
  live under `:plugins: :load_paths:` in project.yml. Ceedling's
  error messages on missing plugins are terse.
- **gcov plugin reports are coupled to host-built coverage.**
  For on-target coverage, write a custom plugin or feed gcovr
  manually after a QEMU run.

## References

Cited inline. Foundational documents:

- Ceedling repository - [github.com/ThrowTheSwitch/Ceedling](https://github.com/ThrowTheSwitch/Ceedling).
- Ceedling overview - [www.throwtheswitch.org/ceedling](https://www.throwtheswitch.org/ceedling).
- Ceedling docs (project.yml + task reference) - [throwtheswitch.github.io/Ceedling/latest](https://throwtheswitch.github.io/Ceedling/latest/).
- CMock semantics (generated API surface, cmock.yml plugins,
  lifecycle, matching modes): [references/cmock.md](references/cmock.md).
- Sibling skills:
  `unity-test-framework-c`,
  `embedded-coverage-strategy-reference`,
  `qemu-system-test-runner`,
  `googletest-embedded-arm`.
