---
name: harness-writing
type: technique
description: >
  Techniques for writing effective fuzzing harnesses across languages.
  Use when creating new fuzz targets or improving existing harness code.
---

# Writing Fuzzing Harnesses

A fuzzing harness is the entrypoint function that receives random data from the fuzzer and routes it to your system under test (SUT). The quality of your harness directly determines which code paths get exercised and whether critical bugs are found. A poorly written harness can miss entire subsystems or produce non-reproducible crashes.

## Overview

The harness is the bridge between the fuzzer's random byte generation and your application's API. It must parse raw bytes into meaningful inputs, call target functions, and handle edge cases gracefully. The most important part of any fuzzing setup is the harness—if written poorly, critical parts of your application may not be covered.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Harness** | Function that receives fuzzer input and calls target code under test |
| **SUT** | System Under Test—the code being fuzzed |
| **Entry point** | Function signature required by the fuzzer (e.g., `LLVMFuzzerTestOneInput`) |
| **FuzzedDataProvider** | Helper class for structured extraction of typed data from raw bytes |
| **Determinism** | Property that ensures same input always produces same behavior |
| **Interleaved fuzzing** | Single harness that exercises multiple operations based on input |

## When to Apply

**Apply this technique when:**
- Creating a new fuzz target for the first time
- Fuzz campaign has low code coverage or isn't finding bugs
- Crashes found during fuzzing are not reproducible
- Target API requires complex or structured inputs
- Multiple related functions should be tested together

**Skip this technique when:**
- Using existing well-tested harnesses from your project
- Tool provides automatic harness generation that meets your needs
- Target already has comprehensive fuzzing infrastructure

## Quick Reference

| Task | Pattern |
|------|---------|
| Minimal C++ harness | `extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)` |
| Minimal Rust harness | `fuzz_target!(|data: &[u8]| { ... })` |
| Size validation | `if (size < MIN_SIZE) return 0;` |
| Cast to integers | `uint32_t val = *(uint32_t*)(data);` |
| Use FuzzedDataProvider | `FuzzedDataProvider fuzzed_data(data, size);` |
| Extract typed data (C++) | `auto val = fuzzed_data.ConsumeIntegral<uint32_t>();` |
| Extract string (C++) | `auto str = fuzzed_data.ConsumeBytesWithTerminator<char>(32, 0xFF);` |

## Tool-Specific Guidance

### libFuzzer

**Harness signature:**
```cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Your code here
    return 0;  // Non-zero return is reserved for future use
}
```

**Compilation:**
```bash
clang++ -fsanitize=fuzzer,address -g harness.cc -o fuzz_target
```

**Integration tips:**
- Use `FuzzedDataProvider.h` for structured input extraction
- Compile with `-fsanitize=fuzzer` to link the fuzzing runtime
- Add sanitizers (`-fsanitize=address,undefined`) to detect more bugs
- Use `-g` for better stack traces when crashes occur
- libFuzzer can start with empty corpus—no seed inputs required

**Running:**
```bash
./fuzz_target corpus_dir/
```

