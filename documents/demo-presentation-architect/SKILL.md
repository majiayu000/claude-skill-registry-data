---
name: demo-presentation-architect
version: 1.1.0
description: Design slide-deck specifications — slide budget, narrative arc, splitting rule, takeaway-led titles, body word budgets, per-slide layout from a fixed catalog. Outputs one `.md` slide-by-slide; never HTML/PDF/PPTX. Always interviews for language + core info first. Use when authoring presentation specs.
---

# Demo Presentation Architect

Design and refine **slide-deck specifications** as a markdown document. Each slide is described by its layout (from a fixed catalog) and its exact text content. This skill never produces HTML, PDF, or PPTX — only the `.md` source another tool (or designer) will consume. Layout catalog in [LAYOUTS.md](LAYOUTS.md); slide-spec template, anti-patterns, and review checklist in [RECIPES.md](RECIPES.md).

## 1. Scope boundaries

- **Output is always one `.md` file.** No HTML, PDF, PPTX, image generation, or styling code. If the user asks for a rendered deck, refuse and offer the `.md` instead.
- **Pairs with — but is distinct from — [[demo-script-architect]].** This skill defines what the audience *sees on each slide*; the script skill defines what the presenter *says*. Both can be produced for the same demo, but they are separate deliverables.
- **Visual exemplar.** A reference HTML deck in this skill folder demonstrates how the layouts look when rendered. The skill never reproduces or regenerates that HTML — it only mines layout *shapes* from it. The full layout catalog and design conventions live in [LAYOUTS.md](LAYOUTS.md).

## 2. Interview-first protocol

**Never start writing the deck without finishing the interview.** Ask in order; wait for each answer:

1. **Language.** "Which language should the deck be written in?" Every piece of slide text — titles, bullets, captions, speaker notes — must be in this language. Do not mix languages unless the user explicitly asks for a bilingual deck.
2. **Main info.** "What is the core content of the presentation?" Probe until you have: **topic** (one sentence), **audience** (technical level, role, prior knowledge), **goal** (think/do/feel by the end), **duration / slide budget**, **source material** (links, docs, prior decks), **constraints** (branding, required slides like title/agenda/Q&A/contact, forbidden content).

Only after both answers are collected, propose the **deck outline** (one line per slide: layout + headline) and wait for approval before expanding into full slide specs.

## 3. Core principles

- **One idea per slide.** If a slide carries two ideas, split it. The headline must be the single takeaway.
- **Layouts come from the fixed catalog in [LAYOUTS.md](LAYOUTS.md).** Never invent a layout name; if none fits, follow LAYOUTS §5 and wait for approval.
- **One title accent per slide.** Every content-slide title has exactly one `<em>...</em>` accent phrase carrying the takeaway word (LAYOUTS §4).
- **Text is final copy, not placeholder.** Write the actual headline, bullets, captions, and speaker notes — never `[insert title here]` or lorem ipsum.
- **Visual hierarchy is explicit.** Each slide spec states what the eye should land on *first*, *second*, *third*.
- **Progressive disclosure across slides.** Concepts build: define → illustrate → apply → summarize. Don't introduce a term on a slide without defining it first (or marking it as assumed knowledge).
- **Speaker notes are optional and short.** Reminders for the presenter — not a script. Use [[demo-script-architect]] for the full narrative.
- **Accessibility-aware copy.** Headlines under ~10 words. Bullets parallel in structure. No text-only color cues ("the red ones"). Image fields always include `alt:` text.

## 4. Content distribution across slides

Decide *which slides exist* before *what's on each*. Apply in order.

### 4.1 Slide budget

Convert duration into a slide count. Default cadence: **~90–120 seconds per content slide** (lower for fast demos, higher for technical deep-dives). Subtract fixed slots (§4.2) from the total. When duration and a requested slide count disagree, surface it as an open question.

### 4.2 Fixed structural slots

Every deck reserves these in order:

- **Open:** `cover` (always).
- **Optional orientation:** team/about, agenda, context — only when the audience needs them.
- **Body:** N content slides driven by the arc (§4.3).
- **Section dividers:** insert `section-divider` slides when the deck has ≥3 distinct sections; skip for ≤8-slide decks.
- **Close:** `recap-numbered` when there are ≥3 takeaways, AND/OR `closing-cta`. A live-demo handoff slide ends with a `handoff-band`.

### 4.3 Narrative arc

