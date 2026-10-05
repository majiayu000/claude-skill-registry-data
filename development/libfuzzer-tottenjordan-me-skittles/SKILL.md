---
name: libfuzzer
type: fuzzer
description: >
  Coverage-guided fuzzer built into LLVM for C/C++ projects. Use for fuzzing
  C/C++ code that can be compiled with Clang.
---

# libFuzzer

libFuzzer is an in-process, coverage-guided fuzzer that is part of the LLVM project. It's the recommended starting point for fuzzing C/C++ projects due to its simplicity and integration with the LLVM toolchain. While libFuzzer has been in maintenance-only mode since late 2022, it is easier to install and use than its alternatives, has wide support, and will be maintained for the foreseeable future.

## When to Use

| Fuzzer | Best For | Complexity |
|--------|----------|------------|
| libFuzzer | Quick setup, single-project fuzzing | Low |
| AFL++ | Multi-core fuzzing, diverse mutations | Medium |
| LibAFL | Custom fuzzers, research projects | High |
| Honggfuzz | Hardware-based coverage | Medium |

**Choose libFuzzer when:**
- You need a simple, quick setup for C/C++ code
- Project uses Clang for compilation
- Single-core fuzzing is sufficient initially
- Transitioning to AFL++ later is an option (harnesses are compatible)

**Note:** Fuzzing harnesses written for libFuzzer are compatible with AFL++, making it easy to transition if you need more advanced features like better multi-core support.

## Quick Start

```c++
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Validate input if needed
    if (size < 1) return 0;

    // Call your target function with fuzzer-provided data
    my_target_function(data, size);

    return 0;
}
```

Compile and run:
```bash
clang++ -fsanitize=fuzzer,address -g -O2 harness.cc target.cc -o fuzz
mkdir corpus/
./fuzz corpus/
```

## Installation

### Prerequisites

- LLVM/Clang compiler (includes libFuzzer)
- LLVM tools for coverage analysis (optional)

### Linux (Ubuntu/Debian)

```bash
apt install clang llvm
```

For the latest LLVM version:
```bash
# Add LLVM repository from apt.llvm.org
# Then install specific version, e.g.:
apt install clang-18 llvm-18
```

### macOS

```bash
# Using Homebrew
brew install llvm

# Or using Nix
nix-env -i clang
```

### Windows

