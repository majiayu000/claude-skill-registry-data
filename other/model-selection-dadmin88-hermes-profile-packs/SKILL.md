---
name: model-selection
description: Select an AI model for a real workload using representative evaluations, current official capability and pricing data, latency and cost measurements, operational constraints, and explicit fallback tradeoffs.
---
# Model Selection

Use when choosing or changing the model behind an AI or agent feature, including deciding whether different task classes should use different models.

## Procedure
1. Define the workload before naming candidates: task distribution, quality bar, context requirements, tool use, structured-output needs, modalities, safety constraints, privacy/data-residency requirements, latency target, throughput, availability expectations, and cost envelope.
2. Include a meaningful non-model or simpler-model baseline when one could solve the task. Do not assume the most capable model is automatically the right system component.
3. Build a candidate set from models that can actually satisfy the required interfaces and deployment constraints. At selection time, verify current model availability, supported features, limits, deprecations, and pricing from official provider documentation because these facts change.
4. Run every candidate on the same representative evaluation set and configuration discipline. Record exact model/version identifiers, relevant reasoning/temperature settings, tool definitions, retrieval context, prompt revision, and evaluation date.
5. Measure task success and important failure categories, not benchmark reputation alone. Include difficult, ambiguous, adversarial, long-context, tool-use, and structured-output cases in proportion to the real workload.
6. Measure operational behavior under realistic conditions: latency distribution, time to first useful output when relevant, token or compute usage, request limits, throughput, retry behavior, error rates, and cost per successful task rather than cost per token in isolation.
7. Evaluate model-specific product risks: instruction following, fabrication, tool misuse, schema reliability, over-refusal/under-refusal, context degradation, multilingual or modality quality, and behavior under untrusted content as relevant to the feature.
8. Compare the Pareto frontier rather than forcing one winner. A smaller model may be best for routine classification while a larger one handles hard planning; routing is justified only when the complexity and failure modes of routing are themselves measured.
9. Define fallback behavior for provider outages, rate limits, model retirement, or degraded performance. Confirm that fallback differences in schema, tools, context, and safety behavior are acceptable before treating models as interchangeable.
10. Record the decision as an evidence-backed snapshot with date, official source links, evaluation results, measured cost/latency, chosen model or routing policy, and conditions that should trigger re-evaluation.

## Decision rules
- Model leaderboards are discovery evidence, not a substitute for workload-specific evaluation.
- Verify unstable facts such as pricing, limits, availability, and feature support from current official provider sources at decision time.
- Compare cost per successful outcome, not headline token price alone.
- Do not choose a larger model solely to compensate for broken retrieval, tools, schemas, or product logic.
- Re-run selection when the workload changes materially or providers release/deprecate models that could alter the tradeoff.

## Quality gate
The model decision is ready when candidates were tested on the real task distribution, current provider facts were verified from official sources, quality and failure modes were compared alongside measured latency and cost, operational constraints and fallback behavior are explicit, and the choice can be revisited from recorded evidence rather than memory.