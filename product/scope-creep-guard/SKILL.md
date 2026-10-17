---
name: scope-creep-guard
description: Reviews proposed features, requirements, tasks, or enhancements against an agreed project goal and classifies each as required, justified, deferred, or rejected. Use when a user asks whether new work belongs in scope, wants to prevent scope creep, needs an evidence-based change-control review, or must decide what to include now, revisit later, or decline.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: review
  audience: product-owners-and-project-maintainers
  tags:
    - scope-control
    - change-control
    - project-goals
    - prioritization
    - decision-making
  status: draft
  side_effects: none
---

# Scope Creep Guard

## Purpose

Review proposed additions against the project's agreed goal, commitments, constraints, and success criteria. Classify every addition as required, justified, deferred, or rejected, with enough evidence to make the scope decision understandable and reversible.

## When to use this skill

Use this skill when:

- New features, requirements, tasks, integrations, platforms, or polish are proposed after a project goal or scope exists.
- A user asks whether an addition belongs in the current project, release, milestone, or task.
- A backlog, review discussion, or stakeholder request is expanding delivery scope.
- A team needs a consistent change-control decision with explicit reasons and consequences.
- The user asks to identify, prevent, or resolve scope creep.

Do not use this skill when:

- The project goal, intended users, or desired outcome is too vague to serve as a decision baseline; clarify the brief first.
- The user needs to define an MVP from scratch; use `mvp-scope-planner`.
- The user wants candidates ranked within an already-approved scope; use `feature-priority-planner`.
- The main task is estimating cost, scheduling work, or implementing an approved addition.

## Inputs to inspect

Start with the smallest sources that establish the decision baseline:

- Project brief, issue, roadmap, milestone, task, or acceptance criteria.
- Explicit goal, target users, desired outcome, success measures, and definition of done.
- In-scope items, non-goals, exclusions, constraints, deadline, budget, and quality requirements.
- The proposed additions and the stated problem or evidence behind each one.
- Existing commitments, dependencies, contracts, standards, or defects that may make an addition mandatory.
- Relevant repository evidence when it confirms current behavior, architecture, or prior decisions.

Do not treat an undocumented preference as an agreed project goal. Label inferred goals and constraints as assumptions.

## Classification rules

Use exactly one primary classification for each proposal:

| Classification | Apply when | Decision effect |
|---|---|---|
| `required` | The addition is necessary to achieve the stated goal, meet acceptance criteria, preserve a core user journey, satisfy a binding dependency, fix a blocking defect, or meet a non-negotiable accessibility, privacy, security, legal, or compatibility obligation. | Include in the current scope, or explicitly revise the goal if it cannot be delivered. |
| `justified` | The addition is not strictly necessary, but evidence shows a proportionate improvement to the stated outcome or a material reduction in delivery, adoption, operational, or maintenance risk. Its cost and tradeoffs are acceptable within current constraints. | Include only with an explicit scope decision and acknowledgment of the tradeoff. |
| `deferred` | The addition may be valuable, but is not necessary now, lacks enough evidence, depends on later learning, or would displace more important work under current constraints. | Record a revisit trigger, required evidence, or target phase; do not silently carry it in current scope. |
| `rejected` | The addition conflicts with the project goal or non-goals, duplicates existing capability, creates disproportionate cost or risk, serves no identified user outcome, or belongs to a different project. | Exclude it and state what evidence or goal change, if any, could justify reconsideration. |

Classification is not prioritization by another name. A low-priority mandatory requirement remains `required`; an attractive idea with no current evidence is usually `deferred`; an idea should be `rejected` only when there is a reason to exclude it, not merely because capacity is tight.

## Workflow

