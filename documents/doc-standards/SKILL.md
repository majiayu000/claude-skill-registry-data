---
name: doc-standards
description: Documentation writing-quality standards — controlled language (ASD-STE100), Google/Microsoft style guide rules, ISO 24495 plain language, AI/agent readability (llms.txt, self-contained sections), and a machine-checkable lint gate. Use whenever writing or reviewing ANY documentation prose — README, API reference, tutorial, how-to, changelog, error message, code comment blocks, llms.txt — even if the user only says "write docs", "document this", "improve the README", "docs smell like AI", or "make the docs clearer". Structure/coverage questions (which doc types exist) belong to a Diátaxis-structure skill if one is installed; THIS skill governs how each sentence and section is written, and provides the lint gate to verify it.
metadata:
  type: reference
  sources: ASD-STE100 Issue 9 (2025-01), Google developer documentation style guide, Microsoft Writing Style Guide, ISO 24495-1:2023, llms.txt spec
---

# doc-standards — write documentation that survives translation, retrieval, and skepticism

Documentation written by an LLM has a smell: elegant-variation synonyms, subordinate
clauses, filler, hedging. The fix is not "write better" — it is adopting the constraints
professional documentation systems already use. This skill stacks five criteria layers,
from structure down to the word, and ends in a machine gate.

## The five layers

| Layer | Question it answers | Source standard |
|-------|--------------------|-----------------|
| 1. Structure | Which document am I writing, for whom? | Diátaxis + ISO 24495 |
| 2. Controlled language | Is each sentence unambiguous? | ASD-STE100 |
| 3. House style | Is it consistent with developer-docs convention? | Google / Microsoft style guides |
| 4. AI readability | Can an agent retrieve and use each section alone? | llms.txt + retrieval practice |
| 5. Verification | Can a machine confirm 2–4? | Vale / bundled checker |

## Workflow

### 1. Structure first (delegate, don't duplicate)

Classify the document before writing a word: **tutorial, how-to, reference, or
explanation** (Diátaxis). Each has a different contract with the reader — a tutorial
promises safe success, a reference promises completeness, a how-to promises a working
result, an explanation promises understanding. Mixing them is the #1 structural defect.

- Generating new docs or auditing coverage → if a Diátaxis-structure skill is installed
  (for example gstack's `document-generate` / `document-release`), invoke it — it owns the
  Diátaxis map. Otherwise classify and scaffold the document type yourself before writing.
  This skill governs the prose inside whatever gets scaffolded.
- Then apply ISO 24495's reader-first gate: state who the reader is and what they must be
  able to DO after reading. If you cannot name the reader, stop and find out. The four
  plain-language principles — relevant, findable, understandable, usable — are the
  acceptance criteria for the whole document, not decoration.

### 2. Draft under controlled language (ASD-STE100)

Read `references/ste100.md` before drafting anything longer than a paragraph. The core
discipline, always in force even without reading the reference:

- **One word, one meaning.** Pick one term per concept and repeat it everywhere.
  Synonym variation ("verify / check / confirm / ensure") is the strongest LLM tell
  and the #1 source of reader doubt ("is a 'token' the same as the 'key' above?").
- **Procedural sentences ≤ 20 words, descriptive ≤ 25.** One instruction per sentence.
- **Active voice, imperative for instructions.** "Run the command", never
  "the command should be run".
- **Simple tenses only.** No present perfect ("has been deprecated" → "was deprecated
  in v2.1").
- **Warnings before the step they protect**, in command form.

### 3. House style pass (Google/Microsoft)

Read `references/style-guides.md` when writing developer-facing docs. Highest-value rules:
second person, present tense, sentence-case headings, goal-before-action steps
("To enable X, run:"), descriptive link text, no "simply/just/easy/please", global-audience
English (no idioms, no "e.g./i.e."), consistent bold-UI/code-font conventions.

### 4. AI-readability pass

Read `references/ai-readability.md` when the docs will be consumed by agents, RAG
pipelines, or coding assistants — which in practice is all public docs now (GitBook
measures ~41% of doc traffic from agents). Core rule: **every heading-delimited section
must make sense retrieved alone** — no "as mentioned above", no split concepts, full
parameter tables, realistic examples with expected output, and an `llms.txt` index at
the docs root.

### 5. De-slop and gate

- If an AI-tell removal skill is installed (for example `stop-slop`), run its checklist
  on the final prose — it owns that layer; don't re-derive its rules here. Without one,
  sweep for the classic tells: filler openers, "not X but Y" contrasts, adverb padding,
  pull-quote sentences, em-dash overuse. One precedence rule: where literary rhythm
  advice ("vary sentence length") conflicts with STE100 uniformity in *procedural*
  steps, STE100 wins inside numbered procedures; rhythm wins in explanations.
- Run the machine gate:

```bash
python3 <this-skill's-base-directory>/scripts/check_docs.py <file-or-dir> [--max-words 25]
```

It checks sentence length, passive voice density, banned words, synonym-set collisions,
heading hierarchy, section self-containment markers, and relative-link integrity —
zero dependencies. If `vale` is installed and a `.vale.ini` exists, it defers the style
layer to Vale (stronger). To set Vale up for a project, read `references/vale-setup.md`.

The gate is advisory line-by-line but binding in aggregate: fix every error-level finding;
use judgment on warnings (quoted text, proper nouns, and code samples are legitimate
exceptions). Do not declare documentation done while the gate reports errors.

## Terminology table (do this once per project)

Before the first doc ships, write a terminology table into the project's docs
(`docs/terminology.md` or a section in the README): each concept, its ONE approved term,
and the banned synonyms. Every later doc, PR description, and error message uses the
approved column. This is the cheapest single intervention — it converts "one word, one
meaning" from a per-sentence effort into a lookup.

**Example:**

| Concept | Approved | Banned |
|---------|----------|--------|
| API credential | API key | token, secret, credential |
| Stop a running job | cancel | stop, kill, abort, terminate |

## When NOT to apply full strictness

- Marketing copy, blog posts, pitch decks — voice matters more than control; use
  stop-slop alone.
- Code comments — follow the surrounding codebase's comment density and idiom instead.
- Legal text — do not simplify contract language; plain-language rewrites of legal
  clauses change meaning.
