---
name: clarify-research-idea
description: Turn vague or partially formed AI, computer-science, data-driven, and engineering-method research directions into evidence-grounded, falsifiable, paper-ready Research Idea Briefs through heuristic questioning, staged confirmation, literature positioning, novelty attack, and method-figure planning. Use when the user needs to clarify a research idea, formalize inputs/outputs/objectives/constraints, frame background and motivation, select 3-5 anchor papers, identify a defensible gap, derive 2-3 contributions, stress-test novelty, or design an input-to-output method framework and core-paper figure. Also trigger on requests such as 明确科研 idea、启发式梳理 idea、互动追问科研问题、梳理论文创新点、定义研究任务、找对标论文、把研究方向变成论文方案、画方法框架图. Do not use as the primary workflow for running experiments, exhaustive systematic reviews, drafting full manuscript sections, or polishing finished prose.
---

# Clarify Research Idea

Convert an early research direction into an auditable idea architecture before detailed experiment design or manuscript writing. Preserve the researcher's judgment: make assumptions and framing visible, challenge weak novelty, and never manufacture supporting evidence.

## Choose the operating mode

Use `guided` by default when the question, gap, or method is uncertain. Ask one high-information question at a time, maintain a visible working draft, and pause at the three checkpoints.

Use `synthesize` when the user supplies enough material or explicitly requests a one-pass result. Complete the brief with labeled assumptions; mark checkpoint-dependent claims `UNCONFIRMED` and request confirmation at the end.

State the selected mode, research domain, maturity level, and intended deliverable in one short line. Let the user correct them cheaply.

## Run the heuristic interaction loop

Read [interactive-heuristics.md](references/interactive-heuristics.md) in `guided` mode, whenever the user's idea is vague, or whenever the user asks for interactive clarification. Treat interaction as part of the method, not as casual clarification.

Use this turn pattern:

1. State the current bottleneck in one sentence.
2. Ask one high-information question that will change the idea architecture.
3. Offer 2-3 plausible answer directions when the user is unsure.
4. Update the visible `Working Idea Canvas` with provenance labels before asking the next question.

Do not overwhelm the user with a survey. If multiple questions are useful, choose the one that best constrains the task, gap, hypothesis, or evidence path. If the user asks for a fast one-pass result, switch to `synthesize` and mark unconfirmed decisions explicitly.

## Maintain provenance

Label substantive content throughout the workflow:

- `PROVIDED`: stated or supplied by the user.
- `VERIFIED`: supported by a checked primary source or supplied artifact.
- `INFERRED`: reasoned from available material but not directly established.
- `PROVISIONAL`: useful working hypothesis awaiting evidence or user confirmation.
- `UNKNOWN`: missing and consequential.

Do not silently upgrade one status to another. When browsing or academic-search tools are available, verify time-sensitive literature claims and bibliographic metadata. Treat failure to find a paper as search incompleteness, not proof of novelty.

## Run the workflow

### 0. Scope the session

Determine the application, research object, current idea, intended venue or audience, available data or system, resource limits, and desired output language. Stay centered on AI, computer science, data-driven science, and engineering-method papers. If the request is primarily qualitative or non-methodological, explain that the mathematical contract must be adapted before continuing.

Identify whether the user has: a broad interest, a question without a task definition, a method without positioning, anchor papers without a gap, or a nearly complete idea needing audit. Use the maturity triage in [interactive-heuristics.md](references/interactive-heuristics.md) to choose the first question. Reuse supplied documents and prior decisions instead of re-asking settled questions.

### 1. Establish the Task Contract

Read [task-formalization.md](references/task-formalization.md). Define the inference-time inputs, required outputs, data or interaction process, model or decision function, objective, constraints, evaluation measures, baselines, assumptions, and explicit exclusions. Use mathematical notation only when it removes ambiguity; do not invent a loss function for appearance.

Require alignment among the claimed problem, information available at use time, optimization target, and evaluation metric.

**Checkpoint 1 — Task Contract:** Present the one-sentence task, compact formulation, success criterion, assumptions, and scope boundaries. In `guided` mode, obtain user confirmation before treating the contract as fixed.

### 2. Make the argument and framing explicit

Read [framing-and-motivation.md](references/framing-and-motivation.md). Build the chain:

`background -> consequential friction -> unresolved cause -> required capability -> proposed research move`

