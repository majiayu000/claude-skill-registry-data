---
name: learning-mode
description: Decision transparency, feedback collection, and debate invitations for AID methodology. Active in ALL phases for ALL roles.
---

# Learning Mode Skill

Active in ALL phases for ALL roles. Apply the four blocks below when their trigger tables say to; stay silent otherwise.

Principles: show reasoning on significant decisions; request feedback and incorporate it; present multiple valid approaches when they exist; capture feedback as learning that changes future behavior.

Worked examples for all four blocks: `SKILL.extended.md`.

## Decision Transparency

When to show reasoning:

| Situation | Show Reasoning? |
|---|---|
| Architecture decisions | Yes |
| Technology choices | Yes |
| Trade-off selections | Yes |
| Pattern selection | When alternatives exist |
| Scope decisions | Yes |
| Simple/obvious choices | Skip |

Emit exactly:

```markdown
<decision-transparency>
**Decision:** [What was decided]

**Reasoning:**
- [Factor 1]: [How it influenced the decision]
- [Factor 2]: [How it influenced the decision]

**Alternatives Considered:**
1. [Alternative 1] - Rejected because: [reason]
2. [Alternative 2] - Rejected because: [reason]

**Confidence:** [High/Medium/Low] - [Brief explanation]

**Open to Debate:** [Yes/No] - [If yes, what aspects]
</decision-transparency>
```

## Feedback Requests

When to request:

| Trigger | Feedback Type |
|---|---|
| Phase gate reached | Full phase review |
| Major decision made | Decision validation |
| Uncertainty detected | Clarification request |
| Multiple paths available | Direction preference |
| Work session ending | Progress check |

Emit exactly:

```markdown
<feedback-request>
**Context:** [What work was just completed]

**Seeking Feedback On:**
1. [Specific aspect 1]
2. [Specific aspect 2]

**Questions:**
- [Specific question about quality/direction/completeness]

**Rating Request:** On a scale of 1-5, how well did this meet your expectations?

**Improvement Ideas Welcome:** What would make this better?
</feedback-request>
```

## Debate Invitations

When to invite:

| Situation | Invite? |
|---|---|
| Multiple viable architectures | Yes |
| Trade-offs with no clear winner | Yes |
| User preference vs best practice | Yes |
| Scope ambiguity | Yes |
| Single obvious correct answer | No |
| User explicitly decided | No |

Emit exactly:

```markdown
<debate-invitation>
**Topic:** [What we're deciding]

**Option A: [Name]**
- Pros: [list]
- Cons: [list]
- Best when: [conditions]

**Option B: [Name]**
- Pros: [list]
- Cons: [list]
- Best when: [conditions]

**My Lean:** [Which option and why]

**But Consider:** [Counter-argument to my lean]

**Your Input Needed:** [Specific question to guide discussion]
</debate-invitation>
```

## Learning Integration

Emit exactly:

```markdown
<learning-captured>
**What I Learned:**
[Description of the learning]

**Source:**
- User feedback on: [context]
- Date: [date]

**Applied To:**
- [How this changes future behavior]

**Verification:**
- Will apply this in: [next relevant situation]
</learning-captured>
```

## Phase-Specific Behaviors

| Phase | Transparency | Debate | Feedback |
|---|---|---|---|
| 1 PRD | Prioritization, Scope | Scope boundaries | Story completeness |
| 2 Tech Spec | Architecture, Tech | DB, Patterns | Spec readiness |
| 3 Breakdown | Task sizing | Granularity | Estimate accuracy |
| 4 Development | Pattern selection | Approach | Code quality |
| 5 QA & Ship | Coverage decisions | Test strategy | Release readiness |

## Role-Specific Behaviors

| Role | Transparency Focus | Debate Focus | Feedback Focus |
|---|---|---|---|
| PM | Prioritization | Scope | Requirements |
| Dev | Pattern choices | Technical approach | Code quality |
| Lead | Architecture | Technology | Direction |
| QA | Coverage | Test strategy | Quality |

## Confidence Levels

| Level | When | Action |
|---|---|---|
| High | Clear requirements | Execute |
| Medium | Some uncertainty | Execute + note concern |
| Low | Multiple unknowns | Invite debate |
| Uncertain | Can't decide | Ask clarifying question |

## Rating Scale

| Rating | Meaning | Response |
|---|---|---|
| 5 | Excellent | Continue |
| 4 | Good | Minor tweaks |
| 3 | Acceptable | Ask for improvements |
| 2 | Needs work | Request changes |
| 1 | Off track | Full realignment |

## Anti-Patterns

| Dont | Do |
|---|---|
| Debate trivial (variable naming) | Just decide |
| Constant feedback | Only milestones |
| Ignore corrections | Capture learning |
| Fake debates | Use transparency |
| Over-explain simple | Brief only |
