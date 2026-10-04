---
name: test-classification
description: Prompt template for test classification stage in Test Audit pipeline
user-invocable: false
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
version: 1.0.1
author: "Ashay Kubal @ Qball Inc."
---

# Test Classification

Prompt template for surface-level test classification and triage. Designed for a Haiku sub-agent to quickly categorize test files and flag those needing deep analysis.

---

## When to Use This Skill

**This is an internal skill loaded by the orchestrator during Test Audit pipeline.**

| Context | Action |
|---------|--------|
| `/test-audit` invoked | Orchestrator loads this skill for Stage 1 |
| Test Audit pipeline triggered by hook | Orchestrator loads this skill for Stage 1 |
| Need to classify test files | Load directly as prompt template for Haiku |

**DO NOT use for:**
- Direct user invocation (not user-invocable)
- Mock detection (use `mock-detection` skill)
- Full audit synthesis (use `test-audit` skill)

---

## Role in Test Audit Pipeline

This skill provides the **first stage** prompt template:

```
test-audit (P0.8) orchestrates:
  Stage 1: test-classification (Haiku) → classification YAML
  Stage 2: mock-detection (Sonnet) → violations YAML
  Stage 3: synthesis (Sonnet) → audit report
```

The orchestrator loads this skill and constructs a 4-part prompt for a general-purpose Haiku sub-agent.

---

## 4-Part Prompt Template

### GOAL

Classify all test files in `{target}` by type and flag files needing deep analysis for mock appropriateness.

### CONSTRAINTS

- Do NOT modify any files
- Classify every test file found
- Use filename-first classification (content validates)
- Flag mock+integration mismatches for deep analysis
- Use AST verification_lines as ground truth when provided in context (do NOT re-count).
  Only fall back to manual counting if AST data is unavailable.
- Complete within 30 tool calls

### CONTEXT

**Target directory:** `{target}`

**Test file patterns:** `*.test.*`, `*.spec.*`, `test_*`, `*.integration.*`, `*.e2e.*`

**Classification rules:** See "Classification Logic" section below

**Deep analysis triggers:** See "needs_deep_analysis Triggers" section below

**Line counting rules:** See "Verification Line Counting" section below

**AST verification_lines (MANDATORY when available):**
If the orchestrator provides `ast_verification_lines` per file, use that value directly as `verification_lines` in the output. Do NOT override with your own count. The AST value is deterministic and precise; heuristic counting at scale is error-prone.

### OUTPUT

Write classification to: `logs/test-classification-{YYYYMMDD-HHMMSS}.yaml`

Write diagnostics to: `logs/diagnostics/test-classification-{YYYYMMDD-HHMMSS}.yaml`

Use the schema specified in "Output Schema" section below.

---

## Classification Logic

### 1. Filename Pattern (Primary)

| Pattern | Category |
|---------|----------|
| `*.integration.*` | integration |
| `*.e2e.*` | e2e |
| `*.test.*`, `*.spec.*`, `test_*` | unit (default) |

### 2. Content Validation (Secondary)

After filename classification, scan content to validate:

| Content Signal | Interpretation |
|----------------|----------------|
| Imports test framework (`jest`, `vitest`, `mocha`, `pytest`) | Confirms test file |
| Imports system modules (`child_process`, `fs`, `http`) | Note for risk assessment |
| Contains `jest.mock()`, `vi.mock()`, `patch()` | Mock indicator |
| Contains `describe(`, `it(`, `test(` | Standard test structure |

### 3. Risk Detection

| Risk | Condition | Recommendation |
|------|-----------|----------------|
| `test_management` | Single file contains multiple test types (unit + integration) | Split into separate files |

---

## needs_deep_analysis Triggers

Flag a file for deep analysis when ANY of these conditions are met:

### Always Flag (Regardless of Mock Indicators)

| Trigger | Reason |
|---------|--------|
| `*.integration.*` file | Integration tests need chain verification - may have T3+ violations without explicit mocks |
| `*.e2e.*` file | E2E tests should have minimal mocking - verify end-to-end flow |

**Rationale:** The absence of `jest.mock()` in an integration test doesn't mean it's clean. T3+ violations (broken integration chains) use inline mock data instead of upstream function outputs. These are only detectable through deep analysis.

### Mock Indicator Triggers

| Trigger | Reason |
|---------|--------|
| Unit test with any `jest.mock()` / `vi.mock()` on core modules | Potential T1 (mocking SUT) or over-mocking |
| Unit test with >3 top-level mocks | Unusual mock density suggests over-mocking |
| Unit test mocking core modules (`spawn`, `fs`, `fetch`, `http`) | Known risky patterns requiring contextual analysis |

---

## Verification Line Counting

Count "verification lines" per file for test effectiveness calculation. This count is used by P0.7 to calculate how many effective test lines remain after violations are identified.

### Exclude from Count

