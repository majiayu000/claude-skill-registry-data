---
name: aigent-business-sites
description: Business-website layer for aigent-design. Use when the work is a marketing site, landing page, service or local business site, ecommerce surface, editorial or membership site, portfolio, or nonprofit site and the job needs content architecture, truthful proof, preserve-mode redesign, or a release audit, not just visual direction.
---

# Aigent Business Sites

This skill adds the business side of a website to `aigent-design`. `aigent-design` still owns authority, direction, the Variance / Motion / Density controls, Taste, Resolve, and Vision. This skill owns what the page has to say, what it is allowed to claim, what a redesign must not break, and when a site is actually ready to ship.

Most of it is ported from [Ultra Web Design](https://github.com/wrg32786/Ultra-web-design). See [`NOTICE.md`](NOTICE.md).

## When to use it

Use it alongside `aigent-design` when the surface has a business job: leads, trials, purchases, bookings, subscriptions, donations, or trust. Skip it for product UI, dashboards, decks, and pure visual experiments.

Keep the path small. A one-line copy or state fix does not need a content matrix.

| Task | Path | Read |
| --- | --- | --- |
| tiny copy, style, or state fix | read, fix, render | nothing extra |
| new section or route in an established brand | read, surface brief, build, render | `reference/business-content.md` |
| preserve-mode redesign | read, preservation inventory, modernize, render | `reference/preserve-redesign.md` |
| full redesign or greenfield site | full `aigent-design` loop plus this skill | all three references |
| audit only, no edits | read, audit, report | `reference/release-audit.md` |

## Always on

### Truth

- Never invent testimonials, metrics, ratings, customers, logos, awards, prices, certifications, capabilities, affiliations, or legal claims.
- Label every uncertain input as `SUPPLIED`, `ASSUMED`, `ILLUSTRATIVE`, `MISSING`, or `PROHIBITED`. Do not quietly promote an assumption to production copy.
- Use the strongest real proof available and never fake a higher rung. The proof ladder is in `reference/business-content.md`.
- Never make a control look functional when it is not. Fake product UI built from empty divs counts.

### Business continuity

In any redesign, inventory routes, redirects, nav labels, forms and field names, analytics events, SEO metadata, proof, legal copy, brand marks, and existing accessibility wins before changing anything. This extends the `TARGET` / `PRESERVE` contract in `aigent-design`. Details in `reference/preserve-redesign.md`.

### Page structure

- One primary business objective and one primary CTA per surface. A secondary CTA is fine when it serves a different readiness level.
- Organize content around visitor questions, not a default Hero, Features, Pricing, FAQ, CTA stack.
- Important claims follow claim, mechanism, proof, implication.
- CTA labels name the next step. Avoid `Learn more` when a better verb exists.

### Anti-generic

- Run the interchangeability test: swap in an unrelated company from the same category. If the page still works, the concept is too generic.
- The page needs at least one detail that only someone who understands the product would add (the soul test).
- Generic-pattern findings must name the harm (repetition, meaninglessness, mismatch, a real defect). "Looks AI-generated" is a symptom, not a finding.
- Do not ban a font, punctuation mark, icon set, or palette just because some skill said so. Fail it when it is unearned, repeated, misleading, or indistinguishable from the category default.

## Working templates

Copy into the target project only what the work needs, then delete unused fields. These are scratch files, not ceremony.

- [`templates/SURFACE-BRIEF.md`](templates/SURFACE-BRIEF.md) one route: job, visitor state, first viewport, proof, states, analytics
- [`templates/CONTENT-MATRIX.md`](templates/CONTENT-MATRIX.md) every section mapped to a visitor question, proof, and truth status
- [`templates/PRESERVATION-INVENTORY.md`](templates/PRESERVATION-INVENTORY.md) what a redesign keeps, evolves, or replaces
- [`templates/QA-REPORT.md`](templates/QA-REPORT.md) design jury, technical audit, findings, context matrix

Visual direction, tokens, and `DESIGN.md` stay with `aigent-design` and `.aigent/design-direction.md`. Do not create a second design contract.

## How it plugs into the aigent loop

1. **Shape** (`aigent-design/reference/shape.md`): add the business objective, visitor awareness state, objections, and proof inventory from `reference/business-content.md`.
2. **Direction**: pick a page grammar and hero form that fit the business type. Do a quick category-rut list before directions so they avoid the default.
3. **Build**: real content or labeled placeholders only.
4. **Taste, Resolve, Vision**: run them as usual. They are the mechanical and visual floor.
5. **Release**: then run the business release checks in `reference/release-audit.md`. Report what was observed and what was not checked.

Never claim a check ran when it did not.

## Evals

[`evals/`](evals/) has six output cases and twenty trigger queries (ten should fire, ten near misses). See [`evals/README.md`](evals/README.md).
