---
name: plannew
description: Use when the user asks to "make a plan", "plan this out", "/ar:plannew", or "/ar:pn", or starts multi-step work that needs tracked steps. Creates a structured plan with checkbox steps, the evidence each step must produce, and the wait process between them.
aliases: [pn]
argument-hint: "[feature or project description]"
---

# Create New Plan (/ar:plannew)

<purpose>

The user's request is the task description for everything below.

## Harness-specific plan lifecycle

- **Claude Code:** Use `EnterPlanMode` and `ExitPlanMode` where this skill instructs; `ExitPlanMode` is the approval boundary.
- **Pi:** Do not call `EnterPlanMode` or `ExitPlanMode` on Pi because Pi exposes neither tool. Write or refine the durable plan note directly, report its exact path for approval, and after approval start execution with `/ar pp <path>`.
- **Native task tracking is conditional:** Before following any task-operation instruction below, use only a mutation tool that the current session actually exposes. Claude uses `TaskCreate`/`TaskUpdate`; Pi and Prime use those tools only when the autorun extension registered them; Codex uses the flat `update_plan` checklist only when exposed (`update_plan` is unavailable in Codex Plan mode). If no native task mutation tool is available, keep progress in the durable Markdown checklist, do not call or retry an unavailable task tool, and report that native task state was not updated. Every unqualified `TaskCreate`, `TaskUpdate`, dependency, and `TaskList` instruction below is conditional on those capabilities.
- **Other harnesses:** Use a native plan-mode boundary and native task tracking only when those tools actually exist; otherwise use the same durable-note approval and checklist workflow as Pi with that harness's documented autorun command spelling.

</purpose>

---

<requirements>

## CRITICAL RULES — SURVIVE COMPACTION

If this session was compacted, these rules STILL apply without exception:

1. **On Claude Code, call ExitPlanMode when ALL planning tasks are complete** — this is Claude Code’s approval boundary. On Pi, report the durable plan note path and wait for explicit user approval.
2. **When TaskCreate is exposed, ALL plan steps require TaskCreate.** If another native checklist mutation tool is exposed, track every step with that tool instead. Otherwise, use the durable Markdown checklist as required by the capability rule above.
3. **ALL user instructions must be directly quoted as a numbered list** at the top of the plan file. Every distinct message, with sub-items for context if needed.
4. **NEVER delete content from plan files.** Only add or make micro-edits. Read before editing. Verify after.
5. **After plan acceptance:** Create [TDD] and [EXEC] tasks for every implementation step before writing any code.
6. **Keep tasks updated:** Before starting any step, `TaskUpdate(status="in_progress")`. When done, `TaskUpdate(status="completed")`.

---

## 1. Foundation (Read First)

### 1.1 Key Principles

| Acronym | Meaning | Question to Ask |
|---------|---------|-----------------|
| TDD | Test-Driven Development | Tests written first? Location specified? |
| DRY | Don't Repeat Yourself | No code duplication? Reusing utilities? |
| OODA | Observe-Orient-Decide-Act | Cycle followed before each decision? |
| KISS | Keep It Simple | Simplest solution that works? |
| YAGNI | You Aren't Gonna Need It | No premature optimization? |
| SOLID | Single responsibility, Open/closed, Liskov, Interface segregation, Dependency inversion | Each principle addressed? |
| RAII | Resource Acquisition Is Initialization | Resources properly managed? |
| WOLOG | Without Loss Of Generality | Solution generalizes appropriately? |

### 1.2 Definition of Concrete

All outputs should include where applicable:

1. **File paths**: `/path/to/file.ts` or `./relative/path.ts`
2. **Line references**: `file.ts:42-56`
3. **Function/class names**: `handleRequest()` in `handler.ts:15-28`
4. **Error messages**: `"socket hang up (ECONNRESET)"`
5. **Testable commands**: `npm test -- --grep "auth"`
6. **Sources and references**: External sources (web URIs, external file URIs, web searches, documentation, research papers) must be recorded with full URIs and cited in plan output

### 1.3 Quality Standards

1. **Sequential improvement**: Each iteration builds on previous insights
2. **Superb quality**: All solutions meet highest standards with thorough justification
3. **Direct quotes**: Show WHY assessments are made, not just WHAT
4. **Verifiable outcomes**: Reasoning transparent and reproducible
5. **Compelling cases**: Selections demonstrate clear superiority

---

## 2. Setup

