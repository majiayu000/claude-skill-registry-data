---
name: "integration-orchestrator"
description: "Generate a phased delivery orchestration plan for creative-direction-driven work: which skills run when, what locks at which gate, how handoffs occur, and how the cadence implements in the team's tools (Jira, Linear, Notion, Figma, GitHub) with AI agents via MCP and CLI. A temporal map of phases, lock points, handoff specs, gate definitions, and QA verification gates. Distinct from `creative-brief` (static project brief) and `creative-direction` (aesthetic direction). Triggers on integration orchestrator, delivery cadence, project orchestration, when does the brief lock, how to phase creative direction, design-development handoff, QA gate, agent-driven QA, and when a creative-direction project is starting, mid-flight with broken cadence, or integrating AI agents into PM workflow. Does NOT fire for project scoping (use `creative-brief`), aesthetic direction (use `creative-direction`), or general project management without a creative-direction throughline."
---

# Integration Orchestrator

A brief tells a team what to make. Creative direction tells them what it should feel like. Neither tells them when each decision locks, who reviews what, or what stops the next phase from starting before the prior one is done. That is the gap this skill fills.

The output is a phased orchestration plan the PM can paste into a calendar Monday morning and start running Tuesday. Phases, gates, lock points, handoffs, QA verification rules, and a platform-specific implementation guide for whatever stack the team actually uses (Jira, Linear, Notion, Figma, GitHub, agile sprints).

---

## What this skill is

A creative-direction project has three layers. The brief layer defines scope, audience, deliverables, constraints, success criteria. The direction layer defines tone, aesthetic, relationship, and sensory ambition. Both produce written artifacts. Neither answers the temporal question: when does the brief lock, when does identity lock, when does copy lock, who reviews each, what gets blocked while a gate is open, what happens when a downstream task discovers the brief is wrong, and what makes "Done" mean tested rather than self-reported.

This skill produces that temporal layer. Most teams have briefs and creative direction but no orchestration plan. The result, by week 3, is everyone working in parallel with no shared sense of which decisions are still open and which are locked. Brief drift. Re-work. Identity tokens shifted after copy was already drafted against the old ones. Engineering shipping before design had a chance to review. "Done" tickets that were never actually verified.

The orchestration plan answers all of that. It is not theory. It is a phased timeline with calendar weeks, ticket templates the PM can paste into Jira or Linear, MCP commands for setup, gate definitions with measurable pass criteria, handoff specs with artifact requirements, and QA verification gates with Playwright or Chrome MCP invocations.

---

## When to use

- Starting a new brand build, rebrand, or campaign and the team needs to sequence the work
- Mid-flight project where the brief is being revisited and downstream work is suffering from constant resets
- Setting up a new team's agent-driven workflow with MCPs and CLI integration
- Multi-team work where handoffs between brand, design, and engineering have broken down
- Establishing QA verification gates so "Done" is measurable, not self-reported
- Migrating from ad-hoc orchestration to a documented cadence
- Onboarding a new PM or design lead onto an existing project that has running tickets but no documented sequencing
- Adding new platforms or tools to an existing workflow and the cadence needs to be re-mapped

---

## When NOT to use

- Use `creative-brief` instead if the deliverable is the project brief itself: scope, audience, deliverables, constraints, success criteria. The orchestrator skill takes the brief as input.
- Use `creative-direction` if the deliverable is the aesthetic direction: tone, aesthetic, relationship, sensory. The orchestrator schedules the work that answers to the direction; it does not produce the direction.
- Generic project management software is the platform; this skill produces the plan that runs IN the platform. Do not run this skill if the team needs help picking a tool; it assumes the tool stack is already chosen.
- Sprint-planning tactics (story-pointing, retros, velocity charts) live downstream of orchestration. The skill produces the cadence; sprint planning fills it in.

---

## Required inputs

