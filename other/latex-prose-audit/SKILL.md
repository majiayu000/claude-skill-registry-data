---
name: latex-prose-audit
description: Use when auditing or revising LaTeX manuscripts for sentence-level academic prose, subject–verb agency, terminology or symbol consistency, article and modifier usage, citation placement, result wording, or LaTeX-safe formatting—especially when a paper contains algorithms, equations, figures, tables, or quantitative claims that need line-specific findings.
---

# LaTeX Prose Audit

## Core principle

Audit the manuscript's sentence-level contract before polishing its surface.
First identify who or what performs an action, what the verb actually claims,
and what noun phrase the reader is asked to interpret. Then check terminology,
articles, modifiers, sentence attachment, captions, equations, and LaTeX
syntax. Do not turn one author's wording into a universal prohibition.

## Use this skill when

- the target is one or more `.tex` files, an included LaTeX file, or a LaTeX-derived manuscript;
- the user asks to audit, proofread, revise, or fix academic writing and formatting;
- the paper contains equations, algorithms, tables, figures, citations, a supplement, or quantitative claims that must remain aligned.

Do not use it for a syntax-only compilation failure with no prose or semantic
question; use the project's LaTeX diagnostic workflow for that narrower task.

## Required reading and scope

1. Read the target file and every relevant `\input`, `\include`, abstract,
   conclusion, supplement, and bibliography entry. Build a file/section map
   before reporting line numbers.
   Enumerate sibling submission artifacts such as highlights, a graphical
   abstract, cover letter, and response letter even when the main file does
   not include them.
2. Inspect the document class, loaded packages, custom macros, citation
   commands, and local formatting conventions. Apply IEEE rules only when the
   target template actually uses them.
3. If the user supplies reference papers, read the complete relevant sections,
   not only titles or abstracts. Read [reference-prose-analysis.md](references/reference-prose-analysis.md)
   when the target uses the calibrated MEC/CMOEA vocabulary or result-writing
   patterns. Use it to retrieve fine-grained examples, not to import a paper's
   overall organization.
4. Read [rules-and-checks.md](references/rules-and-checks.md) before the first
   full audit. Use its rules as checks with evidence, not as a word blacklist.
5. Read [the house-style card](references/styles/house-style-card.md) unless
   the user names another venue or team style. Its author voice, sentence
   rhythm, connective profile, and banned constructions are audit rules for the
   team's manuscripts, and they take precedence over this skill's generic
   examples where the two differ. For a full audit of a team manuscript, also
   read Sections 4, 5, 7, and 13 of [the full team house style](references/styles/team-house-style.md).
6. Run [the fingerprint script](scripts/style_fingerprint.py) on the target
   when Python is available. Use its flags as leads: read each flagged sentence
   before reporting it. Pass the manuscript's term ledger with `--terms` when
   one exists. For a full audit of a submission, `--report` with the
   manuscript, supplement, and response letter collects every check in one
   Markdown file.

## Audit workflow

### 0. Establish the artifact boundary

Record the files, included children, language, document class, citation
system, and requested mode. Preserve the user's scope: audit only unless the
user authorizes edits or selects `--fix`.

### 1. Build four small ledgers

- **Vocabulary ledger:** term, meaning, grammatical role, abbreviation, and
  approved variants.
- **Notation ledger:** symbol, quantity, domain/index, first definition, and
  every cross-file use.
- **Claim ledger:** exact claim, artifact or citation supporting it, claim
  strength, aggregation/statistical unit, and remaining limitation.
- **Artifact ledger:** equation/algorithm/figure/table/paragraph references
  and whether prose, math, pseudocode, and captions describe the same object.

Do not invent a canonical term when the paper has not yet defined one; report
the missing decision instead.

### 2. Run the four rule categories in order

