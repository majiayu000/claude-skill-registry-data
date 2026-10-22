---
name: author-calibrated-eval
description: "Polish LLM-written prose with the author's own reading as ground truth."
user-invocable: true
disable-model-invocation: true
origin: shimo4228
---

# Author-Calibrated Eval

The ground truth for whether generated prose is "worth reading" lives in the eyes of the person who reads it (the author).
Build the loop on that premise. Split the roles three ways.

| What is checked | Who checks it |
|---|---|
| Readability and reading value (taste) | **The author**'s blind side-by-side read |
| Faithfulness (things not in the materials, comparison target, qualifiers, substituted subject) | **LLM judge**. A cutoff of binary checks |
| Format (position of citation marks, presence of markers, character count) | **Code** |

Asking the LLM judge for a holistic readability verdict does not make it a substitute for the author. Measured
(2026-09-23, jev-research-pipeline): even with a rubric that stated explicitly "having more information is not a reason to win",
the Opus judge picked the more information-dense version as "easier to understand" in both orderings, while the author called the short
version "very easy to understand" and the information-dense version "hard to read". On the other hand, the judge caught, in both orderings,
a substituted comparison target that the author had not noticed while reading.

## 1. Fix the materials

- Fix, one case at a time, the input used when the actual output was produced (that day's full set of materials). If the materials
  include third-party original text, store them in a private location, not in a public repo
- Assign each case to dev or holdout. Derive the assignment from the case id alone (so that when the number of cases grows later,
  no case moves between dev and holdout)
- Give the writer, the judge, and the author the same materials. If only the judge is shown a trimmed excerpt,
  it will wrongly flag facts the writer legitimately used as "not in the materials"

## 2. Have the author do a side-by-side read first (before running the judge)

Before running the judge loop, have the author read once. Skip this and you keep polishing the prompt to fit the judge
without noticing the gap between the judge's criteria and the author's.

- Line up 3 drafts per case: the current output / a candidate / **a strong model's reference draft** (same instructions, same materials).
  Hide which is which, vary the order per case, and keep the mapping in a separate file
- Ask the author only 2 things: "Which one is best?" and "Why (in a word)?". Accept "all of them are bad" as an answer
- Use how the reference draft is read to isolate the cause
  - The same complaint arises even with the strong model → the cause is how it is being asked to write (instruction framing, how
    materials are passed). Switching models will not fix it
  - Only the strong model is good → the cause is the model. Decide which model to use before polishing the prompt
- The author's one-word comment becomes, as is, material for the next instructions and rubric (e.g. "my eyes glaze over", "it skips
  explaining the premise", "the odd disclaimer is off-putting")

## 3. Iterate on a hard-case set, widen at milestones

- From dev, pick **one case per failure type** to form the hard-case set (e.g. overclaiming an interpretation / linking separate
  results causally / misaligned citation numbers). Run each iteration on just these few cases
- Each time a candidate is ready, check it on the hard-case set: the judge's cutoff → the author reads one draft per case
  (asking only "is it readable?" and "where did you stop?")
- Once a candidate passes both the author and the cutoff on the hard-case set, have it write **a few cases of different types from
  holdout**, and check them with the cutoff and the author's reading. This is the stage that checks whether polishing tuned to the
  hard cases also holds on materials it has not seen
- The axes of variants are instructions × model × materials (thickness) × a second self-check pass. The polishing work may run on a
  model with a free tier separate from production

## 4. The cutoff judge

Build the judge following the pattern in skill: llm-as-judge (binary checks, a one-line rationale, a single fatal No
means fail, no numeric scoring or aggregation). Only the points that worked for this use are listed here.

- **What to check**: what a number actually means (what it is a number of) and its comparison target / preservation of the original's
  qualifiers ("can ~", "in many cases") / not writing a design intent as a result / substitution of the research subject / content
  not found in the cited source
- **Check with code before judging**: position of citation marks, presence of markers, character count. Show the judge those results
  as fact lines. If the code check misjudges, the judge's cutoff is dragged along with it, so after fixing a check, re-run it on the
  existing drafts before passing them to the judge
- **Judge one draft at a time**: the cutoff is pass/fail, so judging each draft individually is enough
- **Keep the judge light**: define a dedicated agent that holds only Read / Write. A general-purpose subagent loads every tool
  definition and all always-loaded rules on each launch, so one judgment cost about 85k tokens, versus about 25k tokens with a
  dedicated agent (measured 2026-09-23). Write output to a location that session can write to (e.g. the scratchpad)

## 5. Extract writing principles from the author's reading

Translate the author's one-word comments into instruction principles. Examples of translations that worked in the 2026-09-23 loop:

| Author's comment | Principle added to the instructions |
|---|---|
| My eyes glaze over / it skips explaining the premise | Write as an explanation for a reader who has not read the paper. For each study: "problem tackled → what was done → what was found". Rephrase technical terms at first use |
| Lots of information but hard to read | Narrow the takeaway facts to 1–2 per study (what mattered was the number of facts and proper nouns, not sentence length) |
| The odd disclaimer is off-putting | Drop disclaimers like "this is not a study that dealt with it directly"; show the research subject within the explanation |
| So short I worry it doesn't capture the substance | At least one sentence for each of the 3 elements per study; set a lower bound on total character count |

After adding a principle, always check whether the cutoff surfaces a new type of breakdown. The more plainly you rephrase, the more
qualifiers drop out and the text drifts toward assertion ("can ~" → "does ~"). A factual breakdown inside readable prose is invisible
to the reader.

## 6. Recognize trivial evaluations

The following comparisons do not measure improvement.

- **Beating a weak baseline**: compare a list of short paraphrases with a fully explained version and the latter wins. A comparison
  against something any rewrite would beat does not show whether things got better
- **Compliance with rules you wrote yourself**: a rising pass rate on the cutoff shows the writer can now follow instructions,
  not that the reading value went up
- **Comparisons with no difference**: if most axes are ties, little can be learned from that comparison
- **Differences the same size as judgment variance**: if the same draft flips pass/fail by ordering or run, do not read it as a
  difference between versions

When in doubt, having the author read one case gets you closer to the right answer faster than running the judge dozens of times.

## Reference example

jev-research-pipeline (2026-09-23): `src/jev_research_pipeline/pipeline/prose_bench.py`
(`jrp prose export|bench|read|gate` — fixing materials / drafts / blind side-by-side reads for the author / per-draft
cutoff), cutoff checks `docs/prose-rubric.md`, judge `.claude/agents/prose-judge.md`,
prompt history `bench/prose/prompts/`, procedure in the same repo's `AGENTS.md` section 「本文を磨く」 ("polishing the body
text"), background in `docs/design/pipeline-design.md` section "Prose bench".
