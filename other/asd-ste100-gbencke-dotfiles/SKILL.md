---
name: asd-ste100
description: >
  Rewrites text into ASD-STE100 Simplified Technical English (STE): a controlled
  language with approved words, one meaning per word, active voice, short sentences,
  and strict rules for procedures and safety instructions. Use when user says
  "simplify to STE", "apply simplified technical english", "asd-ste100", "make this
  STE compliant", "controlled language", or invokes /ste. Also use it to write
  STE reports and investigations that carry ASCII charts and diagrams.
---

# ASD-STE100 Simplified Technical English Skill

Rewrite text into **Simplified Technical English (STE)**, the ASD-STE100 controlled language for technical documentation. STE was built so that any reader — especially a non-native English speaker — understands the text on the first read, and so that translation and maintenance stay cheap and safe.

STE is **not** plain English. Plain English aims for general clarity. STE enforces precise rules: a restricted vocabulary where each word has one meaning and one part of speech, and a fixed set of grammar and structure rules.

## The Two Parts of ASD-STE100

| Part | What it is |
|------|-----------|
| **Writing rules** | ~65 rules across 9 sections covering words, grammar, style, sentence and paragraph structure, procedures, and safety instructions. |
| **Dictionary** | ~900 approved general words. Each has one approved meaning and one approved part of speech, with STE and non-STE example sentences. |

Beyond the dictionary you may add **Technical Names** (nouns for parts, tools, materials — e.g. "grease", "runway") and **Technical Verbs** (project-specific actions — e.g. "to ream", "to rivet"). Everything else must come from the approved dictionary.

---

## The Core Principle

> **One word, one meaning, one part of speech.**

- **One meaning.** Use a word only with its approved meaning. `follow` means "come after", not "obey" → write *"Obey the safety instructions"*, not *"Follow the safety instructions"*. `fall` means "move down by gravity", not "decrease".
- **One part of speech.** Use a word only as its approved part of speech. `oil` is a noun → *"The oil is dirty"* is allowed; *"Oil the valve"* is not. `test` is a noun → write *"Do the test"*, not *"Test the unit"*.
- **One approved synonym.** Pick the approved word and always use it. Use `start` (not begin/commence/initiate), `make sure` (not verify/check/confirm/ensure), `do` (not achieve/carry out/accomplish), `about` (not concerning/regarding), `help` (not assist/facilitate).

---

## The Rewriting Process

Run these passes in order. Each targets one layer.

### Pass 1 — Words (Section 1)

- Replace every unapproved word with its approved equivalent or a rephrase.
- Keep each word to its approved meaning and part of speech.
- Keep Technical Names and Technical Verbs; do not "simplify" a correct technical term.
- Cut jargon, slang, and idioms. No figurative language.

| Unapproved | Approved |
|-----------|----------|
| assist / facilitate | help |
| commence / initiate / begin | start |
| verify / ensure / confirm / check | make sure |
| terminate / cease | stop |
| accomplish / perform | do |
| approximately | about |
| prior to | before |
| sufficient | enough |
| additional | more |
| obtain | get |
| utilize | use |
| deactivate | de-energize / set to off (per project) |

### Pass 2 — Noun clusters (Section 2)

A noun cluster is a string of nouns used as one idea. **Maximum three words.** More than three forces the reader to guess the relationships.

- Allowed: *"overhead panel"*, *"runway light"*.
- Not allowed: *"overhead panel battery section"*.
- Break long clusters with prepositions and articles: *"the battery section of the overhead panel"*.
- Do not drop articles (a, an, the). STE keeps them for clarity and translation.

### Pass 3 — Verbs and voice (Section 3)

1. **Active voice, always.** Name who does the action.
   - Not: *"The screws must be replaced."* → *"Replace the screws."* (procedure) or *"The mechanic replaces the screws."* (description).
2. **Approved tenses only.** Simple present, simple past, simple future. **No present perfect, no progressive.**
   - Not: *"We have received the reports."* → *"We received the reports."*
3. **No compound / helper verb stacks** beyond the approved auxiliaries and modals (can, must, etc.).

### Pass 4 — Sentences and structure (Sections 4, 6)

- **Descriptive sentence: 25 words maximum.**
- **One topic per paragraph.** Start each paragraph with its topic sentence.
- **Paragraph: 6 sentences maximum.**
- Give information gradually; use key words to link sentences and paragraphs.
- Use a vertical list for parallel items or conditions instead of one long sentence.

### Pass 5 — Procedures (Section 5)

- **Procedural sentence: 20 words maximum.**
- **One instruction per sentence** — unless two actions happen at the same time.
- Write instructions in the **imperative (command) form**: *"Remove the electrical power from the system."*
- If an instruction starts with a condition or descriptive phrase, separate it with a comma: *"Before you remove the panel, de-energize the circuit."*
- Split multi-step non-STE sentences into numbered steps.

### Pass 6 — Safety instructions (Section 7)

Warnings and cautions protect people and equipment. They come **before** the step they apply to.

- Start with a clear command or condition (what to do / not do), then explain the risk.
- `WARNING` = risk of injury or death to persons. `CAUTION` = risk of damage to equipment.
- Example: *"WARNING: DO NOT TOUCH THE PROBES TOGETHER. IF THE PROBES TOUCH, THEY CAN BECOME DEMAGNETIZED."*

### Pass 7 — Punctuation and word counts (Section 8)

- Use standard punctuation **except the semicolon (;)** — it invites over-long sentences. Split into two sentences instead.
- Use hyphens to join closely related words.
- In a vertical list, the colon (:) ends the lead sentence; each item then counts as a new sentence for word-count limits.
- Text in parentheses counts as one word of the sentence, and also as its own sentence.

---

### Pass 8 — ASCII charts and diagrams

Add an ASCII chart or diagram each time the text has numbers, a sequence, a flow, a structure, or a comparison. Use as many as the text supports. A reader must see the result before reading the words. Skip a chart only when the text has nothing to draw.

**When to use which visual:**

| Content in the text | Visual to use |
|---|---|
| Counts or percentages to compare | Horizontal bar chart |
| Parts of one total | Stacked bar (100%) or a breakdown tree |
| Numbers over time | Vertical column chart or sparkline row |
| Events in order, with times | Timeline |
| A process, a pipeline, or data movement | Flow diagram with boxes and arrows |
| Calls between systems | Sequence diagram (one column per actor) |
| A rule or a filter that makes a decision | Decision tree |
| Many items narrowed to fewer | Funnel |
| Before and after a change | Two bars side by side for each item |
| Status of many items | Grid or matrix with symbols and a legend |

**Rules for every chart:**

1. Put each chart in a fenced code block (```text) so the monospace alignment stays.
2. Keep each line at 100 characters or less.
3. Use box-drawing characters (`┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼ ▶ ▼`) and bar blocks (`█ ▓ ▒ ░`). Use one set in all of the document.
4. Scale the bars to the data. Calculate the bar length (`value / max × width`) with a script. Do not estimate it. Write the number and the percentage at the end of each bar.
5. Give each chart a title line, the units, and a legend if it uses more than one symbol.
6. Labels in a chart obey the STE word rules. Technical Names (table names, function names, IDs) stay unchanged.
7. Put one STE sentence before each chart. The sentence gives the result that the chart shows. The chart supports the text. It does not replace the text.
8. Every number in a chart comes from the source data. Never invent a value to make a chart look complete. If a value is not known, write `n/a` and say why in the text.
9. Totals in a chart must agree with the totals in the text and the tables.

**Examples:**

```text
Bar chart — cases by result (n = 766)
Shows forms     ████████████████████████████████████████  486  63%
Hidden by bug   ██████████████▌                           176  23%
No forms        ████████▌                                 104  14%
```

```text
Flow — one form from Classic to the UI
┌─────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────┐
│ Classic │──▶│ PlatformSync │──▶│ Medical form │──▶│   UI   │
└─────────┘   └──────────────┘   └──────────────┘   └────────┘
```

```text
Decision — is the form visible for this case?
            form.caseId = this case?
             ├── yes ──▶ VISIBLE
             └── no ───▶ form.caseId is empty?
                          ├── no ───▶ HIDDEN
                          └── yes ──▶ assignedDate >= case.createdDate?
                                       ├── yes ──▶ VISIBLE
                                       └── no ───▶ HIDDEN
```

---

## Output Format

When you finish, deliver:

1. **Rewritten text** — fully STE-compliant, with ASCII charts and diagrams from Pass 8 where the text has numbers, sequences, flows, or structures.
2. **Rule log** — a short bulleted list of the main rules applied, cite the section: `[Word 1.3]`, `[Sentence 5.1]`, `[Voice 3.6]`. Pattern-level, not line-by-line.
3. **Flagged terms** — any word you could not resolve to an approved word without more context, and any term you kept as a Technical Name / Technical Verb.

---

## Execution Rules

- Never invent approved status. If unsure whether a word is approved, flag it: `[⚠ verify against STE dictionary: …]`. The authoritative dictionary is Part 2 of ASD-STE100 (free from asd-ste100.org).
- Never change technical meaning. Losing precision to fit a word limit is a failure, not a simplification. Split the sentence instead.
- Never merge two instructions to save a sentence. One instruction, one sentence.
- Never use passive voice "for variety". Active voice is a hard rule.
- Keep articles and required prepositions even when they add words — they aid comprehension and translation.
- Safety instructions obey the same word limits (20 words) and always precede their step.
- If the text is already short and simple, still verify vocabulary and voice, then output.

---

## Quick Reference — The STE Checklist

- [ ] Every word approved, or a Technical Name / Technical Verb?
- [ ] Each word used with one approved meaning and part of speech?
- [ ] Active voice?
- [ ] Only simple tenses (no present perfect, no progressive)?
- [ ] Noun clusters ≤ 3 words?
- [ ] Procedural sentence ≤ 20 words? Descriptive ≤ 25?
- [ ] One instruction per sentence?
- [ ] Instructions in imperative form?
- [ ] Paragraph ≤ 6 sentences, one topic, topic sentence first?
- [ ] No semicolons?
- [ ] Warnings/cautions before the step, command first then risk?
- [ ] A chart or diagram for each set of numbers, sequence, flow, or structure?
- [ ] Each chart in a code block, ≤ 100 characters wide, with a title, units, and legend?
- [ ] Bars calculated from the data, with the value and percentage written at the end?
- [ ] Chart totals agree with the text and the tables?

If any box is unchecked, revise until it is.

---

## Examples

**Before (Non-STE):**
> "After you have removed the electrical power from the system, make sure that the refueling panel switches go back to their normal position."  *(23 words, present perfect, two ideas)*

**After (STE):**
> "(1) Remove the electrical power from the system.
> (2) Make sure that the refueling panel switches move back to their normal position."

---

**Before (Non-STE):**
> "The battery is not user-replaceable; it can only be replaced by an approved service provider."  *(passive, semicolon)*

**After (STE):**
> "Do not replace the battery. Only an approved service provider can replace it."

---

**Before (Non-STE):**
> "Verify that the overhead panel battery section indicator illuminates."  *(unapproved verb, 4-word noun cluster)*

**After (STE):**
> "Make sure that the indicator on the battery section of the overhead panel comes on."

---

**Before (Non-STE):**
> "We have received the technical reports and are currently reviewing them."  *(present perfect, progressive)*

**After (STE):**
> "We received the technical reports. We examine them now."
