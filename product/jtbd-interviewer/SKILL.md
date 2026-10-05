---
name: jtbd-interviewer
type: conversational
description: "Conduct Jobs-to-be-Done interviews — switch triggers, hiring criteria, outcome expectations."
version: 0.1.0
---

# JTBD Interviewer Skill

## When to Use

**Primary triggers:**
- "JTBD interview", "jobs-to-be-done interview", "interview about switching"
- "why did they switch", "why did customers switch", "why did someone switch"
- "understand why people use", "discovery interview"
- "purchase story", "switching story", "timeline interview"
- "why did someone hire", "customer switching story"
- "user research", "qualitative product discovery"

---

## Use When

- Conducting qualitative product discovery before building or pivoting a product or feature
- Understanding why customers switched from a competitor or prior solution
- Running user research before Ulwick-style quantitative outcome prioritization
- Documenting the first 3–5 customer switching stories for a new product or feature
- The participant is present (live or async) and ready to be interviewed — this skill **conducts** the interview

---

## Do Not Use When

- You need a survey or questionnaire — use `copy-planner` for content briefs
- You want to review an existing interview transcript — use `interview-critic`
- You need a structured research protocol for a formal study — use `study-design-planner`
- The interviewee was NOT the decision-maker — ask for the actual decision-maker first
- You need operational project context from a client — use `discovery-proposal` for that

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Live participant ready for a switching interview | This skill — conducts interview using Moesta timeline + Four Forces |
| Need to understand WHAT outcomes to optimize (not WHY switch) | Run jtbd-interviewer first, then route to Ulwick opportunity survey |
| Want to review quality of a completed transcript | Use `interview-critic` |
| Need quantified job importance/satisfaction data | Run 10+ interviews first, then apply Ulwick opportunity algorithm |
| Client project intake, not user research | Use `discovery-proposal` |
| Have a transcript to analyze, not a live participant | Use phuryn/pm-skills `summarize-interview` (community skill) |

---

## What You Get

- **Job Statement** (Ulwick syntax): When [context], I want to [action], so I can [outcome]
- **Four Forces Summary**: Push, Pull, Anxiety, Habit — each with a direct quote and confidence level
- **Struggling Moments**: 2–3 concrete friction points in the participant's own words
- **Candidate Outcome Statements**: For future Ulwick quantification
- **Interview Quality Score**: 1–5 with justification and unanswered questions

---

## Background

Most product teams skip the "why did they switch" question and jump to feature prioritization. A JTBD switching interview reconstructs the causal narrative behind adoption — who struggled with what, what promise pulled them forward, what fear almost stopped them, what habit they gave up. That narrative is the foundation for job statements, messaging, and outcome prioritization.

**The Four Forces tracked throughout every interview:**
- **F1 Push**: frustration with the current situation driving the participant away
- **F2 Pull**: the aspiration or promise of the new solution attracting them forward
- **F3 Anxiety**: fear that the new solution might not work or might cause harm
- **F4 Habit**: inertia of current behavior — what worked "good enough" that had to be abandoned

A switch happens when F1 + F2 > F3 + F4.

---

## Companion Skills

- **interview-critic**: Reviews a completed transcript for Four Forces coverage, job statement validity, and interviewer technique quality
- **study-design-planner**: Formal research protocol after JTBD discovery
- **copy-planner**: Messaging work informed by job statements

---

## meta-router Registry Note

Listed under the **Planners** table (discovery intent, not review intent).
Trigger signals: `JTBD interview, user research, switching story, discovery interview, purchase story, why did they switch`
