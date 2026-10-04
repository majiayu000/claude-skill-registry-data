---
name: invocable-methods
description: "Use when designing or reviewing Apex actions exposed to Flow or similar orchestration layers via `@InvocableMethod`, especially around wrapper DTOs, bulk-safe list contracts, and error behavior. Triggers: 'InvocableMethod', 'InvocableVariable', 'Flow Apex action', 'bulk-safe invocable', 'Apex action input/output', 'callout=true', 'flowTransactionModel', 'Invocable.Action', 'action returns wrong record', 'output list size'. NOT for wiring the action into Flow Builder — use flow/flow-action-framework. NOT for an Agentforce agent action — use agentforce/custom-agent-actions-apex."
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
  - "my apex action updated the wrong record in a record-triggered flow"
  - "why can I only have one InvocableMethod per class"
  - "invocable action returns fewer results than inputs"
  - "callout=true in an invocable throws uncommitted work pending"
  - "flow action faults for all records when one input is bad"
  - "make an apex action accept a generic sObject collection from a flow"
  - "invoke a custom invocable action from Apex or REST"
  - "write a test class for an invocable method with 200 inputs"
  - "call apex from a flow action"
inputs:
  - "Flow or action use case and expected record volume"
  - "whether the action needs complex request or response fields"
  - "error-handling expectation for the calling automation"
  - "whether the action calls an external system, and which flow type invokes it"
  - "whether the class will ship in a managed package or as an Agentforce action"
outputs:
  - "invocable method design recommendation"
  - "review findings for contract, bulk safety, and wrapper usage"
  - "Apex action scaffold with request and response DTOs"
  - "bulk-safe boundary class + service + 200-input test class"
  - "the `actionCalls` fragment with flowTransactionModel and faultConnector"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when Flow or another orchestration layer needs a custom Apex action and the design must survive real volume, not just one-click demos. The key is respecting the invocable contract: public static entry point, list-oriented inputs and outputs, explicit wrapper fields, and behavior that remains bulk-safe under declarative orchestration.

---

## Before Starting

- What automation will call this action, and can it invoke the method for many records in one transaction?
- Does the action need simple primitive inputs, or does it need a wrapper request/response contract?
- What should the calling Flow do on partial failures or validation errors?

## Questions to Ask Before Configuring

Ask these before writing the class. Each one maps to a documented platform behaviour in
`references/gotchas.md`; an assistant that skips them produces an action that passes its first test
and mis-attributes results the first time a flow batches interviews.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Which automation calls this, and can it fire for a batch of records in one transaction?" | The output list must match the input list in size *and* position (apexdev L5456–5457); a single-record implementation is wrong the moment it is batched | The volume the test class must drive, and whether a result list can be built from a `Map` or must be walked by index |
| "When input 7 of 200 is invalid, must the other 199 still process?" | An escaping exception faults the whole invocation, not one input; the guide's own remedy is to report failures inside the result object (apexdev L5318–5319) | The failure contract: per-input `success` + `errorMessage` fields, or a deliberate all-or-nothing throw with a `faultConnector` behind it |
| "Does this action call an external system, and is the caller a screen flow?" | `callout=true` only starts a new transaction in a screen flow with Transaction Control set to let the flow decide (apexdev L26872–26880) | The `callout` modifier, the `flowTransactionModel` value, and whether the callout must move to async |
| "Which fields does the contract need today, and which will it need in a year?" | An invocable method cannot be removed from a later package version (apexdev L5460–5461) and its name must match the flow's, case-sensitively (apexdev L5731) | Wrapper DTOs over primitives, so a new field never changes the method signature |
| "Does the flow pass one known sObject type, or does the admin choose?" | Generic `sObject` inputs work, but the flow must carry `T__` / `U__` `dataTypeMappings` (api_meta L70192–70203), and `List<List<sObject>>` is a runtime error as a wrapper field (apexdev L5440–5442) | A concrete type, or the generic design plus the flow-side mappings it obliges |
| "Will this class ship in a managed package or become an Agentforce action?" | Only *global* invocable methods appear in a subscriber org's Flow Builder (apexdev L5462–5465); an Agentforce action "must be global static" (apexdev L43653) | The visibility decision, and one action per outer class (apexdev L5422) |
| "Who runs the flow, and do they have Apex class access?" | "the running user must have the corresponding Apex class security set in their user profile or permission set" (apexdev L5172) | The permission set shipped in the same manifest, with `classAccesses` naming the class |

