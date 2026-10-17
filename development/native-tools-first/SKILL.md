---
name: native-tools-first
description: Right-size non-trivial technical plans and implementations around existing libraries, CLIs, platform features, standards, workflows, and repository utilities before adding custom code. Use when a solution could duplicate native capabilities or drift into an oversized framework; skip trivial edits and tightly specified implementations.
---

# Native Tools First

Deliver the single requested outcome with the smallest justified integration of proven capabilities. “Native first” is an evidence check, not a command to make every solution small: substantial custom code is correct when current acceptance criteria and verified tool gaps require it.

## Establish the boundary

Before coding:

1. Restate the outcome in one concrete, observable sentence. Treat current-ticket acceptance criteria as the definition of done.
2. Inventory relevant libraries, CLIs, platform features, standards, existing workflows, and repository utilities. Assign each responsibility to its natural owner. Inspect repository configuration and locked or installed versions before proposing replacements.
3. When native capability is uncertain or version-sensitive, check authoritative documentation for the version in use. Separate verified behavior from inference; do not design around remembered limitations.
4. Identify the smallest missing integration or glue. Explain why configuration, composition, or an existing extension point cannot supply it.
5. Separate current acceptance criteria from useful future concerns. Make the latter explicit non-goals or follow-up candidates instead of building for them now.
6. State authorization boundaries. This skill changes the technical approach, not permission: it does not authorize deployments, external writes, messages, purchases, destructive actions, or broader repository changes.
7. Forecast likely files, new dependencies, and rough change size. Use this as a drift tripwire, not a quota or a target.

When the approach involves meaningful judgment, present a compact scope gate before implementation:

```text
Outcome: <one observable result>
Native owners: <tool -> responsibility>
Custom glue: <missing behavior and why it is needed>
Non-goals: <future-ticket or out-of-scope concerns>
Forecast: <files, dependencies, rough size>
Decision: <material tradeoff or “none”>
```

Pause for the user only when the decision would materially change behavior, scope, dependencies, cost, risk, or authorization. If the user requested autonomous execution or the agreed plan already resolves the choice, show the gate as a checkpoint and continue.

## Implement the vertical slice

- Prefer one end-to-end slice that consumes native tool outputs and uses the tool’s storage, identity, policy, lifecycle, and validation mechanisms where they fit.
- Keep custom code at integration boundaries. Map every custom layer to a current acceptance criterion and remove anything that cannot be justified by one.
- Preserve safety, observability, recovery, and fail-closed behavior. Do not equate safety with maximal custom machinery; first use native constraints, boundary validation, idempotency, and existing recovery mechanisms.
- Reuse repository conventions and utilities unless evidence shows they cannot meet the requirement. Avoid parallel sources of truth and duplicated validation.
- Test the integration at the observable boundary, including relevant failure behavior, rather than testing only the glue in isolation.

Stop and re-evaluate before introducing any of these:

- a new framework, generic abstraction, or operating mode;
- a major dependency;
- a custom ledger, state machine, identity layer, or storage system;
- validation already owned by an existing tool;
- material growth beyond the file, dependency, or size forecast.

At a tripwire, revisit the inventory and authoritative docs, explain what new evidence requires the expansion, and update the scope gate. Ask for direction if the revised approach creates a material choice. Proceed with the larger solution when the evidence and acceptance criteria justify it; never force an artificially small design.

## Report the result

Summarize:

- what each existing tool owns;
- what custom glue was added and which acceptance criterion required it;
- what was deliberately deferred;
- whether files, dependencies, and size stayed within forecast, with reasons for any variance;
- what behavior and failure modes were verified.
