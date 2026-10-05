---
name: deslop
description: Audit and harden existing codebases (especially AI-generated / vibe-coded ones) for production readiness. Use when the user asks to review, audit, clean up, harden, deslop, refactor, or fix quality issues across an existing codebase. Works in two phases — first a thorough multi-pass audit written to a structured file, then systematic fixes applied in safety-tiered order. Language-agnostic. Does NOT change business logic — only hardens, cleans, and robustifies.
---

# Deslop — Code Hardening Skill

Systematically audit and harden an existing codebase for production. Designed for AI-generated ("vibe coded") codebases that work superficially but are fragile, sloppy, or insecure under real-world conditions.

**This skill operates in two strict phases. Never mix them.**

```
Phase 1: AUDIT   →  produces  AUDIT.md  (human-reviewable, machine-parseable)
Phase 2: FIX     →  consumes  AUDIT.md  →  applies fixes in safety order
```

The user provides a codebase (directory path or repo). They may specify focus areas, exclusions, or constraints. If not specified, audit everything.

---

## Phase 1: AUDIT

**MANDATORY before starting**: Read the full audit checklist and format spec:
```
Read ~/.claude/skills/deslop/references/checklist.md     # 15-category audit checklist with specific patterns
Read ~/.claude/skills/deslop/references/audit-format.md  # Structured finding format for AUDIT.md
```

The audit runs five sequential passes. Each pass builds on the previous. Never skip a pass — thoroughness matters more than speed.

### Pass 0 — Reconnaissance

Map the codebase before judging anything. Do NOT write findings yet.

1. **Generate file tree**: `find . -type f | head -500` or equivalent. Understand the shape.
2. **Classify files**: Source, tests, configs, migrations, infra, docs, generated, vendored.
3. **Identify the stack**: Language(s), framework(s), package manager, build system, runtime.
4. **Build dependency map**: Which files import from which. Use `grep -rn "import\|require\|from\|include"` or language-specific tooling.
5. **Identify entry points**: Main files, route handlers, API endpoints, CLI entry points, event handlers.
6. **Detect existing tooling**: Check for `.eslintrc`, `pyproject.toml`, `tsconfig.json`, `.prettierrc`, `Makefile`, CI configs, etc.
7. **Run available linters**: If linters are configured, run them and capture output. If not, note this as a finding. Common commands:
   - JS/TS: `npx eslint . --format json 2>/dev/null` or `npx tsc --noEmit 2>&1`
   - Python: `python -m pylint **/*.py --output-format=json 2>/dev/null` or `python -m flake8 . 2>&1`
   - Go: `go vet ./... 2>&1`
   - Rust: `cargo clippy --message-format=json 2>/dev/null`
   - If no linter is configured, skip — don't install new tooling unless asked.
8. **Produce the codebase map**: Write a structured summary to the top of `AUDIT.md`:
   - Stack summary (language, framework, runtime)
   - File count by category
   - Module/directory architecture
   - Entry points
   - High-coupling modules (most imports in + out)
   - Linter output summary (if available)

**Output of Pass 0**: The "Codebase Overview" section of `AUDIT.md`. No findings yet.

### Pass 1 — Patterns & Consistency

Scan for mechanical quality issues that don't require deep semantic understanding. Process file-by-file, prioritizing high-coupling modules first (from Pass 0's dependency map).

**What to scan** (load `~/.claude/skills/deslop/references/checklist.md` categories 8-14):
- Naming convention violations and inconsistencies
- DRY violations — duplicated logic blocks, copy-pasted code
- Dead code — unused functions, unreachable branches, commented-out code, unused imports
- Magic numbers and hardcoded values
- Missing type annotations (for typed languages)
- Inconsistent patterns (e.g., callbacks in one file, promises in another)
- KISS/YAGNI violations — unnecessary abstractions, premature optimization
- Dependency issues — unused deps, circular imports

**Chunking strategy for large files (>500 lines)**: Read in function/class-sized chunks. Never split in the middle of a function. When analyzing a chunk, re-read the file's import header for context.

**For each finding**: Write it to `AUDIT.md` using the format from `~/.claude/skills/deslop/references/audit-format.md`.

### Pass 2 — Logic & Resilience

