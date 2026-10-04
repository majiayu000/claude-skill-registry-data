---
name: autoresearch
description: Runs autonomous keep/discard experiments on a codebase to optimize a single metric for a fixed duration, in the style of karpathy/autoresearch. Use when the user says "autoresearch" (optionally with a focus, e.g. "autoresearch the optimizer"), asks to run experiments on a repo overnight, to hill-climb or optimize a metric autonomously, or points at a repo with a karpathy-style program.md.
---

# Autoresearch

Metric-gated experimental research on a codebase for a fixed duration.
Subagents propose and run experiments. The metric decides what survives.
The clock decides when to stop. You decide neither.

```
Setup ──► clock check ──► dispatch ONE experiment ──► verify ──► gate ──► log ──┐
              ▲                                                                 │
              └──────────────────── time remains ───────────────────────────────┘
              └── deadline passed ──► confirm best ──► final summary
```

## Role and Iron Laws

You are the **orchestrator**: manage the clock, dispatch subagents, verify
results, gate outcomes, keep the ledger. All experimental work — designing
changes, editing code, running training/benchmarks — happens inside subagents.

```
1. THE CLOCK DECIDES WHEN TO STOP. NOT YOU.
2. THE METRIC DECIDES WHAT SURVIVES. NOT YOU.
3. ONE EXPERIMENT IN FLIGHT AT A TIME. NEVER PARALLEL.
4. EVERY FACT YOU NEED LIVES IN THE LEDGER FILES, NOT IN YOUR HEAD.
```

Law 3 deliberately deviates from the parallel-subagent pattern of sibling
skills: experiments mutate shared state (one working tree, one branch, one
compute resource). Parallel dispatch corrupts the protocol. Dispatch each
subagent **blocking** (foreground) and wait for its result.

Law 4 is what lets a run survive 100+ experiments: your context will be
compacted or reset overnight. See **Resume**.

Degrees of freedom are split on purpose:
- **Hypothesis selection is free.** Subagents choose what to try; you and they
  may be ambitious, radical, creative — anything inside the focus and scope.
- **The protocol is fixed.** Verify, gate, and log exactly as written below.
  No judgment calls except the simplicity criterion.

**No subagent tool in this harness?** Run the dispatch template yourself, one
experiment per iteration, and still run Verify and Gate as a separate step
afterwards — never trust the number you just produced without re-extracting
it. Re-read the ledger TSV before every hypothesis instead of remembering it.

## Inputs

| Input | Required | Example |
|---|---|---|
| Target repo | yes | `~/code/autoresearch` |
| Metric + direction + extraction | yes | `val_bpb`, lower is better, `grep "^val_bpb:" <log> \| awk '{print $2}'` |
| Experiment command | yes | `uv run train.py` |
| Time budget per run | yes | 5 minutes wall clock |
| Mutable scope | yes | `train.py` only |
| Duration | yes | "overnight" = 8 hours |
| Frozen scope | recommended | `prepare.py`, evaluation code, dependencies |
| Noise floor | recommended | run-to-run spread of the metric, e.g. `0.002`; unknown → measured in setup |
| Cost tolerance | optional | `peak VRAM may not exceed baseline by >10%` + its extraction command |
| Holdout command | optional | a second eval on data the loop never sees; run once, at the end |
| Byproducts to clean between runs | optional | `checkpoints/`, `__pycache__` |
| Research focus | optional | "attention variants", "the optimizer only" |
| Run tag | auto | date-based, e.g. `sep23` |

The extraction command must print **one number and nothing else**; write it
so it reads a log path (`<log>`), not a fixed filename.

**Research focus** — a free-form directive from the user's prompt: a component,
an idea family, a constraint, or a hunch. It bounds hypothesis selection in
every dispatch; it never changes the gate. Record it verbatim in the ledger.

**Native mode** — if the target repo contains a karpathy-style `program.md`,
read it first and adopt its mechanics (metric, commands, scopes, budgets)
verbatim. Two things always follow this skill instead: logs and the ledger
live in `/tmp` (see Setup), and the orchestrator gates, not the subagent.
A user-stated focus overrides its open-ended charter for choosing hypotheses.

**Metric integrity** — the code that computes and prints the metric must sit
in the frozen scope. If the user's scopes leave it mutable, flag it and get
the scopes corrected before starting: experiments that can touch the metric
computation produce incomparable numbers. The same applies to the eval data:
if the mutable scope can choose or filter what the metric is computed on,
that selection is frozen too.

