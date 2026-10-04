---
name: planner
description: High-fidelity universal planning orchestrator. Transmutes complex requests into structured, skill-aware roadmaps with sequential phases, dependency-aware task sequencing, embedded test procedures, and gap-free coverage enforced by targeted user questioning before any plan is saved.
allowed-tools: list_dir, view_file, write_to_file, run_command, grep_search
---

# Universal Planner (Master Orchestrator)

This skill is the central authority for all project planning, architectural mapping, and task decomposition. This skill should be used for any request that requires multi-step implementation, refactoring, or new system design.

## 1. Pre-Planning: Skill Discovery
Before drafting a plan, the agent **MUST** perform "Skill Awareness" scanning:
1.  **Scan**: Run `list_dir` on `.agent/skills` to identify available specialized capabilities.
2.  **Analyze**: Match the technical requirements of the request (e.g., UI, AI, Persistence) to the relevant skills.
3.  **Cross-Reference**: If a skill is identified, the agent **MUST** use `view_file` on its `SKILL.md` to understand its specific standards (e.g., naming conventions, required base classes) before writing tasks for that module.

## 1b. Pre-Planning: Gap Resolution (MANDATORY Before Writing the Plan)
A plan must be complete before it is written. Incomplete information produces incomplete plans. The agent **MUST** execute this protocol before drafting Section IV:

### Step 1 — Gap Audit
After gathering context from the request and skill scan, the agent identifies every open question across these categories:
- **Scope**: Are there features, edge cases, or system boundaries that are undefined?
- **Inputs / Outputs**: Are data contracts, file formats, API signatures, or return types unclear?
- **Dependencies**: Are there external systems, libraries, or services whose behavior is unspecified?
- **Error & Edge Cases**: Are failure modes, null states, invalid inputs, or race conditions unaddressed?
- **Acceptance Criteria**: Is there any success condition that could be interpreted in more than one way?

### Step 2 — Ask Targeted Questions
If **any** gaps are found, the agent **MUST** ask the user to resolve them **before writing a single task**. Questions must be:
- **Targeted**: One question per gap. No compound questions.
- **Contextual**: Each question must explain *why* it matters to the plan (e.g., "This affects how the Save phase is structured").
- **Exhaustive in one round**: All gaps must be surfaced in a single question pass. The agent must not ask follow-up questions after the plan has started.

Format:
```
Before I write the plan, I need to resolve the following gaps:

1. [Gap area] — [Question]? (Affects: [which phase/module])
2. [Gap area] — [Question]? (Affects: [which phase/module])
...
```

### Step 3 — Confirm Completeness
Once all questions are answered, the agent confirms: *"All gaps resolved. Proceeding to plan."*
Only then does it write the roadmap. **A plan saved with known gaps is a plan error.**

### Step 4 — Mandatory Pause for Approval (CRITICAL)
After writing the roadmap to a `.md` file in `Documentation/Plans/`, the agent **MUST STOP ALL IMPLEMENTATION**.
No code changes, file deletions, or system modifications are permitted until the user provides explicit approval of the roadmap in Section IV. 
Failure to stop and wait for approval is a direct violation of this skill's protocol.
Proceeding to implementation without approval is an architectural risk and is PROHIBITED.
Once approval is received, the agent may state: *"Plan approved. Starting implementation."* and proceed to the first task.
## 2. Plan Structure: Modular Roadmap
All plans are saved to `Documentation/Plans/{task-slug}.md`. They must follow this high-fidelity structure:

### I. Executive Summary
- **Goal**: A single, punchy sentence defining the final outcome.
- **Success Metrics**: 2-3 measurable criteria for success (e.g., "Zero compile errors," "Visual parity with GDD mockups").

### II. Skill Matrix
A table mapping the project's technical components to your available skills:
| Component | Required Skill | Implementation Role |
|-----------|----------------|----------------------|
| [e.g., Save System] | `unity-data-persistence` | Handles JSON serialization and file I/O. |
| [e.g., Player HUD] | `unity-ui-toolkit` | Manages UXML layouts and USS styling. |

### III. Logic & Architecture (Optional)
A brief text description or Mermaid diagram of how the systems will interact.

### IV. Phased Roadmap (Sequential Stages)
The roadmap is a strict **sequence of Stages**. Each Stage represents a coherent unit of work that must be fully complete before the next Stage begins. Within each Stage, work is divided into **Modules**, then **Tasks**.

---

#### Stage Structure
Each Stage follows this template:

```
## Stage <N>: <Stage Name>
> **Entry Condition**: <What must be true before this Stage can begin>
> **Exit Condition**: <What must be true for this Stage to be considered complete>

### Module <N.M>: <Module Name>

- [ ] [P<N>.<M>.<T>] Task Name: <Specific Action>
      depends_on: <task-id | none>
      Verify: <Exact check or command>

[...more tasks...]

### 🧪 Stage <N> Test Procedures
> Executed once all tasks in this Stage are complete.
<See Test Procedure Format below>
```

---

#### Dependency Rules
Every task **MUST** carry a dependency declaration. This is non-optional:

- **No dependency** → `depends_on: none`
- **Single dependency** → `depends_on: <task-id>`
- **Multiple dependencies** → `depends_on: <task-id>, <task-id>`

Dependency IDs use the format `P<stage>.<module>.<task>` (e.g., `P1.2.3` = Stage 1, Module 2, Task 3).

The agent **MUST NOT** begin a task until all tasks in its `depends_on` field are marked `[x]`.

If a dependency chain creates a **cycle**, the plan is invalid — restructure stages before saving.

---

#### Test Procedure Format
A **Test Procedure block** is appended to every Stage that produces testable output. It is **not optional** if the Stage touches logic, data, UI, or any externally visible behavior.

