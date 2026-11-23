---
name: orc-decision-models
description: Build bounded semantic decisions in ORC with llm-decision, boolean llm-condition gates, and registered native decision providers such as Jev. Use for described enum routing, finite tool arguments, applicability and completion checks, or decision-model integration and evidence.
---

# Decision models in ORC trees

For per-node provider selection, ordinary LLM versus native decision registration, and effective context limits, read [native provider selection](references/native-provider-selection.md). Native registered names are not interchangeable with ordinary chat model IDs.

Start from the consuming revision, the observable goal and the evidence needed to decide. A fast finite answer is useful only if its errors and abstention policy fit the application. Read [current contracts](references/contracts-and-observability.md) before implementing, [Jev](references/jev.md) for native configuration, and [tree patterns](references/tree-patterns.md) for composition.

## Choose the node and question

| Need | Node or integration |
| --- | --- |
| Boolean predicate controlling eligibility | `llm-condition`: true succeeds, valid false fails without a provider failure kind |
| Boolean or one finite choice retained as data | `llm-decision`: exactly one write; valid false/none succeeds |
| Runtime capability/source IDs | `llm-decision` with `:options-from` included in reads; described runtime alternatives |
| Unrestricted prose, arbitrary values or nested argument maps | Ordinary typed `llm` or deterministic computation |
| Several labels/checks or native Score | Separate decision leaves, or explicit custom native client; not a first-class multilabel/Score leaf |

At ORC `1851212396cced2fc4533fda30b824bd4b691390`, the earlier condition metadata defect is fixed. Prefer supported native nodes over copying the old workaround. A conversational model can power either node. Jev is registered with `:protocol :decision` and selected per node by its registered provider name; its supported boolean/Choice requests participate in normal accounting and execution budgets. Merely assigning a Jev model identity to a chat provider does not switch protocols.

Question meaning belongs in explicit instructions and criteria. Describe every blackboard key, including intermediate and parent records. For static choices use `[:enum {:description "Meaning of this answer" :descriptions {id "Applicability and result" ...}} id ...]`. For runtime choices supply a typed vector of `{:id :description}` and preserve opaque IDs verbatim. Include a genuine none/clarify option when no action may fit. Code validates exact identities, schemas, bounds, permission and already typed routes. Never classify human/AI message meaning with regex, phrase lists or substring checks; never fabricate work or recovery with canned prose.

## Assemble the tree

1. Give a decision exactly one answer key with boolean or finite enum schema. Runtime options may use a string answer. Do not add a prose reasoning write to `llm-decision`, even for a conversational model. Use a separate ordinary `llm` action if a generated explanation or dynamic arguments are needed.
2. Supply actual task/evidence in declared reads. Map each criterion to the evidence the model needs, including material qualifications and missing information. On the inspected input-field-guide stack, native state carries values and the question instructions include the declared input meanings; function-mode ordinary requests include that guide too. Inspect the real wire request for the consuming revision instead of duplicating descriptions by hand or assuming every version transmits them. See [input field guide](../orc-model-sio/references/input-field-guide.md) and [context flow](../orc-blackboard-contracts/references/context-flow.md).
3. Route the answer with exact top-level `condition` guards in guarded `sequence` branches. Use authored `tool` leaves, code tools or prebuilt `delegate` specialists. Read [orc-tools](../orc-tools/SKILL.md) for catalogs, dynamic arguments and recursive action chains. The host owns the executable mapping; a chosen catalog ID is not permission to execute arbitrary code.
4. Keep provider failure, semantic no, abstention and failed effect distinct. Invalid/missing/out-of-set output fails the decision and writes nothing. A fallback may otherwise blur failed inference with a negative verdict: inspect structured failure evidence and restrict recovery eligibility.
5. Set `:min-confidence` only when confidence is a meaningful available signal; it requires an offered `:abstain`. Conversational decisions and native boolean Noul return no confidence, so a floor makes every valid answer abstain. At this pin, boolean `:abstain false` is incorrectly rejected during public workflow build even though false is offered; do not rely on it until repaired. If semantic abstention is required, use a described enum with a distinct clarify/defer option. Do not add a confidence floor to Noul merely to create uncertainty handling: it supplies no confidence. Jev Choice confidence is not measured correctness. Validate task suitability on representative evidence.
6. Sequence new assessments after dependent observations. Parallelize only independent checks with separate writes. One finite leaf is one question; the lower-level provider API can batch boolean/enum outputs, but sibling questions do not see each other's answers. Validate the selected joint proposal before effects.
7. Bound revision with actual tree structure and budget, then reassess the revised artifact and verify the domain projection. A valid decision is not proof the parent goal holds.

## Verify useful outcomes

Exercise true and false predicates, valid false decisions, no applicable route, literal runtime IDs, malformed/provider failures, confidence absent/below floor, contradictory checks, stale evidence and failed tool effects. Inspect actual serialized requests, node instance inputs/outputs, `:condition-answer` or `:decision`, failure kind, model identity and usage; exclude credentials. Read family usage through `get-family-usage`, and compare captured physical attempts when a campaign cap matters. Custom native clients outside the registered path still require their own accounting.

Synthetic responses prove mechanics, not semantic quality, calibration, cost or latency. Preserve first attempts and repairs separately. Use [orc-observe-debug](../orc-observe-debug/SKILL.md) and [orc-model-sio](../orc-model-sio/SKILL.md) for boundary evidence.

## Score-only quality judges

For post-completion evaluation use [orc-judges](../orc-judges/SKILL.md). Native Score remains a custom integration; PR 43 did not repair judge attachment/scheduling. Its ordered-band policy can require a unique maximum and treat exact ties as ungradable. The registered Choice router instead accepts the provider's offered selection when consistent within declared reporting resolution; do not silently impose the stricter judge policy on it. Never invent feedback or confuse expected position with the selected band.

## Current proof and narrow limits

Read [current proofs and limits](references/current-proofs-and-limits.md) when validating merged behavior. Actual native/chat decisions and nominal recursive tool paths ran, but boolean-false abstention, cancelled-family trace/delivery, and ordinary generation's resolved-model event provenance retain open repair obligations. Keep deterministic fixtures, live outcomes and later assisted repairs distinct.

## Assess completed work and choose continuation

For a selected repair route, use the [correction packet](../orc-compose-specialists/references/authored-controller.md#carry-substantive-correction-to-the-owner) to carry the actual criterion and artifact; selecting an owner alone supplies neither.

A decision can run after an entire specialist or a parallel join. Give it the parent goal, actual current results, coverage/gaps, relevant source versions and effect receipts. Describe outcomes such as satisfied, revise, consult-another-capability, wait or handoff; route the finite result through exact guards. A successful child tick is evidence of execution, not automatically of goal fulfillment.

Use the [post-execution decision pattern](../orc-design-tree/references/agent-design-literature.md#decisions-after-an-entire-subtree) and [authored goal controller](../orc-compose-specialists/references/authored-controller.md) for bounded return paths. Jev can choose a known failed criterion or specialist without prose. When revision needs a novel question or critique, obtain it from an ordinary LLM with the actual failed artifact as input. Refresh after dependent actions; parallel questions cannot consume each other's answers. A post-completion monitoring judge does not automatically continue the active tree.

## Standard-node fallback revision

The locally verified standard-node fallback revision adds backups directly to decisions and conditions, including compatible registered native/chat routes. It preserves negative answers and decision contracts; a schema failure or abstention is not an outage. Read [configured model fallback](../orc-model-sio/references/configured-model-fallback.md). This support is not yet published or merged.
