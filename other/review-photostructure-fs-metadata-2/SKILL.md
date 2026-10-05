---
name: review
description: Review code for potential issues and improvements. Use when asked to review specific files, functions, or code sections.
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, WebSearch
---

# Code Review

Review the mentioned code for potential issues and improvements.

## Before you start

Study the following project documents before reviewing:

- **AGENTS.md** — project conventions, critical knowledge, anti-patterns, and CI/CD constraints
- **CONTRIBUTING.md** — development setup, pre-commit checklist, npm script naming conventions
- **doc/gotchas.md** — platform-specific quirks, timeout issues, testing pitfalls
- **doc/C++\_REVIEW_TODO.md** — C++ review checklist (memory management, RAII, platform API usage, security validation)

Also check these configuration files for applicable rules:

- **eslint.config.mjs** — ESLint rules including security plugin
- **tsconfig.base.json** — strict TypeScript settings (`exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`, etc.)
- **.clang-tidy** — C++ static analysis checks (bugprone, performance, clang-analyzer)

**Only report verified bugs, things that are actually wrong.** Do NOT report:

- Speculative future risks ("if someone later removes this guard...")
- Feature requests or suggestions disguised as issues
- Things you haven't proven with concrete evidence from the codebase

For EVERY potential issue, you MUST complete these steps before reporting:

1. **Read the actual code** (not just the diff). Follow the full call chain
2. **Search for all callers/usages** to understand context
3. **Read any design docs or TPPs** that explain the rationale
4. **Construct a concrete failing scenario.** If you can't describe
   exactly how the bug manifests, it's not an issue
5. **Discard it** if your research shows it's intentional or already handled

**Use subagents liberally:**

- **Exploration**: When more than three files need review, or the code is
  complex, launch Explore subagents (one per file/area) to gather findings
- **Validation**: Before reporting ANY issue, launch a subagent to verify
  it. Have it trace the full call chain, search for guards/handlers you
  might have missed, and read relevant design docs. If the subagent can't
  confirm the bug, discard the issue
- **Iteration**: After your initial analysis, launch a second round of
  subagents to dig deeper into the most promising findings. Check edge
  cases, race conditions, and interaction effects between changed files

If you find zero real issues after thorough research, say "No issues found."
Do not pad the list.

## What to look for

**Correctness**

- Logic or implementation errors
- If correct but surprising, suggest a clearer equivalent or a comment
- Don't trust docs or implementation as authoritative. If they disagree,
  flag it, consider what you think is correct (it may be neither!), and
  explain your reasoning

**Code quality**

- Violations of project design principles or coding standards
- Dead code (suggest deleting it)
- Comments that merely restate the function name (suggest removing)

**Cross-platform safety**

- C++ code must use RAII for all resource management (no raw malloc/free, no
  leaked CoreFoundation refs, no unclosed handles)
- Path handling must account for platform differences (UNC paths on Windows,
  symlinks, mount points)
- Native code must use Node-API v9 correctly (proper ref counting, error
  propagation, async worker lifecycle)

**Security**

- Path traversal or injection vulnerabilities (verify realpath/canonicalization)
- Buffer overflows or integer overflow in string conversions
- Unsafe use of child_process, eval, non-literal require (per eslint-plugin-security)
- Thread safety issues in C++ (std::atomic vs volatile, data races)

**Refactoring**

- Duplicated logic across platform implementations that could be shared
- Overly complex functions that should be decomposed
- Abstractions that no longer fit (or missing abstractions that cause repeated code)
- Do NOT flag naming preferences or stylistic choices

**Testing gaps**

- Missing coverage for critical paths or edge cases
- Tests that use anti-patterns from AGENTS.md (arbitrary timeouts, forcing GC,
  setImmediate in afterAll)
- Dynamic filesystem values tested with exact equality instead of type checks
- Missing Windows retry logic for directory cleanup

**TypeScript strictness**

- Code must compile under the project's strict settings (exactOptionalPropertyTypes,
  noUncheckedIndexedAccess, etc.)
- No inline imports — use standard top-level imports
- Scripts must be `.ts` executed with `tsx`, never `.js`/`.mjs`/`.cjs`

## Response format

1. Completely omit any issues that are irrelevant after research and analysis.
2. Sort remaining issues by severity (Critical > High > Medium > Low).

For each issue use a short ID (e.g. `#A`, `#B`) and include:

- **Priority**: Critical / High / Medium / Low
- **Problem**: What's wrong, why, and the concrete scenario where it fails
- **Proof**: The specific code path or test that demonstrates the bug
- **Solution**: A concrete fix
- **Location**: File and line reference

Emit detailed findings, and then use `AskUserQuestion` with checkboxes for each item so the user can
accept, veto, or comment on each one individually.