What a proper configuration adds over just writing the annotation: the action returns one result per input in the caller's order, one bad input costs one record instead of the whole batch, the transaction model is a decision rather than a discovery, and the contract can gain a field without breaking every flow already bound to it.

---

## Core Concepts

### Invocable Methods Are Boundary Adapters

An invocable method is not the whole business layer. It is the entry point that translates Flow-friendly inputs into the service layer. Keep the annotation boundary small and delegate the actual behavior elsewhere.

### The Contract Is List-Oriented

Invocable methods are designed around list inputs and outputs even when a Flow screen makes the action feel single-record. Bulk-safe design still matters because declarative automation can batch work in ways the first demo does not show.

### Wrapper DTOs Improve Stability

When the action needs more than a trivial parameter, request and response wrapper classes with `@InvocableVariable` make the contract clearer and more extensible. They also make labels and descriptions visible to Flow builders.

### Error Behavior Must Match The Calling Automation

Some invocables should fail the Flow loudly. Others should return result objects containing success flags and error messages so the Flow can branch. Decide that behavior intentionally rather than by accident.

### The Contract, In One Table

| Rule | Value | Source |
|---|---|---|
| Method | `static`, `public` or `global`, on an outer class | apexdev L5421 |
| Methods per class | exactly one annotated | apexdev L5422 |
| Stackable annotations | `@Deprecated` only | apexdev L5430 |
| Parameters | at most one, and it must be a `List<…>` | apexdev L5432 |
| Return | a `List<…>` of a permitted type, or void | apexdev L5443–5454 |
| Size and order | i-th output ↔ i-th input | apexdev L5456–5457 |
| Errors | reported in the result, same count as inputs | apexdev L5318–5319 |
| Wrapper fields | `public`/`global` instance members only — no static, final, protected, private, or properties | apexdev L5718–5723 |
| Parameter class ctor | visible no-arg constructor from API 66.0 | apexdev L5737–5739 |

### Modifiers, And What Each One Buys

| Modifier | Effect | Default |
|---|---|---|
| `label` | action name on the Flow canvas; the Agentforce reasoning engine reads it (apexdev L43664–43666) | the method name |
| `description` | action description in Flow Builder | Null |
| `category` | Flow Builder grouping | Uncategorized |
| `callout` | declares an external call; gates the screen-flow transaction switch | `false` |
| `configurationEditor` | registers a custom property editor LWC — see `lwc/custom-property-editor-for-flow` | standard editor |
| `iconName` | static-resource SVG or an SLDS icon on the canvas | standard icon |
| `capabilityType` | integrating capability, format `Name://Name` (e.g. `PromptTemplateType://SalesEmail`) | none |

Sourced from apexdev L5404–5417. UNVERIFIED (2026-09-05): the Apex Developer Guide's modifier list states no per-modifier API-version floor, and none of the `label` / `description` / `callout` / `capabilityType` / `category` / `configurationEditor` / `iconName` entries carries a "available in API version N and later" note. Do not quote a floor for these; the nearest grounded version facts are the API 66.0 no-argument-constructor rule for parameter classes (apexdev L5737–5739) and the flow-side floors — `flowTransactionModel` API 51.0, `storeOutputAutomatically` API 48.0, `FlowDataTypeMapping` API 48.0 (api_meta L68487, L68530, L70179).

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

### Seed-Then-Fill Result Construction

**When to use:** Always, in any action that can fail per input.

