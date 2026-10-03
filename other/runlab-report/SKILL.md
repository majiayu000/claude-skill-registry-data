---
name: runlab-report
description: Render the full training overview — where the athlete stands, what the data supports, what it does not, and what to do next — as an audited HTML and Markdown report. Use when the user asks for "the big picture", "a full analysis of my training", "the runlab report", or invokes /runlab:runlab-report. Runs every analysis over the whole history, takes minutes and writes files, so only the user starts it.
allowed-tools: Read, Write, Bash
disable-model-invocation: true
argument-hint: "[--since YYYY-MM-DD]"
---

# runlab report

This is the main deliverable. It is not a document you write; it is a document
the renderer assembles from three separate things:

| Part | Who produces it | What it holds |
|---|---|---|
| the **spec** | `scripts/report.py`, from its analysis catalogue | which numbers appear where, and which slots need a sentence |
| the **result files** | `scripts/report.py`, one per analysis it ran | the numbers themselves |
| the **interpretation store** | **you** | the sentences, each bound to the data it was written for |

The split is the mechanism. You cannot put a number in the report, because your
part of the file has no numeric fields. The renderer refuses to emit a number
that no result file contains, and it marks a sentence as stale when the data
behind it changed after the sentence was written.

Read `/runlab:runlab-methodology` first if it is not loaded. The evidence grades
below come from there.

## Standing rules

- Everything runs through the shim:
  `bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/<script>.py" [args]`
- Before relying on a flag, run the script with `--help`. If it disagrees with
  what is written here, follow `--help` and tell the user the skill is out of
  date. Never work around a missing script by computing the number yourself.

## Step 1 — the state of the data

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" --section computed
```

`read-db.py` always prints JSON; there is no `--json` flag. Useful sections,
each passable to `--section` (repeatable, dotted):

| Section | What it settles |
|---|---|
| `computed.activities` | how many runs, over what span, how old the cache is |
| `computed.gates` | per analysis: what it requires, what is there, what is short |
| `computed.comparison_base` | whether comparison against the athlete's own history is possible at all |
| `computed.data_quality` | channel coverage, always as `n` of `n_total` |
| `computed.anchors` | per anchor: `zone_statement_allowed`, `requires_uncertainty` |
| `computed.patterns_open`, `computed.tests_due` | what is open and what is overdue |
| `problems` | state files that failed validation — deal with these first |

Any gate whose `missing[]` is non-empty is a section the report will show as an
explicit gap rather than omit. `shortfall` is the number to quote: "three more
long runs", not "not enough data". This step is orientation — step 2 applies the
same gates itself and reports what it did with them — so skip it when the user
only wants the document.

## Step 2 — build the whole report in one call

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/report.py" \
  --lang de,en --out <data root>/reports --json
```

That one command is the whole pipeline: it walks the analysis catalogue, checks
each section's data precondition, computes the ones that pass, files every answer
as a result file, builds the spec, and renders HTML and Markdown per language.
`--dry-run` reports the plan without writing anything; `--list-sections` prints
the catalogue; `--sections <ids>` restricts it; `--since <date>` narrows the
window.

Exit codes: `0` a report · `1` a section whose gate opened could not be computed
· `2` **a number has no source** · `3` the render was not reproducible, or
`--strict-text` and a slot is unfilled · `4` misuse.

Read three things out of the payload, in this order:

| Field | What to do with it |
|---|---|
| `sections[]` | each carries `state` (`present` or `gap`), `reason`, `n`, `result_ids`, `missing[]`. Report the gaps to the user with their shortfall: "zones needs one heart-rate anchor" — never "not enough data". |
| `render.<lang>.audit` | `n_unresolved` and `n_literals` must both be zero. They are, or the exit code was 2 and something is wrong with the spec, not with your prose. |
| `interpretation.slots[]` | the sentences you owe. |

For a history-wide scan the report does not cover — hunting correlations,
proposing new patterns — delegate to the `runlab-history` subagent. It returns a
condensed proposal; the decision stays here.

