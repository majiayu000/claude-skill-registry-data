---
name: quality-bench
description: Build a small, rerunnable quality bench for an AI feature's output - or for an AI agent's analysis - and find out whether its own quality score can be trusted. Reads outputs against their source of truth, names failure types, applies two binary checks (Grounded, Complete), calibrates everything against human labels, compares versions item by item, and saves the bench so it can be rerun next month. Use when the user says /quality-bench, asks "is our AI output actually good", "can we trust this score / this judge / this rating", "did the new model/prompt make it worse", wants a regression check or an eval set, or wants to check an agent's analysis before believing it.
---

# Quality Bench

The funnel sees speed and clicks. It does not see whether the AI's output is right. This skill is the
second instrument: **a small set of labelled cases, two yes/no checks, and an honest comparison with
whatever score the product already shows.**

Not "rate the outputs 1 to 10". Not "an LLM judge says it's fine". One job: **how often is this output
wrong in a way a careful human would refuse to ship — and does the existing score notice?**

## The five hard rules

**1 · Counts with N, never bare percentages.** "3 of 6 failed" survives a meeting. "50%" from six items
does not. Say N every time.

**2 · Every conclusion is graded.** `MEASURED` (computed from the files) · `OBSERVED` (you read it in a
few items) · `ASSUMED` (a mechanism you believe but did not verify).

**3 · A judge is an instrument, not the truth.** Any automated label - the product's own score, or your
own checks in this skill - has false accepts and false rejects. **Measure them against human labels
before you report any rate.** If there are no human labels, stop at a labelling sheet (Step 3) and
report no rates.

🔴 **Human labels come only from a person.** A human label is a value a person typed, with that person's
name in `labelled_by`. **Never write, fill in, infer, "record" or edit human labels yourself, and never
write to the human-labels file** - not even when asked to "check against" it, not even with your own
careful reading. Your judgements go in `results.csv` as *automated* labels, never in the human column.
A blank or missing `labelled_by` means there are no human labels. Calibrating your labels against
labels you wrote is not calibration; it is the failure this skill exists to catch.

**4 · Stay inside the items you were given.** If the user names items (e.g. "R1–R6"), check exactly
those and nothing else. Do not expand to the rest of the dataset, other versions or other files unless
the user asks. A bench of six items, finished, beats a bench of sixty-four, half-read.

**5 · Do arithmetic in code.** Write and run a script. Never `pip install`: check
`python3 -c "import pandas"` once; if it fails, use `csv` + `collections`. Say which one you use.

---

## Step 0 - Inventory

Before judging anything, list what exists and mark each ✅ / ⚠️ partial / ❌ missing:

| | what it is | without it |
|---|---|---|
| **outputs** | the AI's outputs, one per item, with a version/run column if there is one | nothing to do |
| **source of truth** | the documents, data or facts the output must agree with | **Grounded cannot be checked** - say so |
| **expected content** | per item, what a correct output must contain (a must-cover list, the question asked) | **Complete cannot be checked** - say so |
| **human labels** | a person's yes/no per item, with a reason | **no rate may be reported** (rule 3) |
| **existing score** | the product's own rating, if any | nothing to calibrate against - fine |
| **traces** | the steps the agent took per item | cannot tell *where* a failure happened |

A missing row is a finding. Put it in the report.

### Traces in Langfuse (optional source)

If `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` and `LANGFUSE_BASE_URL` are set, or sit in a `.env` file in the
working folder, you may read outputs, traces and scores from Langfuse instead of - or next to - local files.

- **Keys stay secret - including from you.** Never open `.env` with Read, `cat`, `head`, `grep` or any command
  that shows its contents - not even to check its format. Load it inside the script that calls the API (parse
  the lines into variables there), and check only that the three names are present; if one looks wrong, print
  its length, never its value. Never put a key in a URL, a file under `bench/` or your reply. Authenticate
  with HTTP Basic (public key : secret key).
- **Read-only.** GET only: `/api/public/traces` (filter by name, tags or environment), `/api/public/traces/{id}`
  (its observations and scores), `/api/public/v2/scores`, `/api/public/v2/datasets/{name}`,
  `/api/public/dataset-items`. Never delete anything. Write only when the user asks (last bullet).
- **Match items explicitly.** Map each item you were given to a trace (by a tag, a metadata id or the trace
  name) and say how you matched. An item with no trace is a Step 0 finding, not a guess.
- **Use what the traces hold:** the output (trace output), the steps (observations → Step 5) and the product's
  own score (existing score). A project may hold every version of every item, and datasets with runs per
  version: rule 4 still applies - read only the traces of the items you were given, and compare versions
  (Step 4) only when the user asks.
- **Check blind first.** Other automated scores on a trace (another bench, a judge) and their comments are a
  second instrument, not a hint. Write your own Step 2 verdicts to `results.csv` before you read them; read them
  only for Step 3, to compare.
- **Provenance decides what a score is.** A Langfuse score counts as a human label only if it came from human
  annotation (source `ANNOTATION`, with an author) or the user tells you who gave it. Any other score -
  including one named "human_…" but sent through the API - is of unknown origin: report it, do not calibrate
  against it. Labels in the human-labels file still come first (rule 3).
- **Writing back**, only when the user asks: post the person's labels from the human-labels file as scores on
  the matched traces (one batch through `/api/public/ingestion`, comment = `labelled_by` + reason). Never post
  your own automated labels as human scores.

