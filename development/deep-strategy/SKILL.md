---
name: deep-strategy
description: Generate comprehensive multi-approach strategies before execution. Extract domain knowledge, create alternative approaches, identify failure modes, and develop risk-aware plans. Use proactively for complex tasks requiring strategic thinking or when multiple approaches might succeed.
allowed-tools: Read, Grep, Glob
---

# Deep Strategy Generation

Apex2's strategy generation phase implemented as a Claude Code skill. Focuses on extracting everything the LLM knows about a problem domain before execution.

## Instructions

When invoked, perform deep strategic analysis focusing on knowledge extraction and strategic planning:

### 1. Domain Knowledge Extraction
Surface all relevant knowledge about the task domain:
- What frameworks, libraries, or tools are commonly used?
- What patterns and best practices apply?
- What are typical approaches for this type of problem?
- What common pitfalls should be avoided?
- What are the key decision points?

### 2. Alternative Approach Generation
Develop 2-3 distinct strategic approaches:
- **Approach A**: Most straightforward, conventional solution
- **Approach B**: More sophisticated, potentially better performance
- **Approach C**: Conservative, minimal change approach
- Each approach should have:
  - Step-by-step execution sequence
  - Required tools/dependencies
  - Expected outcomes
  - Risk assessment

### 3. Failure Mode Analysis
Identify common failure scenarios and remediation strategies:
- Installation/dependency issues
- Configuration problems
- Runtime errors
- Performance bottlenecks
- Security considerations
- Data corruption risks

### 4. Risk Assessment and Mitigation
For each approach, evaluate:
- Implementation risk (complexity, unfamiliar tech)
- Operational risk (system impact, data loss potential)
- Maintenance risk (long-term support, technical debt)
- Success probability and confidence levels

### 5. Validation Strategy Planning
Define how success will be verified:
- Test scenarios and expected results
- Performance benchmarks if relevant
- Security validation steps
- Rollback procedures if things go wrong

### 6. Prerequisites and Dependencies
List everything needed before starting:
- Software versions required
- Configuration files to prepare
- Data sources needed
- Permissions or access requirements
- Environmental setup steps

## Category-Specific Strategic Patterns

### Software Development Tasks
Consider:
- Testing strategy (unit, integration, e2e)
- Code review requirements
- Documentation needs
- Rollback capability
- Performance implications

### Data/ML Tasks
Consider:
- Data validation and quality checks
- Training parameter selection
- Model evaluation metrics
- Resource requirements (CPU/GPU/memory)
- Result interpretability

### System Administration Tasks
Consider:
- Backup requirements before changes
- Service maintenance windows
- Monitoring and alerting setup
- Rollback procedures
- Impact on dependent services

### Security Operations
Consider:
- Principle of least privilege
- Immutable infrastructure practices
- Audit trail requirements
- Emergency access procedures
- Compliance implications

## Strategic Analysis Process

1. Use Grep to search for related patterns in existing codebase
2. Use Read to examine relevant configuration files, documentation
3. Use Glob to discover similar tasks or examples
4. Synthesize findings into comprehensive strategic options
5. Prioritize approaches based on context and constraints

## Output Format

Provide structured strategy output:

```
Domain Analysis:
  - Key patterns: [list]
  - Common tools: [list]
  - Best practices: [list]
  - Critical considerations: [list]

Strategic Approaches:

Approach A: [Brief name]
  Description: [what it does]
  Steps: [numbered list]
  Pros: [advantages]
  Cons: [disadvantages]
  Risk: [level - Low/Medium/High]
  Success Rate: [estimated]

Approach B: [Brief name]
  [same structure]

Failure Mode Prevention:
  - [issue]: [prevention strategy]
  - [issue]: [prevention strategy]

Recommended Strategy:
  Primary: Approach [A/B/C] - [reasoning]
  Backup: Approach [A/B/C] - [reasoning]
  Validation: [how to verify success]
  Rollback: [how to undo if needed]

Prerequisites:
  Required: [list of must-haves]
  Recommended: [list of should-haves]
```

## When to Use

This skill excels when:
- Complex, multi-step problems need solving
- Multiple valid approaches exist
- High-level strategic planning is needed
- Domain expertise needs to be extracted
- Risk assessment is critical
- Best practices should guide the solution

The goal is to think deeply about the problem space before diving into implementation, ensuring the chosen approach is well-considered and positioned for success.
