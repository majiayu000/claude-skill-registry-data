---
name: sadd:do-and-judge
description: Execute a task with sub-agent implementation and LLM-as-a-judge verification with automatic retry loop
argument-hint: Task description (e.g., "Refactor the UserService class to use dependency injection")
---

# do-and-judge

## Task
Execute a single task by dispatching an implementation sub-agent, verifying with an independent judge, and iterating with feedback until passing or max retries exceeded.

## Context
This command implements a **single-task execution pattern** with **meta-judge → LLM-as-a-judge verification**. You (the orchestrator) dispatch a meta-judge (to generate evaluation criteria) and an implementation agent **in parallel**, then dispatch a judge with the meta-judge's evaluation specification to verify quality. If verification fails, you launch new implementation agent with judge feedback and iterate until passing (score ≥4) or max retries (2) exceeded.

Key benefits:

- **Fresh context** - Implementation agent works with clean context window
- **Structured evaluation** - Meta-judge produces tailored rubrics and checklists before judging
- **External verification** - Judge applies meta-judge specification mechanically — catches blind spots self-critique misses
- **Parallel speed** - Meta-judge and implementation run simultaneously
- **Feedback loop** - Retry with specific issues identified by judge
- **Quality gate** - Work doesn't ship until it meets threshold

**CRITICAL:** You are the orchestrator only - you MUST NOT perform the task yourself. IF you read, write or run bash tools you failed task imidiatly. It is single most critical criteria for you. If you used anyting except sub-agents you will be killed immediatly!!!! Your role is to:

1. Analyze the task and select optimal model
2. Dispatch meta-judge AND implementation agent **in parallel as foreground agents** (meta-judge first in dispatch order)
3. Dispatch judge agent with meta-judge's evaluation specification
4. Parse verdict and iterate if needed (max 2 retries)
5. Report final results or escalate

## RED FLAGS - Never Do These

**NEVER:**

- Read implementation files to understand code details (let sub-agents do this)
- Write code or make changes to source files directly
- Skip judge verification to "save time"
- Read judge reports in full (only parse structured headers)
- Proceed after max retries without user decision

**ALWAYS:**

- Use Task tool to dispatch sub-agents for ALL implementation work
- Dispatch meta-judge and implementation agent in parallel (meta-judge FIRST in dispatch order)
- Wait for BOTH meta-judge and implementation to complete before dispatching judge
- Pass meta-judge evaluation specification to the judge agent
- Include `CLAUDE_PLUGIN_ROOT=`${CLAUDE_PLUGIN_ROOT}`` in prompts to meta-judge and judge agents
- Parse only VERDICT/SCORE/ISSUES from judge output
- Iterate with feedback if verification fails

## Process

### Phase 1: Task Analysis and Model Selection

Analyze the task to select the optimal model:

```
Let me analyze this task to determine the optimal configuration:

1. **Complexity Assessment**
   - High: Architecture decisions, novel problem-solving, critical logic
   - Medium: Standard patterns, moderate refactoring, API updates
   - Low: Simple transformations, straightforward updates

2. **Risk Assessment**
   - High: Breaking changes, security-sensitive, data integrity
   - Medium: Internal changes, reversible modifications
   - Low: Non-critical utilities, isolated changes

3. **Scope Assessment**
   - Large: Multiple files, complex interactions
   - Medium: Single component, focused changes
   - Small: Minor modifications, single file
```

**Model Selection Guide:**

| Model | When to Use | Examples |
|-------|-------------|----------|
| `opus` | **Default/standard choice**. Safe for any task. Use when correctness matters, decisions are nuanced, or you're unsure. | Most implementation, code writing, business logic, architectural decisions |
| `sonnet` | Task is **not complex but high volume** - many similar steps, large context to process, repetitive work. | Bulk file updates, processing many similar items, large refactoring with clear patterns |
| `haiku` | **Trivial operations only**. Simple, mechanical tasks with no decision-making. | Directory creation, file deletion, simple config edits, file copying/moving |

**Specialized Agents:** Common agents from the `sdd` plugin include: `sdd:developer`, `sdd:researcher`, `sdd:software-architect`, `sdd:tech-lead`, `sdd:qa-engineer`. If the appropriate specialized agent is not available, fallback to a general agent without specialization. You MUST use general-purpose every time, when there no direct coralation between task and specialized agent, or agent is not available!

### Phase 2: Dispatch Meta-Judge and Implementation Agent (IN PARALLEL)

**CRITICAL**: Launch BOTH agents in a single message using two Task tool calls. The meta-judge MUST be the first tool call in the message so it can observe artifacts before the implementation agent modifies them.

