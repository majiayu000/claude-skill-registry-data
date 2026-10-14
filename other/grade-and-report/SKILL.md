---
name: grade-and-report
description: Submit a draft (and optionally the prompt behind it) to Amdahl Eval, poll the queued run to a verdict, and report the result using Amdahl's own report card. Use after ground-and-draft, before anything publishes. Also covers A/B-ing two drafts on frozen evidence and taking a median of N to see past the noise.
---

# grade-and-report

The second half of the loop: (ground-and-draft) → **Grade → Fix**.

Submits to Eval, waits, and shows the **server-authored report card**.

## The one rule

**Paste the report card. Do not restate the numbers in your own words.**

`GET /eval-runs/{id}/report` returns finished markdown: the draft's score, the
rewrite's score, the bar, the transition, the customer quotes, and any caveat.
Show that block as written.

This is not a style preference. The eval reports two different artifacts — your
draft and a rewrite Amdahl generated — and the run's `pass` / `fail` bucket
follows the _rewrite_ while the score follows your draft. Summarising a run in
your own words is precisely where the two get merged, and the result is a
confident sentence about the user's copy built on a number that was never about
their copy. Live example: run `783c94c1` carries `overall_score: 1.0` for a
draft that passed **2 of 5** checks. The card says 2.6/5, 2 of 5. Your summary
would have said "scored perfectly".

`overall_score` was re-pointed at the submitted draft at `eval_version` 2.14.0,
so on a run at that version or later it IS your draft's grade — but on anything
older it is still the blend above, and the field gives you no way to tell which
you are holding except `eval_version`. The card and `report.headline.*` are
labelled on every run, which is why they stay the thing to read.

If you need a number in your own prose — to compare runs, to decide whether to
iterate — read `report.headline.*`, which is the same derivation the card
renders, so the two cannot disagree.

## Steps

1. **Build the inputs.** Message-only grades the copy. Add `prompt` to grade the
   instruction that produced it too — that is the half you can actually reuse.
   Add `audience` (e.g. `"VP of Marketing"`) and, when the account is in your
   corpus, `account`, to scope the evidence. Homepage/hero copy runs unscoped.

   You do not have to guess whether an account is in your corpus. Run without
   one and the verdict comes back with `requires_input` when scoping would have
   helped — naming the field and, when a company in your draft resolves against
   your own data, the exact value to re-run with and how many utterances sit
   behind it. Nothing is retrieved using that suggestion; it only takes effect
   when you send it.

2. **Grade.**

   ```bash
   export AMDAHL_KEY='...'              # Settings, then Developer, Create key
   bash scripts/grade.sh draft.md runs/2026-08-03-launch "" "VP of Marketing"
   ```

   Submits (with retries), polls to terminal, writes `scorecard.json` +
   `report.md`, and prints the card.

3. **Show the card.** `report.md`, verbatim, in the section order below.

4. **Read the two things worth reading — and skip the three that look
   readable.**
   - **The fraction, not the score.** `submitted.checks` — "2 of 5" — is the
     measurement; `score_15` is `1 + 4·(passed/total)`, a rendering of it. With
     five binary checks the dial has six positions, so an edit that does not
     flip a whole check is invisible in the number. If you iterate and the score
     does not move, you have learned you have not yet flipped a check.
   - **The quotes, especially a `contradicts`.** A customer arguing against a
     claim you hold is the highest-value output of the whole run. Escalate it;
     do not average it away.
   - **Not the Improved row, not `lift`, not `transition`.** The improved side
     is a rewrite the eval writes for itself, and its own field says so:
     `improved.usage` is `illustration_only`. Read it for the _wording_ it
     reaches for; do not read its number. Measured at eval_version 2.9.0 (n =
     89 runs / 40 distinct messages, one tenant): the improved side clears the
     4.2 bar on **92%** of them, so it is close to a constant — and because
     `lift` is `improved − submitted`, that makes `lift` **−0.90 correlated
     with your own draft's score** on that same run set. A big lift means your
     draft scored low, not that the rewrite added much. The noise-floor filter
     does not fix this: restricted to the runs where `lift_reportable` is
     `true`, the correlation is still **−0.88**. `transition` inherits the
     same problem — its first half is the submitted verdict by definition,
     and its second half is a 92% constant. **Use the submitted fraction. It
     is the only number on the card that is about your writing.**

     Bounds on the 92%: the same statistic read 71.0% at eval_version 2.7.0,
     on a message population that overlaps with but is not identical to the
     89-run 2.9.0 population above. The two readings are separate
     measurements taken at different versions on partly different message
     populations — not a controlled before/after of the same experiment — so
     do not read the difference between them as caused by the version bump.

     Re-taken at eval_version 2.15.0, and the property holds: over a 90-day
     window of 410 scored runs (one tenant, all message populations that
     workspace ran), `improved_mean_15` is **4.24** against the same 4.2 bar
     while `submitted_mean_15` is **2.38**. Read that as corroboration, not
     as a third value of the 92%: a mean is not a pass rate, and this is a
     different and larger population. What it establishes is the thing the
     92% was evidence for — the improved side still sits on the bar, three
     versions on — so the guidance above stands rather than needing a fresh
     correlation. The pass rate itself has not been re-taken at 2.15.0.

