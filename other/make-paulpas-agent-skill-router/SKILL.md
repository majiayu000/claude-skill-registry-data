---




name: make
description: Implements systematic build orchestration (Makefile, Nix, Bazel, Just)
  with dependency tracking, incremental compilation, phony targets, and cross-platform
  portability for reproducible software construction.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: make, build system, makefile, compilation, incremental build, build automation,
    justfile, phony targets
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: implementation
  output-format: code
  content-types:
  - code
  - guidance
  - do-dont
  - examples
  related-skills: testing, refactoring, ci-cd-pipelines




---




# Build Orchestration & Make Patterns

Implements systematic build orchestration to transform source artifacts into reliable, reproducible outputs. A well-designed build system is not just a collection of commands — it is the contract between developers and the compilation pipeline, enforcing correctness through dependency tracking, incremental execution, and explicit phony target separation. Follow the Unix philosophy (KISS) by keeping recipes focused, transparent, and composable.

## TL;DR Checklist

- [ ] Define all non-file targets as `.PHONY` explicitly
- [ ] Use automatic variables (`$@`, `$<`, `$^`) to avoid hardcoding file paths
- [ ] Ensure incremental builds work (changed file triggers correct recompilation, unchanged files skipped)
- [ ] Separate build steps into logical targets (clean, test, deploy, install)
- [ ] Validate cross-platform compatibility or use platform-specific conditionals
- [ ] Document required tools and environment variables at the top

---

## When to Use

Use this skill when:

- Creating a `Makefile` or similar build script for a new project
- Refactoring a chaotic build process into deterministic, incremental targets
- Diagnosing why a build system is rebuilding everything on every run
- Setting up standard development workflows (`make test`, `make lint`, `make deploy`)
- Migrating from ad-hoc shell scripts to structured dependency graphs

---

## When NOT to Use

Avoid this skill for:

- Complex multi-language monorepos with hundreds of microservices — use Bazel, Buck2, or Nx instead
- Projects already managed by a package manager's build hook (e.g., `npm run build`, `cargo build`) unless you need orchestration across multiple tools
- Pure runtime configuration — Make is for building artifacts, not managing deployment environments

---

## Core Workflow

1. **Map Dependencies** — List every input file and required external tool for each output artifact.
   **Checkpoint:** Every target must list its exact prerequisites; missing dependencies cause silent build failures.

2. **Define Phony Targets** — Mark all non-file targets (like `clean`, `test`, `install`) as `.PHONY` immediately.
   **Checkpoint:** If a file named `clean` or `test` exists, Make will skip the target without `.PHONY`.

3. **Write Pattern Rules** — Use `%` pattern rules and automatic variables to handle multiple similar targets without repetition.
   **Checkpoint:** Verify `$@`, `$<`, and `$^` resolve correctly before adding more source files.

4. **Test Incremental Builds** — Touch a single source file and verify only dependent targets rebuild.
   **Checkpoint:** No stale artifacts should remain; `make clean` must fully reset state.

5. **Enforce Exit Codes** — Every recipe step must propagate failures (`set -e` in shell recipes, explicit checks).
   **Checkpoint:** A failed linting or test step must abort the build immediately, not continue to packaging.

6. **Document & Standardize** — Add a `help` target showing available commands and required environment variables.
   **Checkpoint:** New developers should run `make help` and understand how to build, test, and clean without reading docs.

---

## Implementation Patterns / Reference Guide

### Pattern 1: Robust Makefile Structure

A production-ready Makefile separates concerns into logical targets, uses automatic variables, and enforces strict error handling.

```makefile
# Build configuration
CC ?= gcc
CFLAGS := -Wall -Wextra -O2 $(EXTRA_CFLAGS)
BUILDDIR := build
SRCDIR := src
TARGET := myapp

.PHONY: all clean test install help

all: $(BUILDDIR)/$(TARGET)

$(BUILDDIR)/$(TARGET): $(wildcard $(SRCDIR)/*.c)
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -rf $(BUILDDIR)

test: $(BUILDDIR)/$(TARGET)
	./run_tests.sh --target=$(BUILDDIR)/$(TARGET)

help:
	@echo "Available targets:"
	@echo "  all      - Build the application (default)"
	@echo "  clean    - Remove build artifacts"
	@echo "  test     - Run integration tests"
	@echo "  install  - Copy binary to /usr/local/bin"
```

