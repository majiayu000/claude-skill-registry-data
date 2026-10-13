---
name: asd-ste100
description: "Write, rewrite, or audit technical documentation in ASD-STE100 Simplified Technical English (Issue 9). Use when the user asks for Simplified Technical English or STE, mentions ASD-STE100, S1000D, ATA iSpec 2200, controlled or constrained English, or asks to make maintenance manuals, work instructions, procedures, safety warnings, SOPs, or operator documentation translation-ready, plain, or compliant with a controlled-language standard."
---

# ASD-STE100 Simplified Technical English

Simplified Technical English is a controlled natural language: a restricted dictionary of
~875 general words plus your own technical terms, and 65 writing rules. It exists so that a
maintenance technician reading in their second language, under time pressure, on a cold ramp,
cannot misread the instruction — and so that machine translation and reuse stay clean.

It is mandatory in aerospace and defense documentation (S1000D, ATA iSpec 2200) and is used
across rail, automotive, medical devices, heavy equipment, and increasingly for text that
LLMs must parse unambiguously.

**STE is not "plain English".** Plain English is a style. STE is a specification: a word is
either approved or it is not, a sentence is either inside the length limit or it is not.
Do not approximate it. Check the dictionary.

## When this skill is running

You are a controlled-language editor, not a copywriter. Three things change:

1. **Vocabulary is closed.** Every word must be approved in the dictionary, or be a technical
   noun / technical verb that fits one of the 26 categories. "Ensure", "perform", "prior to",
   "utilize", "should", "however" are all out.
2. **Variety is a defect.** The same thing gets the same name and the same sentence pattern
   every time. Synonyms are an error, not style.
3. **The rules beat your ear.** Text that obeys STE reads blunt and repetitive to a native
   speaker. That is the intended output, not a draft to be smoothed.

## The hard limits

| Constraint | Procedural writing | Descriptive writing |
|---|---|---|
| Sentence length | **20 words** (5.1) | **25 words** (6.3) |
| Instructions per sentence | **one** unless simultaneous (5.2) | n/a |
| Verb form | imperative / command (5.3) | imperative **not** permitted (6.x) |
| Voice | active only (3.6) | active; passive only when the agent is unknown (3.6) |
| Paragraph | n/a | **max 6 sentences**, one topic (6.5, 6.6) |
| Multi-word nouns | **max 3 words** (2.1) | **max 3 words** (2.1) |
| Semicolon | never (8.1) | never (8.1) |

Tenses: infinitive, imperative, simple present, simple past, simple future, past participle as
an adjective. **Nothing else** — no perfect, no continuous, no conditionals (3.2, 3.4).

Word count rules make the limits workable: a parenthetical, a number with its unit, an
abbreviation, quoted text, a heading, or a hyphenated word each count as **one word** (8.5–8.7),
and a colon inside a vertical list ends the sentence for counting purposes (8.4).

## Workflow

### Writing new text

1. **Classify first.** Procedure, description, or safety instruction? The rules differ, and the
   wrong classification produces text that fails on every sentence.
2. **Fix the terminology before the prose.** List the items you must name. Pick one technical
   noun for each from the company glossary (1.8–1.11), and use nothing else for the rest of
   the document.
3. **One action per sentence, verb first.** "REMOVE THE COVER." Condition before command, with
   a comma: "If the pressure is more than 800 kPa, close the valve." (5.4)
4. **Check every word against the dictionary** as you go, not afterwards —
   `references/approved-words.md`. Unknown word → is it a technical noun or technical verb in
   one of the categories in `references/writing-rules.md`? If not, look it up in
   `references/replacements.md`.
5. **Run the checker** (below) and resolve every error.

### Rewriting existing text into STE

Work sentence by sentence; do not try to rewrite a paragraph in one pass.

1. **Split.** Break every sentence at its conjunctions until each one carries one idea. Length
   violations almost always dissolve here.
2. **De-passivate.** Find the agent and make it the subject, or make the sentence a command.
3. **Fix the verbs.** Perfect and continuous tenses → simple tenses. Nominalizations back into
   verbs: "do an inspection of" → "INSPECT" (3.7).
4. **Swap the words.** `references/replacements.md` gives the approved alternative for 1312
   not-approved words. When no alternative carries the meaning, **restructure the sentence**
   (9.1) — do not force a bad substitution.
5. **Break up the noun strings.** Any modifier chain over three words gets a preposition:
   "horizontal cylinder pivot bearing" → "the pivot bearing of the horizontal cylinder" (2.1).
6. **Re-check.** Rewriting introduces new violations; run the checker again.

### Auditing someone else's text

Report findings as `rule number — what is wrong — the compliant rewrite`. Lead with the errors
that recur across the document (one bad term used 40 times) before the one-off sentence
violations. A compliance report that lists 300 individual findings and no pattern is not useful.

