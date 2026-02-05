---
name: audit-remediation
description: Apply approved remediation actions from audit resolution. Implements config file updates, template syncs, and code fixes using appropriate domain/config agents. Use when audit findings have been approved for remediation and need implementation.
---

# Audit Remediation Skill

> **ROOT AGENT ONLY** - Called by /audit command after user approves fixes.

**Purpose:** Apply approved remediation actions to fix audit violations

**Trigger:** After user selects remediation options in resolution phase

**Input:**

- `remediation_plan[]` - approved fixes from resolution phase
- `templates` - updated templates from template-update skill
- `repoType` - repository type (library/consumer)

**Output:**

- `applied_fixes[]` - list of fixes applied successfully
- `failed_fixes[]` - list of fixes that failed with errors
- `files_modified[]` - list of files changed
- `summary` - remediation results for report

---

## Workflow Steps

**1. Parse Remediation Plan**

- Extract fix metadata from remediation_plan
- Group by type: config, template, code, file-creation
- Determine which agents/skills to invoke
- Build execution queue ordered by dependency

**2. For Each Approved Remediation:**

| Remediation Type   | Agent/Skill                  | Action                                    |
| ------------------ | ---------------------------- | ----------------------------------------- |
| Config file update | Domain-specific config agent | Apply template to config file, re-audit   |
| Template sync      | File write (templates/)      | Copy updated template to correct location |
| Code fix           | coder-agent                  | Apply code changes, validate syntax       |
| File creation      | template-based               | Create file from template with vars       |

**3. Execute Fixes in Order**

```
For each fix in remediation_plan:

  a. Identify target file location
  b. Determine remediation type
  c. Apply fix using appropriate agent/tool
  d. Validate fix was applied:
     - File exists and contains expected content
     - No syntax errors introduced
     - Related configs still valid
  e. Track result (success/failure/warning)
```

**4. Handle Failures Gracefully**

- If fix fails: record error, continue with remaining fixes
- Always batch all possible fixes before stopping (continue through all remediation actions)
- Collect failure messages for user review

**5. Track All Modifications**

- Record each file modified with before/after state
- Note remediation type and agent used
- Track applied_fixes vs failed_fixes separately

**6. Return Summary**

```json
{
  "applied_fixes": [
    {
      "type": "config",
      "file": ".eslintrc.js",
      "agent": "eslint-agent",
      "status": "success"
    }
  ],
  "failed_fixes": [
    {
      "type": "code",
      "file": "src/auth.ts",
      "agent": "coder-agent",
      "error": "Syntax validation failed: unexpected token"
    }
  ],
  "files_modified": 5,
  "summary": "Applied 7/8 fixes. 1 fix failed - requires manual review."
}
```

---

## Remediation Type Patterns

### Config File Update

**Pattern:**

1. Spawn appropriate config agent with template
2. Agent validates template applies correctly
3. Agent writes config to correct location
4. Agent runs self-audit on new config
5. Track success/failure

**Example:**

```
Remediation: Fix .eslintrc.js
→ Spawn eslint-agent with template
→ Agent validates and applies
→ Agent audits result
→ Track: "config/.eslintrc.js: success"
```

### Template Sync

**Pattern:**

1. Copy template from remediation_plan to correct location
2. Validate file was written
3. No further validation needed (metadata updated, not functional change)

**Example:**

```
Remediation: Sync TypeScript template
→ Copy plugins/metasaver-core/skills/config/workspace/typescript-configuration/templates/...
→ to packages/web/tsconfig.json
→ Track: "template-sync/tsconfig.json: success"
```

### Code Fix

**Pattern:**

1. Spawn coder-agent with specific fix description
2. Agent applies code changes to file
3. Validate syntax (no parse errors)
4. Run relevant linting/formatting
5. Track success/failure with error messages

**Example:**

```
Remediation: Fix missing error handling in auth.ts
→ Spawn coder-agent with fix description
→ Agent modifies file
→ Validate TypeScript: pnpm tsc --noEmit
→ Track: "code/src/auth.ts: success" or "code/src/auth.ts: failed (error: ...)"
```

### File Creation

**Pattern:**

1. Load template for new file
2. Substitute variables (paths, names, etc.)
3. Write to target location
4. Validate file exists
5. Track success/failure

**Example:**

