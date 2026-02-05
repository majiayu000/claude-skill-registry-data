---
name: bash-scripting
description: Master of defensive Bash scripting for production automation, CI/CD pipelines, and system utilities. Expert in safe, portable, and testable shell scripts. Use when writing, creating, authoring, generating, or developing bash scripts, shell scripts, or automation. Also triggers for learning bash best practices, understanding defensive programming patterns, implementing error handling, ensuring portability, following shellcheck recommendations, or applying production-grade bash standards. Helps with CI/CD scripts, system utilities, deployment automation, and production bash code.
allowed-tools: [Read, Edit, Write, Grep, Glob, Bash]
---

## Reference Files

Deep-dive guides for specific topics:

- [patterns-and-conventions.md](patterns-and-conventions.md) - Defensive programming patterns, strict mode, and code style
- [safety-and-security.md](safety-and-security.md) - Security patterns, input validation, and hardening
- [portability-and-compatibility.md](portability-and-compatibility.md) - Cross-platform compatibility and Bash version features
- [documentation-and-ci-cd.md](documentation-and-ci-cd.md) - Documentation standards and CI/CD integration
- [performance-and-optimization.md](performance-and-optimization.md) - Optimization techniques and profiling
- [advanced-techniques.md](advanced-techniques.md) - Advanced patterns, dependencies, and common pitfalls
- [tools-and-frameworks.md](tools-and-frameworks.md) - Essential tools, testing frameworks, and external resources

---

# Bash Scripting

Master guide for defensive Bash scripting following production-grade best practices. This skill provides comprehensive patterns, standards, and techniques for writing safe, portable, and maintainable shell scripts for automation, CI/CD pipelines, and system utilities.

Use this skill when writing new bash scripts or improving existing ones to follow defensive programming principles.

## Focus Areas

- Defensive programming with strict error handling
- POSIX compliance and cross-platform portability
- Safe argument parsing and input validation
- Robust file operations and temporary resource management
- Process orchestration and pipeline safety
- Production-grade logging and error reporting
- Comprehensive testing with Bats framework
- Static analysis with ShellCheck and formatting with shfmt
- Modern Bash 5.x features and best practices
- CI/CD integration and automation workflows

## Core Approach

Essential defensive programming patterns (see [patterns-and-conventions.md](patterns-and-conventions.md) for complete details):

- **Strict mode**: Always use `set -Eeuo pipefail` with error trapping
- **Quote variables**: Prevent word splitting and globbing issues
- **Safe iteration**: Use proper arrays, avoid `for f in $(ls)`
- **Conditionals**: Use `[[ ]]` for Bash, `[ ]` for POSIX
- **Temp files**: Create safely with `mktemp` and cleanup traps
- **Output**: Prefer `printf` over `echo` for reliability
- **Input validation**: Check required variables with `: "${VAR:?message}"`
- **Safe operations**: End option parsing with `--`, use `rm -rf -- "$dir"`
- **NUL-safe patterns**: Use `find -print0 | while IFS= read -r -d ''` for filenames
- **Logging**: Implement structured logging with configurable verbosity
- **Idempotency**: Design scripts to be repeatable and support dry-run modes

## Quality Checklist

- Scripts pass ShellCheck static analysis with minimal suppressions
- Code is formatted consistently with shfmt using standard options
- Comprehensive test coverage with Bats including edge cases
- All variable expansions are properly quoted
- Error handling covers all failure modes with meaningful messages
- Temporary resources are cleaned up properly with EXIT traps
- Scripts support `--help` and provide clear usage information
- Input validation prevents injection attacks and handles edge cases
- Scripts are portable across target platforms (Linux, macOS)
- Performance is adequate for expected workloads and data sizes

## Output

Production-ready deliverables:

- Bash scripts with defensive programming practices
- Test suites using bats-core or shellspec with TAP output
- CI/CD pipeline configurations for automated testing
- Documentation (shdoc markdown, shellman man pages)
- Static analysis configuration (.shellcheckrc, .shfmt.toml)
- Security review with SAST and secrets scanning
- Structured logging and observability

## Where to Find What

- **Getting started**: Review Focus Areas and Core Approach above
- **Defensive patterns**: [patterns-and-conventions.md](patterns-and-conventions.md) - Strict mode, quoting, code style
- **Security**: [safety-and-security.md](safety-and-security.md) - Input validation, secure file ops, hardening
- **Cross-platform**: [portability-and-compatibility.md](portability-and-compatibility.md) - Platform detection, Bash versions
- **CI/CD setup**: [documentation-and-ci-cd.md](documentation-and-ci-cd.md) - GitHub Actions, pre-commit hooks
- **Performance**: [performance-and-optimization.md](performance-and-optimization.md) - Profiling, logging, optimization
- **Advanced patterns**: [advanced-techniques.md](advanced-techniques.md) - Complex patterns, dependencies, pitfalls
- **Tools**: [tools-and-frameworks.md](tools-and-frameworks.md) - ShellCheck, bats-core, external resources
