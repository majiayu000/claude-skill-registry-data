---
name: orc-repl-researcher
description: Build, run, inspect, and recover an adaptive ORC repl-researcher stage inside a behavior or specialist. Use for runtime exploration, generated behavior trees, described tools, bounded fan-out, and evidence-driven focused repair.
---

# Build an accountable researcher behavior

Use a researcher where discoveries change the necessary actions or tree shape. Keep known prerequisites, routing, delivery checks, and reusable specialists in the authored tree. A researcher is a node inside that methodology, not a replacement for all of it. Start from the consuming project's instructions, ORC principles, exact revision, and intended observable result.

Read [design and completion](references/design-and-completion.md) when choosing the adaptive boundary, [setup and contracts](references/setup-and-contracts.md) before implementation, and [palettes](references/palettes.md) before generating code. These references contain the operating knowledge; private examples and benchmark folders are not prerequisites.

Read [model-facing construction](references/model-facing-construction.md) before authoring the researcher's runtime instruction or context. The runtime model does not inherit the agent's skill context. Give it executable construction grammar as well as applicable rules, exact local schemas, tool bindings and repair/completion criteria. Verify the complete relevant example and contracts in the actual first request. An instruction merely saying to use schemas did not prevent fresh models from repeatedly omitting coordinator schemas. A working generic example guides construction; the model must still choose task actions and produce its own semantic answers.

Use recursive mode explicitly in new examples: `:rlm {:recursive? true :checkpointed? true ...}`. The cycle is design → emit → execute → observe → refine → final completion. R-inject supplies useful prior behavior context to this loop. Terminal mode is a compatibility distinction, not the recommended researcher architecture.

## Give the adaptive stage a precise contract

- Describe its goal, inputs, required outputs, evidence, permitted effects, useful partial results, and honest failure. Define concrete Malli schemas with descriptions on the actual blackboard. A populated unrelated field does not satisfy a missing deliverable.
- Place the researcher standalone, in an authored sequence, under an eligible fallback, or inside a delegated specialist as appropriate. Independent researcher stages can run in authored parallel with disjoint writes. Build and verify children before their parent delegates to them.
- Choose a registered model and supported options deliberately. Temperature is adjustable, often decimal, and provider dependent; omit unsupported parameters. Set independent provider, iteration, child-tree, campaign and enclosing limits. Use an actual bounded family call budget.
- Describe tools by purpose, applicability, argument/result schemas, authority, failure meanings and replay semantics. Provide real trusted callers. Preserve discovered opaque references and prepare dynamic arguments from observed values. Code handles literal transforms/effects; models handle semantic work.

Use [blackboard contracts](../orc-blackboard-contracts/SKILL.md), [model/SIO](../orc-model-sio/SKILL.md), [tools](../orc-tools/SKILL.md), [specialists](../orc-compose-specialists/SKILL.md) and [runtime bootstrap](../orc-runtime-bootstrap/SKILL.md) at these seams. Use [decision models](../orc-decision-models/SKILL.md) for finite semantic routing/checking in the authored tree. Do not invent emitted decision/delegate nodes merely because authored ORC supports them.

For model switching, read [researcher model contracts](references/model-contracts.md). It covers the local code-value-only prompt repair, actual inline versus emitted wire contracts, structural attempt ownership, and the independently executed composed recovery proof.

## Distinguish the three execution surfaces

The authored DSL, inline SCI helpers, and emitted vector compiler have different palettes and guarantees. At the inspected revision the emitted palette is sequence, parallel, map-each, llm, code, final, chunk-document and aggregate. Invoke bound tools from generated code; place unsupported control/delegation outside the researcher in authored behaviors.

The prime model sees input previews and variable metadata. Full values remain accessible through `get-input`/`get-var` and can be passed to subwork. The declared final-write contract is advertised, but a preview is not a full read schema or source. Inspect the actual model request when visibility matters.

For emitted work, provide explicit concrete schemas for every fresh write, map item binding and aggregate. Map results for map-shaped inputs preserve original fields and merge named child writes. Put consumers after the join; sibling parallel branches must not read each other's pending writes. Choose fan-out from actual input cardinality and a measured concurrency bound.

