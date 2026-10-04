---
name: problem-mapping
version: 1.0.0
description: Foundational problem framing for design sprints and product strategy. Based on Google Design Sprint "Understand" phase methodology. Use when teams need to establish shared understanding before ideation - defining problem statements, identifying users/stakeholders, setting success criteria, documenting constraints and assumptions, and capturing pain points. Works in solo, team synchronous, or team asynchronous modes. Creates structured problem map document as foundation for HMW exercises and solution generation.
---

# Problem Mapping

Problem Mapping helps teams understand and frame design challenges before jumping to solutions. Based on the "Understand" phase from Google Design Sprint methodology, this skill structures messy problem spaces into clear goals, assumptions, and pain points.

## What This Skill Does

- Facilitates structured problem exploration through guided questioning
- Captures goals, users, constraints, and assumptions systematically
- Documents pain points and challenges
- Creates shared understanding document as sprint foundation
- Does NOT generate solutions or make decisions (that comes later)
- Does NOT interpret findings (humans decide significance)

## Workflow Decision Tree

**Start here:** "I'd like to start a problem mapping session"

Claude will ask: **"How are you running this session?"**

1. **Solo** → Individual exploration with Claude
2. **Team Sync** → Team together, Claude facilitates discussion
3. **Team Async** → Team provides input separately, Claude synthesizes

Each mode follows the same 6-step questioning framework but adapts the interaction style.

## Solo Mode

Use when working through problems independently - initial exploration, personal projects, or prep work.

### How It Works

