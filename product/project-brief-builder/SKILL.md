---
name: project-brief-builder
description: Converts a rough project idea, feature concept, product request, or early problem statement into a structured project brief. Use when the user asks to clarify an idea, write a project brief, define goals, identify users, capture constraints, set success criteria, state assumptions, exclude out-of-scope work, or prepare an idea for planning, design, or implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: generator
  audience: founders-product-managers-developers-designers-and-project-maintainers
  tags:
    - project-brief
    - product-planning
    - requirements
    - scope
    - success-criteria
    - assumptions
  status: draft
  side_effects: none
---

# Project Brief Builder

## Purpose

Convert an ambiguous project idea into a concise, structured brief that can guide planning, design, implementation, research, or stakeholder review.

This skill turns rough input into explicit goals, users, use cases, constraints, success criteria, assumptions, risks, exclusions, open questions, and next steps. It preserves uncertainty instead of pretending that missing information is known.

The result should be useful as a handoff artifact before writing a roadmap, implementation plan, design spec, issue backlog, proposal, or requirements document.

## When to use this skill

Use this skill when:

- The user provides a rough project idea and wants it organized.
- The user asks for a project brief, concept brief, product brief, feature brief, or planning brief.
- A feature request needs clearer goals, users, constraints, success criteria, and non-goals.
- A vague idea needs to be made actionable before estimating or implementing it.
- A stakeholder request includes mixed goals, possible solutions, and unresolved assumptions.
- A project needs alignment around scope before a roadmap or implementation plan is created.
- A user wants to compare possible directions but first needs the core brief written.
- A repository, README, proposal, issue, or notes file contains scattered project intent that should be synthesized into a brief.

Common trigger phrases include:

- “Turn this idea into a project brief.”
- “Help me clarify this project.”
- “Write a brief for this feature.”
- “Define goals, users, and success criteria.”
- “What assumptions are we making?”
- “What is out of scope?”
- “Make this idea ready for planning.”
- “Create a product brief.”
- “Structure this concept.”
- “Help me scope this before building.”

Do not use this skill when:

- The user only needs an implementation plan for an already-scoped brief.
- The user asks to reconcile an existing plan with repository progress.
- The primary task is market research requiring current external sources.
- The user needs a polished marketing page, pitch deck, or launch announcement rather than a planning brief.
- The request is only to write code or change repository files.
- Another more specific domain skill already covers the requested artifact.

## Inputs to inspect

Start with the user-provided idea, notes, or conversation context.

If working inside a repository or document set, inspect only relevant sources such as:

- `README.md`
- `VISION.md`
- `BRIEF.md`
- `PRD.md`
- `ROADMAP.md`
- `PLAN.md`
- `TODO.md`
- `BACKLOG.md`
- `docs/`
- `planning/`
- `product/`
- `requirements/`
- issue templates or local issue exports
- design notes, research notes, or stakeholder notes
- existing examples, demos, or prototypes that reveal intended behavior

Do not read the whole repository unless the project idea depends on broad context. Prefer the smallest set of files needed to understand the intended outcome.

## Brief principles

Build the brief around decisions, not decoration.

A strong brief should:

- State the problem before prescribing a solution.
- Identify who benefits and who must operate or maintain the project.
- Separate goals from features.
- Convert vague aspirations into observable outcomes.
- Make constraints explicit.
- Preserve assumptions and open questions.
- Name exclusions so the project does not silently expand.
- Distinguish must-have scope from nice-to-have scope.
- Avoid inventing facts, metrics, stakeholders, deadlines, or requirements without evidence.
- Use plain language that both technical and non-technical stakeholders can review.

## Information model

Cover these sections unless the user asks for a different format:

| Section | Purpose |
|---|---|
| `Working title` | Short descriptive name for the project. |
| `One-sentence summary` | Plain-language explanation of what the project is. |
| `Background` | Context, origin, current pain, or opportunity. |
| `Problem statement` | The specific problem to solve, not just the proposed solution. |
| `Target users and stakeholders` | Primary users, secondary users, buyers, maintainers, approvers, or affected groups. |
| `User needs and use cases` | Jobs to be done, scenarios, and expected user outcomes. |
| `Goals` | Intended business, user, technical, operational, or learning outcomes. |
| `Non-goals and exclusions` | Explicitly out-of-scope work, audiences, platforms, features, and behaviors. |
| `Scope` | Must-have, should-have, could-have, and deferred capabilities. |
| `Constraints` | Time, budget, technology, compliance, accessibility, data, staffing, platform, brand, or operational limits. |
| `Success criteria` | Observable conditions that indicate success. |
| `Metrics or signals` | Quantitative or qualitative indicators to watch when applicable. |
| `Assumptions` | Beliefs being treated as true without proof. |
| `Risks` | What could make the project fail, stall, or produce harm. |
| `Dependencies` | People, decisions, systems, data, integrations, approvals, or prior work needed. |
| `Open questions` | Questions that must be answered before planning, design, implementation, or launch. |
| `Recommended next steps` | Small follow-up actions to validate, plan, or execute. |

