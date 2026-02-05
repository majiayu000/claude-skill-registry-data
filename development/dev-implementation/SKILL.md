---
name: ring:dev-implementation
description: |
  Gate 0 of the development cycle. Executes code implementation using the appropriate
  specialized agent based on task content and project language. Handles TDD workflow
  with RED-GREEN phases. Follows project standards defined in docs/PROJECT_RULES.md.

trigger: |
  - Gate 0 of development cycle
  - Tasks loaded at initialization
  - Ready to write code

NOT_skip_when: |
  - "Code already exists" → DELETE it. TDD is test-first.
  - "Simple feature" → Simple ≠ exempt. TDD for all.
  - "Time pressure" → TDD saves time. No shortcuts.
  - "PROJECT_RULES.md doesn't require" → Ring always requires TDD.

sequence:
  before: [ring:dev-devops]

related:
  complementary: [ring:dev-cycle, ring:test-driven-development, ring:requesting-code-review]

input_schema:
  required:
    - name: unit_id
      type: string
      description: "Task or subtask identifier being implemented"
    - name: requirements
      type: string
      description: "Task requirements or acceptance criteria"
    - name: language
      type: string
      enum: [go, typescript, python]
      description: "Programming language for implementation"
    - name: service_type
      type: string
      enum: [api, worker, batch, cli, frontend, bff]
      description: "Type of service being implemented"
  optional:
    - name: technical_design
      type: string
      description: "Path to technical design document"
    - name: existing_patterns
      type: array
      items: string
      description: "Existing code patterns to follow"
    - name: project_rules_path
      type: string
      default: "docs/PROJECT_RULES.md"
      description: "Path to project rules file"

output_schema:
  format: markdown
  required_sections:
    - name: "Implementation Summary"
      pattern: "^## Implementation Summary"
      required: true
    - name: "TDD Results"
      pattern: "^## TDD Results"
      required: true
    - name: "Files Changed"
      pattern: "^## Files Changed"
      required: true
    - name: "Handoff to Next Gate"
      pattern: "^## Handoff to Next Gate"
      required: true
  metrics:
    - name: result
      type: enum
      values: [PASS, FAIL, PARTIAL]
    - name: agent_used
      type: string
    - name: tdd_red_status
      type: enum
      values: [completed, failed]
    - name: tdd_green_status
      type: enum
      values: [completed, failed]
    - name: files_created
      type: integer
    - name: files_modified
      type: integer
    - name: tests_added
      type: integer

agent_selection:
  criteria:
    - pattern: "*.go"
      keywords: ["go.mod", "golang", "Go"]
      agent: "ring:backend-engineer-golang"
    - pattern: "*.ts"
      keywords: ["express", "fastify", "nestjs", "backend", "api", "server"]
      agent: "ring:backend-engineer-typescript"
    - pattern: "*.tsx"
      keywords: ["react", "next", "frontend", "component", "page"]
      agent: "frontend-bff-engineer-typescript"
    - pattern: "*.css|*.scss"
      keywords: ["design", "visual", "aesthetic", "styling", "ui"]
      agent: "ring:frontend-designer"
  fallback: "ASK_USER"

verification:
  automated:
    - command: "go build ./... 2>&1 | grep -c 'error'"
      description: "Go code compiles"
      success_pattern: "^0$"
    - command: "npm run build 2>&1 | grep -c 'error'"
      description: "TypeScript compiles"
      success_pattern: "^0$"
  manual:
    - "TDD RED phase failure output captured before implementation"
    - "Implementation follows project standards from PROJECT_RULES.md"

examples:
  - name: "Go backend implementation"
    input:
      unit_id: "task-001"
      requirements: "Add user authentication endpoint with JWT"
      language: "go"
      service_type: "api"
    expected_output: |
      ## Implementation Summary
      **Status:** PASS
      **Agent:** ring:backend-engineer-golang
      
      ## TDD Results
      | Phase | Status | Output |
      |-------|--------|--------|
      | RED | ✅ | FAIL: TestUserAuth - expected token, got nil |
      | GREEN | ✅ | PASS: TestUserAuth (0.003s) |
      
      ## Files Changed
      | File | Action | Lines |
      |------|--------|-------|
      | internal/handler/auth.go | Created | +85 |
      | internal/handler/auth_test.go | Created | +120 |
      
      ## Handoff to Next Gate
      - Ready for Gate 1: YES
---

# Code Implementation (Gate 0)

## Overview

This skill executes the implementation phase of the development cycle:
- Selects the appropriate specialized agent based on task content
- Applies project standards from docs/PROJECT_RULES.md
- Follows TDD methodology (RED → GREEN → REFACTOR)
- Documents implementation decisions

## CRITICAL: Role Clarification

