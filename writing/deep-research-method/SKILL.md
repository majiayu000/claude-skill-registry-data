---
name: deep-research-method
description: "Run evidence-backed research for Ottili agents: score sources 0-10 (authority/recency/corroboration, keep >=6), cite every claim with URL + retrieval date + pinned version, resolve contradictions by quality weight, and state confidence high/medium/low. Use when an agent must answer a question from the web, write a research brief, audit a source, or decide which of two conflicting facts to trust. Not for reading a single known-good document."
compatibility: Ottili research workflow; generic (no platform dependency)
license: MIT
---
# Deep Research Method

## When to invoke
Answering any question that requires evidence from the web; writing a research
brief; auditing a source; deciding between two conflicting facts. Do NOT use for
reading a single document you already trust, or for summarising a file you have
locally.

## When to invoke (concrete triggers)
| Trigger | Load? |
|---|---|
| "research this", "find sources for", "what is the evidence for" | YES |
| "two sources disagree", "which is right", "contradiction" | YES |
| "is this source credible", "score this source" | YES |
| "summarise this PDF/article" (single doc, already in hand) | NO |
| "what does the code do" (local repo) | NO |

## Procedure (numbered — follow in order)
1. **Decompose the question** into sub-questions before fetching anything. A
   sub-question that cannot be answered by a source is a scope gap, say so.
2. **Score every source 0-10 before using it** (table below). Only sources >=6
   are kept; a source scoring 5 is discarded unless it is the *only* source for
   a sub-question, in which case it is flagged `low` confidence.
3. **Fetch the primary, not the summary.** A secondary source never carries a
   retrieval date that proves you read the primary. Record URL + retrieval date
   + pinned version for every claim.
4. **Quote under 15 words.** Anything longer is a summary with a citation, not
   a quote. Paraphrase bait is how citations drift.
5. **Resolve contradictions by quality weight**, never by majority vote and
   never by averaging (see `references/contradiction-handling.md`).
6. **State confidence**: high (primary + >=2 corroborating), medium (primary
   only), low (secondary only). Never claim high without corroboration.

## Decision tables
- **Quality score**: authority 0-4, recency 0-3, corroboration 0-3. >=6 keep.
- **Authority**: official body/standards org = 4; major vendor = 3; academic =
  3; established media = 2; blog/unknown = 0-1.
- **Recency**: <1 year for fast-changing = 3; 1-3 years = 2; 3-5 years = 1;
  >5 years = 0 unless the fact is stable.
- **Corroboration**: 3+ independent = 3; 2 = 2; 1 = 1; none = 0. "Independent"
  means distinct upstreams, not distinct URLs: two pages that copy the same primary
  count as one. Verify with `scripts/score_sources.py corroboration`.
- **Confidence**: high = primary + >=2 corroborating; medium = primary only;
  low = secondary only; none = no source.
- **Citation rules**: every claim needs URL + title + retrieval date; a claim
  missing any one is downgraded one rung. Quotations <=15 words are fine with a
  citation; longer ones need a page/section reference. A paraphrase must change
  wording, argument order, or level of abstraction; otherwise it is a quote.
  Version-sensitive facts record the exact version seen and are re-fetched if
  older than 7 days. Contradictions are recorded in `references/incidents.md`
  with both sources and the resolution (see `references/citation-discipline.md`).

## Near-miss triggers (stop and re-check before proceeding)
- A source with no retrieval date -> not evidence, re-fetch and record.
- A secondary source used as the sole evidence -> fetch the primary.
- A contradiction resolved by majority vote -> re-weight by quality.
- A fact stated without a source -> mark it as unverified.
- Two sources disagree and the answer averages the numbers -> fake precision;
  list, weight, state the range.
- A 2024 fact used for a 2026 question without re-checking -> re-fetch.
- A kept source with score <6 -> it was never scored.
- Two URLs that agree exactly on a value but share an upstream -> the fake middle;
  they are one source, not two. Count upstreams, not URLs.
- A kept source with no retrieval date or no pinned version -> it is memory, not
  evidence; run `scripts/score_sources.py provenance` to catch it.

