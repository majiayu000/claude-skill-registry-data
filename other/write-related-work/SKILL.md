---
name: write-related-work
description: Use when drafting, revising, or auditing an engineering-paper Related Work section, especially when it reads as a paper-by-paper list, repeats the Introduction, mixes classification criteria, asserts gaps without evidence, or fails to connect grouped literature boundaries to the paper's model and method.
---

# Write Related Work

## Purpose

Use Related Work as the evidence layer of the paper's motivation. Organize prior work by mechanisms that matter to the target problem, establish what each research line already supports, and end each line at the exact assumption or capability boundary that motivates the paper.

## Required resources and routing

1. Always read [the core contract and quality gates](references/core/contract-and-quality-gates.md) in full.
2. Always read [the reader and terminology contract](references/core/reader-and-terminology-contract.md).
3. Read [the house-style card](references/styles/house-style-card.md) unless the user names another venue or team style. It governs author voice, sentence rhythm, connectives, subsection titles, and paragraph openers, and it overrides the generic example sentences of this skill where they differ. When drafting or revising, also read Sections 8 and 9 (titles and Related Work openers) of [the full team house style](references/styles/team-house-style.md); read its other sections only when the card's last table names them.
4. Read [the Chinese manuscript adapter](references/languages/zh.md) when the manuscript is written in Chinese.
5. Read [the MEC domain pack](references/domains/mec.md) only for mobile edge computing, UAV-MEC, HAP-UAV, vehicular edge computing, dispersed edge computing, or directly adjacent MEC settings. It also holds the reference-scale and citation-recovery tables.
6. If no domain pack matches, derive the classification axes and terminology from the target manuscript and verified literature. Do not import MEC taxonomies into another field.
7. Run [the fingerprint script](scripts/style_fingerprint.py) on the draft before delivery when Python is available, with the ranges of the scale statement as `--scale` and the term ledger as `--terms`. `--spine --section related` prints the paragraph-opening sentences for the center-sentence audit.

## Governing distinction

- **Introduction:** a category-level map that establishes importance, focus, and motivation.
- **Related Work:** paper-level evidence that validates the map and delimits the unresolved boundary.

Begin from the focus already established in the Introduction. Do not replay the complete motivation chain or pre-write the proposed method.

## Workflow

### 1. Recover the paper's claim chain

Read the Introduction, contribution list, model, method, and relevant bibliography. Extract:

1. the target operating condition;
2. the modeled mechanism that closest work omits or simplifies;
3. the algorithmic difficulty created by that mechanism;
4. the proposed module that addresses each residual difficulty.

Mark unknown items as evidence gaps. Do not infer them from titles.

### 2. Build a coverage matrix

| Literature axis | One classification criterion | Categories | Representative evidence | Residual boundary | Paper need motivated |
|---|---|---|---|---|---|

Every subsection needs one explicit comparison axis. Every boundary must follow from the papers discussed immediately before it. Every major motivation in the paper must have a defensible home in the matrix.

### 3. Choose motivation-aligned axes

Use the smallest set of axes that mirrors the paper's argument. Typical axes include system architecture, the closest physical or service mechanism, problem formulation, and solver family. Add an axis only when it supports a distinct boundary. A shared keyword or publication chronology is not enough.

Within one subsection, keep the criterion stable and make the categories mutually distinguishable and collectively adequate for the evidence actually covered. Do not claim a universal taxonomy unless the search supports it. For a solver-family subsection, declare one axis and apply the self-test in the core solver-family rule.

### 4. Draft category paragraphs

Use:

1. category center sentence defining the shared mechanism;
2. representative evidence grouped by that mechanism;
3. class-level capability;
4. exact retained assumption or missing capability;
5. transition to the next class or paper-level need.

A representative paper normally needs only its setting, distinguishing mechanism or decision, and the result necessary for comparison. Expand only the closest work whose exact assumption establishes the target boundary. The paragraph must remain intelligible without author names.

### 5. Control claims and citations

Place each citation after the smallest supported proposition. Do not move one paper across subsections merely to fill a taxonomy. When one source genuinely supports two axes, name the distinct analytical role each time.

End each subsection with:

`shared capability -> retained assumption -> consequence in the target setting`

End the section by combining those residual boundaries into the smallest defensible gap. Prefer bounded formulations such as “these mechanisms have not been jointly evaluated in the reviewed settings.” Avoid “no work,” “the first,” and universal absence claims without a search record that can support them.

When the closing paragraph restates the Introduction's gap, follow the closing-gap rule in the core contract.

### 6. Run the audit

Apply the core classification, evidence, gap, citation, paragraph, and resolution gates, followed by the selected domain gates. Confirm that:

- headings alone reproduce the literature-side logic;
- opening sentences form a coherent classification story;
- every paper belongs under the declared criterion;
- every limitation follows from described evidence;
- the final gap maps to actual model or method needs;
- the section neither duplicates the Introduction nor leaks method details.

## Reader gates (check before delivering)

1. Every coined term is defined by function at first use (T); no variable-like names for decisions or objectives.
2. Every definite expression has an antecedent (A); every action has a purpose or a cost (Q).
3. Each proposition has one home (D); each universal or negative claim is tagged and supported (C).
4. Length is inside the declared scale range, or the deviation is recorded (S).
5. Sentence rhythm and connectives are inside the house-style band, or each remaining flag and its reason are listed in the delivery note, not in the manuscript (R).
6. Ledgers and notes stay out of the manuscript (H).

## Output constraints

- Preserve citation keys, terminology, and target-venue conventions.
- When drafting, provide the finished section rather than a literature-search diary.
- Keep ledgers, term tables, and audit notes out of the manuscript text and appendices unless the user asks for them.
- When auditing, report failures by subsection and paragraph role, then provide a corrected evidence map or revision.
- Do not alter bibliography entries or manuscript sections outside the authorized scope.

