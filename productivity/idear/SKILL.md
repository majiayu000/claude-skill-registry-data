---
name: idear
description: Turn a user's rough software, tool, automation, or AI-product idea into a clarified product definition, evidence-backed feasibility report, and implementation-ready technical handoff. Use when a user asks whether an idea can be built, whether suitable technologies/permissions/APIs exist, whether others have built it, what competing products or open-source projects exist, or how to begin if it is viable.
---

# Idear

Idear is a three-stage, evidence-first product discovery workflow. It is not a generic brainstorming skill and it is not an implementation skill. Its purpose is to move a rough idea to a defensible go/no-go decision, then prepare a later development agent to take over with the correct context.

Follow the user's language for all user-facing conversation and generated artifacts. Use concise, direct language. Distinguish verified facts from inferences and untested assumptions.

## Operating Model

Users do not select stages or modes. Detect the current stage from the conversation and advance naturally. A user may add a constraint at any time; update the saved context, revisit affected conclusions, and do not retain conclusions that depended on the old constraint.

The stages are:

1. Product clarification
2. Feasibility research and report
3. Technical path and development handoff

Do not begin implementation while using this skill. If the user asks to build after Stage 3, hand off to the relevant planning or implementation workflow using the generated handoff artifacts.

## Artifact Location

At the start of Stage 1, create an idea workspace. Resolve its location in this order:

1. A path explicitly named by the user.
2. `docs/idear/<YYYY-MM-DD>-<slug>/` in the active project repository.
3. `work/idear/<YYYY-MM-DD>-<slug>/` when there is no project repository.

Use a short, stable ASCII slug. Do not create empty files before their stage needs them. Maintain `project-context.yaml` throughout all stages.

## Stage 1: Product Clarification

### Goal

Convert the user's rough idea into a product definition that is concrete enough to research.

### Required behavior

- Save the user's original wording in `00-raw-idea.md` before substantially reframing it.
- Ask one high-leverage clarification question at a time. Do not present a survey.
- Seek the problem, target user, operating environment, primary workflow, success condition, hard constraints, and non-goals.
- Treat stated constraints as binding. Examples include "LAN only", "no account", "offline", "no cloud", a target platform, or a budget limit.
- Make reasonable, clearly labelled assumptions when they do not materially change the research direction. Ask instead when an unknown would change the architecture, permissions, cost, legal posture, or feasibility conclusion.
- Summarize periodically so the user can correct the direction.
- Do not conduct broad feasibility research until there is a coherent product definition, except for small factual checks required to understand a term the user used.

### Completion gate

Write `01-product-definition.md`, update `project-context.yaml`, and ask the user to confirm or correct the clarified definition. The definition must state:

- Problem and value proposition
- Target users and scenarios
- Core product behavior
- Hard constraints
- Explicit non-goals
- Assumptions and open questions
- A one-paragraph clear product description

Only proceed to Stage 2 after the user confirms it, or clearly asks to proceed despite recorded assumptions.

Read `references/stage-1-clarification.md` before conducting Stage 1.

## Stage 2: Feasibility Research And Report

### Goal

Determine whether the defined product is technically and practically viable, using current evidence rather than model memory.

### Required research

For every idea, determine which of these are relevant and investigate them:

- Required platform capabilities, APIs, protocols, hardware, data sources, and integrations
- Authentication, authorization, operating-system permissions, security, privacy, licensing, compliance, and deployment constraints
- Existing products, commercial tools, open-source projects, SDKs, standards, and papers
- Whether similar work actually uses the mechanism claimed for it, rather than an assumed mechanism
- The project's differentiation from the closest existing alternatives
- Cost, operational burden, maintenance risk, and environmental prerequisites
- The smallest proof-of-concept that could remove the largest remaining uncertainty

### Evidence rules