### 2.1 Plan Mode Check

**Claude Code only:** If not already in plan mode, use `EnterPlanMode` now. **Pi:** remain in the current mode and write the durable plan note directly.

### 2.2 Planning Task Setup — STOP: MUST DO BEFORE ANY PLANNING

> **STOP. Before writing one word of plan content, complete ALL steps below. Do not skip. Do not defer.**

**Step A — Establish the planning boundary:** On Claude Code, call `EnterPlanMode` if needed. On Pi, do not call a plan-mode tool; use the durable plan note.

**Step B — Record ALL user instructions** as a numbered list at the top of the plan file.
Every distinct message must appear with sub-items for context if necessary:
```markdown
## User Messages (exact quotes, in order)

1. "first message the user sent"
   - Context: what prompted this; what was happening at the time
2. "second message — a correction or clarification"
   - Context: what changed from the previous message
```
Include EVERY distinct user message that shaped this plan. Do not summarize or merge messages.

**Step C — Create [PLANNING] tasks** for EVERY step AND substep via TaskCreate:
1. `TaskCreate(subject="[PLANNING] Step N: [name]", activeForm="Planning [name]...")`
2. `TaskCreate(subject="[PLANNING] Step N.M: [substep]", activeForm="Planning [substep]...")`
3. `TaskCreate(subject="[PLANNING] Req: [distinct-requirement]")` for each requirement
4. Wire dependencies: `TaskUpdate(taskId=N, addBlockedBy=[N-1])` for sequential steps

**Step D — Verify:** Call `TaskList` and confirm ALL [PLANNING] tasks visible before continuing.

**Step E — Track Progress**:
- Start each task: `TaskUpdate(taskId, status="in_progress")`
- Finish each task: `TaskUpdate(taskId, status="completed")`

---

## 3. MODE: PLAN CREATION (Not Execution)

You are creating a NEW plan from scratch. No existing plan to reference. Do NOT execute code changes until plan approved.

</requirements>

---

<workflow>

## 4. Process Steps

**PERSISTENT RULE**: After EVERY step AND substep of your plan (both during creation and execution), you must output the exact string "Wait," then execute §5 Wait Process "out loud" step by step and substep by substep.

### Step 1: Identify Expertise Areas
List expertise areas needed. Act as expert. **Output in plan**: State expertise explicitly.

### Step 2: Generate Best Practices
For each expertise area separately, write:
- 10 general best practices
- 10 task-specific best practices

**Output in plan** under "## Best Practices" as numbered list.

### Step 3: Explore Context
Understand existing work. Determine right integration point. Avoid duplication.

### Step 4: Launch Explore Subagents
Use Task tool to launch parallel Explore subagents (up to 3) to understand:
1. Existing implementations and patterns
2. Related components and dependencies
3. Testing patterns and conventions

**CRITICAL - Verify Subagent Findings:**
1. Use Read tool to verify EVERY file reference
2. Confirm code snippets match actual content
3. Do NOT trust unverified claims
4. CITE file:line-range for verified findings
5. Mark unverifiable findings as "[UNVERIFIED]"

### Step 5: Requirements Discovery
1. **Clarify Goal**: What specific outcome does this plan achieve?
2. **Identify Stakeholders**: Who benefits? (users, developers, maintainers)
3. **Define Success Criteria**: How will we know when complete?
4. **Scope Boundaries**: What is IN scope? What is OUT of scope?

### Step 6: Architecture Exploration
Before designing, explore codebase:
1. Use Glob to find related files
2. Read 2-3 similar implementations for reference
3. Identify existing patterns to follow
4. **Concrete Requirement**: Cite specific files (e.g., `src/handler.ts:42-56`)

### Step 7: Launch Plan Subagent
Use Task tool with Plan subagent to design implementation from exploration results.

### Step 8: Plan Structure
Create plan addressing the §1.1 Key Principles checklist:
- [ ] TDD, [ ] DRY, [ ] OODA, [ ] KISS, [ ] YAGNI, [ ] SOLID, [ ] RAII, [ ] WOLOG

### Step 9: Describe Logic Flow
Trace logic flow through the description. Show data/control flow.

### Step 10: Use Actual Quotes
Quote actual code with file:line-range references. No paraphrasing.

### Step 11: Critique Work
Critique overall + line-by-line against ALL best practices (Step 2) and quality standards (§1.3).

