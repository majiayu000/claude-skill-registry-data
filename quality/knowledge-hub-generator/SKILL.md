---
name: knowledge-hub-generator
description: >-
  Draft and quality-check pages for the IPA Knowledge Hub in the site's house
  style. Use when creating a new .qmd Hub page from source material, adapting
  outside content into a Hub page, or reviewing an existing page for structure,
  tone, frontmatter, references, and Diátaxis fit. Replicates the
  quality-control workflow of IPA's Knowledge Hub Generator assistant.
---

# Knowledge Hub Generator

Draft accessible Hub pages and quality-check them against the site's
conventions. This skill packages the house style that IPA's Knowledge Hub
Generator assistant applies, so any contributor produces pages consistent with
the rest of the Hub.

The Hub is a **public** Quarto site of research and data-science guidance for
Innovations for Poverty Action (IPA), organized by the Diátaxis framework
(tutorial / how-to / reference / explanation). Pages are `.qmd` with YAML
frontmatter. The value the Hub adds is research-and-operations context --- not
restating tool documentation that already exists elsewhere.

## When to use this skill

- Drafting a new Hub page from notes, a slide deck, a paper, or another
  document.
- Adapting outside or internal material into a public Hub page.
- Reviewing or revising an existing page for structure, tone, frontmatter,
  references, and Diátaxis fit.

## Core principles

These shape every drafting and review decision. Detail lives in
`references/page-anatomy.md`.

1. **Pick the Diátaxis type first.** The type determines the whole structure, so
   settle it before drafting. Ask the human whether the page is a **tutorial**,
   **how-to guide**, **reference**, or **explanation**; if the material makes
   the type obvious, propose one and confirm. The type is machine-read, not just
   editorial: it goes in the page's `categories:` frontmatter, where the
   `_extensions/diataxis-badge` filter renders it as a badge above the title and
   the How-to Guides hub (`how-to-guides.qmd`) auto-lists every page categorized
   `how-to`. Read `references/diataxis-framework.md` for what each type is for
   and how it should read (grep the file for the type name, e.g.
   `How-to guides`, to jump to its section). The four canonical sources:
   tutorials <https://diataxis.fr/tutorials/>, how-to
   <https://diataxis.fr/how-to-guides/>, reference
   <https://diataxis.fr/reference/>, explanation
   <https://diataxis.fr/explanation/>. Diátaxis is the work of Daniele Procida
   (<https://diataxis.fr/>), used under CC BY-SA 4.0; cite the website when you
   reproduce it.

2. **Public audience first.** Write for a competent reader at any research
   organization. Keep IPA-specific content --- the Enterprise license, internal
   guidelines, Box links, support channels, named projects --- out of the main
   flow and inside a `callout-note` (or `callout-warning` for a data-safety
   rule). Rule of thumb: *if it would not apply to someone at another
   organization doing similar work, it belongs in a callout.*

3. **Point, do not duplicate.** For install steps, API details, and anything a
   tool's own documentation maintains, link to the canonical source rather than
   reproducing it. Reproduced steps go stale; the Hub's value-add is context.

4. **Recommended path only; no negative-space writing.** Give the reader the one
   recommended way to do the thing. Do not enumerate tools, alternatives, or
   options the reader does not need, and do not describe what the page is *not*
   covering.

5. **Never fabricate references.** Cite only sources that appear in the supplied
   material or that have a real, verifiable URL. If a claim needs a citation and
   none exists, flag it to the human rather than inventing one.

## Drafting workflow

1. **Confirm objective, audience, and type.** Ask what the page is for and who
   reads it, and settle the Diátaxis type (principle 1). Ask for the source
   material if it has not been supplied. Do not draft a page unprompted --- this
   skill supports the human writing the page, it does not replace them.

2. **Pick the page archetype.** Hub pages come in two shapes, and the choice
   follows from the Diátaxis type and content area (see the map in
   `references/page-anatomy.md`):
   - **Prose page** (explanation / reference, and prose how-to) --- `abstract`,
     a Key Takeaways callout, prose with nested callouts and tables. Follow
     `references/page-anatomy.md`; canonical example
     `research-design/research-methods.qmd`.
   - **Tutorial / how-to page** (hands-on, step-by-step) --- Recognition and
     Attribution box, Learning Objectives, input/output code, exercises, and a
     Key Points closer. Follow `references/tutorial-pattern.md`; canonical
     example `data-science/data-analysis/for-loops.qmd`.

3. **Draft the page** with the complete shared frontmatter, the archetype's body
   structure, and --- when the page has real sources --- References / Additional
   Resources in Chicago author-date format. `just new-page <dest>` creates a
   page from `page-template.qmd`.

4. **Place the file and wire it up.** Use lowercase-hyphenated names; each
   directory has an `index.qmd`. `_quarto.yml` uses one sidebar per topic
   section (hybrid navigation): find the sidebar with the matching `id:` (e.g.
   `data-quality`) and add a `text:`/`href:` pair in the right place. Pages
   listed in no sidebar show none. Also add the page to its section's
   `index.qmd` link cards.

5. **Quality-check before handing back.** Run the checklist in
   `references/qc-checklist.md`. At minimum, run `just vale-file <file>`
   (writing style) and `just fmt-md <file>` (markdown formatting) on every page
   created or modified, and fix what they report.

## Reviewing an existing page

Work in small chunks --- one page or one section at a time --- rather than
sweeping many pages at once. Apply the core principles and the QC checklist, and
confirm with the human before making significant structural changes to existing
content.

## Bundled references

- `references/page-anatomy.md` --- the house style: the two page archetypes and
  when to use each, shared frontmatter, the prose-page structure, public-first
  callouts, credits, references, and shared formatting (headings, images,
  tables, code blocks, index landing pages). Read this before drafting or
  reviewing.
- `references/tutorial-pattern.md` --- the Carpentries-style tutorial / how-to
  structure (Recognition and Attribution, Learning Objectives, input/output
  code, exercises, Key Points). Read this when the page is hands-on.
- `references/diataxis-framework.md` --- the full Diátaxis framework reference.
  Read the section for the page's type before drafting; grep for the type name
  to jump to it.
- `references/qc-checklist.md` --- the quality-control steps to run before
  handing a page back. Read this before finishing any page.
