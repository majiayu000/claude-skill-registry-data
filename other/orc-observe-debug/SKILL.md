---
name: orc-observe-debug
description: Investigate and monitor ORC workflow ticks through durable traces, node I/O, event projections, streaming, and provider requests. Use when an ORC tree fails, returns surprising or partial results, loses live updates, or needs operational visibility.
---

# Observe and debug an ORC tree

The structured-contract repairs are integrated in merged ORC snapshot `250de6e6de2ad95647ef6da4c69220c2bd631279`; read [the verified repair path](../orc-model-sio/references/structured-contract-repairs.md) before applying historical parser/metadata limitations below. It covers generated model-visible output meanings, paired strict parsing, null preservation and execution-owned provider observations. Verify the loaded revisions; older consumers may lack these APIs.

Start with the running application's ORC/Grain versions and the exact tenant, sheet, and tick. Check the current ORC source before copying a diagnostic command; the source-pinned query and wire map is in [references/evidence-path.md](references/evidence-path.md).

For differences across models, protocols or generated roles, follow [the model-contract investigation recipe](../orc-model-sio/references/model-portability.md). Attribute each result to its first failing boundary and exact loaded source; null content, a failed route, a false semantic condition and invalid typed output are distinct outcomes.

## Trace the actual execution

1. Read `:sheet/get-trace` for the tick. It gives node status, timing, lineage, read/write **keys**, and size profiles. It does not contain blackboard values.
2. For each relevant node, take its `:trace-instance-id` from `:node-traces` and call `:sheet/node-trace-detail`. Record actual `:inputs`, `:outputs`, `:rejected-outputs`, `:failure-kind`, and `:provider-evidence`. A node ID alone is ambiguous across retries and `:map-each` items.
3. Follow `:sheet/get-trace-family` through delegated child ticks and `:sheet/get-correlated-traces` across independent roots in one operation. Read the workflow definition/version used by the tick when explaining an instruction or key contract.
4. Read the tenant-scoped tick events and the affected read model or public query. Domain events may carry operation tags rather than tick tags: join their operation identity explicitly instead of assuming the tick read contains every effect. The return value and an ephemeral stream are not proof that a write landed. Distinguish an execution failure from a stale projection or a faulty diagnostic harness. A REPL/MCP client wait timeout may leave the evaluation running: inspect its original tick/result artifact and owned workers before rerunning, so an observer timeout does not duplicate effects.

## Inspect failure evidence without copying secrets

Inspect the public execution result, the exact failed node completion and tenant-scoped tick events separately from the tick lifecycle projection. A local HTTP 502 reproduction at ORC `481523c2d9cda6bb0bc835c78f7d24c6a5bef9dc` found the fictional bearer token in the first three surfaces while the lifecycle projection contained none. The client supplied typed category/status, but ORC's completion lost them. A clean lifecycle view therefore does not establish safe or complete node evidence.

The historical ordinary safe typed failure repair and scoped alternative proof were independently observed in a **local, unmerged checkout**; see [scope and evidence](../orc-model-sio/references/scoped-model-alternatives.md). For admission, identify the gate's persisted start and its exact earlier predecessor, then compare canonical inputs, context and typed failure; a nearby failure is insufficient. Count actual requests and completed effects. Demand the exact reason in negative controls. Observe deadline retention from frozen tick options at this pin, not absent node-trace fields; retention does not prove expiry enforcement.