Both agents run as **foreground** agents. Wait for both to complete before proceeding to Phase 3.

#### 2.1 Meta-Judge Prompt

The meta-judge generates an evaluation specification (rubrics, checklist, scoring criteria) tailored to this specific task. It will return to you the evaluation specification YAML.

```markdown
## Task

Generate an evaluation specification yaml for the following task. You will produce rubrics, checklists, and scoring criteria that a judge agent will use to evaluate the implementation artifact.

CLAUDE_PLUGIN_ROOT=`${CLAUDE_PLUGIN_ROOT}`

## User Prompt
{Original task description from user}

## Context
{Any relevant codebase context, file paths, constraints}

## Artifact Type
{code | documentation | configuration | etc.}

## Instructions
Return only the final evaluation specification YAML in your response.
```

```
Use Task tool:
  - description: "Meta-judge: {brief task summary}"
  - prompt: {meta-judge prompt}
  - model: opus
  - subagent_type: "sadd:meta-judge"
```

#### 2.2 Implementation Agent Prompt

Construct the implementation prompt with these mandatory components:

**Zero-shot Chain-of-Thought Prefix (REQUIRED - MUST BE FIRST)**

```markdown
## Reasoning Approach

Before taking any action, think through this task systematically.

Let's approach this step by step:

1. "Let me understand what this task requires..."
   - What is the specific objective?
   - What constraints exist?
   - What is the expected outcome?

2. "Let me explore the relevant code..."
   - What files are involved?
   - What patterns exist in the codebase?
   - What dependencies need consideration?

3. "Let me plan my approach..."
   - What specific modifications are needed?
   - What order should I make them?
   - What could go wrong?

4. "Let me verify my approach before implementing..."
   - Does my plan achieve the objective?
   - Am I following existing patterns?
   - Is there a simpler way?

Work through each step explicitly before implementing.
```

**Task Body**

```markdown
## Task
{Task description from user}

## Constraints
- Follow existing code patterns and conventions
- Make minimal changes to achieve the objective
- Do not introduce new dependencies without justification
- Ensure changes are testable

## Output
Provide your implementation along with a "Summary" section containing:
- Files modified (full paths)
- Key changes (3-5 bullet points)
- Any decisions made and rationale
- Potential concerns or follow-up needed
```

**Self-Critique Suffix (REQUIRED - MUST BE LAST)**

```markdown
## Self-Critique Verification (MANDATORY)

Before completing, verify your work. Do not submit unverified changes.

### Verification Questions

| # | Question | Evidence Required |
|---|----------|-------------------|
| 1 | Does my solution address ALL requirements? | [Specific evidence] |
| 2 | Did I follow existing code patterns? | [Pattern examples] |
| 3 | Are there any edge cases I missed? | [Edge case analysis] |
| 4 | Is my solution the simplest approach? | [Alternatives considered] |
| 5 | Would this pass code review? | [Quality check] |

### Answer Each Question with Evidence

Examine your solution and provide specific evidence for each question.

### Revise If Needed

If ANY verification question reveals a gap:
1. **FIX** - Address the specific gap identified
2. **RE-VERIFY** - Confirm the fix resolves the issue
3. **UPDATE** - Update the Summary section

CRITICAL: Do not submit until ALL verification questions have satisfactory answers.
```

**Dispatch**

Determine the optimal agent type based on the task and avaiable agents, for exmple: code implementation -> `sdd:developer` agent. If you not sure, better use `general-purpose` agent, than dispatch incorrect agent type.

```
Use Task tool:
  - description: "Implement: {brief task summary}"
  - prompt: {constructed prompt with CoT + task + self-critique}
  - model: {selected model}
  - subagent_type: "{selected agent type}"
```

#### 2.3 Parallel Dispatch Example

Send BOTH Task tool calls in a single message. Meta-judge first, implementation second:

```
Message with 2 tool calls:
  Tool call 1 (meta-judge):
    - description: "Meta-judge: {brief task summary}"
    - model: opus
    - subagent_type: "sadd:meta-judge"

  Tool call 2 (implementation):
    - description: "Implement: {brief task summary}"
    - model: {selected model}
    - subagent_type: "{selected agent type}"
```

Wait for BOTH to return before proceeding to Phase 3.

### Phase 3: Dispatch Judge Agent

After BOTH meta-judge and implementation complete, dispatch the judge agent.

CRITICAL: Provide to the judge EXACT meta-judge's evaluation specification YAML, do not skip or add anything, do not modify it in any way, do not shorten or sumaraize any text in it!

**Extract from meta-judge output:**
- The final evaluation specification YAML

**Extract from implementation output:**
- Summary section (files modified, key changes)
- Paths to files modified

