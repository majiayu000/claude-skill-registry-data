---
name: orc-researcher-pattern-reuse
description: Configure and verify prior-pattern guidance for recursive ORC REPL researchers, using described catalogs or ontology classification and R-Inject. Use when researchers should design better trees from previous behaviors or when auditing whether stored guidance reached a model.
---

# Reuse patterns in a recursive researcher

Help a researcher design, execute, inspect and refine a tree using relevant prior knowledge. Keep the task's success contract authoritative. Retrieved patterns are advice to adopt, adapt or reject according to that contract.

Before writing the prime instruction/context, read [researcher setup](../orc-repl-researcher/references/setup-and-contracts.md) and [model-facing construction](../orc-repl-researcher/references/model-facing-construction.md). Retrieved design advice does not supply the consuming compiler's executable grammar, concrete local coordinator schemas or trusted tool bindings. Give those to the runtime model separately and inspect the actual first request. A relevant selected pattern can still produce an unsupported composite map, missing schemas or incorrect named writes; classification fitness is not executable correctness.

Use a recursive, checkpointed researcher explicitly:

```clojure
:rlm {:recursive? true
      :checkpointed? true
      :auto-classify? true
      :auto-classify-threshold 0.7
      :auto-classify-behavioral-threshold 0.6}
```

Add task-appropriate provider, classification, iteration and campaign deadlines, generation limits and call budgets. The threshold values above are source defaults, not calibrated accuracy guarantees. Omit `:auto-classify?` when supplying an explicit context or using only a described catalog.

## Choose the reuse mechanism

| Need | Mechanism |
| --- | --- |
| Give the researcher known deterministic capabilities | Describe available code nodes and bound tools, including arguments, outputs, effects and failure semantics. |
| Reuse a verified callable specialist | Register an authored subtree and compose it through `:delegate` with explicit reads/writes. |
| Supply selected design advice | Provide explicit context through the node's supported context interface. |
| Find relevant stored patterns before design | Configure ontology classification and R-Inject with a ready corpus/index. |
| Improve advice from repeated executions | Deliberately configure occurrence capture, judging, consolidation and refresh; verify the complete evidence chain. |

A retrieved source pattern does not register an executable specialist. A code catalog is not an automatically learned corpus. These mechanisms can be combined, but record what each actually supplies.

## Build the design loop

Describe the researcher's goal, source inputs, required outputs, success evidence and permitted effects. Require meaningful typed intermediate values, with descriptions, including generated mapping item and aggregate keys. Semantic interpretation belongs in LLM or decision nodes; arithmetic and deterministic operations belong in code. Do not interpret human or AI meaning with regex, phrase matching or response templates.

Require the researcher to emit a supported generated-tree DSL, execute it, inspect the real outcome and either repair useful surviving work or finalize actual values. Recursive mode continues the design loop after a generated tree returns. It does not make the first generated tree correct or remove the need to inspect failures. Use current-campaign drill-down tools for trajectory, failures, node outputs and input profiles when a summary is insufficient.

Keep reusable advice conditional: capabilities; when a strength applies; when a weakness applies; recommended structure or alternative; source provenance and evidence status. Compare the advice to the task before reusing its schema or structure. Preserve sequential preconditions, coherent fallback goals and independent parallel effects.

## Set up and verify corpus guidance

Read [corpus and controls](references/corpus-and-controls.md) when enabling automatic classification, bootstrapping a store, choosing retrieval dependencies or troubleshooting missing guidance. Loading a library, enabling a flag or recording an assignment is insufficient: prove a ready index, an actual candidate selection and the exact injected text in the actual provider request.

For monitoring or a paired experiment, read [evidence and promotion](references/evidence-and-promotion.md). Preserve the input/contract, assignment, candidate IDs and versions, rendered block/hash, full request, emitted tree, attributed execution values and independent task outcome. Use a context control for holdouts; caller-thread bindings may not reach Grain pollers.

If a reranker fails or classification defers, report uncertainty. Do not interpret it as proof of a novel behavior. When a generated tree fails, inspect missing schemas, exact I/O and tool results before accepting the model's explanation of the cause.

## Improvement and promotion boundary

Reuse of human-authored advice can help a live run without proving automatic learning. Learning across runs additionally requires correctly attributed execution/quality evidence, a persisted advice change, a refreshed index and that exact changed advice influencing a later successful execution. One successful guided run and one failed control are useful apparatus evidence, not a general performance claim.

Manually promoting a generated behavior means reviewing its executable source, contracts and effects, verifying it, then registering an authored reusable specialist. Harvested descriptions remain advice until such an executable is registered and exercised.

When available, use the companion researcher setup skill for the node/runtime contract and the ORC blackboard, tools, specialist composition, model/SIO and observability skills for their respective seams. This skill's references contain the reuse controls and proof criteria without depending on private projects or talks.
