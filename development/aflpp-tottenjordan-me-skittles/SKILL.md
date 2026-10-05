---
name: aflpp
type: fuzzer
description: >
  AFL++ is a fork of AFL with better fuzzing performance and advanced features.
  Use for multi-core fuzzing of C/C++ projects.
---

# AFL++

AFL++ is a fork of the original AFL fuzzer that offers better fuzzing performance and more advanced features while maintaining stability. A major benefit over libFuzzer is that AFL++ has stable support for running fuzzing campaigns on multiple cores, making it ideal for large-scale fuzzing efforts.

## When to Use

| Fuzzer | Best For | Complexity |
|--------|----------|------------|
| AFL++ | Multi-core fuzzing, diverse mutations, mature projects | Medium |
| libFuzzer | Quick setup, single-threaded, simple harnesses | Low |
| LibAFL | Custom fuzzers, research, advanced use cases | High |

**Choose AFL++ when:**
- You need multi-core fuzzing to maximize throughput
- Your project can be compiled with Clang or GCC
- You want diverse mutation strategies and mature tooling
- libFuzzer has plateaued and you need more coverage
- You're fuzzing production codebases that benefit from parallel execution

## Quick Start

```c++
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Call your code with fuzzer-provided data
    check_buf((char*)data, size);
    return 0;
}
```

Compile and run:
```bash
# Setup AFL++ wrapper script first (see Installation)
./afl++ docker afl-clang-fast++ -DNO_MAIN=1 -O2 -fsanitize=fuzzer harness.cc main.cc -o fuzz
mkdir seeds && echo "aaaa" > seeds/minimal_seed
./afl++ docker afl-fuzz -i seeds -o out -- ./fuzz
```

## Installation

AFL++ has many dependencies including LLVM, Python, and Rust. We recommend using a current Debian or Ubuntu distribution for fuzzing with AFL++.

| Method | When to Use | Supported Compilers |
|--------|-------------|---------------------|
| Ubuntu/Debian repos | Recent Ubuntu, basic features only | Ubuntu 23.10: Clang 14 & GCC 13<br>Debian 12: Clang 14 & GCC 12 |
| Docker (from Docker Hub) | Specific AFL++ version, Apple Silicon support | As of 4.35c: Clang 19 & GCC 11 |
| Docker (from source) | Test unreleased features, apply patches | Configurable in Dockerfile |
| From source | Avoid Docker, need specific patches | Adjustable via `LLVM_CONFIG` env var |

### Ubuntu/Debian

Prior to installing afl++, check the clang version dependency of the packge with `apt-cache show afl++`, and install the matching `lld` version (e.g., `lld-17`).


```bash
apt install afl++ lld-17
```


### Docker (from Docker Hub)

```bash
docker pull aflplusplus/aflplusplus:stable
```

### Docker (from source)

```bash
git clone --depth 1 --branch stable https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
docker build -t aflplusplus .
```

### From source