**Judge prompt template:**

```markdown
You are evaluating an implementation artifact against an evaluation specification produced by the meta judge.

CLAUDE_PLUGIN_ROOT=`${CLAUDE_PLUGIN_ROOT}`

## User Prompt
{Original task description from user}

## Evaluation Specification

```yaml
{meta-judge's evaluation specification YAML}
```

## Implementation Output
{Summary section from implementation agent}
{Paths to files modified}

## Instructions

Follow your full judge process as defined in your agent instructions!

## Output

CRITICAL: You must reply with this exact structured evaluation report format in YAML at the START of your response!
```

CRITICAL: NEVER provide score threshold, in any format, including `threshold_pass` or anything different. Judge MUST not know what thershold for score is, in order to not be biased!!!

**Dispatch:**

```
Use Task tool:
  - description: "Judge: {brief task summary}"
  - prompt: {judge verification prompt with exact meta-judge specification YAML}
  - model: opus
  - subagent_type: "sadd:judge"
```
```

### Phase 4: Parse Verdict and Iterate

Parse judge output (DO NOT read full report):

```
Extract from judge reply:
- VERDICT: PASS or FAIL
- SCORE: X.X/5.0
- ISSUES: List of problems (if any)
- IMPROVEMENTS: List of suggestions (if any)
```

**Decision logic:**

```
If score ≥4:
  → VERDICT: PASS
  → Report success with summary
  → Include IMPROVEMENTS as optional enhancements

IF score ≥ 3.0 and all found issues are low priority, then:
  → VERDICT: PASS
  → Report success with summary
  → Include IMPROVEMENTS as optional enhancements

If score <4:
  → VERDICT: FAIL
  → Check retry count

  If retries < 3:
    → Dispatch retry implementation agent with judge feedback
    → Return to Phase 3 (judge verification with same meta-judge specification)

  If retries ≥ 3:
    → Escalate to user (see Error Handling)
    → Do NOT proceed without user decision
```

### Phase 5: Retry with Feedback (If Needed)

**Retry prompt template:**

```markdown
## Retry Required

Your previous implementation did not pass judge verification.

## Original Task
{Original task description}

## Judge Feedback
VERDICT: FAIL
SCORE: {score}/5.0
ISSUES:
{list of issues from judge}

## Your Previous Changes
{files modified in previous attempt}

## Instructions
Let's fix the identified issues step by step.

1. Review each issue the judge identified
2. For each issue, determine the root cause
3. Plan the fix for each issue
4. Implement ALL fixes
5. Verify your fixes address each issue
6. Provide updated Summary section

CRITICAL: Focus on fixing the specific issues identified. Do not rewrite everything.
```

### Phase 6: Final Report

After task passes verification:

```markdown
## Execution Summary

**Task:** {original task description}
**Result:** ✅ PASS

### Verification
| Attempt | Score | Status |
|---------|-------|--------|
| 1 | {X.X}/5.0 | {PASS/FAIL} |
| 2 | {X.X}/5.0 | {PASS/FAIL} | (if retry occurred)

### Files Modified
- {file1}: {what changed}
- {file2}: {what changed}

### Key Changes
- {change 1}
- {change 2}

### Suggested Improvements (Optional)
{IMPROVEMENTS from judge, if any}
```

## Error Handling

### If Max Retries Exceeded

When task fails verification twice:

1. **STOP** - Do not proceed
2. **Report** - Provide failure analysis:
   - Original task requirements
   - All judge verdicts and scores
   - Persistent issues across retries
3. **Escalate** - Present options to user:
   - Provide additional context/guidance for retry
   - Modify task requirements
   - Abort task
4. **Wait** - Do NOT proceed without user decision

**Escalation Report Format:**

```markdown
## Task Failed Verification (Max Retries Exceeded)

### Task Requirements
{original task description}

### Verification History
| Attempt | Score | Key Issues |
|---------|-------|------------|
| 1 | {X.X}/5.0 | {issues} |
| 2 | {X.X}/5.0 | {issues} |
| 3 | {X.X}/5.0 | {issues} |

### Persistent Issues
{Issues that appeared in multiple attempts}

### Options
1. **Provide guidance** - Give additional context for another retry
2. **Modify requirements** - Simplify or clarify task
3. **Abort** - Stop execution

Awaiting your decision...
```

## Examples

### Example 1: Simple Refactoring (Pass on First Try)

**Input:**

```
/do-and-judge Extract the validation logic from UserController into a separate UserValidator class
```

**Execution:**

```
Phase 1: Task Analysis
  → Model: Opus

Phase 2: Parallel Dispatch (single message, 2 tool calls)
  Tool call 1 — Meta-judge (Opus)...
    → Generated evaluation specification YAML
    → 3 rubric dimensions, 6 checklist items
  Tool call 2 — Implementation (sadd:meta-judge + Opus)...
    → Created UserValidator.ts
    → Updated UserController to use validator
    → Summary: 2 files modified, validation extracted

Phase 3: Dispatch Judge (with meta-judge specification)
  Judge (sadd:judge)...
    → VERDICT: PASS, SCORE: 4.2/5.0
    → ISSUES: None
    → IMPROVEMENTS: Add input validation for edge cases

Phase 6: Final Report
  ✅ PASS on attempt 1
  Files: UserValidator.ts (new), UserController.ts (modified)
```

### Example 2: Complex Task (Pass After Retry)

**Input:**

```
/do-and-judge Implement rate limiting middleware with configurable limits per endpoint
```

**Execution:**

```
Phase 1: Task Analysis
  - Complexity: High (new feature, multiple concerns)
  - Risk: High (affects all endpoints)
  - Scope: Medium (single middleware)
  → Model: opus

Phase 2: Parallel Dispatch (Attempt 1)
  Tool call 1 — Meta-judge (Opus)...
    → Generated evaluation specification YAML
    → 4 rubric dimensions, 8 checklist items
  Tool call 2 — Implementation (sadd:meta-judge + Opus + sdd:developer)...
    → Created RateLimiter middleware
    → Added configuration schema

Phase 3: Dispatch Judge (with meta-judge specification)
  Judge (sadd:judge + Opus)...
    → VERDICT: FAIL, SCORE: 3.1/5.0
    → ISSUES:
      - Missing per-endpoint configuration
      - No Redis support for distributed deployments
    → IMPROVEMENTS: Add monitoring hooks

Phase 5: Retry with Feedback
  Implementation (sadd:meta-judge + Opus)...
    → Added endpoint-specific limits
    → Added Redis adapter option

Phase 3: Dispatch Judge (Attempt 2, same meta-judge specification)
  Judge (sadd:judge + Opus)...
    → VERDICT: PASS, SCORE: 4.4/5.0
    → IMPROVEMENTS: Add metrics export

Phase 6: Final Report
  ✅ PASS on attempt 2
  Files: RateLimiter.ts, config/rateLimits.ts, adapters/RedisAdapter.ts
```

### Example 3: Task Requiring Escalation

**Input:**

```
/do-and-judge Migrate the database schema to support multi-tenancy
```

**Execution:**

```
Phase 1: Task Analysis
  - Complexity: High
  - Risk: High (database schema change)
  → Model: opus

Phase 2: Parallel Dispatch
  Meta-judge → evaluation specification YAML
  Implementation → initial migration scaffolding

Attempt 1: FAIL (2.8/5.0) - Missing tenant isolation in queries
Attempt 2: FAIL (3.2/5.0) - Incomplete migration script
Attempt 3: FAIL (3.3/5.0) - Edge cases in existing data migration

ESCALATION:
  Persistent issue: Existing data migration requires business decisions
  about how to handle orphaned records.

  Options presented to user:
  1. Provide guidance on orphan handling
  2. Simplify to new tenants only
  3. Abort

User chose: Option 1 - "Delete orphaned records older than 1 year"

Attempt 4 (with guidance): PASS (4.1/5.0)
```

## Best Practices

### Model Selection

- **When in doubt, use Opus** - Quality matters more than cost for verified work
- **Match complexity** - Don't use Opus for simple transformations
- **Consider risk** - Higher risk = stronger model

### Meta-Judge + Judge Verification

- **Never skip meta-judge** - Tailored evaluation criteria produce better judgments than generic ones
- **Reuse meta-judge spec on retries** - The evaluation specification stays constant across retry attempts; only the implementation changes
- **Parse only headers from judge** - Don't read full reports to avoid context pollution
- **Trust the threshold** - 4/5.0 is the quality gate
- **Include CLAUDE_PLUGIN_ROOT** - Both meta-judge and judge need the resolved plugin root path

### Iteration

- **Focus fixes** - Don't rewrite everything, fix specific issues
- **Pass feedback verbatim** - Let the implementation agent see exact issues
- **Same meta-judge spec** - Do NOT re-run meta-judge on retries; the evaluation criteria don't change
- **Escalate appropriately** - Don't loop forever on fundamental problems

### Context Management

- **Keep it clean** - You orchestrate, sub-agents implement
- **Summarize, don't copy** - Pass summaries, not full file contents
- **Trust sub-agents** - They can read files themselves
- **Meta-judge YAML** - Pass only the meta-judge YAML to the judge, do not add any additional text or comments to it!