1. Claude asks structured questions about the problem
2. Think out loud and answer thoughtfully (don't rush)
3. Claude structures responses into problem map
4. Review and refine together

### Question Framework

1. **Problem Statement** - What are we trying to solve?
2. **Users/Stakeholders** - Who's involved? Who's affected?
3. **Goals** - What does success look like?
4. **Constraints** - What's limiting us? (time, resources, technology)
5. **Assumptions** - What are we taking for granted?
6. **Pain Points** - What are the key challenges or frustrations?

### Your Role

- Think out loud, don't self-censor
- Challenge own assumptions
- Ask Claude to dig deeper if stuck
- Don't rush - this is thinking time

## Team Sync Mode

Use when team is together (in-person or video call) - kickoff meetings, workshops, retreat sessions.

### Preparation

- Share problem context with team beforehand
- Reserve 45-60 minutes uninterrupted
- One person operates Claude (facilitator)
- Everyone else focuses on discussion

### How It Works

1. Facilitator reads Claude's prompts to team verbatim
2. Team discusses each question together
3. Facilitator relays key points to Claude
4. Claude documents in real-time and keeps session on track

### Roles

**Facilitator (you):**
- Read Claude's prompts verbatim (phrasing is intentional)
- Give space for discussion, don't rush
- Capture and relay team responses
- Trust Claude to redirect if discussion drifts

**Claude:**
- Provides structured prompts with facilitation tips
- Captures team responses
- Identifies when discussion goes off-track
- Reminds facilitator of next steps

**Team:**
- Discuss openly and challenge assumptions
- Build on each other's ideas
- Stay focused on current question

### Timing

- Problem Statement (10 min)
- Users/Stakeholders (5 min)
- Goals (10 min)
- Constraints (5 min)
- Assumptions (10 min)
- Pain Points (10 min)

Total: ~50 minutes

## Team Async Mode

Use when team is distributed, busy schedules, or when gathering diverse perspectives independently matters.

### Process

**Phase 1: Generate Questions (5 min)**
- Brief Claude on problem
- Claude creates question set
- Review and adjust if needed

**Phase 2: Distribute (You handle)**
- Send questions to team via preferred channel (Slack/email/doc)
- Give clear deadline (24-48 hours typical)
- Encourage honest, individual responses (2-3 sentences per question)
- Team doesn't see each other's answers yet

**Phase 3: Compile (10 min)**
- Copy/paste all team responses to Claude
- Include who said what (names or roles)
- Perfect formatting not required

**Phase 4: Synthesis (Claude does this)**
- Structures all responses
- Identifies common themes
- Highlights divergent perspectives
- Reveals patterns in thinking
- Does NOT interpret what patterns mean

**Phase 5: Review (Team)**
- Share Claude's synthesis with team
- Team discusses what they see
- Humans interpret significance together

### Format Flexibility

Claude asks what format works for your team:
- Markdown document
- Google Doc template
- Slack message format
- Email format
- Other

## Output Document

All modes produce a structured problem map:

```markdown
# Problem Map: [Project Name]

**Date:** [Date]
**Participants:** [Names/Roles]
**Mode:** [Solo/Team Sync/Team Async]

---

## Problem Statement
[Clear, concise description of challenge]

---

## Users & Stakeholders
**Primary Users:**
- [User type]: [Main needs/goals]

**Stakeholders:**
- [Stakeholder]: [Interest/influence]

---

## Success Criteria
What "good" looks like:
1. [Measurable outcome]
2. [Measurable outcome]
3. [Measurable outcome]

---

## Constraints
**Time:** [Limitations]
**Resources:** [Budget, team, tools]
**Technical:** [Platform, integration, legacy]
**Business:** [Policy, compliance, market]

---

## Assumptions
Things we're taking for granted (need validation):
- [Assumption about users]
- [Assumption about solution]
- [Assumption about context]
- [Assumption about feasibility]

---

## Pain Points & Challenges
Key problems and frustrations:
- [User pain point]
- [Business challenge]
- [Technical obstacle]
- [Process friction]

---

## Open Questions
What we need to learn or validate:
- [Research question]
- [Validation needed]
- [Knowledge gap]

---

## Next Steps
[If team decided on immediate actions]
```

### Team Async Addendum

Async mode adds individual perspectives section:

```markdown
---

## Individual Perspectives

**On [Topic]:**
- [Person A]: [Their view]
- [Person B]: [Their view]
- [Person C]: [Their view]

**Patterns Observed:**
- [Common theme]
- [Area of alignment]
- [Area of divergent thinking]

**Note:** Shows what team said, not what it means. 
Team discusses significance together.
```

## Common Pitfalls

Claude catches these automatically:

❌ **Jumping to solutions** - "We should build X"
✅ **Staying in problem space** - "Users struggle with Y because Z"

❌ **Vague goals** - "Make it better"  
✅ **Specific criteria** - "Reduce task time from 5 min to 2 min"

❌ **Hidden assumptions** - Treating beliefs as facts
✅ **Named assumptions** - "We assume users have smartphones (needs validation)"

❌ **Problem statements that are actually solutions** - "We need a mobile app"
✅ **Clear problem statements** - "Users can't access information when away from desktop"

## Best Practices

### All Modes
- Don't rush - this is thinking time, not execution
- Challenge assumptions actively
- Stay focused - one question at a time, resist solution talk
- Verify accuracy of documentation

### Solo Mode
- Think out loud - more material = better structure
- Use "I don't know" - Claude helps figure it out
- Revisit earlier answers when new insights emerge

### Team Sync Mode
- Read prompts verbatim - Claude's phrasing is intentional
- Embrace silence - let team think before answering
- Capture spirit, not transcript - main points matter
- Watch for energy - if stuck, tell Claude and ask for help

### Team Async Mode
- Give clear deadline - respects team's time
- Encourage brevity - 2-3 sentences sufficient
- Don't prime responses - let team think independently
- Share synthesis before discussing - let it sit if possible

## What Happens Next

After Problem Mapping:

1. **Lightning Talks** - Experts share knowledge about users, business, tech (use `hmw-affinity` skill during talks)
2. **Prioritize** - Which problems are most important?
3. **Research** - Which assumptions need validation first?
4. **Ideate** - Generate solutions (use `crazy-8s` skill)

Problem Mapping creates the foundation. Everything else builds on this shared understanding.

**Note:** In Google Design Sprints, Problem Mapping is part of the "Understand" phase. After this foundational work, teams conduct Lightning Talks where experts present insights. During talks, team members capture "How Might We" (HMW) opportunities - that's a separate skill (`hmw-affinity`).