- **Project type.** New brand build, rebrand, single landing page, campaign, identity refresh, website refresh, microsite, product launch. The type implies a default phase decomposition that the skill adapts to the specific project.
- **Team composition.** Total size and role mix. Solo, small (2-3), medium (4-7), large (8+). Whether AI agents (Claude Code, Claude in Chrome, others) participate in production, QA, or both.
- **Tool stack.** Which of Jira, Linear, Notion, Figma, GitHub the team uses. Plus QA tooling (Playwright, Chrome MCP, Windows MCP, mobile testing harnesses) if known. Plus communication and paging channel (Slack, email, in-tool mention). The output adapts to the actual stack.
- **Timeline target.** Express (compressed timelines, fewer reviewers, accept higher rework risk), standard (typical cadence at the project type's default duration), or thorough (more reviewers, formal phase reviews, lower rework risk at the cost of slower delivery).
- **Existing constraints.** What is already locked? Brief approved, identity locked, platform fixed, brand voice already shipped, content management system non-negotiable. The orchestrator plan handles greenfield and mid-flight equally; the existing constraints input is how mid-flight projects are accommodated.
- **AI agent participation.** Which workflows include agents and at what fidelity. Examples: Claude Code does production tasks against a state file in the repo; Claude in Chrome runs human-readable QA flows on the staging deployment; the agent has access to the Linear MCP and the GitHub MCP but not Jira; the agent can move tickets between Todo, In Progress, Waiting, and Blocked but cannot move to Done (Done requires a human verification step).
- **Risk profile.** Optional input naming the failure modes the team is most worried about: brief drift, parallel-work conflicts, QA gaps, agent runaway. The orchestration plan front-loads mitigations for the named risks.

---

## Output format

Default output is a markdown document, typically saved as `ORCHESTRATION.md` at the project root or in a `docs/` subdirectory. The document contains the full plan and is the canonical reference for the team.

Structure:

1. **Project orchestration plan.** Phased timeline with calendar weeks, milestone dates, phase outputs.
2. **Per-phase gate specs.** What enters, what exits, who approves, the measurable pass criteria for each gate including the QA verification gate.
3. **Lock-point register.** What becomes immutable when, where the locked artifact lives, who can request a change, and what re-review work a change triggers.
4. **Tool-stack implementation guide.** Concrete setup for Jira, Linear, Notion, Figma, and GitHub as applicable, with MCP commands or CLI invocations for the parts that automate.
5. **QA verification gate spec.** Which automated tests must pass, which MCPs run them, where evidence attaches, what happens on failure.
6. **Handoff specs.** Artifacts transferred per handoff, locked items, change-request protocols, adjacent-observation routing.
7. **Cross-skill dependency graph.** Which skills run in which phase, what each skill consumes, what each produces.
8. **Risk register.** Cadence-specific risks with mitigations.

The document is the orchestration plan. The next step after delivery is for the PM to set up the team's tools to match (Jira epics, Linear projects, Notion databases, Figma libraries, GitHub branch protection) and start running the plan.

---

## Reference files

- [`references/cadence-patterns.md`](references/cadence-patterns.md). The 7 project-type cadences in detail with phase decomposition, timelines, gate definitions, and tool-stack implementation skeletons.
- [`references/gate-definitions.md`](references/gate-definitions.md). Each standard gate with trigger, approver, pass criteria, what's blocked, what's already locked, and change-request protocols.
- [`references/handoff-protocols.md`](references/handoff-protocols.md). The standard handoffs between phases and skills, plus the adjacent observation handoff for filing things noticed while working nearby.
- [`references/platform-implementation.md`](references/platform-implementation.md). How the orchestration maps to Jira, Linear, Notion, Figma, and GitHub, including MCP integration notes per platform and CLI alternatives where MCP is the wrong tool.
- [`references/team-size-modulation.md`](references/team-size-modulation.md). How cadences scale across solo, small, medium, and large teams.
- [`references/automation-and-qa-tooling.md`](references/automation-and-qa-tooling.md). The QA verification gate pattern, MCP vs CLI tradeoffs, session memory and momentum patterns, code-to-ticket linkage, and evidence trails.
- [`references/example-orchestration.md`](references/example-orchestration.md). A complete worked example showing all sections populated for a representative scenario.


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The framework: 7 considerations for orchestration: [method](references/domain-guide.md#the-framework-7-considerations-for-orchestration).
- Common project-type cadences: [method](references/domain-guide.md#common-project-type-cadences).
- Failure patterns: [method](references/domain-guide.md#failure-patterns).
