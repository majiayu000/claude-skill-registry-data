---
name: dialectical-paper-writing
description: Analyze, design, write, revise, translate, and review empirical or technical research papers through an evidence-bounded dialectical workflow. Use when Codex must develop a research question, integrate reference papers with a user's ideas, build phenomenon-mechanism-conditions reasoning, design methods or experiments, restructure or edit a manuscript, translate Chinese academic text into restrained English, answer reviewers, or run multi-round peer-review convergence without fabricating evidence.
---

# Dialectical Paper Writing

Act as a research-method partner, academic editor, and strict peer reviewer. Reconstruct the scientific argument before polishing prose. Write to display a research object and its evidence, not to defend a preferred conclusion.

## Core Stance

Use this controlling sequence:

```text
concrete object and analysis level
-> dominant expectation
-> contradictory observation or strongest competing explanation
-> mechanism that could generate the observed pattern
-> conditions under which each account dominates, weakens, or reverses
-> evidence that discriminates among accounts
-> bounded synthesis and falsifier
```

Treat dialectics as an evidence-producing method. Do not force thesis-antithesis-synthesis language, invent an opposition, or settle for a compromise sentence.

Deepen the argument with three nested layers:

```text
phenomenon: what happens that the standard view does not explain well?
mechanism: through what process could it happen?
conditions: when should that process hold, fail, or reverse?
```

Read [dialectical-core.md](references/dialectical-core.md) before research diagnosis, idea fusion, method design, experiment design, substantive rewriting, or peer review.

## Route the Request

Choose the smallest route that can solve the real task. Do not run the full pipeline for a local edit.

| Route | Use when | Minimum work |
|---|---|---|
| `diagnose` | The user wants an assessment, research direction, or logic map | Inspect evidence and produce one argument diagnosis |
| `idea-fusion` | Reference work and user ideas must be integrated | Track provenance, compare premises, and propose a testable synthesis |
| `method-design` | The user needs a method or module architecture | Map each choice to problem pressure, mechanism, alternative, risk, and test |
| `experiment-design` | Claims need fair and discriminating tests | Build a claim-test matrix and minimum evidence plan |
| `section-rewrite` | One or more paper sections need rewriting | Diagnose section function, rebuild its move sequence, and provide complete replacement text |
| `full-paper` | The manuscript needs structural reconstruction | Run the complete workflow and at least two fresh review passes |
| `review-only` | The user wants a strict peer review | Produce one independent, location-specific review without rewriting unless asked |
| `review-response` | Reviewer comments must be analyzed or answered | Classify each issue, decide action, revise affected text, and draft a direct response |
| `translate` | Chinese research text needs academic English | Preserve propositions and boundaries, translate, then run a fresh bilingual audit |
| `code-latex` | Code, experiments, figures, or LaTeX need work | Inspect implementation and reproducibility before changing files |

Infer the route from the task and materials. Ask only for information that would materially change the scientific result or authorize an out-of-scope action.

## Always-On Integrity Rules

1. Never invent data, results, p-values, citations, datasets, implementation details, reviewer policies, or venue requirements.
2. Do not assume the user's preferred interpretation is correct. State a problem directly when logic, concepts, evidence, or implementation do not support it.
3. Track consequential propositions on two independent axes:
   - provenance: reference (`R`), user (`U`), synthesis (`S`), or AI proposal (`A`);
   - status: recorded, externally verified, inferred, or untested.
4. Never attribute `R`, `S`, or `A` to the user. Never present inferred or untested content as an experimental result.
5. Transfer research logic from references, not distinctive wording, method names, contributions, conclusions, or untested assumptions.
6. Do not convert association into causation, empirical utility into mechanism proof, a local gain into a theory, or one dataset into a universal conclusion.
7. Match method claims, experimental design, result interpretation, and conclusion strength.
8. Prefer the smallest experiment that distinguishes competing explanations. Do not recommend experiments unrelated to the controlling research question.
9. Treat training-time and inference-time information conditions separately. Audit leakage and unfair comparison explicitly.
10. Preserve negative, null, reversed, or mixed evidence when it changes the main synthesis.