**How it works:** Build `results` with one entry per input *before* the query, then fill entries by index. Never append results only on the success path and never build them from a `Map.values()` or a `List<Database.SaveResult>` — both change the size or the order. `references/code-examples.md` §3 is the reference implementation.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Flow needs custom business logic not available declaratively | `@InvocableMethod` + service layer | Clean Apex/Flow boundary |
| Action needs multiple inputs or outputs | Wrapper DTOs with `@InvocableVariable` | Stable, discoverable contract |
| Logic must handle many records safely | List-based bulk-safe processing | Declarative callers can batch |
| Flow needs to branch on mixed outcomes | Response DTO with success/error fields | Better than throwing blindly for every record |
| Action must call an external system from a screen flow | `callout=true` + Transaction Control set to let the flow decide | The only combination that commits and starts a new transaction (apexdev L26872–26876) |
| Action must call an external system from a record-triggered flow | Enqueue async work, or set `flowTransactionModel` to `NewTransaction` | `callout=true` alone does not move a non-screen flow out of the current transaction (apexdev L26877–26880) |
| The same collection action must serve several objects | Generic `List<SObject>` wrapper field + `T__`/`U__` `dataTypeMappings` in the flow | api_meta L70192–70203 |
| Apex must call a standard or custom action | `Invocable.Action.createStandardAction` / `createCustomAction` then `invoke()` | apexrefguide L160877–160997 |
| A second "single-record" variant is requested | A second outer class delegating to the same service | One annotated method per class (apexdev L5422) |

## Recommended Workflow

1. **Fix the contract before writing code.** Answer the seven rows in *Questions to Ask Before Configuring*, then write down: the input field list, the output field list, the failure mode (per-input result vs throw), and whether the action calls out. Check the contract table above against each choice.
2. **Write the boundary class.** One outer class, one `@InvocableMethod`, `public static`, one `List<Request>` parameter, `List<Result>` return. Wrapper classes carry only `public` instance fields with `@InvocableVariable` labels and descriptions the admin can act on. Copy the shape from `references/code-examples.md` §2; do not restate the guide's rules from memory — `references/gotchas.md` has the ones that bite.
3. **Write the service so it costs one SOQL and one DML for N inputs.** Seed the results list from the input list first, collect ids into a `Set`, query once with `WITH USER_MODE`, build the DML list de-duplicated by record Id, run one `Database.update(records, false, AccessLevel.USER_MODE)`, then fold the save results back onto input positions. `references/code-examples.md` §3.
4. **Write the test at 200 inputs, and assert order and limits, not just success.** Seed with `templates/apex/tests/TestDataFactory.cls`, assert `results.size() == inputs.size()`, assert `results[i]` corresponds to `inputs[i]` for every `i`, and assert `Limits.getQueries()` and `Limits.getDmlStatements()` deltas are exactly 1. Add the mixed-outcome case and the empty-list case. `references/code-examples.md` §4.
5. **Run the checker over the source tree.** `python3 skills/apex/invocable-methods/scripts/check_invocable_methods.py --manifest-dir force-app`. It flags a second `@InvocableMethod` in one class, a non-static or non-`List` signature, SOQL/DML inside a loop, a missing `label`, `@InvocableVariable` on a static or final field, a callout without `callout=true`, and a return type that is neither a `List` nor `void`. Exit code 1 means findings, and every CRITICAL is a contract violation, not a style note.
6. **Wire the flow deliberately.** Set `flowTransactionModel` on purpose, attach a `faultConnector`, and bind `inputParameters` by the exact case-sensitive Apex field names. `references/code-examples.md` §6; fault-path design belongs to `flow/fault-handling`, action design on the flow side to `flow/flow-action-framework`.
7. **Verify in the org.** Deploy in the order in `references/code-examples.md` §8 (permission set before flow), then prove registration and index alignment with the REST describe and a two-input POST (§9), and confirm the debug log shows one SOQL and one DML for a 200-record run.

---

## Review Checklist

