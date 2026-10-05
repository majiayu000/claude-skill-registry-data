---
name: tpp
description: Work on a Technical Project Plan. Use when starting complex features, cross-platform changes, native module modifications, or multi-session work that needs persistent context.
argument-hint: "[path-to-tpp]"
disable-model-invocation: false
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, WebSearch, Skill
---

# Work on TPP

Make progress on the referenced Technical Project Plan.
Determine the current phase and take appropriate action.

## Required Reading First

Before any work, you MUST read:

- **CLAUDE.md** — project conventions, critical knowledge, anti-patterns, and CI/CD constraints
- **CONTRIBUTING.md** — development setup, pre-commit checklist, npm script naming conventions
- **doc/gotchas.md** — platform-specific quirks, timeout issues, testing pitfalls
- **doc/TPP-GUIDE.md** — how TPPs work in this project
- When touching native C++ code, also read:
  - **doc/C++\_REVIEW_TODO.md** — memory management, RAII, platform API usage, security validation
  - The relevant platform API reference:
  - **doc/MACOS_API_REFERENCE.md**, **doc/LINUX_API_REFERENCE.md**, **doc/WINDOWS_API_REFERENCE.md**

## Process

1. Read the TPP from `_todo/`
2. Read all files listed in the TPP's "Required reading" section
3. Identify the current phase from the checklist
4. Do the work for that phase
5. Update the TPP with progress and discoveries
6. When a phase is complete, check off the phase and move to the next

## Phase-Specific Guidance

### Research & Planning

- Read relevant source code — don't guess how things work
- Check all three platform implementations (darwin/, linux/, windows/)
- Search for prior art in the codebase
- Validate assumptions about platform APIs with web searches
- Document findings in the TPP's Lore section

### Write Breaking Tests

- Write tests that demonstrate the problem or define the new behavior
- Tests must follow project conventions: no exact equality for dynamic values, no arbitrary timeouts
- Ensure tests are deterministic and CI-reliable across all platforms

### Design Alternatives

- Use the /replan skill for complex design decisions
- Document at least two options with pros/cons
- Consider cross-platform implications for every option
- Evaluate backwards compatibility impact
- Prefer zero runtime dependencies — solve with native APIs or stdlib, not npm packages

### Implementation

- Follow RAII for all native resource management
- Platform-specific code goes in platform directories (darwin/, linux/, windows/)
- Shared interfaces go in src/common/
- Run `npm run preflight` before declaring implementation complete

### Review & Refinement

- Use the /review skill to catch issues
- Verify all three platforms build and pass tests
- Check for memory leaks (see CLAUDE.md memory leak detection section)

## When Context Runs Low

If you're running low on context, run `/handoff` to persist your progress before the session ends.
