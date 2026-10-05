---
name: design-chisel-processor
description: Develop, challenge, and document Chisel processor microarchitecture designs before implementation. Use when discussing or writing design documents for processor pipelines, queues, issue logic, rename, ROB, LSU, caches, MSHRs, forwarding, wakeup, replay, flush, privilege, exceptions, or other cycle-accurate hardware mechanisms; when converting design conversations into stable Markdown specifications; or when reviewing a proposed Chisel CPU design for correctness, timing, area, verification cost, and cross-document consistency.
---

# Design Chisel Processor

Build processor designs from precise state semantics and cycle boundaries. Preserve the user's architecture unless a correctness failure forces a change.

## Start

1. Read repository instructions such as `AGENTS.md`.
2. Locate architecture overview, topic documents, protocol documents, and relevant RTL with `rg`.
3. Separate four sources:
   - current RTL;
   - reference implementations;
   - current proposed design;
   - new recommendations.
4. Treat the user's latest correction as authoritative for the proposed design.
5. Ask only when an unresolved choice changes correctness or interfaces.

For an existing repository, identify the documentation hierarchy before analysis. Read both overview and topic document when the topic spans them.

Current RTL describes implementation status. Proposed design documents describe intended architecture. Missing RTL does not invalidate a proposal.

## Analyze one mechanism

Use this order:

1. Define every field and signal.
2. State producer, consumer, set condition, clear condition, valid interval.
3. State same-cycle priority.
4. Draw combinational work and register boundaries by cycle.
5. Enumerate normal, miss, nack, kill, flush, replay, retry, and late-response paths.
6. Check slot reuse and stale ownership.
7. Give a concrete counterexample cycle for each defect.
8. Derive assertions.
9. Evaluate critical path, fanout, ports, storage mapping, code size, and verification cost.

Never use an unqualified `s1/s2/s3`. Name the subsystem, such as `LSU s2 / DCache s1`.

## Close correctness

For every stateful structure, prove:

```text
allocation
-> active ownership
-> all possible responses
-> completion or retry
-> release
-> safe reuse
```

Check:

- one-shot events cannot be missed;
- persistent state substitutes for missed events where required;
- flush blocks all forbidden side effects before registers clear;
- external transactions that cannot be canceled retain ownership;
- old responses cannot target a reused slot;
- release and same-cycle reuse rules are explicit;
- multiple writes to one field have a total priority order;
- speculative wakeup has a complete correction path;
- data visibility follows actual RAM read/write semantics.
- committed and speculative entries sharing one structure have separate flush rules.

Derive identity protection from actual lifetime and ownership. Do not add `generation`, epoch, or ROB identity by habit. A bare index can be sufficient when release, reuse, masks, fixed pipeline latency, or retained ownership prove that stale targeting cannot occur.

Read [references/review-checklist.md](references/review-checklist.md) for the full checklist.

## Compare alternatives fairly

Compare complete implementations under the same capacity, width, stage boundaries, and correctness requirements.

- Include every required set, clear, bypass, retry, release, and ownership mechanism.
- Do not create a counterexample by omitting maintenance already specified for an alternative.
- If a mechanism is unspecified, state the defect conditionally: "If this clear or bypass is absent, the following trace fails."
- Separate unavoidable datapath cost from optional persistent-state maintenance.
- Preserve the selected design unless a concrete invariant fails or measured timing evidence justifies changing it.

For persistent masks, count initial generation, ongoing set and clear networks, same-cycle bypasses, update ports, flush, and slot reuse. For recomputation, count the comparison and selection network on every attempt, including duplicated lanes.

## Evaluate timing and physical cost

Count topology, not only gates:

- comparator count and width;
- source and destination fanout;
- long module-to-module buses;
- priority encoders and wide muxes;
- random update ports;
- replicated read muxes for multiple lanes;
- register boundaries that synthesis must preserve.

Distinguish:

```text
logical cost
physical routing risk
critical-path depth
state-maintenance cost
verification cost
```

Do not claim placement or routing behavior without synthesis evidence. State likely structures and request timing reports when needed.

## Write design documents

Maintain:

1. one architecture overview for cross-module facts and core invariants;
2. topic documents for long state machines or subsystems;
3. protocol documents for Bundles, fields, interfaces, tables, and assertions.

Each state field should include:

```text
semantics
set condition
clear condition
valid interval
consumers
same-cycle priority
invariant
```

Use [references/design-document-template.md](references/design-document-template.md) when creating or restructuring documents.

When a fact affects multiple documents, update all of them in one change. Search for obsolete names and rejected mechanisms after editing.

## Plan Chisel implementation

Before coding:

- freeze interface and state semantics;
- choose register array, SRAM/BRAM, FIFO, CAM, mask, or side table intentionally;
- specify all valid/ready/kill/flush interactions;
- define state transition tables;
- derive assertions and directed tests.

Prefer explicit masks, `Vec`, and per-lane logic when they expose hardware topology. Avoid relying on source-code grouping to control FPGA placement. Add a register boundary when timing requires a guaranteed pipeline cut.

Read [references/chisel-guidance.md](references/chisel-guidance.md) before turning the design into RTL.

## Verify changes

For implementation work, provide:

- state transition table;
- Chisel assertions;
- directed ChiselTest scenarios;
- actual test results with failing cycle and signals.

For documentation-only work:

1. search for stale terminology and conflicting rules;
2. check Markdown fences and conflict markers;
3. compare overview, topic, protocol, assertions, and stage plan;
4. independently review substantial changes with a subagent when available.

Subagent review should be read-only. Ask it for findings by severity, file and line, and a concrete counterexample. Reuse a reviewer that already knows the project when repository rules request that behavior.

## Communicate

- Start by restating the current design accurately.
- Report correctness defects before optimizations.
- Give exact cycle examples.
- Mark unverified statements as hypotheses.
- Say explicitly when no new defect was found.
- Avoid replacing the design with a familiar external architecture without authorization.
