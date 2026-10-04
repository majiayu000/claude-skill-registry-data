---
name: nfc
description: >
  Use this skill whenever the user wants output shaped for clarity, directness, and low
  cognitive load. Triggers include: "NFC", "[NFC: strict]", "plain language", "plain English",
  "simplified technical english", "STE", "clarity filter", "strict mode", "make this
  unambiguous", "no metaphors", "write this literally", "reduce cognitive load", or any
  request to rewrite text so it is easier to process. Also use it when the user states they
  are neurodivergent, autistic, or ADHD and asks for clearer communication, and when a task
  produces instructions, procedures, or safety-critical steps where ambiguity is expensive.
---

# Neuro-Attuned Communication Filter (NFC)

Constrains generated text so it is literal, predictable, and easy to process. NFC applies the
mechanical writing rules of ASD-STE100 (Simplified Technical English) to ordinary output.

NFC is a filter on the final answer. It changes how the answer is written. It does not change
what the answer says, and it does not change how much research or reasoning goes into it.

---

## Activation

| Form | Example | Effect |
|---|---|---|
| Explicit tag | `[NFC: strict]` | Applies that mode to the current reply |
| Named mode | "use NFC strict" | Applies that mode to the current reply |
| Persistent | "stay in NFC clear" | Applies that mode to every reply until the user cancels |
| Bare | "use NFC" | Applies `standard` |
| Cancel | "stop NFC", "normal mode" | Returns to unfiltered output |

Default mode when NFC is active but no mode is named: **`standard`**.

If the user names a mode that does not exist, use the closest match and state which mode you
applied in one line, before the output.

---

## Modes

Modes increase in strictness: `standard` → `clear` → `strict`. Each mode inherits every
constraint of the mode before it.

### `standard` — baseline clarity (default)

Removes vagueness and inflated language while keeping a natural voice. Use for general
explanations and conversation.

### `clear` — contextual clarity

Adds structure, controlled sentence length, and defined terms. Keeps enough connective language
to explain reasoning. Use for recommendations, comparisons, and teaching material.

### `strict` — maximum fidelity

Applies the ASD-STE100 mechanical rules in full. Output is literal and instantly actionable.
Use for instructions, procedures, configuration steps, and safety-critical or
decision-critical content.

---

## Rule table

Apply every rule for the active mode. These are countable, so check them.

| Constraint | `standard` | `clear` | `strict` |
|---|---|---|---|
| Words per sentence | ≤ 30 | ≤ 25 | ≤ 20 procedural, ≤ 25 descriptive |
| Sentences per paragraph | ≤ 8 | ≤ 6 | ≤ 6 |
| Instructions per sentence | any | 1 preferred | exactly 1 |
| Topics per paragraph | 1 preferred | 1 | 1 |
| Voice | active preferred | active; passive only if the actor is unknown | active only; passive only in descriptions where the actor is unknown |
| Verb forms | any | simple present, past, future | infinitive, imperative, simple present, simple past, simple future, past participle as adjective only |
| Present perfect | allowed | avoid | prohibited — use simple past |
| `-ing` forms | allowed | only as a noun | only as a technical noun, or inside one |
| Words per noun cluster | ≤ 4 | ≤ 3 | ≤ 3 |
| Articles (`the`, `a`) | normal | required | required, never dropped |
| Omitted subject or verb | allowed | avoid | prohibited |
| Idioms and metaphors | use sparingly | explain on use | prohibited |
| Jargon | define on first use | define on first use | define on first use, or replace it |
| Hedging ("might", "perhaps") | allowed | only when the uncertainty is real | only when the uncertainty is real, and state the cause |
| Emoji | allowed | sparingly | prohibited |
| Lists | as useful | for any 3+ items | required for any sequence of steps |

Word substitutions and the full rule set: `references/style-rules.md`.

---

## Output syntax

Higher modes constrain layout, not just wording.

### `standard`

Prose with headings where the topic changes. No fixed template.

### `clear`

```
<Heading>

<Lead sentence stating the conclusion.>

- <Point>
- <Point>

<Closing sentence stating what to do next, if there is an action.>
```

State the conclusion first, then the support. Do not build up to the answer.

### `strict`

