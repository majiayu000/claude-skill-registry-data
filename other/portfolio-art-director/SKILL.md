---
name: portfolio-art-director
description: Turn a person's real work into a portfolio with a point of view - what to lead with, how to present each project, and which few components carry the personality - using components from tryvitrine.dev. Use when building or redesigning a personal, studio or case-study site.
---

# /portfolio-art-director

A portfolio is read by someone deciding whether to trust you with work. Lead with the work, show judgement, and make contact effortless. The personality comes from one or two signature details, not from everything moving.

## 1. Gather the facts

Collect these before designing anything:

- Name, role and city.
- 3–6 projects with year, your role, the problem, what you did and the outcome (a number if there is one).
- Who the reader is (a recruiter, a client, a collaborator) and what you want them to do (email, book, read the CV).

No placeholders: if a fact is missing, ask.

## 2. Choose a register

Pick one: **editorial** (serif, calm, text-led), **visual** (image-led, big type, a living backdrop) or **technical** (mono details, systems, numbers). The register decides every later choice.

## 3. The page, in order

1. **Name and intro:** `masthead-nav` folding into a bar. Inline links inside the intro use `draw-link`. A signed name (`flourish-name`, `seal-signature`) only if it fits the register.
2. **Selected work:** a list to read (`highlighter-row`) or objects to look at (`specimen-card`, `folio-card`, `approach-card`). Each project gets year, role and outcome.
3. **One case in depth:** before and after, decisions, constraints. Depth beats twelve thumbnails.
4. **Experience:** `meander-timeline`, dated and expandable.
5. **Contact:** `sign-off-footer` with the email to copy, local time and availability.

## 4. Signature, sparingly

Choose **one** of: a background behind the name (`silk-field`, `dune-field`, `star-trails`), a typographic moment (`chapter-numeral`, `end-credits`, `constellation-name`) or a cursor (`glow-pointer`, `nib-trail`), scoped to one section. Everything else stays still and fast.

## 5. Check

- Every project has a year, a role and a real outcome.
- Contact is reachable in one click from every screen.
- Run `/accessibility-pass` and `/responsive-audit`. The 375px view should still lead with the work.

## Output

The register, the section plan with components and reasons, the chosen signature detail, and the copy gaps still to fill.
