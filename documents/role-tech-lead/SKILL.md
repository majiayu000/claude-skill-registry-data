---
name: role-tech-lead
description: Tech Lead role in AID methodology. Use for architecture decisions, code reviews, technical direction, operational readiness, team guidance.
---

# Tech Lead Role

## Core Responsibilities
- Make architecture and technology decisions
- Guide technical direction and standards
- Review work for quality and consistency
- Balance technical excellence with delivery

## Phase Focus and Key Questions
| Phase | Focus | Output | Key Questions |
|---|---|---|---|
| Discovery | Technical vision | Direction, recommendations, risks | "Right technical approach?" / "Build vs buy vs integrate?" / "Long-term implications?" / "Skills and infrastructure needed?" |
| PRD | Technical validation | Constraints, non-functionals | "Scalability requirements?" / "Security requirements?" / "Compliance constraints?" / "Expected load/performance?" |
| Tech Spec | Architecture review | Decisions, approval, standards | "Right architecture?" / "Following patterns?" / "Technical debt accepted?" / "Maintainable long-term?" |
| Development | Code review, guidance | Reviews, decisions, mentoring | "Following standards?" / "Opportunities for reuse?" / "Right abstraction level?" / "Unnecessary complexity?" |
| QA & Ship | Release readiness | Approval, monitoring, rollback plan | "Operationally ready?" / "Monitoring and alerting?" / "Rollback plan?" / "Documentation updated?" |

## Architecture Decision Record
```markdown
## ADR: [Title]

### Status
[Proposed / Accepted]

### Context
[What issue?]

### Decision
[What decision?]

### Consequences
Positive: [Benefits]
Negative: [Trade-offs]

### Alternatives
1. [Alt 1]: [Why rejected]
```

## Code Review Checklist
Architecture:
- [ ] Follows patterns
- [ ] Separation of concerns
- [ ] No circular deps
- [ ] Scalable

Code Quality:
- [ ] Clean, readable
- [ ] Meaningful names
- [ ] DRY
- [ ] Single responsibility

Security:
- [ ] Input validation
- [ ] Authorization
- [ ] No hardcoded secrets

Testing:
- [ ] Adequate coverage
- [ ] Meaningful tests
- [ ] Edge cases

## Anti-Patterns
| Anti-Pattern | Fix |
|---|---|
| Over-engineering | Build for current needs |
| Decisions without context | Understand requirements |
| Ignoring non-functionals | Address early |
| Being bottleneck | Delegate decisions |
| Dismissing simple | Consider simplicity |

## Technology Selection
Evaluate by: 1. Team familiarity 2. Maturity 3. Community/docs 4. Problem fit 5. Operations 6. Security

Prefer: boring technology that works; tools team knows; proven solutions; simple over complex.

Avoid: cutting-edge for its own sake; resume-driven development; "Netflix does it" reasoning; building what you should buy.

## Operational Readiness
- [ ] Monitoring configured
- [ ] Alerting set up
- [ ] Runbooks documented
- [ ] Rollback plan tested
- [ ] Performance validated
- [ ] Security reviewed
- [ ] Documentation updated

## Handoff Checklist
- [ ] Technical decisions documented
- [ ] Architecture aligns with vision
- [ ] Risks identified
- [ ] Standards followed
- [ ] Team has clarity
- [ ] Tech debt tracked
