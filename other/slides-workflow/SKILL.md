---
name: slides-workflow
description: "Apply a narrative-first workflow to plan, write, build, and validate strategic presentations and HTML slide decks with responsive layouts, design tokens, data visualization, speaker-ready copy, and accessible exports. Use when the user requests this workflow or wants an additional slide-quality pass alongside installed presentation tooling. Turkish triggers: sunum oluştur veya düzenle, slayt akışı ve görsel kalite, PPTX'i doğrula."
---

# Slides

Design a narrative first and a visual deck second. Resolve skill-dir to this folder before using bundled search and validation tools.

## Workflow

1. Define audience, decision, time limit, slide count, evidence, brand, and output format.
2. Write a one-sentence narrative and a slide-by-slide argument before layout.
3. Choose one strategy and layout family.
4. Use one message per slide; move supporting detail to notes or appendix.
5. Build from design tokens and reusable slide patterns.
6. Turn data into a stated insight, not decoration.
7. Validate sequence, evidence, readability, overflow, contrast, and export behavior.

Read only the needed reference:

- references/slide-strategies.md for narrative structures;
- references/layout-patterns.md for composition;
- references/copywriting-formulas.md for concise persuasion;
- references/html-template.md for HTML deck structure;
- references/create.md for the complete creation flow.

## Search the bundled slide library

~~~text
python "<skill-dir>/scripts/search-slides.py" "investor pitch" -d strategy
python "<skill-dir>/scripts/search-slides.py" "metrics dashboard" -d layout
python "<skill-dir>/scripts/search-slides.py" "problem urgency" -d copy --json
~~~

Use returned patterns as candidates; adapt them to the audience and evidence.

## Implementation rules

- Use semantic design tokens for color, type, spacing, and chart styling.
- Keep text within safe margins and test the smallest intended viewport.
- Provide alt text or a text summary for charts and meaningful images.
- Label axes, units, dates, samples, and sources.
- Prefer editable text and vector shapes over text baked into images.
- Keep animation optional, purposeful, and reduced-motion compatible.

## Output contract

Provide:

- narrative and slide outline;
- final deck or implementation files;
- source list and chart-data provenance;
- speaker notes when requested;
- validation results for overflow, links, contrast, and export.

## Guardrails

- Do not invent metrics, testimonials, citations, or customer logos.
- Do not shrink body text to force excessive copy onto one slide.
- Do not use a chart without stating its takeaway.
- Do not hardcode a provider, model, or host-specific path.
