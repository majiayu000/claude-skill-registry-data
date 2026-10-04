---
name: auto-research
description: Use when running or designing a measured self-improvement loop on a YURI subsystem — "climb this metric", "optimize the resolver", "autoresearch", "improve X until the score goes up" — or when deciding whether a subsystem is loop-improvable at all. Also use before touching an evaluator, benchmark, or scorer while a loop is in flight.
triggers:
  - "/autoresearch"
  - "autoresearch"
  - "self-improvement loop"
  - "frozen evaluator"
  - "climb the benchmark"
scope: harness
invocation: workflow
---

# Auto-Research — measured self-improvement loops

Authority: `_SYSTEM/yuri-origin.md` → **Loop Discipline** states WHAT is required. This skill is the
operational HOW. It does not restate that doctrine and must not contradict it — on conflict, origin wins.

Harness-neutral. Claude Code, Codex CLI, OMP, and Cursor all run the same loop; nothing here depends on
one harness's permission layer (that is exactly the point of the enforcement ordering below).

Worked references in this repo: `_SYSTEM/eval/atlas-score.mjs` (navigation quality, hit@k over a 40-item
JSONL benchmark) and `_SYSTEM/eval/build-score.mjs` (build health, weighted components with `--runs=N`
median + variance for noise). Read one before writing a new scorer — the shape is already settled.

## The entry gate

**A subsystem is loop-improvable exactly when it has an immutable scorer.** No frozen benchmark → no
loop. Build the benchmark first, or do not run. Writing benchmark ground truth is an owner judgment; the
lane being measured does not get to author what counts as correct.

Before iteration 1, all four must hold:

1. A scorer exists as a separate artifact from everything the loop may edit.
2. The scorer is frozen (all four layers below armed).
3. The benchmark passes the construct-validity check.
4. You are on a scratch branch, not `main`.

## Construct validity — check before you trust a number

Verify the benchmark measures what the system **claims to do**, not merely something adjacent that is
easy to score. This is the expensive failure mode because it looks exactly like success: a reproducible,
defensible number answering the wrong question.

<!-- @anchor: v1 | failure: Atlas benchmark construct-validity miss, 2026-07-26 (all 40 items in _SYSTEM/eval/atlas-benchmark.jsonl are "what file does X?") | regression: this section + the entry gate -->

The Atlas case: every question in `atlas-benchmark.jsonl` asks "what file does X?", while Atlas claims
faceted region navigation. That metric can only ever reward a filename index. A genuine-looking negative
result meant nothing — the system was never asked to do the thing it exists to do.

Run these three, in order, on any benchmark before it gates anything:

- **Claim mapping.** Write the subsystem's claimed capability in one sentence. Map each question type to
  a clause of it. Unmapped clauses = untested capability; unmapped questions = you are measuring
  something else.
- **Leakage scan.** Grep question text for tokens of the expected answer's path. `q037` leaked
  "graduation ladder" → `alpha-factor-library/graduation.mjs` and produced a hit that proved nothing
  about retrieval.
- **Reachability check.** Can the system reach each expected answer *at all*? A coverage ceiling (the
  answer is not in the index) and a ranking failure (it is, but ranked low) are different diagnoses with
  different fixes. Conflating them sends the loop after the wrong knob.

**Keep unwinnable questions.** A question the system cannot answer is a mapped blind spot. Pruning to a
flattering set converts a diagnostic into a scoreboard.

## The four enforcement layers, ordered by universality

Order matters: layers 1–2 bind all four harnesses and every model. Layer 4 binds one harness and only
while it is loaded.

1. **`chmod 444` on the eval directory.** OS file mode. Binds every process, harness, agent, and script —
   nothing negotiates with the filesystem.
2. **The loop self-aborts.** Refuse to start, and re-check every iteration, if
   `git diff HEAD -- _SYSTEM/eval/` is non-empty. Cheap, deterministic, harness-independent.