1. **Establish the decision baseline.** State the project goal, target users, desired outcome, current scope, non-goals, success criteria, constraints, and planning horizon. Separate explicit evidence from assumptions. If the baseline cannot support a defensible review, identify the minimum decisions needed before classification.
2. **Normalize the proposals.** Rewrite each addition as a concrete outcome or obligation. Split bundled requests when their components could receive different classifications. Merge true duplicates without losing attribution.
3. **Identify the rationale.** For each proposal, name the user, problem, obligation, dependency, risk, or evidence offered in support. Do not accept “nice to have,” stakeholder seniority, sunk effort, or implementation novelty as sufficient rationale.
4. **Test goal alignment.** Ask whether the proposal directly enables the desired outcome, merely improves it, is unrelated, or conflicts with a stated non-goal. Cite the goal, criterion, constraint, or repository evidence used.
5. **Test necessity.** Consider the consequence of omission. Mark an item `required` only when omission prevents success, violates a binding condition, breaks an essential journey, or leaves unacceptable risk. Do not defer baseline accessibility, privacy, security, or correctness obligations as polish.
6. **Test proportionality.** For non-required additions, compare expected outcome or risk reduction with cost, complexity, dependencies, schedule pressure, operational burden, and future maintenance. Use ranges or qualitative judgments when precise estimates are unavailable.
7. **Classify each proposal.** Assign one primary classification using the rules above. Include confidence and distinguish missing evidence from negative evidence. Resolve classification disagreements by exposing which baseline assumption or tradeoff differs.
8. **Define the decision consequence.** For `justified` items, state what current work, time, or capacity absorbs the addition. For `deferred` items, name a concrete revisit trigger or evidence need. For `rejected` items, state the conflict and whether any plausible goal change would reopen the decision.
9. **Check the portfolio effect.** Review the additions together. Several individually small justified items may collectively violate the deadline, complexity budget, or project coherence. Reclassify or present scope options when the combined effect changes feasibility.
10. **Return a decision record.** Make unresolved decisions, assumptions, and owners visible. Recommend no file edits or implementation unless the user separately authorizes them.

## Output format

Return:

```md
## Scope baseline

- Goal:
- Target users and outcome:
- Current scope and non-goals:
- Success criteria:
- Constraints and planning horizon:
- Assumptions or missing baseline decisions:

## Classification summary

| Proposal | Classification | Confidence | Goal connection | Key evidence | Decision consequence |
|---|---|---:|---|---|---|

## Decision details

### Proposal name — required | justified | deferred | rejected

- Rationale:
- Consequence of omission:
- Cost, risk, and dependency effect:
- Decision:
- Revisit trigger or reconsideration condition, if applicable:

## Combined scope effect

- Capacity or schedule effect:
- Complexity and maintenance effect:
- Work displaced or goal change required:

## Open decisions

- Decision, owner, and evidence needed.
```

If the baseline is insufficient, return a provisional classification only where evidence supports one and mark the rest `unclassified` pending named decisions. `Unclassified` is a temporary review state, not a fifth outcome.

## Quality bar

The task is complete only when:

- Every proposal is normalized and classified, or explicitly left provisionally unclassified because the baseline is inadequate.
- Every classification cites a project goal, success criterion, constraint, obligation, non-goal, user outcome, or concrete repository evidence.
- Required work is distinguished from beneficial optional work.
- Deferred work has a revisit trigger, evidence need, or target phase rather than a vague “later.”
- Rejected work has a clear exclusion reason and is not rejected solely because capacity is currently limited.
- The combined effect of all accepted additions is assessed against current constraints.
- Assumptions, uncertainty, tradeoffs, displaced work, and necessary goal changes are explicit.
- The review does not silently expand the project or implement the additions.

## Edge cases

- If stakeholders disagree about the goal, present classifications under each materially different goal interpretation and identify the decision owner.
- If an addition exposes a missing baseline obligation, classify it `required` and explain why the original scope was incomplete rather than treating it as optional scope creep.
- If a proposal is valuable but too large, do not automatically split it into a token version. Defer it or identify a smaller coherent outcome only when that outcome has independent value.
- If a fixed deadline and required work conflict, state which constraint, deliverable, or goal must change. Do not relabel required work as optional to make the plan appear feasible.
- If evidence is weak, prefer `deferred` with a validation trigger over speculative acceptance or permanent rejection.
- If a previously rejected item is proposed again, review new evidence or a changed goal; do not reopen the decision based only on repetition.

## Related skills

- `project-brief-builder`
- `requirements-gap-finder`
- `mvp-scope-planner`
- `feature-priority-planner`
- `constraint-mapper`
