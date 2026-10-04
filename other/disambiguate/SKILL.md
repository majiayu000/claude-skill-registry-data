---
name: disambiguate
tier: D
category: tooling
description: >-
  Rewrite a requirement so it can only be read one way. Distilled from
  ASD-STE100 Simplified Technical English — forty years of aerospace evidence
  about what a reader misreads when they cannot ask the author what he meant.
  Turns a vague ask ("handle errors gracefully", "the system should support
  X") into something atomic, owned, bounded, and testable, and says which of
  five reader-questions each defect leaves open. Ships a deterministic checker
  (scripts/disambiguate.py, stdlib only) that catches the mechanical
  ambiguity — agentless passive, noun stacks, weak modals, unquantified
  deltas, compound obligations, over-length sentences, condition-after-action,
  synonym drift — so judgment goes to the parts that need it. USE WHEN:
  sharpening a requirement, acceptance criterion, ticket, spec line, PRD,
  API contract, error message, runbook step, or agent prompt. Also when a review
  comment says "unclear" or "what does this mean", when two people read the
  same line differently, and when writing instructions for someone who cannot ask
  a follow-up question. Triggers on "disambiguate", "improve this
  requirement", "tighten this spec", "make this unambiguous", "is this clear",
  "rewrite this ticket", "sharpen this AC", "review this requirement",
  "simplified technical english", "STE", "controlled language". NOT FOR:
  prose style or tone editing (this makes text precise, not pleasant),
  formatting a design doc (use make-spec), deciding what belongs IN one
  (use spec-contract), or deciding *what* to build (this
  sharpens a decision already made, it does not make it).
---

# disambiguate — make a requirement readable exactly one way

**A requirement is read by someone who cannot ask you what you meant.
Every reading your words permit is a system someone might build.**

## Why an aerospace writing standard is the right source

ASD-STE100 Simplified Technical English exists because maintenance manuals
were killing people. Technicians across dozens of first languages read
procedures written by native English engineers, misread them, and aircraft
came apart. The standard is not a style guide that emerged from taste. It is
an incident ledger. Each rule closes one observed way a reader went wrong.

Its design assumptions are worth stating plainly, because they are what makes
it transfer:

1. The reader may not share the author's language or background.
2. The reader **cannot ask a follow-up question.**
3. A misreading is expensive and discovered late.
4. The reader consumes **one unit at a time, out of context** — they do not
   read the document, they read the step in front of them.

Those four conditions describe a technician at 3am with a torque wrench. They
also describe, exactly, an engineer picking up your ticket, a contractor
reading your spec, and an agent executing your prompt. That is the whole
argument for this skill. The domain is different. The reader is the same.

The standard's second lesson is structural, and it is the one most writing
advice misses:

> **Clarity is not produced by exhortation. It is produced by closing the
> state space.**

"Be clear" is unenforceable. "A sentence has at most 20 words, one instruction,
one meaning per word, and no semicolon" is checkable, and clarity falls out of
it. This skill inherits that: it does not advise, it detects and substitutes.

## The five questions

The standard's rules and recommendations collapse into five questions a reader
must be able to answer **from the text alone**. Every ambiguity defect is one
of these going unanswered. When you review a requirement, walk the five.

| | The reader asks | And cannot answer it when… |
|---|---|---|
| **A** | **Which thing?** | the text points without naming |
| **B** | **Who must, and must they?** | the actor or the obligation is missing |
| **C** | **How do I know it is done?** | no observation settles it |
| **D** | **Can I hold this?** | the unit exceeds what one pass can carry |
| **E** | **Can I parse it at all?** | the construction admits two grammars |

The full catalog — every defect, the reading it permits, and the rewrite — is
in `references/ambiguity-catalog.md`. The highest-yield ones:

**A — Which thing?**
- A bare `this` / `it` / `they` with two candidate antecedents. The two
  readings routinely have opposite consequences: *"If you engage the pins
  incorrectly with the seats, they can become damaged"* — the pins, or the
  seats? Name the noun, accept the repetition.
- A noun stack of four or more (`user session token refresh interval config`).
  **A noun stack is a relation graph with the edges deleted.** The fix is not
  to shorten it. It is to put the edges back with prepositions, then keep each
  resulting group to three words.
- Three names for one object across a document. The reader assumes three
  objects. Elegant variation is a virtue in prose and a defect in a spec.

**B — Who must, and must they?**
- Agentless passive. *"The data is validated"* — by whom? This is the single
  most common requirement defect, because it reads as complete while naming
  nobody.
- A non-command instruction leaves **three** things open at once: whether the
  step is required, who does it, and whether it has already been done.
  *"The test can be continued"* is permission, capability, and a past-tense
  report all at once. *"Continue the test"* is one thing.
- `should` / `may` / `could`. Two readers ship two systems and both claim
  conformance. Pick `must`, `can`, or `will`.

**C — How do I know it is done?**
- A state-assertion with no action. *"No leaks are permitted"* names a desired
  world and no observation. *"Make sure that there are no leaks"* names a check
  someone can perform. **Convert every desire into an observation.**
- A direction of change with no baseline. *"Different temperatures will change
  the cure time"* is not wrong, it is unusable. *"The cure time is 2 hours at
  20 °C"* is a requirement. If no value of the system makes the sentence false,
  it cannot be tested.
- A hedge that defers the decision back to the reader: *appropriately*,
  *gracefully*, *as needed*. The disagreement is not avoided, only postponed
  to review.
- A risk without its consequence. Stating the outcome is what makes a person
  careful. *"Cleanliness is imperative"* does not, *"oxygen and grease make an
  explosive mixture"* does.

**D — Can I hold this?**
- Over-length: 20 words for an instruction, 25 for a description. The ceilings
  differ **because the modes differ** — an instruction is executed under load
  one step at a time. A description is read as a unit. Never apply one ceiling
  to the other mode.
- Compound obligation. Two actions in one sentence means a reader can do the
  first, stop, and still record the step as done. Split it — unless the actions
  genuinely occur at the same time (*"Remove and discard the seal"*), which is
  the only case where one sentence is right.
- The semicolon, banned outright. It joins two independent clauses, so the unit
  now holds two statements and a test cannot report which half failed.

**E — Can I parse it at all?**
- `-ing` forms. *"Changing filters"* is the act of changing, or the filters
  that change.
- A dropped `that`. *"Make sure the valve is open"* hides where the main clause
  ends. Most languages cannot drop the equivalent word, so a translating reader
  stalls.
- **Condition after action.** *"Set the switch to NORMAL when the light comes
  on"* makes the reader act, then learn whether it applied. The condition is
  the applicability test, so it has to arrive first, separated by a comma. This
  one is worth internalizing beyond requirements — it is why `if` precedes the
  body in every language you write.

## The shape to rewrite into

Each slot exists because one of the five questions demands it. This is not a
template borrowed from a testing framework. It is what falls out of the rules.

```
[Condition]            When <observable state>,          ← E, arrives first
[Actor + action]       <actor> <single imperative verb>  ← B, one owner one act
[Bounded object]       <object with its threshold>.      ← C, testable
[Verification]         Make sure that <observation>.     ← C, a check, not a wish
[Consequence]          If not, <named outcome>.          ← C, why it matters
```

Worked, from a real ticket:

> **Before** — The system should handle authentication errors gracefully and
> retry as needed.

Five questions, five failures: *which* errors (A). *The system* is not an actor
and *should* is not an obligation (B). *Gracefully* and *as needed* have no
observable (C). Two obligations sit in one sentence (D).

> **After**
> When the identity provider returns 5xx, the auth service retries the token
> request three times at 200 ms intervals.
> After the third failure, the auth service returns 503 and writes one error
> record with the provider response code.
> Make sure that no retry occurs on a 4xx response.

Longer. That is the trade, and it is the right one: the second version cannot
be built two ways.

## Procedure

1. **Declare the mode before checking anything.** Procedural (commands the
   reader) or descriptive (informs them)? This sets the ceiling and the verb
   rules, and mixing the two in one unit is itself a defect. A requirement is
   normally procedural with a descriptive precondition.
2. **Run the checker.** `python3 scripts/disambiguate.py <file> [--json]`.
   It settles the mechanical layer so your attention goes to the semantic one.
   `--glossary terms.json` supplies product names and proper nouns that count
   as one word.
3. **Fix structure before vocabulary.** The common error is to swap words and
   call it done. Most real ambiguity is structural: a noun stack, a compound
   obligation, an inverted condition. A word-for-word replacement is often not
   enough, and reaching for one is the tell that the sentence needs splitting.
4. **Rewrite, never merely flag.** See below.
5. **Re-run, and read the diff aloud.** If the rewrite is longer and duller and
   admits one reading, it is correct.
6. **Report what changed and which question it closed** — not a list of rule
   numbers. The author should learn the five questions, not memorize a linter.

## The substitution discipline

The source standard never lists a disallowed word without an approved
alternative, a compliant example, **and** the non-compliant example beside it.
That is a deliberate design choice and the most transferable thing about the
whole document:

> **A prohibition without a substitute is not actionable. It is a complaint.**

So: never emit "this is vague." Emit the rewrite. If you cannot produce the
rewrite because you lack the domain fact — the actual threshold, the actual
actor — then **say which fact is missing and who has it.** "This needs a
latency target, ask the SRE on-call" is actionable. "This is unmeasurable" is
not. The checker enforces this on itself: every finding carries a `fix`, and a
test fails the build if one does not.

## Traps

| Trap | Why it is wrong |
|---|---|
| Shortening by deleting words | *"If installed, remove the shims"* is shorter and slower to read. Terseness is not clarity. Restore the subject, the article, the verb. |
| Applying the 20-word ceiling to prose | Descriptive text gets 25, and the count rules are not word-splitting: a parenthetical, a quoted span, a number with its unit, and a hyphenated compound each count as **one**. |
| Treating the checker's silence as approval | It clears the mechanical layer only. Word-sense, atomicity, and whether the threshold is the *right* threshold all need judgment. |
| Flagging every passive | Passive with a named agent is a style cost. Passive **without** one is a missing owner. Only the second is a defect. |
| Splitting genuinely simultaneous actions | *"Remove and discard the seal"* is one action. Atomicity is ontological, not grammatical. |
| Rewriting a quoted string, placard, or external API field | Some text cannot be changed. Count it as one word and leave it alone. |
| Reproducing the standard | Do not paste its dictionary or rule text into a repo. Cite the rule number and link the free download. |

## Deterministic / latent split

The checker owns the part that is mechanical. You own the part that needs to
know what the system does.

**Script** — the word-count algorithm (parenthetical, quoted span, uppercase
run, number with unit, hyphenated compound, and identifier each count as one),
plus detectors for agentless passive, noun stacks, bare demonstratives,
ambiguous pronoun antecedents, weak modals, dropped subjects, state-assertions,
unquantified deltas, vague predicates, missing consequences, over-length,
compound obligations, semicolons, paragraph overrun, mode mixing, `-ing` forms,
dropped `that`, condition-after-action, contractions, Latin abbreviations,
opaque phrasal verbs, slash conjunctions, and synonym drift across a document.

Attachment ambiguity around "with" (A3) is **not** detected. It needs a parse,
and the surface rule fired on every imperative containing the word. Word-sense
ambiguity and false friends are not detected either — both need vocabulary this
skill does not ship. Noun stacks are detected **only in command form** — in a declarative the
detector cannot tell the finite verb from a modifier, and four attempts at a
surface proxy each broke something. A command whose verb is outside the
vocabulary is not recognized at all. `references/ambiguity-catalog.md` lists
every limit with its measured cost.

The rule underneath all of these: **the parser fails open, the detectors fail
quiet.** Where the document structure cannot be resolved, more text gets
checked and the uncertainty is reported, because a missed finding is invisible.
Where a *detector* cannot decide, it stays silent, because a false positive
teaches the reader to ignore it.

**You** — which preposition restores the right relation in a noun stack,
whether two actions are genuinely simultaneous, whether a word is ambiguous
*in this domain*, what the threshold should actually be, what the real risk
level is, and whether the requirement is worth having at all.

Where the algorithm cannot decide — a multi-word proper noun or a document
title needs domain knowledge — it reports an advisory naming the gap and the
remedy rather than guessing. Silent approximation would read as coverage. The
catalog's "Known limits" table states every boundary up front, because a limit
you discover reads as a bug and a limit that is written down reads as a
boundary.

## Validation

```bash
python3 -m pytest tests/ -q            # 154 tests
python3 tests/mutation_proof.py        # each fix is proven load-bearing
python3 scripts/disambiguate.py --count "Remove the safety pin (10)."   # → 5
python3 scripts/disambiguate.py REQUIREMENTS.md --strict                # CI gate
```

The word-count tests use the worked examples published in the standard's
section 8, where it states the expected count for each sentence — so the
algorithm is checked against the authority rather than against my reading of
it. Every detector asserts both polarities: it fires on the defect and stays
silent on the clean rewrite.

## Provenance and copyright

Distilled from **ASD-STE100 Issue 9 (January 2025)**, © ASD, Brussels. The
standard is free to download from [asd-ste100.org](https://www.asd-ste100.org)
and is the authority. This skill is a reading of it, not a copy. ASD grants
reproduction rights to a defined set of organizations, so **no dictionary
entries and no rule text are redistributed here.** What ships is the distilled
principle set, an original detector implementation, and short example sentences
used as test fixtures.

Rule references (`3.6`, `GR-4`, `5.2`) point into the standard so a reader can
check the source. STE proper is a controlled language with an approved
vocabulary, and word-level conformance needs the official dictionary, which this
skill deliberately does not carry. What it carries is the part that generalizes.

## References

- `references/ambiguity-catalog.md` — the full catalog: every defect, the
  readings it permits, the rewrite, and the rule it comes from.
- `scripts/disambiguate.py` — the deterministic core.
- `tests/test_disambiguate.py` — oracle cases and both-polarity detector tests.
