---
name: generating-kb-articles
description: Generate professionally formatted .docx Knowledge Base articles following the Loxihart brand template. Use when creating SOPs, reference guides, troubleshooting guides, runbooks, onboarding docs, process documents, or any internal KB article. Triggers on requests mentioning KB article, knowledge base, SOP, reference guide, troubleshooting guide, runbook, onboarding guide, internal documentation, or Loxihart-branded documents.
metadata:
  version: "1.3.0"
---

## Evals

**Should trigger:**
1. "Write a KB article for the FreshService ticket about VPN reconnect failures"
2. "Create an SOP for the Loxihart new-hire mailbox provisioning process"
3. "Generate an Loxihart-branded reference guide for the ticketing workflow"

**Should NOT trigger:**
1. "Set up the automated KB pipeline for our client" — building the generation pipeline → building-kb-pipelines
2. "Populate the screenshots in this KB draft" — screenshot capture and insertion → kb-screenshot-automator

---

<essential_principles>

This skill generates .docx KB articles that match the Loxihart Reference Guide Template exactly. Every output preserves the template's brand system, structure, and formatting.

**Brand Colors (Official Loxihart Palette):**
- Orange (Meteor): #E2690E — used for H2 headings, warning boxes
- Light Blue (Deep Space): #5391AA — used for info box borders
- Dark Blue (Eclipse): #00405F — used for titles, table headers

**Brand Constants (from Loxihart-ReferenceGuideTemplate-2026.docx):**
- Fonts: Rubik (body, 11pt), Roboto Condensed Medium (headings)
- Title: Bold, #00405F, 20pt, bottom rule
- H1: Roboto Condensed Medium, #0E2841, 24pt
- H2: Roboto Condensed Medium, #E2690E, 20pt
- H3+: Roboto Condensed Medium/Condensed, #0E2841, 18pt descending
- Warning box: border/text #E2690E, fill #FFEBDE, icon ⚠
- Info box: border #5391AA, text #043854, fill #F5FBFF, icon ⓘ
- Best Practice box: NoteBox style, top/bottom borders #DDDDDD, star bullet
- Table headers: fill #00405F, Rubik, white text
- Table alt rows: fill #F2F2F2
- Header: Logo left, "Loxihart [Department]" + category right
- Footer: "Copyright © Loxihart Inc. [Year]" left, "CONFIDENTIAL" center (#C00000 bold), "Page | #" right
- **Paragraph defaults:** Left aligned, line spacing Multiple 1.15, no extra space before/after
- **TOC styling:** H1 entries bold, H2+ entries italic and indented
- **Lists:** All bullets/numbered items size 11pt; unordered hierarchy: • ○ ▪ • ○; numbered: 1 a i 1 a; numbering resets per section
- **Callout box spacing:** Minimal spacing after callout boxes — no blank spacer paragraphs between callouts and content

**PDF and File Output Naming Standards (REQUIRED — applies to every output generated):**
- **Filename:** `Loxihart, [Full article title as written in the document header].pdf` or `.docx`
  - Auto-populated from the article title — never hardcoded or abbreviated
  - Example: `Loxihart, What To Do When BitLocker Asks for Your Recovery Key.pdf`
- **PDF meta bar text:** `Loxihart, [Short topic label]`
  - Short label describing the topic — not the article ID, version, or audience string
  - Example: `Loxihart, BitLocker Recovery Key`

**Related Articles Rule (REQUIRED — no exceptions):**
- NEVER include a "Related Articles" section unless the user explicitly provides a list of confirmed published article titles from the live KB system (e.g., FreshService)
- Do NOT generate, infer, suggest, or fabricate article references — unpublished article IDs are not real links and create broken references in the KB
- If a user asks for related articles without providing confirmed published titles, respond: "Related Articles requires confirmed published article titles from FreshService. Please provide them or skip this section."
- This rule applies to both PDF and .docx outputs

**Template fidelity is non-negotiable.** The generated .docx uses docx-js with exact Loxihart brand colors, fonts, spacing, and callout box patterns extracted from the source template.

**Doc types drive smart defaults.** Each doc type has pre-configured optional sections. Users can override.

**Interactive Q&A gathers content.** Targeted clarifying questions before generation — collect metadata, then content section by section.

**Output is always .docx** using the generation script at `scripts/generate-kb-docx.js`.

**Assets are bundled.** The Loxihart logo and callout icons are in `templates/media/`. The base template .docx is in `templates/` for reference.

</essential_principles>

<intake>

What type of KB article do you need?

1. **SOP** — Standard Operating Procedure (step-by-step process with roles)
2. **Reference Guide** — Informational reference for a system, tool, or concept
3. **Troubleshooting Guide** — Problem diagnosis and resolution paths
4. **Runbook** — Operational procedures for incidents or deployments
5. **Onboarding Guide** — New hire or role setup and orientation
6. **Process Document** — Cross-functional workflow documentation
7. **Other** — Custom KB article (specify sections needed)

**Wait for response before proceeding.**

</intake>

<routing>

| Response | Doc Type | Workflow |
|----------|----------|----------|
| 1, "SOP", "procedure" | SOP | workflows/create-article.md |
| 2, "reference", "guide" | Reference Guide | workflows/create-article.md |
| 3, "troubleshooting", "diagnosis" | Troubleshooting Guide | workflows/create-article.md |
| 4, "runbook", "incident", "operational" | Runbook | workflows/create-article.md |
| 5, "onboarding", "new hire", "setup" | Onboarding Guide | workflows/create-article.md |
| 6, "process", "workflow", "cross-functional" | Process Document | workflows/create-article.md |
| 7, "other", "custom" | Custom | workflows/create-article.md |

All types route to the same workflow. The workflow loads `references/doc-type-defaults.md` to apply smart section defaults.

**Intent-based routing:** If user provides doc type + content in their initial message, extract what's given, set type automatically, and skip to asking about gaps only.

**After reading the workflow, follow it exactly.**

</routing>

<reference_index>

| Reference | Purpose |
|-----------|---------|
| references/doc-type-defaults.md | Which optional sections to include per doc type |
| references/template-structure.md | Complete section registry with field specs |

</reference_index>

<workflows_index>

| Workflow | Purpose |
|----------|---------|
| workflows/create-article.md | Interactive Q&A → collect content → generate .docx |

</workflows_index>

<script_index>

| Script | Purpose |
|--------|---------|
| scripts/generate-kb-docx.js | docx-js script: JSON config → styled Loxihart .docx |

</script_index>

<template_index>

| Template | Purpose |
|----------|---------|
| templates/Loxihart-base-template.docx | Source template for reference |
| templates/media/logo.jpg | Loxihart logo for header |
| templates/media/warning-icon.png | Warning callout icon |
| templates/media/bestpractice-icon.png | Best practice callout icon |

</template_index>


---

## CLAIMS
<!-- [SOURCED] or [GENERATED] labels for assertions in this skill. None yet — footer added by audit fix pass. -->

## COUNTEREXAMPLE
<!-- Known cases where this skill should NOT activate or may produce wrong output -->

## CONTRADICTIONS
<!-- ! Conflicts with other skills or system prompts -->
