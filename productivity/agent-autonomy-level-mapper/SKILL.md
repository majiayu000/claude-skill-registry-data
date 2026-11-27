---
name: agent-autonomy-level-mapper
description: "Produces a per-task autonomy map that assigns each agent action one of five levels - suggest, draft, act-with-approval, act-and-report, or act-silently - using a stakes x reversibility x confidence scoring matrix, plus an approval-gate specification and promotion criteria. Use when deciding how much an Artificial Intelligence (AI) agent should do on its own; designing permissions for an agent with tool access; debating whether an action needs human approval; or planning how to expand agent autonomy over time."
---

# Agent Autonomy Level Mapper

> Autonomy is not a product-wide setting. It is a decision made per action, and it should be earned.

## What this skill is

A decision workflow that breaks an agent's job into discrete actions and assigns each one an autonomy level from a five-level ladder. Each action is scored on stakes, reversibility, and the agent's measured confidence, and the score maps to a level with a matching approval-gate design. The output is an autonomy map product, design, engineering, and risk teams can agree on and revisit as the agent proves itself.

## What it solves

- One global "autonomous mode" toggle that is too risky for some actions and too timid for others
- Approval prompts on trivial actions that train users to click "Approve" without reading
- Irreversible actions (sending, paying, deleting) running without a gate
- Autonomy decisions made on demo confidence rather than measured accuracy
- No defined path for an agent to earn more autonomy, or to lose it after incidents

## When to invoke

- Designing a new agent that can call tools, write data, or contact people
- Stakeholders disagree on whether an action needs human approval
- Users complain about too many confirmations, or about surprises
- Expanding an assistant from suggesting to acting
- Post-incident review of an agent action that should have been gated

## Phase 1: Decompose the job into actions

List every discrete action the agent could take. Split compound actions: "Process refund" becomes *look up order*, *calculate amount*, *draft customer message*, *issue refund*, *send message*.

| Action | Object affected | Who sees the effect | Tool or system |
|--------|-----------------|---------------------|----------------|
| Issue refund | Customer payment | Customer, finance | Billing system |

Read-only actions (search, summarize, look up) still go on the list; they are usually the first candidates for silent autonomy.

## Phase 2: Score each action

Score 1 (low) to 5 (high) on each axis:

| Axis | 1 | 3 | 5 |
|------|---|---|---|
| Stakes (S) | Cosmetic, internal, easily ignored | Visible to others, moderate cost if wrong | Financial, legal, safety, or reputational harm |
| Irreversibility (R) | One-click undo, no side effects | Undo possible with effort or delay | Cannot be undone (sent, paid, deleted, published) |
| Confidence gap (C) | Measured accuracy at or above 98 percent on this action | 85-97 percent | Below 85 percent, or not yet measured |

Confidence must come from evaluation data on this action type, not from the model's self-reported certainty. Unmeasured equals 5.

```
Autonomy risk = S x R + 2 x C
Range: 3 to 35
```

Multiplying stakes by irreversibility reflects that a high-stakes action with a reliable undo is far safer than one without.

## Phase 3: Map risk to autonomy level

| Risk score | Level | Agent behavior | User experience |
|-----------:|-------|----------------|-----------------|
| 3-7 | L5 Act silently | Performs the action, logs it | Visible only in history |
| 8-12 | L4 Act and report | Performs, then notifies with undo | Summary with undo window |
| 13-19 | L3 Act with approval | Prepares the action, waits for confirm | Approval card with diff and consequences |
| 20-26 | L2 Draft | Produces a draft the user must edit or send | Editable draft, user executes |
| 27-35 | L1 Suggest | Recommends options, takes no action | Suggestions the user can ignore |

Override rules, applied after scoring:
- Any action with R = 5 (cannot be undone) is never placed above L3, regardless of confidence
- Actions affecting people outside the organization are capped at L4
- Regulatory or contractual requirements override the score in either direction
- If a user explicitly asks for an action in the moment, the agent may move up one level for that instance only

## Phase 4: Specify the approval gates

For every L3 action, and every L4 undo window, define the gate:

| Element | Specification |
|---------|---------------|
| Trigger | What state causes the gate to appear |
| Content | What will happen, to whom, and the exact values (amount, recipients, records) |
| Diff | Before and after for edits; full preview for sends |
| Consequence line | One sentence on what cannot be undone |
| Options | Approve, edit, reject with reason, always-allow-for-this-type (if permitted) |
| Timeout behavior | What happens if the user does not respond (default: do nothing) |
| Batch rule | When multiple approvals may be combined into one review |

Undo windows for L4: 5-30 seconds for messages, up to 24 hours for reversible data changes. Name the window length in the notification.

## Phase 5: Define promotion and demotion criteria

Autonomy is earned with evidence. For each action, set the rule to move one level:

| Direction | Criteria (example) |
|-----------|--------------------|
| Promote | 200+ instances at current level, approval-without-edit rate above 95 percent, zero Severity 1 incidents |
| Demote | Any Severity 1 incident, or edit-before-approve rate above 20 percent over 2 weeks |
| User override | Users may lower autonomy for themselves at any time; raising it requires the action to be eligible |

## Output

- Action inventory with scope and affected parties
- Scoring table (S, R, C, risk score) per action
- Autonomy map: each action assigned L1-L5 with override notes
- Approval-gate specification for every L3 and L4 action
- Promotion and demotion criteria with the metrics to instrument
- Open questions for risk, legal, or policy review

## Operating rules

**Always**
- Score actions individually, never the agent as a whole
- Use measured accuracy for the confidence axis; treat unmeasured as lowest confidence
- Show exact values and recipients in every approval gate
- Default to doing nothing when an approval times out
- Let users reduce autonomy for themselves without friction

**Never**
- Let model self-reported confidence substitute for evaluation data
- Place an irreversible external action at L5
- Gate trivial actions just to appear safe; it creates approval fatigue
- Promote autonomy without a defined metric and threshold
- Ship act-and-report without a working undo
