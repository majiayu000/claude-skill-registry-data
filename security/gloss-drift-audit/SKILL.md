---
name: gloss-drift-audit
description: Use when a source text has been re-vendored, re-collated, or corrected and translations, glosses, or image prompts were derived from the older reading — or when hash/staleness checks report clean but shipped content still says the wrong thing. Covers classical Chinese corpora, any source→translation→prompt→image chain, and deciding which derived rows must be redone before paying to re-render.
user-invocable: true
argument-hint: "[path to the corpus or derived-content dir]"
metadata:
  version: "1.0.0"
---

# Gloss Drift Audit

When a source text is corrected, everything derived from it inherits the old reading. This skill is the order of operations for finding what inherited it — and, just as important, for **not** re-deriving the 96% that is fine.

## The chain

```
source ──► gloss ──► prompt ──► rendered asset
  free      free       free        PAID
```

Every arrow can change meaning. Cost is flat until the last one. That asymmetry dictates the whole order: settle meaning first, move prompts only where meaning actually moved, render once at the end.

## Two failure classes — do not conflate them

| | Movement staleness | Meaning error |
|---|---|---|
| What happened | source moved under the gloss | gloss was wrong the day it was written |
| Detectable? | yes — stamp the source digest per axis | **no** — nothing in the text reveals it |
| Self-clearing? | yes, on restamp | no |
| Typical measure | `sha(source) != stamp` | none exists by default |

**The trap:** a corpus with a green staleness report can be full of mistranslations. A real case — a verse glossed 祈父 (an office: Minister of War, from 《詩經·小雅·祈父》) as "his father" — was never stale for a moment. Its source had not moved in years. Every gate said PASS.

If your only instrument is a digest comparison, you are measuring bookkeeping and calling it correctness.

## Order of operations

1. **Re-measure the baseline first.** A baseline taken after a fix cannot show the fix worked. Expect the number to have moved since it was last written — derived edits ride along with unrelated passes.
2. **Exclude dead data.** Rows superseded downstream (editorial rewrites, overrides) often keep a stale field that nothing renders. Comparing it manufactures findings no reader will ever see. In one audit, **9 of the 10 worst-scoring rows were dead data.**
3. **Run the free comparison** (below), knowing its coverage.
4. **Run the register** (below). This is the instrument with reach.
5. **Correct glosses.** Restamp that axis only.
6. **Re-judge prompts for exactly the corrected rows** — never all of them. Prompt and gloss were authored together from the same reading, so correcting one convicts the other. But check: a generic prompt may be right either way and cost nothing.
7. **Render last, once.**

## Instrument 1 — repeated-source comparison (free, low reach)

If the corpus repeats a source passage across entries, compare the glosses those entries received. Identical source, unrelated output convicts one of them, and generating that comparison needs no expertise — only adjudicating it does.

Band by content-word overlap (share of the **shorter** gloss's content words present in the longer — not Jaccard, which punishes terseness). Sample every band by eye before trusting the boundaries.

**Know its reach before you invest in it.** In one corpus this covered **4.3%** of rows and found zero real errors; its one flagged pair was paraphrase, tripped by short-gloss arithmetic (four content words a side, so one synonym swings the ratio a quarter). Carry the content-word count in the report so a reader sees that — **do not introduce a minimum length until the report reads clean.** A threshold tuned to the answer is not a measure.

Ship it as a **ratchet, not a finder**: it refuses a future pass that retranslates one twin and not the others.

## Instrument 2 — the crux register (hand-seeded; mining fails)

A register of fixed terms that must not be read compositionally: titles, offices, place names, allusions. Each entry: the term, its sense, **its source**, forbidden markers, expected markers.

**Do not try to mine it from the corpus.** This was attempted and measured:

| ranking over 5,687 recurring binomes | candidates | led with |
|---|---|---|
| no stable rendering across glosses | 616 | grammatical collocations |
| inconsistent proper-noun treatment | 2,215 | fragments spanning clause boundaries |
| both filters | 345 | still collocations |

The real crux scored identically to noise, while genuine allusions (彭祖, 大禹, 太乙, 文武) were rendered consistently and scored clean. **Telling a fixed allusive term from an ordinary collocation IS the register's knowledge, so it cannot be bootstrapped from the text the register judges.** Seed it from scholarship and from every error you find by hand.

Two seeded terms found two live violations on first run. Small registers pay.

## Flag and decline — never auto-correct

The checker reports; a human decides. Forbidden-marker present = violation. Expected marker absent = *unconfirmed*, **not** a failure — a correct gloss may reach the sense by other words.

A mechanism that rewrites meaning across thousands of rows is how fabricated content ships. When a transform cannot do something correctly, it must decline rather than guess: an unglossed row matches the source and is never wrong; an invented one is a silent mistranslation.

## Stamps: one per axis, moving with the value

Give each derived axis its own digest of the source it was authored from. Fixing the gloss must not silently clear the prompt's flag — that is how rows leave the review population without being reviewed. Restamp in the same code path that writes the value; a stamp someone must remember is a stamp that eventually does not happen.

Leave the *downstream* stamp disagreeing on purpose. That disagreement is the render queue.

## Red flags

- "The staleness report is green" → it measures movement, not meaning.
- "Re-derive everything to be safe" → that is the paid axis. Re-derive what changed.
- "This ranking found 94 problems" → check for dead data before believing it.
- "Tighten the threshold until it reads clean" → you are tuning to the answer.
- "Fix the gloss now, the picture later" → the picture is now unreviewed and looks reviewed.
- "The refresh already judged this row" → check what question it asked. *Did it move?* is not *is it right?*

## Real-world impact

One pass over a 4,096-verse corpus: baseline re-measured 1,761 → 1,247 (an earlier pass's edits had never been counted); a generated data file found **768 rows behind** because a JSON edit never triggered regeneration; three meaning errors found and fixed; render queue grew **774 → 776**, not 774 → 4,096.

## Testing status

Derived from a production failure — a shipped mistranslation that every automated gate passed — rather than from synthetic pressure scenarios. The numbers above are measured, not estimated. Subagent baseline testing has not been run.
