---
name: test-fixture-creation
description: Guidelines for creating unbiased test fixtures that integrate with project infrastructure. Use when creating fixtures for manual testing, setting up E2E test scenarios, or building code samples with deliberate issues for LLM review. Ensures fixtures work with hook automation and pass Phase 1 checks.
user-invocable: false
allowed-tools:
  - Bash
  - Edit
  - Glob
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Test Fixture Creation

Guidelines for creating test fixtures that work with Bulwark's hook-based automation and avoid bias that could compromise testing.

---

## When to Use This Skill

**Load this skill when:**
- Creating fixtures for manual testing of skills or agents
- Setting up E2E test scenarios that require hook automation
- Building code samples with deliberate issues for LLM review

**DO NOT use for:**
- Unit test fixtures (those can be isolated in tests/fixtures/)
- Mock data for automated tests
- Documentation examples

---

## Core Principles

### 1. No Bias in Fixtures

**CRITICAL**: Fixtures must not contain any indicators that they are test fixtures.

| Forbidden | Why | Alternative |
|-----------|-----|-------------|
| `test-*.ts`, `*-fixture.ts` | Filename reveals intent | `user-service.ts`, `data-processor.ts` |
| `// This is a test file` | Comment reveals intent | No explanatory comments |
| `// Intentional bug here` | Points to the issue | Let LLM discover it |
| `fixture/`, `test-data/` | Directory name reveals intent | `scripts/components/`, `lib/` |
| `FIXME`, `TODO: test` | Markers reveal intent | Remove all markers |

**Why this matters**: When Claude knows code is a test fixture, it may:
- Skip hook automation ("this is just a test")
- Ignore pipeline suggestions
- Produce different results than real code review

### 2. Project Infrastructure Integration

Fixtures must be placed within project infrastructure to enable hook automation.

**Required for hooks to fire:**
- Code must be in directories covered by `tsconfig.json` include paths
- Project must have working `just typecheck` and `just lint` recipes
- Fixtures must pass Phase 1 checks

**Placement Strategy:**
```
PROJECT_ROOT/
├── scripts/
│   ├── components/     ← Place fixtures here
│   │   ├── user-service.ts
│   │   ├── data-processor.ts
│   │   └── workflow-handler.ts
│   └── lib/            ← Supporting stubs
│       ├── database.ts
│       └── logger.ts
```

### 3. Fixtures Must Pass Phase 1

Fixtures should compile and lint successfully so that Phase 2 (LLM review) can run.

**Phase 1 Requirements:**
- `just typecheck` passes (no TypeScript errors)
- `just lint` passes (no lint errors)
- All imports resolve

**Common Issues:**
| Problem | Solution |
|---------|----------|
| Missing Node.js types | Avoid `fs`, `events`, `Buffer` - use pure TS |
| Import resolution | Create stub files in `scripts/lib/` |
| Type errors | Use `as unknown as T` for intentional unsafe casts |

### 4. Deliberate Issues for Phase 2

Fixtures should contain issues that TypeScript allows but are bad practice:

**Security Issues (user-service.ts):**
- SQL injection via string interpolation
- Hardcoded API keys and secrets
- Path traversal vulnerabilities
- Insecure token generation

**Type Safety Issues (data-processor.ts):**
- Excessive `any` in properties and parameters
- Unsafe type assertions (`as unknown as T`, `as any`)
- Missing return types

**Linting Issues (workflow-handler.ts):**
- Single-letter function names (`p`, `x`, `z`)
- Generic variable names (`s`, `d`, `c`, `i`, `r`)
- Deep nesting (8+ levels)
- High cyclomatic complexity

**Coding Standards Issues (config-manager.ts):**
- Multiple responsibilities in one file
- Global mutable state
- Implicit side effects (auto-initialization)
- Mixed concerns in functions

---

## Fixture Creation Workflow

### Step 1: Plan Fixture Structure

```
1. Identify skill/agent sections to test
2. Map each section to a fixture file
3. Plan deliberate issues for each file
4. Identify supporting stubs needed
```

### Step 2: Create Supporting Infrastructure

```typescript
// scripts/lib/database.ts - Stub for database imports
export interface QueryResult {
  rows: Record<string, unknown>[];
}

export const db = {
  async query(sql: string): Promise<QueryResult> {
    return { rows: [] };
  }
};
```

### Step 3: Create Fixture Files