### Step 12: Propose Multiple Solutions
Propose ≥3 distinct solutions to each issue. Choose best with compelling justification.

### Step 13: Thread Management
Each thread of updates (different approaches/solutions being refined) needs a unique name with incrementing version number (`<taskname>-v1`, `<taskname>-v2`, ...). This enables referencing specific iterations: "In auth-solution-v2 we tried X, but auth-solution-v3 uses Y".

### Step 14: Final Verification - Completeness Check

1. **Verify ALL cases from the user's request:**
   1. [ ] Primary use case implemented
   2. [ ] ALL edge cases from requirements included
   3. [ ] ALL languages/platforms mentioned covered
   4. [ ] ALL file types/formats specified handled
   5. [ ] ALL user examples addressed
   6. [ ] No requirements silently dropped

2. Check your work. Do not hallucinate.
3. Verify all file references with Read tool
4. Confirm code examples are syntactically correct
5. Ensure no steps skipped (check TaskList)
6. **If ANY case missing**: Return to relevant step. Do NOT proceed incomplete.

---

## 5. Wait Process (Sequential Improvement Methodology)

After outputting "Wait," execute these 8 steps:

1. **Elaborate Best Practices**: Elaborate and refine best practices lists (create new lists if none exist yet) as numbered list for current context; keep refining as new circumstances develop
2. **Comprehensive Critique**: Harshly and constructively critique overall + line-by-line against every single best practice and criteria
3. **Pre-mortem Analysis**: Identify potential failure modes, edge cases, weaknesses. Assume disaster → determine what went wrong → prevent those outcomes
4. **Multiple Solution Generation**: Propose ≥3 superb quality concrete solutions (high-level + specific code quotes) to each identified issue in your task, critiques, and pre-mortem analysis
5. **Synthesized Solution Building**: Synthesize insights from all cumulative context including all previous critiques, the original work (if applicable), all previous proposed solutions, and all accumulated best practices to create refined solutions that incorporate lessons learned from the complete analysis
6. **Sequential Quality Enhancement**: Each proposal must be superb quality, building on benefits of previous iterations
7. **Best Solution Selection**: Choose the optimal solution from all proposals including the original, synthesized, or combinations of all proposals, in ranked order with compelling justification
8. **Error Correction Protocol**: On error: immediately TaskCreate(fix) → TaskUpdate ALL steps from error point onward (failed_step and all subsequent steps) back to "pending" or "in_progress" status → Update dependencies (addBlockedBy) for reset steps to reflect corrected sequence → execute corrective steps → return to the step that produced the error and redo from there

---

## 6. Checkbox Management

1. **Create plan with checkboxes** → Put all in TaskList via TaskCreate
2. **Execute each checkbox** → Execute Wait Process after completion
3. **Check off only when**: Execution complete AND error correction complete
4. **On errors**: Continue until resolved, then check off

</workflow>

---

<output_contract>

## 7. Output Format

### Plan Structure
1. **Summary**: 2-3 sentences (goal + approach)
2. **Checklist**: Concrete items with file:line-range references
3. **Dependencies**: What must be done first?
4. **Risks**: What could go wrong?
5. **Verification**: How to test each step?

### Code Block Format
```language
// File: /path/to/file.ext
// Line: XX-YY (where this code goes)
// Purpose: Brief description

[actual code here - not pseudocode]
```

**Requirement**: Every implementation step needs ≥1 code block showing exact change.

</output_contract>

---

<delegation>

## 8. Subagent Guidelines

| Subagent Type | When to Use |
|---------------|-------------|
| **Explore** | Codebase exploration, finding patterns, understanding implementations |
| **Plan** | Designing approaches, alternatives, architectural decisions |
| **code-architect** | Complex architectural planning (Claude Code `feature-dev` plugin, when installed) |
| **code-explorer** | Deep analysis of existing features (same plugin) |
| **code-reviewer** | Code quality, bugs, security review (Claude Code `pr-review-toolkit` plugin, when installed) |

**Parallel execution**: Launch multiple in single message when tasks are independent.

</delegation>

---

<acceptance_protocol>

## 9. Plan Acceptance and Execution Protocol

When the plan is ready for approval, use the harness-specific boundary above: Claude Code calls **ExitPlanMode**; Pi reports the durable note path and waits for explicit approval before `/ar pp <path>`.

Then transition to execution:

