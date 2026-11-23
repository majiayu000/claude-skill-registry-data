---
name: orc-design-tree
description: Design a hand-assembled ORC behavior tree from a knowledge-work goal, including known specialist selection and revisiting, typed context, success conditions, control nodes and bounded recovery.
---

# Design an ORC tree

Use this when the user needs the **behavior and shape** of a new tree or a structural redesign. For implementation of already chosen child workflows, use `orc-compose-specialists`. These skills share the [specialist design reference](references/specialist-design.md): use it for decomposition, recursive delegation, routing and reusable capability contracts.

For a goal that needs repeated deliberation, read [authored goal solving](references/authored-goal-solving.md). It covers choosing and revisiting known specialists, missing-information requests, reassessment after a subtree/join, honest stopping and retained work. These behaviors do not require a researcher or runtime tree generation.

For a new application, route directly to [blackboard contracts](../orc-blackboard-contracts/SKILL.md) for typed data seams, [runtime bootstrap](../orc-runtime-bootstrap/SKILL.md) for standalone dependencies and service lifetimes, [model/SIO](../orc-model-sio/SKILL.md) for provider requests and parsed outputs, [Grain application](../orc-grain-application/SKILL.md) for guarded domain writes/queries, and [observability](../orc-observe-debug/SKILL.md) for durable proof. Read each at the boundary the goal needs; this is a responsibility map, not a required universal stage sequence.

## Check the first application boundary

Before choosing a new application's first blackboard fields, read [blackboard contracts](../orc-blackboard-contracts/SKILL.md). Keep structured state, source facts and intermediate results as described native records across delegates and model inputs. A typed intent output does not make opaque JSON/EDN input strings typed; absence of `:any` alone is insufficient. Use text for genuine prose or an explicit external text protocol. See [the first-use contract check](references/first-use-contract-check.md) for the short review and its evidence.

When a skill or source read is truncated, retrieve the missing relevant sections in smaller reads before relying on it. Record remaining unread guidance as a limit; loading an entry point is not evidence that every linked workflow was followed.

## Ground the design

1. Read ORC’s tracked [agent instructions](../../AGENTS.md), [principles](../../docs/ORC-PRINCIPLES.md), current DSL implementation, and the relevant application contract. Follow the consumer application’s own instructions if it provides them. Check its branch and revision first; examples from older apps are evidence, not authority. Read [behavior tree assembly](references/bt-assembly.md) before choosing control nodes. Its reading route links public BT literature and self-contained specialist guidance; use the literature for design logic and current ORC source for execution guarantees.
2. State the user's goal as observable postconditions: the useful output, where it lands, acceptable partial outcomes, and what constitutes honest failure. Name the inputs and the evidence that would prove success after a tick, including projection read-back. Start with one vertical path from input to useful output.
3. Work backward from each postcondition: what action can establish it, what preconditions make that action eligible, and what alternative method can achieve the same goal? Use a postcondition–precondition–action fallback where it clarifies the behavior. Identify distinct behaviors that have their own goal and contract; use `:delegate` where a specialist can be independently run, reused, or evolved. Recursively decompose prerequisites only where intermediate evidence, reuse, alternative methods or recovery justify a boundary; stop at bounded judgments/actions or deterministic capabilities. Design from the goal downward, then register dependencies from the leaves upward. Nested composition, revisiting a known specialist and automatic re-ticking are separate mechanisms; do not infer support for self-referential delegate cycles.

For independently retryable work, alternative methods and recovery, use the [control-boundary review](../orc-compose-specialists/references/control-boundaries.md) when deciding which transitions belong in the tree and which bounded policies belong in code.

## Choose nodes by responsibility

