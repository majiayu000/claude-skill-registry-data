---
name: mock-detection
description: Deep mock appropriateness analysis for Test Audit pipeline
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Task
  - Write
version: 1.0.1
author: "Ashay Kubal @ Qball Inc."
---

# Mock Detection

Prompt template for deep mock appropriateness analysis using call graph tracing. Designed for a Sonnet sub-agent to detect T1-T4 violations and track violation scope.

---

## When to Use This Skill

**This is an internal skill loaded by the orchestrator during Test Audit pipeline.**

| Context | Action |
|---------|--------|
| `/test-audit` invoked | Orchestrator loads this skill for Stage 2 |
| Test Audit pipeline triggered by hook | Orchestrator loads this skill for Stage 2 |
| Need deep mock analysis | Load directly as prompt template for Sonnet |
| Files flagged by test-classification | Analyze only `needs_deep_analysis: true` files |

**DO NOT use for:**
- Direct user invocation (not user-invocable)
- Surface-level classification (use `test-classification` skill)
- Full audit synthesis (use `test-audit` skill)

---

## Role in Test Audit Pipeline

This skill provides the **second stage** prompt template:

```
test-audit (P0.8) orchestrates:
  Stage 1: test-classification (Haiku) → classification YAML
  Stage 2: mock-detection (Sonnet) → violations YAML    ← THIS SKILL
  Stage 3: synthesis (Sonnet) → audit report
```

The orchestrator loads this skill and constructs a 4-part prompt for a general-purpose Sonnet sub-agent.

---

## 4-Part Prompt Template

### GOAL

Analyze flagged test files for T1-T4 violations using mock appropriateness rubric and call graph analysis. Track the full scope of each violation for test effectiveness calculation.

### CONSTRAINTS

- Do NOT modify any files
- Only analyze files with `needs_deep_analysis: true` from classification
- Use call graph analysis to detect broken integration chains
- Track violation scope (all affected lines, not just violation line)
- Provide full context for each violation (line, snippet, reason, fix)
- Complete within 50 tool calls

### CONTEXT

**Classification output:** `{classification_yaml_path}`

**Files to analyze:** List of files with `needs_deep_analysis: true`

**Mock appropriateness rubric:** See "Mock Appropriateness Rubric" section below

**T1-T4 detection patterns:** See "T1-T4 Detection Patterns" section below

**Violation scope tracking:** See "Violation Scope Tracking" section below

**Extended stub/fake patterns:** See `references/stub-patterns.md` — Meszaros taxonomy, class hierarchy detection, factory function classification

**False positive prevention:** See `references/false-positive-prevention.md` — Two-tier allowlist (Universal Safe / Context-Dependent) and decision tree. Consult BEFORE flagging borderline patterns.

### OUTPUT

Write violations to: `logs/mock-detection-{YYYYMMDD-HHMMSS}.yaml`

Write diagnostics to: `logs/diagnostics/mock-detection-{YYYYMMDD-HHMMSS}.yaml`

Use the schema specified in "Output Schema" section below.

---

## Mock Appropriateness Rubric

Determine whether mocks are appropriate based on test type:

| Test Type | Expected Mocks (OK) | Inappropriate Mocks (VIOLATION) |
|-----------|---------------------|--------------------------------|
| **Unit** | External deps (DB, HTTP, fs) to isolate unit | Mocking function/module under test (T1) |
| **Integration** | Unrelated systems only | Mocking integration boundaries (T3), broken chain (T3+) |
| **E2E** | Almost never | Any mock breaking end-to-end flow |

### Mixed-Type Files (MANDATORY)

Test files commonly contain multiple test types in different describe blocks (e.g., unit tests at top, integration tests at bottom). You MUST evaluate mock appropriateness **per describe block/section**, not per file. A `jest.fn()` that is safe in a unit test section is a T3 violation in an integration test section of the same file.

Classification signals (language-agnostic — apply to TypeScript, Python, Java, Go, Ruby, etc.):
- Block/suite name containing keywords: `integration`, `e2e`, `end-to-end`, `acceptance`, `system`
- Preceding comments or section headers: `// INTEGRATION TESTS`, `# E2E`, `/* system tests */`
- Setup patterns within the block (real DB connections = integration, browser launch = e2e)

If AST integration-mock metadata is available (from `just integration-mocks`), use it as ground truth for section boundaries and mock locations. Validate AST leads and add any the AST missed.

