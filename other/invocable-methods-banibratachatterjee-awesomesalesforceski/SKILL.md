---
name: invocable-methods
description: "Use when designing or reviewing Apex actions exposed to Flow or similar orchestration layers via `@InvocableMethod`, especially around wrapper DTOs, bulk-safe list contracts, and error behavior. Triggers: 'InvocableMethod', 'InvocableVariable', 'Flow Apex action', 'bulk-safe invocable', 'Apex action input/output'. NOT for general Flow design without a custom Apex action boundary."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Operational Excellence
  - Reliability
tags:
  - invocablemethod
  - invocablevariable
  - flow-apex-action
  - wrapper-dto
  - bulk-safe
triggers:
  - "how do I write a bulk-safe invocable method"
  - "InvocableVariable wrapper pattern for Flow"
  - "Apex action input and output design"
  - "when should Flow call Apex via InvocableMethod"
  - "invocable method limitations and contracts"
  - "how to call apex from flow"
inputs:
  - "Flow or action use case and expected record volume"
  - "whether the action needs complex request or response fields"
  - "error-handling expectation for the calling automation"
outputs:
  - "invocable method design recommendation"
  - "review findings for contract, bulk safety, and wrapper usage"
  - "Apex action scaffold with request and response DTOs"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when Flow or another orchestration layer needs a custom Apex action and the design must survive real volume, not just one-click demos. The key is respecting the invocable contract: public static entry point, list-oriented inputs and outputs, explicit wrapper fields, and behavior that remains bulk-safe under declarative orchestration.

## Before Starting

- What automation will call this action, and can it invoke the method for many records in one transaction?
- Does the action need simple primitive inputs, or does it need a wrapper request/response contract?
- What should the calling Flow do on partial failures or validation errors?

## Core Concepts

### Invocable Methods Are Boundary Adapters

An invocable method is not the whole business layer. It is the entry point that translates Flow-friendly inputs into the service layer. Keep the annotation boundary small and delegate the actual behavior elsewhere.

### The Contract Is List-Oriented

Invocable methods are designed around list inputs and outputs even when a Flow screen makes the action feel single-record. Bulk-safe design still matters because declarative automation can batch work in ways the first demo does not show.

### Wrapper DTOs Improve Stability

When the action needs more than a trivial parameter, request and response wrapper classes with `@InvocableVariable` make the contract clearer and more extensible. They also make labels and descriptions visible to Flow builders.

### Error Behavior Must Match The Calling Automation

Some invocables should fail the Flow loudly. Others should return result objects containing success flags and error messages so the Flow can branch. Decide that behavior intentionally rather than by accident.

## Common Patterns

### Thin Invocable To Service

**When to use:** Business logic already belongs in a service or should be reusable elsewhere.

**How it works:** The invocable method accepts request DTOs, delegates to a service, and maps responses back into Flow-friendly result DTOs.

**Why not the alternative:** Fat invocable classes are hard to reuse and version.

### Request/Response Wrapper Pattern

**When to use:** More than one input or output field is needed.

**How it works:** Define nested request and response classes with `@InvocableVariable` annotations.

### Partial-Result Action Pattern

**When to use:** Flow should decide what to do with mixed success outcomes.

**How it works:** Return one response object per input with success flags and error text instead of throwing immediately for every failure.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Flow needs custom business logic not available declaratively | `@InvocableMethod` + service layer | Clean Apex/Flow boundary |
| Action needs multiple inputs or outputs | Wrapper DTOs with `@InvocableVariable` | Stable, discoverable contract |
| Logic must handle many records safely | List-based bulk-safe processing | Declarative callers can batch |
| Flow needs to branch on mixed outcomes | Response DTO with success/error fields | Better than throwing blindly for every record |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] The invocable method is an adapter, not the entire business implementation.
- [ ] Input and output shapes respect list-oriented contracts.
- [ ] Wrapper DTOs are used when the contract is non-trivial.
- [ ] The implementation is bulk-safe and not single-record by assumption.
- [ ] Error behavior is chosen intentionally for the calling Flow.
- [ ] Labels and descriptions are meaningful for automation builders.

## Salesforce-Specific Gotchas

1. **Invocable methods feel single-record in Flow and still need bulk-safe logic** — do not design for only one input.
2. **Poorly designed wrapper classes make Flow configuration painful** — labels and field meanings matter.
3. **Throwing every error may be the wrong contract for orchestration** — sometimes returning per-record result objects is better.
4. **An invocable boundary is not a substitute for a real service layer** — reuse suffers if all logic stays in the action class.

## Output Artifacts

| Artifact | Description |
|---|---|
| Invocable review | Findings on wrapper design, bulk safety, and caller contract |
| Action scaffold | `@InvocableMethod` pattern with request and response DTOs |
| Flow/Apex boundary guidance | Recommendation for when the action should throw vs return structured results |

## Related Skills

- `apex/apex-design-patterns` — use when the invocable is becoming the whole business layer and needs proper service boundaries.
- `admin/flow-for-admins` — use when the automation decision should stay declarative and may not need Apex at all.
- `apex/exception-handling` — use when the action’s failure contract and logging need refinement.
