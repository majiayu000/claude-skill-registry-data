---
name: replan
description: Iterative deep planning with critiques and alternatives. Use when facing complex design decisions, cross-platform changes, native module modifications, or API changes requiring thorough analysis.
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# Replan

You are going to **replan** - an iterative process of designing, critiquing, and refining a plan.

## Required Reading First

Before planning, read and internalize the relevant project documentation:

- **CLAUDE.md** — project conventions, critical knowledge, anti-patterns, and CI/CD constraints
- **CONTRIBUTING.md** — development setup, pre-commit checklist, npm script naming conventions
- **doc/gotchas.md** — platform-specific quirks, timeout issues, testing pitfalls
- When touching native C++ code, also read the relevant platform API reference:
  - **doc/MACOS_API_REFERENCE.md**, **doc/LINUX_API_REFERENCE.md**, **doc/WINDOWS_API_REFERENCE.md**

## Process

### 1. Understand & Clarify

- Read relevant code, documentation, and constraints
- State any assumptions you're making
- Ask clarifying questions before proceeding
- Identify which platforms are affected (Windows, macOS, Linux)

### 2. Initial Plan

Design your first approach, considering requirements and existing solutions.

### 3. Critique

Generate thorough critiques of your plan:

#### General Engineering

- Does it balance simplicity with good engineering?
- Is it maintainable, testable, DRY, scalable?
- Scrutinize for "hand-wavy" aspects - don't assume how things work, study the code
- For novel libraries/APIs, validate with web searches
- Note uncertainties as risks

#### Cross-Platform Correctness

- Does this work on all three platforms (Windows, macOS, Linux)?
- Are there platform-specific API differences that need separate implementations?
- Have you verified API availability against target OS versions?
- Does Alpine Linux (musl libc) need special handling?
- Will this work under ARM64 emulation (5x slower) and in CI environments?

#### Security & Memory Safety

- Does the change follow RAII patterns for all resource management?
- Are there path traversal, null byte injection, or TOCTOU risks?
- Is thread safety maintained? (GVolumeMonitor is NOT thread-safe; DiskArbitration requires dispatch queues)
- Are all platform API return values checked and errors handled?
- Does string conversion handle overflow and encoding errors?

#### Backwards Compatibility

- Does this break the existing public API surface?
- Will existing consumers need code changes?
- Are new fields additive (not removing or renaming existing ones)?
- Does the TypeScript interface remain compatible?
- Will prebuilt native binaries need rebuilding for all platforms?

#### Performance & Reliability

- Could this hang on network filesystems? Is there a timeout?
- Does this create threads appropriately? (Windows thread pool has a 5s shutdown timeout)
- Will this degrade CI reliability? (See platform performance multipliers in CLAUDE.md)
- Are tests deterministic and not dependent on dynamic filesystem state?

### 4. Alternatives

Brainstorm alternatives based on critiques. Goals:

- Simplify the plan
- Reduce complexity and risk
- Improve code quality and maintainability
- Minimize cross-platform divergence

### 5. Develop Best Alternative

Select the most promising alternative and develop it fully.

### 6. Iterate

Repeat steps 3-5 at least **three times**, asking for user feedback at each iteration.

### 7. Final Plan

Assemble the best features from all iterations into a robust final plan.

## Output Format

For each iteration, present options with pros/cons:

### Option A: [Name]

[Description]

**Pros:** ...
**Cons:** ...
**Risks:** ...
**Platforms affected:** ...

### Recommendation

[Which option and why]

## Design Principles

This project values (in priority order):

1. **Correctness** - Native APIs must be called correctly per official documentation. No assumptions.
2. **Safety** - RAII for all resources, no leaks, no UB, no TOCTOU. Security audit grade A.
3. **Cross-platform parity** - All three platforms must work. Platform-specific code goes in platform directories.
4. **Backwards compatibility** - Published npm package. Don't break consumers.
5. **Simplicity** - Prefer the simplest correct solution. Don't over-engineer.
6. **Zero runtime dependencies** - Solve with native APIs or Node.js stdlib. Don't pull in npm packages.
7. **Testability** - Tests must be deterministic and CI-reliable. Never assert exact values for dynamic filesystem properties.
8. **Performance** - Native module should be fast, but correctness and safety come first.