```typescript
// scripts/components/user-service.ts
// NO comments explaining this is a test!
// File looks like production code

import { db } from '../lib/database';

const API_KEY = 'sk_live_...';  // Hardcoded secret

export async function getUserByEmail(email: string) {
  const query = `SELECT * FROM users WHERE email = '${email}'`;  // SQL injection
  // ... rest of realistic code
}
```

### Step 4: Verify Phase 1 Passes

```bash
# Must pass before creating test cases
just typecheck
just lint
```

### Step 5: Create Test Protocol

Use conversational, non-developer prompts:

```markdown
**Prompt** (conversational):
I just joined the team and was asked to review the user authentication module
before we go live. Can you take a look at scripts/components/user-service.ts
and let me know if there's anything concerning?
```

**NOT:**
```markdown
**Prompt** (too technical):
Run code-review on the SQL injection vulnerability in getUserByEmail().
```

### Step 6: Add Cleanup Steps

```markdown
## Cleanup Steps

### CLEANUP-P4-001: Remove Component Fixtures
rm -rf scripts/components/
rm -rf scripts/lib/database.ts
rm -rf scripts/lib/logger.ts
```

---

## Prompt Writing Guidelines

### Realistic User Language

Users don't speak in technical jargon. Prompts should reflect real conversations.

| Bad (Technical) | Good (Realistic) |
|-----------------|------------------|
| "Review the SQL injection in line 14" | "The login seems slow and I'm worried about security" |
| "Check for any usage" | "Sometimes we get weird undefined errors" |
| "Analyze cyclomatic complexity" | "I can barely understand what this code does" |
| "Validate SRP compliance" | "This file seems to do a lot of different things" |

### Symptom-Based Prompts

Describe symptoms, not root causes:

```
"After I select a date range on the app, the app hangs. Could you please
debug, fix and validate the issue after loading the appropriate skills
and pipeline agents?"
```

**NOT:**
```
"timerangecalc() is giving an out of bound error"
```

---

## Cleanup Protocol

**MANDATORY**: All fixtures must be cleaned up after testing.

### Cleanup Checklist

1. [ ] Remove fixture files (`scripts/components/*.ts`)
2. [ ] Remove supporting stubs (`scripts/lib/database.ts`, etc.)
3. [ ] Remove empty directories
4. [ ] Clear diagnostic logs (optional)
5. [ ] Verify `just typecheck` passes after cleanup
6. [ ] Check `git status` for orphaned artifacts

### Cleanup Commands

```bash
# Remove fixtures
rm -rf scripts/components/
rm -f scripts/lib/database.ts scripts/lib/logger.ts

# Verify clean state
just typecheck
git status
```

---

## Diagnostic Output

After creating fixtures, document the mapping:

```yaml
diagnostic:
  skill: test-fixture-creation
  timestamp: 2026-01-31T12:00:00Z
  fixtures_created:
    - file: scripts/components/user-service.ts
      section: Security
      issues: [sql_injection, hardcoded_secrets, path_traversal]
    - file: scripts/components/data-processor.ts
      section: Type Safety
      issues: [excessive_any, unsafe_assertions]
    - file: scripts/components/workflow-handler.ts
      section: Linting
      issues: [poor_naming, deep_nesting, high_complexity]
    - file: scripts/components/config-manager.ts
      section: Coding Standards
      issues: [multiple_responsibilities, global_state, side_effects]
  supporting_stubs:
    - scripts/lib/database.ts
    - scripts/lib/logger.ts
  phase1_validation:
    typecheck: passed
    lint: passed
```

---

## Learnings Log

### Session 32 (2026-01-31)

1. **Fixtures in project infrastructure**: Test fixtures need to be in project directories (not tests/fixtures/) so hooks fire correctly
2. **No @types/node**: Pure TypeScript fixtures avoid dependency on @types/node
3. **Stub imports**: Create minimal stubs for imports to make fixtures compile
4. **Realistic prompts**: Non-developer language produces more realistic test results
5. **Cleanup discipline**: Always add cleanup steps to test protocols
6. **ESLint config required**: Without `.eslintrc.json`, `just lint` skips TypeScript - Phase 1 incomplete
7. **Package.json for deps**: Need `package.json` with typescript, eslint, @typescript-eslint/* for real Phase 1 checks
8. **Warnings vs Errors**: ESLint warnings (intentional `any`, unused vars) don't block Phase 1; only errors block
9. **Separate fixture locations**: Use `scripts/components/` for direct invocation, `scripts/services/` for pipeline integration
10. **Pipeline vs Direct tests**: Direct invocation uses `--section` flag (deterministic); pipeline tests LLM judgment (stochastic)