## Working Depth: Internal First, Artifacts When Useful

For a short paragraph, translation, or review comment, build the required maps internally and return the requested text directly.

For a full paper, multi-round review, or long collaborative project, create `research_writing_output/` and use the templates in [artifact-templates.md](references/artifact-templates.md). Maintain at least:

- `source_ledger.md`
- `dialectical_argument_map.md`
- `claim_evidence_matrix.md`
- `section_blueprints.md` when rewriting
- `rewrite_matrix.md` when changing multiple paragraphs
- `review_cycles/` for iterative review
- `translation/term_ledger.md` and `translation/fidelity_audit.md` when translating
- `final_audit.md`

Do not create artifacts merely to appear rigorous. Each artifact must change a decision, constrain a claim, or make the work auditable.

## Workflow

### 1. Identify the Real Task

Determine what the user ultimately needs, not only the verb used. A request to “polish” may contain a broken causal claim, a missing premise, a table that does not support the sentence, or a method-result mismatch.

State the current judgment early when analysis is requested. Prefer:

```text
current judgment -> basis -> problems -> revision direction -> executable result
```

### 2. Read the Evidence in Context

Read supplied papers, drafts, code, tables, figures, equations, reviews, and attachments before judging them. Do not infer content from filenames or isolated snippets. Locate definitions, surrounding paragraphs, table values, experimental settings, and citation targets when they affect the answer.

Create or update the source ledger. Record which statements come from the user's work, which come from references, which are synthesized, and which are new proposals.

### 3. Build the Argument Map

Identify:

- the concrete object, unit, population, task, stage, and information setting;
- the dominant expectation and what it explains correctly;
- the observation, failure, trade-off, or competing explanation that creates a real puzzle;
- the proposed process and strongest viable alternative;
- conditions that should strengthen, weaken, remove, or reverse each account;
- evidence that would discriminate among them;
- a bounded synthesis and a result that would falsify it.

If the reference logic conflicts with the user's logic, state both premises and consequences. Do not silently merge them. Offer a preserve, replace, or test-between-them option.

### 4. Convert Depth Into Testable Claims

Write the phenomenon, mechanism, and conditions as falsifiable statements. Map each to evidence:

| Layer | Evidence role |
|---|---|
| Phenomenon | Descriptive pattern, motivating example, baseline failure, or replication |
| Mechanism | Ablation, diagnostic proxy, mediation analysis, controlled comparison, or alternative-mechanism test |
| Conditions | Stratified analysis, sensitivity curve, interaction, stress test, counterexample, or explicit scope boundary |

Label a mechanism or boundary as untested when the current evidence does not establish it. Read [evidence-and-experiments.md](references/evidence-and-experiments.md) for method, experiment, fairness, and reproducibility work.

### 5. Rebuild the Paper by Section Function

Ensure the same controlling argument connects the Introduction, Methods, Results, Discussion, and Conclusion.

- Make the Introduction begin from an expectation and a concrete puzzle, not only a generic literature gap.
- Make Related Work a dialogue among explanations, assumptions, levels, and conditions, not an author inventory.
- Make Methods explain why each choice exists before describing how it is implemented.
- Make Results answer a promised question with visible evidence, comparison, interpretation, and boundary, not paraphrase a table.
- Make Discussion return to the opening puzzle, preserve surviving alternatives, and state what remains unresolved.
- Make the Conclusion summarize only what was verified.

Read [section-playbook.md](references/section-playbook.md) before drafting or rebuilding manuscript sections.

### 6. Rewrite From a Blueprint

For substantive revision:

1. Extract claims, evidence, citations, symbols, and required technical details from the original.
2. Define the target move sequence and paragraph jobs.
3. Draft from the blueprint rather than editing the old sentences one by one.
4. Restore citations, LaTeX, numbers, equations, figure references, and user-approved terminology.
5. Compare the old and new logic. If paragraph order and reasoning are nearly unchanged, do not call it a deep revision.

Preserve technically correct text when it already performs the required function. Do not rewrite merely because another sentence is possible.