**Resources:**
- [FuzzedDataProvider header](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h)
- [libFuzzer documentation](https://llvm.org/docs/LibFuzzer.html)

### AFL++

AFL++ supports multiple harness styles. For best performance, use persistent mode:

**Persistent mode harness:**
```cpp
#include <unistd.h>

int main(int argc, char **argv) {
    #ifdef __AFL_HAVE_MANUAL_CONTROL
        __AFL_INIT();
    #endif

    unsigned char buf[MAX_SIZE];

    while (__AFL_LOOP(10000)) {
        // Read input from stdin
        ssize_t len = read(0, buf, sizeof(buf));
        if (len <= 0) break;

        // Call target function
        target_function(buf, len);
    }

    return 0;
}
```

**Compilation:**
```bash
afl-clang-fast++ -g harness.cc -o fuzz_target
```

**Integration tips:**
- Use persistent mode (`__AFL_LOOP`) for 10-100x speedup
- Consider deferred initialization (`__AFL_INIT()`) to skip setup overhead
- AFL++ requires at least one seed input in the corpus directory
- Use `AFL_USE_ASAN=1` or `AFL_USE_UBSAN=1` for sanitizer builds

**Running:**
```bash
afl-fuzz -i seeds/ -o findings/ -- ./fuzz_target
```

### cargo-fuzz (Rust)

**Harness signature:**
```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    // Your code here
});
```

**With structured input (arbitrary crate):**
```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: YourStruct| {
    data.check();
});
```

**Creating harness:**
```bash
cargo fuzz init
cargo fuzz add my_target
```

**Integration tips:**
- Use `arbitrary` crate for automatic struct deserialization
- cargo-fuzz wraps libFuzzer, so all libFuzzer features work
- Compile with sanitizers automatically via cargo-fuzz
- Harnesses go in `fuzz/fuzz_targets/` directory

**Running:**
```bash
cargo +nightly fuzz run my_target
```

**Resources:**
- [cargo-fuzz documentation](https://rust-fuzz.github.io/book/cargo-fuzz.html)
- [arbitrary crate](https://github.com/rust-fuzz/arbitrary)

### go-fuzz

**Harness signature:**
```go
// +build gofuzz

package mypackage

func Fuzz(data []byte) int {
    // Call target function
    target(data)

    // Return codes:
    // -1 if input is invalid
    //  0 if input is valid but not interesting
    //  1 if input is interesting (e.g., added new coverage)
    return 0
}
```

**Building:**
```bash
go-fuzz-build
```

**Integration tips:**
- Return 1 for inputs that add coverage (optional—fuzzer can detect automatically)
- Return -1 for invalid inputs to deprioritize similar mutations
- go-fuzz handles persistence automatically

**Running:**
```bash
go-fuzz -bin=./mypackage-fuzz.zip -workdir=fuzz
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **Low executions/sec** | Harness is too slow (logging, I/O, complexity) | Profile harness, remove bottlenecks, mock I/O |
| **No crashes found** | Coverage not reaching buggy code | Check coverage, improve harness to reach more paths |
| **Non-reproducible crashes** | Non-determinism or global state | Remove randomness, reset globals between iterations |
| **Fuzzer exits immediately** | Harness calls `exit()` | Replace `exit()` with `abort()` or return error |
| **Out of memory errors** | Memory leaks in harness or SUT | Free allocations, use leak sanitizer to find leaks |
| **Crashes on empty input** | Harness doesn't validate size | Add `if (size < MIN_SIZE) return 0;` |
| **Corpus not growing** | Inputs too constrained or format too strict | Use FuzzedDataProvider or structure-aware fuzzing |

## Reference material

**[references/patterns.md](references/patterns.md)** — the step-by-step process and common harness patterns

**[references/advanced.md](references/advanced.md)** — advanced usage, practical rules, and anti-patterns

## Related Skills

### Tools That Use This Technique

| Skill | How It Applies |
|-------|----------------|
| **libfuzzer** | Uses `LLVMFuzzerTestOneInput` harness signature with FuzzedDataProvider |
| **aflpp** | Supports persistent mode harnesses with `__AFL_LOOP` for performance |
| **cargo-fuzz** | Uses Rust-specific `fuzz_target!` macro with arbitrary crate integration |
| **atheris** | Python harness takes bytes, calls Python functions |
| **ossfuzz** | Requires harnesses in specific directory structure for cloud fuzzing |

### Related Techniques

| Skill | Relationship |
|-------|--------------|
| **coverage-analysis** | Measure harness effectiveness—are you reaching target code? |
| **address-sanitizer** | Detects bugs found by harness (buffer overflows, use-after-free) |
| **fuzzing-dictionary** | Provide tokens to help fuzzer pass format checks in harness |
| **fuzzing-obstacles** | Patch SUT when it violates harness rules (exit, non-determinism) |

## Resources

### Key External Resources

**[Split Inputs in libFuzzer - Google Fuzzing Docs](https://github.com/google/fuzzing/blob/master/docs/split-inputs.md)**
Explains techniques for handling multiple input parameters in a single fuzzing harness, including use of magic separators and FuzzedDataProvider.

**[Structure-Aware Fuzzing with Protocol Buffers](https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md)**
Advanced technique using protobuf as intermediate format with custom mutators to ensure fuzzer mutates message contents rather than format encoding.

**[libFuzzer Documentation](https://llvm.org/docs/LibFuzzer.html)**
Official LLVM documentation covering harness requirements, best practices, and advanced features.

**[cargo-fuzz Book](https://rust-fuzz.github.io/book/cargo-fuzz.html)**
Comprehensive guide to writing Rust fuzzing harnesses with cargo-fuzz and the arbitrary crate.

### Video Resources

- [Effective File Format Fuzzing](https://www.youtube.com/watch?v=qTTwqFRD1H8) - Conference talk on writing harnesses for file format parsers
- [Modern Fuzzing of C/C++ Projects](https://www.youtube.com/watch?v=x0FQkAPokfE) - Tutorial covering harness design patterns