3. **Git pre-commit hook** rejecting any commit touching the eval dir without an explicit unfreeze env
   var. Catches the drift that survives 1–2 (someone chmod'd back).
4. **Harness permission config** (Claude `settings.json` deny, Codex sandbox, etc.). A **bonus** layer,
   never load-bearing. A deny rule the other three harnesses never read is not enforcement — it is a
   note to one reader.

Never rely on layer 4 alone. That is the whole reason the ordering is written down.

## Verifier isolation

The scorer runs in a fresh process with **no access to the proposal, the diff, or the reasoning**. A
checker sharing the maker's context inherits its blind spots and rubber-stamps them. See the ISOLATION
RULE comment block at the top of `atlas-score.mjs` for the concrete contract: it reads the benchmark file
and the resolver's stdout, nothing else. If you find yourself wanting to pass "context about what
changed" into the scorer, stop — that urge *is* the failure mode.

## The loop

```
scratch branch → freeze (4 layers) → construct-validity check → baseline score
  ↓
propose ONE change → measure (fresh process) → keep if metric improved, revert if equal or worse
  → append iteration, knob, before, after, verdict to an append-only results log → repeat
```

**Single-knob mutation.** One change per iteration. Two knobs and the attribution of any gain is lost —
you learn the score moved, not what moved it, and the next iteration builds on a guess.

**Append-only log.** Never rewrite past entries. The log is the only record of which hypotheses died, and
a loop that can edit its history can launder a regression.

**Noise.** For a metric with run-to-run variance (tests, timing), take a median over N runs and report
variance — `build-score.mjs --runs=N` does this. A single run cannot separate a real regression from a
flake, and a loop that reverts on noise wanders.

## Legitimate vs illegitimate evaluator interaction

Same files touched, opposite epistemics. **The test: can you justify the change from theory or first
principles, without reference to which questions currently fail?** If the justification requires the
failure list, it is optimizing the evaluator.

| Legitimate | Fraud |
|---|---|
| Add IDF weighting derived from corpus statistics — principled, derivable before seeing any score | Twiddle constants until the benchmark passes |
| Fix a construct-validity defect by **adding** question types that test the claimed capability, removing no hard question | **Delete** the questions the system failed |
| Fix a leaking question so it stops giving away its own answer | Add a question shaped around what the system already does well |
| Version the scorer explicitly, re-baseline, and mark historical scores incomparable | Silently retune weights mid-run |

Any change to the benchmark or scorer ends the current run. Re-freeze, re-baseline, note the version
break in the log. There is no such thing as adjusting the ruler and keeping the measurements.

## When NOT to loop

- **No frozen scorer.** Build it first, or do the work by hand.
- **Behavioural or noisy metrics** with no stable ground truth ("does the output read better") — model
  opinion is not a measurement.
- **Fewer than ~25 benchmark items.** Thin benchmarks get exploited: a handful of items is memorizable,
  and one lucky item swings the score more than any real improvement.
- **The change is a one-shot fix.** A loop is for climbing a gradient, not for applying a known patch.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I'll just tweak the scorer to be more fair" | You are the thing being scored. Apply the theory test: if you cannot justify the tweak without naming which questions fail, it is fraud. <!-- @anchor: none — doctrinal, from yuri-origin Loop Discipline --> |
| "The benchmark is obviously wrong here" | Sometimes true — and it still ends the run. Fix it, re-freeze, re-baseline, mark the version break. Do not fix it and keep climbing. <!-- @anchor: v1 | failure: Atlas construct-validity miss 2026-07-26 | regression: Construct validity section --> |
| "This question is unwinnable so it should go" | Unwinnable = mapped blind spot, the most valuable item in the set. Removing it raises the number and lowers the information. <!-- @anchor: v1 | failure: Atlas construct-validity miss 2026-07-26 | regression: "Keep unwinnable questions" --> |
| "This hit proves retrieval works" | Check for leakage first. `q037` contained "graduation ladder" and the expected answer was `graduation.mjs` — the hit measured string overlap, not navigation. <!-- @anchor: v1 | failure: q037 answer leakage, atlas-benchmark.jsonl, 2026-07-26 | regression: Leakage scan --> |
| "I'll freeze it after I get a good baseline" | The baseline is the measurement most worth trusting and the one you just took with an editable ruler. Freeze first, always. <!-- @anchor: none — doctrinal --> |
| "Component tests passed so the pipeline works" | Green-in-isolation says nothing about the seam. `atlas-regions.mjs` never read `edges.json`; both sides were fine and the pipeline was not. Test the connection explicitly. <!-- @anchor: v1 | failure: atlas-regions.mjs / edges.json seam miss, 2026-07-26 | regression: this row + Track-B "dispatch the seam, not just the parts" --> |
| "One harness enforces it, that's enough" | Harness config is layer 4. Codex, OMP, and Cursor never read Claude's `settings.json`. Layers 1–2 or it is not frozen. <!-- @anchor: none — structural, from yuri-origin Loop Discipline layer ordering --> |
| "Two knobs, but they're independent" | Then run two iterations. Independence is a claim; the log records only that the score moved. <!-- @anchor: none — doctrinal --> |

## Red flags — STOP the run

- About to edit anything under `_SYSTEM/eval/` mid-loop
- Justifying a scorer or benchmark change by naming which items fail
- The score improved and you cannot name the single knob that moved it
- Running on `main`
- The scorer is being handed the diff, the proposal, or "context"
- Baseline taken before the freeze
- Rewriting or pruning past entries in the results log

Any one of these: revert to the last logged good state, re-freeze, re-baseline.

## Provenance

The loop pattern (frozen evaluator, propose→measure→keep-or-revert, single-knob mutation, append-only
log) is adopted from the publicly discussed autoresearch pattern as an unprotectable idea. `karpathy/
autoresearch` carries **no license** (GitHub API returns `license: null`) — all rights reserved. No text
from that repo is copied or closely paraphrased here or in `_SYSTEM/eval/*`; the wording, vocabulary, and
enforcement model are YURI's own.

## Session Notes

**2026-07-26** — Skill authored. Tools: Read/Grep over `_SYSTEM/yuri-origin.md` (Loop Discipline),
`.claude/rules/skill-creation.md`, `skills/writing-skills/SKILL.md`, `_SYSTEM/eval/atlas-score.mjs`,
`_SYSTEM/eval/build-score.mjs`, `_SYSTEM/eval/atlas-benchmark.jsonl`. Verified locally before citing:
q037 leakage (grep of the benchmark line — question text contains "graduation ladder", expected path
`graduation.mjs`); the seam miss (`edges.json` referenced only by `atlas-edges.mjs`, the writer —
`atlas-regions.mjs` never reads it). Corrections: none. Errors: none. Notes: `/autoresearch` alias file
created at `.claude/commands/autoresearch.md` per the skill-creation checklist step 2. No RED baseline
run yet — the rationalization table is anchored to the 2026-07-26 Atlas findings, not to subagent
pressure-test transcripts; a baseline run per `writing-skills` RED-GREEN-REFACTOR is the open item.
