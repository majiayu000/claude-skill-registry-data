---
name: learning-path-generator
description: Create a structured learning plan for any skill or topic. Use this skill when the user says "learn", "how do I learn", "learning path", "study plan", "teach.
---

# Learning Path Generator

Create a structured, week-by-week learning plan for any skill or topic. No more "I'll figure it out as I go." Get a clear roadmap from beginner to competent with specific resources, milestones, and practice projects.

## Instructions

### Step 1: Understand the Goal

From the user's request, identify:

- **What they want to learn** — Be specific. "Python" is different from "Python for data analysis."
- **Current level** — Complete beginner, some exposure, intermediate looking to level up?
- **Available time** — Hours per week they can dedicate
- **Learning style** — Videos, reading, hands-on projects, courses?
- **Goal** — What does "learned" look like? Get a job? Build a project? Pass an exam? Just understand it?
- **Timeline** — Any deadline?

If the topic is clear, start building. Ask one question max if you need to narrow the scope.

### Step 2: Research the Best Path

Use WebSearch to find:

- The most recommended learning resources for this topic (courses, books, tutorials)
- Common beginner mistakes and plateaus
- The skill tree (what to learn first, what depends on what)
- Real practice projects at different levels

### Step 3: Build the Learning Path

Structure it in phases:

```markdown
# Learning Path: [Skill/Topic]

**Goal:** [What they'll be able to do when finished]
**Time Commitment:** [X hours/week]
**Total Duration:** [X weeks]
**Starting Level:** [Beginner / Intermediate / etc.]

---

## Phase 1: Foundation ([Weeks X-X])

**Goal:** [What you'll know/be able to do after this phase]

### Week [X]: [Topic]
- **Learn:** [Specific concept or module]
- **Resource:** [Specific course, chapter, tutorial, or video with link if possible]
- **Practice:** [Hands-on exercise or mini-project]
- **Milestone:** [How to know you've got it]

### Week [X]: [Topic]
- **Learn:** [Concept]
- **Resource:** [Resource]
- **Practice:** [Exercise]
- **Milestone:** [Checkpoint]

---

## Phase 2: Building Skills ([Weeks X-X])

**Goal:** [What this phase achieves]

[Same weekly structure...]

**Phase Project:** [A real project that uses everything from this phase]

---

## Phase 3: Applied Practice ([Weeks X-X])

**Goal:** [What this phase achieves]

[Same weekly structure...]

**Phase Project:** [A more complex project]

---

## Phase 4: Advanced / Specialization ([Weeks X-X])

[Only include if the user's goal requires it]

---

## Resources Summary

| Resource | Type | Cost | Phase |
|----------|------|------|-------|
| [Resource 1] | [Course/Book/Tutorial] | [Free/$X] | Phase 1 |
| [Resource 2] | [Type] | [Cost] | Phase 2 |

## Common Pitfalls

- [Mistake 1 — what it is and how to avoid it]
- [Mistake 2]
- [Mistake 3]

## How to Know You're Ready

[2-3 concrete indicators that the user has achieved their learning goal. Not vague "you'll feel confident" but specific: "You can build X without looking anything up" or "You can explain Y to someone else."]
```

### Step 4: Writing Rules

- **Be specific with resources.** Not "watch YouTube videos." Instead: "[Course Name] by [Creator] on [Platform]." Verify these exist.
- **Milestones must be testable.** The user should know definitively whether they've hit each checkpoint.
- **Practice projects should be real.** Not "build a to-do app" unless that actually exercises the right skills. Projects should be things the user would actually want to build or use.
- **Pace matters.** Don't cram 40 hours of content into a "1 week" block. Be honest about how long things take.
- **Front-load wins.** The first week should produce a visible result so the user stays motivated.

### Step 5: Save and Deliver

Save as: `Learning Path - [Topic].md`

Offer: "Want me to go deeper on any phase, find alternative resources, or create a daily schedule that fits your calendar?"

## Rules

- Always verify that recommended resources still exist and are current. Don't recommend a 2018 course for a field that changed completely in 2024.
- Free resources first, paid only when they're significantly better.
- Never overestimate pace. Most people overcommit and then quit. Build in buffer weeks.
- Include at least one project per phase. Learning without building is forgetting.