Record the intended reader update, the current default view, and the strongest counter-position in a `Framing Intent` block. Allow framing to guide emphasis and argument order, but never let it bias evidence retrieval, omit material counterevidence, or turn a hypothesis into a fact.

Express each challenge as a causal requirement, not an adjective: property of the setting -> technical difficulty -> why generic methods fail -> capability the solution must provide.

### 3. Position against 3-5 anchor papers

Read [anchor-paper-positioning.md](references/anchor-paper-positioning.md). Select papers by role rather than fame: problem anchor, method anchor, closest competitor, experiment anchor, and optional writing/architecture anchor. A paper may fill more than one role.

Verify title, authors, year, venue or repository, and DOI or stable URL. Extract `WHY / HOW / WHAT / LIMIT / TRANSFER` for each paper. Compare task assumptions and evidence, not only module names. Derive high-level writing characteristics without copying distinctive wording.

### 4. Derive and attack the idea

Read [novelty-and-falsification.md](references/novelty-and-falsification.md). Consider three routes: a genuinely new problem, an old problem with an ignored condition or failure mode, or new evidence/understanding that changes a boundary. Force each candidate through:

`observed gap -> underlying cause -> design principle -> method component -> expected evidence`

Generate alternatives only when they help the user choose. Reduce the selected idea to one core hypothesis and 2-3 contribution cards. Attack it with the closest existing method, the simplest plausible baseline, alternative explanations, confounds, negative cases, and feasibility limits. In `guided` mode, run the reviewer-simulation questions from [interactive-heuristics.md](references/interactive-heuristics.md) before treating a contribution as stable.

**Checkpoint 2 — Positioning and Hypothesis:** Present the verified anchors, defensible gap, rejected alternatives, core hypothesis, and falsifier. In `guided` mode, obtain user confirmation before freezing the method architecture.

### 5. Design the method architecture and core figure

Read [framework-figure.md](references/framework-figure.md). Map every challenge to a design principle, every principle to a component or procedure, and every component to a claim and validation hook. Build an editable textual specification and a Mermaid draft using:

`context/input -> problem structure -> method components -> objective/constraints -> output -> evidence`

Keep the figure causal and selective. Do not add decorative modules merely to make the method look complex. If the user requests an actual `.pptx`, hand the approved figure specification to a presentation-generation workflow rather than making PowerPoint a hidden dependency of this skill.

### 6. Compile and audit the Research Idea Brief

Read [output-schema.md](references/output-schema.md). Produce one coherent brief, not disconnected brainstorming notes. Include the Task Contract, Framing Intent, anchor-paper matrix, gap, hypothesis, contribution cards, challenge-solution map, method architecture, claim-evidence matrix, Mermaid figure, falsification plan, risks, and unresolved decisions.

Score readiness on clarity, positioning, novelty, feasibility, falsifiability, and claim-method-evidence consistency. Treat the score as a diagnostic, not scientific proof. Include the final `Working Idea Canvas` and checkpoint decisions so later experiment-design and paper-writing workflows can inherit the reasoning path. Do not declare the idea ready while a critical item is `UNKNOWN`.

**Checkpoint 3 — Final Idea Architecture:** Ask the user to approve or revise the final hypothesis, contributions, method figure, and unresolved high-risk assumptions. Mark the brief `CONFIRMED`, `PROVISIONAL`, or `BLOCKED` accordingly.

## Enforce integrity rules

- Never fabricate papers, identifiers, results, datasets, mechanisms, novelty, or feasibility.
- Never present desired rhetorical direction as empirical evidence.
- Never claim novelty solely because the current search did not find prior work.
- Never define a contribution with prestige adjectives such as “novel,” “robust,” or “comprehensive” without a concrete difference and validation path.
- Bind every contribution to an observable claim and at least one fair comparison, ablation, diagnostic, stress test, or boundary test.
- Preserve inconvenient counterevidence and explain whether it weakens, redirects, or bounds the idea.
- Prefer a simpler idea when it explains the same challenge with fewer assumptions.

## Handoff boundary

Stop after the confirmed Research Idea Brief and core-figure specification. Provide experiment hooks, not a fully executed experiment campaign. Route exhaustive literature reviews, detailed experiment implementation, full manuscript drafting, language polishing, and final PPT production to their corresponding workflows while carrying forward the confirmed Task Contract, claim-evidence matrix, anchor papers, and decision status.
