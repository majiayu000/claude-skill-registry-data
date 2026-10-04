---
name: planrefine
description: Use when the user asks to "refine the plan", "critique the plan", "/ar:planrefine", or "/ar:pr". Critiques an existing plan against the actual code, records a change ledger, and iterates until a full pass finds no new material issue.
aliases: [pr]
argument-hint: [plan file or content]
---

# Refine Existing Plan (/ar:planrefine)

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
5. **All plan changes require before/after blocks** showing exact text being replaced with file:line-range.
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

## 3. MODE: PLAN REFINEMENT (Not Execution)

You are refining an EXISTING plan with deep critique and mandatory code verification. Do NOT execute code changes until plan approved.

### Critical Constraints: Preserve Existing Work

**Prohibited:**
1. Do NOT replace entire plan
2. Do NOT skip sections
3. Do NOT make changes without citing code evidence
4. Do NOT delete essential content
5. Do NOT remove working functionality

**Required:**
1. Critique each section individually
2. Verify code proposals against actual codebase
3. Propose modifications with file:line-range evidence
4. PRESERVE all existing sections unless explicitly asked to remove

### Anti-Deletion Guard (Mandatory)

When editing the plan file:
1. **Read the full file first** using the Read tool before any Edit call
2. **Use only micro-edits** — `old_string` must be ≤ 5 lines maximum
3. **Verify after every Edit:** Read the file again and confirm nothing was deleted
4. **If you need to reorganize:** Write the complete new version in one Write call with all existing content preserved — do not use Edit for large restructuring
5. **Never use Edit to replace large sections** — if old_string > 5 lines, use Write for the full file instead

After any plan file edit, output the verification line:
`[Edit verified: was N lines, now M lines — no content lost]`

### Before/After Block Requirement

Every proposed change to any file MUST include:

```
**BEFORE** (`file.ext:line-start`–`line-end`):
[exact current text from file — no paraphrasing]

**AFTER:**
[exact new text with change applied]

**Justification:** [why this change is needed, with evidence]
```

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

### Step 3: Plan Inventory
List from existing plan:
1. All sections
2. Stated goals
3. Code references
4. Assumptions

### Step 4: Launch Explore Subagents for Verification
Use Task tool to launch parallel Explore subagents (up to 3) to:
1. Verify all code references match actual codebase
2. Find related implementations plan may have missed
3. Check existing patterns and conventions

**CRITICAL - Verify Subagent Findings:**
1. Use Read tool to verify EVERY file reference
2. Confirm code snippets match actual content
3. Do NOT trust unverified claims
4. CITE file:line-range for verified findings
5. Mark unverifiable findings as "[UNVERIFIED]"

### Step 5: Code Verification (MANDATORY)
For EACH code reference in plan:
1. READ the actual file using Read tool
2. VERIFY plan's description matches actual code
3. CHECK if proposals follow existing patterns
4. CITE file:line-range for all findings

**Output Format:**
```
Plan says: "Add validation to processRequest()"
Actual at src/handler.ts:42-58: Function is `handleRequest`, not `processRequest`
Recommendation: Use correct function name, extend existing validation at :44-48
```

### Step 6: Section-by-Section Critique (MINIMUM 3 PASSES — REQUIRED)

For each section, output headers "PASS 1:", "PASS 2:", "PASS 3:", evaluating:
1. **Goal Alignment**: Does it achieve the stated goal?
2. **Code Feasibility**: Did you READ the actual files at cited line ranges?
3. **UX Excellence**: Easy to use correctly, hard to use incorrectly?
4. **Code Excellence**: Meets TDD, DRY, KISS, YAGNI, SOLID per §1.1?

After completing each pass, you MUST output the completion marker (exactly this format):
`[PASS N COMPLETE: found X issues, Y corrections made]`

Only proceed to §7 after outputting a pass marker with 0 issues found (`[PASS 3 COMPLETE: found 0 issues, 0 corrections made]` at the earliest).
If Pass 3 finds issues, run Pass 4 and continue until a pass finds 0 new issues.
Do NOT summarize or skip passes — each pass must produce output.

### Step 7: Launch Plan Subagent for Alternatives
Use Task tool with Plan subagent to evaluate alternative approaches discovered during verification.

### Step 8: Describe Logic Flow
Trace logic flow through the description. Show data/control flow.

### Step 9: Use Actual Quotes
Quote actual code with file:line-range references. No paraphrasing.

### Step 10: Critique Work
Critique overall + line-by-line against ALL best practices (§1.1) and quality standards (§1.3).

### Step 11: Propose Multiple Solutions
Propose ≥3 distinct solutions to each issue. Choose best with compelling justification.

### Step 12: Synthesize Refinements
Rank refinements. Output as tracked changes showing before/after.

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

### Refinement Structure
1. **Summary of Changes**: What is being improved and why
2. **Tracked Changes**: Show before/after for each modification
3. **Code Evidence**: file:line-range references for all claims
4. **Impact Assessment**: What does this change affect?

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
| **Explore** | Verify code references, find missed implementations, check patterns |
| **Plan** | Evaluate alternative approaches, consider tradeoffs |
| **code-reviewer** | Detailed code quality analysis of proposed changes (Claude Code `pr-review-toolkit` plugin, when installed) |
| **code-explorer** | Deep analysis of existing feature implementations (Claude Code `feature-dev` plugin, when installed) |

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
   - **Stage 1**: Inventory existing plan, verify code references
     → Output **AUTORUN_INITIAL_TASKS_COMPLETED** when Stage 1 done
   - **Stage 2**: Section-by-section critique, propose multiple solutions
     → Output **CRITICALLY_EVALUATING_PREVIOUS_WORK_AND_CONTINUING_TASKS_AS_NEEDED** when Stage 2 done
   - **Stage 3**: Final verification, synthesize refinements
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

</acceptance_protocol>
