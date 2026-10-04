---
name: launch-checklist
description: Stage-gate launch readiness review for Alpha, Closed Beta, Open Beta, and GA. Builds a checklist by function with owners, evidence, and sign-offs, ending in go / no-go. Use before promoting a release or when asked "are we ready to launch?" For launch strategy and messaging, use gtm-plan.
---

# Launch Checklist

Decide whether a release is ready for its next stage, with evidence instead of vibes.

## Reasoning Framework

Launch readiness is a gate, not a feeling. Every item needs an owner and evidence (a link, a test run, a recorded sign-off), and every stage has a quality bar. The checklist grows with the stage: Alpha needs a fraction of what GA needs. "No-go" is a legitimate, useful answer. The job is to make the risk visible, not to get to yes.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Readiness checklist | Markdown, from `references/checklist-template.md` | Launch DRI, approvers |
| Recommendation | Go / Go with conditions / No-go, with blockers and owners | Decision meeting |

## When to Use

- Before a stage promotion (Alpha → Closed Beta → Open Beta → GA)
- A go/no-go meeting is coming up
- Someone asks "are we ready?" and nobody can answer with evidence

## When NOT to Use

- Planning positioning, channels, and enablement: use `gtm-plan`
- Writing the release notes: use `create-release-notes`

## Inputs

1. **What is launching** and a link to the PRD.
2. **Target stage and date.**
3. **Open bug counts** by priority (P0/P1/P2), or where to find them.
4. **Evidence links**: tests, dashboards, docs, runbooks, support plan, reviews.
5. **Approvers** per function (see `map-stakeholders` if unclear).

## Steps

1. **Confirm the stage bar.** Read `references/release-stages.md` for the target stage's access level, quality bar, and promotion criteria.
2. **Build the checklist.** Copy `references/checklist-template.md` and keep every item tagged with the target stage or an earlier one. Drop items that don't apply, and record the reason as N/A.
3. **Collect evidence.** Mark each item ✅ (with a link), ⚠️ (plan, owner, date), ❌ (blocked), or N/A (reason). Ask for anything missing. Never assume an item is done.
4. **Check the quality bar.** Compare open P0/P1/P2 counts with the stage's bar. Any P0 is an automatic no-go.
5. **List blockers and risks** with impact, plan, owner, and due date.
6. **Recommend.** Go, Go with conditions (each condition has an owner and deadline), or No-go (blockers plus the earliest re-review date). Explain the call in two or three sentences.
7. **Record sign-offs** as the approvers actually give them. Leave a row blank until the person has decided.
8. **Plan post-launch checks** at +1 day and +1 week, and schedule a retro.

## Examples

- "Promote smart filters to Open Beta on Friday; here's the export of open bugs." Build the checklist through the OB items, find 2 open P2s against a zero-P2 bar, and recommend go with conditions only if approvers accept those P2s in writing. Otherwise no-go.
- "Are we ready for GA?" Ask for evidence links, fill the checklist, and flag missing security sign-off and untrained support as blockers.

## Guardrails

- No evidence, no ✅.
- The stage bar is fixed. An exception must be accepted explicitly by the approvers and recorded in the checklist.
- Don't record approvals the user hasn't confirmed.
- Keep internal system names and customer names out of anything committed to this public repo.

## Related Skills

- `gtm-plan`: the launch plan this checklist gates
- `create-release-notes`: GA release notes
- `decision-brief`: run the go/no-go decision meeting
- `map-stakeholders`: find the right approvers
- `library/lenny-podcast/lenny-shipping-products/SKILL.md`: shipping discipline