5. **Fix.** Apply the suggestions to the draft _and_ to the prompt, then re-run
   as a **new** run folder. Runs are immutable.

## Output contract

Fixed section order. Nothing between §1 and §2.

1. **The card** — `report.md` pasted verbatim. No preamble, no "here's how it
   did", no reformatting the table.
2. **What you changed, or would change** — your own words, about the _edits_,
   never restating a score.
3. **Anything a `contradicts` quote surfaced** — the belief, and the quote.
4. **What you ran** — run id, whether the evidence was pinned, and `reused`.

When a run comes back `not_applicable`, the card says so and says why; report
that. It is not a failing grade and must not be presented as one.

## A/B-ing two drafts

```bash
bash scripts/ab.sh v1.md v2.md runs/ab-hook "VP of Marketing"
```

Grades v1 fresh, grades v2 **pinned to v1's evidence**, and reports the delta
between the two **submitted** drafts.

> **Do not A/B on `compare.score_delta`.** It differences `overall_score`, and
> that field's meaning changed at `eval_version` 2.14.0: before it, the delta was
> mostly rewrite-versus-rewrite — on a live pinned pair whose true draft delta
> was **−0.8** (2.6 → 1.8), it reported **−0.167** — and a pair that SPANS that
> version differences two different quantities, which the endpoint does not
> check. `ab.sh` reads `report.headline.submitted.score_15` on each side instead,
> which means one thing on both sides of the line. `evidence_overlap` from the
> compare endpoint _is_ correct and worth reading — it tells you the pin held.

Pinning matters because a second search returns different quotes, so an
unpinned difference could be your edit or could be retrieval.

## One run is not a measurement

```bash
bash scripts/repeat.sh draft.md runs/noise-check 5
```

Grades the same draft N times, drops degenerate runs, reports the **median** and
the range plus a pass **rate**.

A single fingerprinted draft graded 15 times on byte-identical input spanned
`overall_score` 0.0 → 1.0 (sd 0.244) and produced all four transitions. That was
measured **before** 2.14.0, so the field it spans is the pre-repoint blend, not
the submitted side — the noise it demonstrates is real and is why this script
exists, but do not read it as a spread on your own draft's grade. Across
18 repeat groups the submitted pass/fail flipped 22% of the time and the
transition changed 33%. The cause is quantization — five binary lines, six
possible scores, the bar at 4.2, so one dimension flipping flips the verdict —
and it does not go away at temperature 0 (measured: identical noise floor across
a 600-call two-arm test).

Vintage: these figures were measured on the superseded 4.x-series judge and
before #2291 made evidence draws deterministic, so they describe the historical
instrument, not the current one.

Take the median before you act on a change, and before you tell anyone a draft
got better. Take it on the **submitted fraction** — medianing `transition` buys
you a stable reading of a number that read 92% at eval_version 2.9.0 anyway
(see step 4 for the bounds on that figure, including the 71.0% reading at
2.7.0 and why the two are not a before/after).

## Grading a batch

```bash
bash scripts/batch.sh launch-q3.tsv runs/q3 3
```