## Pitfalls from research
- P1: Source quality is judged before reading; a good-looking page can be wrong.
- P2: Retrieval dates are mandatory; memory is not evidence.
- P3: Contradictions must be surfaced, not averaged away.
- P4: Secondary sources masquerading as primary are the common failure.
- P5: Stale facts are reused because they were once verified.
- P6: A source that scores 5 is not "close enough" — it is discarded, unless it
  is the only source for a sub-question, in which case it is flagged low.
- P7: Averaging two sources into a middle value produces a number no source
  claimed; it reads as precision and carries no evidence.

## Verification checklist
- [ ] Question decomposed into sub-questions.
- [ ] Every source scored 0-10 before use; only >=6 kept.
- [ ] Every source has URL + retrieval date + pinned version.
- [ ] Every claim cites a source; no unsourced claims.
- [ ] Contradictions listed and resolved by quality weight.
- [ ] Confidence stated (high/medium/low) with the reason.
- [ ] Quotations under 15 words.
- [ ] `scripts/score_sources.py corroboration` passes: every kept URL traces to
  a distinct upstream. Two URLs sharing an upstream count as one source.
- [ ] `scripts/score_sources.py provenance` passes: every kept source carries
  URL + retrieval date + pinned version.

## Worked examples

### Good — scored, cited, confidence-stated answer
Question: "What is the retention period for GDPR erasure requests?"

1. Decompose: (a) the statutory deadline, (b) whether it has changed, (c) any
   member-state derogation.
2. Score candidates before reading: the EU legal-summary page scores 10
   (authority 4, recency 3, corroboration 3); a blog scores 2 and is discarded.
3. Fetch the primary legal text first; record URL + retrieval date + version.
4. Cite by short paraphrase under 15 words, with the URL next to each claim.
5. Two independent upstreams corroborate -> confidence `high`, stated with the
   reason.

Result: every claim carries URL + retrieval date + version; confidence is high
only because two upstreams corroborate. Detection signal: no claim lacks a
citation, and the confidence word is followed by "because ...".

### Bad — unsourced claim dressed as a finding
"The model is 3x faster than the baseline." No URL, no retrieval date, no version.

Why it fails: the claim cannot be verified or re-checked. The rule is URL +
retrieval date + pinned version for every claim; a claim without a source is a
confidence of `low` and must be flagged, not asserted.
Detection signal: a sentence with a number and no citation.

### Bad — contradiction averaged into a fake middle
Source A (university preprint, score 8) says "one month". Source B (industry
report, score 6) says "two months".

Why it fails: averaging to "one and a half months" produces a number no source
claimed; it reads as precision and carries no evidence. Resolve by quality
weight: cite A as primary, note B as a lower-weight disagreement, and state the
range (one to two months). Never majority-vote and never average.
Detection signal: the summary names both sources and gives a range, not a
single number.

### Bad — quoting 22 words to "prove" a point
`"the results show a statistically significant improvement in latency,
throughput, and accuracy across all benchmarks"`.

Why it fails: long quotations are paraphrase bait and easy to misquote. Keep
quotations under 15 words; anything longer is a summary with a citation, not a
quote.
Detection signal: a blockquote longer than 15 words that is not labelled a
summary.

More worked examples, each ending with the check that would have caught it, live
in `references/examples.md`.

## Related skills
- [verifiable-environments](../verifiable-environments/SKILL.md) — the SPEC a verifier is derived from is a research product with cited sources; a verifier's bypass audit is itself a research claim.
- [skill-authoring-evals](../skill-authoring-evals/SKILL.md) — the source-scoring rubric and the trigger-eval methodology are research products; cite them and state confidence.

## References
- procedures: references/procedures.md
- citation discipline: references/citation-discipline.md
- scoring: references/source-scoring.md
- contradiction handling: references/contradiction-handling.md
- confidence ladder: references/confidence-ladder.md
- staleness: references/staleness.md
- source scoring: references/source-scoring.md
- cite fetch: references/cite-fetch.md
- examples: references/examples.md
- incidents: references/incidents.md
- SOURCES: references/SOURCES.md
