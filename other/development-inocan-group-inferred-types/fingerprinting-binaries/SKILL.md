---
name: fingerprinting-binaries
description: Identifies binary file characteristics including compiler signatures, version information, and build environment details. Use when analyzing unknown binaries, investigating binary origins, or identifying build configurations.
---

# Binary Fingerprinting

## Detection Workflow

1. **Extract strings**: Use `strings` to get all strings, identify version strings, find compiler-related strings, extract build information
2. **Analyze imports**: Identify imported functions, check library dependencies, assess API usage patterns, identify OS/version
3. **Examine code structure**: Analyze function prologues/epilogues, check for stack canaries, identify security features, assess code patterns
4. **Assess binary characteristics**: Determine architecture, identify compiler, estimate build date, classify binary type

## Key Patterns

- Compiler signatures: GCC/Clang/MSVC artifacts, compiler version indicators, optimization level signatures, standard library versions
- Build information: build timestamps, source file paths, debug symbols, build configuration strings
- Library signatures: static library linking, library version indicators, custom library usage, third-party dependencies
- Architecture features: CPU architecture (x86, ARM, MIPS), instruction set extensions (SSE, AVX, NEON), endianness (little/big), ABI

## Output Format

Report with: id, type, subtype, severity, confidence, binary_info (architecture, endianness, file_type, entry_point), compiler_info (compiler, version, optimization, confidence), build_info (build_date, build_host, source_paths), libraries, security_features, recommendations.

## Severity Guidelines

- **INFO**: Informational only, no security impact
- **LOW**: Outdated compiler or libraries with known issues
- **MEDIUM**: Missing security features

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies