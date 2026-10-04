---
name: paper-term-glossary-builder
description: Build beginner-friendly, source-grounded glossaries for academic papers, research PDFs, paper-derived HTML digests, literature review notes, and technical reading workflows. Use when Codex is asked to extract difficult terminology from a paper, explain paper-specific meanings, verify uncertain definitions with web search or AnySearch, create nested prerequisite-term explanations, produce a glossary.md/glossary.html, or help new readers understand dense research jargon.
---

# Paper Term Glossary Builder

Create a paper-specific glossary that reduces reading friction for newcomers. The output must explain what each term means in the paper, what a beginner must know first, and which definitions were verified from the paper or external sources.

## Core Contract

- Treat the paper or its generated HTML as the primary source for paper-specific meaning.
- Explain terms for a smart beginner entering the field, not for an expert reviewer.
- Prefer grounded definitions over generic encyclopedia blurbs.
- Verify uncertain, overloaded, or high-impact terms with AnySearch or another current search source.
- If an explanation introduces new technical terms, add nested prerequisite entries until the reader has a usable path. Limit recursion depth to 2 by default, or 3 when the user asks for more.
- Mark uncertainty explicitly. Do not invent definitions, expansions, datasets, metrics, or paper claims.
- Keep secrets and API keys out of the output and logs.

## Input Routing

Use the richest available input:

1. Paper HTML digest from `paper-pdf-to-structured-html`, especially its section prose, captions, assets, and page text.
2. PDF extraction manifest, page text, or OCR output.
3. Raw PDF, if no digest exists. In that case, first extract text or use `paper-pdf-to-structured-html` if the user also needs a readable paper digest.
4. User-provided notes or target audience constraints.

If the paper has an existing `research/paper-html/<slug>/` work directory, write the glossary there unless the user gives another target.

Recommended outputs:

- `<paper-workdir>/glossary.md` for editable notes.
- `<paper-workdir>/glossary.html` only when the user wants a browsable or shareable artifact.
- `<paper-workdir>/glossary-sources.json` only when source tracking or later automation matters.

Read `references/output-schema.md` when creating a durable glossary file.

## Workflow

### 1. Build The Candidate Term Ledger

Scan the paper title, abstract, section headings, method descriptions, tables, figure captions, glossary-like paragraphs, and repeated technical phrases.

Prioritize:

- acronyms and expanded forms;
- algorithms, model families, architectures, losses, metrics, benchmarks, datasets, simulators, sensors, robot platforms, and task names;
- field-specific multiword terms;
- terms that carry the paper's central argument;
- terms that are common in the field but hard for newcomers;
- terms whose meaning changes across domains.

Avoid overloading the list with generic words, author names, ordinary verbs, and obvious terms unless the paper uses them in a specialized way.

For each candidate, record:

- term;
- aliases or acronym expansion;
- category;
- first and strongest source locations;
- short source snippet or paraphrased evidence;
- why it is difficult;
- priority: `must-know`, `helpful`, or `optional`;
- verification need: `paper-defined`, `verify-external`, or `uncertain`.

### 2. Rank For Beginner Reading Value

Rank by practical reading impact, not raw frequency.

Use this scoring intuition:

- central to the paper's thesis or taxonomy;
- appears in multiple major sections;
- needed to understand figures, tables, or experiments;
- likely unfamiliar to a new reader;
- overloaded or ambiguous across fields;
- acts as a prerequisite for other terms.

For a first pass, keep the main glossary to 20-40 terms per paper. Put the rest in an optional "Further Terms" section.

### 3. Define Each Term In Three Layers

Each main entry should include:

- plain-language definition;
- paper-specific meaning;
- why it matters for reading this paper;
- where it appears;
- prerequisite terms;
- related or contrast terms;
- confidence and sources.

Use paper wording as evidence, but paraphrase rather than copying long passages.

### 4. Verify Uncertain Meanings

Use AnySearch when a term is not clearly defined by the paper, is overloaded, is an acronym with multiple expansions, affects a central claim, or the user asks for verified explanations.

Search strategy:

- Prefer official docs, original papers, benchmark/dataset pages, standards, project repos, or reputable survey/tutorial sources.
- For model, dataset, benchmark, and algorithm names, search the exact name plus the paper domain.
- For acronyms, search the acronym plus the nearby expanded phrase or section context.
- Use multiple sources when results conflict.
- Keep external definitions subordinate to the paper-specific usage.

Record verification as:

- `paper`: meaning grounded only in the current paper;
- `external-confirmed`: external source agrees with paper usage;
- `external-disambiguated`: external source resolves an ambiguous term;
- `uncertain`: no reliable confirmation found or definitions conflict.

### 5. Add Nested Prerequisite Explanations

When a definition introduces another technical term that a newcomer may not understand, add it as a child entry if it is necessary for comprehension.

Rules:

- Default max depth: 2 levels below the main term.
- Avoid circular definitions. If A needs B and B needs A, rewrite one definition using simpler language.
- Prefer short prerequisite entries: 1-3 sentences unless the term is also a main glossary term.
- Reuse existing entries instead of duplicating definitions.
- Mark nested terms with paths such as `VLA -> policy -> action space`.

### 6. Produce The Glossary

Use a concise structure:

- Reading Orientation: how to use the glossary.
- Must-Know Terms.
- Nested Prerequisite Map.
- Helpful Terms.
- Optional Further Terms.
- Source And Confidence Notes.
- Unresolved / Manual-Check Terms.

For project work, include a short section such as "How this helps the current reading sprint" when the user is using the glossary for a specific project.

### 7. Validate

Before finishing:

- Check every main term has a definition, paper-specific meaning, and source location.
- Check external claims have source labels.
- Check nested terms do not recurse forever or create circular definitions.
- Check acronyms have expansions or are marked unresolved.
- Check the output is readable without opening the PDF for every entry.
- Run a light link/path check if images or source links are included.

## AnySearch Use

If AnySearch is installed, load its skill only when verification is needed. Follow its CLI rules and do not save API keys without user approval.

Good query patterns:

- `"<term>" "<paper domain>" definition`
- `"<dataset or benchmark name>" official`
- `"<algorithm/model name>" original paper`
- `"<acronym>" "<expanded phrase or nearby context>"`

For current or version-sensitive terms, do not rely on stale model memory.

## Output Tone

Write in Chinese by default when the user is Chinese. Preserve English technical terms, acronyms, model names, dataset names, and source titles. Use direct explanations rather than ornate prose.

## Stop Conditions

Stop and ask only when:

- the paper/source file cannot be found;
- the user must choose between multiple papers;
- external verification would require credentials or sensitive data;
- the user requests a strict source policy that is unavailable.
