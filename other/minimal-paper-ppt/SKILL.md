---
name: minimal-paper-ppt
description: Use when creating, outlining, or editing a minimalist academic PPT/PPTX deck from AI paper notes, especially outputs from $agent-paper-reader. Best for Chinese research talks, paper-reading reports, agent/LLM paper seminars, multi-paper comparisons, experiment idea decks, and clean white-background slides with large dark-blue titles, black section headers, concise bullets, and no decorative clutter.
---

# Minimal Paper PPT

Use this skill to turn paper-reading notes into a clean, editable academic PowerPoint deck. It is optimized for Chinese AI/Agent paper reading reports and should pair naturally with `$agent-paper-reader`.

## Core Style

The target style is minimalist academic notes:

- White background.
- Large centered dark-blue title.
- Black bold section headings.
- Left-aligned body text with short bullets.
- Dense enough for research discussion, but not paragraph-heavy.
- No decorative cards, no icon clutter, no gradients, no ornamental shapes.
- Avoid red spell-check underlines, overflow, cramped line spacing, and tiny text.

Read `references/minimal-academic-style.md` before building or outlining a deck in this style.

## Source Handling

Preferred inputs:

- `$agent-paper-reader` single-paper output.
- `$agent-paper-reader` multi-paper comparison output.
- Paper PDF/LaTeX plus reading notes.
- User's rough research ideas, experiment plans, or reproduction notes.

If source content is missing, first create a compact claim spine from the available notes. Do not invent paper claims, metrics, or experiment results.

When producing an actual PPTX, use the Presentations skill and artifact-tool presentation JSX. Prefer the Presentations plugin helper scripts and `createSlideContext` helpers such as `ctx.addText`, `ctx.addShape`, and `ctx.addImage` for absolute positioning. Do not rely on untested raw `slide.compose(text(..., { position: { x, y } }))` positioning. Render previews and inspect readability before final delivery.

## Deck Modes

Choose one mode:

- `single-paper-report`: one paper reading report.
- `multi-paper-comparison`: compare several papers or a literature cluster.
- `research-idea`: turn paper insights into proposed experiments.
- `reproduction-plan`: turn a paper into an implementation and evaluation plan.
- `appendix-notes`: dense discussion notes for group meetings.

Read `references/deck-blueprints.md` for slide sequences.

## Mapping From Agent Paper Reader

Map `$agent-paper-reader` sections into slides:

- Problem -> background/problem slide.
- Gap in Existing Methods -> motivation/prior gap slide.
- Proposed Method -> method overview and agent-loop slide.
- Advantages and Evidence -> experiment/evidence slide.
- Limitations and Hidden Assumptions -> limitations slide.
- What We Can Do Next -> experiment ideas or next-work slide.
- Bottom Line -> closing synthesis slide.

Read `references/paper-reader-mapping.md` when converting notes into slide content.

## Slide Writing Rules

- Every slide needs one clear claim in the title or top section.
- Prefer 3-5 bullets per slide.
- Keep each bullet to one line when possible; split long bullets across slides rather than shrinking text too far.
- Use Chinese for explanations unless the user asks for English. Keep paper names, benchmarks, and method names in English.
- Preserve technical terms accurately: planner, executor, memory, verifier, tool use, agent loop, benchmark, ablation.
- For multi-paper decks, use tables sparingly and keep them readable.
- Put citations or paper names in a quiet footer only when needed.

## Required QA

Before delivering a PPTX:

- Render slide previews.
- Check title/body text does not overlap or overflow.
- Check body text is readable at thumbnail size.
- Check all slides follow the same typography, margins, and title placement.
- Confirm the deck has no accidental spell-check underlines, broken glyphs, placeholder text, or invented claims.
- If a rendered preview shows elements piled up near the top-left corner, fix the generation code to use the Presentations context helpers for positioning before continuing.

Read `references/pptx-qa.md` for visual and content checks.

## Output Contract

If the user asks for a deck outline, return a slide-by-slide outline.

If the user asks for an actual PPTX, create the PPTX, render previews, iterate if needed, and provide the final file path plus a short summary of the deck structure.

If the source is an `$agent-paper-reader` output, explicitly say which sections were mapped into slides.