**BINDING: AST classification is final.** When the AST script classifies a section as integration or e2e, that classification is NOT subject to LLM override. You MUST evaluate mocks in that section against integration/e2e rules — even if you believe the section is "actually" a unit test. Dismissing an AST T3 lead by re-classifying the section as a different test type is a rule violation. If you believe the section is mislabeled, note it as advisory — but still flag T3 violations against the classified type.

See `references/false-positive-prevention.md` § "Worked Example: Mixed-Type File" for a concrete demonstration.

### Key Principle

A mock is inappropriate when it **defeats the purpose of the test**:
- Unit test claims to test function X but mocks function X → T1
- Integration test claims to verify HTTP calls but mocks HTTP → T3
- Test verifies function was called but not what it produced → T2

---

## T1-T4 Detection Patterns

### T1: Mocking System Under Test

**Severity:** Critical
**Priority:** P0 (False Confidence)

**Detection patterns:**
- `jest.spyOn(ModuleUnderTest, 'functionBeingTested')`
- `jest.mock('./file-being-tested')`
- `vi.mock()` on the module imported in the test's subject
- Mock intercepts the exact function the test claims to verify

**Call graph check:** Trace from test assertion back to setup. If mock sits between "action" and "assertion" for the claimed behavior, it's T1.

### T2: Verifying Calls Not Results

**Severity:** High
**Priority:** P1 (Incomplete Verification)

**Detection patterns:**
- `expect(fn).toHaveBeenCalled()` without result assertion
- `expect(fn).toHaveBeenCalledWith(...)` without verifying the effect
- `verify(mock).someMethod()` without outcome check

**Call graph check:** After the `toHaveBeenCalled` assertion, is there a result/state assertion for the same operation?

### T3: Mock at Integration Boundary

**Severity:** Critical
**Priority:** P1 (Incomplete Verification)

**Detection patterns:**
- In `.integration.*` file: `jest.mock('node-fetch')`, `jest.mock('fs')`, `jest.mock('http')`
- In integration test: Mocking the very boundary being integrated

**Call graph check:** Does the test claim to verify "integration with X" while mocking X?

### T3+: Broken Integration Chain

**Severity:** Critical
**Priority:** P0 (False Confidence)

**Detection patterns:**
- `mockData` used where real function output should flow
- Data manually constructed instead of flowing from upstream function
- Integration test with hardcoded intermediate values
- Property access on manually-constructed objects used in downstream calls (e.g., `mockOrder.id` passed into new objects)

**Class hierarchy signals** (see `references/stub-patterns.md` for full taxonomy):
- Classes named Fake*/Stub*/Mock*/InMemory*/Test* that implement interfaces or extend base classes
- Manual stub objects without naming conventions (all methods are no-ops or return hardcoded values)
- Factory functions prefixed with `buildMock*` or `createFake*`

**Call graph check:** Trace data flow. If Component A should output to Component B, but test injects `mockAOutput` into B, the chain is broken.

### T4: No Test Execution Verification

**Severity:** Medium
**Priority:** P2 (Pattern Issues)

**Detection patterns:**
- Test file exists but `just test` not run
- Tests pass in isolation but skip in suite
- Manual notation: "Requires V3 manual verification"

**Note:** T4 is primarily a process check. Flag for manual review.

---

## Violation Scope Tracking

Track the **full scope** of each violation - not just the violation line, but all lines affected by it. This enables accurate test effectiveness calculation.

### Scope Calculation Rules

| Violation Type | Scope Definition |
|----------------|------------------|
| **T1 (Mock SUT)** | All lines that use the mock: assertions depending on mock, calls using mock return value |
| **T2 (Call-only)** | The assertion line itself (single line) |
| **T3 (Mock boundary)** | All lines using the mocked boundary (similar to T1) |
| **T3+ (Broken chain)** | All lines using the incorrect/mocked data downstream |

### Example

```javascript
// Line 15: Mock setup (violation line)
const mockSpawn = jest.spyOn(child_process, 'spawn')
  .mockReturnValue(mockProcess);

// Lines 20-95: All use mockSpawn results
const proxy = startProxy();      // Line 20 - uses mock
await proxy.waitForReady();      // Line 21 - uses mock
expect(proxy.port).toBe(8080);   // Line 25 - assertion on mock
// ... more lines using mock ...
expect(proxy.isRunning()).toBe(true);  // Line 95 - still mock

// violation_scope: [15, 95]
// affected_lines: 80
```

---

## Call Graph Analysis Approach

For each flagged file, perform systematic analysis:

