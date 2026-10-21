---
name: pptx-production-suite
description: Plan, route, produce, validate, and review editable PPTX deliverables from Markdown, documents, web research, existing slides, or templates. Use when a user wants to create, redesign, beautify, annotate, animate, or production-review a PowerPoint presentation and needs a clear materials checklist, suitable tool route, and a single verified final PPTX.
---

# PPTX Production Suite

Use this skill as a routing and delivery gate, not as a replacement for the actual PPTX authoring engine. It is account- and project-neutral: do not embed a customer's content, local paths, proprietary template, brand assets, API key, or internal validation tool.

## Start with a preparation checklist

Before creating files, generating images, or entering an authoring workflow, state:

1. Task type: new deck, template fill, 1:1 beautification, comment application, animation enhancement, or final review.
2. Content authority: the exact source document, current PPTX, user-provided text, or verified web source.
3. Tool route: required, conditional, and unavailable tools with their roles.
4. Materials available and missing: brand, template, images, fonts, page ratio, notes, language, and destination.
5. Next confirmation point and final acceptance standard.

Do not turn this into needless approval ceremony. Continue when the source and choices are sufficient; stop only for a missing source, template, license decision, or choice that changes the resulting deck.

## Dependency preflight

Installing this skill installs only this router. It does **not** install or copy `ppt-master`, PowerPoint, review skills, browser tools, or image tools.

Before choosing a route, check the current environment and report the result:

- `ppt-master` (or an equivalent editable-PPTX authoring engine) is required to create or change an editable deck.
- An independent review capability is required before final delivery.
- PowerPoint is preferred when native transitions or object animation must be proven.
- Image, browser, HTML, Figma, and Notion tools are conditional: require them only when the selected route needs them.

If a required dependency is absent, stop before authoring. Name the missing dependency, explain why it is needed, and tell the installer to obtain it from its trusted upstream source before restarting this workflow. Do not install dependencies, bundle their files, or silently substitute a weaker route without the user's approval.

Read `references/toolchain.md` for the dependency matrix and route rules.

## Choose one route

| Goal | Route |
| --- | --- |
| Create or reorganize an editable deck from source material | A configured PPTX authoring engine, normally `ppt-master` |
| Put new content into an existing PPTX template | The engine's template-fill route |
| Preserve every slide, order, and source text while improving layout | The engine's 1:1 beautification route |
| Apply browser/editor annotations | Apply approved comments to the actual editable source, then revalidate |
| Keep content/layout but add notes, transitions, or object animation | Native PPTX animation/notes route |
| Check a completed deck only | Production review and validation route |

Do not use HTML screenshots as final editable PPTX slides. Do not change page count, order, or source text on a 1:1 beautification request without explicit approval.

## Production rules

- Establish one content authority. Other documents or slides may be visual references but must not silently become a competing source of truth.
- Use licensed user material, clearly reusable sources, or approved generated imagery. Record each final image's source/prompt, intended use, and license decision.
- Lock content and layout before configuring native animation. Animation must reinforce slide meaning and use real target objects.
- Keep raw exports, caches, traces, rejected versions, and temporary sources out of the final delivery path.
- Never claim cross-application animation parity. PowerPoint's native package is authoritative; other viewers are supplemental checks.

## Validation and final delivery

Validate the actual PPTX, not only a screenshot:

- Slide count, aspect ratio, fonts, overflow, notes, images, and source-to-slide correspondence.
- Package readability and, when applicable, transition/object animation targets, order, and durations.
- Representative native playback in PowerPoint or an honestly stated equivalent limitation.
- No credentials, private paths, unlicensed material, customer data, or obsolete release candidates.
- A final independent review of content authority, provenance, artifacts, and validation evidence.

Deliver one verified release PPTX with its defined source snapshot. Report its path, slide count, validation evidence, and remaining human review step. Do not commit, upload, or publish unless the user explicitly authorizes it.
