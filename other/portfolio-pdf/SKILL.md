---
name: portfolio-pdf
zh_name: "作品集 PDF"
en_name: "Portfolio PDF"
emoji: "📄"
description: "A designer's portfolio as a PDF or an image set for one situation: a job application, a client, a school (titled pieces within its limits) or a promotion packet with a criteria map, from their work library and a saved target."
en_description: "A designer's portfolio as a PDF or an image set for one situation: a job application, a client, a school (titled pieces within its limits) or a promotion packet with a criteria map, from their work library and a saved target."
category: slides
scenario: personal
tags: ["portfolio pdf", "pdf portfolio", "school portfolio", "slideroom", "promotion packet", "promo packet", "作品集PDF"]
triggers:
  - "portfolio pdf"
  - "pdf portfolio"
  - "portfolio for school"
  - "slideroom"
  - "promotion packet"
  - "promo packet"
od:
  mode: deck
  craft:
    requires:
      - typography
      - accessibility-baseline
      - anti-ai-slop
  scenario: personal
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
  example_prompt: "A 10 MB PDF of my portfolio for the Acme senior product designer job, from my work library, with a short cover note."
---

<!-- Kit skill (openspec add-tailored-portfolios). -->
# Portfolio PDF

A portfolio as pages: one `.slide` per page at the target's size, exported as a PDF within its size limit, or as one image per piece for a school. It is always built for a **target** (`save_open_design_portfolio_target`), which picks the projects, their order, the privacy ceiling, the cover note and the limits.

## Before the first page

1. **Read the library** (`get_open_design_library`) and the target. If there is no target for this situation, save one: its name and kind, the pasted ad, brief, rules or criteria as `notes`, and the projects. Show the suggested order with the words each project matched, and let the designer change it.
2. **Brief** with `prepare_open_design_brief` and `portfolio: { target: "<slug>" }`. The brief lists the target's projects in order, only work within its ceiling, the cover note, the page size and the limits, and its kind's part. Register with the same `portfolio`.
3. **Check** with `check_open_design_artifact`, then **export**: `export_open_design_artifact` with `format: "pdf"` and the target's `maxBytes`; for a school image set, `format: "jpeg"` with the image limit as `maxBytes`. If the PDF can't fit, the export names the heaviest pages: use smaller pictures there or split them.

## Pages

- Page size from the brief: A4 or US Letter (landscape for screens, portrait for posters and print work) or 16:9. Set it on `.slide` and in `@page`.
- **Cover**: the designer's name, role, contact and the cover note, unchanged. Mark it `data-od-cover`.
- **Per project**: a summary page (role, team, dates, the main outcome), then the decisions with the chosen and rejected options, then the outcome, exactly as the brief writes it. Two to five pages a project; mark each project's pages `data-od-project="<slug>"`.
- Pictures with the brief's markup only (`data-od-asset` on each), so export can check them against the ceiling.
- A closing page with contact details.

## By kind

- **Job**: lead with the projects the ad's words matched; echo the ad's words only where the library supports them.
- **Client**: a "For you" page after the work, marked `data-od-for-you`, linking the redesign concept and before/after page the brief names, called a concept.
- **School**: one piece per `.slide`, each with `data-od-piece="<title, year, medium>"` (the exported file takes its name from it), exactly the number of pieces the school takes, each image within its limit. Follow the school's own naming and caption rules from the notes.
- **Promotion**: after the cover, a criteria map: a table with every criterion in order, each row marked `data-od-criterion`, the projects and outcomes that show it, and "No evidence yet" where there is none. Never drop a criterion and never stretch a project to fit one. Promotion packets are internal: export as a file only.

## Rules

- Only library facts; ask for what's missing, or leave it out.
- Nothing stricter than the target's ceiling. Export and publish refuse it and name the picture.
- Tokens only, from the design system's `:root`.