## Workflow

### 1. Establish brief scope

Identify:

- The artifact being produced.
- The audience for the brief.
- Whether the brief is for a product, internal tool, feature, research project, content project, event, or operational initiative.
- Whether the user wants a quick brief, detailed brief, or planning-ready brief.
- Whether the work is purely conceptual or grounded in existing repository or document evidence.

If the audience or intended use is unclear, choose a reasonable default and state it as an assumption.

### 2. Extract explicit facts

From the prompt and available materials, list what is actually known:

- Proposed solution or concept.
- Problem or opportunity.
- Target users or stakeholders.
- Desired outcomes.
- Existing constraints.
- Mentioned technologies, channels, formats, or platforms.
- Deadlines, milestones, or urgency.
- Required integrations or dependencies.
- Known exclusions.

Do not treat guesses as facts. Mark thinly supported details as assumptions or open questions.

### 3. Separate problem, solution, and outcome

Rewrite the idea into three distinct layers:

1. **Problem:** What pain, gap, risk, or opportunity exists?
2. **Solution direction:** What project, product, feature, workflow, or artifact might address it?
3. **Outcome:** What will be better if the project succeeds?

If the user only provided a solution, infer the likely problem cautiously and label it as an inference.

If several possible problems could motivate the same idea, list the alternatives and ask or recommend validation.

### 4. Identify users and stakeholders

Define groups precisely enough to guide decisions.

For each important group, capture:

- Who they are.
- What they need.
- What they currently do instead.
- What success looks like for them.
- How much influence they have over requirements or approval.
- Whether they are primary, secondary, internal, external, operational, or affected stakeholders.

Avoid generic labels such as “users” when a more specific group is available.

### 5. Convert goals into testable outcomes

Transform broad goals into observable criteria.

Weak goal:

```txt
Make onboarding better.
```

Stronger goal:

```txt
New contributors can find setup instructions, run the project locally, and complete the first example without maintainer help.
```

For each goal, define:

- The intended outcome.
- The user or stakeholder served.
- Evidence that would show progress.
- Whether it is a must-have, should-have, or nice-to-have outcome.

### 6. Define scope boundaries

Create three levels of scope:

1. **In scope:** Necessary capabilities or deliverables.
2. **Deferred:** Valuable but not required for the first useful version.
3. **Out of scope:** Work that should not be included unless the brief changes.

Use exclusions to prevent common scope creep, such as:

- Extra user roles.
- Additional platforms.
- Advanced automation.
- Custom integrations.
- Admin features.
- Full rebrands or rewrites.
- Migration of historical data.
- Enterprise compliance requirements.
- Real-time collaboration.
- Monetization or billing.
- Analytics dashboards.

Do not exclude something if it is necessary for the core project outcome.

### 7. Capture constraints and dependencies

List limits and prerequisites that shape feasible options.

Consider:

- Timeline and sequencing.
- Budget or staffing.
- Technical stack.
- Hosting or runtime environment.
- Data availability and data quality.
- Security, privacy, legal, compliance, and licensing requirements.
- Accessibility and localization expectations.
- Brand, content, or design standards.
- Browser, device, or platform support.
- External APIs, vendors, or services.
- Organizational approvals.
- Maintenance ownership after delivery.

If no constraint is known, say so and identify the highest-impact constraints to confirm.

### 8. State assumptions explicitly

Record assumptions as statements that can be validated.

Good assumptions:

- “Primary users have enough context to provide their own project goals.”
- “The first version can be delivered without payment or account management.”
- “Existing documentation is accurate enough to reuse.”

Poor assumptions:

- “Users will like it.”
- “It should be easy.”
- “The data is probably fine.”

For each important assumption, include the implication if it is wrong.

### 9. Identify risks and open questions

Separate risks from questions:

- A **risk** is a possible future issue that could harm the project.
- An **open question** is missing information needed to make a decision.

Prioritize risks and questions by their ability to change scope, cost, design, implementation, or launch readiness.

Do not flood the brief with generic risks. Include only risks that plausibly matter for this project.

### 10. Define success criteria and signals

Success criteria should be observable and tied to the brief’s goals.

Use a mix of:

- Functional acceptance criteria.
- User outcome criteria.
- Operational criteria.
- Quality criteria.
- Accessibility or usability criteria.
- Adoption, retention, engagement, support, or conversion signals when appropriate.
- Qualitative feedback signals when quantitative metrics are not available.

Avoid fake precision. If no baseline exists, phrase metrics as signals to establish rather than targets to guarantee.

### 11. Draft the brief

Write the brief in a structured format.

Use concise language, but include enough detail that another agent, designer, developer, or stakeholder can act on it without rereading the raw idea.

When the input is sparse:

- Produce a useful first-draft brief.
- Label inferred content clearly.
- Use placeholders sparingly.
- Put missing information in `Open questions` instead of blocking the whole task.

When the input is rich:

- Synthesize rather than copy.
- Resolve duplicate statements.
- Highlight contradictions.
- Preserve important nuance.

### 12. Recommend next steps

End with practical follow-up actions.

Good next steps may include:

- Answering high-impact open questions.
- Validating a key assumption with users.
- Choosing a target user segment.
- Creating a lightweight prototype.
- Writing an implementation plan.
- Drafting acceptance criteria or issues.
- Reviewing technical feasibility.
- Confirming constraints with stakeholders.

Avoid jumping directly to implementation when the brief still contains unresolved scope-changing questions.

## Output format

Return the result using this structure:

```md
## Project brief

### Working title

...

### One-sentence summary

...

### Background

...

### Problem statement

...

### Target users and stakeholders

| Group | Role | Needs | Success looks like |
|---|---|---|---|

### Goals

| Priority | Goal | Outcome | Evidence of success |
|---|---|---|---|

### User needs and use cases

- ...

### Scope

#### In scope

- ...

#### Deferred

- ...

#### Out of scope

- ...

### Constraints

- ...

### Success criteria

- [ ] ...

### Metrics or signals

- ...

### Assumptions

| Assumption | Why it matters | If wrong |
|---|---|---|

### Risks

| Risk | Impact | Mitigation |
|---|---|---|

### Dependencies

- ...

### Open questions

| Priority | Question | Why it matters |
|---|---|---|

### Recommended next steps

1. ...
```

For a lighter user request, keep the same sections but make each section concise.

For a planning-ready request, add:

```md
### Milestone candidates

| Milestone | Purpose | Exit criteria |
|---|---|---|

### Candidate first version

- Must include:
- Can omit:
- Validation needed before build:
```

If source documents were inspected, add:

```md
## Sources used

- `path/to/file`: relevant evidence.
```

## Quality bar

The task is complete only when:

- The brief is specific to the provided idea or inspected materials.
- The problem, solution direction, and desired outcomes are distinguishable.
- Primary users and stakeholders are named or explicitly marked as unknown.
- Goals are outcome-oriented rather than only feature-oriented.
- Success criteria are observable.
- Constraints, assumptions, risks, dependencies, and open questions are separated.
- Exclusions are explicit enough to prevent likely scope creep.
- Inferred content is labeled as inference or assumption.
- Missing information appears as prioritized open questions.
- Recommended next steps are concrete and ordered.
- No unsupported market, legal, financial, medical, or technical claims are presented as facts.
- No files, issues, boards, or remote systems are modified unless the user separately asks for implementation.

## Edge cases

### The idea is only one sentence

Produce a first-draft brief using cautious inferences. Keep assumptions and open questions prominent. Do not ask so many questions that no useful artifact is produced.

### The user already has a detailed PRD

Summarize and normalize it into the brief format. Highlight contradictions, missing decisions, and scope gaps instead of rewriting everything from scratch.

### The input mixes several project ideas

Separate the ideas. Either create one brief per idea or recommend choosing one primary project before planning.

### The user asks for a plan, not a brief

If scope is unclear, build the brief first and recommend a plan as the next step. If scope is already clear, use a planning skill instead.

### The idea depends on external facts

Flag which claims require current research or source verification. Do not browse or assert current market, legal, pricing, policy, or competitor facts unless the user asked for research and the environment supports it.

### The stakeholder goal conflicts with user value

Call out the tension explicitly. Propose alternative success criteria that balance stakeholder outcomes with user outcomes.

### The project is non-software

Adapt the same structure to the domain. Users may become readers, attendees, clients, operators, students, maintainers, or beneficiaries. Deliverables may be documents, workshops, campaigns, services, workflows, or physical outputs.

### The user wants implementation immediately

Brief first only to the minimum level needed to avoid building the wrong thing. Identify unresolved questions that could materially change implementation.

## Related skills

- `project-plan-reconciler`
- `ui-design-direction-builder`
- `repo-next-steps-review`
