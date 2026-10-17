---
name: portfolio-project-planner
description: Plans a portfolio-oriented software project so implementation, documentation, screenshots, demos, architecture reasoning, and case-study evidence develop together. Use when the user asks to plan a project for a portfolio, GitHub showcase, case study, demo-ready build, recruiter-facing proof, launch narrative, or evidence-backed development process.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: developers-students-career-changers-portfolio-builders-and-technical-writers
  tags:
    - portfolio
    - case-study
    - documentation
    - demos
    - screenshots
    - architecture
    - evidence-planning
  status: draft
  side_effects: none
---

# Portfolio Project Planner

## Purpose

Plan a software project as both a working implementation and a portfolio artifact, ensuring that code, documentation, screenshots, demos, architectural reasoning, validation evidence, and case-study material are captured throughout the build instead of reconstructed after the project is finished.

## When to use this skill

Use this skill when:

- The user wants to plan a project that will appear in a portfolio, GitHub profile, resume, case study, demo page, or launch post.
- The project needs implementation tasks and storytelling artifacts to develop in parallel.
- The user wants a plan for capturing screenshots, demos, decisions, tradeoffs, metrics, before/after evidence, or process notes while building.
- The user asks how to make a project more portfolio-worthy before implementation starts.
- A rough project idea needs milestones that include code, docs, visuals, demos, and proof of quality.
- The user wants to show architectural reasoning, technical tradeoffs, accessibility, performance, testing, or product thinking as part of the final artifact.

Do not use this skill when:

- The user only wants a generic implementation plan with no portfolio, demo, or case-study goal.
- The user only needs final marketing copy or a completed case study after the project is already done.
- The user is asking for a repository readiness review of an existing public project.
- The task is only visual polish, accessibility review, or documentation SEO without project planning.
- The request requires private, employer-owned, or confidential material that should not be included in a public portfolio.

## Inputs to inspect

Start with the user's project idea, audience, portfolio goal, constraints, preferred stack, available time, and desired proof points.

If working inside a repository or project folder, inspect relevant planning and public-facing files such as:

- `README.md`
- `BRIEF.md`, `PRD.md`, `PLAN.md`, `ROADMAP.md`, or `TODO.md`
- `docs/`
- `design/`, `wireframes/`, or mockups
- `demo/`, `examples/`, or app routes intended for demos
- Architecture notes, ADRs, schema files, API contracts, or integration docs
- Existing screenshots, videos, benchmark notes, test reports, or accessibility reports
- Portfolio, case-study, resume, or launch-post drafts if provided

Do not read the entire repository by default. Start with planning, documentation, and demo-facing artifacts, then inspect implementation files only when they affect feasibility, evidence, screenshots, demos, or architecture claims.

## Workflow

1. Define the portfolio outcome: target audience, desired impression, project narrative, role being demonstrated, and final artifacts such as README, live demo, screenshots, video, case study, or architecture writeup.
2. Identify the product core: user problem, primary workflow, must-have features, non-goals, constraints, and success criteria for a credible finished project.
3. Map evidence needs before implementation:
   - Screenshots or videos needed to explain the product
   - Demo scenarios that show the strongest user flow
   - Architecture decisions and tradeoffs worth documenting
   - Tests, benchmarks, accessibility checks, or quality signals worth capturing
   - Process artifacts such as sketches, requirements, issue plans, milestones, or before/after comparisons
4. Split the project into milestones that produce both working software and portfolio evidence. Avoid milestones that only say “build feature” without a matching proof artifact.
5. For each milestone, specify:
   - Implementation deliverables
   - Documentation or case-study notes to write at that moment
   - Screenshot, video, demo, metric, test, or decision evidence to capture
   - Acceptance criteria
   - Risks, dependencies, and scope boundaries
6. Plan architectural reasoning checkpoints before irreversible or high-impact decisions. Capture alternatives, chosen approach, tradeoffs, and evidence for the decision.
7. Plan demo readiness alongside implementation: seed data, stable flows, empty/error/loading states, deployment needs, sample credentials, privacy-safe data, and reproducible demo steps.
8. Plan documentation incrementally: README sections, setup instructions, feature walkthrough, architecture diagram, testing notes, deployment notes, and case-study outline.
9. Add portfolio polish gates for first impression, accessibility, responsive screenshots, project metadata, live-demo links, and final narrative consistency.
10. Finish with immediate next actions that start both the code path and the evidence-capture path.

## Output format

Return the plan using this structure:

```md
## Summary

Brief statement of the portfolio goal, target audience, and recommended build narrative.

## Portfolio outcome

- Target audience:
- Role or strengths demonstrated:
- Final artifacts:
- Core proof points:

## Milestone plan

| Milestone | Implementation deliverables | Evidence to capture | Documentation/case-study work | Acceptance criteria |
|---|---|---|---|---|
| 1. Name | ... | ... | ... | ... |

## Demo and screenshot plan

| Moment | What to show | Required app state/data | Capture format | Notes |
|---|---|---|---|---|

## Architecture and decision log plan

| Decision | Options to compare | Evidence needed | When to decide | Output artifact |
|---|---|---|---|---|

## Quality and credibility checks

- [ ] Tests or validation:
- [ ] Accessibility:
- [ ] Performance or reliability:
- [ ] Documentation accuracy:
- [ ] Privacy-safe demo data:

## Risks and scope controls

| Risk | Portfolio impact | Mitigation |
|---|---|---|

## Immediate next actions

1. ...
2. ...
3. ...
```

If the user asks for a shorter response, keep the milestone plan, evidence plan, and immediate next actions.

## Quality bar

The task is complete only when:

- The plan connects implementation work to visible portfolio evidence.
- Each milestone includes at least one code deliverable and one documentation, demo, screenshot, decision, or validation artifact.
- The plan identifies what should be captured during the build, not only after completion.
- Demo scenarios are specific enough to reproduce with data, routes, commands, or user actions.
- Architecture reasoning includes alternatives, tradeoffs, and evidence instead of only naming a final choice.
- Public-facing artifacts avoid private data, secrets, employer-owned details, and unverifiable claims.
- The final plan distinguishes must-have portfolio proof from optional polish.

## Edge cases

- If the project idea is vague, create a provisional plan around a small credible MVP and list the decisions needed to sharpen the portfolio narrative.
- If the project is already partly built, first separate evidence that already exists from evidence that still needs to be captured or recreated honestly.
- If the user has limited time, prioritize one polished demo path, one strong screenshot set, and one clear architecture decision over many shallow features.
- If the project is backend-only or CLI-focused, plan terminal captures, API examples, logs, diagrams, benchmarks, tests, and integration demos instead of UI screenshots.
- If claims require metrics, benchmarks, accessibility scores, or external validation, mark them as planned evidence until measured.
- If the portfolio audience is unclear, optimize for a technical reviewer who wants to see problem framing, engineering judgment, working software, and proof of quality.

## Related skills

- `project-roadmap-builder`
- `implementation-plan-writer`
- `repo-public-profile-polish`
- `portfolio-case-study-writer`
