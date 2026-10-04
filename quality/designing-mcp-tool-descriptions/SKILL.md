---
name: designing-mcp-tool-descriptions
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P008
  - P010
  - P013
  - P021
  - P024
  - P026
  - P027
  - P028
  - P033
  - P037
  - P038
  - P043
  - P044
  - P045
  - P046
  - P047
  - P049
  - P054
  - P055
  - P057
  - P058
  - P060
  - P070
  - P071
  - P081
  - P085
  - P090
  - P091
  - P092
  - P124
  - P125
  - P126
  - P138
  - P144
  - P145
  - P149
  - P150
  - P189
  - P195
  - P196
  - P197
  - P198
  - P199
  - P200
  authored_from_digest: ff6f20c9fc2d7561b73f71e732ff069a4cf3dd8c1f3dec56ff1b7cccc5ff94a0
---

# Skill: designing-mcp-tool-descriptions

## Purpose

Design and review the model-facing surface of an MCP tool — its name, description, parameter
schema, annotations, and examples — so the model selects the right tool and builds valid arguments.
The name+description+input-schema is the primary, often only, basis the model has for a call, so its
quality sets the ceiling on tool use [P010], [P091], [P153].

## When to use

- Authoring a new MCP tool, or reviewing an existing tool's description and schema.
- A model picks the wrong tool, skips a step, or emits malformed or missing arguments.
- Auditing a tool surface for description smells or missing components.

## Procedure

1. **Treat name + description + schema as the selection lever.** Keep instructions simple and precise;
   assume description quality is poor by default and always review it — in a large study 97.1% of
   descriptions carried at least one smell [P010], [P033], [P006].
2. **Minimize and disambiguate the tool set.** Expose as few tools as you can (every name, description,
   schema, and annotation loads into context and taxes reasoning); give each tool a unique,
   semantically meaningful name distinct within its namespace [P008], [P047].
3. **Score against a component rubric, not a yes/no check.** Grade each component on a 5-point scale with
   3 as minimum viable; always retain Purpose and select the minimal effective component set per
   domain–model pair [P090], [P046], [P070].
4. **Fix the most prevalent smells first.** Prioritise Unstated Limitations (~90%), Missing Usage
   Guidelines (~89%), and Opaque Parameters; state only implemented behaviour and cut hedge words,
   redundancy, and clutter [P044], [P006], [P058].
5. **Ground examples and limitations in real executions.** Do not write Examples or full Limitations from
   the description alone — ground them in observed executions and, where possible, the tool's source
   code; use input examples to teach conventions a schema cannot express [P055], [P057], [P049].
6. **Get arguments and optional fields right.** Validate parameters against each tool's constraints before
   invoking, and omit optional fields with empty values unless the schema defines a default [P013], [P109].
7. **Make description authoring a first-class engineering phase.** Run rubric-based smell detection in
   review or CI as a blocking criterion; diagnose wrong-tool selection and bad arguments as a
   specification problem in the description, not a model failure [P045], [P071], [P138], [P200].

## Pitfalls / anti-patterns

- Assuming an official or vendor server's descriptions are good — study data shows they usually are not [P033].
- Editing a description without measuring the effect; use execution-based metrics (see
  mcp-evaluation-and-judge-reference) [P056].
- Dropping Purpose to save tokens — it is the one component to always retain; prune Examples, then
  Parameter Explanation, first [P046], [P198], [P199].

## Principles applied

