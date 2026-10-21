---
name: technical-writer
owner: baseline
description: Standard operating procedure for producing a documentation page end to end — gather source material, classify, draft against the measured corpus profile, then run the reader-level and humanizer passes and both gates. Use for any page on a documentation surface, or when rewriting a page that reads as machine-written. Orchestrates technical-writing, reader-level and humanizer in a fixed order.
---

This skill is the pipeline. `technical-writing` carries the craft rules and the measured targets; this skill says what order to do things in, what to gather first, and what must pass before a page is done.

Two failure modes it exists to prevent:

1. **Writing before knowing.** A page drafted from the model's impression of a system is fluent and unfalsifiable. It reads as generated because it is describing a guess. Step 1 is not optional.
2. **Passing the checks in the wrong order.** Simplifying after de-slopping reintroduces phrasing that the de-slop pass already cleaned, so the pass has to run twice and the second run flattens the prose.

---

## Step 1 — Prepare context

Nothing is drafted until this is done. Produce a source table before writing a sentence.

1. **Read the implementation, not the description of it.** For each claim the page will make, open the file that makes it true — the hook script, the config key, the CLI parser, the schema. Record `path:line`.
2. **Run the thing** where running it is cheap. A flag table copied from a parser is right; a flag table recalled is not. Capture real output for the examples.
3. **Reconcile against the governing docs.** Where this repository has a constitution, a genesis spec, or a manifest, the page must not contradict it. Note the Article or section each claim answers to.
4. **Check third-party APIs against current documentation** before describing them (the declared documentation provider, official docs, or a pinned local cache). Never from recall.
5. **List what you could not verify.** Anything left unverified is cut from the draft or written as an explicit open question. It is never softened into a vague sentence.

Output of this step is a working note: claim → source → verified date. Every factual sentence in the finished page traces back to a row in it.

**If the source material is thin, the page is thin.** Do not pad it with description. A short page that is entirely true is the correct deliverable.

---

## Step 2 — Classify and shape

Pick exactly one Diátaxis type: `reference`, `explanation`, `tutorial`, or `howto`. This decides the numeric targets, the heading grammar, the person and the passive rate. See `technical-writing` Step 1.

Then sketch the section list before prose. Headings are noun phrases for reference and explanation; gerunds are correct for roughly a third of tutorial and how-to headings. Corpus mean heading length is 2.7 words.

Check the section count against the corpus: reference runs about 1,160 words per section, explanation 445, tutorial 225, how-to 201. A page with two enormous sections is under-structured.

---

## Step 3 — Draft

`Skill(technical-writing)` — the craft rules and the measured profile.

Draft from the Step 1 source table only. While drafting, hold the four range moves in mind, because they are the ones that cannot be added by a later pass without rewriting:

- Vary the paragraph opening move. Assertion should be about two thirds, not all of them.
- Let roughly one sentence in nine run past 30 words, and put a short one after it.
- Use `can`, `may`, `must`, `will`, `should` — about 20 per 1000 words.
- Use the passive where the actor is irrelevant. Reference prose is around 36% passive.

Name real identifiers, enumerate real options, and show real output. Density of evidence is what separates a technical writer's page from a plausible one.

---

## Step 4 — Reader level

```
node .claude/skills/reader-level/score.mjs --target 11 <file>     # reference, explanation
node .claude/skills/reader-level/score.mjs --target 10 <file>     # tutorial, how-to
```

`Skill(reader-level)` for the rewriting moves when it fails.

**Use these targets, not the skill's default of 9.** `reader-level` is a *ceiling* — it catches prose pitched above the reader. `technical-writing` sets the *floor*. Professional documentation measures at grade 10.7, so a target of 9 drives the page below the corpus band and strips the qualifying clauses that carry the meaning. Run together at target 11, the two gates bracket the page into the range real documentation occupies.

The other three reader-level limits (hard words, clause load, jargon load) stay at their defaults. They do not conflict with the corpus profile: the corpus sits at roughly 0.36 subordinate clauses and 0.6 identifiers per sentence, inside both limits.

---

## Step 5 — Humanizer

`Skill(humanizer)` on the full draft. Always. Use its output.

Then re-check that its edits did not flatten the page: humanizer removes patterns, and removal moves several axes downward at once. Step 6 catches this.

---

## Step 6 — Gates

Both must pass, in this order.

```
node .claude/skills/technical-writing/measure.mjs --type <type> <file>
node .claude/skills/reader-level/score.mjs --target <11|10> <file>
```

The first is the binding one. Threshold 4.5; the corpus median is 0.14. If it fails, read the named axes — each finding says which direction the page is wrong in and why that direction reads as machine-written — and return to Step 3. Do not tune sentences one at a time to move the number; fix the underlying habit the axis is reporting.

If a fix at Step 3 depends on a fact you do not have, go back to Step 1. A page that cannot pass without inventing something is a page missing source material.

---

## Step 7 — Read it

The gates cannot see these. Run them by hand before declaring done.

- **Paragraph-reshuffle.** Swap two body paragraphs. If nothing breaks, the section is a list wearing prose.
- **Treadmill.** Per paragraph, ask what is new. Cut what is not.
- **Headings alone.** Read them in order. They should read as a table of contents, not a series of claims.
- **Trace three claims.** Pick three factual sentences at random and find their row in the Step 1 table. A miss means the page invented something, and the whole page needs re-checking.
- **Type leakage.** Instruction on a reference page, explanation inside a tutorial — move it and link.

---

## Receipt

Close with:

| Field | Value |
|---|---|
| Page type | one of the four |
| Sources verified | count, and anything left unverified |
| measure.mjs | score before → after (threshold 4.5) |
| reader-level | grade before → after (target 11 or 10) |
| Axes moved | the ones that were out of band and now are not |

A receipt that cannot honestly be written means the page is not done.
