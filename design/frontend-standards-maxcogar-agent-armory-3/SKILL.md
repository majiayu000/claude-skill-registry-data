---
name: frontend-standards
description: "The Expert Standard applied to frontend engineering and UI/UX. Activates whenever Claude is building, modifying, or evaluating any user-facing interface — React components, HTML pages, forms, dashboards, navigation, layouts, modals, or any interactive UI element. This skill ensures frontends are evaluated against established UI/UX standards (WCAG 2.2, Nielsen's heuristics, Gestalt principles, semantic HTML, responsive design, performance budgets) rather than pattern-matched against what modern websites typically look like. If Claude is writing JSX, HTML, CSS, or any frontend code, this skill applies. If Claude is making a layout decision, choosing a component pattern, designing a form, or building navigation, this skill applies. Covers both visual design and engineering correctness — aesthetics and usability are both part of the standard."
---

# Frontend Standards

## Why This Exists

When Claude builds a UI, the natural reference point is "what do modern websites look like?" That produces interfaces that resemble other interfaces without being evaluated against any actual standard — the same pattern-matching problem the Expert Standard exists to prevent, just applied to interfaces instead of code.

The result is frontends that converge on the same safe defaults: blue-and-white card grids, Inter or Roboto, generic layouts that look like every other AI-generated interface. They might be technically functional and even visually clean, but they haven't been evaluated against the established principles that govern whether an interface actually works for real people in real conditions.

Frontend engineering has decades of research, ISO standards, and established principles behind it. The standards exist. The question is whether they're being applied or whether the interface was pattern-matched into existence.

## The Standards That Govern Frontend Work

Before making a UI decision, identify which standard applies — the same mental move the Expert Standard demands for any engineering judgment.

### Visual Design

Visual design has established principles the same way code architecture does. An interface that ignores them isn't just ugly — it fails to communicate.

**Typography is the primary interface.** Most interfaces are mostly text. Whether the user can instantly distinguish headings from body text from labels from secondary information determines whether the interface communicates or confuses. Typography hierarchy, readability research on line height and line length, and font pairing principles all govern this — they're not aesthetic preferences, they're communication engineering.

**Color communicates before the user reads a word.** A cohesive palette with clear hierarchy — dominant colors, supporting colors, sharp accents — signals intentional design and helps users parse the interface. But color is also an engineering constraint: contrast ratios have specific measurable requirements under WCAG, and color alone can never be the only way information is conveyed.

**Spatial composition guides attention.** Whitespace is not wasted space — it creates hierarchy and focus. Alignment creates reading paths. Grouping through proximity signals relationships. These follow from Gestalt principles — how humans actually perceive visual relationships — not from design trends.

**Animation communicates state changes.** A loading spinner says "wait." A slide transition says "you moved here." A hover effect says "this is interactive." Animation that doesn't communicate is noise. And animation must respect users who experience motion sickness — `prefers-reduced-motion` exists for a reason.

**Design direction must be intentional.** The worst frontend failure isn't choosing the wrong style — it's not choosing at all and converging on the generic default. A bold maximalist dashboard and a refined minimal settings page are both correct if the direction is intentional and executed consistently. The aesthetic should follow from the interface's purpose and audience.

### Accessibility — WCAG 2.2

Accessibility is an ISO standard (ISO/IEC 40500:2025) and a legal requirement under the ADA, Section 508, and the European Accessibility Act. It governs whether everyone can use the interface — including keyboard users, screen reader users, people with motor disabilities, people with low vision, and colorblind users.

The core question: can every user perceive, operate, understand, and rely on this interface regardless of ability?

This means semantic HTML so assistive technology can parse the page. Keyboard access for every interactive element. Proper form labels that don't disappear. Focus management that doesn't trap users. Touch targets large enough to hit accurately. Content that works at 400% zoom.

These aren't aspirational goals — they have specific, measurable requirements. Read `references/wcag-checklist.md` for the concrete checks. Read `references/measurable-standards.md` for the specific numbers (contrast ratios, target sizes, timing thresholds).

### Usability — Nielsen's 10 Heuristics

These have been the industry standard for interaction design since 1994. They work because they're broad principles about how humans interact with systems, not rules tied to any specific technology.

The most commonly violated in AI-generated frontends:

**Visibility of system status.** If the system is doing something, the user needs to know. Loading states, progress indicators, success and failure feedback, save confirmation. Most generated frontends only build the happy path — the user clicks a button and... nothing visibly happens until the result appears. Or doesn't.

**Error prevention and recovery.** Preventing errors is better than reporting them (disable submit until valid, constrain input types, confirm destructive actions). When errors happen, the message must say what went wrong, why, and what to do about it — in the user's language, not the system's.

**User control and freedom.** Users make mistakes. Every flow needs escape hatches — undo, cancel, back, close, Escape key. Modals that can only be closed by clicking a specific button violate this. Multi-step flows without back buttons violate this.

**Consistency with platform conventions.** Links should look like links. Buttons should look like buttons. Navigation should be where users expect it. Custom interaction patterns require users to learn something new — don't invent them without a strong reason.

**Recognition rather than recall.** Don't force users to remember information between screens. Show recent selections, prefill known values, keep context visible.

### Performance — Core Web Vitals

Google's measurable performance standards directly affect user experience and search ranking. They govern whether the interface feels fast and stable or sluggish and janky.

The core concerns: how quickly the main content appears, how fast interactions respond, and whether content shifts around unexpectedly after loading. These have specific thresholds — see `references/measurable-standards.md`.

In practice: set explicit dimensions on images and embeds so the layout doesn't jump, lazy-load content below the fold, don't block rendering with synchronous scripts, avoid layout-triggering CSS properties in animations.

### Responsive Design

Responsive design is not "add media queries." It's designing for the actual range of conditions users encounter — screen sizes from 320px to ultrawide, touch and pointer inputs, content that's longer or shorter than the design assumed, slow connections, zoom levels up to 400%.

The test that matters: does the interface work when the content is different from the mock? When a name is 3 characters or 40? When a description is empty or three paragraphs? If the layout breaks on real content, it's not responsive — it's a picture of a layout.

## Design Decisions Report

After building or significantly modifying any frontend component, write a brief design decisions report. This is not optional — it is the mechanism that ensures the standards above were actually applied rather than silently skipped. An agent cannot write "I chose this layout because Gestalt proximity principles group related form fields" if it didn't actually reason about that. The report IS the enforcement.

The report also serves as a handoff document. When another agent modifies this component later, they get the report alongside the code and understand the intent behind each decision. Without it, the next agent pattern-matches against the existing code and potentially undoes correct decisions because they don't understand why they were made.

Keep it concise — a practical record, not a compliance document.

**Include:** Design direction and why. Layout decisions and which principles drove them. Accessibility approach and what was verified. Interaction states handled. Compromises made and why. Standards referenced by name.

**Save it** alongside the component it describes, named so the connection is obvious.

## What This Skill Is Not

This isn't perfectionism or bureaucracy. Prototypes can note "accessibility deferred" in the report and move on. The point is making tradeoffs visible and intentional, not invisible and accidental.

For a structured deep review of existing frontend code, use the `/expert-review` command.
