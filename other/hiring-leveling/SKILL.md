---
name: hiring-leveling
description: Apply rubric-based leveling to engineering candidates and IC promotions. Define clear expectations for each level (Junior, Mid, Senior, Staff, Principal) across technical, collaboration, and impact dimensions. Grounded in industry leveling frameworks from LeadDev and common EM practice.
triggers:
  - "level this candidate"
  - "promotion decision"
  - "leveling rubric"
  - "is this a senior engineer"
  - "hiring level"
  - "staff engineer"
  - "career ladder"
audience:
  - manager
---

# Hiring & Leveling

Make consistent, defensible leveling decisions for hiring and promotions using explicit rubrics.

---

## Why Rubrics Matter

Without explicit rubrics:
- Same candidate is leveled differently by different interviewers
- Promotions feel political or arbitrary
- Engineers don't know what "good" looks like at the next level
- Bias creeps in through undefined criteria

---

## The Three Dimensions

Evaluate every engineer across three dimensions. All three matter; the mix shifts by level.

### 1. Technical Scope
*What is the size of the technical problem they can own independently?*

### 2. Collaboration & Influence
*How do they work with others and drive outcomes beyond their own code?*

### 3. Impact & Ownership
*How do they define, prioritize, and deliver work that matters to the business?*

---

## Level Definitions

### Junior Engineer (L3)
| Dimension | Bar |
|---|---|
| Technical | Owns tasks within a defined feature; asks for guidance on unknowns; writes tests with prompting |
| Collaboration | Works within team; learns from code review; doesn't block others |
| Impact | Completes assigned work; meets deadlines with support; grows in scope over time |

**Promotion signal**: Consistently delivers without needing task breakdown from manager.

---

### Mid-Level Engineer (L4)
| Dimension | Bar |
|---|---|
| Technical | Owns features end-to-end; makes sound design choices within the system; identifies edge cases proactively |
| Collaboration | Gives useful code review; unblocks others; communicates status proactively |
| Impact | Defines and completes work; estimates accurately; flags risks early |

**Promotion signal**: Teammates rely on them for technical guidance; starts influencing design of adjacent work.

---

### Senior Engineer (L5)
| Dimension | Bar |
|---|---|
| Technical | Owns a domain or system; makes architectural decisions; leads production readiness |
| Collaboration | Mentors juniors and mids; drives RFC/design doc process; aligns with PM/design |
| Impact | Identifies the right problems to solve; delivers projects with ambiguous requirements; improves team practices |

**Promotion signal**: They make the whole team better, not just their own output. Peers seek their technical opinion before deciding.

---

### Staff Engineer (L6)
| Dimension | Bar |
|---|---|
| Technical | Influences architecture across multiple teams or systems; drives tech strategy decisions |
| Collaboration | Trusted advisor to engineering managers and directors; leads cross-team initiatives |
| Impact | Shapes quarterly/annual technical roadmap; identifies systemic problems and fixes them durably |

**Promotion signal**: Impact is felt outside their immediate team. Other teams change how they work because of their influence.

---

### Principal Engineer (L7+)
| Dimension | Bar |
|---|---|
| Technical | Org-wide technical authority; evaluates make/buy/partner decisions; defines standards |
| Collaboration | Influences executive decisions; builds organizational capability |
| Impact | Responsible for multi-year technical strategy; their decisions affect the whole engineering org |

---

## Interview Calibration Guide

### Mapping Interview Signals to Levels

After each interview, score the candidate on each dimension (1-4):
- **1**: Below bar for this level
- **2**: Meets bar inconsistently
- **3**: Meets bar consistently
- **4**: Above bar for this level

```markdown
## Candidate: [Name]
**Leveling for**: [L4 / L5 / etc.]
**Interviewer**: [Name]
**Interview type**: [System Design / Coding / Behavioral]

| Dimension | Score (1-4) | Evidence |
|---|---|---|
| Technical | | [specific observation] |
| Collaboration | | [specific observation] |
| Impact | | [specific observation] |

**Hire/No Hire**: [decision]
**Confidence**: [High/Med/Low]
**Level if hire**: [L4 / L5 — might be over/under]

**Key evidence**:
- Strongest signal: [what convinced you]
- Concern: [what gave you pause]
```

### Calibration Rules
- Score on *evidence*, not vibes — every score needs a behavioral example
- "They seemed smart" is not a data point; "they caught the off-by-one in the distributed lock design" is
- Leveling bias check: Would you give a different level if this person had a different background? If yes, examine why.

---

## Promotion Template

For an IC promotion decision:

```markdown
## Promotion Recommendation: [Name] — [Current Level] → [Target Level]

**Manager**: [Name]  
**Review period**: [dates]

### Evidence of Operating at Target Level

**Technical**:
- [Specific project/decision demonstrating target-level technical scope]
- [Code quality, design quality, system impact]

**Collaboration**:
- [How they influenced others — reviews, mentoring, RFCs, cross-team work]

**Impact**:
- [Business/product impact of their work — not effort, outcome]

### Sustained Performance
[Evidence this isn't a one-time peak — consistency over time]

### Peer Feedback Summary
[Themes from peer reviews — what do colleagues consistently say?]

### Growth Areas at New Level
[What do they need to work on as they grow into the new level?]

### Decision
[ ] Promote now  
[ ] Promote next cycle — [what needs to happen first]  
[ ] Not yet — [specific gaps to address]
```

---

## Common Leveling Mistakes

| Mistake | Fix |
|---|---|
| Promoting on tenure, not performance | "They've been here 3 years" is not a leveling criterion |
| Leveling on potential, not demonstrated behavior | "They could do Staff work" — show me evidence they already are |
| Skipping levels to retain | Creates long-term resentment if they later underperform at the higher level |
| No documented evidence | "We all agree they deserve it" — document it anyway, for the engineer's benefit |
| Inflation in strong teams | Senior on your team ≠ Senior by industry standard — calibrate externally |

---

## References
- LeadDev: [Engineering Career Ladders](https://leaddev.com/career-paths-and-progressions)
- Will Larson: *An Elegant Puzzle* — on leveling and career development
- Camille Fournier: *The Manager's Path*
- [progression.fyi](https://progression.fyi) — public engineering ladders for calibration