Checkpointed emitted code must retain quoted `(fn ...)` source or a registered qualified function. A runtime closure cannot be reconstructed after restart. An SCI `defn` is not an application tool registration. Give generated LLM leaves typed results and, when the task or downstream assessment needs it, a concise node-specific rationale with its own described key. A rationale is not universally required or a proven quality improvement; finite decisions need no invented prose.

## Run, observe, and repair from evidence

Read [recovery and limits](references/recovery-and-limits.md) for model-driven repair versus process recovery, and [observability](references/observability.md) for exact source, ticks, effects and model bodies. Run through public build/execute boundaries and verify both task values and projected effects.

After an emission, inspect the actual child result before finalization. Missing or nil required outputs demand investigation. A genuine empty extraction can be valid if the source and task support it. Use `tree-failures`, `tree-detail`, `tree-trajectory`, `node-output` and `node-input-profile` when the summary is insufficient; prove actual calls and results rather than searching generated code for API names. Preserve the correct UUID, tick, item index, execution context and attempt.

Use surviving verified work in the smallest eligible follow-up tree. Do not repeat successful external effects as a way to hide failed diagnostics. Keep strict final schemas and independent coverage/grounding checks. Completion status, schema validity, correct tool invocation and useful task completion are different evidence.

Review narrative claims as well as structured fields. A correct readiness flag does not justify an invented organizational policy, and completed prerequisites do not establish later real-world completion. Have semantic children cite supplied evidence, identify what remains unknown, and consume explicit code-produced totals when arithmetic is needed. Literal identity/schema checks cannot certify every sentence of a report.

If a field asks whether evidence establishes a prerequisite, false means it is not established by that evidence. It does not prove the prerequisite failed or never happened. Preserve unknown underlying facts explicitly and review generated explanations/reporting against that distinction.

Never infer intent, applicability, source support or completion from word/phrase matching in human or model messages. Never manufacture analysis or repair prose with templates. A documented literal parser, identity join, exact arithmetic or serializer belongs in code; semantic interpretation belongs in models.

Source revision matters: generated LLM options, some intermediate hydration/feedback paths, and ordinary model leaves in a delegated researcher specialist had reproduced gaps at the [source-status snapshot](references/source-status.md). That delegated case involved invalid campaign reservation fields under a positive shared budget; direct sequences worked. The later [model-contract campaign](references/model-contracts.md) proves specific repaired option paths and typed composition through a saved frontier, not closure of every historical gap. Recheck the consuming revision and reproduce a claimed repair; do not carry obsolete workarounds forward or switch new designs to terminal mode.

## Reuse and improvement

For explicit examples/catalogs or automatic classification, injected descriptions, consolidation and harvest, read [researcher pattern reuse](../orc-researcher-pattern-reuse/SKILL.md). These are configured capabilities, not an automatic learning guarantee. Retain versioned causal evidence from past execution to the next real request and outcome. For quality monitoring use [judges](../orc-judges/SKILL.md); asynchronous grading does not replace an active acceptance gate. GEPA and prompt-training setup are separate work.

Finish with the adaptive boundary, authored and emitted trees, schemas/tools/models, real result checks, durable lineage, physical attempts, recovery proof, and any remaining gap. Controlled provider programs prove engine mechanics; live runs prove observed model behavior for those inputs. [Literature](references/literature.md) explains the research principles and their limits.

## Standard-node fallback revision

For model outages, the locally verified standard-node fallback revision covers prime, inline and emitted calls, including specialist defaults, declared inline output contracts, preserved generation options and durable role selection. Read [configured model fallback](../orc-model-sio/references/configured-model-fallback.md). Fallback and the model-contract repairs are integrated in merged ORC `4966c8e35e3bb5939570bfc645eac52a8d18eb6e`, with SIO `e61e11a9` and client `f5fa99d8`; verify loaded pins. The `9116dc99`/`bc65561e` acceptance is historical. See [current integration status](../orc-model-sio/references/model-portability.md#current-authoring-and-source-checkpoint) for the merged repair map and separate unmerged PR #50 timeout correction. Older sources retain the historical option-propagation gaps.