**This skill ORCHESTRATES. Agents IMPLEMENT.**

| Who | Responsibility |
|-----|----------------|
| **This Skill** | Select agent, prepare prompts, track state, validate outputs |
| **Implementation Agent** | Write tests, write code, follow standards |

---

## Step 1: Validate Input

<verify_before_proceed>
- unit_id exists
- requirements exists
- language is valid (go|typescript|python)
- service_type is valid (api|worker|batch|cli|frontend|bff)
</verify_before_proceed>

```text
REQUIRED INPUT (from ring:dev-cycle orchestrator):
- unit_id: [task/subtask being implemented]
- requirements: [acceptance criteria or task description]
- language: [go|typescript|python]
- service_type: [api|worker|batch|cli|frontend|bff]

OPTIONAL INPUT:
- technical_design: [path to design doc]
- existing_patterns: [patterns to follow]
- project_rules_path: [default: docs/PROJECT_RULES.md]

if any REQUIRED input is missing:
  → STOP and report: "Missing required input: [field]"
  → Return to orchestrator with error
```

## Step 2: Validate Prerequisites

<block_condition>
- PROJECT_RULES.md does not exist at project_rules_path
</block_condition>

If condition is true, STOP and return error to orchestrator.

```text
1. Check PROJECT_RULES.md exists:
   Read tool → project_rules_path (default: docs/PROJECT_RULES.md)
   
   if not found:
     → STOP with blocker: "Cannot implement without project standards"
     → Return error to orchestrator

2. Select implementation agent based on language:
   
   | Language | Service Type | Agent |
   |----------|--------------|-------|
   | go | api, worker, batch, cli | ring:backend-engineer-golang |
   | typescript | api, worker | ring:backend-engineer-typescript |
   | typescript | frontend, bff | frontend-bff-engineer-typescript |
   
   Store: selected_agent = [agent name]
```

## Step 3: Initialize Implementation State

```text
implementation_state = {
  unit_id: [from input],
  agent: selected_agent,
  tdd_red: {
    status: "pending",
    test_file: null,
    failure_output: null
  },
  tdd_green: {
    status: "pending",
    implementation_files: [],
    pass_output: null
  },
  files_created: [],
  files_modified: [],
  commit_sha: null
}
```

## Step 4: Gate 0.1 - TDD-RED (Write Failing Test)

<dispatch_required agent="[selected_agent]" model="opus">
Write failing test for unit_id following TDD-RED methodology.
</dispatch_required>

```yaml
Task:
  subagent_type: "[selected_agent]"  # e.g., "ring:backend-engineer-golang"
  model: "opus"
  description: "TDD-RED: Write failing test for [unit_id]"
  prompt: |
    ⛔ TDD-RED PHASE: Write a FAILING Test

    ## Input Context
    - **Unit ID:** [unit_id]
    - **Requirements:** [requirements]
    - **Language:** [language]
    - **Service Type:** [service_type]

    ## Project Standards
    Read and follow: [project_rules_path]

    ## Ring Standards Reference
    For Go: https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/golang.md
    For TS: https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/typescript.md

    ## Your Task
    1. Write a test that captures the expected behavior
    2. The test MUST FAIL (no implementation exists yet)
    3. Run the test and capture the FAILURE output

    ## Requirements for Test
    - Follow project naming conventions from PROJECT_RULES.md
    - Use table-driven tests (Go) or describe/it blocks (TS)
    - Test the happy path and edge cases
    - Include meaningful assertion messages

    ## Required Output Format

    ### Test File
    **Path:** [path/to/test_file]
    
    ```[language]
    [test code]
    ```

    ### Test Execution
    **Command:** [test command]
    **Result:** FAIL (expected)

    ### Failure Output (MANDATORY)
    ```
    [paste actual test failure output here]
    ```

    ⛔ HARD GATE: You MUST include actual failure output.
    Without failure output, TDD-RED is not complete.
```

## Step 5: Validate TDD-RED Output

<block_condition>
- failure_output is missing
- failure_output does not contain "FAIL"
</block_condition>

If any condition is true, re-dispatch agent with clarification.

```text
Parse agent output:

1. Extract test file path
2. Extract failure output

if failure_output is missing or does not contain "FAIL":
  → STOP: "TDD-RED incomplete - no failure output captured"
  → Re-dispatch agent with clarification

if failure_output contains "FAIL":
  → implementation_state.tdd_red = {
      status: "completed",
      test_file: [extracted path],
      failure_output: [extracted output]
    }
  → Proceed to Step 6
```

## Step 6: Gate 0.2 - TDD-GREEN (Implementation)

**PREREQUISITE:** `implementation_state.tdd_red.status == "completed"`

