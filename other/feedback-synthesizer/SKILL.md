---
name: feedback-synthesizer
version: 1.3.3
author: Personify Labs
description: >
  Turns raw survey results (scores + open-text comments) or any pile of
  qualitative feedback (reviews, support tickets, open-ended comments) into
  a scored, statistically-tested, thematically-coded synthesis with
  severity-ranked findings. Trigger when someone pastes raw survey data, a
  CSV of responses, or a pile of qualitative feedback and wants it turned
  into findings. Entry point 2 of the research loop (see research-loop);
  also runs standalone without a survey-architect-built survey.
tags:
  - user-research
  - ux-research
  - qualitative-analysis
  - statistics
  - thematic-coding
license: CC-BY 4.0
---

# Feedback Synthesizer

Takes raw numbers and raw comments and produces one connected picture, not
two separate reports that happen to sit in the same doc.

Most teams either report a score or summarize comments. This skill's whole
job is to make the two inform each other — a score drop with no thematic
explanation isn't a finding yet.

-----

## Step 0: What are you looking at?

Identify the input type before doing anything:

- **From survey-architect** (a `/research/<study-name>/01-survey-spec.json`
  exists) → read it for instrument, scoring formula, and expected n. Use
  it, don't re-derive.
- **Standalone raw data** (pasted CSV, app store reviews, support ticket
  export, no spec file) → identify the instrument from the data itself
  if it's a known format (SUS items, an 0–10 NPS column, etc.), or treat
  it as unstructured qualitative feedback if there's no scale attached.
  Say explicitly which case you're in — don't silently assume a scale
  that isn't there.

-----

## Step 1: Quantitative scoring

**Run `scripts/scoring.py` — do not compute these by hand.** Every
instrument formula, the confidence interval, and the significance tests
are exact, deterministic calculations with no judgment involved, which
is exactly the kind of task that should never depend on an LLM doing
arithmetic in its head. Call the matching function for the instrument in
use:

| Instrument | Function |
|---|---|
| SUS | `sus_score(responses)` |
| UMUX | `umux_score(responses)` |
| UMUX-Lite | `umux_lite_score(item1, item2)` |
| NPS | `nps_score(responses)` |
| CSAT | `csat_top_two_box(responses)` or `csat_mean(responses)` — state which |
| SEQ / CES | `seq_score(responses)` / `ces_score(responses)` |
| SUPR-Q | `supr_q_score(five_point_items, nps_item_0_to_10)` |

If the instrument doesn't map to one of these (a custom item set), say
so explicitly rather than forcing it through the nearest function.

### Confidence intervals and significance testing

Also not optional, also run through the script — call
`confidence_interval(scores)` and, when comparing against a benchmark
or prior wave, `significance_vs_benchmark(scores, benchmark)` or
`compare_waves(scores_a, scores_b)`. Never report a headline score
without its CI, and never call a difference "significant" without
having actually run the test. The confidence level itself
(`scoring.DEFAULT_CONFIDENCE_LEVEL`, currently 90%) is centralized in
the script, not restated here — if it ever changes, it changes in one
place.

