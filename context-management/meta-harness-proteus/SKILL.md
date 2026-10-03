---
name: meta-harness-proteus
description: Run one iteration of proteus memory-summary evolution. Called by meta_harness.py.
---

# Meta-Harness — proteus memory-summary evolution

Run ONE iteration. Do all work in the main session — do NOT delegate to subagents.

**You do NOT run benchmarks.** You analyze prior results, prototype a mechanism,
and write new candidate summary compressors. The outer loop (`meta_harness.py`)
scores them on (fidelity, chars) separately, with no model and no network.

## What a candidate is

A summary compressor: it turns one campaign-memory record (a dict — see
`corpus.py`) into the short string injected into the policy's context on
retrieval. The proteus analog of a memory system. The grading is in
`corpus.py::score_fidelity`: the fraction of load-bearing facts (target,
surface, strategy, outcome, quality, difficulty, transfer hint) that survive in
your summary. Context cost = `len(summary)`.

## The objective

Preserve fidelity (>= the floor in `config.yaml`, currently 0.70 worst-record)
while using FEWER characters than `agents/baseline_incumbent.py`. The frontier
is Pareto: fidelity up, chars down. You cannot win by dropping facts — a summary
that loses a required fact loses fidelity and falls off the frontier.

## CRITICAL CONSTRAINTS

- Implement exactly **3** new compressors this iteration.
- Each must change a *mechanism*, not a constant. Bad: "same template, drop the
  organism." Good ideas: abbreviation/symbol encoding of fixed vocab
  (surface types, outcomes); a key:value micro-syntax instead of prose;
  dropping only provably-redundant words; reordering so the highest-value facts
  survive truncation; field-name elision where the value is self-identifying.
- **No record-specific hints.** Never hardcode a target name, campaign_id, or
  any value from `corpus.py` into a compressor. It must generalize to unseen
  records. (This is the anti-leakage rule — load-bearing for proteus.)
- Do not abort early or write "the frontier is optimal".

## Workflow

1. **Analyze.** Read `logs/evolution_summary.jsonl` (what's been tried),
   `logs/frontier.json` (current best), `corpus.py` (records + rubric),
   `agents/baseline_incumbent.py` (the system to beat).
2. **Prototype (mandatory).** Write a throwaway script in `/tmp/` that runs your
   compression idea over a couple of `corpus.py` records and checks fidelity by
   eye before committing. Delete it after.
3. **Implement.** For each of 3 candidates: copy `agents/baseline_incumbent.py`
   to `agents/<snake_name>.py`, subclass `SummaryCompressor`, implement
   `summarize(self, record) -> str`. Import from `candidate_base`. Self-critique:
   is this a new mechanism or just a tweaked constant? If the latter, rewrite.
4. **Validate.** `python -c "import agents.<name>; print('OK')"` from the repo root.
5. **Write `logs/pending_eval.json`:**

```json
{
  "iteration": <N>,
  "candidates": [
    {"name": "<snake_name>", "hypothesis": "<falsifiable claim about fidelity/chars>"}
  ]
}
```

Output: `CANDIDATES: <name1>, <name2>, <name3>`

## Interface

```python
from candidate_base import Record, SummaryCompressor

class MyCompressor(SummaryCompressor):
    def summarize(self, record: Record) -> str:
        ...   # pure, deterministic, no I/O, no LLM
```
