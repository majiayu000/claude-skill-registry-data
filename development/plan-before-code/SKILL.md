---
name: plan-before-code
description: Guide exploration and planning phases before implementation using agentic coding best practices. Includes LLM task suitability assessment, token cost.
---

# Plan Before Code

Guide Codex through systematic exploration and planning before implementation. This planning-first workflow significantly improves code quality and reduces iterations.

## When to Use This Skill

Use this skill for:

- Any non-trivial implementation (>30 minutes estimated)
- Features requiring multiple files or components
- Bug fixes that need root cause analysis
- Refactoring existing code
- New features in unfamiliar codebases
- Architecture decisions
- Security-sensitive changes

**Trigger phrases**: "plan before code", "explore first", "don't code yet", "planning phase", "investigation first", "research before implementing", "should I use AI for this", "LLM suitability", "token cost estimate"

## What This Skill Does

Implements a planning-first best practice: **Plan-Then-Execute**.

### Phase 1: Exploration (Gather Context)
- Read relevant files without modifying
- Understand existing architecture and patterns
- Identify dependencies and constraints
- Map affected components

### Phase 2: Planning (Design Before Code)
- Break down the task into steps
- Identify potential challenges
- Consider alternative approaches
- Plan testing strategy
- Get approval before proceeding

### Phase 3: Execution (Implement the Plan)
- Follow the approved plan
- Make small, incremental changes
- Test continuously

## Instructions

### Step 0: Assess LLM Task Suitability

Before planning the implementation, determine whether an LLM-assisted approach is the right fit for the task. Not every task benefits from AI assistance; some tasks are better handled with traditional tooling.

**Suitability Decision Matrix**:

| Factor | LLM-Appropriate | LLM-Unsuitable |
|--------|-----------------|----------------|
| **Precision** | Approximate answers acceptable | Exact math or deterministic output required |
| **Creativity** | Synthesis, generation, summarization | Strict rule-following, lookup tables |
| **Error tolerance** | Minor errors acceptable with review | Zero-error tolerance (financial, medical) |
| **Domain** | General programming, writing, analysis | Proprietary algorithms, real-time systems |
| **Volume** | Batch processing of similar items | Sequential dependencies between items |
| **Knowledge** | Leverages broad training knowledge | Requires proprietary or very recent data |

**Token Cost Estimation** (for batch/pipeline tasks):

```
Total Cost = (items x avg_tokens_per_item x price_per_token) + 20% buffer

Example:
- 50 files x 3,000 tokens each x $0.003/1K tokens (input)
- = 50 x 3 x $0.003 = $0.45 input
- + output tokens + 20% buffer
- ≈ $1.00 total estimate
```

**Pipeline Mental Model** (5 stages for LLM-powered workflows):

```
Acquire → Prepare → Process → Parse → Render
  │          │          │         │        │
  ▼          ▼          ▼         ▼        ▼
Get raw    Format     LLM call  Extract  Generate
data       into       (non-     structured final
           prompts    deterministic) results output
```

Use this model when planning any multi-step task that involves LLM processing. The key insight: isolate the non-deterministic LLM step (Process) from deterministic steps (Acquire, Parse, Render) to make the pipeline debuggable and retryable.

### Step 1: Request Exploration

Use this exact pattern:

```
"I need to [implement feature/fix bug/refactor code].

IMPORTANT: Do NOT write any code yet.

First, please explore and understand:
1. Read [relevant files/directories]
2. Identify existing patterns for [similar functionality]
3. Map out all files that will need changes
4. List any dependencies or constraints
5. Research any unfamiliar concepts

Provide a summary of your findings."
```

### Step 2: Review Exploration Results

Codex will respond with structured findings:

```
I've explored the codebase. Here's what I found:

1. **Current Structure**
   - Description of existing architecture
   - Key files and their purposes

2. **Existing Patterns**
   - How similar functionality is implemented
   - Conventions used

3. **Dependencies**
   - External libraries
   - Internal modules

4. **Constraints**
   - Must work with existing systems
   - Performance requirements
   - Security considerations
```

Review these findings carefully and correct any misunderstandings.

### Step 3: Request Detailed Plan

```
"Based on your exploration, please create a detailed implementation plan.

Include:
1. Approach and architecture decisions
2. Step-by-step implementation sequence
3. Files to create/modify (in order)
4. Testing strategy
5. Potential challenges and mitigations
6. Estimated complexity

Do NOT implement yet - just the plan."
```

### Step 4: Review and Approve Plan

Codex will provide a structured plan:

```
## Implementation Plan

### Approach
[High-level approach description]

### Implementation Steps

**Step 1: [First Task]**
- Files: [list of files]
- Changes: [description]

**Step 2: [Second Task]**
- Files: [list of files]
- Changes: [description]

### Testing Strategy
- Unit tests for [components]
- Integration tests for [workflows]

### Potential Challenges
1. [Challenge]: [Mitigation]
2. [Challenge]: [Mitigation]

### Estimated Complexity
[Low/Medium/High] - [time estimate]
```

