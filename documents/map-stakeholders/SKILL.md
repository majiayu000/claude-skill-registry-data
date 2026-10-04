---
name: map-stakeholders
description: Map stakeholders for a project or decision (who decides, influences, or can block, and what each cares about) with a power/interest grid, RACI, and engagement plan. Use when starting an initiative, before a contentious decision, or when alignment keeps breaking down.
---

# Map Stakeholders

Make influence explicit, then turn it into a schedule of conversations.

## Reasoning Framework

Projects stall on people more often than on plans. Decision makers aren't consulted early, a quiet gatekeeper (security, legal, finance) surfaces late, or two executives want different outcomes and nobody noticed. A stakeholder map names who decides, who influences, and who can block, and it records what each person cares about in their own terms. An engagement plan then makes sure the important conversations happen before the meeting where the decision is made.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Stakeholder map | Markdown: stakeholder table, power/interest grid, RACI, engagement plan | The PM (private working document) |

The map contains candid assessments of people. Treat it as private.

## When to Use

- Kicking off a cross-team initiative
- Preparing for a decision that some people will resist
- A project keeps getting reopened, escalated, or quietly blocked
- A new PM ramping up on an org

## When NOT to Use

- Asking for one decision from one person: use `decision-brief`
- Launch approvals for a release: use `launch-checklist` (it has a sign-off table)

## Inputs

1. **The initiative** and the 2–5 key decisions or milestones ahead.
2. **Known stakeholders**: names or roles, and their teams.
3. **Known positions and history**: past objections, commitments, politics you're aware of.
4. **Your relationships** with each person (optional).
5. **Names or roles?** Ask which the user prefers in the document.

## Steps

1. **Scope it**: the initiative, its goal, and the key decisions it needs.
2. **List stakeholders by category** so nobody is forgotten:
   - **Decision makers**: approve scope, budget, or launch.
   - **Influencers**: people decision makers listen to (architects, senior ICs, peers).
   - **Implementers**: teams doing the work or carrying dependencies.
   - **Impacted**: users, support, sales, operations.
   - **Gatekeepers**: security, privacy, legal, finance, platform owners. These are the most often forgotten.
3. **Profile each one**: role, what they care about (goals, metrics, worries), current stance (champion, supporter, neutral, skeptic, blocker), power (H/M/L), interest (H/M/L), and what you need from them.
4. **Place them on the grid:**

   | | Low interest | High interest |
   |---|---|---|
   | **High power** | Keep satisfied | Manage closely |
   | **Low power** | Monitor | Keep informed |

5. **Write a RACI for each key decision**: Responsible, Accountable, Consulted, Informed. Add S (Supportive) for RASCI if helpful. Each decision gets exactly one Accountable.
6. **Plan engagement** for everyone in Manage closely and Keep satisfied: objective, the message framed in their terms, channel (1:1, doc review, steering meeting), cadence, owner, and next action with a date. Pre-wire decisions with 1:1s before the group meeting.
7. **Flag risks**: conflicting goals between decision makers, single points of failure, unknown stances. Add a mitigation for each.
8. **Set a refresh date.** Update after major meetings or when a stance changes.

## Template

```markdown
# Stakeholder Map: [Initiative]
Goal: [..] · Key decisions: [1..] · Updated: [YYYY-MM-DD]

## Stakeholders
| Person/role | Category | Cares about | Stance | Power | Interest | Need from them |
|---|---|---|---|---|---|---|

## Grid
(2x2 table: who sits in each quadrant)

## RACI
| Decision | R | A | C | I |
|---|---|---|---|---|

## Engagement plan
| Stakeholder | Objective | Message (their terms) | Channel | Cadence | Next action (date) |
|---|---|---|---|---|---|

## Risks
| Risk | Mitigation | Owner |
|---|---|---|
```

## Examples

- "I'm starting a pricing change that touches sales, finance, and support." Surface finance and legal as gatekeepers, name one Accountable for the price decision, and schedule 1:1s with the sales lead before the steering meeting.
- "Our platform migration keeps getting reopened." Find two decision makers with conflicting goals (cost versus reliability) and plan a joint decision session with explicit criteria.

## Guardrails

- Private by default. Don't put this map in shared drives or commit it to this public repo.
- Describe interests and observed behavior, not personalities. No speculation about personal lives.
- Use roles instead of names when the user prefers, or when the document might travel.
- Exactly one Accountable per decision.
- Stances are hypotheses until confirmed in conversation. Mark them "assumed" until then.

## Related Skills

- `decision-brief`: the pre-wired decision meeting
- `gtm-plan` and `launch-checklist`: launch owners and approvers
- `storytelling-for-impact`: framing the message for each audience
- `library/lenny-podcast/lenny-stakeholder-alignment/SKILL.md` and `library/lenny-podcast/lenny-managing-up/SKILL.md`: deeper playbooks