```
Topic: <noun phrase>

Definitions:                          (include only if a technical term appears)
- <Term>: <one-sentence definition>

Steps:                                (include only if the reader must do something)
1. <Imperative verb> <object>.
2. <Imperative verb> <object>.

Facts:                                (include only if the reader must know something)
- <One statement per line.>

Result: <What the reader will observe when the steps are complete.>

Warning: <Condition that causes damage, data loss, or injury.>
```

Rules for `strict` layout:

- Omit any section that has no content. Do not write "None" or "N/A".
- Start every step with an imperative verb.
- Put a warning **before** the step it applies to, not after.
- One fact per line. Do not join facts with "and" or ";".

---

## Self-check

Run this against your draft before you send it. Do not describe the check in the output.

**Every mode:**

1. Did I remove every metaphor, idiom, and figure of speech the mode prohibits?
2. Is every technical term defined on first use, or replaced?
3. Does any sentence exceed the word limit? Count the longest one.
4. Did I state the conclusion before the reasoning?

**`clear` and `strict` also:**

5. Does any paragraph exceed 6 sentences?
6. Is any sentence passive where the actor is known? Rewrite it as active.
7. Does any noun cluster exceed 3 words?

**`strict` also:**

8. Does every step start with an imperative verb?
9. Does any sentence contain more than one instruction? Split it.
10. Did I use the present perfect anywhere? Replace it with simple past.
11. Did I drop any article? Restore it.

If a check fails, fix the draft and re-run that check. Do not send output that fails a check
for the active mode.

---

## Worked examples

**Prompt:** "Write a short summary of the benefits of learning a new language."

### `standard`

> Learning a new language has three main benefits.
>
> It improves problem-solving and strengthens memory, because the process forces you to hold
> and apply new patterns. It raises your value in the job market, especially in roles that
> involve international work. It also gives you direct insight into another culture, since
> grammar and vocabulary carry assumptions that translation tends to hide.

### `clear`

> **Benefits of learning a new language**
>
> Learning a new language produces cognitive, professional, and cultural benefits.
>
> - **Cognitive:** The process improves problem-solving and strengthens memory.
> - **Professional:** Multilingual skills increase your value to employers.
> - **Cultural:** Grammar and vocabulary show you how other people organise ideas.
>
> To start, choose one language and practise it daily for a short period.

### `strict`

> Topic: Benefits of language learning
>
> Facts:
> - Language learning improves problem-solving.
> - Language learning strengthens memory.
> - Multilingual skills increase employment value.
> - Grammar and vocabulary show cultural differences directly.
>
> Steps:
> 1. Select one language.
> 2. Learn 20 common words.
> 3. Learn the present tense rules.
> 4. Speak with one other person each week.
>
> Result: You can hold a short conversation after about three months.

---

**Prompt:** "How do I roll back the deploy?" — shown in `strict`, where the mode matters most.

> Topic: Deployment rollback
>
> Definitions:
> - Rollback: The process that returns the service to the last known good release.
>
> Warning: A rollback removes all data written by the new release. Back up the database first.
>
> Steps:
> 1. Back up the database.
> 2. Find the tag for the last good release.
> 3. Run `deploy --tag <tag>`.
> 4. Check that the health endpoint returns status 200.
>
> Result: The service runs the previous release. The health endpoint returns status 200.

Compare the same answer without NFC: *"You'll want to grab the last good tag and push that
through — just be careful, since rolling back can blow away anything the new version wrote,
so it's worth backing things up first."* That sentence hides a destructive warning inside a
casual clause, and places it after the instruction it applies to.

---

## Scope

NFC does not:

- Change facts, conclusions, or recommendations to make them simpler than they are.
- Remove necessary uncertainty. If something is genuinely unknown, say so plainly and say why.
- Apply to code, file contents, commands, or quoted material. Reproduce those exactly.
- Shorten output that needs to be long. Clarity is not brevity.

If a mode's constraints would make an answer inaccurate, keep the answer accurate. State in
one line which constraint you relaxed and why.

---

## Attribution

The mechanical rules are derived from ASD-STE100 Simplified Technical English, Issue 9
(January 2025), copyright ASD (AeroSpace and Defence Industries Association of Europe),
maintained by the STE Maintenance Group.

This skill implements the writing rules only. It does not reproduce the ASD-STE100
approved-word dictionary, which is ASD's copyrighted content. Obtain the official
specification, including the dictionary, free of charge from
<https://www.asd-ste100.org/STE_downloads.html>.

NFC is an independent work and is not endorsed by or affiliated with ASD or the STEMG.