| Need | ORC choice |
| --- | --- |
| One bounded semantic judgment that gates an action | `llm-condition`; true succeeds and valid false fails |
| Semantic classification with a durable finite result | `llm-decision` with exactly one answer write, then exact `condition` guards |
| Finite semantic routes, applicability checks or ordered scores | Consider a decision model; use [orc-decision-models](../orc-decision-models/SKILL.md) to choose and wire it |
| One bounded generation or analysis step | `llm` with a specific instruction and typed output |
| One fixed tool call with flat arguments | Authored `tool` with declared contracts |
| Deterministic transform, nested argument construction or several calls | `code` using guarded `:call-tool-fn` |
| Steps all required in order | `sequence` |
| Ordered, meaningful alternatives or recovery | `fallback` |
| Independent work with separate output ownership | `parallel` |
| Per-item work on a collection | `map-each`; account for `:partial` and result compaction |
| Reusable multi-step specialist | `delegate` to a child workflow |
| Reassess and revisit known work until settled | Isolated bounded controller child; see [authored controller](../orc-compose-specialists/references/authored-controller.md) |

For custom tools, described capability catalogs, dynamic arguments and result-dependent action chains, read [orc-tools](../orc-tools/SKILL.md). It covers tool behaviors containing multiple actions and the separate researcher binding/code-generation path.

For bounded semantic decisions, consider a decision model alongside ordinary LLMs. Choose from task evidence, required context, error costs, latency and integration effort; use a generative LLM when writing or deeper reasoning is required. Supported native boolean/Choice providers run through `llm-decision`/`llm-condition`, selected per node by their registered provider name. Custom clients remain appropriate for unsupported primitives. Read [decision-model tree patterns](../orc-decision-models/references/tree-patterns.md) for finite arguments, specialist selection and work checks. Semantic assessments and tool effects have separate success evidence.

Reserve `repl-researcher` for genuinely open-ended, iterative exploration. In a hand-assembled tree, an LLM decision can route to a code action or another specialist tree. A tool need not be exposed as an RLM tool merely to be callable from a known tree. Never infer intent, applicability, completeness, grounding or answer quality by matching words or phrases in human or AI messages. Use semantic LLM/decision-model assessments with typed outcomes. Never use canned prose templates to manufacture the knowledge work, clarification or successful recovery. Code may parse a documented literal grammar or serialize a schema; justify that concrete contract, and keep output presentation separate from semantic judgment.

Separate **specialist selection** from **alternative methods**. A semantic route chooses an eligible capability; exact guards dispatch it. A fallback tries methods for one goal, with applicability and failure meaning recorded. A selected specialist failure does not make an unrelated specialist eligible. Define an honest no-match/clarification/defer outcome, and check each child’s produced artifact or projected effect against the parent goal.

For each `fallback`, write down why a child may fail, which next child is eligible, and whether the final result still satisfies the **same parent goal**. An explicit success condition can precede an action when repeating it is unnecessary. ORC treats `:partial` as a stopping result in a fallback and a continuation in a sequence; decide whether downstream work can accept that result. Use deterministic conditions for already-typed facts and LLM judgment for meaning. A static condition reads a top-level key; materialize a nested route/boolean with a code transform or write it as a separate typed key before comparison. `llm-condition` maps both a negative judgment and a provider failure to node `:failure`; use `llm-decision` to retain a finite answer and inspect structured failure evidence when these require different responses. Use ordinary `llm` for explanations or unrestricted output, not as a mandatory workaround. State parallel policies and output ownership, and verify effects still in flight after early completion. Classical BTs may continuously recheck guards; ORC's event-sourced execution does not promise continuous polling or preemption of a running provider call. Design an explicit later tick or application trigger for facts that can change after a turn begins.

A finite decision has one write and needs no prose rationale; ordinary generation leaves retain the reasoning-first convention. Use the [decision contracts](../orc-decision-models/references/contracts-and-observability.md) for the consuming revision's assessment evidence and failure behavior.

Recovery must preserve the parent postcondition. Make grounding explicit and expose retrieval failure as evidence. Valid schemas, source-ID membership and exact quotations establish representation and literal provenance; they do not establish that final claims follow from the evidence. Preserve observations, estimates and forecasts as different evidence, including material source qualifications. Use an ordinary typed semantic check on the actual artifact and evidence when unsupported or overstated work could otherwise complete successfully; see [semantic acceptance and bounded repair](references/bounded-repair.md).

For one planned revision, use the [two-attempt repair pattern](references/bounded-repair.md). For evidence-dependent revisits, use the [bounded controller](../orc-compose-specialists/references/authored-controller.md): a terminal condition with `:on-fail :running` **inside `:check`** repeats an isolated child. Keep the business stopping bound below its effective engine cap, including the parent's remaining tick ceiling. Code functions return writes, not node-status control.

