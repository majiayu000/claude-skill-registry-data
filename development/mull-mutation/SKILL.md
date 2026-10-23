---
name: mull-mutation
description: "Runs Mull, the LLVM-IR mutation testing tool, against C/C++ test binaries built with Clang: covers install (the version-matched mull-NN package), the -fpass-plugin build flags for the Mull IR frontend, mull-runner invocation, the mutator catalog, path filtering, and GitHub Actions CI. Use when a C or C++ project needs mutation-score verification with the tool already chosen. Does not select among mutation tools and does not cover other languages (stryker-mutation for JS/TS, stryker-net-mutation for .NET, pitest-mutation for the JVM, mutmut-mutation for Python)."
---

# mull-mutation

## Overview

Per [mull-readme][mr]:

[mr]: https://github.com/mull-project/mull

> "Mull is a practical mutation testing and fault injection tool
> for C and C++."

Per [mull-readme][mr], Mull is "LLVM-based" and "Built on LLVM IR
(Intermediate Representation) and utilizes LLVM JIT compilation."

The LLVM-IR foundation means Mull operates at a layer below the
source language - any LLVM-emitting frontend (Clang, Rust's
rustc, Swift's swiftc) can in principle work, though C / C++ are
the primary targets.

The foundational paper per [mull-readme][mr]: "Mull It Over:
Mutation Testing Based on LLVM" (2018), Denisov & Pankevich.

## When to use

- A C / C++ project needs mutation-quality verification of its
  test suite.
- A library shipping safety-critical code (embedded, kernel,
  cryptography) needs the highest-confidence test suite.
- Language ecosystems without a native mutation tool need an
  LLVM-IR-level fallback.

## Step 1 - Install

Latest release per [mull-changelog]: 0.34.0 (May 2026). Mull ships as a
version-matched package: `mull-19` bundles LLVM 19.1.7, and the suffix MUST
match the Clang you compile with (plugin / ABI compatibility), per
[mull-install].

```bash
# macOS / Linuxbrew
brew install mull-project/mull/mull

# Linux (Ubuntu/Debian): install the version-matched mull + clang packages
# from the Mull apt repo per the official guide: https://mull.readthedocs.io
```

## Step 2 - Build the project for mutation

Mull needs the test binary built with `-O0 -g` (no optimization,
debug symbols) and the Mull IR frontend, which current Mull loads as a
compiler plugin via `-fpass-plugin` (the old `-Xclang -load` legacy-pass
approach is gone), per [mull-tutorial]. The plugin path is version-suffixed
and must match the installed `mull-NN` package and the Clang version:

```bash
# CMake-based project. The "19" in the plugin path, the mull-19 package, and
# clang-19 must all agree.
cmake -DCMAKE_C_COMPILER=clang-19 -DCMAKE_CXX_COMPILER=clang-19 \
      -DCMAKE_C_FLAGS="-O0 -g -grecord-command-line -fpass-plugin=/usr/lib/mull-ir-frontend-19" \
      -DCMAKE_CXX_FLAGS="-O0 -g -grecord-command-line -fpass-plugin=/usr/lib/mull-ir-frontend-19" \
      -B build/

cmake --build build/
```

The Mull pass instruments the compiled IR with conditional mutation
points; at runtime, the runner enables / disables each mutation
to test which the test suite catches.

## Step 3 - Run

```bash
# The runner binary is version-suffixed too. The default IDE reporter prints
# killed / survived mutants to the console (per [mull-cli]).
mull-runner-19 build/tests/MyTests
```

Output:

```
[killed]   src/cart.cpp:42 - Conditional Boundary
[survived] src/cart.cpp:78 - Arithmetic Operator Replacement
[survived] src/cart.cpp:103 - Statement Removal

Mutants killed: 87 (74.4%)
Mutants survived: 30
Mutation score: 74.4%
```

## Step 4 - Mutators

Mull's mutator catalog (representative; per the paper + code):

| Mutator                          | Example                                           |
|----------------------------------|---------------------------------------------------|
| Arithmetic Operator Replacement   | `+` → `-`                                          |
| Conditional Boundary               | `<` → `<=`                                          |
| Conditional Negation               | `==` → `!=`                                         |
| Statement Removal                  | `delete x;` → (removed)                             |
| Return Value Replacement           | `return x;` → `return 0;`                            |
| Constant Mutation                  | `42` → `0`, `1` → `0`                                |

LLVM-IR-level mutation means some source-level patterns produce
equivalent IR (no mutation possible) - Mull skips those silently.

## Step 5 - Filtering

Mull accepts include / exclude path filters:

```bash
mull-runner-19 build/tests/MyTests \
  --include-path "src/checkout/*" \
  --exclude-path "third_party/*" \
  --exclude-path "tests/*"
```

Always exclude tests + third-party - mutating those is
meaningless.

## Step 6 - Reports

```bash
# Elements = interactive HTML report (mutation-testing-elements);
# Sarif = machine-readable for GitHub Code Scanning. Per [mull-cli], pick
# reporters by name and set the output dir / base name explicitly.
mull-runner-19 build/tests/MyTests \
  --reporters Elements,Sarif --report-dir ./mull-report --report-name results

# Outputs under ./mull-report/ (results.html, results.sarif)
```

The Elements report shows a per-file mutation breakdown; the Sarif output
uploads to a code-scanning dashboard. Other reporters per [mull-cli]:
`IDE` (console), `SQLite`, `GithubAnnotations`, `Patches`.

## Step 7 - CI integration

```yaml
- run: |
    # install mull-19 + clang-19 per the official guide (Step 1) before this step
    cmake -B build/ -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_C_COMPILER=clang-19 -DCMAKE_CXX_COMPILER=clang-19 \
      -DCMAKE_C_FLAGS="-O0 -g -fpass-plugin=/usr/lib/mull-ir-frontend-19" \
      -DCMAKE_CXX_FLAGS="-O0 -g -fpass-plugin=/usr/lib/mull-ir-frontend-19"
    cmake --build build/
    mull-runner-19 build/tests/MyTests --reporters Sarif --report-dir ./mull-report --report-name results
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: mull-results
    path: ./mull-report/
```

For PR-incremental runs, scope to changed files:

```bash
CHANGED=$(git diff --name-only origin/main...HEAD | grep -E '\.(c|cpp|h|hpp)$')
mull-runner-19 build/tests/MyTests --include-path "$(echo $CHANGED | tr ' ' ',')"
```

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Mutating Release builds                                                | Optimizer changes IR shape; mutators behave unpredictably.                | Build with `-O0 -g` (Step 2). |
| Including `tests/` in mutation                                         | Mutates the tests; meaningless.                                          | Exclude tests path (Step 5). |
| Mismatched LLVM versions (mull-19 plugin but compiled with clang-17) | Plugin load / ABI incompatibility.                                  | Match the suffix across package, plugin path, and clang (Step 2). |
| Running on every PR                                                    | Slow; team disables.                                                      | Schedule + per-changed-file scope (Step 7). |
| Setting an unrealistic mutation score gate                             | Forces low-value tests.                                                   | Start at current baseline. |

## Limitations

- **LLVM toolchain dependency.** Requires the same LLVM version
  Mull was built against; can be tricky in heterogeneous CI.
- **C / C++ primary; other languages incidental.** Swift / Rust
  via LLVM-IR work in principle but with less polish.
- **Build configuration constraint.** `-O0` builds run slower
  than Release; mutation-runs are inherently slow.
- **No native incremental mode.** Use `--include-path` for git-diff
  scoping (Step 7).
- **Smaller community than Stryker / PIT.** 811 stars per
  [mull-readme][mr] vs Stryker's thousands; tooling integration
  varies.

## References

- [mr][mr] - Mull README: LLVM-based, C/C++ primary, foundational
  2018 paper "Mull It Over: Mutation Testing Based on LLVM"
  (Denisov & Pankevich).
- [mull-changelog] - release history (latest 0.34.0, May 2026).
- [mull-install] - apt repo + version-matched `mull-NN` package.
- [mull-tutorial] - `-fpass-plugin` build instrumentation.
- [mull-cli] - `mull-runner` flags and reporter names.
- `stryker-mutation`,
  `stryker-net-mutation`,
  `pitest-mutation`,
  `mutmut-mutation` - 
  per-language siblings.

[mull-changelog]: https://github.com/mull-project/mull/blob/main/CHANGELOG.md
[mull-install]: https://mull.readthedocs.io/en/latest/Installation.html
[mull-tutorial]: https://mull.readthedocs.io/en/latest/tutorials/HelloWorld.html
[mull-cli]: https://mull.readthedocs.io/en/latest/CommandLineReference.html
