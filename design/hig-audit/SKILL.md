---
name: hig-audit
description: "Inspect an existing product and produce evidence-backed, prioritized UI/UX findings before recommending or implementing changes."
---

# Diagnose the existing experience

Follow the [root contract](../../SKILL.md). Read the [coverage map](../../references/coverage-map.md) and [finding template](../../templates/finding.md). Apple context: HIG-003 and APPLE-006 in the [source register](../../references/source-register.md). The audit method below is WORKFLOW.

## Inputs and access levels

Accept a repository, running product, prototype, screenshots, analytics, research, or a combination. Declare what each supports. Code can reveal handlers and state ownership; runtime checks can reveal behavior; screenshots can reveal visible presentation. None alone establishes every property.

If only screenshots are available, annotate visible issues and testable hypotheses. Do not claim the absence of keyboard support, hidden settings, or error recovery without inspecting them. If only code is available, identify likely failures and the runtime conditions needed to confirm them.

## Procedure

### A. Establish the product’s jobs

Write the primary user, task, starting condition, intended result, and consequence of failure. Identify roles and permission boundaries. Distinguish frequent operational work from occasional setup. Identify what the product deliberately optimizes for: speed, precision, comparison, learning, creative control, or another documented outcome.

Inventory existing capabilities before recommending removal. Mark business-critical behavior, regulatory or contractual constraints supplied by the project, and established terminology. Do not invent user personas from a color palette or claim a feature is unused without evidence.

### B. Build a screen-and-flow map

For each core journey, map entry point → decision → action → system response → completion/recovery. Include sign-in or permission gates, return navigation, deep links, and resumable work. Record which data must survive each boundary and which component owns it.

Map global navigation, local navigation, contextual actions, status, and content separately. Flag one symbol performing incompatible jobs in different locations. Inventory reusable components and token families so repeated symptoms can be grouped by cause.

### C. Exercise representative conditions

Start with one end-to-end critical task, then the highest-risk adjacent paths. For each sampled flow, try:

- First use and returning use; valid, empty, unusually long, and realistic dense content.
- Success, validation failure, server failure, interrupted request, and recoverable retry.
- Navigation away and back; refresh/relaunch where applicable; session change.
- Narrow and wide windows; enlarged text; keyboard or appropriate alternate input.

Sample intentionally rather than pretending to test every combination. Mark untouched roles, platforms, screens, and states as untested. Use [audit-context.md](../../templates/audit-context.md) to make coverage visible.

### D. Review through five questions

**Understanding:** Can the user identify the purpose, current situation, available choices, and result of the next action?

**Operation:** Can the task be completed with the required input methods without hidden gestures or accidental activation?

**Continuity:** Do selections, drafts, filters, focus, and location survive expected interruptions?

**Recovery:** Can the user understand a failure and get back to useful work without unnecessary repetition or loss?

**Presentation:** Does the hierarchy, density, language, and visual treatment support this task rather than compete with it?

Record positive findings too. A dense comparison table, a deliberate confirmation, or a visible advanced option may be serving the task well. Preserve it unless evidence supports a different treatment.

### E. Convert symptoms into repairable findings

Do not write “improve hierarchy.” Identify what competes with what, the affected task, and how the conflict appears. Do not write “too many clicks” without examining whether the steps prevent errors or preserve context.

Separate the immediate symptom from the likely cause. A missing result might come from filtering, stale state, access restrictions, or a failed request—not poor typography. Identify alternative explanations and a discriminating test.

For each finding, attach stable ID, reproduction, evidence, scope, confidence, priority, smallest repair, risk, and acceptance test. Group repeated manifestations under a shared cause while retaining affected locations.

## Output

Produce a concise diagnosis, protected-strengths list, coverage table, prioritized finding ledger, and recommended next slice. Include no more speculative redesign than the evidence supports. Identify which proposed changes need a usability study or product decision rather than a code patch.

## Completion gate

A useful audit answers: what is wrong, for whom, where, why it matters, how we know, what should change, what must not change, and how to verify the repair. If any of those are unknown, label the gap rather than inventing certainty.
