---
name: domain
description: "Sharpen domain terms and record decisions in CONTEXT.md and ADRs."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills domain-modeling (Codex copy, + CONTEXT-FORMAT.md, ADR-FORMAT.md), ubiquitous-language"
---

# Domain

Keep the project's language sharp: one name per concept in `CONTEXT.md`, and the decisions a future reader would trip over in ADRs. A shared glossary is what lets the user, the code and the next agent mean the same thing by "Order".

Pick the branch from the argument:
- `domain` alone: **sweep** this conversation and the code for terms (sections 1-2).
- `domain <term>`: **sharpen** that term (sections 1-2).
- `domain adr <decision>`: **record** a decision (section 3).

Other skills (`grill`, `architecture`) send their terms and decisions here; the formats below are the single source.

## 0. Find the files

- `CONTEXT-MAP.md` at the root: several contexts. Read it and work in the context the topic belongs to; ask when that's unclear.
- Only a root `CONTEXT.md`: one context.
- Neither: create root `CONTEXT.md` when the first term resolves, and `docs/adr/` with the first ADR. No empty scaffolding.

Formats and an example live in `references/formats.md`.

Done when: you know which `CONTEXT.md` and which `docs/adr/` this topic belongs to.

## 1. Sharpen the terms

Sweep: list the domain nouns and verbs in the conversation and the code, then flag three problems: one word used for different concepts, different words for one concept, and vague or overloaded words.

Then work each term in play:
- **Challenge against the glossary.** "`CONTEXT.md` defines cancellation as voiding the whole Order; you seem to mean cancelling one line. Which is it?"
- **Propose a precise term for a fuzzy one.** "By 'account' do you mean the Customer or the User? Those are different things."
- **Stress-test with an invented scenario** that forces a boundary: "An Order ships in two Shipments and one is cancelled before dispatch. How many Invoices exist?"
- **Cross-check the code.** When the user says how something works, read the code. Surface a contradiction with `path:line`: "`orders/cancel.ts:30` cancels whole Orders, but you said partial cancellation is possible. Which is right?"
- **Be opinionated.** Pick the best word for each concept and list the rest as aliases to avoid.

Done when: every term in play has one name and one definition the user accepted.

## 2. Write CONTEXT.md

Update it the moment a term resolves, not in a batch at the end.
- **Domain terms only**: words a domain expert would use. Generic programming concepts (timeout, retry, endpoint) and class names without domain meaning stay out.
- **No implementation details.** It is a glossary, not a spec, a plan or a scratch pad.
- **Tight definitions**: one or two sentences saying what the thing is, not what it does.
- **`_Avoid_:` line** for the rejected aliases.
- **Relationships** in bold terms with cardinality where it's clear: "An **Order** produces one or more **Invoices**."
- **Subheadings** when natural clusters emerge; a flat list when they don't.
- **Flagged ambiguities**: a short section for resolved confusions, so nobody reintroduces them.

If code still uses an old name for a renamed term, list those identifiers as a follow-up; renaming code is a refactor for the `architecture` skill.

Done when: the file is updated and a re-read finds no implementation detail in it.

## 3. Record an ADR

Offer one only when all three hold:
1. **Hard to reverse**: changing your mind later costs something real.
2. **Surprising without context**: a future reader would ask "why on earth did they do it this way?"
3. **A real trade-off**: there were genuine alternatives, and this one won for specific reasons.

If any is missing, skip it and say which in one line. Typical qualifiers: architectural shape, how contexts integrate, technology with lock-in, ownership and scope lines (the explicit no's too), deliberate deviations from the obvious path, constraints invisible in the code, rejected alternatives someone will propose again.

Write `docs/adr/NNNN-<slug>.md`, numbered one past the highest existing. A single paragraph is a complete ADR: context, decision, why. Add `Status`, `Considered options` or `Consequences` only when they carry information. When a decision is replaced, write a new ADR and mark the old one `Status: superseded by ADR-NNNN`; leave its text as history.

Done when: the ADR is saved with the next number, and any ADR it replaces is marked superseded.

## 4. Report

List the terms added or changed, the ambiguities still open, and each ADR written or declined with the reason.
