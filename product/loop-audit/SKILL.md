---
name: loop-audit
description: Audit whether the self-improvement loop is actually producing value and telling the truth about itself — convergence vs busy-work, claim substantiation against git, tech-tree accuracy, and owner-signal health. Use whenever the owner asks how the project management, tech tree, ledger, or improvement loop is doing; whenever you suspect the loop is polishing its own instrumentation instead of the product; before trusting a run of ledger claims; or when deciding whether the loop has converged and should stop. Complements the `singularity` skill, which RUNS cycles — this one JUDGES them.
---

# Auditing the loop

`singularity` runs improvement cycles. This skill asks the uncomfortable question:
**are those cycles worth anything, and is the record of them true?**

A self-improving loop that also writes its own report card has an obvious
failure mode. It will not announce itself. It looks like steady green cycles.

## Primary sources — go to these, never to a summary

| Source | What it is |
|---|---|
| `docs/agi/IMPROVEMENT_LEDGER.md` | one table row per cycle + a machine-readable `<!-- cycle:{...} -->` stanza |
| `git log` / `git show` | what actually changed, and when |
| `config/tech-tree.json` + `docs/agi/RESEARCH_BACKLOG.md` | the tree spec and the states it derives from |
| `data/agi-signals.jsonl` | every owner lightbulb request and its acknowledgement |
| `docs/agi/progress/repo-activity.json` | per-repo commit lanes |
| `tools/agi/cycle-metrics.js`, `tools/dev/run-probes.js` | the loop's own instruments |
| `http://localhost:3184/api/status` | what the owner actually sees (GET only; do not restart the server) |

## The four questions

### 1. Is it compounding, or oscillating?

Parse every stanza and compute, over time — real numbers, not impressions:

- `verified_improvements` per cycle, and `cost_turns` per improvement
- `defects` caught pre-ship vs post-ship
- `scaffold_added` vs `scaffold_retired` — **is the system accreting faster than it prunes?**
- **reversals**: cycles that undid earlier work. Search for the same file or
  surface moved one way and then back. Oscillation is the busy-work signature
  the owner has explicitly forbidden.
- cluster the `second_order` lesson strings: how many **distinct** lessons are
  there really, versus the same lesson restated? A loop that keeps relearning
  one lesson is not compounding.

The blunt version of this question: **what fraction of cycles improved the
product, versus the loop's own instrumentation?** Report the ratio.

### 2. Do the claims survive contact with git?

Take a **stratified sample of at least 8 cycles** across the whole range — not
the most recent ones, which are freshest and best-behaved.

For each, check the row's claims and the stanza's `verified_improvements`,
`verification[]` and `defects[]` against `git log`/`git show` for that date and
those files. Flag:

- claimed work with no corresponding commit
- a `verification[]` entry naming a check that does not exist, or could not have
  passed at that time
- `defects: preship` where the defect was in fact found by the owner *after*
  shipping
- corrections folded in quietly instead of being labelled as corrections

**Report a rate, not anecdotes:** of N cycles sampled, how many had ≥1 claim you
could not substantiate. A rate is falsifiable; a story is not.

Known base-rate from a real audit: in one session an agent filed three framework
defects that were all later measured false, and wrote "21/21 probes" in a commit
when the run was 19 pass / 1 fail / 1 skip. Over-claiming here is not
hypothetical.

### 3. Does the tech tree tell the truth?

The test that matters: **if the owner clicks the most prominent `available` node
tomorrow, do they get real, valuable work?**

- any node marked available that is already done, already impossible, or a
  duplicate
- `grown` nodes that were never actually delivered
- `gated` nodes that do not say what the owner must decide
- prerequisite edges that are decorative rather than real
- staleness: when was the spec last meaningfully edited, against the cycle pace
- the available:grown ratio — is `available` a dumping ground that never drains?

### 4. Is the owner's lever connected?

From `data/agi-signals.jsonl`: total requests, still pending, acked; latency from
`at` to `ackAt` (median and worst); and — the one that matters — **did each ack
correspond to real shipped work?** An ack claiming delivery with no matching
change is the most serious finding this audit can produce.

Also check the standing rule that the agent acks its **own test clicks as test
clicks**, so they can never burn a real owner request.

## Method

Run it as a fan-out with an **adversarial verify pass** — one agent per question,
then a separate agent per material finding whose job is to *refute* it, defaulting
to refuted. Self-audit without an adversary reproduces the bias being audited.

Mark every finding `measured` / `source-read` / `inferred`. Reading code and
predicting behaviour is inferred. Prefer a finding marked *unclear* with a stated
test over a confident wrong verdict.

## Reporting

Lead with the answer to "is this working?", then the evidence. Include:

- what is **healthy** — an audit that only finds problems is not calibrated
- confirmed findings, ranked by consequence
- findings that were **refuted** during verification, and why (this is the
  calibration signal — an audit with nothing refuted probably did not try)
- for each recommendation, the measured axis and direction it would move

## The stopping condition

The loop must be able to *finish*. If every remaining item is polish, say so and
recommend stopping rather than inventing a next stage — a recursive improvement
process without a stopping condition manufactures exactly the busy work it exists
to avoid.
