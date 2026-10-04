---
name: project-design-reviewer
description: Use when Codex should critique whether a project, feature, architecture, workflow, or implementation plan is well designed before or during implementation. Review design files, specs, READMEs, architecture docs, plans, or inferred designs for problem fit, requirements quality, feasibility, tradeoffs, risks, assumptions, interfaces, data, operations, and actionability. If no design artifact exists, use codex-deep-interview to elicit the user's design intent, or ask permission to infer a draft design from the local implementation and confirm it before reviewing. Use anysearch only for design claims that require current external evidence, official docs, benchmarks, standards, platform limits, or best practices.
---

# Project Design Reviewer

Critique the design itself, not only whether implementation matches a design. This skill is for project/feature/architecture sanity review before committing to a direction, and for catching designs that are unclear, overbuilt, under-specified, risky, or based on weak assumptions.

## Review Modes

1. Existing design artifact.
   - Use when the user provides or points to `DESIGN.md`, `ARCHITECTURE.md`, specs, PRDs, ADRs, implementation plans, diagrams, README sections, or planning notes.
   - Review the artifact directly after reading relevant local context.

2. No design artifact, user has design intent.
   - Use `$codex-deep-interview` to clarify the design idea before judging it.
   - Ask one concise question at a time until the problem, users, constraints, non-goals, success criteria, and key decisions are clear enough to review.
   - Produce a short design-intent brief, then review that brief.

3. No design artifact, implementation exists.
   - Do not silently treat the codebase as the intended design.
   - Ask permission before reverse-engineering a design draft from implementation.
   - If approved, inspect local code/docs/tests, summarize the inferred design, mark inferred parts clearly, and ask the user to confirm or correct it before issuing a final design review.

## Workflow

1. Locate design evidence.
   - Search likely files first: `DESIGN*`, `ARCHITECTURE*`, `SPEC*`, `ADR*`, `docs/**`, `README*`, `plans/**`, `.codex/**`, `AGENTS.md`, issue/PR notes if available.
   - Read the smallest set that explains purpose, constraints, architecture, and intended behavior.
   - Keep local facts separate from inferred intent.

2. Choose the mode.
   - If a design artifact exists, review it.
   - If no artifact exists and the user's design idea is underspecified, invoke `$codex-deep-interview`.
   - If no artifact exists but implementation exists, ask: "I do not see a design file. Should I infer a draft design from the current implementation for your confirmation before reviewing it?"

3. Build the design-under-review.
   - Summarize the design in plain language.
   - Identify goals, non-goals, users/operators, constraints, architecture, interfaces, data/state, dependencies, rollout/migration, operations, and acceptance criteria.
   - Mark missing or inferred sections explicitly.

4. Route uncertainty and external evidence.
   - Use local evidence for repo-specific design claims.
   - Use `$uncertainty-router` when it is unclear whether to inspect, search, test, ask, or assume.
   - Use `$anysearch` only when the design depends on external current facts or accepted guidance, such as official framework docs, cloud service limits, API behavior, security standards, legal/regulatory constraints, benchmark results, pricing/cost assumptions, or current ecosystem best practices.
   - Prefer official docs, standards, vendor docs, primary research, or authoritative project docs over blogs.
   - Cite external sources in the review when they materially affect a finding.

5. Review the design dimensions.
   - Problem fit: Does the design solve the stated problem for the intended users?
   - Scope: Are goals, non-goals, and boundaries explicit enough to prevent drift?
   - Requirements: Are functional and non-functional requirements testable?
   - Architecture: Are components, responsibilities, interfaces, and data/state flows coherent?
   - Feasibility: Is the design realistic for the team, timeline, dependencies, tools, and operating environment?
   - Tradeoffs: Are complexity, speed, flexibility, reliability, cost, security, usability, and maintainability choices explicit?
   - Assumptions: Which assumptions are unsupported, stale, risky, or user-preference dependent?
   - Operations: Are rollout, migration, observability, failure recovery, support, and maintenance considered when relevant?
   - Actionability: Could implementation start from this design without hidden decisions?

6. Classify findings.
   - Blocker: Design is likely to fail, mis-solve the problem, or create severe risk unless changed.
   - Major: Important ambiguity, missing decision, unsupported assumption, or costly tradeoff.
   - Minor: Clarity, completeness, or polish issue that does not block the next step.
   - Observation: Useful context or strength worth preserving.

7. Recommend next action.
   - Prefer concrete design edits over vague advice.
   - If the design is not ready, say what must be decided before implementation.
   - If the design is good enough, state the conditions and verification gates for proceeding.
   - Route to `$decision-record-writer` when a reviewed choice should become a durable decision note.
   - Route to `$codex-consensus-plan` only after the design direction is sufficiently sound and ready to become an implementation plan.

## Output Shape

Use this structure unless the user asks for a different format:

- Design under review
- Evidence inspected
- Overall assessment
- Strengths to preserve
- Findings by severity
- External evidence used, if any
- Required design changes
- Open questions
- Proceed / revise / stop recommendation

For each finding, include:

`Severity | Design area | Issue | Why it matters | Evidence | Recommendation`

## Boundaries

- Do not write production code as part of this skill.
- Do not pretend an inferred design is user-approved.
- Do not require external search for ordinary local design critique.
- Do not overfit to generic architecture patterns when project constraints point elsewhere.
- Do not reduce the review to code-style or implementation-diff review; use code only as evidence for inferred design or design feasibility.

## Source-Aware Notes

This skill's shape is inspired by public design and architecture review patterns such as software design review skills, architecture reviewer agents, and Well-Architected review frameworks. Use those ideas as review heuristics, not as rigid doctrine.
