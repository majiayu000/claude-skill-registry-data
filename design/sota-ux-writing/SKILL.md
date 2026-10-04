---
name: sota-ux-writing
description: >-
  State-of-the-art UX writing and product-copy guidance (2026) covering voice
  and tone systems, plain language (ISO 24495-1), microcopy (buttons, labels,
  empty states, onboarding, notifications), error and feedback message craft,
  and the accessibility and localization of interface language (WCAG 2.2
  language criteria, alt text, ICU pluralization, i18n-safe strings). Use when
  writing or reviewing ANY user-facing interface text — web, mobile, desktop,
  or CLI products — AND when auditing existing product copy for clarity,
  consistency, tone, accessibility, and localization readiness. Trigger
  keywords: UX writing, microcopy, product copy, content design, error message,
  empty state, button label, tooltip, onboarding copy, form label, placeholder,
  notification, toast, confirmation dialog, tone of voice, terminology, plain
  language, readability, alt text, i18n strings, localization, translation.
---

# SOTA UX Writing & Product Copy

## Purpose

Expert-level rules for the *words inside the product*: labels, buttons, errors,
empty states, onboarding, notifications, and every other string a user reads
while trying to get something done. The core thesis: **interface text is
functional infrastructure, not decoration — a user reads it under task
pressure, often in a second language, often through a screen reader, and every
word either moves them forward or costs them a support ticket.**

Boundaries: this skill owns the *language*. The UX *patterns* the language
lives in (when to show an empty state, validation timing, dialog escalation)
are `sota-frontend-design` rules/04; technical documentation is
`sota-docs-workflow`; outward-facing marketing content is `sota-copywriting`;
CLI-specific output contracts are `sota-cli-ux`.

## BUILD mode

When writing or changing interface text:

1. **Write the unhappy paths first** — errors, empty states, and confirmations
   carry more consequence than the happy path (`rules/03`).
2. **Apply the plain-language spine** to every string: relevant, findable,
   understandable, usable (ISO 24495-1) — front-load the point, one idea
   per sentence, common words (`rules/01`).
3. **Name things once.** Check the product glossary before introducing a term;
   never let the UI, docs, and API call the same concept different names
   (`rules/01` §4).
4. **Buttons are verbs with objects** ("Delete project", never "OK"/"Yes"),
   and every dialog states the specific consequence (`rules/02`).
5. **Write for the translator and the screen reader as you go**: externalized
   strings, ICU plurals, named placeholders, descriptive link text, accessible
   names matching visible labels (`rules/04`).
6. Before finishing, run each loaded rules file's **Audit checklist** against
   the diff — including the greps for banned strings.

## AUDIT mode

When reviewing existing product copy:

1. Inventory the string surface: localization files (`*.json`, `*.po`,
   `*.strings`, `*.xlf`), hardcoded literals in components, error-message
   constants, email/notification templates.
2. Run the banned-pattern greps from each rules file's audit checklist
   (e.g. `"click here"`, `"an error occurred"`, `"invalid input"`,
   concatenated plurals).
3. Walk the critical flows as a user: signup, first-run empty state, a failed
   payment/submit, a destructive action. Judge every string against
   `rules/01`–`03`.
4. Check localization readiness (`rules/04`) even for single-language
   products — retrofitting string externalization is expensive.

### Severity conventions

- **Critical** — copy that causes data loss or deception: destructive-action
  dialog whose buttons don't name the action; error message leaking secrets,
  internals, or account existence; consent text that misrepresents what
  happens; dark-pattern confirmshaming.
- **High** — copy that blocks task completion or excludes users: error with no
  next step; placeholder used as the only label; icon-only control with no
  accessible name; untranslatable concatenated strings; link text meaningless
  out of context ("click here").
- **Medium** — friction and inconsistency: same concept under two names;
  jargon or internal codenames in UI; blame-framed errors; toasts carrying the
  only path to an action; missing empty-state guidance.
- **Low** — polish: tone drift, capitalization inconsistency, "please"
  inflation, exclamation marks, filler words ("simply", "just").

### Finding format

`file:line | rule violated | severity | effort | fix` — quote the current
string and propose the exact replacement string; copy findings without a
proposed rewrite are half-findings.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-voice-tone-plain-language.md` | Establishing or auditing the overall language system: voice vs tone, stress-aware tone shifts, plain-language rules (ISO 24495-1), readability, terminology/glossary discipline, capitalization and punctuation conventions. |
| `rules/02-microcopy-components.md` | Writing the words in components: buttons/CTAs, labels vs placeholders vs hints, empty states, onboarding and tooltips, confirmation dialogs, notifications/toasts/badges, counts and plurals, relative time, link text, loading/progress text. |
| `rules/03-errors-feedback.md` | Anything that reports a problem or outcome: error-message anatomy, no-blame framing, validation wording, security-sensitive errors, warnings vs errors, success confirmations, permission prompts, and dark-pattern-free upsell moments. |
| `rules/04-accessibility-localization.md` | Making the language reach everyone: WCAG 2.2 language criteria, alt text craft, accessible names, screen-reader-facing strings, string externalization, ICU plurals, translator context, text expansion, RTL, inclusive language. |

## Top-10 non-negotiables

1. **Every error says what happened and what to do next** — a dead-end error
   is a support ticket with extra steps. (rules/03 §1)
2. **Buttons and dialog actions are verb+object** ("Delete project",
   "Keep editing") — never bare "OK/Yes/No" pairs on anything consequential.
   (rules/02 §1, §5)
3. **The system takes the blame**: "We couldn't save your changes", never
   "You entered invalid data". (rules/03 §2)
4. **One concept, one name**, everywhere — UI, docs, API, support. Maintain a
   glossary; renames are migrations, not edits. (rules/01 §4)
5. **Placeholders are never labels**; hint text never disappears while the
   user still needs it. (rules/02 §2)
6. **No copy relies on color, position, or an icon alone** to carry meaning;
   every control has an accessible name matching its visible label.
   (rules/04 §2)
7. **Link and button text stands alone**: "View invoice #1042", never
   "click here" or a bare "Learn more". (rules/02 §8)
8. **No string concatenation, ever** — ICU MessageFormat with named
   placeholders and real plural rules; "1 items" ships nowhere. (rules/04 §4)
9. **Front-load every string**: the first three words carry the point;
   scanning users read little else. (rules/01 §2)
10. **Security-sensitive copy never leaks**: auth errors don't confirm account
    existence, error surfaces never show stack traces, internals, or secrets
    — cross-check `sota-code-security` rules/02 and /07. (rules/03 §4)
