---
name: jev-judgment-design
description: "Design how a closed LLM judgment (relevance, novelty, evidence strength) moves to TypeSafe Jev. Use when replacing an LLM judgment with Jev, or when a Jev judgment lets everything through. For Jev's API and primitives, use typesafe:typesafe-ai first."
user-invocable: true
origin: shimo4228
---

# Jev judgment design

Jev answers closed questions with probabilities and does not write prose. Moving an LLM pipeline's judgments to Jev makes them cheap
and parallel, but Jev answers only within the state it is handed. This skill owns the design of that state and of the side that
decides accept/reject from the answers. The general design guidance for Jev (state / instructions / criteria, choosing Choice, Noul,
or Score, no-match, set thresholds on your own data) is canonical in plugin skill `typesafe:typesafe-ai`, so read that
first and read only the judgments layered on top here.

Sources: the implementation in jev-research-pipeline (https://github.com/shimo4228/jev-research-pipeline) and the article
"Moving the research judgments I left to an LLM to Jev, a judgment-only model"
(https://zenn.dev/shimo4228/articles/jev-research-judgment-offload).

## 1. Move only closed judgments

Move to Jev the judgments whose answer can be stated as a yes/no probability, one pick from a set of options, or a point on a graded
scale. Keep work with an open-ended answer shape, such as where to search next or how to write, with the LLM. After the move, watch the
instrument "number of LLM judgments during a run", not "number of questions to Jev" — Jev's question count may grow by as many
judgments as were moved.

## 2. Put what the judgment is made against into state

"Is it relevant" lets through anything that shares vocabulary when the comparison target is not in state. Jev is answering exactly
what it was asked, so the fix belongs in state, not in the question. Make the comparison target **the question that theme is currently
seeking an answer to**, and pass scope, exclusions, and already-accepted evidence along with it.

```python
state = {
    "question": {
        "title": question.title,        # the question currently seeking an answer
        "brief": question.brief,        # scope
        "evidence": question.evidence,  # what counts as evidence
        "not": question.negative_topics,  # topics that overlap in vocabulary but are out of scope
    },
    "source": {"title": ..., "url": ..., "excerpt": ...},
    "evidence_set": accepted_claims,    # evidence already accepted for this question (the baseline for novelty)
}
```

- In `not`, list the neighboring topics that are especially easy to confuse (e.g. "alignment training of a model alone" for a question
  about intent alignment — most sources with alignment in the title were vocabulary matches such as cross-modal alignment)
- Ask about novelty as "what does it add to `evidence_set`", not "is it new for this theme"

## 3. Put "only shares vocabulary" at the bottom tier of a Score

When asking about closeness on a graded scale, put "a different problem that only shares vocabulary" at the very bottom. Without this
tier, Jev has no choice but to pull toward a nearby tier.

```python
class Overlap(UseEnumMemberDocstrings, IntEnum):
    other_problem = 0
    """It works on a different problem that happens to share vocabulary."""
    same_field = 1
    """Same field as `question`, but not the problem `question` asks about."""
    same_problem = 2
    """It works on the problem `question` asks about, from another angle."""
    same_question = 3
    """It asks what `question` asks and reports an answer to it."""
```

Measured (2026-09-23, 3 sources with "intent" in the title against one question): they split into other_problem at 0.60 /
same_field at 0.53 / same_problem at 0.77. Even with the same vocabulary, the tiers separate once placed next to the question.

## 4. Jev answers, code decides

Accept/reject is decided not by Jev's output but by code applying thresholds.

- **Separate the cutoff (gate) from the ordering (placement).** Use Noul probabilities (is it relevant, is the method usable, does the
  evidence type fit) only for the cutoff; they can only drop things. Use the weighted Score tiers for ordering and the acceptance line.
  Mixing the cutoff into the weighting lets a strong tier compensate for a weak cutoff
- Measured (2026-09-23): a source at tier same_problem 0.77 had a relevance probability of 0.44, fell short of the 0.5 cutoff, and was
  rejected. Treat the tier and "is it relevant" as separate answers

## 5. The unit of judgment is "1 source × 1 question"

- A design that asks about each sentence in isolation loses context and inflates the question count by the number of sentences (a real
  case: 20,000 questions and a 283 KB report for one run on one theme). Make the unit one source
- Split into 2 stages: first, per source, ask cheaply in 1 request whether it "seems relevant" to every question, to narrow the
  candidates. Ask in detail only about the remaining "source × question" pairs. Judgments that need a sentence unit
  (does this sentence advance the question, does the source really say that) are done only within accepted sources, and whatever can
  be matched as a string is matched by code first

## 6. Place sources that must pass (canary)

Even if narrowing reduces volume, volume alone cannot tell you whether sources that should have been read were dropped too. For each
question, place a few sources known to be "must pass", and record on every run whether they passed. If a canary drops, suspect state
(`brief` / `not`) before the thresholds.

## 7. Calling from Pydantic AI

Pydantic AI's TypeSafe model (as-of 2026-09-23, https://pydantic.dev/docs/ai/models/typesafe/):

```python
from pydantic_ai import Agent

agent = Agent("typesafe:jev-1.13.0", output_type=Answers)
run = await agent.run(json.dumps(state, ensure_ascii=False, sort_keys=True))
dist = run.response.provider_details["probabilities"]
```

| Output type field | Jev primitive |
|---|---|
| `float` (`ge=0, le=1`) | Noul (probability of "yes") |
| `Literal[...]` / string Enum | Choice |
| `IntEnum` with docstrings | Score |

- Pin the version (thresholds were tuned against that version). Check in code that `run.response.model_name` matches the pinned
  version
- Read probabilities and distributions from `provider_details`; do not decide accept/reject from the rounded values in `run.output` alone

## 8. Keep searching and writing with the LLM, and swap models by string

If the LLMs used during a run are also called from the same `Agent`, you can swap only the writing model or the search-query model with a
single string, without changing the judgment types. Things that only need to be produced once before a run, like questions and search
queries, can be written outside the run by a strong model (Claude etc.) and stored in files, removing them from the LLM calls during
the run.
