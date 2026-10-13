---
name: designing-hitl-workflows
version: "1.0.0"
description: >
  Designs human-in-the-loop (HITL) checkpoints for AI agent workflows —
  deciding where to pause for human approval, structuring the approval
  interface, handling timeouts and non-responses, and building escalation
  paths from automated to human. Covers implementation patterns for n8n
  wait nodes, Claude API stop sequences, and Base44 approval queue panels.
  Activates when designing agents that need human oversight, building
  approval workflows, adding checkpoints to autonomous processes, deciding
  what actions require human sign-off, structuring escalation from AI to
  human, or building trustworthy agents for client delivery. Also triggers
  on: pause before action, approval queue, human approval, agent oversight,
  require confirmation, HITL, human review, escalation workflow, client
  agent trust, consequential action, irreversible action.
---

# HITL Workflow Design

The purpose of HITL is not to slow down automation — it's to build trust
in automation by making the right actions safe to delegate and keeping
humans in control of the actions that aren't.

An agent that always asks for approval isn't autonomous. An agent that
never asks isn't trustworthy for consequential work. HITL is the design
discipline that determines which is which.

---

## Decision Tree

```
What are you building?
  │
  ├─ Where should I put checkpoints in this workflow?
  │    → Section 1: Checkpoint Placement Framework
  │
  ├─ What should the approval interface look like?
  │    → Section 2: Approval Interface Patterns
  │
  ├─ What happens if the human doesn't respond in time?
  │    → Section 3: Timeout and Escalation Handling
  │
  └─ I'm implementing HITL in n8n / Claude API / Base44
       → references/hitl-patterns.md (implementation patterns)
```

### Is HITL required here?

Run this gate on each action the agent can take:

```
Is the action irreversible OR high-consequence OR affects a non-consenting third party?
  ├─ YES → HITL checkpoint REQUIRED (Section 1: "always checkpoint")
  └─ NO  → Is it a high-volume batch whose aggregate undo cost is high?
            ├─ YES → HITL checkpoint REQUIRED (batch approval)
            └─ NO  → No checkpoint; log and monitor, or automate freely
```

---

## Section 1: Checkpoint Placement Framework

Place checkpoints based on two dimensions: **reversibility** and
**consequence**.

```
                    HIGH CONSEQUENCE
                           │
         CHECKPOINT        │    ALWAYS CHECKPOINT
         if high volume    │    (mandatory human review)
                           │
LOW ─────────────────────────────────────────── HIGH
REVERSIBILITY             │                  REVERSIBILITY
                           │
         AUTOMATE          │    LOG AND MONITOR
         freely            │    (audit trail, no pause)
                           │
                    LOW CONSEQUENCE
```

**Always checkpoint** (high consequence, low reversibility):
- Sending emails to external clients on behalf of a human
- Creating or modifying contracts, invoices, or financial records
- Publishing content to a live site or social channel
- Deleting records, files, or data
- Committing code to a protected branch
- Any action affecting a third party who didn't consent to automation

**Checkpoint if high volume** (low consequence, but many at once):
- Batch operations: tagging 500 contacts, updating 100 records
- Even if each action is individually reversible, the aggregate effort
  to undo justifies a checkpoint

**Log and monitor** (high reversibility, low consequence):
- Internal drafts, staging changes, read operations
- Classification, summarization, analysis without side effects

**Automate freely** (low consequence, fully reversible):
- Formatting, categorizing, enriching data
- Generating options for human selection
- Any operation that produces output without acting on it

### The "surprised" test

Before finalizing checkpoint placement: would a reasonable client be
surprised to learn this action happened automatically without their
knowledge? If yes: add a checkpoint.

---

## Section 2: Approval Interface Patterns

### Required output template — minimum viable approval message

Every approval request MUST answer:
1. **What action is about to happen?** (specific, not "send email")
2. **What is the target?** (who/what will be affected)
3. **Why is the agent doing this?** (one-sentence reasoning)
4. **What are the options?** (Approve / Reject / Modify)
5. **What happens if no response?** (default behavior on timeout)

**Template:**

```
🔔 Approval Required

Action:  Send proposal email to Marcus Webb (marcus@acmecorp.com)
Reason:  Discovery call completed — agent generated follow-up proposal
         based on call notes. Budget: $8,500, SOW attached.

[Approve] [Reject] [Edit before sending]

No response in 4 hours → action will be paused, not sent.
```

### What to avoid

- Vague summaries ("Agent wants to proceed") — never acceptable
- Binary approve/reject without a modify path for consequential actions
- Defaulting to approval on timeout (see Section 3)
- Approval requests to Slack/email without a direct action link
- Multiple pending approvals in one message thread — each request must be
  its own isolated message with its own action buttons

---

## Section 3: Timeout and Escalation Handling

**Default on timeout: pause, never proceed.**

An agent that proceeds without approval when the human doesn't respond is
not a HITL system — it's an automated system with a courtesy notice. The
default on timeout must be to pause the workflow and hold state.

### Timeout ladder

```
T+0:00  → Approval request sent (primary channel: Slack DM or email)
T+1:00  → Reminder with escalating urgency language
T+4:00  → Escalation to secondary contact (if defined)
T+24:00 → Workflow paused, task queued for manual review
T+72:00 → Task expires, logged as "requires re-initiation"
```

Adjust timeframes to workflow urgency. A client-facing proposal can wait
24 hours. A time-sensitive booking might need 30 minutes.

### Escalation path configuration

Every HITL workflow should define:
```yaml
primary_approver: [EMAIL]
secondary_approver: [backup contact or team channel]
timeout_minutes: 240
on_timeout: pause  # never: auto-approve
escalation_message: "Action pending approval for 4 hours — needs review"
```

---

## Implementation Patterns

Platform-specific implementation — n8n Wait nodes, Claude API tool-based
HITL / stop sequences, and the Base44 approval queue panel — lives in
**[references/hitl-patterns.md](references/hitl-patterns.md)**. Place the
checkpoints here (Sections 1–3), then wire them up there.

---

## Self-Verification

- [ ] Every checkpoint placement justified by the reversibility/consequence matrix
- [ ] Every approval message answers all 5 required questions
- [ ] Timeout default is pause (never auto-approve)
- [ ] Escalation ladder defined for every HITL workflow
- [ ] "Surprised" test passed for all un-checkpointed consequential actions

---

## CLAIMS
- Defaulting to auto-approve on timeout defeats the purpose of HITL and
  creates liability for the agent operator — pause is always the correct default
- Binary approve/reject without a modify path leads to approval fatigue;
  reviewers begin approving blindly when they can't easily correct

## COUNTEREXAMPLE
- For very high-frequency, low-stakes operations (tagging 1000 newsletter
  subscribers), per-item HITL is impractical; batch approval with sampling
  review is more appropriate

## CONTRADICTIONS
- Full HITL on every consequential action conflicts with automation ROI
  for high-volume workflows; the resolution is batching and sampling,
  not eliminating checkpoints
