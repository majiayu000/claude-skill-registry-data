---
name: Codex Delegation Criteria
description: This skill should be used when deciding whether to "delegate to codex", "hand off to codex", "use codex for this", or when Claude needs to determine if a task is appropriate for Codex vs handling directly. Provides decision criteria for task routing between Claude and Codex.
version: 0.1.0
---

# Codex Delegation Criteria

Decision framework for routing tasks between Claude Code and OpenAI's Codex agent.

## Overview

Claude Code and Codex have complementary strengths. Claude excels at interactive, exploratory work requiring judgment. Codex excels at bounded, well-defined tasks that can run asynchronously. Effective delegation maximizes throughput by matching tasks to the right agent.

## Quick Decision Matrix

| Factor | Favor Codex | Favor Claude |
|--------|-------------|--------------|
| **Scope** | Clearly bounded | Open-ended |
| **Urgency** | Can wait 5-30 min | Needed now |
| **Iteration** | One-shot execution | Back-and-forth likely |
| **Complexity** | Junior dev could do it | Requires judgment |
| **Context** | Self-contained | Needs conversation history |
| **Output** | Code/PR | Explanation/discussion |

## When to Delegate to Codex

### Strong Codex Candidates

**QA Tasks**
- Run linters and fix violations
- Add test coverage to existing code
- Code review with specific checklist
- Security audit for known patterns

**Clearly-Scoped Bug Fixes**
- Issue has clear reproduction steps
- Fix location is known or obvious
- Success criteria are testable
- No architectural decisions needed

**Repetitive Multi-File Changes**
- Rename across codebase
- Add consistent error handling
- Update import paths
- Apply pattern to multiple files

**Background Work**
- Tasks that don't block current flow
- Work that can be reviewed later
- Parallel workstreams

### Codex Task Characteristics

- Has a GitHub issue or clear spec
- Can be described in a CTM (Codex Task Manifest)
- Success is objectively verifiable
- Scope fits in a single PR
- No conversation needed during execution

## When to Keep in Claude

### Strong Claude Candidates

**Architecture and Design**
- System design decisions
- API design choices
- Trade-off analysis
- Refactoring strategy

**Exploratory Work**
- Debugging without clear cause
- Investigation and research
- Prototyping approaches
- Understanding unfamiliar code

**Interactive Tasks**
- Work requiring clarification
- Iterative refinement
- Real-time feedback loops
- Teaching and explanation

**Urgent Work**
- Blocking other tasks
- Part of active development flow
- Needs immediate feedback
- Time-sensitive fixes

### Claude Task Characteristics

- Requires judgment or creativity
- Benefits from conversation
- Needs context from current session
- Urgency doesn't allow 5-30 min wait
- Scope is unclear or evolving

## Decision Process

### Step 1: Check Urgency

```
Is this blocking your current work?
├── Yes → Keep in Claude
└── No → Continue to Step 2
```

### Step 2: Check Scope Clarity

```
Can you write a clear CTM with:
- Specific success criteria
- Defined file scope
- Testable outcome
├── Yes → Continue to Step 3
└── No → Keep in Claude
```

### Step 3: Check Iteration Need

```
Will this likely need back-and-forth?
├── Yes → Keep in Claude
└── No → Continue to Step 4
```

### Step 4: Check Complexity

```
Could a competent junior dev do this with clear instructions?
├── Yes → Delegate to Codex
└── No → Keep in Claude
```

## Proactive Delegation Triggers

Claude should suggest Codex delegation when detecting:

### Language Patterns

- "Fix all the lint errors in..."
- "Add tests for..."
- "Review this code for..."
- "Update all files that..."
- "Rename X to Y across..."

### Task Patterns

- Multiple files need same change
- Task matches existing GitHub issue
- Request is well-specified with clear criteria
- Task is independent of current conversation
- User mentions "background" or "later"

### Context Patterns

- User is in a flow working on something else
- Task is tangential to main work
- Output is a PR (not explanation)
- Success is binary (works/doesn't)

## Delegation Workflow

When delegating to Codex:

1. **Confirm with user**: "This looks like a good Codex task. Want me to submit it?"
2. **Generate CTM**: Create Codex Task Manifest from task details
3. **Show CTM for review**: Let user approve or adjust
4. **Submit via `/codex:submit`**: Hand off to Codex
5. **Continue other work**: Don't block on Codex completion
6. **Check later**: Use `/codex:status` to monitor

## Anti-Patterns

### Don't Delegate

- Tasks requiring access to conversation context
- Work that needs Claude's tool access (Codex is sandboxed)
- Anything involving secrets or credentials
- Tasks where you're unsure of the approach
- Work that would be faster to just do

### Don't Keep

- Simple, well-defined tasks just because they're "easy"
- Repetitive work that could run in background
- QA tasks that don't need judgment
- Work blocking you from higher-value tasks

## Examples

### Delegate to Codex

```
User: "Can you add test coverage for the new handler?"
→ Clear scope, QA task, can run async
→ Suggest: "This is a good Codex task. Generate CTM?"
```

```
User: "Fix all the golangci-lint errors"
→ Well-defined, repetitive, objectively complete
→ Suggest: "Perfect for Codex. Submit now?"
```

```
User: "Review the PR for security issues"
→ Checklist-based, bounded scope
→ Suggest: "Codex can handle this review"
```

### Keep in Claude

```
User: "How should we structure the new API?"
→ Architecture decision, needs discussion
→ Handle directly, don't suggest Codex
```

```
User: "Debug why this test is flaky"
→ Investigation needed, unclear scope
→ Handle directly, explore interactively
```

```
User: "I need this fix in the next 5 minutes"
→ Urgent, can't wait for Codex
→ Handle directly, prioritize speed
```

## Integration with Orca

Tasks delegated to Codex often map to:

- **GitHub issues**: Use issue number in CTM
- **Task nugs**: Extract task details from nugget
- **Friction reports**: Codex PRs generate learning

After Codex completes, friction reports can be mined into Orca traps and rules for continuous improvement.