### Step 1: Identify Test Claims

What does each test claim to verify? Look at:
- Test name/description (`it('starts proxy correctly', ...)`)
- Assertion statements (what is being expected?)

### Step 2: Trace Data Flow

How does data flow from setup → action → assertion?
- Where is input created?
- What transforms the input?
- What does the assertion check?

### Step 3: Locate Mock Interception

Where do mocks intercept this flow?
- Is mock between action and the claimed verification?
- Does mock replace real behavior the test should exercise?

### Step 4: Evaluate Appropriateness

Does the mock defeat the test's purpose?
- If test claims "proxy starts" but mocks spawn → T1
- If test claims "API integration" but mocks fetch → T3

---

## Output Schema

The output MUST include a top-level `reviewed_files: [...]` list (paths relative to `${CLAUDE_PROJECT_DIR}`) so the Stop hook can suppress per-file pipeline-recursion fires on subsequent turns. Mirror the same list in both the violations log and the diagnostic log. Empty list `[]` is valid if no files matched the detection target.

```yaml
# Top-level — required for Stop-hook suppression contract.
reviewed_files:
  - tests/proxy.test.ts
  - tests/api.integration.ts
  - tests/workflow.integration.ts
  - tests/config.test.ts

metadata:
  skill: mock-detection
  timestamp: "{ISO-8601}"
  classification_source: logs/test-classification-{YYYYMMDD-HHMMSS}.yaml
  model: sonnet
  files_analyzed: 5

violations:
  - file: tests/proxy.test.ts
    line: 15
    violation_scope: [15, 95]
    affected_lines: 80
    rule: T1
    severity: critical
    priority: P0
    pattern: "jest.spyOn(child_process, 'spawn')"
    code_snippet: |
      const mockSpawn = jest.spyOn(child_process, 'spawn')
        .mockReturnValue(mockProcess);
    reason: |
      Test claims to verify "proxy starts correctly" but mocks spawn().
      This provides false confidence - mock always succeeds.
      Lines 15-95 all use this mock, making them ineffective.
    suggested_fix: |
      Replace mock with real spawn. Use port check to verify proxy started.

  - file: tests/api.integration.ts
    line: 8
    violation_scope: [8, 45]
    affected_lines: 37
    rule: T3
    severity: critical
    priority: P1
    pattern: "jest.mock('node-fetch')"
    code_snippet: |
      jest.mock('node-fetch');
      // ... later in test
      const response = await fetchUserData(userId);
    reason: |
      Integration test should verify real HTTP communication.
      Mocking fetch defeats the purpose of integration testing.
    suggested_fix: |
      Remove jest.mock('node-fetch'). Use test server or MSW.

  - file: tests/workflow.integration.ts
    line: 42
    violation_scope: [42, 78]
    affected_lines: 36
    rule: T3+
    severity: critical
    priority: P0
    pattern: "Broken integration chain"
    code_snippet: |
      const result = await processOrder(mockOrderData);
      // mockOrderData should come from createOrder() output
    reason: |
      Test uses mockOrderData instead of real createOrder() output.
      This breaks the integration chain - no real integration tested.
    suggested_fix: |
      Replace mockOrderData with: const order = await createOrder(input);

  - file: tests/config.test.ts
    line: 42
    violation_scope: [42, 42]
    affected_lines: 1
    rule: T2
    severity: high
    priority: P1
    pattern: "expect(db.save).toHaveBeenCalled()"
    code_snippet: |
      await saveConfig(newConfig);
      expect(db.save).toHaveBeenCalled();
    reason: |
      Verifies db.save was called but not what was saved.
      Call verification without result verification is incomplete.
    suggested_fix: |
      Add result verification: expect(saved.value).toBe(newConfig.value);

totals:
  critical: 3
  high: 1
  medium: 0
  low: 0
  total_affected_lines: 154

file_summaries:
  # For each file, compute affected_lines as the UNION of all violation_scope ranges
  # (merge overlapping/identical ranges). Do NOT sum individual affected_lines values.
  # Example: two violations both scoped to [228, 269] = 42 affected lines, not 84.
  - file: tests/proxy.test.ts
    verification_lines: 95
    affected_lines: 80
    test_effectiveness: 16%
  - file: tests/api.integration.ts
    verification_lines: 55
    affected_lines: 37
    test_effectiveness: 33%
  - file: tests/workflow.integration.ts
    verification_lines: 50
    affected_lines: 36
    test_effectiveness: 28%
  - file: tests/config.test.ts
    verification_lines: 40
    affected_lines: 1
    test_effectiveness: 98%

summary: |
  Analyzed 5 flagged files. Found 4 violations affecting 154 lines.
  3 files below 95% test effectiveness threshold.
  P0 violations (false confidence): proxy.test.ts, workflow.integration.ts
  P1 violations (incomplete): api.integration.ts, config.test.ts
```

