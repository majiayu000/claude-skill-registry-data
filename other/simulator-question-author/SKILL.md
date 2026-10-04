---
name: simulator-question-author
description: "Convert a system-design question into two DSDS simulator Markdown guides: a learner-facing builder walkthrough and an author-facing Question Studio walkthrough. Use when mapping an interview or curriculum prompt to simulator components, workloads, test-case rows, grading rules, evaluation evidence, and honest modeling boundaries."
---

# Simulator Question Author

This is a standalone, vendor-neutral skill. Everything required for its normal
workflow is inside this directory; do not assume access to a source repository,
another skill, Codex, or an OpenAI product.

The embedded capability and Question Studio snapshot was verified on
**2026-09-21**. If the user supplies newer UI, schema, or runtime documentation,
prefer that evidence and identify any compatibility change.

## Output contract

Given one system-design question, create exactly:

1. `builder-walkthrough.md` — how a learner builds, configures, runs, and verifies
   the design in the simulator.
2. `question-studio-walkthrough.md` — how an author recreates the question in
   Question Studio, including scenarios, grading, compiled row intent, preview,
   export, and discrimination checks.

Place both files in the user-selected output location. If no writable filesystem
is available, return two separately labeled Markdown artifacts with those exact
filenames. Cross-link them using relative links.

Do not create topology JSON, Django assignments, screenshots, indexes, or extra
documents unless the user explicitly requests them.

## Minimum input

The only required input is the raw system-design question. Use supplied scale,
NFRs, solution hints, difficulty, or simulator details when available. Make
conservative assumptions when values are missing and list them visibly. Ask a
question only when the accepted solution family or dominant lesson cannot be
chosen without materially changing the result.

## Embedded source of truth

Use the bundled references in this order:

1. [Simulator feasibility and physics](references/simulator-feasibility.md)
2. [Component and metric catalog](references/component-and-metric-catalog.md)
3. [Grading DSL and evaluation](references/grading-dsl-and-evaluation.md)
4. [Question Studio authoring](references/question-studio-authoring.md)
5. [Walkthrough pair contract](references/walkthrough-pair-contract.md)

The QuickCart files under `examples/quickcart/` are a worked pattern, not a
template to copy blindly.

If an implementation detail is absent from this package, do not invent it.
Choose a supported proxy, make it explanation-only, or label it for validation
against the target simulator version.

## Workflow

### 1. Translate the lesson

- Normalize the prompt into an architecture task rather than application code.
- Extract each functional requirement, NFR, scale fact, constraint, expected
  tradeoff, and interviewer hint.
- Choose one dominant lesson, bottleneck, workload character, and plausible wrong
  design.
- Follow [question-translation-playbook.md](references/question-translation-playbook.md).

### 2. Run the feasibility gate

Classify every source requirement as one of:

- runtime-simulated;
- structurally graded;
- semantically inferred;
- budget-constrained;
- explanation-only;
- deferred.

Choose discrete or analytic execution based on the evidence the lesson needs.
Do not promise application logic, provider behavior, transport physics,
consistency guarantees, or metrics not described in this package.

If the dominant lesson is not honestly representable, explain the nearest
supported reframing instead of writing misleading walkthroughs.

### 3. Create one internal authoring contract

Before drafting either document, establish one shared contract in working notes:

- stable title and title-derived slug;
- question type, entry format, difficulty, domains, concepts, and workload;
- canonical topology and accepted equivalent variants;
- component label-to-type mappings;
- edge modes and routing assumptions;
- resource and capacity derivation;
- workload cases, fixed seeds, durations, request mix, faults, and invariants;
- structural rules, semantic criteria, rubric checks, points, and threshold;
- one passing design, one plausible near miss, and one anti-gaming design;
- unsupported or narrative-only concerns.

Both outputs must be derived from this same contract.

### 4. Design grading and compiled row intent

- Bind every gradeable statement to one implemented surface: structural,
  semantic, runtime metric, invariant, or budget.
- Use exactly the four row types documented in the grading reference:
  `SIMULATOR_CONFIG`, `STRUCTURAL_RULE`, `SEMANTIC_CRITERION`, and
  `RUBRIC_CHECK`.
- Prefer structural rules for topology checks. The visual Studio's advanced
  verdict selector exposes simulation/invariant metrics, not topology metrics.
- Keep human UI units distinct from raw DSL units. For example, Studio error
  rate `1%` corresponds to raw `summary.errorRate < 0.01`.
- Ensure every runtime metric has a scenario capable of producing it.

### 5. Write the builder walkthrough

Start from [builder-walkthrough.template.md](assets/builder-walkthrough.template.md).

The document must provide exact placement, configuration, connection, run, and
verification steps; governing arithmetic; expected good and bad results; the
execution mode; authoritative evidence; and modeling boundaries. Separate
modeled/graded decisions from narrative tradeoffs.

### 6. Write the Question Studio walkthrough

Start from
[question-studio-walkthrough.template.md](assets/question-studio-walkthrough.template.md).

Use the visible stage and control names in the bundled Studio reference. Supply
exact field values, requirement-to-check traceability, compiled row inventory,
preview/export checks, and passing/failing/anti-gaming acceptance cases.

### 7. Enforce the pair contract

Follow [walkthrough-pair-contract.md](references/walkthrough-pair-contract.md) and
compare the files side by side. Titles, slug, scale, component types, topology,
capacity math, workload, faults, thresholds, and expected evidence must agree.

### 8. Validate honestly

Always perform these offline checks:

- no unresolved template placeholders;
- reciprocal relative links resolve;
- all component tokens, rule kinds, semantic kinds, and metrics occur in the
  bundled catalogs;
- request weights total 100%;
- warmup is below duration;
- raw fraction/percentage conversions are correct;
- every graded runtime check has an executable scenario;
- good, near-miss, and anti-gaming designs separate for the intended reason.

If the target environment allows access to Question Studio, additionally compile
the project and run the passing and failing designs. Report offline consistency,
Studio compilation, and behavioral simulation as separate validation levels.
Never claim a design passes merely because the Markdown is internally coherent.

## Completion standard

The task is complete only when:

- the question has one clear teaching objective;
- every graded requirement has a supported evidence source;
- the author can recreate the question without guessing field values;
- the learner can recreate the intended design without hidden configuration;
- one good design passes and one plausible wrong design fails for the intended
  reason;
- both files use the same modeling boundaries;
- the response names the two artifacts and states the validation actually done.
