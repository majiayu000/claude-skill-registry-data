---
name: write-introductions
description: Use when drafting, revising, or auditing an engineering-paper Introduction, especially when the motivation chain is weak, literature detail overwhelms the argument, the scenario does not motivate the method, citations are reused without distinct roles, or contributions overstate the supplied evidence.
---

# Write Introductions

## Purpose

Build an Introduction as a causal argument rather than a compressed literature review or method manual. Reading only the paragraph-opening center sentences should reveal why the problem matters, what precise limitation remains, which scenario or operating condition exposes it, what decision difficulty follows, and why the proposed method needs its stated modules.

## Required resources and routing

1. Always read [the core contract and quality gates](references/core/contract-and-quality-gates.md) in full.
2. Always read [the reader and terminology contract](references/core/reader-and-terminology-contract.md).
3. Read [the house-style card](references/styles/house-style-card.md) unless the user names another venue or team style. It governs author voice, sentence rhythm, connectives, paragraph openers, and the contribution list and roadmap, and it overrides the generic example sentences of this skill where they differ. When drafting or revising, also read Sections 4, 9, and 11 (merging, Introduction openers, contribution list and roadmap) of [the full team house style](references/styles/team-house-style.md); read its other sections only when the card's last table names them.
4. Read [the Chinese manuscript adapter](references/languages/zh.md) when the manuscript is written in Chinese.
5. Read [the MEC domain pack](references/domains/mec.md) only when the manuscript concerns mobile edge computing, UAV-MEC, HAP-UAV, vehicular edge computing, dispersed edge computing, or a directly adjacent MEC setting. It also holds the reference-scale tables for the scale statement.
6. If no domain pack matches, apply the generic workflow and derive domain facts only from the manuscript and supplied sources. Do not treat MEC examples as universal content.
7. Run [the fingerprint script](scripts/style_fingerprint.py) on the draft before delivery when Python is available, with the ranges of the scale statement as `--scale` and the term ledger as `--terms`; `--citations` also lists citation keys repeated within the Introduction. `--spine --section intro` prints the paragraph-opening sentences for the center-sentence audit.

## Workflow

### 1. Establish the problem-method contract

Read the abstract, current Introduction, Related Work, system model, method, contribution list, and relevant bibliography. Write one grounded sentence for each item:

- application importance and concrete operating problem;
- decisive limitation in the closest research line;
- scenario cycle, actors, and decision types (trigger and completion boundary only when needed);
- coupled decisions, objectives, and hard constraints;
- structure that weakens a standard solver;
- proposed module that addresses each stated difficulty;
- evidence that supports each contribution claim.

Do not draft past an unresolved item. Mark it as an evidence or model gap instead of inventing it.

### 2. Build a citation-role ledger

| Claim | Exact source passage | Introduction role | Used elsewhere here? | Proposition | Home paragraph | Keep, merge, or move |
|---|---|---|---|---|---|---|

Verify each claim in the source itself. Assign each source one primary role in the Introduction, use the smallest sufficient citation cluster, and place citations immediately after the proposition they support. If a source appears more than once, retain the repetition only when it supports materially independent claims and record that reason. Detailed paper-by-paper comparisons belong in Related Work. Default: explain a trade-off or gap in one paragraph, and make every other mention one clause; deviate when a second paragraph adds an independent fact, and record the reason.

### 3. Draft the center-sentence spine

Use this generic functional sequence, merging adjacent functions when causality remains clear:

1. field importance and concrete problem;
2. current research focus and decisive limitation;
3. motivation-aligned classification of the closest research;
4. shared boundary that motivates the target setting;
5. target setting, decisions, objectives, and main constraints;
6. method motivation derived from the setting's structure;
7. proposed method and module-to-difficulty mapping;
8. bounded contributions and paper organization.

The sequence is a reasoning contract, not a fixed paragraph count. When the selected domain pack defines a stricter chain, follow it.

### 4. Fill paragraphs at Introduction resolution

Use `primary center sentence -> cause or fact -> necessary evidence -> consequence or transition`. Give each paragraph one main rhetorical job. Keep symbols, equations, protocol branches, exact constraint semantics, implementation steps, and detailed benchmark results in their proper later sections.

Prefer compact paragraphs, but split by rhetorical turns rather than sentence count. A classification paragraph may be longer when every sentence answers the same comparison question.

### 5. Derive the method from the problem

Proceed in this order:

1. name the exact decision or information structure created by the target setting;
2. explain why the general solver family is suitable;
3. identify why its standard form is insufficient;
4. map each proposed module to one stated difficulty;
5. claim only effects supported by the manuscript's analysis or experiments.

Popularity is not method motivation. The solver family is the carrier; the problem-specific mechanism is the reason for the design.

### 6. Close with contributions and audit

Use two or three contributions spanning the paper's actual novelty layers, in the order `scenario/model -> formulation -> method`, with the evidence as the result sentence of the last item. Start each item with an action and new object, then state a bounded effect or validation scope. Follow the house-style contribution and roadmap shapes, and keep the list consistent with the abstract and the Conclusion.

Run the core center-sentence, classification, evidence, citation, paragraph, and module-mapping gates. Then run the selected domain gates. Revise until the Introduction is causal, source-grounded, non-redundant, and clearly separated from Related Work.

## Reader gates (check before delivering)

1. Every coined term is defined by function at first use (T); no variable-like names for decisions or objectives.
2. Every definite expression has an antecedent (A); every action has a purpose or a cost (Q).
3. Each proposition has one home (D); each universal or negative claim is tagged and supported (C).
4. Length is inside the declared scale range, or the deviation is recorded (S).
5. Sentence rhythm and connectives are inside the house-style band, or each remaining flag and its reason are listed in the delivery note, not in the manuscript (R).
6. Ledgers and notes stay out of the manuscript (H).

## Output constraints

- Match the manuscript's language, terminology, notation, and citation format.
- Deliver only the requested prose or audit by default.
- Keep ledgers, term tables, and audit notes out of the manuscript text and appendices unless the user asks for them.
- In an audit, lead with the center-sentence spine and the highest-impact causal or evidence failures.
- Do not modify Related Work, the system model, the method, or the bibliography unless the user authorizes those edits.