**Oracle, not claim** — a subagent's reported number is a claim; the
extraction you run yourself is the oracle, and only the oracle feeds the
gate. A model grading its own run (self-score, LLM judge in the mutable
scope) is never the metric. No deterministic extraction exists → this skill
does not apply; say so instead of climbing on vibes.

If required inputs are missing and no `program.md` supplies them, ask the user
once, up front, for everything at once. After setup, never ask again.

## Setup

Track this checklist:

```
- [ ] 1. Clock: date +%s, deadline computed, run count estimated
- [ ] 2. Branch: fresh autoresearch/<tag> from current HEAD, tree clean
- [ ] 3. Ledger TSV + progress file created in /tmp
- [ ] 4. Baseline recorded as best; extraction proven; noise floor set
- [ ] 5. Executor pin recorded
```

1. **Clock.** Record start timestamp and deadline. Runs available ≈
   duration ÷ (per-run budget + ~2 min overhead). Fewer than ~5 → tell the
   user now; the run will mostly measure noise.
2. **Branch.** `git -C <repo> checkout -b autoresearch/<tag>` from current
   HEAD. Must be fresh — if the branch exists or the tree is dirty, stop and
   tell the user. Every git command in this run uses `git -C <repo>` — never
   rely on cwd. This skill never runs `git reset --hard`, `git clean`, or
   `git stash` (the stash stack is shared with every other worktree).
3. **Ledger.** Everything lives in `/tmp` — never inside the target repo, so
   no reset, checkout, or subagent commit can ever touch the record.
   `<L>` = `/tmp/autoresearch-<tag>-<timestamp>` is the prefix for all of it:
   - `<L>.tsv` — the ledger TSV, header row, tab-separated:
     `n	commit	<metric>	cost	status	description`
     — status is `baseline`, `keep`, `keep (simplicity)`, `discard`,
     `discard (noise)`, `discard (scope)`, `discard (cost)`, or `crash`;
     cost is the cost-tolerance value if declared, else `0`. Crashes log
     metric `NA`, never a number. **The ledger TSV is the source of truth**:
     current best = the last `baseline`/`keep`/`keep (simplicity)` row.
   - `<L>.md` — progress file: goal, focus (verbatim), metric spec,
     commands, scopes, noise floor, start, deadline, executor pin, a
     `## Queue` of untried hypotheses, and an `## Experiments` section.
     Narrative mirror — when it disagrees with the TSV, the TSV wins.
   - `<L>-exp<N>.log` — one run log per experiment (`-exp<N>b.log` for a
     confirmation re-run). Logs are never overwritten, so crashes need no
     copying and every number stays re-checkable.
4. **Baseline.** Dispatch a subagent to run the experiment command
   **unmodified** into `<L>-exp0.log`, `<L>-exp0b.log` and, if one run is
   under ~5% of the duration, `<L>-exp0c.log`. Extract each yourself: every
   extraction must print exactly one number — if not, fix the extraction
   command with the user now; this is the last moment you can.
   - Best = the median of the baseline values (two runs: their mean).
   - Noise floor (if not given) = max − min of the baseline values. `0`
     means the harness is deterministic: any strict improvement wins and no
     confirmation runs are needed.
   - Record row `0` in the TSV (`baseline`), and best + noise floor in the
     progress file.
   - Baseline crashes: fix-dispatch up to 3 times (fixes limited to the
     mutable scope — anything else escalates immediately), then escalate —
     there is no run without a baseline.
5. **Executor pin.** Record host and hardware in the progress file. If the
   run moves to another machine, re-run the baseline and start a new best —
   numbers do not transfer across executors.

Setup is the only phase where user interaction is allowed. Afterward the loop
runs lights-out until the deadline.

## The Experiment Loop

Before **every** dispatch: `date +%s` vs deadline. Remaining time less than
one per-run budget → Final Summary.

### 1. Dispatch

One subagent, blocking. Strict template — fill the brackets, keep the
structure:

