---
name: simulator-question-author
description: "Convert a system-design question into two DSDS simulator Markdown guides: a learner-facing builder walkthrough and an author-facing Question Studio walkthrough. Use when mapping an interview or curriculum prompt to feasible simulator components, workloads, grading rules, test-case rows, acceptance designs, and honest modeling boundaries."
---

# Simulator Question Author

Create a coherent pair of walkthroughs from one system-design question:

1. `builder-walkthrough.md` — how a learner builds, configures, runs, and verifies
   the design in the simulator.
2. `question-studio-walkthrough.md` — how an author recreates the question in
   Question Studio, including scenarios, grading, compiled row intent, preview,
   export, and discrimination checks.

The core workflow is plain Markdown and deliberately vendor-neutral. An LLM does
not need Codex or OpenAI-specific tooling to follow it. `agents/openai.yaml` is
optional discovery metadata only.

## Output boundary

- Write exactly the two files above unless the user explicitly requests more
  artifacts.
- Place them in the user-selected directory. Otherwise use
  `examples/<question-slug>/` relative to the documentation root.
- Cross-link the two files with relative links.
- Do not silently create question packages, topology JSON, Django assignments,
  screenshots, or index edits. Those are separate deliverables.
- If the source question must be split into incompatible lessons, ask which
  lesson to document before producing more than one pair. When one lesson clearly
  dominates, choose it and list the deferred concerns in both guides.

## Required input

The minimum input is the raw system-design question. Use provided scale, NFRs,
expected solution hints, and target difficulty when available. When values are
missing, make conservative, visible assumptions that preserve the lesson. Ask a
question only when choosing the dominant lesson or accepted solution family would
materially change the result.

## Source-of-truth order

When the simulator repository is available, resolve disagreements in this order:

1. Executable engine schemas, capability registries, and evaluator code.
2. Current Question Studio renderer controls and compiler code.
3. The support ledger and maintained specifications.
4. Existing examples and older fixtures.

Examples are patterns, not proof that a field or import path still works. Never
copy a legacy package or walkthrough claim without checking the current contract.

Primary repo sources:

- `src/engine/analysis/supportLedger.ts`
- `src/engine/analysis/authoringCapabilities.ts`
- `src/engine/analysis/question.ts`
- `src/engine/analysis/structural.ts`
- `src/engine/analysis/semanticCriteria.ts`
- `src/engine/analysis/rubric.ts`
- `src/engine/analysis/questionAuthoring*.ts`
- `src/engine/runSimulation.ts`
- `src/engine/analysis/fluidModel.ts`
- `src/engine/catalog/paletteTemplates.ts`
- `src/renderer/src/components/authoring/`
- `specs/test-case-catalog.md`
- `specs/support-ledger-and-runtime-semantics.md`

If these sources are unavailable, use the bundled references and explicitly mark
implementation-dependent details for repository validation.

## Workflow

### 1. Translate the lesson

- Normalize the prompt into an architecture task, not an application-coding task.
- Extract every functional requirement, NFR, scale fact, constraint, expected
  tradeoff, and interviewer hint.
- Choose one dominant lesson, bottleneck, workload character, and plausible wrong
  design.
- Read [question-translation-playbook.md](references/question-translation-playbook.md).

### 2. Run the feasibility gate

- Classify each requirement as runtime-simulated, structurally graded,
  semantically inferred, explanation-only, or deferred.
- Check the current support tier and choose discrete or analytic evaluation based
  on the evidence the lesson needs.
- Do not invent simulator support for application logic, transport physics,
  consistency guarantees, provider behavior, or metrics that are not implemented.
- Read [simulator-feasibility.md](references/simulator-feasibility.md).

If the dominant lesson is not honestly representable, stop and explain the
nearest supported reframing instead of writing misleading walkthroughs.

### 3. Design one internal authoring contract

Before writing either file, establish one shared contract in working notes:

- stable title and derived slug;
- question type, entry format, difficulty, domains, concepts, workload category;
- canonical topology and allowed equivalent variants;
- component label-to-type mappings;
- edge model and routing assumptions;
- node capacity derivation and any authored givens;
- workload cases, deterministic seeds, duration, request mix, faults, and
  invariants;
- structural rules, semantic criteria, rubric checks, points, and pass threshold;
- one passing reference design and at least one plausible gamed design;
- unsupported or narrative-only concerns.

Every learner-facing claim and every Question Studio field must derive from this
same contract.

### 4. Design grading and row intent

- Bind every gradeable prompt statement to one real surface: structural,
  semantic, runtime metric, invariant, budget, or justification.
- Treat the four compiled row types and evaluator behavior as a DSL, not prose.
- Prefer structural rules over `topology.*` rubric metrics in the current visual
  Studio, because the advanced verdict selector exposes simulation and invariant
  metrics, not topology metrics.
- Keep raw DSL units distinct from Studio display units; for example, Studio
  error rate `1%` compiles to `summary.errorRate < 0.01`.
- Read [grading-dsl-and-evaluation.md](references/grading-dsl-and-evaluation.md).

### 5. Write the learner builder walkthrough

- Start from [builder-walkthrough.template.md](assets/builder-walkthrough.template.md).
- Give exact placement, configuration, connection, run, and verification steps.
- Include the governing arithmetic and expected results, not just a topology
  picture.
- Explain whether the run is discrete or analytic and which displayed evidence is
  authoritative.
- Separate modeled/graded decisions from narrative tradeoffs.

### 6. Write the Question Studio walkthrough

- Start from
  [question-studio-walkthrough.template.md](assets/question-studio-walkthrough.template.md).
- Use current visible stage and control names.
- Provide exact values for every field needed to reproduce the shared contract.
- Include a traceability table from requirement to Studio control, DSL row/check,
  and evidence.
- Include passing, failing, and anti-gaming acceptance cases.
- Read [question-studio-authoring.md](references/question-studio-authoring.md).

### 7. Enforce the pair contract

Read [walkthrough-pair-contract.md](references/walkthrough-pair-contract.md), then
verify:

- titles, slug, scale, component types, topology, capacity math, workload, and
  expected metrics agree across both files;
- every Question Studio grading rule corresponds to a learner-visible obligation;
- every expected learner result is actually measurable by the selected execution
  mode;
- multiple valid variants are not accidentally excluded;
- unsupported concerns are labeled consistently;
- links resolve and no template placeholders remain.

### 8. Validate against the implementation

When repository execution is available:

- validate component types against the current palette/catalog;
- validate rule kinds and verdict metrics against engine registries;
- compile an equivalent Question Studio project or question package;
- run the passing and gamed designs when topology fixtures exist;
- distinguish validation performed from validation still required.

Do not claim a design passes merely because the Markdown is internally
consistent.

## Quality gates

The pair is complete only when:

- the question has one clear teaching objective;
- every graded requirement has an implemented evidence source;
- every runtime check has a scenario that can produce its metric;
- high-scale questions use analytic evidence only for behavior the fluid model
  supports;
- discrete semantic checks use a tractable workload;
- the author can reproduce the question without guessing field values;
- the learner can reproduce the intended design without hidden configuration;
- one good design passes and one plausible wrong design fails for the intended
  reason;
- the final response reports the two file paths and validation performed.

## Optional modes

- For a separately requested Django assignment, additionally read
  [django-assignment-template.md](references/django-assignment-template.md).
- For use outside an LLM skill system or outside this repository, read
  [portable-usage.md](references/portable-usage.md).