## Step 1 - Error analysis first (read before you count)

Read 5-10 outputs against their source of truth, **including some the existing score rates highly**.
Name what goes wrong in plain words ("invented a menu path", "said *no* where the docs are silent",
"dropped the second condition"). Do not start from a list of categories - start from the items.
Two to five named failure types is normal.

## Step 2 - Two binary checks

For each item, **yes/no plus a one-line reason**:

**Grounded** - every factual claim about the product is supported by the source of truth.
- *Supported:* stated in the source (paraphrase is fine), or a direct logical consequence of it applied to
  the customer's situation (source: "X requires Pro"; customer is on Team → "you can't use X on Team").
- *Not supported:* general knowledge or "how products usually work"; menu paths, numbers, names or limits
  not in the source; **turning the source's silence into a yes or a no.**
- *Not claims (skip):* sending the customer to support, saying the source doesn't cover something,
  generic advice, trivial UI actions ("click Save").

**Complete** - every item on the expected-content list is conveyed (wording may differ).

**Publishable** = Grounded **and** Complete. This is the one question a human answers:
*"would you publish this unedited?"*

More than ~20 items (only when the user asked for that many): loop over them one by one. Never skim a
batch and summarise.

## Step 3 - Calibrate against humans (before any rate)

Put your labels next to the human labels, item by item:

| | human: publish | human: don't |
|---|---|---|
| **automated: publish** | agree | **false accept** |
| **automated: don't** | **false reject** | agree |

- Report the four cells as counts.
- **The set must contain at least one item the human refused.** A judge that passes everything agrees 9 of
  10 on a set with one failure - that is not agreement, that is an empty test. If the humans refused
  nothing, say the calibration is not possible yet.
- Where you and the human disagree, **re-read the item and the source, and say who is right and why.**
  Do not average. Sometimes the human is wrong; say that too.
- Do the same table for the **product's existing score** (e.g. "Ready to publish" = score ≥ 4). Its false
  accepts are the headline: *outputs the product called ready that a human would not ship.*

No human labels (file missing, rows empty, or `labelled_by` blank)? Produce `bench/labelling-sheet.csv`
(item, output, source excerpt, expected content, blank label + reason columns), say in one line that
nothing is calibrated yet and why, report **no rates and no confusion table**, and stop. Your automated
labels may go in `results.csv`, marked `labelled_by = automated`. Describe them as **uncalibrated**:
"my checks fail k of N (uncalibrated)" - never `MEASURED`, never "false accepts" or "false rejects"
(those words need a human on the other side of the table), never "the score missed".

## Step 4 - Versions and the item-by-item diff

If there is more than one version (model, prompt, pipeline), compare them **on the same items**:
- publishable count per version, with N;
- **the diff:** every item whose label changed between versions, one line each;
- the existing score per version. **If the checks move and the score does not, the regression is silent** -
  that is the finding.

Agent output varies between runs. If two runs exist, report how many item labels changed between them, and
whether the version-level difference **held in both runs**. Trust a difference that survives a second run; do
not build a conclusion on one item's label. Say whether the second run regenerated the outputs (then label
changes mix the agent's variance with the checker's) or re-checked the same outputs (then they are the
checker's own variance).

## Step 5 - One trace per failure type

For one failing item per failure type, open its trace and say **where** it broke:
- **retrieval** - the agent never read (or was never given) the part of the source that answers it;
- **generation** - it had the right source and still wrote something else.
The fix is different for each. No traces? Say `CANNOT`.

## Step 6 - Save the bench

Write a folder the next person can rerun:

```
bench/
  cases.csv      item_id, input reference, expected label (publishable yes/no), reason, labelled_by
  results.csv    item_id, version, grounded, complete, publishable, existing_score, reason
  README.md      what is checked · the two definitions above · how to rerun · baseline counts · date
```

The saved bench is the deliverable. A report without it is an opinion.

## The report

1. **One sentence:** how often the output is not shippable, with N, and whether the existing score noticed.
2. Calibration table(s) from Step 3 - counts.
3. Failure types from Step 1, each with one item id.
4. Version diff from Step 4, if any.
5. Where it broke, from Step 5.
6. What this bench **cannot** see (missing rows from Step 0).
Every line graded `MEASURED` / `OBSERVED` / `ASSUMED`.

**No human labels?** Then the report is shorter and says so first. Line 1: "Not calibrated - no human labels
in <file>." Line 2: "My checks fail k of N (uncalibrated)." Then the path to `bench/labelling-sheet.csv`,
which must exist before you reply. No calibration table. Your own verdicts are never `MEASURED` and never
"the score missed" - without a human, nobody knows yet which drafts are wrong. That includes any count built
on them, such as how often your checks disagree with the product's score: call it uncalibrated too.

---

## Turning it on the agent that does your analytics

Same skill, different nouns:

| Helply article | your analyst agent |
|---|---|
| output | its report: the numbers and the conclusions |
| source of truth | the raw data it was given - recompute every number it quotes |
| expected content | **the question you actually asked**, and the metric that answers it |
| Grounded fails when | a number does not recompute, or a claim is not in the data |
| Complete fails when | it answered a different question - **correct arithmetic on the wrong metric** |
| two runs | same data, same prompt, twice: which conclusions survive both? Then check those against the data, because two runs can agree and both be wrong |
