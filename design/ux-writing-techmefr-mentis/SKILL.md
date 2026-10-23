---
name: ux-writing
description: "Use when writing any text a user reads in the product: labels, buttons, errors, empty states, confirmations, emails. Complements skills/accessibility and the i18n conventions."
---

# ux-writing

Business layer (`business/README.md`), applied at step 6 of the dev pipeline. Interface text gets
written in the last ten minutes by a developer with a component to finish, and then it's what every
user reads for the next three years.

This block isn't about tone of voice, which belongs to whoever owns the brand. It's about the specific
places where wording causes a support ticket, a wrong click, or a user stuck with no route forward.

**Boundary with an org design catalogue.** Where one exists, its UX-writing skill covers the same subject
**at design time**, inside a mockup, and carries the organisation's own rules — form of address, one word
per action, explicit button labels. Where that plugin is installed, **it is the authority on the wording
rules and this block defers to it**; what remains here is the code-time pass, on text that reaches a diff
without ever passing through a mockup: validation messages, error states, transactional emails,
concatenated strings. A dedup audit on 2026-08-06 confirmed the overlap is real; this is the resolution,
and the two must not diverge on a shared rule.

**An applied override is recorded, not hidden.** Write what the governing wording rules require, and leave one
short neutral trace addressed to whoever can decide (a line in the PR description, the task summary or an
ADR): which rule was overridden, by what, and that it is a resolved case. Never phrase it as "a conflict
between mentis and the house rules" to a non-technical stakeholder — that framing reads as broken even when
the case is a normal, resolved one, and has already caused a real project to get abandoned and restarted over
nothing. Raise one specific, named question to the decider only when no rule anywhere actually resolves the
case.

## When
As soon as a diff adds or changes text a user sees: a field label, a button, a validation message, an
error, an empty state, a confirmation dialog, a notification, a transactional email.

## Steps

**Read only the sections the string actually touches.** The rules live one file per section under
`references/`; a failure path is §1, a control or a label is §2, an empty list is §3, and §4 and §5
apply to every string in a product that already has strings.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Errors: what happened, and what to do now | writing anything on a failure or validation path | [`01-errors.md`](./references/01-errors.md) |
| 2 | Labels and buttons: describe the outcome | a button, link, field label, menu entry or confirmation | [`02-labels-buttons.md`](./references/02-labels-buttons.md) |
| 3 | Empty states | a list, table, search or dashboard region can come back with nothing | [`03-empty-states.md`](./references/03-empty-states.md) |
| 4 | One product, one voice | writing a string in a product that already has strings | [`04-one-voice.md`](./references/04-one-voice.md) |
| 5 | Mechanics that keep it consistent | adding a string to a translation file, or assembling one from parts | [`05-mechanics.md`](./references/05-mechanics.md) |
| 6 | Links, instructions, plain language, inclusive wording, culture | a link is added, an instruction points at the screen, or text for a wide or multilingual audience is written | [`06-links-and-inclusive-wording.md`](./references/06-links-and-inclusive-wording.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: every new user-facing string has a next action
where it's an error, a consequence where it's destructive, and a term consistent with the rest of the
product. Where the wording carries brand or legal weight, it goes to whoever owns that.

## Guardrails
- **Never ship a placeholder** (§5.12). "Lorem ipsum", "TODO", "test" and a bare "Error" all reach
  production eventually.
- **Never invent a legal or commercial commitment in interface text** — a guarantee, a deadline, a
  price, a promise about data (§2.10). That's someone else's decision to make.
- **Never leave an error with no next action** (§1.2), and never leak internals in one (§1.5).
- **Never build a sentence by concatenating fragments** (§5.3), and never put markup in a translated
  string (§5.8).
- **Never show an empty state where a request failed** (§3.3).
- **Never write a link as "click here" or "read more" alone** (§6.1), and **never point at the screen by
  colour or position alone** (§6.7).
- Never let humour into an error path: the person reading it is already having a problem (§1.11).
- This block doesn't own tone of voice or brand vocabulary. Where it conflicts with them, they win.

## Origin
Assembled from public sources: established interface-writing guidance as published in the major design
systems' content guidelines, written without internal UX-writing expertise. The full provenance and the
refresh log are in [`references/origin.md`](./references/origin.md).
