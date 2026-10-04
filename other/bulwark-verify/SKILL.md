---
name: bulwark-verify
description: Generate runnable verification scripts for components. Orchestrates assertion-patterns and component-patterns to produce executable scripts.
user-invocable: true
skills:
  - assertion-patterns
  - component-patterns
  - bug-magnet-data
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - Skill
  - Task
  - Write
version: 1.0.1
author: "Ashay Kubal @ Qball Inc."
---

# Bulwark Verify

## Purpose

Generate runnable verification scripts that test real component behavior without mocks.
This skill orchestrates assertion-patterns (P2.1) and component-patterns (P2.2) to produce
executable scripts for any component type.

## When to Use

**Load this skill when:**
- User requests `/bulwark-verify [path]`
- test-audit Step 7 needs verification scripts
- Generating standalone verification for a component

**DO NOT use for:**
- Running existing tests (use `just test`)
- Writing unit tests (implement directly)
- Test auditing (use `test-audit` skill)

---

## Usage

```
/bulwark-verify [path] [--execute]
```

**Examples:**
- `/bulwark-verify src/cli.ts` - Generate verification script for CLI
- `/bulwark-verify src/server.ts --execute` - Generate and run
- `/bulwark-verify` - Infer from recent context

---

## MANDATORY EXECUTION STEPS

> **WARNING**: These steps are BINDING instructions, not suggestions. You MUST execute
> each step in order. Do NOT substitute your judgment for these instructions.
> Do NOT skip sub-agent spawning. Do NOT modify the execution flow.

When this skill is loaded, execute these steps **exactly as written**:

### Step 1: Resolve Target

```
IF $ARGUMENTS provided:
    target = first non-flag argument
    execute_flag = "--execute" in $ARGUMENTS
ELSE:
    Look for component files in recent conversation context
    IF found: target = that path
    ELSE: Ask user: "Which component should I generate a verification script for?"
```

### Step 2: Detect Project Language