Refer to the [Dockerfile](https://github.com/AFLplusplus/AFLplusplus/blob/stable/Dockerfile) for Ubuntu version requirements and dependencies. Set `LLVM_CONFIG` to specify Clang version (e.g., `llvm-config-18`).

### Wrapper Script Setup

Create a wrapper script to run AFL++ on host or Docker:

```bash
cat <<'EOF' > ./afl++
#!/bin/sh
AFL_VERSION="${AFL_VERSION:-"stable"}"
case "$1" in
   host)
        shift
        bash -c "$*"
        ;;
    docker)
        shift
        /usr/bin/env docker run -ti \
            --privileged \
            -v ./:/src \
            --rm \
            --name afl_fuzzing \
            "aflplusplus/aflplusplus:$AFL_VERSION" \
            bash -c "cd /src && bash -c \"$*\""
        ;;
    *)
        echo "Usage: $0 {host|docker}"
        exit 1
        ;;
esac
EOF
chmod +x ./afl++
```

**Security Warning:** The `afl-system-config` and `afl-persistent-config` scripts require root privileges and disable OS security features. Do not fuzz on production systems or your development environment. Use a dedicated VM instead.

### System Configuration

Run after each reboot for up to 15% more executions per second:

```bash
./afl++ <host/docker> afl-system-config
```

For maximum performance, disable kernel security mitigations (requires grub bootloader, not supported in Docker):

```bash
./afl++ host afl-persistent-config
update-grub
reboot
./afl++ <host/docker> afl-system-config
```

Verify with `cat /proc/cmdline` - output should include `mitigations=off`.

## Writing a Harness

### Harness Structure

AFL++ supports libFuzzer-style harnesses:

```c++
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // 1. Validate input size if needed
    if (size < MIN_SIZE || size > MAX_SIZE) return 0;

    // 2. Call target function with fuzz data
    target_function(data, size);

    // 3. Return 0 (non-zero reserved for future use)
    return 0;
}
```

### Harness Rules

| Do | Don't |
|----|-------|
| Reset global state between runs | Rely on state from previous runs |
| Handle edge cases gracefully | Exit on invalid input |
| Keep harness deterministic | Use random number generators |
| Free allocated memory | Create memory leaks |
| Validate input sizes | Process unbounded input |

> **See Also:** For detailed harness writing techniques, patterns for handling complex inputs,
> and advanced strategies, see the **fuzz-harness-writing** technique skill.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Low exec/sec (<1k) | Not using persistent mode | Create a LLVMFuzzerTestOneInput style harness |
| Low stability (<85%) | Non-deterministic code | Fuzz a program via stdin or file inputs, or create such a harness |
| GCC plugin error | GCC version mismatch | Ensure system GCC matches AFL++ build and install gcc-$GCC_VERSION-plugin-dev |
| No crashes found | Need sanitizers | Recompile with `AFL_USE_ASAN=1` |
| Memory limit exceeded | ASan uses 20TB virtual | Remove `-m` flag when using ASan |
| Docker performance loss | Virtualization overhead | Use bare metal or VM for production fuzzing |

## Reference material

**[references/campaigns.md](references/campaigns.md)** — campaign execution, corpus management, multi-core fuzzing, and CMPLOG

**[references/analysis.md](references/analysis.md)** — coverage measurement and sanitizers

**[references/examples.md](references/examples.md)** — compilation, advanced usage, and worked examples

## Related Skills

### Technique Skills

| Skill | Use Case |
|-------|----------|
| **fuzz-harness-writing** | Detailed guidance on writing effective harnesses |
| **address-sanitizer** | Memory error detection during fuzzing |
| **undefined-behavior-sanitizer** | Detect undefined behavior bugs |
| **fuzzing-corpus** | Building and managing seed corpora |
| **fuzzing-dictionaries** | Creating dictionaries for format-aware fuzzing |

### Related Fuzzers

| Skill | When to Consider |
|-------|------------------|
| **libfuzzer** | Quick prototyping, single-threaded fuzzing is sufficient |
| **libafl** | Need custom mutators or research-grade features |

## Resources

### Key External Resources

**[AFL++ GitHub Repository](https://github.com/AFLplusplus/AFLplusplus)**
Official repository with comprehensive documentation, examples, and issue tracker.

**[Fuzzing in Depth](https://aflplus.plus/docs/fuzzing_in_depth/)**
Advanced documentation by the AFL++ team covering instrumentation modes, optimization techniques, and advanced use cases.

**[AFL++ Under The Hood](https://blog.ritsec.club/posts/afl-under-hood/)**
Technical deep-dive into AFL++ internals, mutation strategies, and coverage tracking mechanisms.

**[AFL++: Combining Incremental Steps of Fuzzing Research](https://www.usenix.org/system/files/woot20-paper-fioraldi.pdf)**
Research paper describing AFL++ architecture and performance improvements over original AFL.

### Video Resources

- [Fuzzing cURL](https://blog.trailofbits.com/2023/02/14/curl-audit-fuzzing-libcurl-command-line-interface/) - Trail of Bits blog post on using AFL++ argument fuzzing for cURL
- [Sudo Vulnerability Walkthrough](https://www.youtube.com/playlist?list=PLhixgUqwRTjy0gMuT4C3bmjeZjuNQyqdx) - LiveOverflow series on rediscovering CVE-2021-3156
- [Rediscovery of libpng bug](https://www.youtube.com/watch?v=PJLWlmp8CDM) - LiveOverflow video on finding CVE-2023-4863
