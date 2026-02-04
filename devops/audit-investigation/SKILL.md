---
name: audit-investigation
description: Use when investigating config file discrepancies during audit. Spawns config agents in waves to compare template standards against actual files. READ-ONLY analysis - agents report findings but make no changes.
---

# Audit Investigation Skill

> **ROOT AGENT ONLY** - Called by /audit command during investigation phase.

**Purpose:** Investigate configuration discrepancies by comparing templates to actual files

**Trigger:** After execution plan approved, before user resolution decisions

**Input:**

- `execution_plan` - waves of (agent, file) pairs from planning phase
- `repoType` - repository type for context
- `repos[]` - list of repositories in scope

**Output:**

- `discrepancies[]` - all findings with severity, location, expected vs actual
- `summary` - aggregate stats by severity and file count

---

## Workflow Steps

**1. Parse Execution Plan**

- Extract waves from execution plan
- Each wave contains max 10 (agent, file) pairs
- Waves execute sequentially, agents within wave execute in parallel

**2. Execute Investigation in Waves**

For each wave:

| Step                             | Action                                  |
| -------------------------------- | --------------------------------------- |
| a. Spawn config agents           | Parallel invocation (max 10)            |
| b. Agent reads template          | From agent's skill templates/ directory |
| c. Agent reads actual file       | From repository using Read tool         |
| d. Agent compares field-by-field | Template rules vs actual config         |
| e. Agent reports discrepancies   | Line numbers, expected/actual, severity |

**3. Aggregate Results from All Waves**

```
For each agent result:
  a. Extract discrepancy findings
  b. Normalize format:
     {
       file: "path/to/file",
       line: 42,
       field: "extends",
       expected: "@metasaver/eslint-config",
       actual: "eslint:recommended",
       severity: "critical" | "warning" | "info",
       agent: "eslint-agent",
       message: "Config extends incorrect base"
     }
  c. Add to master discrepancies array
```

**4. Sort by Severity**

```
Priority order:
  1. critical - Blocks compliance, must fix
  2. warning - Recommended fix, impacts quality
  3. info - Optional improvement, style preference

Within same severity: alphabetical by file path
```

**5. Generate Summary**

```json
{
  "total_files": 12,
  "total_discrepancies": 47,
  "by_severity": {
    "critical": 8,
    "warning": 24,
    "info": 15
  },
  "by_agent": {
    "eslint-agent": 12,
    "prettier-agent": 8,
    "typescript-agent": 15,
    "vite-agent": 12
  }
}
```

**6. Return Structured Output**

- Complete list of discrepancies for resolution phase
- Summary for user presentation
- NO CHANGES MADE - all read-only investigation

---

## Agent Invocation Pattern

**Parallel Wave Execution:**

```
Wave 1 (10 agents):
  Task 1: subagent_type="core-claude-plugin:config:eslint-agent"
    Prompt: "Audit .eslintrc.js in /path/to/repo against your template. Report discrepancies."

  Task 2: subagent_type="core-claude-plugin:config:prettier-agent"
    Prompt: "Audit .prettierrc in /path/to/repo against your template. Report discrepancies."

  ... (up to 10 parallel)

Wait for all Task 1-10 to complete, collect results

Wave 2 (remaining agents):
  ... repeat pattern
```

**Agent Instructions:**

Each config agent receives:

1. Target file path to audit
2. Repository context (type, location)
3. Instruction: "READ-ONLY audit - compare template to actual, report discrepancies"
4. Expected output format (JSON with discrepancies array)

---

## Severity Classification

| Severity | Criteria                               | Examples                                                                |
| -------- | -------------------------------------- | ----------------------------------------------------------------------- |
| critical | Breaks standards, blocks functionality | Missing required plugin, incorrect parser, wrong extends chain          |
| warning  | Impacts quality, recommended fix       | Suboptimal rule config, missing recommended plugin, style inconsistency |
| info     | Optional improvement                   | Comment formatting, property order, alternative valid config            |

**Agent Responsibility:** Each config agent determines severity based on template rules.

---

## Output Format

**Discrepancies Array:**

```json
[
  {
    "file": "packages/web/.eslintrc.js",
    "line": 3,
    "field": "extends",
    "expected": ["@metasaver/eslint-config"],
    "actual": ["eslint:recommended"],
    "severity": "critical",
    "agent": "eslint-agent",
    "message": "Config must extend @metasaver/eslint-config for standards compliance"
  },
  {
    "file": "packages/api/prettier.config.js",
    "line": 5,
    "field": "semi",
    "expected": false,
    "actual": true,
    "severity": "warning",
    "agent": "prettier-agent",
    "message": "Semicolons should be disabled per house style"
  }
]
```

**Summary Object:**

```json
{
  "total_files": 12,
  "total_discrepancies": 47,
  "by_severity": {
    "critical": 8,
    "warning": 24,
    "info": 15
  },
  "by_agent": {
    "eslint-agent": 12,
    "prettier-agent": 8,
    "typescript-agent": 15,
    "vite-agent": 12
  },
  "files_with_issues": [
    "packages/web/.eslintrc.js",
    "packages/api/prettier.config.js",
    "packages/web/tsconfig.json"
  ]
}
```

---

## Error Handling

| Scenario         | Action                                                          |
| ---------------- | --------------------------------------------------------------- |
| File not found   | Report as critical: "Missing required config file"              |
| Agent crashes    | Log error, continue with remaining agents, flag for user review |
| Template missing | Report as critical: "Agent template unavailable - cannot audit" |
| Parse error      | Report as critical: "Config file syntax invalid"                |
| No discrepancies | Return empty array for that file (success)                      |

