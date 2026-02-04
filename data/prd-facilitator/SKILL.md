---
name: prd-facilitator
description: Transform project ideas into requirements documentation focusing on user outcomes and functionality, not implementation. Use when partner describes a new project or feature idea and needs a PRD capturing requirements before implementation, when unclear what to build but not yet ready for technical planning
---

# PRD Facilitator

## Overview

Transform rough project ideas into clear Product Requirements Documents (PRDs) through structured questioning focused on user outcomes and functionality.

**Core principle**: Understand WHAT the project should accomplish and WHY it matters to users, NOT HOW it will be implemented.

**Announce at start**: "I'm using the PRD Facilitator skill to help you document requirements for this project."

## The Process

Copy this checklist to track progress:

```
PRD Facilitator Progress:
- [ ] Phase 1: Understanding User Outcomes (problem, users, success criteria gathered)
- [ ] Phase 2: Expert Routing (domain expert suggested if applicable, or skipped)
- [ ] Phase 3: Document Requirements (PRD created in docs/prd.md)
- [ ] Phase 4: Clean Handoff (stopped cleanly, offered implementation transition)
```

### Phase 1: Understanding User Outcomes

**Focus**: What should this accomplish? Who benefits? What does success look like?

**Question discipline**:
- Ask 1-3 highly related questions, OR
- Ask 1 unrelated question
- Never ask more than 3 questions in one response
- Iterate - you can ask more in the next round

**Redirect implementation talk**:
- If partner mentions tech details → acknowledge, then refocus: "Let's capture what it needs to do first, then we can tackle implementation separately"
- If you're tempted to ask about architecture → Stop. Ask about user needs instead.

**Example questions**:
- "What problem does this solve for users?"
- "What would make this successful in your eyes?"
- "Who will use this and in what context?"

**Anti-pattern questions** (don't ask these in PRD phase):
- "Which framework should we use?"
- "What database are you thinking?"
- "iOS or Android?"

### Phase 2: Consult Domain Experts

When the project falls into a specialized domain, **pause and route to experts**:

**Domains requiring experts**:
- **Game design** → Suggest consulting game-designer agent
- **Software architecture** → Suggest consulting software-architect agent
- **Domain-specific (trading, finance, etc.)** → Suggest consulting relevant expert

**How to suggest**:
"This is a [domain] project. Before I help document requirements, would it be valuable to consult the [expert-type] agent to explore design approaches?"

**Don't**:
- Provide domain expertise yourself when specialized agents exist
- Skip suggesting experts because "it seems simple"

### Phase 3: Document Requirements

**Create PRD with flexible structure adapted to project type**:

**Common sections** (adapt as needed):
- **Purpose**: What problem does this solve?
- **User Outcomes**: What users will be able to do
- **Success Criteria**: How you'll know it works
- **Scope**: What's in/out for this version
- **Open Items**: Unanswered questions, next steps, risks

**Key rule**: Stay at requirements level, not implementation level.

**Good PRD content**:
- "Users can track daily coffee consumption and see weekly patterns"
- "System suggests when caffeine intake exceeds personalized limits"
- "Must work offline with periodic sync"

**Bad PRD content** (too implementation-focused):
- "SQLite database with tables for drinks and patterns"
- "React Native app with Chart.js for visualizations"
- "Redux for state management"

### Phase 4: Clean Handoff

When PRD is complete:

**Stop cleanly**. Say: "PRD complete. This documents what the project should accomplish. Ready to move to implementation planning?"

**Don't**:
- Continue into architecture design unprompted
- Start discussing tech stack
- Begin writing code
- Create implementation plans

**Wait for explicit confirmation** before transitioning to implementation phase.

## Quick Reference

| Phase | Focus | Questions | Output |
|-------|-------|-----------|--------|
| Understanding | User outcomes, success criteria | 1-3 related OR 1 unrelated | Clear problem statement |
| Expert Routing | Suggest domain experts | When applicable | Expert consultation |
| Documentation | What/Why not How | N/A | PRD document |
| Handoff | Stop cleanly | Offer implementation transition | Wait for confirmation |

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Asking about tech stack | Technical details mentioned → attraction to implementation | Acknowledge tech mention, refocus on requirements |
| 7+ questions at once | Want comprehensive understanding upfront | Iterate with 1-3 questions, gather info over multiple rounds |
| Providing domain expertise directly | Feels efficient to help directly | Route to specialized agents when domain is complex |
| Continuing to design after PRD | Natural momentum to keep going | Stop. Ask if they want implementation phase. Wait. |

## Red Flags - You're Doing It Wrong

- Asking "which framework?" or "what database?" in PRD phase
- More than 3 questions in one response
- Providing game design / architecture advice without suggesting expert consultation
- Discussing implementation details before PRD is approved
- Creating technical diagrams or code during PRD phase

**If you catch yourself doing these → Stop. Return to Phase 1.**

## Example

**User**: "I want to build a mobile app for tracking my coffee consumption. It should help me understand my caffeine patterns and maybe suggest when I'm drinking too much. I'm thinking SQLite for local storage and maybe some charts."

**You**: "I'm using the PRD Facilitator skill to help you document requirements for this project.

Let's focus on what you want this app to accomplish first, then we can tackle implementation separately.

Here are my questions:
1. What specific insights about your coffee habits would be most valuable to you?
2. When you say 'drinking too much' - should that be based on general health guidelines, or do you want to set personal limits?"

[After gathering requirements through iteration...]

**You**: "I'll create a PRD document capturing these requirements in docs/prd.md:

**Purpose**: Help you understand caffeine consumption patterns and make informed decisions about intake.

**User Outcomes**:
- Track each coffee/caffeine intake with time, amount, type
- Visualize daily and weekly consumption patterns
- Receive notifications when approaching personal limits
- Export data for health tracking

**Success Criteria**:
- User can log a drink in under 10 seconds
- Pattern visualization shows clear trends over time
- Limit suggestions are based on personal thresholds user sets

**Scope (v1)**:
- IN: Manual drink logging, basic charts, personal limit alerts
- OUT: Automatic detection, social features, health provider integration

**Open Items**:
- Define specific chart types after reviewing mockups
- Determine notification timing strategy
- Consider accessibility requirements

PRD complete. This documents what the project should accomplish. Ready to move to implementation planning?"

## Related Skills

**When PRD leads to implementation**:
- skills/collaboration/brainstorming (for design exploration)
- skills/collaboration/writing-plans (for implementation tasks)
