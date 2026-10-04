---
name: code-review
description: Comprehensive code review with distinct aspect based sections. Use when reviewing code, checking for security issues, finding type safety problems, auditing code quality, or when user asks to review code, PRs or changes. Three-phase workflow runs static tools, LLM judgment, and writes diagnostic log.
user-invocable: true
skills:
  - subagent-prompting
  - subagent-output-templating
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
version: 1.2.0
author: "Ashay Kubal @ Qball Inc."
---

# Code Review

Comprehensive code review with four independently-referenceable sections. Runs static tools first (fail fast), then applies LLM judgment for patterns tools cannot catch.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Code review | "Review this code", "Check my changes", "Code review for PR" |
| Security review | "Check for security issues", "Find vulnerabilities", "OWASP audit" |
| Type safety check | "Find any usage", "Check type safety", "Null handling issues?" |
| Quality check | "Is this code clean?", "Check code quality", "Standards compliance" |

**DO NOT use for:**
- Running tests (use `just test`)
- Auditing test quality (use `test-audit` skill)
- Debugging issues (use `issue-debugging` skill)
- Performance profiling (requires runtime analysis)

---

## Dependencies

This skill references supporting files. Understanding what's required vs optional ensures consistent execution.

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Pattern references** | `references/{section}-patterns.md` | **REQUIRED** | Always load for each enabled section |
| **Framework patterns** | `frameworks/{detected}.md` | **CONDITIONALLY REQUIRED** | If framework detected → MUST load; if not detected → skip |
| **Examples** | `examples/anti-patterns/*.ts`, `examples/recommended/*.ts` | OPTIONAL | For calibration on ambiguous cases; kept for model portability |
| **Diagnostic schema** | `references/diagnostic-schema.md` | **REQUIRED for Phase 3** | When emitting the diagnostic log (full schema, field rules, examples, Stage-5 aggregation) |

**Fallback behavior:**
- If framework detected → Loading `frameworks/{name}.md` is REQUIRED
- If no framework detected → Skip framework patterns entirely (do not load `generic.md`)
- If a referenced file is missing → Note in diagnostic log, continue with available patterns

---

## Usage

```
/code-review [path] [flags]
```

**Arguments:**
- `path` - File or directory to review (default: files in recent context)

**Flags:**
- `--quick` - Tiered review by change size (Security-only for <50 lines)
- `--framework=<name>` - Override auto-detected framework (react|express|django|generic)
- `--include-git-context` - Include git history for complexity findings
- `--section=<name>` - Run single section only (security|type-safety|linting|standards)

**Examples:**
- `/code-review src/auth/` - Full review of auth directory
- `/code-review src/api.ts --quick` - Quick review (tiered by lines)
- `/code-review src/ --section=security` - Security section only

---

## Three-Phase Workflow

**CRITICAL**: All three phases are REQUIRED. Do not skip any phase.

```
Phase 1: Static Analysis (Deterministic, language-aware)
├── For each file in scope, detect language from extension → run matching recipe(s):
│   ├── .ts/.tsx/.js/.jsx → just typecheck ; just lint
│   ├── .py               → just typecheck-py ; just lint-py
│   ├── .sh/.bash         → just lint          (shellcheck)
│   ├── .json             → just validate-json
│   ├── .yaml/.yml        → just validate-yaml
│   └── (other/unknown)   → just typecheck ; just lint  (project default)
├── Tool present AND reports problems → STOP, return to user (fail fast)
└── Tool absent (recipe prints "… not installed; skipping") → log warning, continue (graceful degrade)

Phase 2: LLM Review (Judgment-Based, applicability-gated)
├── Detect each file's language (extends Framework Detection — same mechanism, per-file)
├── For each (section, language): consult the Language Applicability table
│   ├── ✅ apply normally · partial apply + Caveat · ❌ skip (record skip_rationale)
├── Load references/{section}-patterns.md for each APPLIED section (REQUIRED)
├── If framework detected: Load frameworks/{detected}.md (REQUIRED)
├── If no framework detected: Skip framework patterns
├── Apply each applied section using loaded patterns
└── Output findings to user

Phase 3: Write Diagnostic Log (REQUIRED)
├── Write to: logs/diagnostics/code-review-{timestamp}.yaml
├── Include: invocation details, static analysis results, findings summary,
│            language_applicability (per-file applied/skipped sections)
└── This phase is MANDATORY - do not return to user without completing it
```