Install Clang through Visual Studio. Refer to [Microsoft's documentation](https://learn.microsoft.com/en-us/cpp/build/clang-support-msbuild?view=msvc-170) for setup instructions.

**Recommendation:** If possible, fuzz on a local x86_64 VM or rent one on DigitalOcean, AWS, or Hetzner. Linux provides the best support for libFuzzer.

### Verification

```bash
clang++ --version
# Should show LLVM version information
```

## Writing a Harness

### Harness Structure

The harness is the entry point for the fuzzer. libFuzzer calls the `LLVMFuzzerTestOneInput` function repeatedly with different inputs.

```c++
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // 1. Optional: Validate input size
    if (size < MIN_REQUIRED_SIZE) {
        return 0;  // Reject inputs that are too small
    }

    // 2. Optional: Convert raw bytes to structured data
    // Example: Parse two integers from byte array
    if (size >= 2 * sizeof(uint32_t)) {
        uint32_t a = *(uint32_t*)(data);
        uint32_t b = *(uint32_t*)(data + sizeof(uint32_t));
        my_function(a, b);
    }

    // 3. Call target function
    target_function(data, size);

    // 4. Always return 0 (non-zero reserved for future use)
    return 0;
}
```

### Harness Rules

| Do | Don't |
|----|-------|
| Handle all input types (empty, huge, malformed) | Call `exit()` - stops fuzzing process |
| Join all threads before returning | Leave threads running |
| Keep harness fast and simple | Add excessive logging or complexity |
| Maintain determinism | Use random number generators or read `/dev/random` |
| Reset global state between runs | Rely on state from previous executions |
| Use narrow, focused targets | Mix unrelated data formats (PNG + TCP) in one harness |

**Rationale:**
- **Speed matters:** Aim for 100s-1000s executions per second per core
- **Reproducibility:** Crashes must be reproducible after fuzzing completes
- **Isolation:** Each execution should be independent

### Using FuzzedDataProvider for Complex Inputs

For complex inputs (strings, multiple parameters), use the `FuzzedDataProvider` helper:

```c++
#include <stdint.h>
#include <stddef.h>
#include "FuzzedDataProvider.h"  // From LLVM project

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    FuzzedDataProvider fuzzed_data(data, size);

    // Extract structured data
    size_t allocation_size = fuzzed_data.ConsumeIntegral<size_t>();
    std::vector<char> str1 = fuzzed_data.ConsumeBytesWithTerminator<char>(32, 0xFF);
    std::vector<char> str2 = fuzzed_data.ConsumeBytesWithTerminator<char>(32, 0xFF);

    // Call target with extracted data
    char* result = concat(&str1[0], str1.size(), &str2[0], str2.size(), allocation_size);
    if (result != NULL) {
        free(result);
    }

    return 0;
}
```

Download `FuzzedDataProvider.h` from the [LLVM repository](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h).

### Interleaved Fuzzing

Use a single harness to test multiple related functions:

```c++
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1 + 2 * sizeof(int32_t)) {
        return 0;
    }

    uint8_t mode = data[0];
    int32_t numbers[2];
    memcpy(numbers, data + 1, 2 * sizeof(int32_t));

    // Select function based on first byte
    switch (mode % 4) {
        case 0: add(numbers[0], numbers[1]); break;
        case 1: subtract(numbers[0], numbers[1]); break;
        case 2: multiply(numbers[0], numbers[1]); break;
        case 3: divide(numbers[0], numbers[1]); break;
    }

    return 0;
}
```

> **See Also:** For detailed harness writing techniques, patterns for handling complex inputs,
> structure-aware fuzzing, and protobuf-based fuzzing, see the **fuzz-harness-writing** technique skill.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No crashes found after hours | Poor corpus, low coverage | Add seed inputs, use dictionary, check harness |
| Very slow executions/sec (<100) | Target too complex, excessive logging | Optimize target, use `-close_fd_mask=3`, reduce logging |
| Out of memory | ASan's 20TB virtual memory | Set `-rss_limit_mb=0` to disable RSS limit |
| Fuzzer stops after first crash | Default behavior | Use `-fork=1 -ignore_crashes=1` to continue |
| Can't reproduce crash | Non-determinism in harness/target | Remove random number generation, global state |
| Linking errors with `-fsanitize=fuzzer` | Missing libFuzzer runtime | Ensure using Clang, check LLVM installation |
| GCC project won't compile with Clang | GCC-specific code | Switch to AFL++ with `gcc_plugin` instead |
| Coverage not improving | Corpus plateau | Run longer, add dictionary, improve seeds, check coverage report |
| Crashes but ASan doesn't trigger | Memory error not detected without ASan | Recompile with `-fsanitize=address` |

## Reference material

**[references/campaigns.md](references/campaigns.md)** — running fuzzing campaigns, managing the corpus, and building a dictionary

**[references/analysis.md](references/analysis.md)** — measuring coverage and wiring up sanitizers

**[references/examples.md](references/examples.md)** — compilation flags, worked real-world harnesses, and advanced usage

## Related Skills

### Technique Skills

| Skill | Use Case |
|-------|----------|
| **fuzz-harness-writing** | Detailed guidance on writing effective harnesses, structure-aware fuzzing, and FuzzedDataProvider usage |
| **address-sanitizer** | Memory error detection configuration, ASAN_OPTIONS, and troubleshooting |
| **undefined-behavior-sanitizer** | Detecting undefined behavior during fuzzing |
| **coverage-analysis** | Measuring fuzzing effectiveness and identifying untested code paths |
| **fuzzing-corpus** | Building and managing seed corpora, corpus minimization strategies |
| **fuzzing-dictionaries** | Creating format-specific dictionaries for faster bug discovery |

### Related Fuzzers

| Skill | When to Consider |
|-------|------------------|
| **aflpp** | When you need serious multi-core fuzzing, or when libFuzzer coverage plateaus |
| **honggfuzz** | When you want hardware-based coverage feedback on Linux |
| **libafl** | When building custom fuzzers or conducting fuzzing research |

## Resources

### Official Documentation

- [LLVM libFuzzer Documentation](https://llvm.org/docs/LibFuzzer.html) - Official reference
- [libFuzzer Tutorial by Google](https://github.com/google/fuzzing/blob/master/tutorial/libFuzzerTutorial.md) - Step-by-step guide
- [SanitizerCoverage](https://clang.llvm.org/docs/SanitizerCoverage.html) - Coverage instrumentation details

### Advanced Topics

- [Structure-Aware Fuzzing with libprotobuf-mutator](https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md)
- [Split Inputs in libFuzzer](https://github.com/google/fuzzing/blob/master/docs/split-inputs.md)
- [FuzzedDataProvider Header](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h)

### Example Projects

- [OSS-Fuzz](https://github.com/google/oss-fuzz) - Continuous fuzzing for open-source projects (many libFuzzer examples)
- [AFL++ Dictionary Collection](https://github.com/AFLplusplus/AFLplusplus/tree/stable/dictionaries) - Reusable dictionaries