<dispatch_required agent="[selected_agent]" model="opus">
Implement code to make test pass following TDD-GREEN methodology.
</dispatch_required>

```yaml
Task:
  subagent_type: "[selected_agent]"
  model: "opus"
  description: "TDD-GREEN: Implement code to pass test for [unit_id]"
  prompt: |
    ⛔ TDD-GREEN PHASE: Make the Test PASS

    ## Input Context
    - **Unit ID:** [unit_id]
    - **Requirements:** [requirements]
    - **Language:** [language]
    - **Service Type:** [service_type]

    ## TDD-RED Results (from previous phase)
    - **Test File:** [implementation_state.tdd_red.test_file]
    - **Failure Output:**
    ```
    [implementation_state.tdd_red.failure_output]
    ```

    ## Project Standards
    Read and follow: [project_rules_path]

    ## Ring Standards Reference
    For Go: https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/golang.md
    For TS: https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/typescript.md

    ## ⛔ CRITICAL: all Ring Standards Apply (no DEFERRAL)
    See Ring Standards for mandatory requirements:
    - Structured JSON logging with trace_id correlation
    - OpenTelemetry instrumentation (spans in every function)
    - Error handling (no panic, wrap with context)
    - Context propagation

    **⛔ HARD GATE:** If you output "DEFERRED" for any Ring Standard → Implementation is INCOMPLETE.

    ## Your Task
    1. Write MINIMAL code to make the test pass
    2. Follow all Ring Standards (logging, tracing, error handling)
    3. **Instrument all code with telemetry** (100% of handlers, services, repositories)
    4. Run the test and capture the PASS output

    ## ⛔ MANDATORY: Telemetry Instrumentation (NON-NEGOTIABLE)

    <cannot_skip>
    - 90%+ instrumentation coverage required
    - WebFetch standards file before implementation
    - Follow exact patterns from standards
    - Output Standards Coverage Table with evidence
    </cannot_skip>

    **every function that does work MUST be instrumented with telemetry.**
    This is not optional. This is not "nice to have". This is REQUIRED.

    ### What "Instrumented" Means
    1. **Extract logger/tracer from context** (not create new ones)
    2. **Create a child span** for the operation
    3. **Defer span.End()** immediately
    4. **Use structured logging** correlated with trace
    5. **Handle errors with span attribution** (business vs technical)

    ### Language-Specific Patterns (MANDATORY)

    **⛔ HARD GATE: Agent MUST WebFetch standards file BEFORE writing any code.**

    | Language | Standards File | REQUIRED Sections to WebFetch |
    |----------|----------------|-------------------------------|
    | **Go** | `golang.md` | "Telemetry & Observability (MANDATORY)", "Child Spans", "Context Propagation", "Anti-Patterns" |
    | **TypeScript** | `typescript.md` | "Observability", "Telemetry Patterns", "Context Propagation", "Anti-Patterns" |

    **⛔ NON-NEGOTIABLE: Agent MUST implement EXACTLY the patterns from standards. no deviations. no shortcuts.**

    | Requirement | Enforcement |
    |-------------|-------------|
    | WebFetch standards file | MANDATORY before implementation |
    | Follow exact patterns | REQUIRED - copy structure from standards |
    | Output Standards Coverage Table | REQUIRED - with file:line evidence |
    | 90%+ instrumentation coverage | HARD GATE - implementation REJECTED if below |

    ### ⛔ FORBIDDEN Patterns (HARD BLOCK)
    
    **Agent MUST WebFetch standards and check Anti-Patterns table. Violations = REJECTED.**

    - **Go:** `golang.md` → "Anti-Patterns" table - MUST check all rows
    - **TypeScript:** `typescript.md` → "Anti-Patterns" table - MUST check all rows

    **If agent uses any forbidden pattern → Implementation is INVALID. Start over.**

    ### Verification (MANDATORY)
    
    **Agent MUST output Standards Coverage Table per `standards-coverage-table.md`.**
    
    - all sections MUST show ✅ or N/A
    - any ❌ = Implementation REJECTED
    - Missing table = Implementation INCOMPLETE

    ## Required Output Format

    ### Implementation Files
    | File | Action | Lines |
    |------|--------|-------|
    | [path] | Created/Modified | +/-N |

    ### Code
    **Path:** [path/to/implementation_file]
    
    ```[language]
    [implementation code]
    ```

    ### Test Execution
    **Command:** [test command]
    **Result:** PASS

    ### Pass Output (MANDATORY)
    ```
    [paste actual test pass output here]
    ```

    ### Standards Compliance
    - Structured Logging: ✅/❌
    - OpenTelemetry Spans: ✅/❌
    - Error Handling: ✅/❌
    - Context Propagation: ✅/❌

    ### Commit
    **SHA:** [commit hash after implementation]
```

