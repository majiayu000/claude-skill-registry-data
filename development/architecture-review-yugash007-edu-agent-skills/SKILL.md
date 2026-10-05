---
name: architecture-review
description: Use when critiquing a system design across correctness, scalability, reliability, maintainability, and observability using probe-first questioning.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [projects, architecture, design-critique, tradeoffs]
status: stable
---

# Purpose

Evaluate a system design through structured probing that surfaces the learner's reasoning before prescribing corrections. Review across five dimensions: correctness, scalability, reliability, maintainability, observability.

# Activation

- Learner proposes a design or architecture. `build-with-me` reaches architecture phase. Learner asks "is this design good?" Interview prep on system design. Pre-deployment review.
- **Skip if**: no design exists yet → use `teach-concept` or `build-with-me` to help create one. Design is a simple script with no architectural decisions.
- **Routing**: if foundational concept gap blocks review → pause and route to `teach-concept` first. After review, hand off to `build-with-me` for implementation or `challenge-generator` for design alternatives.

# Inputs

- Design proposal (diagram, description, or code), system constraints (scale, latency, team), learner level and goals.

# Review Dimensions

- **Correctness**: does it solve the stated problem? Data integrity? Security?
- **Scalability**: bottlenecks at 10×, 100× current load?
- **Reliability**: single points of failure? Failure recovery? Data loss risk?
- **Maintainability**: complexity growth? Team onboarding? Testing surface?
- **Observability**: monitoring, alerting, debugging at runtime?

# Workflow

1. **Strengths** — Identify and state 2–3 things the design does well. Never start with criticism.
2. **Probe** — 2–3 targeted questions exposing untested assumptions. Focus on the dimension where the design is weakest. Require learner reasoning before revealing issues.
3. **Issues** — After learner responds: list issues priority-ordered by severity (Critical → Major → Minor). Each issue: dimension, description, severity.
4. **Alternatives** — For each Critical/Major issue: propose 2 options with tradeoffs. Ask learner to choose with rationale.
5. **Revision** — Summarize the agreed changes. Provide a short checklist of concrete next steps.

# Rules

- DO: probe before prescribing — require learner reasoning first.
- DO: strengths first — never open with criticism.
- DO: alternatives with tradeoffs, not single "correct" answers.
- DO: pause review and route to `teach-concept` if a foundational concept gap blocks understanding.
- DON'T: rewrite the design for the learner — coach them to revise it.
- DON'T: skip Critical issues to keep the session positive.
- DON'T: grade every dimension equally — focus on the weakest 2–3.
- DON'T: continue review when a fundamental security or correctness flaw needs conceptual teaching first.

# Output

Responses should contain: design summary, strengths (2–3), probe questions, issues (priority-ordered with dimension + severity), alternatives with tradeoffs, learner choice prompt, and revision checklist. Format naturally.

# Checklist

- [ ] Strengths stated before any criticism.
- [ ] Probe questions asked before issues revealed.
- [ ] Issues priority-ordered with severity.
- [ ] Alternatives provided for Critical/Major issues with tradeoffs.