**Why Phase 1 First:**
- Saves tokens (don't analyze code that won't compile)
- Eliminates false positives (LLM doesn't rediscover tool findings)
- Fail fast on obvious issues

**Why Phase 3 is Required:**
- Enables pipeline orchestration to collect sub-agent outputs
- Provides observability for multi-agent workflows
- Creates audit trail for code review decisions

---

## Sections

Each section is independently referenceable by pipeline agents via `--section=<name>`.

### Quick Reference

| Section | Boundary | Key Patterns | Severity Range |
|---------|----------|--------------|----------------|
| Security | Threats & exploits | OWASP Top 10, injection, auth | Critical-Important |
| Type Safety | Type system holes | `any`, null, unsafe assertions | Critical-Important |
| Linting | Style requiring judgment | Complexity, naming, structure | Important-Suggestion |
| Coding Standards | Conventions & architecture | Patterns, documentation | Important-Suggestion |

### Language Applicability

Not every section applies to every language. Before running a section on a file, detect the file's language (see [Framework Detection](#framework-detection)) and consult this table. This prevents hallucinated findings (e.g., "type safety" on a bash script) and wasted passes.

| Section | TS/JS | Python | Bash | JSON/YAML | Rust | Go | Java/Kotlin | Reason |
|---------|-------|--------|------|-----------|------|-----|-------------|--------|
| **Security** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OWASP concepts are language-agnostic |
| **Type Safety** | ✅ | partial | ❌ | ❌ | ✅ | ✅ | ✅ | TS/Python/Rust/Go/JVM have type systems; bash + data formats don't |
| **Linting** | ✅ | ✅ | ✅ if shellcheck | partial | ✅ if clippy | ✅ if golangci-lint | ✅ if ktlint | Always conceptually applicable; tool varies |
| **Coding Standards** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | CS1–CS4 from Rules.md are language-agnostic |

**Section-selection rule** — for each file in scope:
1. Detect language from file extension (this extends [Framework Detection](#framework-detection) — same mechanism, file-level granularity).
2. For each of the 4 sections, look up the (section, language) cell:
   - **✅** — apply the section normally.
   - **partial** — apply with reduced scope and attach a `Caveat` to any finding (e.g., Python type hints are optional, not enforced; data formats have schema-shaped structure, not a type system).
   - **❌** — skip the section; record the file + skipped section in the Phase 3 diagnostic's `language_applicability.sections_skipped` with a `skip_rationale`.
3. Record applied + skipped sections per file in the Phase 3 diagnostic (`language_applicability` field — see [Diagnostic Output](#diagnostic-output-required)).

---

## Security

### Purpose
Identify security vulnerabilities that static analysis cannot catch.

### Boundary
Threats and exploits: authentication/authorization logic, injection patterns, secrets exposure, CSRF, CORS misconfigurations.

**Does NOT cover:** Type errors (→ Type Safety), code style (→ Linting).

### Prerequisites
- `just typecheck` passed
- `just lint` passed

### Patterns (REQUIRED)
Load `references/security-patterns.md` for:
- OWASP Top 10 checklist with detection criteria
- Framework-specific patterns (from `frameworks/{detected}.md` if framework detected)

### Examples (OPTIONAL - for calibration)
Reference when encountering ambiguous cases:
- Anti-patterns: `examples/anti-patterns/security.ts`
- Recommended: `examples/recommended/security.ts`

### What to Skip (Common False Positives)
- Parameterized queries flagged due to nearby string concatenation
- Test fixtures with intentional "vulnerable" code
- Comments containing SQL/code examples
- Sanitization already applied upstream

### Output Requirements
- confidence: verified | suspected
- evidence: Data flow trace or pattern match
- owasp: Category reference (e.g., A03:2021-Injection)

---

## Type Safety

### Purpose
Identify type system holes that bypass compile-time safety.

### Boundary
Type system integrity: explicit `any`, implicit any from missing types, unsafe type assertions, null/undefined handling gaps.

**Does NOT cover:** Runtime errors from logic bugs (→ tests), security issues (→ Security).

### Prerequisites
- `just typecheck` passed (confirms type-correct, looking for holes)

### Patterns (REQUIRED)
Load `references/type-safety-patterns.md` for:
- `any` usage patterns (explicit, implicit, from libraries)
- Null handling patterns (optional chaining gaps, assertion misuse)
- Unsafe assertion patterns (as unknown as T, non-null assertion operator)

### Examples (OPTIONAL - for calibration)
Reference when encountering ambiguous cases:
- Anti-patterns: `examples/anti-patterns/type-safety.ts`
- Recommended: `examples/recommended/type-safety.ts`

### What to Skip (Common False Positives)
- `any` in test fixtures for flexibility
- `any` in JSON parsing with immediate validation
- Third-party library types that require `any`
- Intentional `as const` assertions

### Output Requirements
- pattern: any_explicit | any_implicit | null_gap | unsafe_assertion
- location: Precise line and column

---

## Linting

### Purpose
Identify code quality issues requiring human judgment beyond what automated linters catch.

### Boundary
Style and structure requiring judgment: cyclomatic complexity, semantic naming, deep nesting, code duplication, unclear control flow.

**Does NOT cover:** Formatting (automated), syntax (compiler), security (→ Security).

### Prerequisites
- `just lint` passed (catches automatable issues)

### Patterns (REQUIRED)
Load `references/linting-patterns.md` for:
- Complexity thresholds (cyclomatic, nesting depth, function length)
- Naming anti-patterns (single letters, generic names, misleading names)
- Structure anti-patterns (god functions, mixed concerns)

### Examples (OPTIONAL - for calibration)
Reference when encountering ambiguous cases:
- Anti-patterns: `examples/anti-patterns/linting.ts`
- Recommended: `examples/recommended/linting.ts`

### What to Skip (Common False Positives)
- Intentionally complex algorithms with comments
- Generated code with unusual patterns
- Legacy code explicitly marked for future refactoring
- Single-letter variables in tight loops (`i`, `j`, `k`)

### Git Context (Optional)
When `--include-git-context` is enabled, include for complexity findings:
```yaml
git_context:
  last_modified: "2025-08-15 by @alice"
  commit_message: "Workaround for #1234"
  note: "Complexity may be intentional - verify before refactoring"
```

### Output Requirements
- pattern: deep_nesting | long_function | generic_naming | god_function
- metrics: Quantitative values where applicable (nesting level, line count)

---

## Coding Standards

### Purpose
Verify adherence to project conventions and architectural patterns.

### Boundary
Conventions and architecture: atomic principles (single responsibility, explicit I/O), documentation quality, pattern adherence, consistency with codebase.

**Does NOT cover:** Style formatting (→ linters), security patterns (→ Security).

### Prerequisites
- Code compiles and passes lint

### Patterns (REQUIRED)
Load `references/standards-patterns.md` for:
- Atomic principles checklist (CS1-CS4 from Rules.md)
- Documentation requirements (when to document, JSDoc format)
- Pattern consistency checks

### Examples (OPTIONAL - for calibration)
Reference when encountering ambiguous cases:
- Anti-patterns: `examples/anti-patterns/standards.ts`
- Recommended: `examples/recommended/standards.ts`

### What to Skip (Common False Positives)
- Prototype/experimental code explicitly marked
- Third-party integration code matching external patterns
- Auto-generated code (migrations, schemas)

### Output Requirements
- principle: cs1_single_responsibility | cs2_no_magic | cs3_fail_fast | cs4_clean_code
- reference: Link to documentation or pattern definition

---

## Framework Detection

Auto-detect framework from project files. **If detected, loading framework patterns is REQUIRED.**

### Detection Logic

```
package.json dependencies → Framework
─────────────────────────────────────
react, next, gatsby       → react
express, fastify, koa     → express
@angular/core             → angular
vue, nuxt                 → vue

requirements.txt / pyproject.toml:
django                    → django
flask                     → flask
fastapi                   → fastapi

(none of above)           → (no framework)
```

### Language Detection (Per-File)

Framework detection above is **project-level** (which `frameworks/{name}.md` to load). Language detection is **file-level**: it drives the Phase 1 recipe to run and the Language Applicability lookup (which sections apply). It **extends** this mechanism — same detection pass, finer granularity — rather than introducing a parallel detection paradigm.

```
extension                        → language
──────────────────────────────────────────────
.ts .tsx .js .jsx .mjs .cjs      → typescript/javascript
.py .pyi                         → python
.sh .bash                        → bash
.json                            → json   (data format)
.yaml .yml                       → yaml   (data format)
.rs                              → rust
.go                              → go
.java .kt .kts                   → java/kotlin
(unrecognized)                   → project default (apply all sections)
```

For each file: detect language → run the matching Phase 1 recipe → gate each section through the [Language Applicability](#language-applicability) table.

### Override
Use `--framework=<name>` to override detection.

### Fallback Behavior
If no framework is detected:
- **Do NOT load `generic.md`** - skip framework patterns entirely
- Continue with core patterns from `references/*.md` files (which are REQUIRED)
- Note in diagnostic log that framework-specific checks were skipped

---

## Quick Mode

When `--quick` flag is specified, sections are tiered by lines changed:

| Lines Changed | Sections Run |
|---------------|--------------|
| <50 lines | Security only |
| 50-500 lines | Security + Type Safety |
| >500 lines | All sections |

**Default (no flag):** All sections (comprehensive review).

---

## Severity Tiers

| Tier | Label | Criteria | Action |
|------|-------|----------|--------|
| **CRITICAL** | Must fix before merge | Security vulnerabilities, type safety holes causing runtime errors | Block merge |
| **IMPORTANT** | Should fix | Anti-patterns, missing tests, significant quality issues | Address before or after merge |
| **SUGGESTION** | Optional | Style improvements, naming clarity, minor refactoring | Consider for future |

---

## Confidence Levels

| Level | Label | Criteria |
|-------|-------|----------|
| **Verified** | Data flow traced, exploit path confirmed | "User input from req.query.id flows to db.query at line 45 without sanitization" |
| **Suspected** | Pattern matches but context unclear | "String concatenation in SQL-like context - verify if this is actually a query" |

---

## Output Format

Output templates follow the `subagent-output-templating` skill (P0.2) structure with skill-specific extensions for code review findings.

### Direct Invocation
Use template from `templates/output-direct.yaml`:
- Summary with counts by severity
- Findings grouped by severity
- Each finding has: file, line, section, pattern, confidence, evidence, description, why, fix

### Pipeline Stage
Use template from `templates/output-pipeline.yaml`:
- Scoped to single section
- Findings list with severity
- Summary statement
- Gate pass/fail for pipeline orchestration

---

## Pipeline Integration

### As Full Auditor (bulwark-code-auditor)
```fsharp
bulwark-code-auditor
├── context: fork (isolated review)
├── skills: code-review
└── Runs all 4 sections, never fixes
```

### As Pipeline Stage (role-based)
```fsharp
SecurityReviewer (--section=security)
|> TypeSafetyReviewer (--section=type-safety)
|> LintReviewer (--section=linting)
|> StandardsReviewer (--section=standards)
|> ReviewSynthesizer (consolidate)
```

---

## Diagnostic Output (REQUIRED)

**MANDATORY**: You MUST write diagnostic output after every review. This is Phase 3 of the workflow and cannot be skipped.

**Standard**: Follows `subagent-output-templating` (P0.2) diagnostic format.

Write diagnostic output to:
```
logs/diagnostics/code-review-{timestamp}.yaml
```

The log MUST include these top-level fields:
- `diagnostic` — skill / timestamp / invocation / static_analysis / findings_summary.
- `reviewed_files` — flat list of reviewed paths relative to `${CLAUDE_PROJECT_DIR}` (Stop-hook per-file suppression contract; `[]` is valid, missing field = strict no-suppress).
- `language_applicability` (P10.21) — per-file `detected_language` + `sections_applied` / `sections_skipped` (+ `skip_rationale`); record `partial` by suffixing the section (e.g. `type_safety_partial`).
- `followup_edits_expected` (P10.22) — one entry per file with a `critical`/`important` finding; omit or `[]` for suggestions-only runs.

**Full schema, field rules, worked examples, and the pipeline Stage-5 aggregation algorithm live in [`references/diagnostic-schema.md`](references/diagnostic-schema.md) — load it when emitting Phase 3 output.**

---

## Completion Checklist

**IMPORTANT**: Before returning to the user, verify ALL items are complete:

- [ ] Phase 1: Static analysis ran (`just typecheck`, `just lint`)
- [ ] Phase 2: LLM review completed for all enabled sections
- [ ] Phase 2: Findings delivered to user (console output)
- [ ] Phase 3: Diagnostic log written to `logs/diagnostics/code-review-{timestamp}.yaml`

**Do NOT return to user until all checkboxes can be marked complete.**