**Graceful Degradation:** If some agents fail, continue with successful agents and report partial results.

---

## READ-ONLY Guarantee

**Critical Rules:**

1. NO Write tool calls - investigation only uses Read tool
2. NO Edit tool calls - no modifications to any files
3. NO file creation - only analyze existing files
4. NO template updates - templates are read-only reference
5. Agents report findings in memory only (JSON output)

**Verification:** Command should validate no file system changes occurred during investigation.

---

## Wave Management

**Why Waves?**

- Control parallelism (max 10 agents per wave prevents resource exhaustion)
- Sequential wave execution ensures results collected before next wave
- Enables progress tracking (wave 1/3 complete)

**Wave Size Optimization:**

| Total Agents | Waves | Agents per Wave   |
| ------------ | ----- | ----------------- |
| 1-10         | 1     | 1-10              |
| 11-20        | 2     | 10, remaining     |
| 21-30        | 3     | 10, 10, remaining |

**Example:**

```
Execution plan: 27 (agent, file) pairs

Wave 1: agents 1-10 (parallel)
Wave 2: agents 11-20 (parallel)
Wave 3: agents 21-27 (parallel)

Total execution time ≈ max(wave_durations)
```

---

## Integration with Other Skills

**Before This Skill:**

- `/skill requirements-phase` - gathers requirements
- `/skill planning-phase` - creates execution plan with waves
- `/skill hitl-approval` - user approves plan

**This Skill:**

- Executes investigation per approved plan
- Spawns config agents in waves
- Collects all discrepancies
- Sorts and aggregates results

**After This Skill:**

- `/skill audit-resolution` - presents findings to user for decisions
- User chooses: apply template, update template, ignore, or custom action

---

## Agent Routing Matrix

| Config Type         | Agent                | Template Location                                           |
| ------------------- | -------------------- | ----------------------------------------------------------- |
| .eslintrc.js        | eslint-agent         | skills/config/code-quality/eslint-config/templates/         |
| .prettierrc         | prettier-agent       | skills/config/code-quality/prettier-config/templates/       |
| tsconfig.json       | typescript-agent     | skills/config/workspace/typescript-configuration/templates/ |
| vitest.config.ts    | vitest-agent         | skills/config/build-tools/vitest-config/templates/          |
| tailwind.config.js  | tailwind-agent       | skills/config/workspace/tailwind-config/templates/          |
| pnpm-workspace.yaml | pnpm-workspace-agent | skills/config/build-tools/pnpm-workspace-config/templates/  |
| .editorconfig       | editorconfig-agent   | skills/config/code-quality/editorconfig-config/templates/   |

**Agent Discovery:** Planning phase maps files to agents using `/skill agent-check`.

---

## Example Execution

**Input:**

```json
{
  "execution_plan": {
    "waves": [
      [
        { "agent": "eslint-agent", "file": "packages/web/.eslintrc.js" },
        { "agent": "prettier-agent", "file": "packages/web/.prettierrc" },
        { "agent": "typescript-agent", "file": "packages/web/tsconfig.json" }
      ],
      [
        { "agent": "eslint-agent", "file": "packages/api/.eslintrc.js" },
        { "agent": "vitest-agent", "file": "packages/api/vitest.config.ts" }
      ]
    ]
  },
  "repoType": "consumer",
  "repos": ["/home/user/code/my-project"]
}
```

**Execution:**

```
Wave 1 (3 agents in parallel):
  → eslint-agent audits packages/web/.eslintrc.js
    Found 4 discrepancies (2 critical, 2 warning)

  → prettier-agent audits packages/web/.prettierrc
    Found 1 discrepancy (1 info)

  → typescript-agent audits packages/web/tsconfig.json
    Found 0 discrepancies

Wave 2 (2 agents in parallel):
  → eslint-agent audits packages/api/.eslintrc.js
    Found 3 discrepancies (1 critical, 2 warning)

  → vitest-agent audits packages/api/vitest.config.ts
    Found 2 discrepancies (2 warning)

Aggregate results: 10 total discrepancies
Sort by severity: 3 critical → 6 warning → 1 info
```

**Output:**

```json
{
  "discrepancies": [
    {
      "file": "packages/web/.eslintrc.js",
      "line": 3,
      "field": "extends",
      "expected": ["@metasaver/eslint-config"],
      "actual": ["eslint:recommended"],
      "severity": "critical",
      "agent": "eslint-agent",
      "message": "Config must extend @metasaver/eslint-config"
    }
    // ... 9 more discrepancies sorted by severity
  ],
  "summary": {
    "total_files": 5,
    "total_discrepancies": 10,
    "by_severity": {
      "critical": 3,
      "warning": 6,
      "info": 1
    },
    "by_agent": {
      "eslint-agent": 7,
      "prettier-agent": 1,
      "vitest-agent": 2
    }
  }
}
```

---

## Configuration

| Setting             | Value               | Rationale                                   |
| ------------------- | ------------------- | ------------------------------------------- |
| Max agents per wave | 10                  | Prevent resource exhaustion                 |
| Wave execution      | Sequential          | Ensure results collected before next wave   |
| Agents within wave  | Parallel            | Maximize throughput                         |
| File access         | Read-only           | Investigation phase - no changes            |
| Error handling      | Continue on failure | Collect partial results if some agents fail |

---

## Used By

- `/audit` command (Phase 5: Investigation)
- Called after planning-phase and hitl-approval
- Feeds results into audit-resolution for user decisions
