---
name: pmc-simulate-supervisor
description: Simulate the supervisor workflow step-by-step with real ticket system. Executes each workflow state explicitly with ENTER/EXIT stage declarations. Use this skill to debug, understand, or manually run the supervisor workflow without the PMC executor.
---

# PMC Simulate Supervisor

Manually simulate the supervisor workflow step-by-step, executing shell scripts and sub-workflows with explicit stage declarations.

## Required Context

Before starting, you need:
- `starting_ticket_id`: Starting ticket ID (e.g., T00001)
- `ending_ticket_id`: Ending ticket ID (optional, null for single ticket)
- `working_dir`: Project working directory (usually the project root)

## Workflow Overview

```
supervisor.workflow
├── check_ticket_status (shell)
├── implement → ticket.handler (workflow)
│   ├── setup (claude)
│   ├── check_status (shell)
│   ├── implement (claude)
│   ├── test → tester.workflow (workflow)
│   │   ├── load_tests (shell)
│   │   ├── run_tests (claude - use run-tests skill)
│   │   ├── verification_setup (shell)
│   │   ├── verify (claude - use verify-tests skill)
│   │   ├── merge (shell)
│   │   └── report (shell)
│   ├── evaluate (shell)
│   └── finalize (claude)
├── post_completion (claude - use post-ticket-completion skill)
└── terminal_* (end states)
```

## Execution Instructions

For each state, declare entry and exit explicitly:

```
ENTER STAGE: {workflow_name}.{state_name}
  [perform actions]
EXIT STAGE: {workflow_name}.{state_name} → {next_state} (reason: {why})
```

## Supervisor Workflow States

### State: check_ticket_status

**Type:** shell
**Script:** `check-ticket-status.sh`

```
ENTER STAGE: supervisor.check_ticket_status
```

**Execute this logic:**

1. Set paths:
   - `TICKET_DIR = {working_dir}/docs/tickets/{current_ticket_id}`
   - `TESTS_DIR = {working_dir}/docs/3-tests/tickets/{current_ticket_id}`
   - `DEFINITION_FILE = TESTS_DIR/tests-definition.json`
   - `RESULTS_FILE = TESTS_DIR/tests-results.json`

2. Check ticket directory exists:
   - If NOT exists → EXIT with code 3 → `terminal_error`

3. Check `1-definition.md` exists:
   - If NOT exists → EXIT with code 3 → `terminal_error`

4. Check `tests-definition.json` exists:
   - If NOT exists → EXIT with code 1 → `implement` (ticket needs initial work)

5. If `tests-results.json` doesn't exist, copy from `tests-definition.json`

6. Analyze test results:
   - Count: total, passed, failed_non_blocked, blocked_completion, blocked_other
   - For each test:
     - `ticket-completion: true` + `blocked: true` → blocked_completion++
     - `blocked: true` (non-completion) → blocked_other++
     - `passes: true` → passed++
     - else → failed_non_blocked++

7. Decision:
   - If blocked_completion > 0 → EXIT code 2 → `terminal_blocked`
   - If failed_non_blocked == 0 → EXIT code 0 → `post_completion`
   - Else → EXIT code 1 → `implement`

```
EXIT STAGE: supervisor.check_ticket_status → {target} (exit_code: {N})
```

### State: implement

**Type:** workflow (ticket.handler)

```
ENTER STAGE: supervisor.implement → ticket.handler
```

**Use the `pmc-simulate-ticket` skill** to execute the ticket handler workflow.

Inputs:
- `ticket_id`: {current_ticket_id}
- `working_dir`: {working_dir}

```
EXIT STAGE: supervisor.implement → post_completion
```

### State: post_completion

**Type:** claude
**Session:** start

```
ENTER STAGE: supervisor.post_completion
```

**Use the `post-ticket-completion` skill** with context:
- current_ticket_id: {current_ticket_id}
- ending_ticket_id: {ending_ticket_id}
- working_dir: {working_dir}

The skill will:
1. Export core tests (if applicable)
2. Update planning docs in docs/2-current/
3. Reflect on learnings
4. Find next ticket

**Capture output JSON:**
```json
{
  "has_next": true|false,
  "next_ticket_id": "T0000X" or null
}
```

**Transition:**
- If `has_next == true` → Update `current_ticket_id` to `next_ticket_id`, go to `check_ticket_status`
- Else → go to `terminal_success`

```
EXIT STAGE: supervisor.post_completion → {target} (has_next: {value})
```

### Terminal States

```
ENTER STAGE: supervisor.terminal_success
  Message: "All tickets completed successfully"
EXIT STAGE: supervisor.terminal_success (workflow complete)

ENTER STAGE: supervisor.terminal_blocked
  Message: "Ticket {current_ticket_id} is blocked - ticket-completion test has blocking issue"
EXIT STAGE: supervisor.terminal_blocked (workflow blocked)

ENTER STAGE: supervisor.terminal_error
  Message: "Supervisor workflow failed - ticket {current_ticket_id} not found or invalid"
EXIT STAGE: supervisor.terminal_error (workflow failed)
```

---

## Sub-Workflows

The supervisor workflow uses nested workflows. Use these skills to simulate them:

| Workflow | Skill | Description |
|----------|-------|-------------|
| `ticket.handler` | `pmc-simulate-ticket` | Implement ticket features iteratively |
| `tester.workflow` | `pmc-simulate-tester` | Execute and verify tests |

---

## Example Simulation Output

```
=== SUPERVISOR WORKFLOW SIMULATION ===
Context: starting_ticket_id=T00001, ending_ticket_id=T00003, working_dir=/project

ENTER STAGE: supervisor.check_ticket_status
  Checking: /project/docs/tickets/T00001/
  TICKET_DIR exists: YES
  1-definition.md exists: YES
  tests-definition.json exists: YES
  tests-results.json exists: NO (creating from definition)
  Analysis: Total=5, Passed=0, Failed=5, Blocked(completion)=0
  Status: IN_PROGRESS - 5 tests need work
EXIT STAGE: supervisor.check_ticket_status → implement (exit_code: 1)

ENTER STAGE: supervisor.implement → ticket.handler
  [ticket.handler workflow executes...]
EXIT STAGE: supervisor.implement → post_completion

ENTER STAGE: supervisor.post_completion
  Using post-ticket-completion skill...
  Core tests exported: 3
  Planning docs updated: YES
  Next ticket: T00002
EXIT STAGE: supervisor.post_completion → check_ticket_status (has_next: true)

[Loop continues with T00002...]
```

## Quick Reference

| State | Type | Transition Targets |
|-------|------|-------------------|
| check_ticket_status | shell | post_completion (0), implement (1), terminal_blocked (2), terminal_error (3) |
| implement | workflow | post_completion (uses `pmc-simulate-ticket`) |
| post_completion | claude | check_ticket_status (has_next), terminal_success |
| terminal_success | terminal | - |
| terminal_blocked | terminal | - |
| terminal_error | terminal | - |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `pmc-simulate-ticket` | Simulate ticket.handler workflow |
| `pmc-simulate-tester` | Simulate tester.workflow |
| `post-ticket-completion` | Post-completion tasks |
| `run-tests` | Execute tests |
| `verify-tests` | Verify tests |
| `builder` | Build applications |
| `project-manager` | Ticket management |