- Browse for claims that may have changed: product capabilities, API behavior, permissions, pricing, project maintenance, policy, regulations, and availability.
- Prefer official documentation, official repositories, specifications, source code, release notes, and primary research.
- Use secondary sources only as supporting material and label them accordingly.
- Never present an inference, search snippet, or unverified claim as a fact.
- Classify material conclusions as `verified`, `reasoned_inference`, or `needs_poc`.
- Record every meaningful source in `sources.yaml` with URL, title, source type, access date, claim supported, and confidence.
- For each competitor or open-source project, record what it does, how it works where evidence permits, its constraints, its maintenance/licensing status, and the difference from this idea.

### Completion outputs

Create and update:

- `02-research-dossier.md`: detailed agent-facing evidence, reasoning, and unresolved questions
- `03-competitor-analysis.md`: comparable products and open-source projects
- `04-risk-register.md`: risks, severity, evidence, mitigation, and validation action
- `sources.yaml`: traceable sources
- `05-feasibility-report.md`: polished user-facing report
- `05-feasibility-report.pdf`: generate when a PDF capability is available or the user requests it
- `decision-log.md` and `project-context.yaml`

Always preserve the Markdown report even when a PDF is produced. Follow `references/stage-2-research.md`, `references/evidence-standards.md`, and `references/report-design.md`. Use the templates in `assets/templates/`.

When producing a PDF, start from `assets/templates/feasibility-report.html` and `assets/templates/feasibility-report.css` where the available PDF workflow can render HTML/CSS. If that workflow is unavailable, use the Markdown report as the source of truth and use the available document/PDF renderer without weakening the report-design requirements.

### User-facing completion response

In the chat, lead with the conclusion, not research narration. State:

- Overall feasibility verdict
- The highest-impact verified facts
- Main blockers and unknowns
- Closest existing work and the meaningful difference
- Recommended next action
- Paths to the generated report and research artifacts

Then ask whether the user wants to proceed to Stage 3. Do not begin Stage 3 merely because the idea is feasible.

## Stage 3: Technical Path And Development Handoff

### Entry gate

Enter only when the user says the idea should be pursued, asks for an implementation approach, or asks for material suitable for another development agent.

### Goal

Research and recommend a credible initial technical direction, then package the context so a future agent can plan and build without rediscovering settled facts and constraints.

### Required behavior

- Research two or three viable technical paths when meaningful alternatives exist.
- Compare each path's prerequisites, performance, complexity, cost, portability, security, maintenance burden, licensing, and fit with hard constraints.
- Recommend one path and explain the trade-offs.
- Define an MVP with explicit in-scope and out-of-scope behavior.
- Define acceptance criteria and the first proof-of-concept tasks.
- Describe a preliminary architecture: components, responsibilities, interfaces/data flow, persistent data, external services, and failure/security boundaries as applicable.
- Do not claim a technical choice is final if the user has not accepted it. Mark it as recommended or proposed.

### Completion outputs

Create and update:

- `06-technical-paths.md`: options and selection rationale
- `07-initial-solution.md`: preliminary architecture, MVP, and PoC plan
- `08-ai-handoff.md`: self-contained handoff for a later development agent or new conversation
- `project-context.yaml`: machine-readable current state
- `decision-log.md`

Read `references/stage-3-handoff.md` before generating these artifacts.

## Context Maintenance

`project-context.yaml` is the authoritative machine-readable state. Update it after each material user clarification, research result, decision, reversal, or identified risk. Do not delete historical decisions; mark them superseded and point to the replacement decision.

The next development agent should be instructed to read `project-context.yaml`, then `08-ai-handoff.md`, then any linked evidence before proposing implementation work.

## Scope And Safety

- Keep research within legal, ethical, and authorized boundaries.
- Surface security and privacy risk without giving instructions that would create unauthorized access or harm.
- Be clear when a result depends on a user-owned test environment, paid account, private data, or administrator permission.
- Do not create a false sense of certainty. A technically plausible project can still be too costly, blocked by permissions, or already well served by existing solutions.
