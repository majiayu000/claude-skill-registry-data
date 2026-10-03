---
name: slide-design
description: Research slide communication. Use when creating, revising, polishing, or reviewing Beamer, PowerPoint, Keynote, or browser slide decks.
user-invocable: true
---

# Slide Design

Beamer is the first-class implementation target; the principles apply across deck formats.

## Stage-Scoped References

Load per stage; do not load them all at every dispatch:

| Reference | Load when |
|---|---|
| `references/planning.md` | PLAN phase - audience-context inventory, deck objective, structure, and main-vs-backup policy. |
| `references/beamer-techniques.md` | IMPLEMENT when creating or refactoring Beamer source, frame structure, columns, figures, tables, equations, navigation, or reusable commands. |
| `references/beamer-overlays.md` | IMPLEMENT when writing Beamer overlays, incremental reveal, alerts, backup links, or stable multi-step technical slides. |
| `references/layout-checks.md` | IMPLEMENT or review when editing Beamer, checking line wraps, overflow, figures, overlays, or final PDF layout. |
| `references/integration.md` | INTEGRATE / final polish - deck-wide consistency, buildability, backup-slide hygiene, and communication review. |

For bundled scripts and assets, `<skill-dir>` is the directory containing this `SKILL.md`; substitute the real path before running commands or copying files.

**Non-Beamer decks (PowerPoint, Keynote, browser slides):** the Core Principle, Audience Context Discipline, Techniques, and non-Beamer-specific checklist items apply; the Beamer references, starter template, and `check_slide_layout.py` do not. Read the build/layout `[BLOCKING]` item as "the deck renders or exports without overflow or unresolved placeholders, verified in the target tool."

## Core Principle

Slides are live communication artifacts. A slide succeeds when the audience recovers the intended point in real time, with imperfect attention and uneven background knowledge.

When rigor and live comprehension compete, preserve the truth of the claim and prioritize the version the audience can understand now. Move derivations, robustness, caveats, and expert objections to oral narration, notes, backup slides, appendix slides, or linked material when they would overload the main path.

**Never use `\resizebox` on text or equations.** It mechanically shrinks content to fit rather than making a design choice, sacrificing visual consistency and signaling that the slide says too much. Content overflowing a slide: simplify it, split the slide, or move material to backup. Exception: `\resizebox` is acceptable for standalone figures or diagrams where mechanical scaling hides no information. Font-size commands (`\small`, `\footnotesize`, etc.) are fine as intentional design choices — de-emphasizing source citations or secondary labels, for example.

## Audience Context Discipline

Run an audience-context pass before optimizing wording or visual style:

- Pick a representative audience member for this talk, not an ideal reader of the paper.
- Per section and dense slide, state what the audience already knows, what they do not know yet, and what they may wrongly infer from familiar terms.
- Per visible line: "What thought should this line trigger?" Then: does the audience have enough context to think it?
- Phrases multiple fields would read differently: add framing before the phrase, or replace it with the intended interpretation.
- Reintroduce unusual notation, model objects, samples, and objectives when they return after a gap.

## Techniques

### Context Engineering

- Lead with the takeaway before evidence when the evidence has many plausible interpretations.
- Use section openers and roadmap returns to tell the audience what question the next block answers.
- Put the slide's purpose in the title or first line when the slide is not self-evident.
- Split main slides and backup slides by audience need: typical-audience context stays on the main path; expert completeness goes to backup.

### Attention Management

- Every visible element competes for attention. Remove, delay, gray out, shrink, or move detail outside the current point.
- Overlays when early material must stay visible for later steps; multiple lighter slides when later steps don't need it on screen.
- Alerts, boldface, color, and size identify the current point and connect related text/equation pieces.
- De-emphasize sources, caveats, and secondary notes rather than letting them compete with the main claim.
- Design for recovery after distraction: a distracted audience member can skim the slide and rejoin the talk.
- Beamer overlay mechanics: load `references/beamer-overlays.md` and reuse `<skill-dir>/assets/beamer-starter-template.tex`.

### Simplification

- One sharp line over a formally complete sentence.
- Short bullets; one-line bullets are a strong default, not an absolute rule.
- Avoid three nested itemize levels on main slides.
- Equations: the minimum expression the live point needs; full derivations and general forms go to backup unless the derivation is the point.
- Tables: only the columns and rows the claim needs, with visual emphasis on the comparison the audience should make.

## Quick Checklist

The implementer walks it before DONE; the reviewer walks what its focus covers. `[BLOCKING]` items must be fixed for APPROVE; `[ADVISORY]` items are recorded and do not block.

- `[BLOCKING]` Audience context established before major claims, unusual notation, nonstandard samples, or field-specific terms. Inside a superRA task tree, verify against the audience-context inventory recorded at planning time (`references/planning.md §Audience-Context Inventory`); standalone, state the assumed representative audience member in the review notes and judge against that.
- `[BLOCKING]` Each main-path slide has a clear communication role: setup, takeaway, evidence, mechanism, transition, or recovery/roadmap.
- `[BLOCKING]` Dense slides use overlays, visual cues, simplification, or a backup split to control attention.
- `[BLOCKING]` Technical rigor intact: omitted details are unnecessary for the live point or available through oral narration, notes, backup slides, appendix slides, or links.
- `[BLOCKING]` No `\resizebox` on text or equations (see Core Principle).
- `[BLOCKING]` Beamer/PDF output builds when the task edits source, with no ignored overflow or missing-asset warnings.
- `[ADVISORY]` Main-slide bullets mostly one line; wrapped bullets retained only when the extra words materially help communication.
- `[ADVISORY]` Titles and first lines state the takeaway or slide purpose rather than only naming the topic.
- `[ADVISORY]` Navigation aids, slide numbers, and backup-slide numbering orient the audience without drawing attention from content.
- `[ADVISORY]` New visual styling stays inside the deck's existing color and command vocabulary — no ad-hoc colors or one-off styling.

## Layout Triage

For Beamer decks, `uv run --script <skill-dir>/scripts/check_slide_layout.py` is the cheap nonvisual pass for likely line wraps, overfull boxes, missing figures, and text near slide boundaries. Load `references/layout-checks.md` for evidence interpretation and layout guidance.

## Beamer Implementation

Start new decks from `<skill-dir>/assets/beamer-starter-template.tex` — it carries the house design language (theme, palette, frame/title templates, list markers, semantic commands) and an overlay command reference. Do not rebuild a preamble from scratch when the template applies.