---

## Diagnostic Output

Write diagnostic output to `logs/diagnostics/mock-detection-{YYYYMMDD-HHMMSS}.yaml`:

```yaml
# Top-level — required for Stop-hook per-file pipeline-recursion suppression.
# List any test/script files analyzed by this run (paths relative to
# ${CLAUDE_PROJECT_DIR}). Empty list `[]` is valid when no test files were
# touched. Missing field disables suppression for this log (strict mode).
reviewed_files: []

diagnostic:
  skill: mock-detection
  timestamp: "{ISO-8601}"
  model: sonnet

execution:
  tool_calls: 35
  files_analyzed: 5
  analysis_depth: "call graph tracing"

decisions:
  - file: tests/proxy.test.ts
    decision: T1_violation
    call_graph_analysis: |
      Test claims: "proxy starts correctly"
      Action: startProxy() calls child_process.spawn()
      Mock: jest.spyOn intercepts spawn()
      Result: Assertion verifies mock behavior, not real spawn
    confidence: high

  - file: tests/config.test.ts
    decision: T2_violation
    call_graph_analysis: |
      Assertion: toHaveBeenCalled() on db.save
      Missing: No assertion on saved data value
      Scope: Single assertion line (minimal impact)
    confidence: high

errors: []
```

---

## Priority Classification

### P0: False Confidence

Tests that pass but provide no real assurance:
- **T1**: Mock hides real failures - test always passes regardless of SUT behavior
- **T3+**: Broken chain means integration is never actually tested

### P1: Incomplete Verification

Tests that run real code but don't fully verify:
- **T2**: Call happened but effect not verified
- **T3**: Integration boundary mocked (partial integration)

### P2: Pattern Issues

Style and organization issues:
- Minor mock patterns
- Test structure recommendations

---

## Integration Notes

### Orchestrator Usage

The orchestrator (P0.8) constructs the full prompt by:

1. Loading this skill content
2. Including classification YAML path in CONTEXT
3. Spawning: `Task(subagent_type="general-purpose", model="sonnet", prompt=...)`
4. Reading output from `logs/mock-detection-{YYYYMMDD-HHMMSS}.yaml`

### Upstream Input

From P0.6 (test-classification):
- `needs_deep_analysis: true` file list
- `verification_lines` count per file
- `mock_indicators` as analysis starting points

### Downstream Output

To P0.8 (test-audit synthesis):
- Violation details with scope tracking
- `affected_lines` per file
- Pre-calculated `test_effectiveness` per file

---

## Batching for Scale

When processing many flagged files (>10), the orchestrator must batch detection to avoid context limits.

### Batching Instructions

```
IF flagged_file_count > 10:
    Split flagged files into batches of 10-15
    FOR each batch:
        Spawn Sonnet sub-agent with batch file list
        Include verification_lines from classification for each file
        Collect violations YAML for batch
    Merge all batch results into single detection output
ELSE:
    Process all flagged files in single sub-agent call
```

### Batch Merge Strategy

When merging batch results:
1. Combine all `violations` arrays
2. Recalculate `totals` across all batches
3. Combine all `file_summaries`
4. Preserve individual violation details exactly

### Parallel Execution

For optimal performance, spawn batch sub-agents in parallel by issuing multiple Task() calls in a single assistant message (the harness runs them concurrently — do **not** use `run_in_background=true`, which violates Rules.md SA5):

```
Task(subagent_type="general-purpose", prompt=batch1_prompt)
Task(subagent_type="general-purpose", prompt=batch2_prompt)
...
```

Read all outputs after completion, then merge.

---

## References

| Document | Purpose |
|----------|---------|
| `references/stub-patterns.md` | Meszaros test double taxonomy, class hierarchy detection, factory function classification |
| `references/false-positive-prevention.md` | Two-tier allowlist (Universal Safe / Context-Dependent), decision tree for violation evaluation |

## Related Skills

- `test-classification` (P0.6) - Surface classification (upstream)
- `test-audit` (P0.8) - Orchestration and synthesis (downstream)
- `pipeline-templates` (P0.3) - Test Audit pipeline definition