Ask questions if anything is unclear:
```
"The plan looks good, but I have questions:
1. Why did you choose approach X over Y?
2. Should we consider Z?"
```

### Step 5: Authorize Implementation

Once satisfied with the plan:

```
"Plan approved. Please proceed with implementation following the steps exactly as outlined."
```

Or request modifications:

```
"Please modify the plan:
- [Change 1]
- [Change 2]

Then proceed with the updated plan."
```

### Step 6: Incremental Implementation

Codex will implement step-by-step:

- Complete one step at a time
- Show progress after each step
- Test incrementally
- Pause if issues arise

### Step 7: Final Verification

```
"Please verify the implementation:
1. Run all tests
2. Check all files modified match the plan
3. Confirm no TODO items left
4. List any deviations from the plan"
```

## Workflow Templates

### Template 1: Feature Addition
```
"I need to add [feature].

Do NOT code yet. First:
1. Explore: [relevant files/areas]
2. Identify: existing patterns
3. Map: affected components
4. Report: findings

Then create detailed plan."
```

### Template 2: Bug Fix
```
"I need to fix [bug description].

Do NOT fix yet. First:
1. Reproduce: the bug
2. Investigate: root cause
3. Analyze: affected areas
4. Report: findings

Then create fix plan with testing strategy."
```

### Template 3: Refactoring
```
"I want to refactor [code area] to [goal].

Do NOT refactor yet. First:
1. Analyze: current implementation
2. Identify: dependencies and usage
3. Research: best practices for [goal]
4. Report: findings

Then create refactoring plan with safety measures."
```

## Common Mistakes to Avoid

### Mistake 1: Skipping Exploration
```
Bad: "Add feature X" -> Codex immediately codes

Good: "Add feature X. First explore, then plan, then code."
```

### Mistake 2: Vague Exploration Request
```
Bad: "Look around and figure it out"

Good: "Explore:
1. Read src/module.js
2. Find similar features
3. Check dependencies
Report findings before planning."
```

### Mistake 3: Approving Incomplete Plans
```
Bad: "Plan: 1. Add code 2. Test" → "Approved"

Good: "Please expand the plan with:
- Exact files to modify
- Step-by-step sequence
- Testing strategy"
```

## Why This Works

**Without Planning**:
- Missed existing patterns
- Incompatible with current architecture
- Missing edge cases
- Multiple iterations needed

**With Planning**:
- Consistent with existing patterns
- Comprehensive implementation
- Edge cases covered
- Done right first time

The planning step takes 5-10 minutes but saves 30-60 minutes of iteration and debugging.

## Quality Checklist

- [ ] Completed exploration phase (no code written yet)
- [ ] Reviewed findings for accuracy
- [ ] Received detailed implementation plan
- [ ] Reviewed and approved (or modified) the plan
- [ ] Authorized implementation to proceed
- [ ] Verified final implementation matches plan
- [ ] All tests passing
- [ ] Documentation updated

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Planning takes too long for a small feature" | The cost of planning a small feature is 15-30 minutes; the cost of rebuilding it after discovering a missed interface constraint or data model conflict is measured in days, and the rebuild introduces regression risk. |
| "The AI will figure out the approach as it codes" | AI code generation without a plan produces locally coherent but globally inconsistent implementations — functions that work in isolation but conflict with existing module boundaries, naming conventions, or data flow assumptions. |
| "We'll discover the edge cases during testing" | Edge cases discovered during testing require code changes, re-review, and re-testing; edge cases discovered during planning require only an updated plan. The earlier the discovery, the cheaper the fix. |
| "The task is straightforward, no exploration needed" | "Straightforward" tasks that touch existing code regularly reveal unexpected constraints: deprecated APIs, circular dependencies, or config assumptions that are only visible through exploration of the actual codebase. |
| "The plan will just become outdated" | A plan that guided implementation is still valuable after the fact as documentation of intent; even a partially outdated plan reduces onboarding time for the next developer who touches the same code. |

## Verification

- [ ] Exploration phase completed: relevant files, functions, and dependencies identified before any code is written
- [ ] Implementation plan documented with specific file paths, function names, and step sequence
- [ ] Plan reviewed and approved before implementation begins (no code written during planning phase)
- [ ] Edge cases and constraints identified in the plan, not discovered during coding
- [ ] Final implementation matches the approved plan (or deviations are documented with rationale)
- [ ] All tests pass after implementation: test suite exits with code 0

## Related Skills

- `test-driven-development` - Plan includes tests-first approach
- `code-quality` - Review plan before implementation
- `context-analysis` - Deep codebase exploration

---

**Version**: 1.1.0
**Last Updated**: February 2026
**Based on**: Codex planning-first implementation practices
**Attribution**: LLM task suitability and pipeline model adapted from [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) (MIT License)


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
