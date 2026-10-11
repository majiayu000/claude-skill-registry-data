---
name: agent-actions
description: "Use when designing or reviewing Agentforce actions, including Flow actions, Apex invocable actions, prompt-template actions, action naming, input and output contracts, confirmation requirements, and safe error behavior. Triggers: 'agent actions', 'flow action for agent', 'agent invocable action', 'action schema design', 'agent action error handling'. NOT for topic boundary design or general Apex invocable guidance when the main concern is not an agent-facing action contract."
category: agentforce
salesforce-version: "Spring '26+"
well-architected-pillars:
  - Reliability
  - Security
  - Operational Excellence
triggers:
  - "how should I design Agentforce actions"
  - "when should the agent use a flow action versus apex action"
  - "agent action naming and input schema"
  - "destructive agent action needs confirmation"
  - "agent action error handling review"
tags:
  - agentforce
  - agent-actions
  - invocable-actions
  - action-contracts
  - confirmation-patterns
inputs:
  - "which business capabilities the agent must invoke"
  - "whether the action is declarative Flow, Apex, or prompt-template based"
  - "expected inputs, side effects, and confirmation requirements"
outputs:
  - "agent action design recommendation"
  - "action contract and naming review findings"
  - "error-handling and confirmation guidance"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# Agent Actions

Use this skill when the agent already knows the right topic, but still needs a safe and understandable way to do work. Agent actions are the operational boundary between conversational intent and real system side effects. Poor action design leads to vague capabilities, hard-to-recover failures, and agents invoking the wrong tool because names or contracts are ambiguous.

The design goal is simple: a small, well-named action set with stable inputs, predictable outputs, and deliberate confirmation for side effects. Salesforce guidance emphasizes keeping action counts low, using clear names and descriptions, and shaping input types so the agent can select and execute actions reliably. Action design should help the agent understand what the tool does, what data it needs, and when failure should be surfaced to the user versus returned as a structured business result.

Agent actions can be Flow-based, Apex invocable, or prompt-template oriented depending on the task. Flow actions are strong when declarative orchestration is enough. Apex invocable actions are better when service-layer control, strict contracts, or heavier logic matter. Prompt-template actions fit generation tasks, not destructive record mutation. The boundary should be chosen intentionally.

---

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- What exact business task should the action perform, and is it read-only or side-effecting?
- Should the action be declarative Flow, Apex invocable, or prompt-template based?
- What inputs are truly required, and what output shape will help the agent reason about success or failure?
- Does the action need confirmation before mutating data, sending messages, or performing irreversible work?
- What's the expected invocation rate? (An action the agent calls 1000 times/day has different safety concerns than one called 5 times/day.)
- Who is accountable for the business contract this action implements? (Action failures become their incident.)

---

## Core Concepts

### Actions Are Capabilities, Not Conversation Dumps

An action should do one business job clearly. Do not create vague actions like `runProcess` or `handleRequest` that hide several outcomes. The LLM selects actions based on semantic clarity of names + descriptions; "do the thing" descriptions produce "do something random" behavior.

Rule of thumb: if you can't explain what the action does to a business user in one sentence, the action is too broad. Split it.

### Naming And Description Drive Tool Selection

The agent relies on action labels, descriptions, and parameter meaning to choose correctly. Human-readable clarity is part of the runtime contract.

**Naming pattern (recommended):**
- Verb-first: `Create_Case`, `Update_Opportunity_Stage`, `Send_Contract_For_Signature`.
- Object-aware: include the primary sObject in the name.
- Avoid generic verbs: `Process`, `Handle`, `Execute` — too vague for the LLM.
- Specific outcome: `Generate_Quote_PDF` beats `Generate_Document`.

**Description pattern:**
- One sentence on what the action DOES.
- One sentence on when to USE it.
- One sentence on what the action does NOT do (prevents over-selection).

### Stable Input And Output Shapes Improve Reliability

The agent needs narrow, predictable parameters and results. Avoid overloading one action with many loosely related required fields or generic object blobs.