```
You are running ONE experiment in an autonomous research loop.

Repo: <path>, branch autoresearch/<tag>, currently at the best-known commit.
Mutable scope: <files>. Frozen scope: <files> — read, never modify.
Metric: <name>, <lower|higher> is better. Current best: <value>.
Noise floor: <value> — a gain smaller than this is not a gain.
Research focus: <verbatim focus, or "none: full mutable scope is fair game">.
Every hypothesis you consider must stay inside the focus.

Read <L>.md and <L>.tsv FIRST. They list every experiment already tried.
Do NOT repeat any of them, including failures — a discard is information,
not an invitation. Prefer the top untried item in the ## Queue, if any.

Your task:
1. Pick ONE untried hypothesis likely to beat the best by more than the
   noise floor.
2. Implement it in the mutable scope. Minimal, focused diff.
3. Commit ONLY mutable-scope paths: git -C <repo> add <files>, then
   git -C <repo> commit -m "<the hypothesis>". Never git add -A.
4. In ONE shell invocation, run and extract:
     cd <repo> && timeout -k 30 <2x budget> <experiment command> \
       > <L>-exp<N>.log 2>&1; echo "exit=$?"; <extraction command on that log>
   Never let run output into your context — redirect, then extract.
   exit=124 or 137 = timed out: treat as a crash.
5. Empty extraction = crash: read `tail -n 50 <L>-exp<N>.log` — never more,
   never `cat`. Trivial cause (typo, missing import): fix, commit, re-run
   once into the same log path. Fundamentally broken idea: stop and report.
6. Report the FINAL commit hash (git -C <repo> rev-parse HEAD), never the
   first one.

Return exactly:
- Hypothesis (one line)
- Commit hash
- Metric value (or CRASH + the last 5 error lines)
- One suggested next experiment based on what you observed

Do NOT decide keep-vs-discard, reset or move the branch, edit <L>.tsv or
<L>.md, or touch any file outside the mutable scope. The orchestrator gates.
```

Pass ledger **paths**, never contents. No deadline awareness for subagents.
Never paste "lessons from past runs" into the prompt as prose — the ledger
is the record, and the subagent reads it as data.

### 2. Verify

Never gate on the report alone. One shell call, no turns in between:

```bash
<extraction command on <L>-exp<N>.log>;       # the oracle value
git -C <repo> rev-parse HEAD;                 # must equal the reported commit
git -C <repo> status --porcelain;             # empty, apart from user-named byproducts
git -C <repo> diff --name-only <best>..HEAD;  # every path inside the mutable scope
<cost extraction, if a cost tolerance is declared>
```

- Oracle empty, or different from the reported number → the report was a
  hallucination: `crash`.
- HEAD ≠ reported commit → an unreported commit exists: `crash`.
- Uncommitted changes inside the mutable scope → the number measured code
  that is not the commit: `crash`.
- Any path outside the mutable scope, committed or dirty → `discard (scope)`,
  whatever the metric says.

### 3. Gate

Take the first row that matches. `margin` = improvement over best in the
metric's direction (positive = better); `floor` = noise floor.

| # | Condition | Status |
|---|---|---|
| 1 | Verify failed, run timed out, or no oracle value | `crash` |
| 2 | Path outside the mutable scope | `discard (scope)` |
| 3 | Cost tolerance declared and broken | `discard (cost)` |
| 4 | `margin > floor`, and `floor > 0` and `margin < 2×floor` | confirm first ↓ |
| 5 | `margin > floor` | `keep` |
| 6 | `margin ≥ −floor` and the diff removes code or cost | `keep (simplicity)` |
| 7 | `0 < margin ≤ floor` | `discard (noise)` |
| 8 | anything else | `discard` |

**Confirm (row 4).** Dispatch a subagent: "Run `<experiment command>` on
commit `<hash>`, unmodified, into `<L>-exp<N>b.log`, using the step-4 shell
invocation. Change nothing. Return the extracted value." Extract it
yourself. Re-gate with the **worse** of the two values, skipping row 4. One
confirmation run is cheaper than a false best that poisons every later
comparison.

**Simplicity (row 6)** is the one judgment call you own: equal-within-noise
metric, less code or cost. A marginal gain bought with disproportionate
complexity is a `discard`. In doubt, the metric wins.

**On any keep**: the branch stays; best = this commit and value.

**On any discard or crash**, in order:
1. Dirty tree? Preserve it as a commit, never a stash:
   `git -C <repo> add -A && git -C <repo> commit -m "wip exp-<N>"`.
2. `git -C <repo> update-ref refs/autoresearch/<tag>/exp-<N> HEAD` — the
   attempt stays reachable for morning review.
3. `git -C <repo> reset --keep <best commit>` — never `--hard`.

**Every experiment**: remove user-named byproducts so runs stay independent.

### 4. Log

Append one row to the ledger TSV, then one entry to the progress file:

```markdown
### Experiment N — <time>
- Hypothesis: <one line>
- Commit: <hash>
- Metric: <value> (best: <value>)
- Status: <status from the gate table>
- Suggested next: <from the subagent>
```

