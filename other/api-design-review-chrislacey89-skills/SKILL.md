---
name: api-design-review
description: "Invoked helper skill for higher-risk API contract decisions, usually called from /research or /write-a-prd. Use when the unresolved question is API shape, compatibility, auth, webhook design, or paradigm choice. Not a default top-level workflow step or a substitute for ordinary implementation work."
---

# API Design Review

Use this skill when API complexity is high enough that the normal `/research` or `/write-a-prd` flow needs a focused contract review.

This is an invoked skill, not a default pipeline step. It exists to add rigor only when the cost of an API mistake is unusually high.

## Invocation Position

This is an invoked helper skill. It normally runs from `/research` or `/write-a-prd` rather than as the first entry point for a feature.

Use it when the unresolved question is the API contract itself: paradigm choice, consumer-facing shape, compatibility posture, or auth and webhook model.

Do not use it for ordinary backend implementation work or for non-API module design questions that belong in `/design-an-interface`.

## Invoke This Skill When

Invoke `/api-design-review` only if at least one of these is true:

- a new external or partner-facing API is being introduced
- an existing request or response contract is changing
- OAuth, scopes, token model, or webhook verification is involved
- there is real uncertainty about paradigm selection (REST, RPC, GraphQL, WebHooks, WebSockets)

You may also invoke it for internal APIs with multiple independent consumers when a contract mistake would create broad cleanup cost.

Do not invoke it for ordinary backend changes that merely happen to call an API without changing the contract shape.

## Goals

Produce a lightweight design review that answers:

- What developer problem is this API solving?
- Who are the consumers and what operations do they need?
- What paradigm best fits the operation inventory?
- What is the minimum viable auth and scope design?
- Is the proposed change additive or breaking?
- What contract details must be fixed before implementation starts?

## Workflow

### 1. Establish the API surface under review

Summarize the proposed API work in a few lines:

- new API vs change to existing API
- internal vs external consumers
- synchronous request/response vs event/webhook delivery
- auth model involved
- known compatibility constraints

If the work is not actually API-shaping, stop and return control to the caller.

### 2. Write the minimum spec-first inputs

Capture these before judging the design:

- **Problem statement** — what developer pain or capability gap exists?
- **Impact statement** — what outcome does solving it enable?
- **Developer consumers** — who integrates with this and what do they care about?
- **Operation inventory** — list the concrete operations the API must support

If these are missing, ask the caller to supply them or derive them from the existing pitch/research context before proceeding.

### 3. Review the design

Evaluate the proposal across these dimensions:

- **Paradigm fit** — does REST/RPC/GraphQL/WebHooks match the operation inventory?
- **Contract shape** — are inputs, outputs, required/optional fields, and defaults explicit?
- **Error design** — are there machine-readable codes plus human-readable messages?
- **Security model** — are scopes, token handling, or webhook verification conservative and clear?
- **Compatibility** — is the change additive, or does it risk breaking existing consumers?
- **Rejected alternatives** — what was considered and why was it rejected?

Prefer additive change over mutation of existing behavior. If a contract must evolve incompatibly, say so explicitly.

### 4. Produce the review result

Return a short memo with these sections:

#### API Design Verdict

- **Proceed** — the contract is shaped enough to enter implementation
- **Proceed with constraints** — acceptable, but only if listed constraints are preserved
- **Revise before implementation** — unresolved design issues remain

#### Must-lock decisions

List the contract decisions that must be fixed before implementation starts.

#### Compatibility classification

State one of:

- **Additive**
- **Potentially breaking**
- **Breaking**

Explain why.

#### Key risks

List the 2-5 highest-risk failure modes.

#### Recommendation

Give the simplest viable recommendation that fits the constraints.

## Output guidance

Keep the output concise. This is a focused design review, not a full PRD or a full research report.

Good outputs help `/research` or `/write-a-prd` sharpen the contract before implementation. Bad outputs restate generic API best practices without deciding anything.

## Handoff

- **Expected input:** API-shaped uncertainty from `/research` or `/write-a-prd`
- **Produces:** a concise verdict, compatibility classification, must-lock decisions, and key risks
- **Returns control to:** the calling skill so shaping can continue with a firmer contract
- **Typical next step:** back to `/research` or `/write-a-prd`, then onward through the normal pipeline
