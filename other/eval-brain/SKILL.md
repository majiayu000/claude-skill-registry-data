---
name: eval-brain
description: >-
  Carefully evaluate and grade the Ramco ERP "Brain" chatbot's answers against the
  ground-truth question bank (BrainEvals-Layer1). Use this skill WHENEVER you are
  scoring, grading, judging, benchmarking, or running an evaluation of Brain answers —
  or when the user says "eval the brain", "score these answers", "run the evals",
  "grade against ground truth", "judge as correct/hallucination", or asks how well the
  Brain answers. Two rules define careful grading here and this skill enforces them:
  (1) drop two-word and otherwise low-quality/malformed questions from the eval set —
  they are not real questions; (2) an answer that is MORE comprehensive than the ground
  truth (a superset) is CORRECT, not a hallucination — a hallucination is ONLY inventing
  facts that are not there. Judge on informational equivalence of the important points,
  semantically, in English.
---

# Evaluating the Brain — careful, fair grading

The Brain answers via the `brain_chatbot` agentic API; you grade each answer against a
ground-truth **expected_response** in the question bank. Grading is **LLM-as-judge**, and the
whole value of this skill is doing it *carefully and fairly* — neither generous nor harsh, and
never mistaking thoroughness for hallucination.

## The two rules that define "careful" here

### Rule 1 — Curate the question set first: drop non-questions
A two-word "question" is not a good question and must not be scored. Before grading, **filter the
bank** and set aside (don't delete — mark `excluded` with a reason) any item that is:

- **Too short / not a real question** — e.g. two-word fragments, a bare code or term with no
  interrogative intent ("PO approval", "GRN status").
- **Malformed or ambiguous** — no answerable proposition; the grader can't tell what a correct
  answer would even be.
- **Out of Layer-1 scope** — needs live transaction/deployment/telemetry data (Tier-2/Tier-3),
  which the documentation Brain deliberately does not hold.
- **`EXPECTED_UNVERIFIABLE`** — the `expected_response` itself is wrong or unanswerable (a
  test-bank quality issue, not a Brain failure).

Report the excluded set separately with counts by reason, and score only the clean set. A rough
heuristic for "too short": fewer than ~4 meaningful words and no clear ask — but use judgment,
not just a word count; a short but well-formed question ("What does GRN stand for?") stays in.

### Rule 2 — A superset answer is CORRECT, not a hallucination
The Brain often answers **more comprehensively** than the terse ground truth. That is good, not a
failure. Grade on **informational equivalence of the important points**, not on length or format:

- If the answer **contains all the important/main points** of the `expected_response` and those
  points are **correct**, the answer is **correct** — even if the ground truth is only a *subset*
  of what the answer says.
- **Extra correct detail is never penalized** and is **never** a hallucination.
- **Hallucination = inventing new things that are not there** — asserting a fact (a name, code,
  value, relationship, rule) that is not supported by the Brain or the sources. Only *fabrication*
  counts. Before flagging a hallucination, try to **confirm the claimed fact is actually absent**
  from the Brain (grep/read) — if it's present, it's not a hallucination.
- This is **English-language semantic matching**, so be careful: paraphrase, synonyms, reordering,
  and different-but-equivalent phrasings all count as matches. Do **not** require verbatim string
  overlap. Conversely, a fluent answer that misses a *load-bearing* expected point, or gets one
  wrong, is not "correct" no matter how polished.

Put simply: **correct = (all important expected points present and right) AND (nothing fabricated)**.
Extra truth is a bonus; missing an important point is a miss; invented facts are the only
hallucination.

## The grading workflow

1. **Load & curate** the bank (Rule 1). Keep a clean set + an excluded set with reasons.
2. **Get the Brain's answer** for each kept question via `brain_chatbot` (two-tier: unlimited
   tool-rounds first, retry capped at 25 on error/limit). Capture `brain_answer` + `brain_sources`.
