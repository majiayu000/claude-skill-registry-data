---
name: presentation-builder
description: "Design standards-aligned K-12 instructional slide decks / presentations. Use this whenever a teacher or coach wants slides, a slideshow, a deck, a 'PowerPoint', or a Google-Slides-style presentation for teaching — including 'turn this lesson into slides', 'make a presentation on…', 'slides for tomorrow's class', or 'a deck to introduce…'. It structures a pedagogically sound deck (one idea per slide, gradual release, visuals, checks for understanding), keeps it aligned to a real cited standard and readable for the grade band, and renders the actual .pptx using the pptx skill. Make sure to use this whenever the user wants teaching content in slide form. Do NOT use it to write the lesson plan itself (use lesson-planner) or to build a test/rubric (use assessment-designer) — it presents instruction, it doesn't replace it."
---

# presentation-builder

Designs classroom slide decks that teach well, then renders them to `.pptx`.

## 1. Follow the pipeline (`references/method.md`)
Within Generation: `Analysis → Standards Alignment → Differentiation → Generation`.

1. **Analysis** — topic, grade band, subject, purpose (intro / direct instruction / review), and how
   many minutes. If a lesson plan already exists, build the deck *from it*. Log assumptions
   (`references/assumptions-protocol.md`).
2. **Standards Alignment** — anchor the deck to a real, cited, verified standard
   (`shared/standards/`, `references/standards-verification.md`).
3. **Differentiation & accessibility** — UDL (visuals + words + audio cues), grade-appropriate
   reading level (`shared/quality/readability-age.md`), high-contrast/large-text, alt text for images;
   keep the cognitive load low (one idea per slide).
4. **Generation** — draft the deck as a **slide outline** using
   `assets/templates/slide-outline-template.md` and the design rules in
   `references/slide-design.md`, then **render a real `.pptx`** with `scripts/build_deck.py` (the shared
   Office engine `shared/office/`, python-pptx — `--pdf` also renders a PDF via LibreOffice for visual
   QA). If the Office library isn't installed, it writes the slide spec and reports an honest gap — the
   host's native `pptx` skill can consume that same spec. Either way, **do not re-implement PowerPoint
   generation** by hand.

## 2. Validate, then gate
Run the universal + slide checks (`references/verification-checklists.md`), self-score against
`references/quality-gates.md`, then hand to **quality-review**.

## 3. Always emit the metadata block
Per `references/metadata-schema.md`, including the standard, grade band, and
`human_review_required: true`. Use placeholder student content only — never real student data.

Artifact types: `references/artifact-types.md`. Outline template: `assets/templates/`. Worked
example: `examples/grade3-fractions-slides.md`.
