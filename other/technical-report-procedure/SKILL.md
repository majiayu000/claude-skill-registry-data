---
name: consolidated-technical-writing
description: "Consolidated technical writing skill combining report production, Typst typesetting, writing procedures, review pipelines, and delivery mechanics."
version: 1.0.0
author: "Technical Writing Team"
license: MIT
metadata:
  hermes:
    tags: [reporting, typst, technical-writing, deliverables, writing, review]
    related_skills: []
    source_export: "July 2026 — consolidated from report-base-procedure, technical-report-procedure, internal-report-procedure, writing-procedure, typst-documents, post-write-review-pipeline"
---

# Consolidated Technical Writing Skill

> A single reference for producing formal technical documents — reports, analyses, memos, presentations, and deliverables — in a reproducible, high-quality workflow.

---

## Table of Contents

1. [Trigger: When to Load This Skill](#1-trigger-when-to-load-this-skill)
2. [Output Format: Typst is Default](#2-output-format-typst-is-default)
3. [Diagram and Visual Conventions](#3-diagram-and-visual-conventions)
4. [Signing Identity](#4-signing-identity)
5. [The 5-Step Writing Procedure](#5-the-5-step-writing-procedure)
6. [Report Types and Templates](#6-report-types-and-templates)
7. [Typst Syntax Essentials](#7-typst-syntax-essentials)
8. [Presentation Format](#8-presentation-format)
9. [Post-Write Review Pipeline](#9-post-write-review-pipeline)
10. [Pitfalls](#10-pitfalls)

---

## 1. Trigger: When to Load This Skill

Load whenever producing **any formal deliverable** — report, analysis, whitepaper, memo, competitive intelligence, research deck, or document intended for structured consumption.

---

## 2. Output Format: Typst is Default

**Typst is the default output format for all reports.**

- Never deliver Markdown as a final deliverable. Markdown is acceptable only as intermediate/source or scratch notes.
- Always produce professional deliverables in Typst unless explicitly overridden.
- Load `typst-documents` skill when Typst generation mechanics are needed.

---

## 3. Diagram and Visual Conventions

- **Never use ASCII diagrams.** Use Mermaid syntax (` ```mermaid ` fenced code blocks) for all diagrams.
- **Static PNG preferred** for data visualizations (matplotlib). Interactive HTML/plotly is a non-starter — CDN-dependent HTML fails silently.
- **Data-driven figures:** Preprocess data into structured JSON first, then generate figures programmatically. See `references/data-driven-figure-generation.md` for the full pipeline.
- **Research-paper aesthetics:** White background, sans-serif fonts (Helvetica/Arial), clean lines. No dark themes, no blog infographics, no emoji.
- **Tight arrows:** Arrowheads must touch box edges. No floating arrows with gaps.

---

## 4. Signing Identity

- **Never reveal the agent name in any report.**
- Each report must define its own signing identity (e.g., "HPC I/O Analysis", "Systems Engineering Team").
- If no identity defined, use a professional title tied to the project domain.
- Hard rule — no exceptions, no "internal use only" carve-outs.

---

## 5. The 5-Step Writing Procedure

| Step | Name | What Happens | Output |
|------|------|--------------|--------|
| 1 | Collect | Gather facts, data, quotes, sources into a JSON artifact | `data-collection.json` |
| 2 | Review | Subagent verifies narrative fits data, finds gaps, adds honesty | Updated artifact + narrative summary |
| 3 | Draft v1 | Write prose in plain text/markdown, no formatting | Revised prose draft |
| 4 | Format | Port to Typst/LaTeX, fix syntax, compile | Compilable source file |
| 5 | Verify | Final subagent checks flow, rechecks data against artifact | Clean PDF ready for delivery |

### Step 1: Collect

Organize all raw material into a JSON artifact (schema in `references/data-collection-template.json`).

**Evidence Hierarchy (highest to lowest trust):**

| Tier | Source Type | Weight |
|------|-------------|--------|
| 1 | Government data | Highest |
| 2 | Peer-reviewed paper | Very High |
| 3 | Professional review/audit | High |
| 4 | News article (reputable) | Medium-High |
| 5 | Blog / analysis | Medium |
| 6 | Social media post | Low-Medium |
| 7 | Comment / anecdote | Low |

**Rule:** Claims based on tier 6-7 evidence must be qualified ("Some consumers report..."). Corroborate with tier 4+ before upgrading.

### Step 2: Review

Dispatch a subagent reviewer with the JSON artifact and checklist:
- Does every claim have a matching entry in `claims[]`?
- Are there contradictory data points?
- Does the narrative account for ALL verified claims?
- Are there negative/critical findings the narrative ignores?
- Are there `unverified_assertions[]` that leaked into the narrative?

**Blocking Gaps:** If `narrative_gaps[]` contains `severity: "blocking"`, stop and report to user before Step 3.

### Step 3: Draft v1

Write prose in plain text/markdown. No formatting yet.

**Draft Rules:**
- Controlling idea in every paragraph
- Evidence follows claim
- Active voice in key assertions
- No filler, no puffery
- Honest representation (including critical findings)
- Every claim must trace back to the JSON artifact

**Review:** Dispatch a subagent to check:
- Does every paragraph connect to a claim?
- Is any claim unsupported?
- Is the tone honest or sycophantic?
- Does the draft have a clear arc?
- Are claims about counts accurate?

**Hard Rule:** Cannot proceed to Step 4 until the Step 3 review completes and passes.

### Step 4: Format

Port locked prose into target format.

**Format Selection:**

| Document Type | Format | Template |
|---------------|--------|----------|
| Client report | Typst | `@preview/biz-report` |
| Technical report | Typst | `@preview/truss-report`, `@preview/basic-report` |
| Internal memo | Markdown or Typst | `@preview/tufte-memo`, `@preview/minimal-note` |
| Academic paper | LaTeX | Venue-specific (NeurIPS, ICML, etc.) |
| Blog post | Markdown | None (platform-native) |
| Research presentation | Typst | `@preview/typslides` |

**Sanitize Before Writing Typst:**
- Forbidden in `.typ` files: `\u0026`, `\u003e`, `\u003c`, `\u0022` — write literal `&`, `>`, `<`, `"`
- After writing: `grep '\u' filename.typ` — if matches, rewrite with literal characters
- Dollar signs: escape `\$` in prices (or write "per month" instead of `/mo`)
- `#` inside headings: triggers code mode. Use `*(Critical)*` not `#severity[Critical]`
- `@` in text: triggers label reference. Use `#"@"` or `#raw("@")`

### Step 5: Verify

Final subagent check:
- Does the final document cite the same sources as the artifact?
- Any claims in the document NOT in the artifact? (Scope creep)
- Is the flow logical?
- Template copy-paste errors? (Inherited text from previous documents)
- Compiles without errors?
- "At a Glance" summary consistent with detailed findings?

**After Step 5:** No further content changes without restarting from Step 3.

---

## 6. Report Types and Templates

Reports are produced using **existing Typst templates** from the Typst Universe. Do not hand-craft document styling.

### Template Catalog

**Academic Papers:**
| Template | Venues | Key Features |
|---|---|---|
| `bloated-neurips` | NeurIPS | Anonymous submission, line numbering |
| `lucky-icml` | ICML | Multi-column, BibLaTeX |
| `clear-iclr` | ICLR | OpenReview-compatible PDF |
| `arkheion` | arXiv | Single-column, ORCID, minimal |

**Technical Reports:**
| Template | Best For | Key Features |
|---|---|---|
| `truss-report` | Systems analysis, benchmarks | ADRs, callouts, trade-off matrices |
| `basic-report` | Lab reports, manuals | Compact mode, clean TOC |
| `modern-technique-report` | Course/methodology | Custom cover, theme colors |

**Business/Client Reports:**
| Template | Best For |
|---|---|
| `biz-report` | Corporate reports, audits, proposals |
| `letterloom` | Formal proposals, business letters |

**Internal Memos:**
| Template | Best For |
|---|---|
| `tufte-memo` | Decision briefs, status updates (sidenotes) |
| `minimal-note` | Quick notes, short briefs |

**Initialize with:**
```bash
/workspace/bin/init-report.sh --name <project> --theme <template>
```

**Environment workaround** (if `typst init` fails with permission denied):
```bash
export TMPDIR=/workspace/tmp
export TYPST_PACKAGE_CACHE_PATH=/workspace/.typst/cache
mkdir -p "$TMPDIR" "$TYPST_PACKAGE_CACHE_PATH"
```

**Compile:**
```bash
typst compile main.typ report.pdf
```

**Template Reuse Rule:** Before creating a new template, check if an existing one covers your report type (see `templates/` in this skill). Use existing if ~80% fits. Do not duplicate.

---

## 7. Typst Syntax Essentials

### Markdown → Typst Syntax Map

| Markdown | Typst (correct) |
|----------|-----------------|
| `# Title` | `= Title` |
| `## Section` | `== Section` |
| `**bold**` | `*bold*` or `#strong[bold]` |
| `less < than` | `less than` or `\<` |
| Pipe tables | `#table(columns: (...), ...)` |
| `\&`, `\$`, `\%` | Literal `&`, `$`, `%` (backslash renders literally) |

### Tables
```typst
#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: none,
  table.header([*Column A*], [*Column B*]),
  [Cell 1], [Cell 2],
)
```

**Critical:** Cell content must be a single argument. Do NOT pass `#v()` and `#text()` as separate arguments. Wrap them inside brackets:
```typst
[Row 1], [#v(4pt)#text(size: 10pt)[detail]],
```

**Headers:** Do NOT use `#text(weight: "bold")[Header]` as a table cell. Use `*[Header]*` instead.

**Alignment in table.cell:**
```typst
// Correct — named argument:
table.cell(colspan: 4, align: center)[*Task*]
// Alternative — content wrapper:
table.cell(colspan: 4)[#align(center)[*Task*]]
```

### Math Mode Triggers
- `$` enters math mode. Escape prices: `\$35M`
- `/` in math mode becomes a fraction. Write "per month" not `$99/mo`
- `#` enters code mode. Inside content brackets, use `#raw("#")` for literal `#`
- `@` triggers label reference. Use `#"@"` or `#raw("@")` for literal `@`
- `<` triggers label target. Use `#raw("<5%")` or write "under 5%"

### CLI vs Python Binding
- **Use native CLI** for anything with tables, custom macros, or math-mode risks
- **Python binding** (`pip install typst`) masks error locations
- **CLI install in containers:**
```bash
curl -L -o /tmp/typst.tar.xz \
  "https://github.com/typst/typst/releases/download/v0.14.2/typst-x86_64-unknown-linux-musl.tar.xz"
tar -xf /tmp/typst.tar.xz -C /workspace/
chmod +x /workspace/typst
/workspace/typst compile doc.typ doc.pdf
```

### Font Fallback
```typst
#let serif = "DejaVu Serif"
#let sans  = "DejaVu Sans"
#let mono  = "DejaVu Sans Mono"
```

"DejaVu" fonts are present on virtually all Linux containers. "Liberation" may be missing in minimal Docker images.

---

## 8. Presentation Format

When producing slides (not reports):

### typslides (Recommended)
```typst
#import "@preview/typslides:1.3.3": *
#show: typslides.with(
  ratio: "16-9",
  theme: "dusky",
  font: "Fira Sans",
  font-size: 20pt,
  show-progress: true,
)
```

**Key commands:**
- `#front-slide(title, subtitle, authors, info)` — title slide
- `#slide(title: "...")[content]` — content slide
- `#focus-slide[content]` — centered emphasis (key takeaway)
- `#framed(title: "...")[content]` — colored box
- `#stress[text]` — bold + theme color
- `#grayed[text]` — muted secondary text

**Research Talk Rules (tight decks):**
- 5-7 slides absolute max for concept talks
- No tables on content slides
- 3-5 bullets per slide, ~40 words max
- Concept talk ≠ project proposal: no phases, no status tables, no facilities
- No filler slides (no Agenda, no Thank You, no references)
- One centered takeaway on the closing slide
- Verify name isn't taken before committing to an acronym/paper title
- No named citations of your own works on slides

**Presentation Design Discipline:**
- Choose archetype: **Concept talk** (~5 slides, argues an idea) or **Project pitch** (~8-10, proposes a research program)
- Never mix them in one deck
- Kill anything before stakes are set
- The talk title must reflect the actual question answered — no buzzwords

---

## 9. Post-Write Review Pipeline

After producing or editing any document, spawn parallel subagent reviewers before delivery.

### Review Dimensions
- **Content accuracy:** Do claims match source data?
- **Style compliance:** No em-dashes, no AI filler, no passive voice in key claims
- **Reference integrity:** Do all refs, cites, figure refs resolve?
- **Terminology consistency:** Uniform product names/acronyms
- **Structural coherence:** Narrative flow, no redundant sections
- **Missing content:** Anything referenced but absent?

### Critical Rules for Reviewers
- If a reviewer finds missing content, **do NOT invent content** to fill the gap. Flag the gap, remove broken references, and ask the user.
- Tables can be dropped if redundant (prose already explains everything).
- Restore accidentally cut content from git baseline, not memory.

### Grading
After fixes, re-run reviewers. Ship only when all sections are at least B-grade.

---

## 10. Pitfalls

### Writing Process Pitfalls
- **Skipping Step 1** — Writing before collecting data produces confident-sounding documents that cite nothing
- **Skipping Step 2** — Drafting without reviewing narrative against data produces documents that ignore critical findings
- **Softening uncomfortable findings** — If the data shows a problem and you omit it, you have failed the honesty rule
- **Merging Step 3 and 4** — Writing prose and formatting simultaneously produces messy content and broken syntax
- **Skipping Step 5** — Delivering without a final data-recheck invites scope creep and template errors
- **Template copy-paste errors** — When reusing a document for a new client, scrub for brand-specific language
- **Claim-count mismatch** — Summary count must equal detail count
- **Inventing numbers** — Never fabricate revenue impact figures
- **Infobox overuse** — When everything is in a box, nothing is emphasized. Use prose + ONE conclusion box

### Typst Compilation Pitfalls
- **Delivering Markdown as final** — Always Typst unless explicitly overridden
- **ASCII diagrams** — Never. Mermaid only
- **Interactive HTML visualizations** — Static PNG preferred. CDN-dependent HTML fails silently
- **Forgetting `typst init` before `typst compile`** — Templates must be initialized first
- **Template not found in Typst Universe** — Pick the next template from the catalog. Do not hand-craft styling
- **Non-ASCII characters in Typst** — Em-dashes, en-dashes, rupee signs, multiplication signs, curly quotes won't render with default fonts. Use ASCII-safe equivalents
- **FontAwesome icon names** — Many names don't exist in the free set and silently fail. Use only well-known free icons
- **Unverified tool claims** — Cross-check license/version claims against primary sources
- **Font warnings are non-fatal** — The PDF compiles fine even with font warnings

### Review Pipeline Pitfalls
- **Reviewers miss issues too** — Do not treat a clean review as proof of correctness
- **Over-cutting** — Verify removed content doesn't break references
- **Stale async results** — Check timestamps and git state before applying suggestions
- **Math errors in review text** — Subagents can be wrong. Use `bc -l` or Python for calculations
- **False algorithm promises** — Text saying "algorithm described below" must have actual content below

---

## References

See the `references/` and `templates/` directories in this skill bundle:

| File | Description |
|------|-------------|
| `references/typst-template-catalog.md` | Full Typst Universe template catalog |
| `references/typslides.md` | typslides package command reference |
| `references/research-deck-style.md` | Research talk deck rules |
| `references/markdown-to-typst-syntax-map.md` | Markdown → Typst conversion checklist |
| `references/typst-pitfalls-session-2026-06-08.md` | Catalog of Typst compilation pitfalls |
| `references/data-driven-figure-generation.md` | Data-driven figure generation pipeline |
| `references/tool-survey-verification.md` | Tool survey verification workflow |
| `references/data-collection-template.json` | JSON artifact schema for Step 1 |
| `templates/academic-presentation.typ` | typslides-based research deck starter |
| `templates/competitive-report.typ` | Competitive intelligence report starter |