Test Procedures must be **fully self-contained** — someone executing them must not need to read any other section. Each procedure specifies:

```
### 🧪 Stage <N> Test Procedures

#### Test <N>.1: <Test Name>
- **Type**: [Unit | Integration | Manual | E2E]
- **Preconditions**: <State of the system before this test runs>
- **Steps**:
  1. <Exact action or command>
  2. <Exact action or command>
- **Expected Result**: <Precise, observable outcome — no ambiguity>
- **Pass Command** *(if automated)*: `<exact command to run>`
- **Fail Indicators**: <What a failure looks like — error message, wrong state, missing output>

#### Test <N>.2: <Test Name>
[...repeat for each test case in this Stage...]
```

Rules for Test Procedures:
- **Cover the happy path AND at least one failure/edge case per module.**
- **Do not write vague outcomes.** "It works" is not an expected result. "The JSON file at `/saves/player.json` contains a `health` field with value `100`" is.
- **Automated tests must include the exact run command.** Manual tests must include step-by-step actions with exact inputs.
- **If a Stage is not yet testable** (e.g., it only creates scaffolding with no observable behavior), write: `> Stage <N> has no test procedures — no observable behavior is introduced.` and explain why.

---

#### Additional Guidelines
- **Priority**: Prioritize structural tasks, technical requirements, and execution steps.
- **Atomic Tasks**: Every task must represent a small, focused unit of work suitable for an "Atomic Commit."
- **Dependency Graph Sanity Check**: Before finalizing the plan, trace the dependency chain from the last task in each Stage back to `none`. Every path must terminate cleanly. Cycles are plan errors.
- **No Orphan Stages**: Every Stage except Stage 1 must reference what it builds on. Entry Conditions enforce this explicitly.

---

#### Full Example

```
## Stage 1: Core Serialization
> **Entry Condition**: Project compiles with zero errors.
> **Exit Condition**: Serializer round-trips player data without data loss.

### Module 1.1: Interface Layer

- [ ] [P1.1.1] Define ISerializable Interface: Create base interface in /Core/Interfaces
      depends_on: none
      Verify: File exists at /Core/Interfaces/ISerializable.cs, zero compile errors.

- [ ] [P1.1.2] Implement PlayerDataSerializer: Extend ISerializable for player struct
      depends_on: P1.1.1
      Verify: Class compiles; manual inspection confirms all required fields are mapped.

### Module 1.2: File I/O

- [ ] [P1.2.1] Build SaveManager: Wire serializer to file I/O layer
      depends_on: P1.1.2
      Verify: SaveManager.cs exists, compiles, exposes Save() and Load() methods.

### 🧪 Stage 1 Test Procedures

#### Test 1.1: Serializer Round-Trip
- **Type**: Unit
- **Preconditions**: PlayerDataSerializer is implemented; test runner is available.
- **Steps**:
  1. Instantiate a PlayerData struct with health=100, level=3, position=(1,2,0).
  2. Call PlayerDataSerializer.Serialize(playerData) → save to /tmp/test_save.json.
  3. Call PlayerDataSerializer.Deserialize("/tmp/test_save.json") → assign to result.
  4. Assert result.health == 100, result.level == 3, result.position == (1,2,0).
- **Expected Result**: All assertions pass; no exception thrown.
- **Pass Command**: `dotnet test --filter "SerializerRoundTripTest"`
- **Fail Indicators**: Assertion error, missing fields in JSON, FileNotFoundException.

#### Test 1.2: Missing File Handling
- **Type**: Unit
- **Preconditions**: No file exists at /tmp/nonexistent.json.
- **Steps**:
  1. Call PlayerDataSerializer.Deserialize("/tmp/nonexistent.json").
  2. Observe return value and any thrown exceptions.
- **Expected Result**: Method returns a default PlayerData struct; no unhandled exception.
- **Pass Command**: `dotnet test --filter "SerializerMissingFileTest"`
- **Fail Indicators**: Unhandled IOException, null reference, application crash.
```

### V. Final Verification Checklist
A global list of final "Acceptance Tests" to run before closing the task.

## 3. Core Principles
1.  **Strict BEM/Coding Standards**: Tasks must specify that implementation follows the `unity-development.md` and `unity-ui-toolkit.md` rules.
2.  **No Magic Values**: Plans must include steps to replace hardcoded values with constants or ScriptableObjects.
3.  **Atomic Verification**: Verification steps must be specific, not generic. (e.g., `Verify: Run test "PlayerDeathTest"` instead of `Verify: Check if player can die`).
4.  **No Risk Register**: Do not include a risk register; instead, build mitigation steps directly into the task list (e.g., "Add null checks for X").
5.  **No Time Estimates**: Do NOT include time-based projections, duration markers, or scheduling information in any part of the plan. Focus exclusively on execution and technical requirements.
6.  **Dependency Integrity**: Never write a task whose `depends_on` references a task that does not exist in the plan. Phantom dependencies are a plan error and must be corrected before saving.
7.  **Gap-Free Completeness**: A plan with unresolved questions, undefined edge cases, or ambiguous acceptance criteria is an invalid plan. Gaps must be surfaced to the user and resolved *before* the plan is written, not after.
8.  **Test Procedures Are Not Optional**: Every Stage that introduces observable behavior must have a `🧪 Stage N Test Procedures` block. Omitting it when behavior exists is a plan error.

## 4. When to Use
- Implementing new game features or mechanics.
- Refactoring existing systems.
- Architectural pivots or system integrations.
- Large-scale documentation updates or GDD expansions.

## 5. Output Location
**MANDATORY**: Save all generated plans to `Documentation/Plans/`. Name files using a descriptive slug (e.g., `combat-overhaul.md`).