- [ ] The invocable method is an adapter, not the entire business implementation.
- [ ] Exactly one `@InvocableMethod` in the class, `public`/`global static`, on an outer class.
- [ ] The return list is seeded from the input list, so size and order can never drift.
- [ ] Wrapper DTOs are used when the contract is non-trivial, with `public` instance fields only.
- [ ] Per-input failures are returned as data; only a whole-call failure throws.
- [ ] `callout=true` is present if and only if the method calls out, and the caller's flow type has been checked against the transaction rules.
- [ ] The `actionCalls` element has a `faultConnector` and a deliberate `flowTransactionModel`.
- [ ] The test class drives ≥ 200 inputs and asserts positional correspondence and constant SOQL/DML counts.
- [ ] A permission set granting `classAccesses` ships with the class.
- [ ] Labels and descriptions are meaningful for automation builders (and for the Agentforce reasoning engine, if the class is an agent action).

## Salesforce-Specific Gotchas

1. **Invocable methods feel single-record in Flow and still need bulk-safe logic** — do not design for only one input.
2. **The output list must match the input list in size and position** — a result list built on the success path silently mis-attributes outcomes.
3. **One class may hold only one `@InvocableMethod`** — a "convenience overload" needs a second outer class.
4. **An escaping exception faults every interview in the batch** — not the one bad input.
5. **`callout=true` starts a new transaction only in a screen flow** — in a record-triggered flow it changes nothing.
6. **`@InvocableVariable` rejects static, final, protected, private and property members** — and the field name matches the flow case-sensitively.
7. **Poorly designed wrapper classes make Flow configuration painful** — labels and field meanings matter.
8. **Throwing every error may be the wrong contract for orchestration** — sometimes returning per-record result objects is better.
9. **An invocable boundary is not a substitute for a real service layer** — reuse suffers if all logic stays in the action class.

Full detail, with line-referenced sources, in `references/gotchas.md`.

## Output Artifacts

| Artifact | Description |
|---|---|
| Invocable review | Findings on wrapper design, bulk safety, and caller contract |
| Action scaffold | Boundary class + bulk-safe service + `-meta.xml`, per `references/code-examples.md` |
| Bulk test class | 200 inputs, positional assertions, constant SOQL/DML assertions |
| Flow wiring fragment | `actionCalls` with `flowTransactionModel` and `faultConnector` |
| Checker report | JSON findings from `scripts/check_invocable_methods.py` |
| Flow/Apex boundary guidance | Recommendation for when the action should throw vs return structured results |

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are writing the class: complete boundary class, bulk-safe service, `callout=true` variant, 200-input test, `actionCalls` fragment, package.xml, deploy order, org verification |
| `references/gotchas.md` | You are reviewing one, or debugging an action that "works" but attributes results to the wrong records; 14 line-referenced platform behaviours |
| `references/llm-anti-patterns.md` | You are checking generated code — 8 mistakes assistants make in this domain, each with a detection hint |
| `references/examples.md` | You want the smallest illustrative wrapper and service pair, plus the REST two-input proof of index alignment |
| `references/well-architected.md` | You are tagging findings by pillar, or need the source list with the claim each one supports |

## Related Skills

- `flow/flow-action-framework` — use when the question is how the flow *calls* the action rather than how the Apex is written.
- `flow/fault-handling` — use when designing what happens after `faultConnector` fires.
- `flow/flow-bulkification` — use when the batching behaviour on the flow side is the thing under review.
- `apex/callouts-and-http-integrations` — use when the action calls an external system and the callout itself needs design.
- `flow/flow-transactional-boundaries` — use when the transaction model, not the action, is the problem.
- `lwc/custom-property-editor-for-flow` — use when the `configurationEditor` modifier needs a custom property editor.
- `apex/apex-design-patterns` — use when the invocable is becoming the whole business layer and needs proper service boundaries.
- `admin/flow-for-admins` — use when the automation decision should stay declarative and may not need Apex at all.
- `apex/exception-handling` — use when the action's failure contract and logging need refinement.
- `agentforce/custom-agent-actions-apex` — use when the same class must serve an Agentforce agent, which adds a `global static` requirement.
