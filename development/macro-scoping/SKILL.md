---
name: macro-scoping
description: >
  Produces a structured macro-scoping document to align the team on what to build, why, and
  to what extent — before any technical design begins. Use this skill whenever a user mentions
  a new feature, an epic, a client request, a scope discussion, or needs to answer "what are
  we actually doing here?" — even if they don't explicitly ask for a scoping document.
  Also trigger when the user says things like "on cadre la feature", "je veux faire un cadrage",
  "on aligne l'équipe", "c'est quoi le périmètre", or "on part sur quoi exactement".
---

## Purpose

Transform a feature request or client need into a structured, one-page alignment document.
The goal is to align everyone on what is being built, why, and where the boundaries are —
before any technical design begins.

## Inputs to collect

Before producing the document, make sure you have:

- A link to the epic / client request (or a description of it)
- Business context
- Constraints (volume, compliance, regulatory)
- The CIDF ticket number (`CIDF-XXXX`) — the tracking ticket on the **CIDF board** (board de cadrage, accessible au TL, CTO et client).
  If the user did not provide it, ask: _"Quel est le ticket CIDF associé à ce cadrage ?"_
  If none exists yet, note it as "à créer" and leave a placeholder in the document.

**Deadline is NOT an input.** The macro-scoping document is one of the inputs that _produces_
a timeline estimate downstream (in the ticket breakdown / chiffrage phase). Never ask for or
mention a deadline in the scoping document itself.

### Mandatory — ask before writing

Never produce the document from the user's initial description alone. Always ask the necessary
questions first, even if the request seems complete. Use the ask_questions tool to gather:

- What are the concrete expected usages of this feature? (defines business rules priority)
- What is the triggering context? (client request, internal need, compliance, linked initiative)
- Are there known external constraints? (RGPD/DPO, third-party dependencies, regulatory)
- What decisions are already made vs. still open? (prevents writing rules that are actually unknown)

Only start writing the document once you have enough validated answers.
If a critical question remains unanswered, mark it explicitly as an open question in the
Questions ouvertes section rather than making an assumption.

## How to produce the document

Read `assets/template.md` and fill in each section methodically. Be declarative and concise.
Avoid technical implementation details — this is a business and functional alignment document.

**Section-specific guidance:**

- **Objectifs**: make them specific and measurable. Prefer "Empêcher X" over "Améliorer Y".
  Avoid vague objectives like "améliorer le système".

- **Hors périmètre**: be explicit and exhaustive. This single section prevents 80% of scope creep.
  When in doubt, add an item.

- **Règles métier**: write each rule as a testable logical condition.
  Each rule must be translatable into a code condition without ambiguity.
  For edge cases (null values, legacy data, missing fields), always define the fallback explicitly.

- **Invariants**: things that must never be violated. Being explicit here protects the whole feature.

- **Risques & Inconnues**: never hide uncertainties. Surface them explicitly — a good scoping
  document acknowledges what is unknown, not just what is known.
  Always use the table format: `Risque / Inconnu | Impact | Statut | Commentaires`.
  Statuts: 🔴 Ouvert · 🟡 En cours · 🟢 Résolu · ⚫ Accepté.
  At macro-scoping stage, most items will be 🔴 Ouvert — that is expected and correct.

- **Questions ouvertes**: this is a **living working section**, not a permanent one.
  It captures what is still unresolved during the scoping process.
  A question is resolved when it migrates to either:
  - A business rule (if it was a functional decision), or
  - The Risques & Inconnues table with status 🟢 Résolu or ⚫ Accepté.
    The section must be **empty when the macro-scoping is closed**.
    If questions remain open at the start of technical scoping, flag them explicitly as blocking or non-blocking.

## Output format

Produce the document in French using `assets/template.md`. Keep it to one page maximum.

## Golden rules

- **Always ask questions before writing.** Never produce the document from the initial description alone.
- No detailed technical design.
- No DB schemas.
- No code.
- No ticket breakdown.
- No deadline — it is an output of chiffrage, not an input to scoping.
- A good macro-scoping document lets anyone explain the feature in 3 minutes, list all business
  rules, and identify external dependencies — without needing to read anything else.

## What a good macro-scoping is NOT

- Not a Jira ticket.
- Not a detailed technical spec.
- Not code.
- Not a disguised implementation.