Grades a manifest of drafts at bounded concurrency, writing each item to
`runs/q3/<id>/{report.md,scorecard.json,grade.log}`.

**The manifest is TSV** - one item per line, blank lines and lines starting with
`#` ignored so you can comment an item out without deleting it:

```
id <TAB> file [<TAB> audience] [<TAB> account]
```

`id` is the directory name under the run-dir and the handle you re-run with, so
keep it filesystem-safe. A `.json` file is sent as the inputs object **verbatim**;
anything else is wrapped as `{"message": <contents>}`, the same rule `grade.sh`
uses. TSV rather than CSV because audience and account are prose that contains
commas far more often than tabs.

**Concurrency defaults to 3**, and the number to think about is requests per
minute, not workers. With the blocking read in `_lib.sh` a single run costs
roughly 1 submit + ~5 blocking reads + 2 fetches over its 2-3 minutes, so 3
workers sit around 10 req/min - an order of magnitude under the 100/min per-IP
limit, with headroom for the retries a bad minute needs. Every worker you add
also adds its share of the retry traffic when things go wrong.

The transport honors 429 `Retry-After` and circuit-breaks a dead endpoint rather
than grinding against it: once the breaker opens the batch stops **launching**
new items and says so, leaving in-flight items alone (they may be one poll from
finishing).

**Re-running only does the casualties.** An item whose `report.md` already exists
is skipped, so after a partial batch you fix whatever broke and run the exact
same command - it backfills the failures without re-grading (or re-paying for)
what already landed. Failed ids are printed at the end as a space-separated list,
ready to paste into a `grep` for a smaller manifest. Delete an item's directory
to force a re-grade.

## Config

| Env var | Default | What it does |
| --- | --- | --- |
| `AMDAHL_KEY` | - | Workspace API key. `AMDAHL_API_KEY` and `AMDAHL_MCP_API_KEY` are accepted too. |
| `AMDAHL_API_BASE` | production | Point at a non-production workspace. |
| `AMDAHL_EVAL_SLUG` | `prompt-and-message-eval` | Which eval to run. |
| `AMDAHL_WAIT_MS` | `30000` | How long the server holds each read open (`?wait_ms=`). `0` falls back to tight polling, only useful against a server that does not support it. |
| `AMDAHL_POLL_ATTEMPTS` | `12` | Poll ceiling, now counted in **blocking reads**, not tight polls: 12 x 30s ≈ 6 minutes. The name is unchanged so an existing override still means "the ceiling". |
| `AMDAHL_POLL_INTERVAL` | `15` | Gap between reads, only used when `AMDAHL_WAIT_MS=0`. |
| `AMDAHL_MAX_RETRIES` | `6` | Attempts per call before it gives up. |
| `AMDAHL_BACKOFF_CAP` | `60` | Ceiling on our own backoff, in seconds. A server-sent `Retry-After` is honored past it - the cap governs guesswork, not an explicit instruction. |
| `AMDAHL_CIRCUIT_THRESHOLD` | `5` | Consecutive hard failures (per call, not per attempt) before the breaker opens. |
| `AMDAHL_BREAKER_FILE` | keyed to `$PPID` | Breaker state file. Workers under one `batch.sh` share one by default; set it explicitly to share across separate invocations. |

## Gotchas

- **A run is queued.** Budget 1–3 minutes; the scripts poll for you.
- **`reuse` defaults to `cached`** (15 min, content-addressed on the inputs), so
  an iteration loop silently replays and the score cannot move. The scripts
  always send `force` and warn loudly if `reused=true` comes back anyway.
- **`dimension.pass` is the boolean; `facet.passed` is a count.** Reading
  `dimension['passed']` yields nothing and prints every dimension as a failure.
- **Not every run has a before/after.** A `not_applicable` run, a failure, or an
  eval whose graders produce no improvement report all return a card with no
  scorecard table and a null `headline`. Do not fabricate one.
- **`audience` can abstain** (`not_provided` / `unresolvable` / `no_evidence` /
  `thin_evidence` / `lookup_failed`). An abstained run was graded against the
  whole corpus, so it is not comparable to a scoped one.
