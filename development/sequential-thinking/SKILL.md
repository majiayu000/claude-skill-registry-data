---
name: sequential-thinking
description: Sequential thinking and structured reasoning process. Use for complex problems, debugging, architectural decisions, or any task requiring careful step-by-step analysis before action.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Sequential Thinking Process

A structured approach to complex problem-solving through deliberate, step-by-step reasoning.

## Core Principles

1. **Think before acting** - Understand the problem fully before proposing solutions
2. **Break down complexity** - Decompose large problems into manageable steps
3. **Verify assumptions** - Test hypotheses with evidence from the codebase
4. **Document reasoning** - Make thought process explicit and traceable
5. **Iterate and revise** - Update understanding as new information emerges

## The Sequential Thinking Framework

### Phase 1: Problem Definition

**What is the actual problem?**
- State the problem in concrete terms
- Identify symptoms vs root causes
- Define success criteria
- List constraints and requirements

```
PROBLEM STATEMENT:
- What: [Specific issue or goal]
- Why: [Impact and importance]
- Constraints: [Limitations to consider]
- Success: [How we know it's solved]
```

### Phase 2: Information Gathering

**What do I need to know?**
- Identify knowledge gaps
- List files to examine
- Define search queries
- Plan investigation order

```
INVESTIGATION PLAN:
1. [ ] Read [file] to understand [aspect]
2. [ ] Search for [pattern] to find [information]
3. [ ] Check [documentation] for [guidance]
4. [ ] Verify [assumption] by [method]
```

### Phase 3: Analysis

**What does the evidence tell me?**
- Examine gathered information
- Identify patterns and relationships
- Form hypotheses
- Consider alternative explanations

```
ANALYSIS:
- Observation: [What I found]
- Interpretation: [What it means]
- Hypothesis: [Possible explanation]
- Evidence for: [Supporting facts]
- Evidence against: [Contradicting facts]
```

### Phase 4: Solution Design

**What are the options?**
- Generate multiple solutions
- Evaluate trade-offs
- Consider edge cases
- Plan implementation steps

```
SOLUTION OPTIONS:
Option A: [Description]
  Pros: [Benefits]
  Cons: [Drawbacks]
  Risk: [Potential issues]

Option B: [Description]
  Pros: [Benefits]
  Cons: [Drawbacks]
  Risk: [Potential issues]

RECOMMENDED: [Choice with rationale]
```

### Phase 5: Implementation

**How do I execute safely?**
- Define clear steps
- Identify checkpoints
- Plan verification at each step
- Consider rollback strategy

```
IMPLEMENTATION PLAN:
1. [ ] Step 1 - [Action]
       Verify: [How to confirm success]
2. [ ] Step 2 - [Action]
       Verify: [How to confirm success]
...
```

### Phase 6: Verification

**Did it work correctly?**
- Test the solution
- Verify success criteria
- Check for side effects
- Document results

```
VERIFICATION:
- Expected: [What should happen]
- Actual: [What happened]
- Conclusion: [Success/Failure/Partial]
- Next steps: [If needed]
```

## Thinking Patterns

### For Debugging

```
SYMPTOM: [What's wrong]

HYPOTHESIS 1: [Possible cause]
  Test: [How to verify]
  Result: [Finding]
  Conclusion: [Confirmed/Rejected]

HYPOTHESIS 2: [Alternative cause]
  Test: [How to verify]
  Result: [Finding]
  Conclusion: [Confirmed/Rejected]

ROOT CAUSE: [Identified cause]
FIX: [Solution approach]
```

### For Feature Implementation

```
FEATURE: [What to build]

REQUIREMENTS:
- Must: [Essential requirements]
- Should: [Important but not critical]
- Could: [Nice to have]

EXISTING CODE:
- [Relevant file/module] - [What it does]
- [Patterns to follow]
- [Constraints from existing code]

DESIGN:
- Data structures: [New types needed]
- Functions: [New functions needed]
- Integration: [How it connects to existing code]

IMPLEMENTATION ORDER:
1. [First thing to implement]
2. [Second thing, depends on first]
...
```

### For Refactoring

```
CURRENT STATE:
- Structure: [How code is organized now]
- Problems: [Why it needs refactoring]
- Dependencies: [What uses this code]

TARGET STATE:
- Structure: [How it should be organized]
- Benefits: [Why this is better]
- Migration: [How to get there safely]

REFACTORING STEPS:
1. [ ] [Safe intermediate step]
       Test: [Verification]
2. [ ] [Next safe step]
       Test: [Verification]
...
```

### For Architecture Decisions

```
DECISION: [What needs to be decided]

CONTEXT:
- Current situation: [Status quo]
- Forces: [Pressures driving change]
- Constraints: [Limitations]

OPTIONS:
A) [First option]
   Pros: ...
   Cons: ...
   
B) [Second option]
   Pros: ...
   Cons: ...

DECISION: [Choice made]
RATIONALE: [Why this choice]
CONSEQUENCES: [What this means going forward]
```

## Anti-Patterns to Avoid

### Premature Action
```
BAD: Jump straight to coding
GOOD: Understand the problem first
```

### Assumption Without Verification
```
BAD: "I think this is how it works"
GOOD: "Let me read the code to verify"
```

### Single Solution Fixation
```
BAD: First idea is the solution
GOOD: Consider multiple approaches
```

### Ignoring Edge Cases
```
BAD: Works for the happy path
GOOD: Consider error cases, boundaries, concurrency
```

### Skipping Verification
```
BAD: It should work now
GOOD: Let me verify it actually works
```

## Applying to Nebula

### For Core Changes
1. Understand the module's responsibility
2. Check all dependents (`cargo tree --invert`)
3. Design change with backward compatibility
4. Implement with tests
5. Verify no breakage across workspace

### For New Features
1. Identify correct crate for the feature
2. Study existing patterns in that crate
3. Design API following project conventions
4. Implement following TDD
5. Document public API

### For Bug Fixes
1. Reproduce the bug
2. Identify root cause (not just symptom)
3. Design fix that addresses root cause
4. Verify fix doesn't break other tests
5. Consider if similar bugs exist elsewhere

## Template Usage

Start complex tasks with:

```
## Sequential Thinking: [Task Name]

### 1. Problem Definition
[Fill in]

### 2. Investigation Plan
[Fill in]

### 3. Analysis
[Fill in after investigation]

### 4. Solution Design
[Fill in after analysis]

### 5. Implementation Plan
[Fill in after design]

### 6. Verification
[Fill in after implementation]
```

This structured approach ensures thorough analysis before action, reducing errors and improving solution quality.
