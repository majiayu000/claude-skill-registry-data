---
name: academic-writing
description: Academic prose support. Use for reviewing, polishing, proofreading, consistency checks, citation checks, or drafting manuscript text in LaTeX, Markdown, Quarto, or plain text.
user-invocable: true
---

# Academic Writing

Three modes — **Review**, **Polish**, **Draft** — over one knowledge base: style, structure, eight consistency dimensions, refactor-and-compile.

## These rules are additive

The rules below constrain or redirect edits where they apply — substance vs prose, in-flight author signals (TODOs, DO NOT EDIT, intent comments), the eight consistency dimensions, ask vs propose vs perform. Everywhere else, polish and proofread as you normally would.

## Preserve substance, polish prose

- **Preserve** — argument, logic, section/paragraph structure, technical claims, author's intent, tone. Sovereign: an edit that would change any of them stops and asks.
- **Polish freely** — wording, sentence structure, clarity, parallelism, hedging calibration, flow, mechanical correctness. This is the editing target.
- **Restructuring** — out of scope unless the request authorizes it and `references/structure.md` is loaded.

## Write to the reader, not the conversation

The document's audience has the document plus venue-appropriate background knowledge — never the editing conversation, the repo, prior drafts, or the project's working vocabulary. Content addressing a different audience, referencing the editing process, or naming artifacts outside their reach does not belong in the document.

**Build the audience model before the first character changes.** Answer both explicitly:

1. **Who is the audience?** The venue fixes tolerated jargon, formality, cite density, and detail: a top-five finance journal reader, an SSRN working-paper reader, a conference audience, a replication-package user, an editor reading a response letter.
2. **What is in their information set?** The current draft, works it cites, venue background knowledge.

Then check each sentence against the set: every term is in the set or defined at first use; every reference resolves from the set; every temporal cue is internal to the document's narrative ("we next turn to robustness"), not external to the editing process ("the table now defines"). `references/style.md §Audience: write to the reader, not the conversation` carries the line-level markers as the safety net; the audience model is the primary discipline.

## Project Conventions in the task tree / CLAUDE.md

Writing-side conventions are paper-specific choices among defensible alternatives a fresh agent would otherwise silently re-decide each session.

**Where they live (ladder, ordered by permanence).** `## Project Conventions` on the `## Objective` of the manuscript-governing ancestor task — the task whose subtree is the manuscript, so every writing agent inherits it via the ancestor chain — then `CLAUDE.md` (project-permanent). No task tree: return the inventory as a conversation reply. Promote up the ladder when the user signals durability.

**What writing contributes** (rows alongside data and modeling contributions):

| Convention | What's recorded | Acid test |
|---|---|---|
| Terminology | Canonical term per key concept where synonyms exist, with first-use location. | Fresh agent would pick a synonym. |
| Abbreviations | Defined short forms, with the spell-out and first-use location. | Fresh agent would re-spell or pick a different acronym. |
| Citation format | Narrative vs parenthetical (`\citet` vs `\citep`), "et al." threshold, multi-citation separator, e.g./i.e./cf. usage. | Fresh agent would guess between conventions. |
| Numerical formatting | Rounding precision, SE/CI delimiter, units, percent-vs-pp convention. | Fresh agent would guess between conventions. |
| Cross-reference phrasing | "Section 3" vs "§3" vs "Sec. 3"; "Table 1" vs "Tab. 1"; label prefixes (`fig:`, `tab:`, `eq:`). | Fresh agent would guess. |
| Voice and tense | "We" vs passive; past for procedure, present for results, or the paper's chosen mix. | Fresh agent would mix conventions inconsistently across sections. |
| Prose typography around notation | Bold/italic/hat conventions for vectors, estimates, random variables when they appear in prose; quote style; em-dash style. | Fresh agent would guess between conventions. |

**Excluded:** math notation (symbol → meaning, equation numbering) — owned by `theory-modeling`'s Notation Conventions table, a sibling subsection inside `## Project Conventions`; section/caption capitalization and page-layout macros — venue / template territory.

**Soft trigger.** First long-form review or first draft pass against a paper with no recorded writing-side conventions: inventory them onto the manuscript-governing task or `CLAUDE.md` before substantive editing. Routine polish and single-lane review do not auto-scan.

**Scanning is unspecified.** Inventory using the detection language in `references/consistency/*.md` and `references/style.md`.

## Before you start

1. **Classify the request into a mode** before reading the file — the mode determines what to load.
2. **Inspect in-flight author work** with `git status` / `git diff` before editing; an unstaged diff often *is* the polish target.
3. **Inline directives are work assigned to you.** `TODO`, `% TODO:`, `\todo{...}`, `[fill in]`, `??`, `XXX`, and crude or placeholder phrasing get cleaned up inside scope. An explicit `DO NOT EDIT` (or equivalent) marks a line or block off-limits even within scope.
4. **Intent comments** (`% intent: …` / `<!-- intent: … -->` above a paragraph) are author-owned:  Polish preserves but never invents them. Full convention in `polish.md §Intent comments` and `draft.md §Intent comments`.

## Mode routing

Loading the listed reference is the authority grant — without `structure.md` loaded, structural edits are out of scope by construction.

| Request shape | Mode | Load |
|---|---|---|
| "Review §X for clarity / consistency / structure"; "Check my citations"; "Find issues in this draft" | **Review** | `references/review.md` + relevant knowledge file(s) |
| "Polish §X"; "Tighten this paragraph"; "Clean up these edits"; "Proofread"; "Apply these review findings" | **Polish (sentence/paragraph scope)** | `references/polish.md` + `references/style.md` |
| Polish that explicitly authorizes restructuring ("restructure §X"; "reorganize the intro"; "strengthen this argument") | **Polish (structural scope)** | `references/polish.md` + `references/style.md` + `references/structure.md` |
| "Draft the methods section"; "Write up the results from these notes" | **Draft** | `references/draft.md` + `references/structure.md` + `references/style.md` |

## Knowledge files

| File | Load when |
|---|---|
| `references/style.md` | Sentence- or paragraph-level edits; language/style review; every Polish and Draft self-check. |
| `references/structure.md` | Structure review, drafting a section, or polish that authorizes restructuring. |
| `references/consistency/*.md` (8 dimensions: terminology, notation, cross-references, citations, numerical, math, argument-logic, code-paper) | Review or polish targets that consistency dimension. |
| `references/planning.md` | PLAN phase for large writing work; the writing header and review-only task tree path. |
| `references/long-form-review.md` | Multi-lane review (style/language, structure, or more than one consistency dimension), `deep` thoroughness, or full-paper / pre-submission scope. |
| `references/refactor-and-compile.md` | Find-replace across the document, build/compile any time edits are made. |
| `references/integration.md` | The writing task is riding `superintegrate`. |

## Coupling to superRA workflows

Most writing work is standalone — terminate at edit + commit, or findings + commit. Larger work (whole-section drafts, whole-paper revisions, R&R passes) routes through `superplan` with `references/planning.md`. Multi-lane, deep, full-paper, or pre-submission review creates a review-only task subtree: reviewers inspect the existing draft through `superimplement`, findings live in task-local `## Review Notes` (`references/long-form-review.md`).