- Comment lines (`//`, `/* */`, `/** */`, `#`)
- Import/require statements (`import`, `require`, `from`)
- Empty/whitespace-only lines
- Test framework boilerplate:
  - `describe(`, `it(`, `test(`
  - `beforeEach(`, `afterEach(`
  - `beforeAll(`, `afterAll(`
  - `setUp(`, `tearDown(`

### Include in Count

- Actual test logic (assertions, function calls, variable assignments within tests)
- Mock setup lines (these may be marked as violation scope by P0.7)
- Assertion statements (`expect(`, `assert`, `should`)
- Setup code within test bodies

---

## Output Schema

The classification output MUST include a top-level `reviewed_files: [...]` list (paths relative to `${CLAUDE_PROJECT_DIR}`) so the Stop hook can suppress per-file pipeline-recursion fires on subsequent turns. Mirror the same list in the diagnostic log. Empty list `[]` is valid if no files matched the classification target.

```yaml
# Top-level — required for Stop-hook suppression contract.
reviewed_files:
  - tests/proxy.test.ts
  - tests/api.integration.ts
  - tests/utils.test.ts

metadata:
  skill: test-classification
  timestamp: "{ISO-8601}"
  target: "{directory}"
  model: haiku

files:
  - path: tests/proxy.test.ts
    category: unit
    total_lines: 150
    verification_lines: 95   # Use ast_verification_lines if provided; only count manually if unavailable
    mock_indicators:
      - "jest.spyOn(child_process, 'spawn')"
    needs_deep_analysis: true
    deep_analysis_reason: "Unit test mocks core module (spawn)"

  - path: tests/api.integration.ts
    category: integration
    total_lines: 80
    verification_lines: 55
    mock_indicators:
      - "jest.mock('node-fetch')"
    needs_deep_analysis: true
    deep_analysis_reason: "Integration test contains mocks"

  - path: tests/utils.test.ts
    category: unit
    total_lines: 60
    verification_lines: 40
    mock_indicators: []
    needs_deep_analysis: false

risks:
  test_management:
    - path: tests/everything.test.ts
      reason: "Single file contains unit, integration, and e2e tests"
      recommendation: "Split into separate files by test type"

summary:
  total_files: 25
  by_category:
    unit: 15
    integration: 8
    e2e: 2
  total_verification_lines: 1250
  needs_deep_analysis: 5
  test_management_risks: 1
```

---

## Diagnostic Output

Write diagnostic output to `logs/diagnostics/test-classification-{YYYYMMDD-HHMMSS}.yaml`:

```yaml
# Top-level — required for Stop-hook per-file pipeline-recursion suppression.
# List any test/script files analyzed by this run (paths relative to
# ${CLAUDE_PROJECT_DIR}). Empty list `[]` is valid when no test files were
# touched. Missing field disables suppression for this log (strict mode).
reviewed_files: []

diagnostic:
  skill: test-classification
  timestamp: "{ISO-8601}"
  model: haiku

execution:
  tool_calls: 15
  files_scanned: 25
  classification_time_estimate: "surface scan"

decisions:
  - file: tests/proxy.test.ts
    decision: needs_deep_analysis
    reason: "Found jest.spyOn on child_process.spawn"
    confidence: high

  - file: tests/utils.test.ts
    decision: clean
    reason: "No mock indicators found"
    confidence: high

errors: []
```

---

## Integration Notes

### Orchestrator Usage

The orchestrator (P0.8) constructs the full prompt by:

1. Loading this skill content
2. Substituting `{target}` with user-provided path or inferred target
3. Spawning: `Task(subagent_type="general-purpose", model="haiku", prompt=...)`
4. Reading output from `logs/test-classification-{YYYYMMDD-HHMMSS}.yaml`

### Downstream Usage

P0.7 (mock-detection) receives:
- List of files with `needs_deep_analysis: true`
- `verification_lines` count per file (for effectiveness calculation)
- `mock_indicators` as starting points for deep analysis

---

## Batching for Scale

When processing large test suites (>20 files), the orchestrator must batch classification to avoid context limits.

### Batching Instructions

```
IF file_count > 20:
    Split files into batches of 20-25
    FOR each batch:
        Spawn Haiku sub-agent with batch file list
        Collect classification YAML for batch
    Merge all batch results into single classification output
ELSE:
    Process all files in single sub-agent call
```

### Batch Merge Strategy

When merging batch results:
1. Combine all `files` arrays
2. Combine all `risks` entries
3. Recalculate `summary` totals across all batches
4. Preserve individual file classifications exactly

### Parallel Execution

For optimal performance, spawn batch sub-agents in parallel by issuing multiple Task() calls in a single assistant message (the harness runs them concurrently — do **not** use `run_in_background=true`, which violates Rules.md SA5):

```
Task(subagent_type="general-purpose", prompt=batch1_prompt)
Task(subagent_type="general-purpose", prompt=batch2_prompt)
...
```

Read all outputs after completion, then merge.

---

## Related Skills

- `mock-detection` (P0.7) - Deep analysis of flagged files
- `test-audit` (P0.8) - Orchestration and synthesis
- `pipeline-templates` (P0.3) - Test Audit pipeline definition
