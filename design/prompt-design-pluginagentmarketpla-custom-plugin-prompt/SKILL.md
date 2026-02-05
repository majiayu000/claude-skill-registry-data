---
name: prompt-design
description: Core prompt design patterns and templates for effective LLM communication
sasmp_version: "1.3.0"
bonded_agent: 01-prompt-fundamentals-agent
bond_type: PRIMARY_BOND
---

# Prompt Design Skill

**Bonded to:** `prompt-fundamentals-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:prompt-design")
```

---

## Parameter Schema

```yaml
parameters:
  task_type:
    type: enum
    values: [generation, classification, extraction, transformation, analysis]
    required: true

  output_format:
    type: enum
    values: [text, json, markdown, code, structured]
    default: text

  constraints:
    type: object
    properties:
      max_length: number
      tone: string
      language: string
```

---

## Core Patterns

### 1. ROLE-CONTEXT-TASK-FORMAT (RCTF)

**Best for:** General-purpose prompts

```markdown
You are a [ROLE] with expertise in [DOMAIN].

## Context
[RELEVANT BACKGROUND INFORMATION]

## Task
[SPECIFIC REQUEST WITH CLEAR OBJECTIVE]

## Output Format
[STRUCTURE AND FORMAT REQUIREMENTS]

## Constraints
[LIMITATIONS AND GUARDRAILS]
```

**Example:**
```markdown
You are a senior software architect with expertise in distributed systems.

## Context
We're designing a new microservices architecture for an e-commerce platform
that needs to handle 10,000 concurrent users.

## Task
Design the service boundaries and communication patterns for the checkout flow.

## Output Format
- Service diagram (ASCII)
- API contracts (OpenAPI style)
- Data flow description

## Constraints
- Use event-driven architecture where possible
- Minimize synchronous calls
- Consider eventual consistency
```

### 2. INSTRUCTION-INPUT-OUTPUT (IIO)

**Best for:** Data processing and transformation

```markdown
## Instruction
[WHAT TO DO WITH THE INPUT]

## Input
[DATA TO PROCESS]

## Expected Output
[FORMAT AND STRUCTURE OF RESULT]
```

### 3. PERSONA-SCENARIO-GOAL (PSG)

**Best for:** Creative and roleplay tasks

```markdown
## Persona
[WHO YOU ARE - background, expertise, personality]

## Scenario
[SITUATION AND CONTEXT]

## Goal
[WHAT TO ACHIEVE]
```

### 4. CONSTRAINT-FIRST (CF)

**Best for:** Safety-critical applications

```markdown
## RULES (Must follow absolutely)
1. [CRITICAL CONSTRAINT 1]
2. [CRITICAL CONSTRAINT 2]

## Your Role
[ROLE DEFINITION]

## Task
[WHAT TO DO WITHIN CONSTRAINTS]
```

---

## Pattern Selection Guide

| Scenario | Recommended Pattern | Reason |
|----------|-------------------|--------|
| Code review | RCTF | Needs clear role and format |
| Data extraction | IIO | Focus on input/output |
| Creative writing | PSG | Needs persona and context |
| Secure applications | CF | Safety constraints first |
| API documentation | RCTF | Structured output needed |
| Translation | IIO | Clear input → output |

---

## Anti-Patterns to Avoid

```yaml
anti_patterns:
  vague_instructions:
    bad: "Make it better"
    good: "Improve readability by using shorter sentences (max 20 words)"

  no_output_format:
    bad: "Analyze this code"
    good: "Analyze this code. For each issue found, provide: issue, severity, fix"

  conflicting_instructions:
    bad: "Be concise. Explain everything in detail."
    good: "Be concise but complete - include all critical details"

  missing_context:
    bad: "Fix the bug"
    good: "Fix the null pointer exception in the user authentication module"
```

---

## Validation Checklist

```yaml
validation:
  structure:
    - [ ] Clear role/persona defined
    - [ ] Task objective is specific and measurable
    - [ ] Output format is explicit
    - [ ] Constraints are stated upfront

  clarity:
    - [ ] No ambiguous terms
    - [ ] One instruction per line
    - [ ] Action verbs used
    - [ ] Examples provided if complex

  completeness:
    - [ ] All necessary context included
    - [ ] Edge cases addressed
    - [ ] Error handling specified
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Inconsistent outputs | Vague instructions | Add specific criteria |
| Wrong format | No format spec | Add explicit format section |
| Off-topic responses | Missing constraints | Add scope boundaries |
| Too verbose | No length limits | Add max length constraint |
| Missing details | Incomplete context | Add more background info |

---

## Integration

```yaml
integrates_with:
  - prompt-templates: Provides reusable patterns
  - prompt-evaluation: Tests pattern effectiveness
  - chain-of-thought: Adds reasoning capability

usage_example: |
  # Combine with few-shot for complex tasks
  [RCTF Pattern]
  +
  [2-3 examples]
  +
  [Current input]
```

---

## References

See `references/GUIDE.md` for detailed methodology.
See `assets/config.yaml` for configuration options.