State the result in plain language alongside the numbers ("the 6-point
drop is outside the margin of error — this is a real change" vs. "the
3-point drop is within the CI — could be noise").

**Three separate questions, never collapsed into one:**

- **Statistical significance** — did `significance_vs_benchmark` /
  `compare_waves` actually return `significant=True`? This is the only
  question those functions answer.
- **Practical significance** — does the *size* of the difference matter
  for the decision the study was run for? A statistically significant
  2-point SUS movement on an n=400 study is real but may not be worth
  acting on; state this explicitly when it applies, don't let a small
  p-value stand in for "this matters."
- **Evidence confidence** — see the dedicated section below. A narrow CI
  does not by itself mean the overall conclusion is trustworthy, and a
  wide CI does not by itself mean it isn't.

A statistically significant result is not automatically important. A
non-significant result — especially at a small n — is not automatically
"no real difference"; it may just mean the study was underpowered to
detect one. Say which situation you're in rather than defaulting to
either reading.

If `scripts/scoring.py` isn't available in the execution environment for
some reason, say so explicitly before falling back to manual
calculation — don't silently compute by hand and present it as if the
script ran.

### Small-sample handling

If n falls below the sample-size floor survey-architect specified (or
below the general rule-of-thumb minimums if there's no spec file):

- **Compute the score anyway.** Never refuse.
- **Widen the CI accordingly** and say so explicitly.
- **Flag it loudly** at the top of the synthesis output, not buried in a
  footnote: `⚠️ LOW CONFIDENCE — n=<X>, below recommended minimum of <Y>.
  Treat this score as directional, not conclusive.`
- If the gap is large enough that the score is essentially unusable for
  the stated decision (see survey-architect's learning goal), **kick
  back to survey-architect** with a note to extend collection — this is
  the loop-back condition, not a silent proceed.

-----

## Step 2: Qualitative coding

Treat this as a protocol, not a single read-through-and-label pass —
initial impressions from comment 1 shouldn't silently become the frame
everything else gets sorted into:

1. **Read the full dataset once before coding anything.** Don't start
   labeling on comment 1.
2. **Generate initial codes** — short, descriptive, close to the data.
3. **Review code consistency** — the same underlying complaint shouldn't
   end up under two different code names.
4. **Merge/split codes** where the initial pass was too fine- or
   coarse-grained.
5. **Identify candidate themes** by grouping related codes.
6. **Actively look for disconfirming cases** — comments that don't fit
   the emerging theme, or that would complicate it. Don't just note
   supporting examples.
7. **Test each theme against the full dataset**, not just the comments
   that inspired it.
8. **Quantify themes only after coding has stabilized** — counting
   before the taxonomy settles bakes in whatever grouping happened to
   come first.
9. **Assign a per-theme coding confidence** (see the Evidence Confidence
   section below) — some themes are obvious, some rest on a handful of
   ambiguous comments; say which.
10. **Cross-reference against the quantitative data** (Step 3).

Taxonomy source:

- **New product or first study:** code comments with an emergent/open
  approach — let themes surface from the data, don't force them into a
  predefined bucket.
- **Product with prior studies:** check
  `/research/_benchmarks/<product>.md` for the existing theme taxonomy.
  Reuse those theme labels where the data fits; only add a new theme
  label if genuinely nothing existing captures it. This is how the
  taxonomy converges over time instead of resetting every study.
- For each theme, report: frequency (n and %), representative
  paraphrased examples (never verbatim quotes — see copyright note
  below), whether it skews toward low or high scorers, and the coding
  confidence from step 9 above.

**Never quote respondents verbatim in synthesis output** — paraphrase
every comment. This matters for two reasons: respondent privacy in
smaller samples, and because verbatim quotes get copy-pasted into
decks and lose the aggregation context.

-----

## Step 3: Cross-reference qual and quant

This is the step most synthesis work skips. For every notable score
change (a wave-over-wave drop, a below-benchmark score, a segment that
scores lower than others):

1. Pull the subset of open-text comments from respondents in that score
   band.
2. Check whether a theme is disproportionately represented in that
   subset vs. the overall theme distribution.
3. If yes, state the connection explicitly: "SUS dropped 8 points this
   wave (95% CI: −11 to −5, statistically significant vs. wave 2). 60%
   of respondents scoring below 60 mentioned the new checkout step,
   vs. 12% of respondents scoring above 80."
4. If no clear theme explains a score change, say that too — an
   unexplained score movement is itself a finding, not a gap to paper
   over.

-----

## Step 4: Severity and priority scoring

This skill owns severity/priority — not the reporter. **Once you have
the raw counts (how many respondents in each score band mentioned the
theme), run `scoring.severity_tier(...)` rather than eyeballing the
percentages** — this is the exact calculation that was wrong in v1.0.0
(diluted by whole-sample frequency instead of within-band frequency),
and it's now a tested function specifically so that bug can't quietly
reappear in prose form. Getting the raw counts right — which respondents
go in which band, whether a comment belongs to the theme — is still
your judgment call; the arithmetic on top of those counts is not.

Score each theme on two axes:

- **Frequency:** what % of respondents *in the affected score band*
  raised it — not what % of the whole sample raised it. A theme
  mentioned by 3 of 4 low scorers is high-frequency even if it's only
  3 of 14 respondents overall. Measuring frequency against the full
  sample dilutes a concentrated signal and can demote a real driver of
  low scores to a lower tier than it deserves. Also report the plain
  overall % for context, but don't let it drive the tier.
- **Impact:** does it correlate with low scores / high effort / low
  completion — i.e., is the theme's presence skewed toward one score
  band vs. another, per the cross-reference in Step 3

Combine into a simple priority tier (not a false-precision numeric
score):

- **Critical** — high frequency *within the affected band* (roughly
  ≥50% of respondents in that band) **and** a clear skew vs. the
  unaffected band (that band's rate is meaningfully higher than the
  rest of the sample's rate for the same theme)
- **Notable** — meets one of the two Critical conditions, not both
  (e.g., mentioned by a majority of low scorers but also shows up
  somewhat among high scorers, or a clear skew but only a small
  minority of the affected band mentions it)
- **Minor** — low frequency within the affected band and no meaningful
  skew vs. the rest of the sample

State the reasoning for each tier assignment explicitly, including both
the within-band and overall frequency numbers — don't just output the
label, and don't let a low overall frequency read as an argument against
a tier the within-band numbers support.

**The frequency/skew tier is a default, not a law.** Pass
`scoring.severity_tier`'s `override` argument (one of
`scoring.VALID_OVERRIDE_REASONS`: `safety`, `accessibility`,
`legal_compliance`, `severe_user_harm`, `critical_task_blockage`) when
one of those considerations should outrank the computed tier — e.g. a
low-frequency accessibility barrier can legitimately outrank a
high-frequency cosmetic complaint. An override is never silent: report
both `computed_tier` (what the frequency math actually produced) and the
override reason side by side, never just the final "Critical" label. An
override is for one of those five named reasons — not for a stakeholder
who'd simply prefer a different number. `severity_tier` raises on any
other reason string rather than accepting it.

**Coding themes from judgment, not keyword matching.** A comment can
belong to a theme without using any of that theme's obvious keywords —
e.g., "had to re-enter my card info twice" belongs in a payment/checkout
friction theme even though it never says "payment." Read each comment
for what it's actually describing, not for whether it contains a
specific word. A literal string search will systematically undercount
themes and produce frequency numbers that look lower than reality.

-----

## Step 4.5: Evidence confidence, claim strength, and uncertainty

Three fields belong on every finding, distinct from anything computed
above:

**Evidence confidence** — how much to trust the *overall conclusion*,
not any one statistic. One of `scoring.EVIDENCE_CONFIDENCE_LEVELS`:
`HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`. Base it on sample quality,
source quality, per-theme coding confidence (Step 2), and whether
qual and quant actually triangulate (Step 3) — not on how narrow the CI
happens to be. State the drivers, not just the label, e.g.:
`{"overall": "MEDIUM", "drivers": {"sample_quality": "high", "coding_confidence": "medium", "triangulation": "low"}}`.
Don't collapse these into a single number — a category is honest about
how fuzzy this judgment is; a number pretends otherwise.

**Claim strength** — tag each finding with one rung of
`scoring.CLAIM_STRENGTH_LEVELS`: `observed` (reported/measured, no
relationship claimed), `associated` (co-occurs with something else,
direction untested), `correlated` (a statistical relationship was
actually tested), or `causal` (one thing was shown to produce another).
**Run `scoring.validate_claim_strength(level)` before writing a claim
down** — it raises if `causal` is used without an experimental or
strong quasi-experimental design behind it, which a survey/feedback
synthesis never has. Default to `correlated` when tempted to say
`causal`.

**Alternative explanations and "cannot determine."** For findings above
`Minor` severity, name at least one plausible alternative reading of the
same data (e.g. "navigation terminology may be unfamiliar" as an
alternative to "navigation is broken") — this is what stops a single
plausible story from being reported as the only one. Separately, list
anything the data genuinely can't answer (e.g. "whether this causes
account abandonment") rather than implying an answer the evidence
doesn't support.

-----

## Step 5: Output

Write `/research/<study-name>/02-synthesis.md` **and**
`02-synthesis.json` — the `.json` is the canonical, machine-readable
artifact research-reporter consumes; the `.md` is the human-readable
copy of the same facts. Before writing, run `scoring.validate_synthesis(synthesis)`
and fill in anything it reports missing. Required shape: `study`,
`product`, `instrument`, `n`, `score` (value + CI), `significance`,
`low_confidence_flag`, `themes` (each with frequency, `severity`
[`tier`, `computed_tier`, `override_reason`], `claim_strength`),
`cross_references`, `evidence_confidence`, `alternative_explanations`,
`cannot_determine`.

Before appending to the benchmark file, check comparability against the
prior wave's recorded instrument/wording/scale/population/sampling
method/trigger (see research-loop's `check_benchmark_comparability`) —
if they don't match closely enough, report the two waves separately
rather than implying a trend. When they do, append the wave's headline
score to `/research/_benchmarks/<product>.md`: date, instrument, score,
CI, n, and the same measurement-condition fields, so the *next* study's
comparability check has something to check against.

-----

## Rules

Priority when rules interact: **STOP** > **MUST NOT** > **MUST** >
**SHOULD** > **MAY** — see `ux-research/README.md` for the full
precedence explanation.

- **STOP** if the sample is so small the stated learning goal can't be
  answered at all — kick back to survey-architect instead of proceeding.
- **MUST NOT** report a score without its confidence interval.
- **MUST NOT** call a numeric difference "significant" without having
  run the actual test.
- **MUST NOT** refuse to score a small sample — flag it loudly and
  proceed instead.
- **MUST NOT** quote respondents verbatim.
- **MUST NOT** force new data into an existing theme taxonomy when it
  genuinely doesn't fit.
- **MUST NOT** code themes by keyword/string matching instead of reading
  each comment for what it actually describes.
- **MUST NOT** measure a theme's frequency only against the whole sample
  when deciding severity — check frequency within the affected score
  band first.
- **MUST NOT** label a finding `causal` without an experimental or
  strong quasi-experimental design — `validate_claim_strength` enforces
  this; don't work around it by skipping the call.
- **MUST NOT** apply a severity override for a reason outside
  `scoring.VALID_OVERRIDE_REASONS`, or apply one silently without
  stating `computed_tier` alongside the override.
- **MUST NOT** treat two benchmark waves as a trend without checking
  comparability first.
- **MUST** report a score movement and a theme together only after
  checking (Step 3) whether they're actually connected — an unexplained
  movement is itself a finding, never papered over.
- **MUST** state the frequency + impact reasoning behind every severity
  tier, not just the label.
- **SHOULD** name at least one alternative explanation for any finding
  above Minor severity, and list what genuinely cannot be determined
  from the data.

-----

## Quick reference

| Situation | Action |
|---|---|
| n below recommended minimum | Score it, widen CI, flag loudly |
| n so small the learning goal is unanswerable | Kick back to survey-architect |
| Score drop, no theme correlation found | Report the drop as unexplained, don't force a story |
| Score drop + strong theme correlation | State both together as one finding |
| New product, first study | Emergent coding |
| Existing product with prior studies | Reuse taxonomy from benchmark file, extend only if needed |
| Standalone data, no spec file | Say so explicitly, identify instrument from data structure |

## Maintaining this skill

`evals/` is the regression suite. After touching `scripts/scoring.py`, run
`python3 -m unittest discover -s evals -v` (CI runs the same). After
touching this file's prose, re-check the cases in
`evals/qualitative_cases.md` by hand.