## Step 3 — write the interpretations you owe

`interpretation.slots[]` lists every unfilled and every stale slot, and each entry
carries the payload that fills it. Merge the `store_fragment` objects into one
file, by convention `<data root>/reports/interpretations.json` (the `reports/`
tree is writable; `state/`, `profile.json` and `cache/results/` are not):

```json
{
  "interpretations": {
    "fatigue.decoupling.claim": {
      "en": {"text": "Efficiency holds until the second hour, then falls steadily.",
             "interpretation_for": "sha256:50e4248273..."}
    }
  }
}
```

- `text` is prose. It carries the meaning, not the measurement — **a digit in it
  is a number nobody can check**, and the audit reports it as one. The figures are
  substituted by the renderer from the result files.
- `interpretation_for` is the hash the slot entry gave you, and it is what makes
  the sentence go stale when the data behind it moves. Take it from the payload;
  do not invent it.
- A slot that sits on a finding card also carries `update_db_fragment`: the same
  sentence as a durable finding for `update-db.py`, already citing that card's
  result id and the metric keys the file really contains. Offer it in step 5.

Then run step 2 again with `--interpretations <store.json>`; the slots you filled
render as sentences and the rest still say what they are missing. Add
`--strict-text` when you want an unfilled slot to be an error rather than a
marker.

## Step 4 — when you need the renderer directly

`report.py` calls `render.py` for you. Reach for the renderer itself only to
re-render an existing spec — for example after editing the interpretation store by
hand:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" \
  --spec <data root>/reports/report.spec.json --root <data root> \
  --interpretations <store.json> --lang en --out <data root>/reports \
  --check --strict-text --verify
```

Its exit codes: `0` clean · `1` usage or input error · `2` **a number has no
source** · `3` an interpretation is missing or stale, or the render is not
deterministic. `--slots` lists slot keys and their hashes, `--bind <file>` fills
an empty `interpretation_for` (never one that differs).

Never remove `--check` to make a report come out. Exit 2 means the document
wanted to state something no analysis produced, and the fix is to run the
analysis or drop the claim. The audit block names each one under `unresolved[]`
with the `result_id` and the metric path it wanted.

## What the finished report must contain

1. **Masthead** — the data basis in one line: number of runs, date range, how
   many carry mechanics, how many carry heart rate, and a single as-of stamp.
   Never mix two.
2. **Key tiles** — the steering numbers, each with its uncertainty.
3. **Finding cards** — status tag (`established`, `provisional`, `no effect`),
   one bold claim, the reasoning, an is-versus-target line **naming the origin of
   the target**, and a statistics line with effect size, `n` and `p`.
4. **Null findings as their own cards.** A measured absence of an effect is a
   result, and the one most often lost. Grey tag, explicit "no action needed".
   A section that quietly omits what was tested and found flat reads as if it
   had never been tested.
5. **Hypotheses** — everything at p ≥ 0.05, each with the observable that would
   decide it.
6. **Limits** — every extrapolation, every soft anchor a conclusion leans on,
   every capability the source cannot deliver.

## Step 5 — offer the state update, do not perform it

The report is a rendering; it is not the database. Findings that should survive
the session go in through `update-db.py`, and only with the athlete's agreement.
Show the payload, then run the writer. Payload rules are in
`/runlab:runlab-methodology`.

## Rules that decide whether this report is worth anything

- **Cite, never compute.** Enforced by `--check`, but hold to it in your own
  prose too: a sentence that carries its own number bypasses the mechanism.
- **One denominator per claim.** "Cadence is low" is an opinion; "cadence below
  target in 9 of 14 easy runs" is a finding.
- **A soft anchor contaminates everything downstream.** If
  `computed.anchors.<key>.zone_statement_allowed` is false, no sentence may name
  a zone without saying the boundary is provisional.
- **The remainder block is reported separately, always.**
- **Do not smooth the story.** If two analyses disagree, print both and say so.