For this diagnostic, use a local endpoint and a fictional token. Measure exposure before redacting the fixture marker, then retain safe snapshots and boolean exposure results. For real failures, extract only allowlisted fields; do not print or save whole transport messages, ex-data or causes. See [model failover and provider failure evidence](../orc-model-sio/SKILL.md#model-failover-and-provider-failure-evidence) before interpreting an unclassified transport failure as temporary.

## Establish what the model received

ORC builds a typed module from described blackboard fields, serializes complex inputs, SIO renders the selected marker, `submit_response` tool or strict JSON-schema contract, and litellm's provider adapter serializes the outgoing request. The durable node trace **does not store that request**. For a controlled local run, capture the serialized HTTP body at the final provider adapter boundary, together with the selected model and non-secret request options. Associate each physical request with a verified structural owner (tick, node, execution context and node attempt); output equality cannot distinguish identical parallel items or failed requests. The reference explains the [verified ordinary-attempt and researcher-reservation correlation seams](references/evidence-path.md#structural-http-attempt-ownership), including their internal instrumentation limitation. Compare complete serialized input values, not only labels or selected identifiers: a canned fixture answer can conceal lost context. Preserve the complete body for comparison; keep credentials out of the capture and handle sensitive inputs under the application's data policy. This proves the body sent by the adapter, not any private transformation inside the provider.

## Native decision calls

A separate historical **local, unmerged repair** retained direct native HTTP status as optional `provider-evidence.transport.http-status` through completion, trace detail and the one-response wrapper’s error terminal. See [scope and evidence](../orc-model-sio/references/scoped-model-alternatives.md). Native429 without a supplied category remains status-only; it is not automatically a temporary rate limit. This terminal-only proof says nothing about partially emitted chat output.

For conversational reasoning models, distinguish declared output rationale, separate provider reasoning, and reasoning token counts. The older inspected OpenRouter adapter dropped the latter two before ordinary ORC traces; later model-contract captures retain reasoning/refusal channels in provider observations. Verify the loaded path and compare its correlated response rather than assuming every `:raw-response` is the full provider message. See [reasoning and completion budgets](../orc-model-sio/references/reasoning-and-completion-budgets.md). Record `length`/truncation separately from missing-key or semantic failures.

For registered native providers inspect condition `:condition-answer` or leaf `:decision` together with normal inputs/outputs, usage and provider evidence. When a custom code client calls an unsupported native primitive, inspect its application-owned request, response and accounting seam. Preserve exact state/questions, answer IDs, original probabilities when supplied, selected finite values, policy route, evidence revision, resolved model and attempt correlation. Label policy reason codes and derived scores; do not attribute them to model reasoning or manufacture certainty. Code-node duration and outputs alone do not prove native usage/cost/budget coverage. Read [decision contracts and observability](../orc-decision-models/references/contracts-and-observability.md) for the required distinctions.

Compare valid invocation, semantic acceptance, tool dispatch and projected outcome separately. Missing responses or incomplete source coverage cannot support a semantic absence/completion claim. Recheck freshness when inference spans changing state, and label fake-client captures as synthetic request construction rather than a live HTTP wire capture.

## Monitor and close the investigation

For custom tools and nested action chains, use [orc-tools](../orc-tools/SKILL.md). Correlate selected catalog/version, prepared arguments, host validation, actual tool results, eligible recovery and domain projections. Follow every result-to-next-action seam rather than stopping at a successful invocation.

Execution-result delivery and trace assembly are separate processors. Poll for a terminal trace whose `:source-event-count` matches canonical tick events after excluding trace publication events; preserve query anomalies. Retrieve every delegated child and its node details. At ORC `1851212396cced2fc4533fda30b824bd4b691390`, `get-family-usage` consolidates registered provider usage across descendants without double counting. Compare it with physical provider captures; conditions now retain answer/I/O/model/usage and decisions retain offered options, selected/set-aside answer and reported native evidence.

Earlier pins can leave a generated child's trace stale when its RLM completion bookend arrives after assembly. The later private repair refreshes that child's trace without redirecting to the source campaign; duplicate delivery adds no revision. Verify the consuming revision includes the repair, retain bounded readiness failure otherwise, and never exclude the late bookend to obtain matching counts. Read [trace revision](references/evidence-path.md#trace-source-revision) for the response shape and verified scope.

Use `:sheet/node-stats` for recurring success, failure, latency, and error patterns. A live `subscribe-execution` stream can omit previews or drop buffered events; large values are capped in the stream. Reconcile every complete operational view with the tenant-scoped event log. Inspect telemetry-exporter retry/drop counters if forwarding is enabled, and distinguish stream reconnection from durable execution recovery.

Report the trace IDs, exact node instance and I/O evidence, provider body capture or its absence, projection state, root cause, and a bounded reproduction/proof of the correction. Record executed test counts when using a test runner: an exit 0 after zero tests is no proof, and unknown or non-test selections must fail before execution. If the work is a real fix, follow the host project's spec and TDD rules and verify a live run as well as a durable test. Do not attribute an unexplained failure to model variance.

## Observe judging separately

Use [orc-judges](../orc-judges/SKILL.md) for grade events, coverage, provenance and calibration. Track producer completion, assessment selection, each physical model attempt, verdict and durable projection separately. A completed tick does not imply judging finished. Compare exact assessed I/O with the final provider request; native custom host-trace is a node-ID placeholder at the inspected pin. Native score projection drops event model provenance and repeated executions can share one score identity; retain richer application evidence rather than interpreting missing fields as a successful complete report.

## Cancellation is durable evidence, not necessarily a complete trace

At the merged revision, family budget admission works, but public adverse tests found a cancelled child without a canonical trace. Child cancellation can also interrupt the worker publishing root cancellation after its SQLite append, so live delivery can be missing while the fact exists. Inspect original tick cancellation events and every started family execution; preserve missing trace/readiness as an open defect. Do not fabricate completion, infer notification delivery from durable append, or call timeout/wedged failure prompt cancellation. Read [current proof limits](../orc-tools/references/current-proofs-and-limits.md).

For ordinary generation, completion event `:model` is configured/requested rather than provider-resolved; retain actual prediction/response identity separately. Native decision completion identity is resolved. Family usage proves reported usage coverage, not correct model provenance or complete traces.

## Inspect researcher iterations and repairs

Use [researcher observability](../orc-repl-researcher/references/observability.md) for immutable iteration code/source, resume state, child ticks, effect receipts and actual model bodies. Inspect get-var :tree-results before drill-down; get-input is only for original inputs. Prove real helper invocations/returned values, no replay of successful work, map identity coverage and strict task completion. Use [reuse evidence](../orc-researcher-pattern-reuse/references/evidence-and-promotion.md) to trace selected description/version through the exact sent request to the next executed tree; a changed body alone is insufficient.

## Prove authored goal continuation

Reconstruct each pass by tick, node and execution context, including tick iteration. The same delegated specialist can have several distinct child ticks. Show the original obligation, missing prerequisite, actual resolver output, resumed specialist input, acceptance result and projected business outcome. A → B → A is stronger evidence than a repeated node name. Preserve completed sibling effects and prove their count; changed prose alone is not evidence of progress.

At ORC `9f7c27357b9f9bcf765fbd86baaedf5911261cd8` with the local structured-contract repairs, a live repeated-judge experiment exposed incorrect writes in the execution result's family `:node-trace`: its combined write index omitted tick identity, so repeated same-sheet child nodes shared an entry. Canonical tick-specific writes and cold reconstruction remained correct. Until verified repaired in the consuming checkout, resolve each completion against its own tick rather than using that result summary to build historical feedback or training examples. The collision winner depends on family enumeration, not necessarily chronological order.

For raw events, resolve node names from `:sheet/node-name-set`; do not assume every completion contains `:node-name`. Resolve delegate writes through `value-log-resolve-writes` and inspect `:sheet/node-trace-detail` for actual inputs. Record both engine `:success` and business outcomes such as waiting/handoff; reporting an unresolved result successfully does not mean the requested effect occurred. On a representation mismatch, inspect the exact response before altering semantic instructions. See [input/output boundary findings](../orc-model-sio/references/input-field-guide.md).

## Standard-node fallback revision

For the locally verified standard-node fallback revision, inspect full trace `:model-fallback` and the authenticated `:sheet/model-candidate-history` query, alongside physical provider attempts. The [fallback recipe](../orc-model-sio/references/configured-model-fallback.md) includes the query envelope and cancellation/stream diagnostics. Fallback is integrated in merged ORC `4966c8e35e3bb5939570bfc645eac52a8d18eb6e`, with SIO `e61e11a9` and client `f5fa99d8`. The original `9116dc99`/`bc65561e` acceptance remains a historical publication checkpoint. Use [current integration status](../orc-model-sio/references/model-portability.md#current-authoring-and-source-checkpoint) to distinguish merged campaign repairs from the separate unmerged PR #50 correction, and verify loaded revisions.
