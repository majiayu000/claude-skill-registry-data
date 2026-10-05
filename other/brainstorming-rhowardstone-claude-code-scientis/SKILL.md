---
name: brainstorming
description: You MUST use this before any creative work - creating features, designing experiments, building components, formulating hypotheses, or modifying behavior. Explores intent, requirements and design before implementation.
user-invocable: true
---

# Brainstorming Protocol

Use this skill BEFORE any creative work to ensure you understand intent and have explored the design space.

## When to Use

**ALWAYS invoke this skill before:**
- Designing experiments
- Formulating hypotheses
- Creating new features or components
- Making architectural decisions
- Starting any non-trivial implementation

## The Process

### 1. Intent Clarification

Before doing anything, answer:
- **What problem are we solving?**
- **Who is the audience/user?**
- **What does success look like?**
- **What are the constraints?**

If any of these are unclear, ASK before proceeding.

### 2. Requirements Gathering

List all requirements:

**Functional requirements:**
- What must this do?
- What inputs does it take?
- What outputs does it produce?

**Non-functional requirements:**
- Performance constraints (time, memory)
- Compatibility requirements
- Quality attributes

**Out of scope:**
- What are we explicitly NOT doing?
- What limitations are acceptable?

### 3. Design Exploration

Explore at least 2-3 approaches:

```markdown
## Approach A: [Name]
- **Pros:** [List advantages]
- **Cons:** [List disadvantages]
- **Complexity:** [Low/Medium/High]
- **Risk:** [What could go wrong]

## Approach B: [Name]
- **Pros:** [...]
- **Cons:** [...]
...
```

### 4. Decision and Rationale

After exploring options:
- **Chosen approach:** Which and why
- **Trade-offs accepted:** What we're giving up
- **Assumptions made:** What we're taking for granted
- **Validation needed:** How we'll know it works

## For Experiment Design

When brainstorming experiments:

1. **Hypothesis clarity**
   - Can you state the hypothesis in one sentence?
   - Is it falsifiable?
   - What would prove it wrong?

2. **Methodology options**
   - What data sources are available?
   - What tools/methods could be used?
   - What are the alternatives?

3. **Controls and baselines**
   - What's the null hypothesis?
   - What's the baseline to compare against?
   - How do we isolate the variable of interest?

4. **Success criteria**
   - What metrics determine success?
   - What thresholds are meaningful?
   - How do we handle negative results?

## For Research Question Formulation

When brainstorming RQs:

1. **Gap identification**
   - What don't we know?
   - Why does it matter?
   - How does this fit the research goal?

2. **Answerability**
   - Can this be answered with available methods?
   - What evidence would answer it?
   - How confident can we be in the answer?

3. **Scope**
   - Is this too broad? Too narrow?
   - Can we answer it in the time available?
   - Does it lead to actionable conclusions?

## Anti-Patterns

**Don't:**
- Jump straight to implementation
- Pick the first idea without exploring alternatives
- Make assumptions without stating them
- Skip the "what could go wrong" analysis
- Proceed with unclear requirements

**Do:**
- Take time to understand the problem
- Explore multiple approaches
- State assumptions explicitly
- Consider failure modes
- Document decisions and rationale

## Output

After brainstorming, document:

```markdown
# Design Decision: [Topic]

## Problem Statement
[Clear description of what we're solving]

## Requirements
[Functional and non-functional requirements]

## Approaches Considered
[At least 2-3 options with pros/cons]

## Chosen Approach
[Which approach and why]

## Trade-offs
[What we're accepting/giving up]

## Next Steps
[Concrete actions to implement]
```

**Think first. Explore options. Then implement.**
