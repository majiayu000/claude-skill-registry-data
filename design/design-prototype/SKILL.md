---
name: design-prototype
description: Use before building or changing any screen (a new page, dialog, panel, or a visual rework), to design it first as a prototype in the project's own design language, which the skill extracts from the codebase and writes down once. Not for implementing the screen and not for reviewing its code.
---

# Design a prototype

**Learn the project's design language, propose prototypes in that language, iterate live, hand off to implementation.**

<HARD-GATE>
No component code, no route, no CSS in the app for the screen being designed until a prototype exists, has been rendered in aiview, and the user has approved it. A tiny change gets a tiny prototype (a cropped HTML fragment of the affected region), but it exists and it is approved.
</HARD-GATE>

## Mindset

**Every choice, palette, type, layout, wording, is specific to this product and the people who use it**, never the default any app would get.

- **Native when a language exists.** The product's own tokens, primitives and words; a prototype inherits distinctiveness and does not reopen it.
- **Grounded in the subject.** Who uses the screen, what it is for, what those people already read every day.
- **Pattern-match before inventing.** A sibling screen that solves the same problem gives the shape; deviate only with a stated reason.
- **Density and hierarchy over decoration.** The summary before the detail, state encoded in form (a chip, an opacity, a stripe) and not only in text, semantic colour apart from the accent.
- **Spend boldness in one place.** One element is the memorable thing, the rest quiet. Before calling a prototype done, remove one thing.
- **The quality floor is built in, never announced.** Responsive to the mobile preset, visible keyboard focus, `prefers-reduced-motion` respected, contrast legible in both themes, touch targets no smaller than the codebase's own buttons.
- **Copy is design content.** Written from the person's side: things named by what people control and recognise (a person manages *reviewers*, not *review_assignment rows*), a control saying exactly what happens, the same name through the whole flow, empty states inviting the next action, errors saying what went wrong and how to fix it, no apology. Sentence case, plain verbs, the product's language.
- **The prototype describes the look, never the framework.** No Tailwind classes or React structure prescribed; the handoff maps to named components.

## Flow

1. **Load or build the design language.** If `design-language.reference.md` exists and is younger than the last change to the token and UI files, read it. Otherwise extract it now as `references/extract.md` says, into the shape of `references/design-language-template.md`, write it, register it, and ask the user in one message: "does this match how you see the product?". No codebase, or a codebase with no language of its own yet (a scaffold, a template, defaults never chosen): `references/greenfield.md`.
2. **Frame the screen**: one question at a time, only what changes the layout: who uses it, the primary action, the data it shows, the states it must handle, where it sits in navigation. Reuse names from `nomenclature`/`AGENTS.md`; never invent product vocabulary.
3. **Plan before the HTML**: the sibling screen it pattern-matches, the layout in one sentence with an ASCII wireframe, its components, the one thing the screen must make obvious. What could have come from any app, or brings a token or pattern the codebase lacks, is revised and the change said. An open layout question is asked on the wireframe. One direction by default; two or three, small and side by side, when asked or when the screen has no sibling.
4. **Render and iterate**: write the file, register and serve it, tell the user the URL, edit the same file as they react. Hand it over as something to change. **A prototype works, it is not a picture**: the behaviour is mocked in the file so the flow can be walked through. Once the visual pass is approved, ask about the flow and mock it. A question about a region of a prototype already rendered is asked through the `point-at` skill. Check every variant and the three viewport presets before calling it done.
5. **Handoff**: an implementation note at the bottom of the prototype file (HTML comment): which existing components each region maps to, which new named components are needed and where they live, copy strings, and the acceptance list (variants times viewports). Then stop; implementation is a separate step the user starts.

## The design language

**`design-language.reference.md` outlives every PR.** It lives in the project's folder in the data home, kind `reference`, tags = design. When the token or UI files have moved on, extract again rather than patch.

## Prototypes

- **File `YYYY-MM-DD-<screen>.prototype.html`** in the data home, at the path the `aiview` skill gives. One screen per file; its variants (states, steps, alternatives) live inside the file, never as sibling files.
- **Self-contained**: inline `<style>` and, if needed, inline `<script>`; no CDN, no build. The `<style>` opens with the design-language tokens as `:root` custom properties (light) plus the dark overrides under `@media (prefers-color-scheme: dark)`, and uses only those tokens. A new token is flagged in the handoff note as "new token: needs a name in the theme".
- **Native look**: every region is recognisably one of the project's components, annotated `data-component="Pill"` so the handoff maps one to one. Real copy in the product's voice, never lorem. Real-looking data.
- **Shared between prototypes**: a component drawn once is bound by every other prototype that needs it, and a screen's variants are declared as buttons the viewer mirrors. How to declare, bind, keep a component bindable, and when to split a screen: `references/binding.md`. The first prototype of a project needs none of it.
- **Register and serve via the `aiview` skill**: kind `prototype` (from the filename), tags = feature, and the group of the piece of work it belongs to. Tell the user the URL it prints.

## Red flags

| Thought | Reality |
|---|---|
| "I know this codebase's style" | Styles drift; re-read the token file and one screen. Cite them. |
| "The user said 'make it pretty'" | Ask what job the screen does; prettiness follows from hierarchy in the existing language. |
| "A cream background and a serif display would look distinctive" | Distinctive-for-the-web is wrong here: the target is native to this product. With no language yet, that look is the first tell in `references/greenfield.md`. |