**Input design rules:**
- Prefer typed primitives (Text, Number, Date, Boolean) over generic SObject blobs.
- Mark inputs as `required` only when they're truly required; optional inputs let the agent adapt.
- Provide default values where safe — reduces the cognitive load on action selection.
- Avoid "payload" fields that hide structured data inside a string (can't validate at design time).

**Output design rules:**
- Return structured success/failure flags (`success: boolean`, `errorCode: string`, `message: string`).
- Include the primary identifier of any created/modified record (agent can reference it in the conversation).
- Never throw raw exceptions as the output — wrap in a business-shaped result.

### Confirmation And Error Behavior Need Deliberate Design

Destructive or customer-visible side effects should be confirmation-aware. Failures should return clear business meaning rather than raw stack traces or empty silence.

**Confirmation patterns:**
- **Always-confirm:** every invocation waits for user confirmation (e.g. sending legal contracts).
- **Threshold-confirm:** confirmation triggers above a threshold (e.g. order > $10k).
- **Two-phase:** action returns a preview, user confirms, action is invoked a second time to commit.
- **Agent-declared:** action declares `requiresConfirmation: true` and the agent runtime handles the UX.

**Error patterns:**
- **Recoverable:** action returns `success: false` + error code; agent can retry with different inputs.
- **Unrecoverable:** action returns clear message; agent escalates to human.
- **Policy-blocked:** action returns "not allowed"; agent explains policy to user.

---

## Common Patterns

### Pattern 1: Flow Action For Declarative Orchestration

**When to use:** The task can be modeled as clear declarative steps and the admin team should retain ownership.

**Structure:** Use a narrow Flow boundary (auto-launched flow with explicit input/output variables). Keep inputs explicit and typed. Ensure the output is meaningful enough for the agent to continue or explain a failure. Fault connectors on every element.

**Why not the alternative:** Apex adds complexity when the task is mainly orchestration; admins can maintain the flow without code skills.

### Pattern 2: Apex Invocable Service Action

**When to use:** The action needs reusable service logic, stricter contracts, or finer transaction control.

**Structure:**
```apex
public class CreateCaseForAccount {
    @InvocableMethod(label='Create Case for Account'
        description='Creates a support case attached to a specific Account and returns the Case ID. Use when customer reports an issue; do NOT use for feature requests (those go to a different action).')
    public static List<Result> createCase(List<Request> requests) {
        // ... bulk-safe implementation
    }

    public class Request {
        @InvocableVariable(required=true label='Account ID' description='Salesforce ID of the parent Account')
        public String accountId;
        @InvocableVariable(required=true label='Subject' description='Short description of the issue, plain English')
        public String subject;
        @InvocableVariable(label='Priority' description='Low, Medium, High; defaults to Medium if omitted')
        public String priority;
    }

    public class Result {
        @InvocableVariable public Boolean success;
        @InvocableVariable public String caseId;
        @InvocableVariable public String errorCode;
        @InvocableVariable public String message;
    }
}
```

The `@InvocableVariable` descriptions ARE the LLM's documentation. Write them well.

### Pattern 3: Confirmation-Gated Mutation Action

**When to use:** The action creates, updates, deletes, or externally sends something significant.

**Structure:**
1. Register the action with `requiresConfirmation=true` (where the platform supports it; otherwise via prompt-instruction pattern).
2. The action's description explicitly states "requires user confirmation before execution".
3. Agent prompt guidance reinforces: "for any action that sends contracts, cancels orders, or updates financial fields, require explicit user confirmation".
4. On user decline, action is never invoked; agent explains to user what was NOT done.

### Pattern 4: Prompt-Template Action For Content Generation

**When to use:** The action's job is to generate text/content from record context (e.g. draft email, summarize case, explain quote).

**Structure:** Register a Prompt Template (via Prompt Builder) as an agent action. The prompt template defines inputs (record references) and the model generates the output. DO NOT use prompt-template actions for mutation — they're generation-only.

### Pattern 5: Read-Only Lookup Action

**When to use:** Agent needs to retrieve information before deciding next steps.

**Structure:** Thin invocable method that executes a specific SOQL query. Read-only; no side effects. Fast (sub-second). Returns a structured result the agent can reason over.

Read-only actions should be plentiful; mutation actions should be scarce. The asymmetry is deliberate — agents should READ freely and WRITE only with deliberation.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Declarative orchestration is sufficient | Flow action (Pattern 1) | Lower implementation overhead |
| Service logic or tighter contract control needed | Apex invocable action (Pattern 2) | Better structure and reuse |
| Task is primarily content generation | Prompt-template action (Pattern 4) | Generation boundary is clearer |
| Action mutates records or triggers external side effects | Confirmation-gated (Pattern 3) | Safer execution |
| Action name and schema feel generic | Redesign before release | Agent selection quality depends on clarity |
| Agent needs to retrieve info before deciding | Read-only Apex lookup (Pattern 5) | Fast, safe, composable |
| Action's work exceeds one transaction | Platform Event publish → async processing | Don't block the conversation on long work |

---

## Well-Architected Pillar Mapping

- **Reliability** — action contract stability; predictable error shapes; confirmation discipline. An unreliable action erodes user trust in the agent.
- **Security** — actions execute with the agent's running user context; CRUD/FLS apply. Destructive actions without confirmation = security failure.
- **Operational Excellence** — action count discipline (fewer, clearer actions beat many vague ones); observability of which actions the agent invokes most.

## Review Checklist

- [ ] Each action performs one business capability clearly.
- [ ] Names and descriptions help the agent choose the right tool.
- [ ] Inputs are narrow, typed, and not overloaded with generic payloads.
- [ ] Outputs communicate business success or failure clearly (not raw exceptions).
- [ ] Destructive or external side effects require deliberate confirmation behavior.
- [ ] Total action set is small enough to stay understandable (< 20 actions per agent).
- [ ] Read-only lookup actions are separated from mutation actions.
- [ ] `@InvocableVariable` descriptions are informative (LLM reads them).
- [ ] Apex invocable actions are bulk-safe (`List<T>` signature).
- [ ] Fault handling designed for each action (per `flow/fault-handling` if Flow-based).


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the business task, action type, side-effect profile, and invocation rate
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above; name and shape the contract deliberately
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

1. **A technically valid invocable action can still be a poor agent action** — generic names and overloaded schemas hurt tool selection.
2. **Prompt-template actions are not the right tool for transactional mutation** — generation and side effects should not be blurred.
3. **Too many actions reduce action selection quality** — a larger tool belt is not always a better one; 20 is a soft upper bound.
4. **Raw exceptions are weak agent outputs** — business-safe result structures help the agent explain failure and recover.
5. **Apex invocable actions share the agent session's governor budget** — CPU + SOQL + DML all contend. A heavy action exhausts the budget for subsequent actions in the same session.
6. **`@InvocableVariable(label=...)` is what the agent sees, not the Apex variable name** — use clear labels.
7. **Flow-backed actions can be deactivated out from under the agent** — deploy gates should include "agent-referenced Flow activation" verification.
8. **Managed-package invocable actions may have opaque contracts** — the agent can call them but may not understand the outputs; wrap in a clarifying Apex invocable.
9. **Actions in Guest-user Agentforce contexts bypass user-specific security** — explicitly audit Guest-invoked actions.
10. **Running-user context is the agent's assigned User record** — not the end-customer interacting with the agent. Sharing implications differ from typical UI flows.

## Proactive Triggers

Surface these WITHOUT being asked:

- **Action with generic verb (`Process`, `Handle`, `Execute`)** → Flag as High. LLM can't select confidently.
- **Mutation action with no confirmation design** → Flag as Critical. User-visible side-effect without a brake.
- **Raw exception in action output** → Flag as High. Agent can't explain the failure.
- **Action set > 25 per agent** → Flag as Medium. Tool-belt bloat; consolidate.
- **InvocableVariable description empty or trivial** → Flag as High. LLM documentation missing.
- **Apex action not bulk-safe (single-instance signature)** → Flag as High. Scale risk.
- **Mutation action in a Guest-user agent without security review** → Flag as Critical.
- **Action name duplicates another action's semantics** → Flag as High. Selection ambiguity.

## Output Artifacts

| Artifact | Description |
|---|---|
| Action design review | Findings on naming, schema, confirmation, failure behavior |
| Action boundary recommendation | Flow vs Apex vs prompt-template guidance |
| Contract pattern | Suggested request and response shape for agent-safe execution |
| Confirmation policy | Which actions require confirmation + the UX pattern |
| Action inventory | List of actions per agent with purpose + owner + invocation rate |

## Related Skills

- **agentforce/agent-topic-design** — when the bigger problem is topic boundary and routing.
- **agentforce/einstein-trust-layer** — when the action's data-handling is a Trust Layer concern.
- **agentforce/agentforce-guardrails** — overall guardrail strategy that actions fit into.
- **agentforce/agent-testing-and-evaluation** — how to verify actions behave correctly in agent context.
- **apex/invocable-methods** — when the action contract issue is really a generic Apex boundary question.
- **flow/flow-action-framework** — when the Flow-side of the action contract is the concern.
