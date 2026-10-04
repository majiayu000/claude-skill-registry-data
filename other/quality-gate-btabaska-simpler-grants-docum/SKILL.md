---
name: Quality Gate Pipeline
description: Multi-gate validation pipeline that runs Compound Engineering specialists against generated code. Used by all agents after code generation to ensure convention compliance, language quality, domain correctness, and architectural fit. Can be invoked standalone to validate any code change.
---

## When to Use

Invoke this skill after any code generation or modification to validate quality. All agents should reference this skill instead of inlining their own quality gate pipeline.

## Step-by-Step Instructions

### Step 1: Determine Applicable Gates

Based on the code domain and change type, determine which gates to run:

| Gate | When | Specialist | Required? |
|------|------|-----------|-----------|
| Convention Compliance | Always | `codebase-conventions-reviewer` | Yes |
| Language Quality | Always | `kieran-python-reviewer` and/or `kieran-typescript-reviewer` | Yes |
| Domain-Specific | Based on domain | See specialist map | Yes |
| Code Simplicity | Always | `code-simplicity-reviewer` | Yes |
| Pattern Consistency | Multi-file changes | `pattern-recognition-specialist` | Conditional |
| Architecture | Structural changes | `architecture-strategist` | Conditional |
| Security | Auth/input handling | `security-sentinel` | Conditional |
| Performance | Query/render paths | `performance-oracle` | Conditional |
| Data Integrity | DB changes | `data-integrity-guardian` | Conditional |

### Step 2: Run Mandatory Gates (in parallel)

Run these three gates simultaneously:

**Gate 1: Convention Compliance**
- Invoke `codebase-conventions-reviewer`
- Check: naming, file placement, import patterns, code structure, ALWAYS/NEVER/MUST directives
- If violations found: fix before proceeding

**Gate 2: Language Quality**
- Python files → invoke `kieran-python-reviewer`
- TypeScript files → invoke `kieran-typescript-reviewer`
- Both languages → invoke both in parallel
- Check: idiomatic patterns, type safety, error handling, edge cases

**Gate 3: Code Simplicity**
- Invoke `code-simplicity-reviewer`
- Check: unnecessary complexity, YAGNI violations, simplification opportunities

### Step 3: Run Domain-Specific Gates

Based on the code domain, run the appropriate specialist(s). See `specialist-map.md` for the complete mapping.

### Step 4: Run Conditional Gates

If applicable based on the change type:
- **Pattern Consistency**: For multi-file changes or extract/consolidate refactors
- **Architecture**: For structural changes (new files, new patterns, changed interfaces)
- **Security**: For auth-related or input-handling changes
- **Performance**: For database queries, pagination, search, or render-heavy components
- **Data Integrity**: For database model or migration changes

### Step 5: Fix and Re-validate

If any gate finds issues:
1. Fix the issues
2. Re-run ONLY the gates that failed
3. Repeat until all gates pass

## Conventions and Best Practices

- Run mandatory gates in parallel for speed
- Domain-specific gates can run in parallel with mandatory gates
- Conditional gates should run after mandatory gates pass
- Always fix issues before presenting output to the developer
- Merge duplicate findings from overlapping specialists into single, actionable items