## The checker

```bash
python3 scripts/ste_check.py FILE [--mode procedure|descriptive|auto] [--quiet]
```

Flags sentence length (with STE word counting), semicolons, contractions, Latin abbreviations,
gendered pronouns, perfect and continuous tenses, passive voice, `-ing` forms, phrasal verbs,
paragraph length, and every word that is not approved — with its approved alternative.

`--quiet` hides `note` findings, which are the words the script cannot judge: it does **not**
know whether `valve`, `bay`, or `accumulator` is a legitimate technical noun. That call is
yours. Run without `--quiet` once per document to make those calls deliberately, then with
`--quiet` while you iterate.

Vocabulary findings are blind to part of speech: a word the dictionary rejects only as a verb
(`service (v)`) is still reported inside a legitimate technical noun ("ground service cart").
Read the part of speech named in the finding before you change anything.

The script is a backstop, not the standard. It cannot see an approved word used with the wrong
approved meaning (1.3), a multi-word noun that is ambiguous, or an instruction that is simply
unclear.

## Worked example

**Non-STE** (36 words, passive, perfect tense, continuous tense, Latin abbreviation, semicolon):

> The pressure relief valve, which has been installed in the forward equipment bay adjacent to
> the accumulator, is being monitored continuously by the system controller; it will
> automatically open when excessive pressure is detected, e.g. above 3000 psi.

**STE** (three sentences, each under 25 words, active voice, simple tenses):

> The pressure relief valve is in the forward equipment bay, adjacent to the accumulator.
> The system controller monitors the valve continuously. The valve opens automatically when
> the pressure is more than 3000 psi.

**Non-STE procedure:**

> Prior to commencing the removal procedure, the technician should ensure that the hydraulic
> fluid has been drained and that additional fluid is not added utilizing the service cart.

**STE procedure** (condition first, one instruction per sentence, imperative):

> 1. Before you remove the unit, make sure that you drained the hydraulic fluid.
> 2. Do not add fluid to the hydraulic reservoir.

**Safety instruction** — command first, then the risk (7.2, 7.3):

> WARNING: DO NOT TOUCH THE EXHAUST DUCT. THE SURFACE IS HOT AND CAN CAUSE BURNS.

## What good looks like

- Every sentence inside its word limit, counted by STE rules — not by `wc -w`.
- The same component has one name on page 3 and page 300.
- A reader can tell from the first three words of each step what they must do.
- Warnings and cautions open with the action, never with the explanation.
- Running `ste_check.py --quiet` returns zero errors, and every remaining `note` is a technical
  noun you can place in one of the 22 categories.

## Gotchas

- **"Ensure" is the most common error.** It is not approved: use `MAKE SURE THAT`. Likewise
  `perform` → `DO`, `prior to` → `BEFORE`, `follow` → `OBEY`, `may` → `CAN`, `should`/`shall`
  → `MUST`, `however` → `BUT`, `therefore` → `THUS`, `rotate` → `TURN`, `press` → `PUSH`,
  `insert` → `PUT`, `required` → `NECESSARY`. Full list in `references/replacements.md`.
- **Part of speech is binding (1.2).** `CHECK`, `TEST`, `DAMAGE`, `COVER`, `OIL` are approved as
  nouns and are errors as verbs: "DO A CHECK OF THE VALVE", not "check the valve".
- **Approved ≠ usable anywhere (1.3).** `FOLLOW` is approved only as "come after". Check the
  approved meaning in the standard, not just the headword.
- **Do not strip articles.** "Remove cover" is wrong; STE requires "Remove **the** cover" (4.5),
  and "make sure **that**" keeps its conjunction (GR-1).
- **Do not smooth the output.** If you find yourself varying a verb for readability, you have
  left STE. Repetition is correct.
- **Technical nouns are not a loophole.** A word is a technical noun because it fits one of the
  22 categories and lives in the project glossary — not because you need it in that sentence.
- **Gendered pronouns and Latin abbreviations are out** (GR-7, GR-6): no "he"/"she", no "e.g.",
  "i.e.", "etc."
- **The standard is free.** When a ruling matters, check Issue 9 itself at https://asd-ste100.org
  rather than trusting the extracted references here.

## References

- `references/writing-rules.md` — all 65 rules by section, the 22 technical noun categories, the
  4 technical verb categories, and GR-1 to GR-8.
- `references/approved-words.md` — the approved dictionary words, grouped by part of speech.
- `references/replacements.md` — not-approved word → approved alternative, and the standard's
  own list of recurring errors.
- `scripts/ste_check.py` — the mechanical checker.

Reference content is extracted from ASD-STE100 Issue 9 (January 2025), © ASD, for use as a
working index. The published standard is the authority and is free to download from
https://asd-ste100.org.