1. **MANDATORY EXECUTION MODE (Goal and Capabilities)**
   1. Your primary objective is to continue the **UNINTERRUPTED, FULLY AUTONOMOUS, NONINTERACTIVE, PATIENT, AND SAFE EXECUTION** of your task and goals.
   2. Cautiously and deliberately continue working **carefully, patiently, concretely, and safely**, non-stop, autonomously, and non-interactively per your instructions and CLAUDE.md philosophy and definition of concrete.
   3. **Permissions Granted:** You have full permission to use all tools (Bash, Edit, Write, etc.) without requiring any further permission prompts.
   4. **Bias Mitigation:** Be cautious, humble, patient, and scrupulous; avoid overconfidence and check your assumptions and your work, explore your environment to ensure you understand the system tasks goals and what is already done, verifying because you are often overconfident, duplicate work, and falsely claim incomplete tasks are "complete" or "production ready".

2. **THREE-STAGE COMPLETION SYSTEM** - Execute all three stages during planning:
   - **Stage 1**: Create initial plan, identify expertise, generate best practices
     → Output **AUTORUN_INITIAL_TASKS_COMPLETED** when Stage 1 done
   - **Stage 2**: Critical evaluation, Wait Process, propose multiple solutions
     → Output **CRITICALLY_EVALUATING_PREVIOUS_WORK_AND_CONTINUING_TASKS_AS_NEEDED** when Stage 2 done
   - **Stage 3**: Final verification, completeness check
     → Output **AUTORUN_ALL_TASKS_COMPLETED_AND_VERIFIED_SUCCESSFULLY** when Stage 3 done
   - **ExitPlanMode**: ONLY allowed after Stage 3 complete

3. **SYSTEM STOP SIGNALS** - NEVER output unless condition met:
   - `AUTORUN_STATE_PRESERVATION_EMERGENCY_STOP` - Emergency stop
   - `AUTORUN_ALL_TASKS_COMPLETED_AND_VERIFIED_SUCCESSFULLY` - Stage 3 done

4. **Safety Protocol**: Execute **ONLY IF** task involves high-risk or irreversible destructive actions (e.g., database operations, file deletion, state modification).
   1. **Assess Risk**: Evaluate if action is irreversible or could cause state corruption.
   2. **Mitigation Action**: If high-risk, execute these steps and explicitly state your actions:
      1. **INITIATE SAFETY PROTOCOL**: Announce 'INITIATE SAFETY PROTOCOL' to begin assessment.
      2. **Secure State**: Create environment backup or state checkpoint **before** proceeding.
      3. **Verify Integrity**: Verify checkpoint succeeded.
      4. **CONSIDER OPTIONS**: List options, evaluate failure modes, select best.
   3. **CRITICAL ESCAPE PRE-CHECK**: If, after mitigation, risk remains irreversible → proceed to step 5.

5. **CRITICAL ESCAPE TO STOP SYSTEM**: Only if irreversible, catastrophic, or cannot be mitigated, immediately output exact string to halt all actions: **AUTORUN_STATE_PRESERVATION_EMERGENCY_STOP**

---

## 10. Post-Acceptance Execution Protocol (Run AFTER User Approves Plan)

Before executing ANY plan step after approval:

1. **Scaffold all tasks.** For each implementation step N in the plan:
   a. `TaskCreate(subject="[TDD] Step N: Write tests for <step description>")`
   b. `TaskCreate(subject="[EXEC] Step N: <step description>")`
   c. `TaskUpdate([EXEC] task, addBlockedBy=[[TDD] task])` — tests must pass before implementation
   d. `TaskUpdate([EXEC] Step N, addBlockedBy=[[EXEC] Step N-1])` — sequential execution

2. **Create final verification task:**
   `TaskCreate(subject="[VERIFY] Run full test suite and confirm all steps complete")`

3. **NEVER start coding** until the full task DAG is created and visible in TaskList.

4. **Task lifecycle during execution:**
   - Before starting each step: `TaskUpdate(taskId, status="in_progress")`
   - When blocked by unexpected work: `TaskCreate(subject="[BLOCKER] description")` immediately
   - When step complete: `TaskUpdate(taskId, status="completed")`, then `TaskList` to find next task
   - Do NOT mark completed unless tests pass and requirements met

5. **Task update frequency:** After every 3 tool calls, check `TaskList` and verify the current task
   is marked `in_progress`. If no task is `in_progress`, mark the correct task before continuing.

</acceptance_protocol>
