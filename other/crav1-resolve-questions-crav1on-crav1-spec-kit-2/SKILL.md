---
name: crav1-resolve-questions
description: Walk Open questions in spec.md one by one. Each question gets keep-open or answer options with impact; patch only that question after a pick. Use after /crav1-tighten-spec when unanswered questions remain. Do not write application code.
disable-model-invocation: true
icon: book-open
color: yellow
---

# Resolve questions

You close **Open questions** (and leftover numbered **Assumptions**) one at a time. Same pacing as `/crav1-tighten-spec`: one `Q#`, options with impact, wait, then patch only that item.

This is not a defect walk. Do not re-run architecture findings here unless they are already written as open questions.

**Do not patch until the user picks a letter for the current question** (or a batch of `Q#: letter` answers).

## Find the spec

Use the spec the user @-mentions. Otherwise the most recently edited file under `docs/specs/` excluding `_template/`. If several, ask which slug. Expected `spec.md` headings: this skill’s `assets/spec.md`.

Read `spec.md` (`## Open questions`, `## Assumptions`, `## Constraints`). Note `diagrams.md` and `adr/`.

## Build the question list (no edits)

Number `Q1`, `Q2`, … in document order.

Include:

1. Every bullet (or numbered item) under **Open questions**
2. Assumptions still marked unresolved (A1, A2, …) if they are not already duplicated as an open question

Skip empty placeholders. Do not invent new questions. If the list is empty, say so and point to Plan Mode (`Shift+Tab`) with `spec.md` attached — not to this skill.

## Walk one question at a time

### Index (every turn, short)

Remaining `Q#` titles only. Mark the current one.

### Current question (full)

For **only** the current `Q#`:

1. **Question** — quote the spec line. One sentence on what is undecided (product vs architecture).
2. **Why it is still open** — what v0, tests, or an ADR cannot finish without this.
3. **Options** — usually 3–5 letters. Use the questions tool when available.

**Always** include **Keep open**. Always include at least two **substantive** answers (not only keep vs cut) unless the only honest answers are keep vs cut-from-v0.

Every option: **letter**, **name**, **what it means**, **impact** (v0/demo/tests, and which files/sections). Use the catalog below. Tailor the answer letters to *this* question (e.g. “self-register” vs “admin-provisions”) — do not offer generic “apply notes.”

4. How to answer: `A` / `B` / … or prose (“Q2: passwords min 12 chars, no recovery in v0”). Batch: `Q1 A, Q2 keep, Q4 C`.

Stop. Do not edit. Do not preview a full patched spec.

### After a choice

1. Patch **only** this question.
   - **Keep open:** leave the bullet. You may sharpen the wording if they asked; do not resolve it.
   - **Answer:** fold the decision into the right place (requirement/journey/acceptance, `## Constraints`, non-goals/later, or a new/updated ADR). **Remove** it from Open questions (or mark the assumption resolved).
   - **Cut from v0:** move to non-goals/later; remove from Open questions.
2. Recap **Added / Removed / Still open** for this `Q#`.
3. If the answer makes a named diagram/ADR wrong, either they also chose `sync-here`, or the **next** item is that drift (do not silently skip).
4. Advance to the next unanswered `Q#`. If none remain, say the open-question list is empty and they can Plan Mode or `/crav1-architecture-reviewer` / `/crav1-tighten-spec` if new gaps appeared.

Do not start the next question’s patch in the same turn unless they batched.

## Resolution catalog (per question)

| Id | Name | What it does | Typical impact |
| --- | --- | --- | --- |
| `keep-open` | Keep open | Leave this question unanswered. No product decision. | Still blocks a fully closed spec. Disk: none, unless they asked to rephrase. **Always offer this.** |
| `answer-A` … | Answer: \<concrete choice\> | Commit one of the real alternatives you listed. | `spec.md` gains a SHALL, constraint, or non-goal; this `Q#` leaves the open list. |
| `answer-custom` | Answer in my words | Use their prose as the decision. Put it in the correct section; do not dump the paragraph into Open questions. | Same as a concrete answer. Offer when choices might not fit. |
| `cut-from-v0` | Cut from v0 | Not deciding how — deciding **not in v0**. | Smaller demo; question removed; lives under non-goals/later. |
| `to-constraint` | Record as constraint | The answer is an accepted tech/limit, not a user journey. | `## Constraints`; not a REQ SHALL about libraries/tables. |
| `to-adr` | Decide via ADR | Real alternatives remain worth recording. Write/update `adr/NNNN`, status `proposed` or `accepted` as they said. | Requirements stay behavioral; question removed once the ADR captures the choice (or stays open if they only drafted the ADR as proposed **and** asked to keep the question — rare; default is remove). |
| `ask` | Narrow first | Ask at most 3 multiple-choice questions **about this Q#**. No file edits. | Retry this `Q#` next turn. Use when your answer options would be a guess. |
| `sync-here` | Sync this artifact | Update the diagram/ADR this answer invalidates. | Only with an answer, not with keep-open. |

Do **not** offer a turn-level “answer all with assumptions.” Guessing is `ask` or `keep-open`.

## Hard rules

- Prefer **cutting scope** over adding features.
- Keep-open is a valid finish for a question. Do not nag them into answering.
- Do not expand v0 to “solve” a question.
- Architecture answers go to Constraints or ADRs, not journeys.
- Do not write application code. Do not start Plan Mode until they are done or they ask.
- Do not patch “to be helpful” when they have not chosen.

## When the list is done

- Remaining items are only those they **kept open**, or the list is empty.
- Tell them: kept-open items stay as the spec’s honest unknowns; empty list → `/crav1-plan-from-spec` or a new chat in Plan Mode with `spec.md` attached.
- Optional next: `/crav1-export-spec` if exports exist, or `/crav1-architecture-reviewer` if answers changed the shape.
