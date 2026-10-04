---
name: agentic-ai-transformation-office
description: Use when the user needs a consulting-style plan to move AI, generative AI, or agentic AI from pilots to measurable enterprise value. Triggers include AI transformation, agentic AI operating model, AI value realization, AI governance, workflow redesign, pilot-to-scale problems, AI portfolio prioritization, human-in-the-loop design, AI adoption, and executive AI roadmap requests.
---

# Agentic AI Transformation Office

Use this skill to structure an enterprise AI or agentic-AI transformation around value, operating model, workflow redesign, governance, adoption, and scaling.

## Reference Loading

Read `references/current-signals.md` when the user asks about current AI transformation trends, market context, executive talking points, or why AI pilots are not scaling.

Read `references/transformation-artifacts.md` when producing a roadmap, governance model, portfolio review, AI operating model, or transformation-office workplan.

## Core Diagnosis

Start by separating five problems that are often mixed together:

1. Value thesis: which business outcome should improve, by how much, and where in the P&L or risk profile?
2. Workflow redesign: what work changes, who owns it, and which handoffs disappear or change?
3. Agent architecture: which tasks are assisted, delegated, automated, or kept human-only?
4. Control model: what requires human validation, audit trails, data permissions, rollback, or compliance review?
5. Adoption system: what incentives, training, rituals, and manager behaviors make the new workflow stick?

Do not let the answer become "deploy better models" unless model capability is clearly the binding constraint.

## Workflow

1. Frame the ambition.
   - State the target business outcome.
   - Define the unit of value: cost, revenue, throughput, cycle time, quality, risk, customer experience, or capacity.
   - Identify the executive owner.

2. Map the workflow.
   - Show current process steps, decision points, systems, data inputs, and exception paths.
   - Mark where AI assists, recommends, drafts, decides, executes, or monitors.
   - Separate task automation from operating-model change.

3. Build a use-case portfolio.
   - Score use cases by value pool, feasibility, data readiness, risk, adoption friction, and time-to-impact.
   - Label each use case as pilot, scale, stop, or redesign.
   - Prefer fewer high-value workflow bets over many disconnected demos.

4. Design the control model.
   - Define human validation points.
   - Define allowed data, tool permissions, escalation paths, and audit logs.
   - Distinguish reversible low-risk tasks from irreversible high-risk decisions.

5. Create the transformation office.
   - Define workstreams: value, workflow, technology/data, risk, change/adoption, and capability building.
   - Set cadence: weekly value review, fortnightly risk review, monthly executive steering.
   - Use a benefits tracker tied to operational metrics, not only usage metrics.

6. Produce the executive output.
   - Situation: why value is not scaling today.
   - Recommendation: 2-4 moves that change the system.
   - Roadmap: 30 / 60 / 90 days and 6-month scale path.
   - Governance: owners, decision rights, controls, metrics.
   - Open questions: data, risk, funding, adoption, and operating-model dependencies.

## Use-Case Scoring

Use a 1-5 score for each dimension:

| Dimension | What to test |
| --- | --- |
| Value pool | Material P&L, risk, speed, quality, or capacity impact |
| Workflow leverage | Removes handoffs, rework, wait time, or decision latency |
| Feasibility | Data access, integration complexity, model/tool maturity |
| Risk | Regulatory, customer, brand, safety, security, or operational exposure |
| Adoption | Manager incentives, user trust, training, and change burden |
| Time-to-impact | Can show measurable progress in 90 days |

Recommended classification:

- Scale now: high value, manageable risk, clear owner, adoption path exists.
- Redesign first: high value but workflow ownership or governance is unclear.
- Pilot narrowly: uncertain value or feasibility, but learning is important.
- Stop: weak value, high risk, or no credible path to adoption.

## Output Templates

### Executive Diagnosis

```markdown
## Situation
<Where the AI effort stands and why value is not scaling>

## Root Causes
1. <Workflow / ownership / data / governance / adoption issue>
2. <...>

## Recommendation
<One clear transformation move or sequence>

## 30 / 60 / 90 Day Plan
- 30 days:
- 60 days:
- 90 days:

## Governance
- Executive owner:
- Value owner:
- Risk owner:
- Workflow owners:
- Review cadence:

## Metrics
- Value:
- Adoption:
- Quality:
- Risk:
```

### Transformation Office Workplan

```markdown
| Workstream | Owner | 30-day deliverable | 90-day deliverable | Metric |
| --- | --- | --- | --- | --- |
| Value |  |  |  |  |
| Workflow redesign |  |  |  |  |
| Data and platforms |  |  |  |  |
| Risk and governance |  |  |  |  |
| Adoption and capability |  |  |  |  |
```

## Guardrails

- Do not imply AI value has been achieved when only usage, pilots, or demos exist.
- Do not recommend broad rollout without workflow ownership, human validation rules, and risk controls.
- Do not treat governance as a blocker only; use it as the design system that lets scaling happen.
- If claims depend on current market data, tell the user what should be verified from primary sources.
