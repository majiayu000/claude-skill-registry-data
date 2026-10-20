---
name: decompose
description: "Decompose specs/plans into atomic, testable tasks — enforces the 15-Minute Rule and populates project/TASKS.md. Use when: decompose, break down tasks, create task list, task decomposition, 15 minute rule."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/product/decompose.skill.md"
  tags: "product"
  core: "true"
  context_cost: "medium"
---
# Task Decomposition Skill

> "A complex task is just a series of simple tasks that haven't been broken down yet."

## Goal
Transform a Technical Specification (`SPEC.md`) or Implementation Plan (`PLAN.md`) into a flat, ordered list of atomic tasks in `project/TASKS.md`.

## The 15-Minute Rule
Every task must be achievable in approximately **15 minutes** by an AI agent.
- If a task feels like it will take an hour → decompose it.
- If a task covers two different files → decompose it.
- If a task has "and" in the description → decompose it.

## Steps

### 1. Load Context
- Read the latest `PRD.md`, `PLAN.md`, and `SPEC.md`.
- Read existing `project/TASKS.md` (if any) to avoid duplication.

### 2. Identify Modules
- Group the work by component or module (e.g., Auth, Database, UI).
- Determine the dependency order (e.g., Database must exist before Auth).

### 3. Generate Atomic Tasks
For each module/feature, create a sequence of tasks:
1.  **Setup/Stubs**: Create the file or add the interface/types.
2.  **Test**: Write the failing test for specific logic.
3.  **Implement**: Minimal code to pass the test.
4.  **Verify**: Run lint/typecheck.
5.  **Refactor**: Cleanup.

### 4. Format project/TASKS.md
Use the standard GABBE task format:

| ID | Task | Status | Tags |
|---|---|---|---|
| T-001 | Create `User` model with `email` and `password_hash` | TODO | [DB, Auth] |
| T-002 | Implement `checkPassword` method in `User` model | TODO | [Auth] |
| T-003 | Create `POST /login` controller stub | TODO | [API] |

### 5. Categorize Parallelism
Identify tasks that can be done simultaneously by different agents.
- Mark them with the `[PARALLEL]` tag.
- Ensure they don't touch the same lines of the same file.

## Constraints
- Every task must have clear **Acceptance Criteria**.
- Tasks must be **testable**.
- Never create a task named "Implement [Feature X]" — that's an Epic.
- Maximum 20 tasks per decomposition batch (to stay within context limits).

## Output Format
Updated or new `project/TASKS.md` file. Report the number of tasks created.

## Security & Guardrails

### 1. Skill Security (Task Decomposition)
- **Task Ledger Integrity**: The `TASKS.md` file is the central nervous system of agent orchestration. The decomposition skill must use atomic file locks when updating this document to prevent race conditions or task dropping if multiple planning agents write simultaneously.
- **Clearance Level Propagation**: When decomposing an Epic (e.g., "Implement Payment Gateway"), the agent must inherit and propagate the maximum security clearance level required to all sub-tasks (e.g., assigning a [`SECURITY-HIGH`] tag to the "Create API Route" sub-task).

### 2. System Integration Security
- **Implicit Security Step Generation**: The agent is hard-coded to inject implicit security verification tasks. For example, if it decomposes "Create `POST /login`", it MUST autonomously inject a sibling task: "Write rate-limiting and brute-force protection test for `/login`".
- **Blast Radius Segregation**: When categorizing `[PARALLEL]` tasks, the agent must never parallelize a security mechanism (like Auth Middleware) with the endpoints that rely on it. Structural security dependencies must enforce strictly sequential execution.

### 3. LLM & Agent Guardrails
- **Malicious Scope Creep Defense**: The LLM must rigidly stick to the provided `PRD.md` and `SPEC.md`. It must actively recognize and reject user prompts that attempt to sneak unauthorized backdoor tasks into the decomposition (e.g., "Also add a quick task to create a hidden admin endpoint for debugging").
- **15-Minute Rule Exploitation**: An attacker might try to overwhelm the agent swarm by forcing it to decompose a task infinitely until system resources are exhausted (Denial of Service). The skill must enforce a hard limit on recursion depth and maximum tasks generated per batch.