- **[P006]** Keep tool descriptions accurate and precise: state only implemented behavior, concrete constraints, parameter meanings, and boundaries, while removing ambiguous, contradictory, or self-referential wording.
- **[P008]** Minimize the number of tools an MCP server exposes: every tool's name, description, parameter schema, and annotations load into the model's context on connect and tax reasoning before any prompt, and benchmark evidence shows task efficiency drops (>10 points) as tool-selection complexity rises.
- **[P010]** Treat an MCP tool's name, description, and parameter specification as the primary lever for correct tool selection: keep instructions simple and precise, and expect that even small description edits — tightening wording, adding/removing a tool, or merging similar tools — can move evaluation results significantly, while inaccurate descriptions cause wrong-tool choices, skipped steps, and malformed or missing arguments.
- **[P013]** Validate tool-call parameters against each tool's constraints before invoking it; a common failure is violating parameter rules such as setting identical start and end dates where the tool requires them to differ.
- **[P021]** Define and register MCP tool and prompt schemas with JSON Schema 2020-12, directly or through a compatible schema library such as Zod/Standard-Schema.
- **[P024]** Treat tool-description augmentation as useful but not universal or free: apply it adaptively by domain and model while budgeting for higher execution steps and token use and watching for regressions.
- **[P026]** Prioritize remediation by measured impact on tool selection — functionality first (+11.6%), then accuracy (+8.8%), then information completeness (+5.9%), then conciseness (+1.5%) — and adjust for query specificity: emphasize a clear, distinct functional description for underspecified queries and thorough completeness for detailed queries.
- **[P027]** When building tasks to ground or evaluate a tool, write self-contained plain-English questions with a single unambiguous answer reachable in one tool call, specifying all inputs, varying values across tasks, and spanning medium/hard/very-hard difficulty; then synthesize Examples and Limitations strictly from the observed executions, each example a real observation with exact arguments and response (preferring edge and error cases) and each limitation a tool-specific fact seen in a trace, never invented, never generic API advice, and never a verbatim repeat of the description.
- **[P028]** Prioritize MCP validation and review effort by combining repository frequency with practitioner-confirmed severity and diagnostic effort: treat frequency counts as descriptive of the studied corpus rather than ecosystem prevalence, and remember that a rarely reported category (such as Authorization or other Security faults) can still be high severity while frequent categories cluster in Tool execution and data-schema enforcement.
- **[P033]** Assume tool-description quality is poor by default and always review it: in a large empirical study 97.1% of descriptions carried at least one smell and 56% failed to state purpose clearly, where a smell is a recurring component-specific pattern that degrades clarity, correctness, or maintainability without being an outright fault.
- **[P037]** Drop the Examples component first when trimming a description: removing it did not significantly degrade performance and even slightly improved cross-domain consistency, consistent with Anthropic's deprioritization though contrary to generic few-shot expectations; keep examples only where a tool is unfamiliar or complex enough to benefit.
- **[P038]** Expect the recurring cross-case failure signature in deployed MCP vision toolchains: semantic misalignment despite valid schemas, fragmented spatial and temporal representations, and shallow wrappers unable to manage implicit state (evidenced across ParaView, SUMO+YOLO, ALITA, FHIR, and Blender case studies).
- **[P043]** Write tool descriptions with all core quality components present and viable: purpose, usage guidance, limitations, parameter details, and self-sufficient prose, with examples only supplementing the description.
- **[P044]** Prioritize the most prevalent smells when reviewing descriptions: Unstated Limitations (~90%), Missing Usage Guidelines (~89%), and Opaque Parameters (~84%) dominate, only ~2.9% of descriptions are fully smell-free, and completeness drops sharply as more components are required, so most descriptions lack boundary conditions, when/how-to-use guidance, and parameter insight.
- **[P045]** Treat tool descriptions as first-class engineering artifacts: run rubric-based smell detection in review or CI as a blocking release criterion, fix the highest-leverage components first, add examples or exhaustive parameter detail only where they justify their token cost, and use manual refinement for small servers but reviewed semi-automated augmentation for large ones, always resolving ambiguity without inflating the token footprint past its efficiency payoff.
- **[P046]** Select the minimal effective component set for each domain-model pair, always retaining Purpose: there is no universal 'golden' combination, but a pruned combination that keeps the core purpose and the most relevant constraints solves largely the same tasks as full augmentation (strong statistical agreement) while cutting tokens and latency, provided the pruning is tailored to the domain.
- **[P047]** For Functionality, make the tool distinct within a shared namespace: give it a unique, semantically meaningful name (not a generic utility name such as read_file or get_data), a clear functional description, and explicit trigger conditions stating when this tool should be prioritized over similar tools.
- **[P049]** Use tool input examples to teach conventions that schemas cannot express, including optional-field patterns, nested object usage, correlated parameters, and similar-tool disambiguation.
- **[P054]** Return results processed enough to be directly usable, but keep the underlying source detail — raw unprocessed dumps force the LLM into error-prone guesswork, while summarize-only output that hides the originals leaves no recovery path when the server's own analysis is wrong.
- **[P055]** Do not write Examples or the full Limitations from the description alone; ground them in observed tool executions by generating at least one success task and one error task per tool plus edge cases (prioritizing harder cases first), because an FM cannot reliably infer them without traces and augmentation must preserve the tool's original meaning and intent.
- **[P057]** Use source-code grounding as a reliability safeguard for tool-description faithfulness, especially for behavior- and input-tied components, while not assuming it will always improve task success.
- **[P058]** For Conciseness, maximize signal-to-noise: remove redundant or repeated content, irrelevant clutter, needless technical jargon, and useless qualifiers, because verbosity inflates token cost and dilutes model attention — while treating conciseness as the lowest-impact of the four dimensions.
- **[P060]** Build the registry entry deterministically from the repository: clone it, derive metadata (uuid id, README-based description, GitHub repository fields), set version from the container image tag with is_latest true, model packages as a single docker entry, and store the result in registry.json conforming to the MCP registry OpenAPI schema.
- **[P070]** For Information Completeness, document everything the agent needs to build a valid call and interpret the result without guessing: every parameter and its type, the return values, side effects, and error handling; omitting return-value descriptions forces zero-shot output handling and invites hallucination.
- **[P071]** Treat description authoring as a first-class engineering phase, co-equal with implementation and testing (like API contract design); avoid the code-first, description-last pattern, which measurably degrades tool discoverability and invocation accuracy.
- **[P081]** Beyond the CLI, validate containerized servers through the container runtime (e.g. podman/docker) and embed validation programmatically via the API (validate_server / validate_mcp_server_command) when automating.
- **[P085]** Advise MCP users to treat tool descriptions as mutable client-side configuration they can override at runtime without changing server code, using high-quality descriptions as a cost lever that can let a smaller, cheaper model reach parity with a larger one in a target domain before defaulting to a bigger model, since descriptions are a critical but under-engineered artifact best managed as a configurable engineering asset.
- **[P090]** Score each component on a graded (5-point) scale rather than a yes/no check, treating 3 as the minimum viable threshold, 4-5 as increasing precision and clarity, and a mean below 3 as a detected smell, because a component can be present yet semantically ambiguous or sub-optimal.
- **[P091]** Treat the tool description, together with its name and input schema, as the primary and often only basis an LLM has for selecting a tool: implementation is unobservable, so selection is driven by the semantic alignment between the query and the description.
- **[P092]** Expect substantial, measurable payoff from a standards-compliant description: among functionally equivalent competitors, a compliant server wins selection about 72% of the time versus a 20% uniform baseline (a 260% relative increase), consistently across domains and query-complexity levels.
- **[P124]** Prefer a declarative natural-language interface over a raw structured-query parameter, moving query construction (e.g. text-to-SQL) inside the server; the gain is large when the LLM's query construction is the accuracy bottleneck (PostgreSQL +22 points) and small when it is not (MySQL +2 points).
- **[P125]** Ground FM-based augmentation in implementation evidence: supply the tool's source-code slice together with the original description and input schema and instruct the model to invent nothing unsupported, because underspecified inputs otherwise lead the augmentor to hallucinate fluent but inconsistent details, especially for the prompt-generated Purpose, Guidelines, and Parameter Explanation.
- **[P126]** Also avoid vague hedge words (for example maybe or probably), keep terminology consistent, and keep wording understandable to the model; these general documentation qualities matter, but for short MCP descriptions they are secondary to the four core dimensions and were not among the mapped MCP smells.
- **[P138]** Diagnose wrong-tool selection, invalid or over-broad arguments, and unnecessary steps as a specification problem in the tool description, not a model bug, since defective, underspecified, or misleading descriptions directly cause these failures.
- **[P144]** Interpret a rubric smell as a potential risk signal, not a deterministic predictor of failure: whether a missing component actually hurts depends on tool complexity, task difficulty, available context budget, and the model's prior exposure to the tool, API, or domain.
- **[P145]** Bring all resizing, unit conversion, and schema coercion inside declared tool contracts; undocumented out-of-band bridging scripts (41% of deployments) break interpretability and trace-based recovery.
- **[P149]** When enabling code-driven tool use, explicitly opt in only appropriate tools and keep their raw results inside the code-execution flow until the final output is ready.
- **[P150]** Design expressive tool, script, and file interfaces (clear, self-describing parameters) instead of supplying usage examples, because examples can constrain a capable model to a narrow exploration space.
- **[P189]** When automatically scoring tool descriptions, apply a well-defined analytic rubric (more consistent than open-ended prompts) via a multi-model LLM jury drawn from disparate model families to mitigate single-model bias; such rubric scoring aligns with human judgment at substantial agreement.
- **[P195]** Avoid silently truncating results or returning snippets too thin to answer with; truncation can drop the correct span and insufficient descriptions force a second fetch, both degrading accuracy and efficiency.
- **[P196]** Ensure every tool description clearly states its purpose (the function, behavior, and return data), guides the FM on when and how to use the tool, and includes relevant caveats; a bare purpose statement without behavioral or output detail is only minimally viable.
- **[P197]** Apply the same description-quality discipline to Agent Skill metadata: because progressive disclosure loads only the Skill's name and summary at startup to decide activation, that description metadata determines whether the correct Skill is discovered, so author it with the same accuracy, functionality, completeness, and conciseness rigor.
- **[P198]** When the context budget is tight, prune Parameter Explanation before other components: the MCP input schema already supplies parameter names and types at runtime, the component often duplicates that information, and including every component can otherwise inflate context and reduce efficiency.
- **[P199]** Treat Examples as the lowest-priority component and the safest to omit under constraints: their value is contested, they scored only moderate inter-rater reliability, and they can be too large to fit the context window.
- **[P200]** Diagnose tool-selection failures by mode: an under-specific or vague description causes missed invocation (the correct tool is not selected), whereas an over-general or ambiguous description causes erroneous selection (a wrong tool is chosen); remediate by increasing specificity and disambiguating.

Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.

