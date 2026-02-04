---
name: adversarial-review
description: |
  Implements Adversarial Agile Processes (AAP) for document and code review.
  Challenges assumptions, questions decisions, and suggests improvements.
  Use when reviewing PRs, documentation, or architectural decisions.
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Adversarial Agile Review Skill

This skill embodies the Adversarial Agile Processes (AAP) philosophy for rigorous review.

## AAP Principles

1. **Challenge Assumptions**: Don't accept claims at face value
2. **Question Clarity**: Demand specificity over vagueness
3. **Suggest Alternatives**: Propose different approaches
4. **Verify Completeness**: Identify missing edge cases
5. **Maintain Transparency**: Document all reasoning

## Review Framework

### Level 1: Surface Review
- Formatting and structure compliance
- Spelling and grammar
- Naming convention adherence

### Level 2: Content Review
- Technical accuracy
- Logical consistency
- Completeness of coverage

### Level 3: Adversarial Review
- Challenge core assumptions
- Identify potential failure modes
- Question architectural decisions
- Propose stress scenarios

## Review Questions

### For Documentation
- Is this clear to someone new to the project?
- What questions might a reader still have?
- Are there unstated assumptions?
- Could this be misinterpreted?

### For Code/Architecture
- What happens under extreme load?
- How does this handle failures?
- Are there security implications?
- What's the maintenance burden?

### For Decisions
- What alternatives were considered?
- What are the trade-offs?
- How will we know if this succeeds?
- What's the rollback plan?

## Output Format

```markdown
## Adversarial Review: [Subject]

### Summary
[Brief overview of findings]

### Challenges Raised
1. **[Challenge]**: [Explanation]
   - Risk: [Potential impact]
   - Recommendation: [Suggestion]

### Questions Requiring Answers
- [Question 1]
- [Question 2]

### Suggested Improvements
1. [Improvement with rationale]

### Strengths Noted
- [Positive observations]

### Verdict
[Ready for next state / Needs revision / Major concerns]
```

## Integration with APS

AAP reviews support document state transitions:
- Draft → Provisional: Basic AAP review
- Provisional → In Review: Full AAP assessment
- In Review → Accepted: Final adversarial challenge