Pick the arc that matches the goal from §2 — it drives the order of body slides. Five arcs (Problem→Solution, System tour, Before/After, Discovery, Tutorial) with sequences and when-to-pick guidance in [RECIPES § 2](RECIPES.md#2-narrative-arcs). **Mixing arcs mid-deck breaks the audience's mental model** — pick one and stay with it.

### 4.4 Splitting rule — one idea per slide

If a candidate slide carries two takeaways, split it. Tell-tale signs:

- The title needs an "and" or a comma joining two unrelated phrases.
- The body would exceed the layout's word budget (§5.5).
- Two card-grids appear on the same slide.
- The `Transition` line would have to introduce a brand-new idea instead of bridging.

When splitting, order by **progressive disclosure**: define a term before the slide that uses it; show a component before the diagram that connects it.

### 4.5 Repetition discipline

A concept appears on at most **two** slides: once when introduced, once when recapped. If it shows up three times, two of the three are redundant — cut. The `recap-numbered` slide counts as the second mention.

## 5. Per-slide content organization

Once a slide's topic is fixed, organize its content using these rules.

### 5.1 Title carries the takeaway, not the topic

The title is what the audience remembers if they read nothing else. Prefer the conclusion over the label. Side-by-side weak vs strong examples in [RECIPES § 3](RECIPES.md#3-title-takeaway-phrasing--examples).

The `<em>` accent always carries the takeaway word.

### 5.2 Eyebrow names the section, not the slide

Use the section label from the arc (§4.3). It recurs across multiple slides in the same section. Don't restate the title or the takeaway here — the eyebrow is *context*, the title is *content*.

### 5.3 Reading flow

The eye lands on, in order: **eyebrow → title → body → callout → footer**. The heaviest visual weight belongs on the title; body content must not compete with it. The `Visual hierarchy` block in the slide spec makes this explicit per slide.

### 5.4 Ordering items within a layout

Different layouts have different ordering principles (importance, salience, chronology, primary→secondary, clockwise from top-left, Western reading flow). Per-layout-family table in [RECIPES § 4](RECIPES.md#4-ordering-items-within-a-layout).

### 5.5 Body word budget

Each layout has a sweet spot — `cover`/`quote` ≤40 words, `title-bullets`/`card-grid` ≤120, hub-spoke / showcase-split ≤140, recap/stat-row ≤80. Full per-layout table in [RECIPES § 5](RECIPES.md#5-body-word-budget-per-layout). Over budget → move detail to speaker notes or split the slide.

### 5.6 Speaker notes scope

Notes capture the *why* and timing cues ("pause here", "answer the question they'll have"). Notes never restate slide text. Keep them ≤40 words per slide. For full narration, hand off to [[demo-script-architect]].

## 6. Per-slide specification format

Every slide in the output `.md` follows the same block shape with `## Slide N`, `**Layout:**`, `**Purpose:**`, `### Content`, `### Visual hierarchy`, optional `### Speaker notes`, and `### Transition`. Field names inside `### Content` come from the chosen layout's required/optional fields in [LAYOUTS § 2](LAYOUTS.md).

Full template in [RECIPES § 1](RECIPES.md#1-per-slide-specification-format).

The `Transition` line is what makes the deck feel like a story rather than a pile of slides. **Mandatory on every slide except the final one.**

## 7. Layout catalog

The full layout taxonomy lives in [LAYOUTS.md](LAYOUTS.md):

- **§1 Primitive blocks** — eyebrow, title-with-accent, slide-footer, card, callout-band, pill-tags, mini-visual, numbered-step, person-card, handoff-band.
- **§2 Layout catalog (14 layouts)** — `cover`, `section-divider`, `title-bullets`, `title-paragraph`, `card-grid`, `profile-grid`, `feature-comparison`, `diagram-hub-spoke`, `showcase-split`, `mode-comparison`, `recap-numbered`, `closing-cta`, `quote`, `stat-row`.
- **§3 Decision flow** — questions in order; first match wins.
- **§4 Design conventions** — accent rule, eyebrow rule, footer rule, single-takeaway rule, card-count caps, language consistency, image alt-text.
- **§5 Adding a new layout** — required procedure when no existing layout fits.

Pick layouts from §2; never invent. If none fits, follow §5.

## 8. Anti-patterns + review checklist

Common anti-patterns (placeholder text, multi-idea slides, invented layouts, wall of text, mixed languages, missing transitions, decorative-only images, multiple `featured` cards) in [RECIPES § 6](RECIPES.md#6-anti-patterns). Pre-handoff review checklist (17 items covering language, accent, layout legitimacy, footer/numbering, hierarchy, transitions, slide count, required slides, card-count caps, placeholders, alt text, takeaway titles, word budgets, arc consistency, repetition) in [RECIPES § 7](RECIPES.md#7-review-checklist).

## 9. Output deliverables

Outline → full slide spec → layout-usage audit → transition map → open questions. Full list in [RECIPES § 8](RECIPES.md#8-output-deliverables).