### Pattern 2: Incremental Build with Pattern Rules (BAD vs. GOOD)

```makefile
# ❌ BAD — hardcodes paths, ignores incremental builds, rebuilds everything every time
build-app:
	gcc -o myapp src/main.c src/utils.c
	echo "Build complete"

clean:
	rm myapp

# ✅ GOOD — pattern rules with automatic variables, incremental dependency tracking
BUILDDIR := build
SRCS := $(wildcard src/*.c)
OBJS := $(patsubst src/%.c,$(BUILDDIR)/%.o,$(SRCS))
TARGET := $(BUILDDIR)/myapp

$(TARGET): $(OBJS)
	@mkdir -p $(dir $@)
	$(CC) $^ -o $@

$(BUILDDIR)/%.o: src/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILDDIR)

.PHONY: all clean test
all: $(TARGET)
```

### Pattern 3: Cross-Platform Tool Detection

Makefiles should gracefully detect available tools rather than assuming a specific environment.

```makefile
# Detect Python version (Unix vs. macOS vs. Windows)
PYTHON := python3
ifeq ($(OS),Windows_NT)
    PYTHON := python
endif

# Use `rm` with platform-safe flags
ifdef MSYSTEM
    RM_CMD := rm -rf
else
    RM_CMD := rm -rf
endif

clean:
	$(RM_CMD) build/ dist/ *.egg-info
```

---

## Constraints

### MUST DO
- Always declare non-file targets as `.PHONY` to prevent filename collisions
- Use automatic variables (`$@`, `$<`, `$^`) instead of hardcoding file paths in recipes
- Implement incremental builds — only rebuild what changed and its dependents
- Fail fast on errors using `set -e` or explicit exit checks in shell recipes
- Provide a `help` target documenting available commands for new contributors
- Use `?=` for user-overridable variables, `:=` for computed values

### MUST NOT DO
- Put `.PHONY` declarations after the targets they reference (Make processes them top-down)
- Hardcode absolute paths in recipes — use variables and automatic variables
- Mix build logic with deployment logic (keep packaging and CI separate from Make)
- Use `system()` or shell built-ins that behave differently across platforms without detection
- Ignore return codes — a failing test or lint step must abort the entire pipeline
- Nest `make` calls unnecessarily (`make -C subdir`) unless building a true multi-component project

---

## Output Template

When implementing or reviewing a build system, produce:

1. **Target Graph** — ASCII or bullet list showing target → prerequisites dependencies
2. **Makefile Snippet** — The exact file content with proper variables, pattern rules, and `.PHONY` declarations
3. **Incremental Test Result** — Verification that touching one source triggers only dependent rebuilds
4. **Error Handling Notes** — How failures are detected and propagated (set -e, explicit checks)
5. **Cross-Platform Coverage** — Identified platform-specific differences and how they're resolved

---

## Related Skills

| Skill              | Purpose                                        |
|--------------------|------------------------------------------------|
| `testing`          | Define test targets and integrate into build flow |
| `refactoring`      | Restructure legacy build scripts into modular patterns |
| `ci-cd-pipelines`  | Connect Make outputs to continuous deployment workflows |

## Live References

> Authoritative documentation links for this domain. The model follows markdown links at load time to resolve external references and inline content.

- [GNU Make Manual](https://www.gnu.org/software/make/manual/make.html) — The definitive GNU Make reference covering variables, patterns, functions, and implicit rules
- [GNU Make Best Practices (Google)](https://github.com/google/simhash/blob/master/Makefile) — Google's open-source Makefiles demonstrating idiomatic build script patterns
- [Just: A Command Runner](https://just.systems/man/en/) — Modern alternative to Make with improved syntax; useful for understanding build tool evolution
- [GNU Make vs Bazel vs Nix (Comparison)](https://blog.bazel.build/2019/02/07/nix-bazel-make.html) — Bazel blog post comparing modern build systems with traditional Make
- [Automating Builds with Make in CI (GitHub Actions)](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-with-make) — GitHub Actions examples for running Make-based builds in CI/CD pipelines
