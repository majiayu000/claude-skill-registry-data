---
name: write-revision-responses
description: Use when preparing a journal revision and its response letter, drafting or auditing responses to editor and reviewer comments, merging a co-author's or supervisor's edits into the manuscript, supplement, and letter, or keeping all submission documents consistent after results, equations, or citations change during a revision.
---

# Write Revision Responses

## Purpose

Turn every editor and reviewer comment into a concrete, checkable change and a response that lets the reviewer find and verify it. The manuscript, the supplement, and the letter are one submission: every quoted passage, number, term, equation number, and citation number must agree across them.

## Required resources and routing

1. Always read [the response contract and quality gates](references/core/response-contract-and-quality-gates.md) in full.
2. When a response changes a manuscript section, revise that section with the matching section skill when it is installed (`write-introductions`, `write-related-work`, `write-system-models`, `write-methods`, `write-experiments`), and audit the sentences with `latex-prose-audit`. This skill decides what changes, where it lives, and how the letter reports it; the section skills govern how the section is written.
3. If the user supplies a letter template from another paper, use it for format, structure, length, and locator phrasing only, never for content.
4. Use [the fingerprint script](scripts/style_fingerprint.py) with `--diff` to classify a co-author's or supervisor's edits against the snapshot (merges, splits, rewrites, deletions) and to compare sentence length and connectives before and after them.

## Workflow

### 0. Inventory the submission

Record the comments verbatim, the current manuscript, supplement, and letter, the version submitted before the revision (it defines what counts as revised), any co-author or supervisor snapshot, the result artifacts, and the venue limits (page count, highlighting rules, upload format). Do not start drafting while a comment, a document, or the revision baseline is missing; report what is missing.

### 1. Build the comment ledger

Give every comment one row: comment id, request, requested action type, owning manuscript unit, planned change, evidence or new experiment, quoted units, status. Keep the numbering of the comments; never merge, skip, or renumber them.

### 2. Decide each response

Answer a request for a model, an experiment, or an analysis with that model, experiment, or analysis. State a scope limit only when the request concerns it, once, and point it to future work. Decline only with evidence, and say what was done instead.

### 3. Revise the manuscript units

Edit the owning unit, not the letter, first. Move an argument to the section where readers check it. Calibrate every revised claim to its evidence. Recompute every number that depends on a rerun.

### 4. Draft the responses

Use the two-paragraph pattern of the contract: what was done and its core argument, then where it is and the quoted passages. Editor responses point to the reviewer responses that carry the change.

### 5. Quote and highlight

Quote complete revised paragraphs verbatim from the compiled documents, including their highlighting. Re-quote a unit in full in every response that relies on it. Highlight only what the policy of the contract allows.

### 6. Synchronize after every change

After a result, model, equation, or citation change, update every document and every quoted copy in the same pass, then recheck every claim whose direction depends on the new numbers and every figure that draws the changed object.

### 7. Integrate co-author or supervisor edits

Keep their version untouched as a snapshot, adopt their framework, respect their deletions, fix only obvious errors with minimal edits, and check their edits for errors before building on them. Classify their edits with the fingerprint script's `--diff` mode and record recurring edit types as writing rules for the next paper. At the end, report every change made after the snapshot with locations.

### 8. Audit and deliver

Compile every document, run the quote, number, and term checks of the contract, and pass all hard gates. Run the fingerprint script with `--report` on the manuscript, the supplement, and the letter (with `--terms` when a term ledger exists), and read every item it lists. Deliver the revised files and a change report; keep ledgers out of the submission documents.

## Output constraints

- Preserve the reviewers' wording in pasted comments; never edit a comment.
- Do not add new models, experiments, citations, or claims that the user has not authorized; propose them instead.
- Do not restore text that a co-author or supervisor deliberately deleted unless the user asks.
- Report anything that could not be verified (a quote that does not compile, a number without an artifact) instead of smoothing it over.
- Match the language, notation, terminology, and citation style of the manuscript.