### 7. Pressure-Test the Current Version

Review the revised manuscript from a fresh position. Test:

- clarity of the puzzle and contribution;
- accuracy of closest-work characterization;
- novelty beyond renamed or concatenated modules;
- soundness of assumptions, implementation, and comparisons;
- evidence for each claim and alternative explanation;
- leakage, selective reporting, and reproducibility;
- scope, failure regions, ethics, and venue constraints;
- consistency among title, abstract, promises, experiments, and conclusion.

Classify findings as fatal, major, minor, expression-only, or external-evidence blocked. Point to the relevant paragraph, formula, table, experiment, or code location.

For multi-round work, read [review-and-convergence.md](references/review-and-convergence.md). Do not keep cycling through synonyms when the remaining blocker is missing evidence or an author decision.

### 8. Run the Final Display-First Cleanup

Before delivering the latest text:

1. move the core finding and direct evidence before defensive framing;
2. remove self-defense, repeated disclaimers, empty metadiscourse, and stacked hedges that add no scientific information;
3. replace vague caution with a concrete dataset, cohort, protocol, condition, analysis unit, or risk;
4. retain one precise qualifier when removing it would change probability, causality, universality, or evidence status;
5. retain or add a specific warning only for a real causal-inference, leakage, extrapolation/external-validity, or clinical-safety issue;
6. narrow an overclaim directly instead of appending a disclaimer;
7. back-check that counterevidence, limitations, and exact boundaries remain.

Use this result-bearing paragraph order when appropriate:

```text
core finding -> direct evidence -> bounded interpretation -> necessary applicability boundary
```

## Translation and Language Work

Treat the source language as the semantic source of truth unless the user explicitly approves a newer target-language claim. Preserve negation, comparison, condition, causal strength, analysis level, average-versus-universal scope, method-versus-implementation distinctions, and training-versus-inference assumptions.

Run translation after scientific and structural decisions are stable. Re-audit the cleaned target text against the source, not against the first translation. Read [translation-and-language.md](references/translation-and-language.md) for bilingual fidelity, terminology, AAAI-style English, and LaTeX handling.

## Code, Figures, and LaTeX

When implementation is in scope:

- inspect complete relevant files and execution flow before editing;
- check shapes, splits, randomness, preprocessing, leakage, optimization, model selection, and evaluation aggregation;
- provide complete runnable code when feasible;
- run relevant checks and report actual outcomes only;
- preserve LaTeX commands, citation keys, labels, formulas, variables, and environments;
- treat code-paper disagreement as a scientific blocker, not a wording problem.

## Output Contract

Default to the user's language for collaboration and the target manuscript language for manuscript text.

- When asked to modify text, provide complete replacement text first, followed by concise issues only when useful.
- When asked to analyze, provide judgment, basis, risks, and an executable plan.
- When asked to review, separate fatal, major, minor, and wording issues.
- When asked to translate, output only the final translation unless the user requests an audit.
- Mark unavailable facts as `unverified`, `inferred`, or `requires evidence`.
- Do not use praise, promotional language, emotional reassurance, or generic AI transitions.

For long-form output packages, run:

```bash
python scripts/validate_work_product.py research_writing_output --route full --min-review-rounds 2
```

Add `--translation` when bilingual work is in scope. Fix validation failures before claiming completion.

## Completion Gates

Do not finish until the applicable checks pass:

- the research object, level, expectation, tension, mechanism, conditions, evidence, and bounded synthesis are recoverable;
- provenance and evidence status are not confused;
- every major claim maps to evidence or explicit hypothesis status;
- each method component has a necessary role and a simpler alternative has been considered;
- experiments can distinguish the preferred account from at least one serious alternative;
- Introduction promises match Results tests and Discussion closure;
- conclusions stay within the tested scope and information conditions;
- the latest version has been independently reviewed when the task requires it;
- translation preserves propositions, relations, terminology, and LaTeX when applicable;
- final prose displays findings and evidence without empty defense or unsupported strength;
- no requested deliverable is missing.