Trace critical paths through the code. This pass requires cross-file context.

**Start from entry points** identified in Pass 0. For each critical path:
1. Trace the happy path from input to output.
2. Then ask: what happens when each step fails?
3. Check every error handling point: is the error caught? Logged? Re-thrown? Swallowed?
4. Check edge cases: null/undefined inputs, empty collections, boundary values, concurrent access.
5. Check data validation at trust boundaries (user input, API responses, file reads, env vars).

**What to scan** (load `~/.claude/skills/deslop/references/checklist.md` categories 2-4):
- Correctness bugs: null derefs, off-by-one, race conditions, resource leaks, incorrect API usage
- Error handling: empty catches, swallowed exceptions, generic catches, missing async error handling, silent failures
- Business logic fragility: happy-path-only logic, missing edge cases, hardcoded business rules
- Regex hacks: patterns that pass test cases but fail on real-world input
- Async issues: unhandled promise rejections, missing await, callback hell without error propagation

**CRITICAL**: Do NOT flag business logic as "wrong" unless it's clearly a bug. The goal is resilience, not redesign. If you're unsure whether something is intentional behavior or a bug, flag it as `[NEEDS_CLARIFICATION]` and describe the concern.

### Pass 3 — Security

**What to scan** (load `~/.claude/skills/deslop/references/checklist.md` categories 1, 7):
- Injection: SQL injection, XSS, command injection, path traversal, SSRF
- Auth/Authz: missing checks, privilege escalation, broken session management
- Secrets: hardcoded API keys, tokens, passwords, connection strings in source
- Crypto: weak algorithms, insecure random, missing HTTPS enforcement
- Input validation: missing server-side validation, inconsistent validation across endpoints
- Data exposure: sensitive data in logs, verbose error messages to clients, PII leaks
- Dependencies: known CVE in dependencies (check lock files if present)

Use OWASP Top 10 as the mental framework. For each finding, note the CWE number if applicable.

### Pass 4 — Synthesis & Prioritization

After all passes complete:

1. **Deduplicate**: Some findings may appear in multiple passes. Merge them, keeping the most severe classification.
2. **Cross-reference**: A DRY violation might also be a security concern (divergent validation logic). Link related findings.
3. **Classify severity** for every finding:
   - **CRITICAL**: Direct security vulnerabilities, data loss risk, crashes in core paths
   - **HIGH**: Logic errors with production impact, missing auth checks, resource leaks
   - **MEDIUM**: Missing validation, performance issues, significant code smells
   - **LOW**: Minor inconsistencies, naming issues, missing docs
   - **INFO**: Style suggestions, optimization opportunities, nice-to-haves
4. **Assign fix tier** (from `~/.claude/skills/deslop/references/fix-playbook.md`):
   - **Tier 1** (safe): No behavioral change possible. Formatting, dead code removal, renaming, type annotations.
   - **Tier 2** (medium): Additive changes. Input validation, error handling, logging. Needs characterization tests.
   - **Tier 3** (high risk): Structural changes. Refactoring APIs, changing data access patterns. Needs human review.
5. **Write the executive summary** at the top of `AUDIT.md`:
   - Total findings by severity
   - Top 5 most critical issues with one-line descriptions
   - Overall assessment: is this codebase production-ready? What's the blast radius of the issues found?
   - Estimated fix effort by tier

6. **Present `AUDIT.md` to the user.** Ask if they want to proceed to Phase 2, adjust priorities, or exclude anything.

---

## Phase 2: FIX

**MANDATORY before starting**: Read the fix playbook:
```
Read ~/.claude/skills/deslop/references/fix-playbook.md  # Safety hierarchy, characterization tests, fix ordering
```

**NEVER start Phase 2 without user confirmation on the audit.** The user must review `AUDIT.md` first.

### Fix Ordering

Process findings in this exact order:
1. **Tier 1 fixes, CRITICAL severity first** → safest changes, highest impact
2. **Tier 1 fixes, remaining severities** → clear out all safe mechanical fixes
3. **Tier 2 fixes, CRITICAL severity** → write characterization tests first, then fix
4. **Tier 2 fixes, HIGH severity** → same pattern
5. **Tier 2 fixes, MEDIUM and below** → same pattern
6. **Tier 3 fixes** → flag for human review, do NOT auto-fix unless user explicitly approves each one

