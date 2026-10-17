---
name: aiwf-avoid-ai-design
description: AIWF design-audit and rewrite workflow for removing generic AI-designed UI and document layout patterns. Use when Codex must detect, audit, or fix AI-looking design in Gradio apps, PDFs, document layouts, web pages, React/Tailwind/shadcn, dashboards, static sites, screenshots, generated reports, or frontend code. Triggers include teal everywhere, purple or blue gradients, generic rounded-card layouts, default Gradio/shadcn styling, AI-looking PDF reports, document layout cleanup, de-slop UI, make it look less AI-generated, design complaints, or layout polish for local AI tools.
---

# AIWF Avoid AI Design

## What This Is

Use this skill to audit and fix design patterns that make local AI tools, reports, and websites look machine-generated.

This is a design-quality tool, not a verdict. A teal button, centered hero, or rounded card is not proof that a model made the artifact. The signal matters when defaults cluster: teal on every control, Inter everywhere, identical cards, generic PDF covers, decorative gradients, no layout rhythm, and no clear reason for any choice.

The job is simple: replace defaults with decisions while preserving the product, code behavior, data, accessibility, and document meaning.

## Modes

`rewrite` is the default when the user points at files and wants them fixed.

`detect` flags design tells only. Use it when the user says scan, audit only, flag only, do not edit, or asks what looks AI-generated.

`edit` applies narrow in-place changes to named files. Use it when the user asks to clean a specific Gradio file, React component, CSS file, PDF source, report template, or document layout.

## Required Workflow

1. Scope the artifact: Gradio app, PDF/report, document, web page, React component, dashboard, screenshot, or full app.
2. Read the actual files first. If only a screenshot or PDF is provided, inspect the visual artifact directly.
3. If the result is visual and a renderer is available, render it. Use screenshots for web/React/Gradio and page renders for PDFs before making visual judgments.
4. Read `references/ai-design-tells.md` for the tell catalog.
5. Read `references/surface-fix-playbooks.md` for the relevant surface: Gradio, PDF/document, React/web, or dashboard.
6. For web pages, React surfaces, dashboards with public-facing areas, or marketing pages, read `references/modern-web-appeal.md` before judging what should replace the AI-looking design.
7. Audit by severity. Mark findings as `code-certain`, `visual-certain`, or `inferred`.
8. Commit to one direction before editing: palette stance, typography stance, layout stance, density, and one signature detail.
9. Edit narrowly. Preserve behavior, props, callbacks, data flow, routing, validation, labels with functional meaning, and accessibility.
10. Re-audit the result. Fix any P0 tells that survived.
11. Verify with the cheapest useful proof: screenshot, PDF render, local build, lint, focused test, or source diff.

## Severity

P0 means a non-designer notices it fast:

- teal used as the answer to every design problem
- purple/blue gradients, glow blobs, or gradient headline text
- default Gradio or shadcn styling shipped as the design
- centered hero plus three identical feature cards
- AI-looking PDF cover pages with huge title, teal strip, soft gradient, and icon cards
- every surface using the same radius, border, shadow, padding, and icon treatment

P1 means a designer or developer notices it:

- Inter, Roboto, Geist, or system stack with no pairing or hierarchy
- `rounded-2xl shadow-lg`, `container mx-auto px-4`, untouched `zinc` or `slate`
- Lucide `Sparkles`, `Zap`, `Rocket`, or emoji used as generic AI/product marks
- colored left-border cards, pill badges, four-column footers, fake stat strips
- Gradio tabs and accordions used as a dumping ground for every control
- PDF tables, callouts, and headings all using the same weight and spacing

P2 means craft polish:

- flat spacing rhythm
- weak contrast
- no empty/loading/error/focus states
- over-structured documents with too many headings and bullets
- motion that is either absent everywhere or copied everywhere

Fix P0 and P1 in normal passes. Fix P2 when it is cheap or when the surface is public-facing.

## Context Profiles

`gradio-local-ai`: Be practical and dense. Put core controls near the main action. Avoid decorative wrappers. Teal is allowed only as a restrained accent, not a whole theme.

`pdf-report`: Use a document grid, real hierarchy, source notes, page numbers, table discipline, and print-safe contrast. Avoid hero-style covers unless the report is meant for marketing.

`document-layout`: Preserve the content and reading order. Fix margins, headings, tables, callouts, captions, and section rhythm before changing wording.

`react-web`: Render before judging. Check CSS, Tailwind classes, component primitives, routes, states, and responsive behavior. Do not rebuild an app when a component pass is enough.

`dashboard`: Favor scan speed, density, clear grouping, status meaning, and tables that survive repeated use. Do not turn operational tools into landing pages.

`marketing-page`: Use real product/place/object imagery or screenshots when possible. The first viewport should signal the actual subject, not a generic value prop wrapper.

State which profile you are using and why.

## Source-Backed Web Appeal

For modern web pages, do not replace AI-looking design with trend-chasing. Use `references/modern-web-appeal.md` to ground the direction in human appeal, credibility, accessibility, responsiveness, and performance.

The short rule: appealing human design makes the page easier to trust, scan, use, and revisit. It does not hide the real product behind generic gradients, identical cards, vague claims, or heavy animation.

## Guardrails

- Do not break working UI or report generation to make it prettier.
- Do not trade teal for another default such as purple gradients, beige startup minimalism, or dark slate cards.
- Do not invent brand claims, metrics, testimonials, or product features.
- Do not hide core AIWF controls in advanced accordions when they should be obvious near Generate or Run.
- Do not add heavy dependencies or start GPU work unless the user asked for it.
- For prose-heavy copy, README/docs text, PDF narrative, or public-facing UI copy, run the AIWF prose scan from `aiwf-avoid-ai-pushes` before finalizing.
- If the artifact is already intentional, say so and stop. A clean audit is a valid result.

## Output Format

For `detect`:

1. Issues found, grouped by P0/P1/P2, with file or page location and confidence.
2. Assessment, with what must change and what is a judgment call.

For `rewrite` or `edit`:

1. Audit summary, grouped by severity.
2. Direction chosen, stated in concrete design moves.
3. Edits made, naming files and the meaningful changes.
4. Verification, including screenshot/build/test/PDF-render results when available.
5. Second-pass audit, especially whether any P0 tells remain.

Keep the final report short. The files and screenshots are the proof.