Map every semantic assessment outcome to an eligible continuation or an explicit unresolved result. A final rejection guard alone does not implement repair; verify the promised path with a rejected artifact. Assess the full goal after useful subtree execution or a parallel join. Choose satisfied, revise the responsible specialist, consult another eligible known specialist, wait, or hand off using actual outputs and current evidence. Resume the original obligation with a focused packet containing the relevant prior draft, new evidence and feedback. Keep successful independent work and completed effects; revalidate changing evidence and authority before acceptance. Use a finite decision when the choice is sufficient, adding generated feedback only when revision needs it.

For open-ended work with available tools or specialists, read [evidence closure](references/evidence-closure.md). Make unread, unavailable and irrelevant evidence distinguishable, and give every completion checker the relevant evidence-access context—not only the routing node.

## Design artifact and proof

For each specialist and checker, map its responsibility or acceptance criterion to required information, authoritative source, blackboard key and actual model input. Use [context flow](../orc-blackboard-contracts/references/context-flow.md) to preserve material qualifications and cross-branch dependencies. A completion checker needs actual results and evidence for the parent goal, explicit current versus historical effect state, and the completeness scope of any receipt ledger; a routing checker also needs described eligible capabilities. Missing required evidence must remain distinguishable from a satisfied or violated criterion.

Produce a compact tree sketch plus a node contract table: name, goal, node type, data dependencies and effects (use `:reads`/`:writes` only where the DSL supports them; use `:check` for a `condition`), model (DSL `:model` for built-in LLM leaves; native client configuration for model-calling code capabilities), success evidence, failure/recovery behavior. For ordinary LLM leaves, include the described node-specific leading rationale field required by the consuming ORC principles; native finite assessments need no fabricated prose. Mark where a live run and projection read-back will check the result. Cover an ambiguous input, a failed action, an already-satisfied goal, a child returning incomplete work, and a fact changing between ticks. For nested specialists include a goal/contract graph, the leaf-to-root build order, exact delegate seams, per-branch write ownership and bounded recovery. Show how the same child can serve a second caller without knowing either caller’s next step. If the user asks for implementation, continue through the repository's Allium and TDD workflow; do not treat the sketch as a verified tree.

For repeat behavior, show A → B → A for one still-open obligation: B's answer reaches A's new invocation, untouched sibling work remains retained, and the business outcome matches projected state. A successfully reported handoff is not an achieved goal. Source anchors and proof limits are in [authored goal solving](references/authored-goal-solving.md#source-and-proof-boundary) and [BT assembly](references/bt-assembly.md).

For larger registered specialist catalogs, read [specialist discovery](references/specialist-discovery.md) before adding graph or ColBERT selection. Keep eligibility, retrieval recall, semantic selection and delegated task success independently observable.

## Plan judging alongside the behavior

For post-completion quality monitoring, rubric design, custom judge behaviors, score-only decision models or node/subbehavior/tree reports, read [orc-judges](../orc-judges/SKILL.md). Define the assessed goal, evidence and described bands during design. Assess a reusable specialist's own result and the parent task separately: an average of child grades does not prove the parent's postcondition. An inline semantic check that gates revision belongs in the active tree; an asynchronous monitor observes completed work and has its own lifecycle. Consult that skill for current native attachment and scheduling support.

When assessments will guide instruction optimization, follow [judge/GEPA readiness](../orc-judges/references/gepa-readiness.md). A task-specific judge subtree may assess the exact specialist artifact against its own evidence and rubric. Verify example identity and evaluator failures through the optimization path before treating monitoring scores as training fitness.

## Place adaptive research inside the behavior

Use [orc-repl-researcher](../orc-repl-researcher/SKILL.md) when discoveries change the needed strategy or tree shape. Keep known routing, prerequisites, reusable delegates and delivery checks structural in the authored tree. Recursive design–execute–observe–refine is primary; generated trees have a narrower palette than authored ORC. Use [researcher pattern reuse](../orc-researcher-pattern-reuse/SKILL.md) when R-inject or described prior patterns should inform that adaptive design. Retrieval is advice, not registration of a callable specialist.