Add the suggestion to the `## Queue` if it is untried. Return to the clock
check.

## Resume

Context compacted, session restarted, or you lost track? Never guess:

1. `ls -t /tmp/autoresearch-<tag>-*.tsv | head -1` → the ledger; read it and
   its `.md` progress file.
2. Best = the last `baseline`/`keep`/`keep (simplicity)` row. N = last row + 1.
3. `git -C <repo> rev-parse HEAD` ≠ best commit → an experiment was
   interrupted before its gate finished. No TSV row for it yet → log it as
   `crash`. Then run the discard steps (they are safe to repeat).
4. Re-check the clock. Continue the loop.

## Stall Recovery

When subagents repeat themselves, propose trivia, or report "no ideas left":

0. **Replay the ledger first.** Keeps, discards, and crashes per hypothesis
   area are already in the TSV. Decide the next rung from those numbers;
   never spend a run to test a dispatch strategy.
1. **Dispatch an ideation subagent**: read the full ledger and both scopes,
   return 5-10 concrete untried hypotheses inside the focus — including
   combinations of near-misses (`discard (noise)` rows first) and radical
   structural changes. Write them to the `## Queue`.
2. **Escalate ambition.** Early experiments tweak knobs; later ones change
   structure. The ledger shows which rung you are on.
3. **Widen an exhausted focus.** If ideation returns nothing viable twice in a
   row, widen to the full mutable scope and log the widening loudly.
4. **Rewind sparingly.** Resetting best to an earlier commit to escape a local
   optimum is allowed but should be very rare. Log it loudly.

Running out of ideas is never a reason to stop.

## Preventing Premature Exit

Every one of these thoughts is a trap:

| Thought | Instead |
|---|---|
| "The metric has plateaued" | Not your call. Dispatch ideation. |
| "10 discards in a row — converged" | Discards are data. Change rung, dispatch. |
| "Good enough to show the user" | Only after the deadline. Check the clock. |
| "Remaining ideas are too radical" | Radical is the correct next rung. Dispatch. |
| "One more run won't matter" | Remaining time ÷ per-run budget = runs left. It matters. Dispatch. |
| "Let me inspect the training output" | No. Run the extraction. Nothing else. |
| "I should ask whether to continue" | The user is asleep. That is the point. |
| "I'll remember the best value" | You won't survive compaction. Read the TSV. |

Any variation of "maybe stop" → check the clock and dispatch again.

## Final Summary

Only after the deadline (let the in-flight experiment finish and gate it —
never kill it for the deadline):

1. **Confirm the branch** sits at the best commit (`git -C <repo> rev-parse
   HEAD` vs the TSV's current best).
2. **Re-measure the best** if any keep happened: one unmodified run into
   `<L>-final.log`. The best was selected from many noisy trials, so its
   logged value is optimistic; report both.
3. **Holdout**, if declared: run it once on the baseline commit and once on
   the best commit. This is its only use — a holdout the loop sees becomes
   training data.
4. Append to the progress file and report:

```markdown
## Summary
- Experiments: N total — K keeps, D discards, C crashes
- Baseline: <value> → Best: <logged value> (re-measured: <value>, noise floor <value>)
- Holdout: <baseline> → <best>, or "none declared"
- Branch: autoresearch/<tag> at <best commit>
- Kept changes: <one line each>
- Nearest misses worth a future run: <discard (noise) rows>
- Ledger: <L>.tsv, <L>.md
- Review: git -C <repo> log --oneline <base>..autoresearch/<tag>
          git -C <repo> diff <base>..autoresearch/<tag>
          git -C <repo> for-each-ref refs/autoresearch/<tag>/
```

Leave the branch checked out at the best commit. Never merge, push, or open a
PR — that is the user's morning decision. To publish a session record
(karpathy PR 44 style), the user can copy `<L>.tsv` into the branch.

## Red Flags — STOP and Reread This Skill

- You are editing a file in the target repo
- Two experiment subagents are running at once
- You gated on a metric value you did not extract from the log yourself
- A keep happened that is not a gate-table row 5 or row 6
- You typed `git reset --hard`, `git clean`, `git stash`, or any git command
  without `-C <repo>`
- A diff touched the frozen scope and you gated on the metric anyway
- `git status --porcelain` was non-empty and you dispatched anyway
- A run log or ledger file was written inside the target repo
- You are composing a message to the user before the deadline
- You have not run `date +%s` since the last subagent returned
- You stated the current best from memory instead of the TSV
- The run moved to another machine and you kept comparing against old rows