3. **Judge each answer** against `expected_response` on the **0–5 scale** (see
   [references/rubric.md](references/rubric.md)):
   `5` fully correct & complete · `4` complete, trivial omission · `3` core present, some
   specifics missing · `2` topic present, major specifics missing · `1` barely any expected
   content · `0` absent or incorrect. **Apply Rule 2 while scoring**: a superset answer whose
   important points match earns a 5 (or 4 for a trivial omission) — the ground truth being a
   subset does **not** cap the score.
4. **Derive the verdict**: `FULL = score ≥ 4`, `PARTIAL = 2–3`, `MISSING = 0–1`;
   `answerable = score ≥ 2`.
5. **Set the flags**: `hallucination` (bool — only true for fabricated facts, per Rule 2),
   `gap_present` (a *genuine Brain knowledge gap*, not a mere retrieval/surfacing miss), and the
   `gap_category` (see rubric).
6. **Aggregate & report** — FULL% / answerable% / mean score, plus the excluded set, gap
   categories, and any regressions vs the prior run.

## Grading discipline (do these while judging)

- **Judge on informational equivalence, not path/format.** The bank's `source_reference` cites an
  idealized `kb/<COMP>/layer*.json` scheme that does **not physically exist** in the delivered
  Brain (which holds the same content as markdown pages + JSONL registers + journey JSON). A
  "wrong file cited" is **not** wrong if the fact is present. Use the GT→Brain layer mapping.
- **Verify before you accept; refute before you fail.** Before accepting a claim as correct,
  confirm the fact is actually in the Brain (catches hallucination). Before marking something
  missing, actively try to *refute* the gap (grep `brain/`, read the cited pages) — many "gaps"
  are the chatbot picking the wrong page (`RETRIEVAL_ONLY`), not absent knowledge.
- **Check the Sources section.** A good answer ends with a **Sources** list of repo-relative
  paths it actually read, and cites component/activity/SP/status/slot codes **exactly**. Missing
  or fabricated citations are a real defect.
- **Honour the standing traps.** e.g. **GRN = Goods Return Note (return *to* supplier), not the
  receipt (GR)** — any answer conflating them fails, however fluent. **ARM cross-check**: claims
  sourced only from Application Reference Manuals (ARM = intended behaviour, possibly stale) must
  be verified against a non-ARM (SP-derived) source; on conflict the SP-derived layer wins.
- **Scrutinize functional-prose answers hardest.** Technical categories (API, UI, schema, CIM)
  score high; functional categories (entity relationships, error messages, SP chains, computation,
  reporting) are where imprecise-but-fluent answers slip through — grade those most skeptically.
- **Be aware of judge variance.** Borderline FULL↔PARTIAL calls carry grader subjectivity; when
  unsure, read the actual Brain page rather than guessing, and record one precise sentence of
  `gap_description` so a human reviewer can calibrate.

## What each graded record should contain
`id, score(0-5), verdict, answerable, brain_answer, brain_sources, hallucination(bool),
gap_present(bool), gap_category, gap_severity, correct_facts, missing_or_wrong,
suggested_resolution`. Plus, for excluded items: `excluded(true), exclusion_reason`.

Full rubric, gap-category enum, worked examples, and the bank layout are in the references:
- [references/rubric.md](references/rubric.md) — the 0–5 scale, verdict banding, gap categories,
  hallucination vs superset examples, the judge discipline in full.
- [references/question-bank.md](references/question-bank.md) — where the bank lives, its fields and
  facets, the train/validation/test splits, the historical scores, and known eval gaps.

## Report structure
ALWAYS produce:

```
# Layer-1 Eval — <run id / date>
## Curation
- kept: N   excluded: M  (by reason: too-short K, out-of-scope K, unverifiable K, malformed K)
## Headline (clean set)
- mean score X.XX/5 · FULL P% · answerable P% · hallucinations H (fabricated facts only)
## Breakdown
- by difficulty, by category/BPC
## Gaps (genuine knowledge gaps only)
- by gap_category, top items with one-sentence descriptions + suggested_resolution
## Regressions vs prior run
- any previously-FULL question now PARTIAL/MISSING (investigate — see reindex-brain Regression Gate)
```
