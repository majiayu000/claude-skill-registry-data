---
name: makefile
description: Makefile skill for the ikigai project
---

# Makefile

## Description

Build system for ikigai Linux coding agent with comprehensive testing, dynamic analysis, code quality, and multi-distribution packaging support.

## Build

- `make all` - Build the ikigai client binary with default debug configuration.
- `make release` - Clean and rebuild the client in release mode with optimizations.
- `make clean` - Remove all build artifacts, coverage data, reports, and distribution packages.
- `make build-tests` - Build all test binaries without running them.

## Installation

- `make install` - Install the ikigai binary and config files to PREFIX (default /usr/local).
- `make uninstall` - Remove installed binary and configuration files from the system.
- `make install-deps` - Install build dependencies using the system package manager.

## Testing

- `make check` - Build and run all tests in parallel (unit and integration).
- `make check TEST=name` - Build and run a single test matching the specified name.
- `make check-unit` - Build and run only unit tests in parallel.
- `make check-integration` - Build and run only integration and database tests.

## Mock Verification

- `make verify-mocks` - Verify OpenAI mock fixtures against real API responses.
- `make verify-mocks-anthropic` - Verify Anthropic mock fixtures against real API responses.
- `make verify-mocks-google` - Verify Google mock fixtures against real API responses.
- `make verify-mocks-all` - Verify all provider mock fixtures against real APIs.
- `make verify-credentials` - Validate API keys in ~/.config/ikigai/credentials.json.

## VCR Recording

- `make vcr-record-openai` - Re-record OpenAI VCR fixtures with real API calls.
- `make vcr-record-anthropic` - Re-record Anthropic VCR fixtures with real API calls.
- `make vcr-record-google` - Re-record Google VCR fixtures with real API calls.
- `make vcr-record-all` - Re-record all provider VCR fixtures.

## Dynamic Analysis

- `make check-sanitize` - Run all tests with AddressSanitizer and UndefinedBehaviorSanitizer.
- `make check-valgrind` - Run all tests under Valgrind Memcheck for memory leak detection.
- `make check-helgrind` - Run all tests under Valgrind Helgrind for thread error detection.
- `make check-tsan` - Run all tests with ThreadSanitizer for race condition detection.
- `make check-dynamic` - Run all dynamic analysis checks sequentially (or parallel with PARALLEL=1).

## Quality Assurance

- `make check-coverage` - Generate code coverage report and enforce coverage thresholds.
- `make coverage-map` - Generate source file to test mapping for targeted coverage runs.
- `make lint` - Run all lint checks (complexity and filesize).
- `make check-complexity` - Check cyclomatic complexity and nesting depth against thresholds.
- `make check-filesize` - Verify all source and documentation files are below size limits.
- `make ci` - Run complete CI pipeline (lint, coverage, all tests, all dynamic analysis).

## Code Formatting

- `make fmt` - Format all source code using uncrustify with project style guide.
- `make tags` - Generate ctags index for source code navigation.
- `make cloc` - Count lines of code in source, tests, and Makefile.

## Distribution

- `make dist` - Create source distribution tarball for packaging.
- `make distro-images` - Build Docker images for all supported distributions.
- `make distro-images-clean` - Remove all Docker images for supported distributions.
- `make distro-clean` - Clean build artifacts using Docker container.
- `make distro-check` - Run full CI checks on all supported distributions via Docker.
- `make distro-package` - Build distribution packages (deb, rpm) for all supported distributions.

## Utility

- `make help` - Display detailed help for all available targets and build modes.
- `make clean-test-runs` - Remove test run sentinel files used for parallel execution.

## Build Modes

| Mode | Flags | Purpose |
|------|-------|---------|
| `BUILD=debug` | `-O0 -g3 -DDEBUG` | Default build with full debug symbols and no optimization |
| `BUILD=release` | `-O2 -g -DNDEBUG -D_FORTIFY_SOURCE=2` | Optimized production build with security hardening |
| `BUILD=sanitize` | `-O0 -g3 -fsanitize=address,undefined` | Debug build with address and undefined behavior sanitizers |
| `BUILD=tsan` | `-O0 -g3 -fsanitize=thread` | Debug build with thread sanitizer for race detection |
| `BUILD=valgrind` | `-O0 -g3 -fno-omit-frame-pointer` | Debug build optimized for Valgrind analysis |

## Common Workflows

```bash
# Development workflow
make clean && make all               # Clean build in debug mode
make check                           # Run all tests
make fmt                             # Format code before commit

# Single test execution
make check TEST=config_test          # Run only config_test

# Quality assurance
make lint                            # Check complexity and file sizes
make check-coverage                  # Generate coverage report
make check-dynamic                   # Run all sanitizers and Valgrind

# Release workflow
make release                         # Build optimized release binary
make ci                              # Run full CI pipeline

# Distribution workflow
make dist                            # Create source tarball
make distro-images                   # Build Docker images
make distro-package                  # Build deb/rpm packages

# Custom builds
make all BUILD=release               # Build in release mode
make check BUILD=sanitize            # Run tests with sanitizers
make check-coverage COVERAGE_THRESHOLD=95  # Require 95% coverage

# Distribution testing
make distro-check DISTROS="debian"   # Test only on Debian
make distro-package DISTROS="fedora ubuntu"  # Build packages for specific distros

# Parallel execution
make -j8 check                       # Run tests with 8 parallel jobs
make check-dynamic PARALLEL=1        # Run sanitizers in parallel

# VCR fixture recording
VCR_RECORD=1 make check-unit         # Re-record fixtures during test run
make vcr-record-openai               # Re-record all OpenAI fixtures
```

## Important Notes

- Never run parallel make with different targets - different BUILD modes use incompatible flags.
- Always stay in project root - use relative paths instead of changing directories.
- Default BUILD mode is debug; specify BUILD=release for optimized builds.
- Coverage requires 100% line, function, and branch coverage by default.
- Maximum file size is 16384 bytes for all non-vendor source and documentation files.
- Cyclomatic complexity threshold is 15, nesting depth threshold is 5.
- Vendor files (yyjson, fzy) compile with relaxed warnings.
- Test binaries support parallel execution using .run sentinel files.
- Signal tests are skipped when running with sanitizers (SKIP_SIGNAL_TESTS=1).