1. **Category A — semantic roles and reference:** identify the grammatical
   subject and classify it as an intentional actor, a neutral reporting
   artifact, or an inanimate object. Only an algorithm, controller, system,
   author, or explicitly modeled agent performs decisions or claims results.
   The complete Rule 1 non-agent list covers algorithm parts; evidence objects
   including metrics, indicators, tests, values, results, data, trends, tables,
   figures, curves, equations, sections, and experiments; and mathematical or
   physical objects including objectives, constraints, formulations,
   representations, populations, archives, states, paths, and costs. Then check
   canonical terminology, abbreviations, `the/a/an`, zero article, and evidence
   verb strength.
2. **Category B — sentence-level English:** check direct verb choice,
   collocations, modifiers, numerical qualifiers, pronouns, `which/where`,
   parentheticals, `respectively`, tense, voice, parallelism, and repetition.
   Check sentence rhythm in both directions: stacked claims that need a split,
   and runs of short sentences or stacked `Since`/`Therefore` openers that need
   a merge.
3. **Category C — mathematical and artifact prose:** check scalar/vector/
   matrix/set/function notation, indices and superscripts, domains, ordered
   sequences, dimensions, units, formula semantics, algorithm line prose,
   equations, figures, tables, captions, ranges, and numerical typography.
4. **Category D — LaTeX source integrity:** check references, labels, citation
   commands, spacing, equation punctuation, protected commands, math/text
   boundaries, URLs, custom macros, and compilation/render verification.

Revise naturalness only after these four categories; preserve the author's
technical meaning and language.

### 3. Classify findings

- **Blocker:** compilation break, undefined or contradictory notation, missing
  algorithm step, invalid comparison, or an unsupported guarantee that changes
  the scientific meaning.
- **High:** claim-evidence mismatch, cross-document inconsistency, wrong
  constraint/metric semantics, or terminology drift affecting interpretation.
- **Medium:** unclear result ordering, causal overstatement, paragraph overload,
  ambiguous reference, or repeated definition.
- **Low:** local awkwardness, caption polish, punctuation, or template style.

Use `--quick` only for Blocker and High findings. The default full audit reports
all actionable findings. `--fix` permits minimal edits after preserving a
before/after mapping; it does not authorize redesigning the model, replacing
citations, or silently changing equations.

### 4. Produce the audit

Lead with the verdict and highest-risk findings. Use this table, sorted by
priority:

| Priority | File:line/section | Finding | Rule/check | Evidence | Minimal correction |
|---|---|---|---|---|---|

Quote only the smallest necessary phrase. Give a replacement sentence when it
is safe; otherwise state what must be verified and why an automatic edit would
be unsafe. Finish with 2–3 positive patterns, an unresolved-check list, and a
short count by priority.

### 5. Verify edits

After `--fix` or an explicitly authorized revision:

1. re-read every changed paragraph and its neighboring equation, figure,
   citation, or algorithm reference;
2. rerun the ledgers and search for stale terms, labels, and symbols;
3. run the project's LaTeX compiler (normally `latexmk` with the target's
   engine) when available, and report the exact command and result;
4. rerun the fingerprint script and compare the sentence-length profile and
   connective counts with the pre-edit run;
5. run `git diff --check` when the target is in a Git working tree.

If compilation is unavailable or the source is incomplete, report that status
explicitly. Never claim that a LaTeX fix is verified from a static text scan
alone.

## Boundaries

- Do not rewrite bibliography records or manufacture citations.
- Do not treat a reference paper's style as proof that its wording is correct.
- Treat every algorithm part listed in Rule 1 as a structural object, not an
  independent actor. When one is the subject of an executed action, change the
  subject to the algorithm/controller or use passive voice. Retain only
  structural descriptions such as `consists of`, `comprises`, `contains`, `is
  designed to`, and `is applied to`.
- Do not enforce one citation syntax, article pattern, math delimiter, or
  non-breaking-space convention without checking the target template.
- Do not edit comments, verbatim blocks, labels, citation keys, macro names,
  or mathematical expressions as if they were ordinary prose.