Check for project manifest files in order (search from target file's directory up to project root):

| Check | Language | Test Runner |
|-------|----------|-------------|
| `package.json` exists | Node | jest/vitest/node |
| `pyproject.toml` OR `setup.py` exists | Python | pytest/python |
| `Cargo.toml` exists | Rust | cargo test |
| None of the above | Generic | bash |

### Step 3: Analyze Component

1. **Read the target file**

2. **Identify component type** using indicators from `component-patterns` skill:
   - Has `spawn`/`exec`/`execSync` imports → Process Spawner
   - Has `listen()`/`createServer`/`express()`/`fastify()` → HTTP Server
   - Has `fs.readFile`/`parse` functions → File Parser
   - Has `process.argv`/`yargs`/`commander`/`argparse` → CLI Command
   - Has database imports (`pg`, `mysql`, `mongoose`, `prisma`) → Database
   - Has `fetch`/`axios`/`got`/`requests` calls → External API

3. **Load dependent skills:**
   - Load `assertion-patterns` skill content
   - Load `component-patterns` skill content

4. **Load bug-magnet-data for the component type** [REQUIRED]:
   - Read the context file matching the component type:
     | Component Type | Context File |
     |----------------|--------------|
     | CLI Command | `bug-magnet-data/context/cli-args.md` |
     | HTTP Server | `bug-magnet-data/context/http-body.md` |
     | File Parser | `bug-magnet-data/context/file-contents.md` |
     | Database | `bug-magnet-data/context/db-query.md` |
     | Process Spawner | `bug-magnet-data/context/process-spawn.md` |
     | External API | `bug-magnet-data/context/http-body.md` |
   - Read the "Applicable Categories" section from the context file
   - Load T0 + T1 data files listed in the context file:
     - T0 (Always): `data/strings/boundaries.yaml`, `data/numbers/boundaries.yaml`
     - T1 (Common): Based on context file recommendations

5. **Select applicable patterns:**
   - From `assertion-patterns`: Identify T1-T4 transformation patterns relevant to the component
   - From `component-patterns`: Select the matching component type template
   - From `bug-magnet-data`: Extract concrete edge case values to include in generated script

### Step 4: Generate Script [SPAWN-REQUIRED]

**You MUST spawn a Sonnet sub-agent for script generation.** Do NOT generate the script yourself.

```
Task(
    description="Generate verification script for {component_name}",
    subagent_type="general-purpose",
    prompt=<constructed_4part_prompt_from_template_below>
)
```

The sub-agent writes the script to `tmp/verification/{component_name}-verify.{ext}`.

### Step 5: Validate Generated Script [REQUIRED]

After the sub-agent returns, validate the generated script syntax:

| Language | Validation Command | Success |
|----------|-------------------|---------|
| Node | `node --check {script_path}` | Exit 0 |
| Python | `python -m py_compile {script_path}` | Exit 0 |
| Bash | `bash -n {script_path}` | Exit 0 |

If validation fails:
1. Read the error message
2. Fix the syntax issue in the generated script
3. Re-validate until successful
4. Only then proceed to Step 6

### Step 6: Report Results

Present summary to user:

```markdown
## Verification Script Generated

**Component:** {component_path}
**Type:** {component_type}
**Language:** {language}

**Script location:** tmp/verification/{name}-verify.{ext}

**To run manually:**
```
{runner_command}
```
```

If `--execute` flag was provided:
1. Run the generated script using Bash
2. Capture output
3. Report PASS/FAIL counts
4. Show any failures with details

---

## Generation Prompt Template

Use this 4-part prompt when spawning the Sonnet sub-agent:

```markdown
## GOAL

Generate an executable verification script for `{component_path}` that tests real
component behavior without mocks. The script must verify observable output and
report clear PASS/FAIL for each test.

## CONSTRAINTS

- Language: {detected_language}
- Test runner: {runner} (e.g., jest, pytest, bash)
- Component type: {detected_type}
- MUST be directly executable: `{runner_command}`
- MUST use assertion patterns from assertion-patterns skill (real output, not mock calls)
- MUST follow component pattern from component-patterns skill ({component_type} verification)
- MUST include edge cases from bug-magnet-data (boundaries, special values, injection patterns)
- Include setup and teardown if component requires it
- Report clear PASS/FAIL for each verification
- Handle cleanup on both success and failure (use trap for bash, afterAll for jest, fixtures for pytest)
- Exit with code 0 on all pass, code 1 on any failure
- EXCLUDE destructive patterns marked `safe_for_automation: false` (add as commented-out manual tests)

## CONTEXT

### Component Code
```{language}
{component_content}
```

### Component Type
{detected_type}

### Applicable Assertion Patterns (from assertion-patterns)
{relevant_assertion_patterns}

### Applicable Component Pattern (from component-patterns)
{component_pattern_template}

### Edge Cases (from bug-magnet-data) [REQUIRED]
Include these edge cases in verification tests:

**T0 (Always include):**
{t0_edge_cases_from_bug_magnet_data}

**T1 (Include if component handles input):**
{t1_edge_cases_from_bug_magnet_data}

**Destructive patterns (manual-only - add as comments):**
{destructive_patterns_if_any}

## OUTPUT

Write script to: `tmp/verification/{component_name}-verify.{ext}`

Extension mapping:
- Node → `.test.js`
- Python → `_test.py`
- Rust → `.rs` (or `.sh` if cargo test not suitable)
- Generic → `.sh`

### Script Structure
1. Setup (create temp files, start services, initialize test DB)
2. Execute component under test
3. Verify observable output (not mock calls)
4. Report PASS/FAIL clearly for each test
5. Cleanup (kill processes, remove temp files)
6. Exit with appropriate code (0 = all pass, 1 = any fail)

### Report your actions to the log file
Write to: `logs/bulwark-verify-{YYYYMMDD-HHMMSS}.yaml`
```

---

## Output Formats

### Generated Script Location
```
tmp/verification/{component-name}-verify.{ext}
```

### README Files (Per-Component)

If generating a README for the verification script, name it per-component to avoid overwrites:
```
tmp/verification/{component-name}-README.md
```

**NOT:** `tmp/verification/README.md` (would be overwritten by subsequent runs)

### Cleanup Behavior

Generated scripts **persist in `tmp/verification/`** for inspection and debugging:
- Scripts are NOT automatically deleted after execution
- `tmp/` is in `.gitignore` - scripts won't be committed
- Manual cleanup: `rm -rf tmp/verification/*`

This allows:
- Post-run inspection of generated scripts
- Iterative refinement of verification approach
- Debugging when tests fail

### Log Schema
```yaml
# Top-level — required for Stop-hook per-file pipeline-recursion suppression.
# List every .sh verification script generated for this run (Bulwark verify
# scripts live under tmp/verification/ but are SCRIPT-bucket files for
# coverage purposes). Paths relative to ${CLAUDE_PROJECT_DIR}. Empty list
# `[]` if no script was emitted. Missing field disables suppression.
reviewed_files:
  - tmp/verification/{component-name}-verify.sh

metadata:
  skill: bulwark-verify
  timestamp: {ISO-8601}
  model: sonnet

generation:
  target: {component_path}
  language: node|python|rust|generic
  component_type: cli|http|file-parser|process|database|api
  script_path: tmp/verification/{name}-verify.{ext}
  patterns_used:
    assertion: [T1_transformation, T2_transformation]
    component: "{component_type} verification"

execution:  # Only if --execute
  ran: true
  runner: {runner_command}
  exit_code: 0|1
  duration_ms: 1234
  results:
    pass: 3
    fail: 0
  output: |
    === Verification: {component} ===
    Test 1: Basic functionality... PASS
    Test 2: Error handling... PASS
    Test 3: Edge cases... PASS
    === All tests passed ===

summary: |
  Generated verification script for {component} ({type}).
  Script: tmp/verification/{name}-verify.{ext}
  Run with: {runner_command}
  [Execution: 3 passed, 0 failed]
```

### Diagnostic Schema
```yaml
# Top-level — mirror the same list emitted in the run log (Stop hook contract).
reviewed_files:
  - tmp/verification/{component-name}-verify.sh

skill: bulwark-verify
timestamp: {ISO-8601}
diagnostics:
  model_requested: sonnet
  model_actual: sonnet
  context_type: main
  language_detected: node|python|rust|generic
  component_type: cli|http|file-parser|process|database|api
  patterns_loaded:
    - assertion-patterns
    - component-patterns
  script_generated: true
  script_path: tmp/verification/{name}-verify.{ext}
  execution_requested: true|false
  execution_result: pass|fail|skipped
  completion_status: success|error
```

Write diagnostic output to: `logs/diagnostics/bulwark-verify-{YYYYMMDD-HHMMSS}.yaml`

---

## Integration with test-audit

When test-audit Step 7 invokes this skill:

1. test-audit provides the test file path and violation info
2. This skill generates a verification script as intermediate artifact
3. The script validates the rewrite approach before modifying the test
4. If verification passes, test-audit proceeds with the rewrite

**Flow:**
```
test-audit Step 7
    → Load assertion-patterns
    → Load component-patterns
    → Generate verification script (tmp/verification/)
    → Run verification script
    → If pass: Apply rewrite to test file
    → If fail: Report issue, do not rewrite
```

---

## Runner Commands by Language

| Language | Default Runner | Command |
|----------|---------------|---------|
| Node | node (built-in test) | `node --test tmp/verification/{name}-verify.test.js` |
| Node (Jest) | jest | `npx jest tmp/verification/{name}-verify.test.js` |
| Python | pytest | `pytest tmp/verification/{name}_test.py -v` |
| Rust | cargo | `cargo test --test {name}` |
| Generic | bash | `bash tmp/verification/{name}-verify.sh` |

When generating scripts, prefer the simplest runner:
- For Node: Use built-in `node --test` if no external deps needed
- For Python: Use `pytest` for better output
- For Generic: Always use bash

---

## Error Handling

### Target file not found
```
Error: Target file not found: {path}
Please provide a valid path to the component you want to verify.
```

### Language detection failed
```
Warning: Could not detect project language. Using generic (bash) templates.
To specify: /bulwark-verify {path} --lang=node
```

### Component type detection failed
```
Warning: Could not determine component type from code analysis.
Please specify: /bulwark-verify {path} --type=cli

Available types: cli, http, file-parser, process, database, api
```

### Script generation failed
```
Error: Failed to generate verification script.
Reason: {error_message}

Check logs/bulwark-verify-*.yaml for details.
```

---

## Examples

### Example 1: CLI Component
```
User: /bulwark-verify src/cli.ts

Output:
## Verification Script Generated

**Component:** src/cli.ts
**Type:** CLI Command
**Language:** Node

**Script location:** tmp/verification/cli-verify.test.js

**To run manually:**
```
node --test tmp/verification/cli-verify.test.js
```
```

### Example 2: HTTP Server with Execution
```
User: /bulwark-verify src/server.ts --execute

Output:
## Verification Script Generated

**Component:** src/server.ts
**Type:** HTTP Server
**Language:** Node

**Script location:** tmp/verification/server-verify.test.js

**Execution Results:**
```
=== HTTP Server Verification: server ===
Test 1: Health endpoint... PASS (HTTP 200)
Test 2: API response... PASS (valid JSON)
Test 3: 404 handling... PASS (HTTP 404)
=== All tests passed ===
```

**Summary:** 3 passed, 0 failed
```

### Example 3: Python Parser
```
User: /bulwark-verify src/parser.py

Output:
## Verification Script Generated

**Component:** src/parser.py
**Type:** File Parser
**Language:** Python

**Script location:** tmp/verification/parser_test.py

**To run manually:**
```
pytest tmp/verification/parser_test.py -v
```
```

---

## Completion Checklist

Before completing bulwark-verify execution, verify ALL items:

### Component Analysis (Step 3)
- [ ] Target file read successfully
- [ ] Component type identified (CLI, HTTP Server, File Parser, Database, Process Spawner, External API)
- [ ] Project language detected (Node, Python, Rust, Generic)
- [ ] `assertion-patterns` skill content loaded
- [ ] `component-patterns` skill content loaded
- [ ] `bug-magnet-data` context file loaded for component type
- [ ] T0 + T1 edge cases loaded from bug-magnet-data

### Script Generation (Step 4)
- [ ] Sonnet sub-agent spawned (NOT generated by orchestrator)
- [ ] Prompt includes component code, assertion patterns, component patterns
- [ ] Prompt includes edge cases from bug-magnet-data (T0 + T1 values)
- [ ] Script written to `tmp/verification/{component_name}-verify.{ext}`

### Validation (Step 5)
- [ ] Syntax validation command executed (node --check, python -m py_compile, bash -n)
- [ ] Validation passed (or errors fixed and re-validated)

### Edge Case Coverage
- [ ] T0 boundary values included (empty string, zero, null)
- [ ] T1 edge cases included if applicable (injection, unicode)
- [ ] Destructive patterns excluded or marked as manual-only comments

### Output
- [ ] Summary presented to user with script location and run command
- [ ] Log written to `logs/bulwark-verify-*.yaml`
- [ ] Diagnostics written to `logs/diagnostics/bulwark-verify-*.yaml`
- [ ] If `--execute`: Script executed, PASS/FAIL results reported

**Do NOT return to user until all applicable checklist items are verified.**

---

## Related Skills

- `assertion-patterns` (P2.1) - T1-T4 transformation patterns
- `component-patterns` (P2.2) - Component-type verification templates
- `bug-magnet-data` (P4.2) - Curated edge case test data
