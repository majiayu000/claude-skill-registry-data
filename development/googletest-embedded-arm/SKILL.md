---
name: googletest-embedded-arm
description: "Author and run GoogleTest 1.17+ for embedded C++ on ARM targets - TEST() / TEST_F() / TEST_P() / TYPED_TEST(), EXPECT_* vs ASSERT_* assertions, fixtures with SetUp() / TearDown(), value-parameterised tests, GoogleMock when paired, cross-compile with arm-none-eabi-g++, run on host or under QEMU via the qemu-system-test-runner skill, --gtest_filter / --gtest_output=xml:results.xml / --gtest_shuffle / --gtest_repeat command-line flags, and XML / JSON output parsing for CI. Use when the unit-under-test is C++ (modern C++17+) and the team wants the de-facto C++ test framework instead of the C-only Unity. For C use unity-test-framework-c; for pure C mocks see the CMock reference in ceedling-build-runner."
metadata:
  keywords: "googletest, gtest, gmock, embedded, arm, c++, cortex-m, cortex-a"
  version: "1.3.8"
---

# googletest-embedded-arm

## Overview

GoogleTest is, per the README at
[github.com/google/googletest](https://github.com/google/googletest),
"Google's C++ test framework" - an xUnit-style framework merged
with GoogleMock so the two ship together. The 1.17.x branch
"requires at least C++17". For embedded ARM use, the framework
runs anywhere a hosted C++ standard library is available - on
the host, under QEMU, and on Cortex-A Linux targets; for
Cortex-M without an OS, a minimal `_write` / `_exit` semihosting
stub is the bridge.

This skill wraps GoogleTest for embedded C++ work. Composes
with:

- `embedded-coverage-strategy-reference`
  for gcov / llvm-cov instrumentation.
- `qemu-system-test-runner`
  for running the binary on a virtual Cortex-M / Cortex-A.
- For pure-C suites, prefer
  `unity-test-framework-c`;
  for mock-heavy suites prefer the Ceedling stack -
  `ceedling-build-runner` (CMock semantics in its references/cmock.md).

## When to use

- Unit-under-test is **C++** (not C). For C, use
  `unity-test-framework-c`.
- Target is **Cortex-A running Linux** or **Cortex-M with semihosting** - anything with enough RAM for the gtest binary (~300 KB stripped).
- Team wants the **de-facto C++ framework** with rich matchers
  (GoogleMock, value-parameterised tests, typed tests).
- The build pipeline can run a host build for speed and a
  cross-compile under QEMU for architecture sanity.

## How to use

1. Confirm the unit-under-test is **C++17+** (for C, use `unity-test-framework-c`).
2. Fetch GoogleTest and build the suite on the **host** for the fast inner loop (`gtest_main` supplies `main()`); author `TEST()` / `TEST_F()` cases - see Authoring.
3. Cross-compile the same suite for the ARM target with `arm-none-eabi-g++` and run it under QEMU for architecture sanity - full toolchain, CMake, and build invariants in [references/cross-compile-and-ci.md](references/cross-compile-and-ci.md).
4. Emit `--gtest_output=xml:results.xml`; gate the host job on the JUnit XML and the QEMU job on the semihosting exit code.
5. Reach for value-parameterised (`TEST_P`), typed (`TYPED_TEST`), and death tests as coverage grows - see [references/authoring-variants.md](references/authoring-variants.md).

The full single-test path (author to QEMU) is in Worked example below.

## Authoring

### Minimal test

Per [google.github.io/googletest/primer.html](https://google.github.io/googletest/primer.html):

```cpp
#include <gtest/gtest.h>
#include "ringbuffer.h"

TEST(RingbufferTest, EmptyOnInit) {
    Ringbuffer<int, 8> rb;
    EXPECT_TRUE(rb.empty());
    EXPECT_EQ(0u, rb.size());
}

TEST(RingbufferTest, PushIncrementsSize) {
    Ringbuffer<int, 8> rb;
    rb.push(42);
    EXPECT_EQ(1u, rb.size());
    EXPECT_FALSE(rb.empty());
}
```

`TEST(SuiteName, TestName)` registers an independent test; the
first argument is "the name of the test suite, and the second
argument is the test's name within the test suite" (Primer doc).

### Fixtures (TEST_F)

When several tests share setup, derive from `::testing::Test`:

```cpp
class RingbufferTest : public ::testing::Test {
protected:
    void SetUp() override { rb.clear(); }
    void TearDown() override { /* nothing */ }
    Ringbuffer<int, 8> rb;
};

TEST_F(RingbufferTest, PopReturnsPushedValue) {
    rb.push(7);
    int v = 0;
    EXPECT_TRUE(rb.pop(&v));
    EXPECT_EQ(7, v);
}
```

Per the Primer: "GoogleTest does not reuse the same test fixture
for multiple tests" - each `TEST_F` gets a fresh instance.

### Fatal vs non-fatal

| Family | On failure | Use when |
|---|---|---|
| `EXPECT_*` (e.g. `EXPECT_EQ`) | Records failure; continues | Each assertion is independent; collect all failures |
| `ASSERT_*` (e.g. `ASSERT_EQ`) | Records failure; **aborts current function** | Subsequent assertions would crash (e.g. null pointer deref) |

Per the Primer: "Usually EXPECT_* are preferred, as they allow
more than one failure to be reported in a test." Use `ASSERT_*`
only when the next line would dereference a possibly-null pointer
returned from the previous check.

Value-parameterised (`TEST_P`), typed (`TYPED_TEST`), and death
tests live in [references/authoring-variants.md](references/authoring-variants.md).

## Worked example

One test from host to QEMU, end to end. It uses the
`RingbufferTest` cases from Authoring above.

1. Put those cases in `test/ringbuffer_test.cpp`.

2. Host build + run (fast inner loop) with the CMake config from
   [references/cross-compile-and-ci.md](references/cross-compile-and-ci.md):

```bash
cmake -S . -B build-host && cmake --build build-host
./build-host/ringbuffer_test
# [==========] Running 2 tests from 1 test suite.
# [  PASSED  ] 2 tests.
```

3. Cross-compile the same source for Cortex-M4 and run it under QEMU:

```bash
arm-none-eabi-g++ -mcpu=cortex-m4 -mthumb -O0 -g -std=c++17 \
    -DGTEST_HAS_PTHREAD=0 --specs=rdimon.specs \
    -I ext/googletest/googletest/include \
    test/ringbuffer_test.cpp ext/googletest/googletest/src/gtest-all.cc \
    -o ringbuffer_test.elf -lrdimon

qemu-system-arm -M mps2-an385 -cpu cortex-m4 -nographic \
    -semihosting-config enable=on,target=native \
    -kernel ringbuffer_test.elf
echo $?   # gtest RUN_ALL_TESTS() return code, propagated via semihosting exit
```

4. Two flags make the target run work: `-DGTEST_HAS_PTHREAD=0` is
   mandatory on bare-metal M-profile (no pthreads, link fails
   without it), and `--specs=rdimon.specs` pulls in the
   [`librdimon`](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain)
   semihosting library so stdout and `exit()` reach QEMU. The
   `-kernel` flag loads the ELF.

5. For a machine-readable gate, add `--gtest_output=xml:results.xml`
   to the host run and count failing testcases - the XML schema
   and parsing pattern are in
   [references/cross-compile-and-ci.md](references/cross-compile-and-ci.md).

## Command-line flags

The flags every embedded run reaches for (per the
[Advanced Guide](https://google.github.io/googletest/advanced.html)):

| Flag | Effect |
|---|---|
| `--gtest_filter=Pattern` | `:`-separated wildcard list; supports `*`, `?`, negative `-` |
| `--gtest_output=xml:results.xml` / `json:results.json` | Machine-readable report for CI |
| `--gtest_shuffle` | Random order each run - reveals inter-test dependencies |
| `--gtest_repeat=N` | Repeat N times (`-1` = infinite, for flake hunting) |

The full flag set (`--gtest_break_on_failure`,
`--gtest_catch_exceptions=0`, `--gtest_brief`,
`--gtest_list_tests`, and more), the XML / JSON output schema, and
the CI-gate parsing pattern are in
[references/cross-compile-and-ci.md](references/cross-compile-and-ci.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `ASSERT_EQ` then ignore the abort and continue | Subsequent assertions undefined; can crash | Use `EXPECT_EQ` unless next line dereferences the value |
| `GTEST_HAS_PTHREAD=1` on bare-metal Cortex-M | Link fails: pthread symbols missing | Always `-DGTEST_HAS_PTHREAD=0` on M-profile cross-builds |
| Death tests on bare-metal | No `fork()`; test hangs or aborts oddly | Skip death tests on M-profile; or use `--gtest_filter=-*DeathTest*` |
| Linking `gtest` without `gtest_main` then no own `main` | "undefined reference to main" | Link `gtest_main` or write `int main(int argc, char **argv) { testing::InitGoogleTest(&argc, argv); return RUN_ALL_TESTS(); }` |
| Test order dependence | `--gtest_shuffle` reveals; CI breaks intermittently | Each `TEST_F` must work in any order; reset state in `SetUp` |
| Optimised coverage build | `-O2` collapses branches gcov can't see | `-O0 -g` for the coverage build per coverage-reference skill |
| `TEST_P` without `INSTANTIATE_TEST_SUITE_P` | Compiles but never runs | Always pair |
| Mocking everything | Tests measure mocks not behaviour | Mock at the I/O boundary only - see ceedling-build-runner's references/cmock.md |

## Limitations

- **C++ only.** For pure C suites use
  `unity-test-framework-c`.
- **Heap required.** GoogleTest allocates internally; ultra-low-
  RAM Cortex-M0 (8 - 16 KB) may not have headroom. Use Unity for
  those targets.
- **No native parameterised test = different test names.** Each
  `TEST_P` instance is `Boundaries/WrapTest.WrapAtCapacity/4` - 
  the `/4` is the param index, not the value. Use
  `INSTANTIATE_TEST_SUITE_P(..., ::testing::PrintToStringParamName())`
  to encode the value into the name.
- **Death tests require `fork()`** - not available on bare-metal
  or under most RTOSes. Per the Advanced Guide they run "in
  separate child processes".
- **No determinism guarantee with `--gtest_shuffle`** - the seed
  is logged but rerunning with the same seed and a code change
  produces a different schedule.
- **GoogleMock pulls in `std::function`-based call recording** - 
  on cross-compiles with `-fno-exceptions` you may need
  `-DGTEST_HAS_EXCEPTIONS=0` to compile cleanly.

## References

Cited inline. Foundational documents:

- GoogleTest README - [github.com/google/googletest](https://github.com/google/googletest).
- GoogleTest Primer - [google.github.io/googletest/primer.html](https://google.github.io/googletest/primer.html).
- GoogleTest Advanced Guide - [google.github.io/googletest/advanced.html](https://google.github.io/googletest/advanced.html).
- ARM GNU Toolchain - [developer.arm.com Tools and Software / GNU Toolchain](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain).
- Deep references (with their own citations): advanced authoring
  (`TEST_P` / `TYPED_TEST` / death tests) in
  [references/authoring-variants.md](references/authoring-variants.md);
  full toolchain, output schema, and CI in
  [references/cross-compile-and-ci.md](references/cross-compile-and-ci.md).
- Sibling skills:
  `unity-test-framework-c`,
  `ceedling-build-runner` (CMock semantics in its references/cmock.md),
  `qemu-system-test-runner`,
  `embedded-coverage-strategy-reference`,
  `hardware-in-loop-reference`.