## Step 7: Validate TDD-GREEN Output

```text
Parse agent output:

1. Extract implementation files
2. Extract pass output
3. Extract standards compliance
4. Extract commit SHA

if pass_output is missing or does not contain "PASS":
  → STOP: "TDD-GREEN incomplete - test not passing"
  → Re-dispatch agent with error details

if any standards compliance is ❌:
  → STOP: "Standards not met - [list failing standards]"
  → Re-dispatch agent to fix

if pass_output contains "PASS" and all standards ✅:
  → implementation_state.tdd_green = {
      status: "completed",
      implementation_files: [extracted files],
      pass_output: [extracted output],
      commit_sha: [extracted SHA]
    }
  → Proceed to Step 8
```

## Step 8: Prepare Output

```text
Generate skill output:

## Implementation Summary
**Status:** PASS
**Unit ID:** [unit_id]
**Agent:** [selected_agent]
**Commit:** [commit_sha]

## TDD Results
| Phase | Status | Output |
|-------|--------|--------|
| RED | ✅ | [first line of failure_output] |
| GREEN | ✅ | [first line of pass_output] |

## Files Changed
| File | Action | Lines |
|------|--------|-------|
[table from implementation_files]

**Files Created:** [count]
**Files Modified:** [count]
**Tests Added:** [count]

## Standards Compliance
- Structured Logging: ✅
- OpenTelemetry Spans: ✅
- Error Handling: ✅
- Context Propagation: ✅

## Handoff to Next Gate
- Implementation status: COMPLETE
- Code compiles: ✅
- Tests pass: ✅
- Standards met: ✅
- Ready for Gate 1 (DevOps): YES
- Environment needs: [list any new deps, env vars, services]
```

---

## Pressure Resistance

See [shared-patterns/shared-pressure-resistance.md](../shared-patterns/shared-pressure-resistance.md) for universal pressure scenarios.

| User Says | Your Response |
|-----------|---------------|
| "Skip TDD, just implement" | "TDD is MANDATORY. Dispatching agent for RED phase." |
| "Code exists, just add tests" | "DELETE existing code. TDD requires test-first." |
| "Add observability later" | "Observability is part of implementation. Agent MUST add it now." |

---

## Anti-Rationalization Table

See [shared-patterns/shared-anti-rationalization.md](../shared-patterns/shared-anti-rationalization.md) for universal anti-rationalizations.

### Gate 0-Specific Anti-Rationalizations

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Test passes on first run" | Passing test ≠ TDD. Test MUST fail first. | **Rewrite test to fail first** |
| "Skip RED, go straight to GREEN" | RED proves test validity | **Execute RED phase first** |
| "I'll add observability later" | Later = never. Observability is part of GREEN. | **Add logging + tracing NOW** |
| "Minimal code = no logging" | Minimal = pass test. Logging is a standard, not extra. | **Include observability** |
| "DEFERRED to later tasks" | DEFERRED = FAILED. Standards are not deferrable. | **Implement all standards NOW** |
| "Using raw OTel is fine" | lib-commons wrappers are MANDATORY for consistency | **Use libCommons.NewTrackingFromContext** |
| "c.JSON() works the same" | Direct Fiber breaks response standardization | **Use libHTTP.OK(), libHTTP.WithError()** |
| "This function is too simple for spans" | Simple ≠ exempt. all functions need spans. | **Add span to every function** |
| "Telemetry adds overhead" | Observability is non-negotiable for production | **Instrument 100% of code paths** |

## Agent Selection Guide

| Language | Service Type | Agent |
|----------|--------------|-------|
| Go | API, Worker, Batch, CLI | `ring:backend-engineer-golang` |
| TypeScript | API, Worker | `ring:backend-engineer-typescript` |
| TypeScript | Frontend, BFF | `frontend-bff-engineer-typescript` |
| React/CSS | Design, Styling | `ring:frontend-designer` |

---

## Execution Report Format

```markdown
## Implementation Summary
**Status:** [PASS|FAIL|PARTIAL]
**Unit ID:** [unit_id]
**Agent:** [agent]
**Duration:** [Xm Ys]

## TDD Results
| Phase | Status | Output |
|-------|--------|--------|
| RED | ✅/❌ | [summary] |
| GREEN | ✅/❌ | [summary] |

## Files Changed
| File | Action | Lines |
|------|--------|-------|
| [path] | [Created/Modified] | [+/-N] |

## Standards Compliance
- Structured Logging: ✅/❌
- OpenTelemetry Spans: ✅/❌
- Error Handling: ✅/❌
- Context Propagation: ✅/❌

## Handoff to Next Gate
- Implementation status: [COMPLETE|PARTIAL]
- Ready for Gate 1: [YES|no]
- Environment needs: [list]
```
