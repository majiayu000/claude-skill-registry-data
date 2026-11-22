---
name: write-abstracts-and-conclusions
description: Use when drafting, revising, or auditing an engineering paper's title, abstract, index terms or keywords, contribution list, roadmap, or Conclusion, especially when the abstract lacks quantitative results, the Conclusion restates contributions or overstates the experiments, future work is a list of unrelated directions, or these summary parts disagree with each other after results change.
---

# Write Abstracts and Conclusions

## Purpose

Write the parts of a paper that readers see first and last as compressed versions of its argument. The title names the system and the approach, the abstract moves from setting to limitation to scenario, formulation, algorithm, and quantified result, the contribution list states what is new with its evidence scope, and the Conclusion summarizes the evidence in the order it was produced and derives future work from the limitations. None of them may claim more than the result sections show.

## Required resources and routing

1. Always read [the core contract and quality gates](references/core/contract-and-quality-gates.md) in full.
2. Always read [the reader and terminology contract](references/core/reader-and-terminology-contract.md).
3. Read [the house-style card](references/styles/house-style-card.md) and Sections 10, 11, and 12 of [the full team house style](references/styles/team-house-style.md) unless the user names another venue or team style. They hold the measured title, abstract, index-term, contribution, roadmap, and Conclusion shapes and the sentence-rhythm band.
4. Read [the Chinese manuscript adapter](references/languages/zh.md) when the manuscript is written in Chinese.
5. Use [the fingerprint script](scripts/style_fingerprint.py) to count words, sentences, and banned constructions when Python is available.
6. The contribution list sits inside the Introduction. When `write-introductions` is installed, use it for the Introduction around the list; this skill governs the list itself and its agreement with the abstract and the Conclusion.

## Workflow

### 1. Build the summary ledger

Read the Introduction, the experimental section, the existing summary parts, and the venue limits. Record one row per claim that a summary part may make:

| Claim | Source sentence in the result sections | Evidence scope (instances, runs, selection) | Numbers with units | Allowed strength | Used in title / abstract / contributions / Conclusion |
|---|---|---|---|---|---|

A claim without a source sentence in the result sections does not enter any summary part.

### 2. Draft the title

Two parts joined by a colon: the system and its setting, then the approach type with its objectives or key mechanism. Check the word range and forbidden words in the house style.

### 3. Draft the abstract

Write one paragraph in the move order of the contract: setting, limiting assumption of existing approaches and its consequence, scenario, decisions and formulation, algorithm, quantified result with scope, and an optional significance sentence. Define every abbreviation. Count words against the venue limit and the house-style range.

### 4. Choose the index terms

Order them from application to solver, four or five terms, matching the vocabulary of the title and the abstract.

### 5. Write the contribution list and roadmap

Two or three items in the order scenario or model, formulation, algorithm; the last item carries one result sentence with its scope. The roadmap gives one sentence per section.

### 6. Draft the Conclusion

Restate the problem, formulation, and algorithm in one or two sentences; summarize each experiment group in the order of the experimental section with its scope; end with a future-work chain derived from stated limitations.

### 7. Synchronize the summary parts

Check that the title, abstract, contribution list, and Conclusion use the same terms, numbers, and evidence scope as the result sections. After any rerun or model change, recheck every number and direction in all four places.

### 8. Measure and audit

Run the fingerprint script on the abstract and the Conclusion, then run the hard gates of the contract. Before submission, `--report` lists the abstract and Conclusion scale with the other checks in one file.

## Reader gates (check before delivering)

1. Every coined term is defined by function at first use (T); every abbreviation is defined in the abstract itself.
2. Every definite expression has an antecedent (A); every action has a purpose or a cost (Q).
3. Each proposition has one home (D); each universal or negative claim is tagged and supported (C).
4. Length is inside the declared scale range, or the deviation is recorded (S).
5. Sentence rhythm and connectives are inside the house-style band, or each remaining flag and its reason are listed in the delivery note, not in the manuscript (R).
6. Ledgers and notes stay out of the manuscript (H).

## Output constraints

- Match the manuscript's terminology, notation, abbreviations, and citation style.
- Deliver only the requested parts; keep the summary ledger out of the manuscript.
- Never introduce a number, instance count, or baseline count that the result sections do not report.
- When auditing, report claim-strength and consistency failures before wording issues.
- Do not modify the result sections, figures, tables, or bibliography unless the user authorizes it.