```
Remediation: Create missing src/index.ts
→ Load template from vitest-config skill
→ Substitute variables
→ Write to src/index.ts
→ Track: "file-creation/src/index.ts: success"
```

---

## Agent Routing Matrix

| Fix Type            | Agent                       | When To Use            |
| ------------------- | --------------------------- | ---------------------- |
| .eslintrc.js        | eslint-agent                | Config violations      |
| .prettierrc         | prettier-agent              | Formatting violations  |
| tsconfig.json       | typescript-agent            | TypeScript violations  |
| vitest.config.ts    | vitest-agent                | Test config violations |
| tailwind.config.js  | tailwind-agent              | Tailwind violations    |
| pnpm-workspace.yaml | pnpm-workspace-agent        | Workspace violations   |
| Code changes        | coder-agent                 | Logic/syntax fixes     |
| New files           | coder-agent (with template) | File creation          |

---

## Error Handling Strategy

**Critical Errors (Halt & Report):**

- File system errors (permission denied, disk full)
- Agent crash during execution
- Syntax validation failure on new code

**Non-Critical (Continue):**

- Config file update with warnings (lint warnings, etc.)
- Optional file already exists
- Template sync skipped (file already matches)

**User Review Required:**

- Code fix completed but logic needs verification
- Multiple fixes affected same file (conflicts)
- Rollback needed (fix broke something else)

---

## State Management

**Before Starting:**

- Snapshot current state of all target files
- Record original versions for rollback if needed

**During Execution:**

- Log each fix attempt (timestamp, agent, result)
- Write lock to prevent concurrent modifications
- Track partial progress in case of interruption

**After Completion:**

- Release lock
- Provide summary of changes
- Save audit-remediation log for review

---

## Integration with Other Skills

**Before This Skill:**

- `audit-workflow` - detects violations
- `remediation-options` - presents user choices
- User approves specific fixes (HITL)

**This Skill:**

- Applies all approved fixes
- Uses config/domain agents for implementation
- Tracks results

**After This Skill:**

- `repomix-cache-refresh` - if files modified
- `report-phase` - generates final report
- Re-audit (if user requests verification)

---

## Output Format for /audit Command

**Success Summary:**

```
Remediation Execution Results
═══════════════════════════════════════

Applied Fixes (7):
  ✅ Config update: .eslintrc.js
  ✅ Config update: .prettierrc
  ✅ Template sync: tsconfig.json
  ✅ Code fix: src/auth.ts
  ✅ File creation: src/types/index.ts
  ✅ Config update: vitest.config.ts
  ✅ Template sync: tailwind.config.js

Failed Fixes (1):
  ❌ Code fix: src/service.ts
     Error: Function signature mismatch with tests

Files Modified: 7

Next Steps:
  1. Review failed fix manually
  2. Run "pnpm audit" to verify
  3. Push changes to review
```

---

## Configuration

| Setting               | Value | Rationale                    |
| --------------------- | ----- | ---------------------------- |
| Validation on writes  | Yes   | Prevent invalid config files |
| Continue on failures  | Yes   | Apply all fixable issues     |
| Snapshot state before | Yes   | Enable rollback if needed    |
| Log all changes       | Yes   | Audit trail required         |

---

## Example Remediation Plan

```json
{
  "remediation_plan": [
    {
      "id": "fix-001",
      "type": "config",
      "configType": "eslint",
      "file": ".eslintrc.js",
      "action": "conform_to_template",
      "template": "eslint-config-template-v1",
      "priority": "high"
    },
    {
      "id": "fix-002",
      "type": "code",
      "file": "src/auth.service.ts",
      "description": "Add missing try-catch block in login method",
      "priority": "high"
    },
    {
      "id": "fix-003",
      "type": "template-sync",
      "file": "tsconfig.json",
      "source": "plugins/metasaver-core/skills/.../tsconfig.template.json",
      "priority": "medium"
    },
    {
      "id": "fix-004",
      "type": "file-creation",
      "file": "src/types/auth.types.ts",
      "template": "typescript-types-template",
      "priority": "low"
    }
  ],
  "templates": {
    "eslint-config-template-v1": {
      /* template content */
    },
    "typescript-types-template": {
      /* template content */
    }
  }
}
```

---

## Used By

- `/audit` command (after user approves fixes)
- `/ms audit` command (for complex audits)
- Multi-phase workflows requiring batch remediation