### Fix Protocol

For every fix:

1. **State the finding ID** (e.g., `SEC-003`) so the user can cross-reference `AUDIT.md`.
2. **For Tier 2+**: Write a characterization test FIRST that captures current behavior. Run it. It must pass.
3. **Apply the fix.** Prefer mechanical transformations (rename, extract, inline) over generative rewrites. If you're rewriting more than ~20 lines, stop and reconsider — you might be changing business logic.
4. **Run the characterization test again.** It must still pass (unless the fix intentionally changes error handling from "silent failure" to "explicit error", in which case update the test).
5. **Run existing tests** if they exist. Nothing should break.
6. **Update `AUDIT.md`**: Mark the finding as `[FIXED]` with a one-line description of what changed.

### Fix Guardrails

**NEVER do any of these during fixes:**
- Change business logic, pricing, billing, or domain rules
- Modify public API contracts (URL paths, request/response shapes, function signatures used by external callers)
- Delete or rewrite tests (you can ADD tests, never remove them)
- Install new dependencies without asking the user
- Rewrite working code just because you'd "write it differently"
- Batch-apply more than one Tier 2+ fix at a time without running tests between
- Assume you know what the user intended — when in doubt, mark `[NEEDS_CLARIFICATION]` and move on

**ALWAYS do these:**
- Keep the application in a deployable state after every individual fix
- Preserve all existing tests in passing state
- Add comments explaining WHY a fix was made (not what — the diff shows that)
- Use the project's existing code style and conventions (detected in Pass 0)
- Prefer the project's existing patterns over "better" patterns from elsewhere

### After All Fixes

1. Run the full test suite (if one exists).
2. Run linters (if configured).
3. Update `AUDIT.md` with a final status section showing: fixed count, skipped count, needs-clarification count, needs-human-review count.
4. Present the summary to the user.

---

## Handling Large Codebases

For codebases with 50+ files or 10,000+ lines:

- **Pass 0 is even more critical.** Spend extra time building the codebase map. Identify the "core" (most-connected modules) vs "periphery" (leaf modules, utilities).
- **Prioritize by connectivity.** Audit core modules first — bugs there have the largest blast radius.
- **Use scripts for mechanical scanning.** Run `bash ~/.claude/skills/deslop/scripts/scan_dead_code.sh` and `bash ~/.claude/skills/deslop/scripts/scan_patterns.sh` to accelerate Pass 1 findings. Review their output rather than manually grepping every file.
- **Use dependency mapping.** Run `bash ~/.claude/skills/deslop/scripts/scan_dependencies.sh` during Pass 0 to build the dependency graph automatically.
- **Chunk Pass 2 by critical path.** Don't try to trace every possible path. Focus on: authentication flow, main CRUD operations, payment/billing (if any), data export/import, and any path that handles sensitive data.
- **Fix periphery first.** During Phase 2, fix leaf modules before core modules. Lower blast radius, and fixes in leaf modules sometimes resolve findings in core modules (e.g., adding validation in a utility function used by core).

---

## Asking Questions

The skill should ask the user questions in these situations:
- **Before starting**: "I'll audit the codebase at `[path]`. Any areas to focus on or exclude?"
- **During Pass 2**: When you encounter something that might be intentional behavior or might be a bug, flag it as `[NEEDS_CLARIFICATION]` in the audit file and batch all clarification questions for the user between Pass 2 and Pass 3.
- **Before Phase 2**: Always. "Here's the audit. Want to proceed with fixes? Any findings to skip or reprioritize?"
- **During Tier 3 fixes**: Each one individually. "This fix would change [specific thing]. Approve?"

Never ask about Tier 1 fixes — just do them. They're safe by definition.

---

## What This Skill Is NOT

- Not a test-writing skill (though it writes characterization tests as a safety mechanism)
- Not a feature-building skill (it never adds new functionality)
- Not a migration tool (it doesn't change frameworks, languages, or architectures)
- Not a style enforcer (it uses the project's existing style, not an external standard)
- Not a replacement for manual security audit (it catches common issues but is not exhaustive)

The single goal: **make the existing codebase more robust, maintainable, and production-ready without changing what it does.**
