# Statistical robustness & error analysis (Elrond's quantitative pass)

A verdict that never does arithmetic is just taste. This pass makes Elrond actually
*compute* how likely a reported result is to be a statistical accident, in both
directions: a false positive (Type I) dressed up as a discovery, and a false negative
(Type II) dressed up as "no effect." Run it on every quantitative headline. Do the
math explicitly, show the numbers, and put them in the Evidence log. When the source
data is present (artifact mode), recompute; when only summary stats are given, do the
back-of-envelope from what's reported.

The rule: **name the error you are most at risk of, then bound its probability.**

**Compute, do not fabricate.** Every number in this pass must come from an actual
calculation on reported values, not a plausible-sounding guess. If you state a binomial
tail, a power figure, or a corrected count, you must be able to show the inputs and the
operation. If the paper does not report enough to compute a check (no N, no SD, no test
statistic), say the check is *blocked for lack of reported values* and name what the
author must report, rather than inventing a number. A confidently-stated statistic the
review did not actually compute is the review's own Type I error.

## A. Type I risk - is this a false positive?

A "significant" result is only impressive relative to how many chances it had to appear.

- **Multiplicity math.** Count the tests actually run (including the silent ones:
  every ROI, layer, threshold, hyperparameter, and subgroup is a test). Under the null,
  the expected number of false positives is `m x alpha`. Compare the number of hits to
  that expectation. Example: 25 ROIs at alpha = 0.05 -> expect ~1.25 false hits by
  chance. Reporting 3/25 "significant" is barely above chance; reporting 21/25 is far
  beyond it (see the binomial check below).
- **Binomial "by chance" check.** Under H0, the number of hits among `m` independent
  tests is Binomial(m, alpha). Compute `P(X >= observed)`. For 21/25 at alpha = 0.05,
  that tail probability is astronomically small, so the *count* is real even if
  individual ROIs aren't. For 3/25, `P(X >= 3) ~ 0.13` - not surprising at all. State
  the number. (Caveat: tests are usually **dependent**, which inflates the true tail;
  note it and prefer a permutation null when the data allow.)
- **Correction.** Apply Holm-Bonferroni (family-wise) or Benjamini-Hochberg (FDR) and
  report how many "significant" results survive. An uncorrected forest of t-tests with
  a couple of `p < 0.05` survivors is usually noise.
- **p-value plausibility.** Is the headline `p` suspiciously just under 0.05
  (0.048, 0.041)? A cluster of marginal p-values across a literature or a paper is a
  p-hacking tell. Report the **s-value** (`-log2(p)`) for intuition: `p = 0.05` is only
  ~4.3 bits of surprise, about the same as calling 4 coin flips. `p = 0.04` is not
  "strong evidence."
- **Forking paths.** If analytic choices were made after seeing the data, the *effective*
  alpha is far above the nominal one; the nominal p is optimistic. Flag and, if possible,
  estimate how many defensible analysis paths existed.

## B. Type II risk - is a null just an underpowered silence?

A non-significant result is only "no effect" if the study could have detected the effect.

- **Power / MDES.** Given the N and design, what is the **minimum detectable effect
  size** at 80% power? If the MDES is larger than any effect the field considers
  meaningful, a null is uninformative, not evidence of absence. State it: "at N = 4,
  80% power requires d ~ 2.4; this design cannot detect a realistic d ~ 0.5."
- **Post-hoc power is not a fix.** Don't compute observed-power from the observed effect
  (it's a monotone restatement of p). Use the *design* to get MDES against a
  field-meaningful effect instead.
- **CI width over p.** A null with a CI spanning from "large negative" to "large
  positive" is uninformative; a null with a tight CI around zero is genuine evidence of
  absence. Read the interval, not the significance star.
- **Equivalence framing.** If the claim is "no difference," was a TOST / equivalence
  test run against a pre-set margin, or is absence inferred from `p > 0.05`? The latter
  is a Type II error waiting to happen.

## C. Is the effect too good (or too clean) to be true?

- **Effect-size sanity.** Compare the reported effect to the plausible range in the
  literature. A d = 3.0 or an r = 0.95 in a noisy domain is more likely a leak/artifact
  (Gate 0) than a real effect. Improbably large is a red flag, not a triumph.
- **Arithmetic consistency (GRIM / SPRITE-style).** Do reported means and SDs match the
  stated N? A mean of 3.47 from N = 7 integer responses may be arithmetically
  impossible. Reported summary stats that can't be produced by any dataset of that size
  are a hard finding.
- **Variance sanity.** SDs near zero, identical values across conditions, or
  suspiciously round numbers warrant a second look at provenance.
- **Fragility index.** For a binary/count outcome, how many event flips would push the
  result from significant to non-significant? A significance that hinges on one or two
  observations is fragile, and the paper should say so.

## D. Combining and cross-checking

- **Bootstrap / permutation first** for small-N or non-normal data. A parametric p at
  N = 4 assuming Gaussianity is not trustworthy; a permutation null is.
- **Combine evidence honestly.** If several weak p-values are offered as a body of
  support, note that a pile of `p ~ 0.04`s is weak, and that Fisher-combining dependent
  tests overstates evidence.
- **Likelihood / Bayes framing (optional).** Where useful, translate `p` into a rough
  Bayes-factor bound or a likelihood ratio so the reader sees evidence strength, not
  just a threshold crossing.

## E. The adversarial reviewer's hard-check battery

These are the specific, computable tests a hostile methods reviewer runs when a result
"smells off." Each is cheap arithmetic on numbers the paper already reports. Run the
ones the design invites; name any that fail as findings.

**Reported-statistics consistency (does the paper agree with itself?)**
- **statcheck / test-stat <-> p recompute.** Recompute the p-value from the reported test
  statistic and df (t, F, chi-square, r). A reported "t(28) = 2.1, p < .01" is wrong: that
  t gives p ~ .045. Internal inconsistency is a hard finding and a fabrication/typo screen.
- **SE / SD / CI coherence.** Check `SE = SD / sqrt(n)` and `95% CI ~ mean +/- 1.96*SE`. A
  CI that doesn't match the reported SD and N means one of them is wrong (or SE and SD
  were confused, which silently halves or doubles the apparent precision).
- **df sanity.** Do the degrees of freedom match N and the design? A t-test df of 28 with
  a claimed N = 12 signals an undisclosed pooling or a different test than named.
- **GRIM / GRIMMER.** For means/SDs of integer (e.g. Likert) items, check that the reported
  mean is achievable given N (GRIM) and the SD is achievable (GRIMMER). Impossible summary
  stats are a data-integrity Blocker.
- **F <-> eta-squared / R^2 <-> F reconstruction.** For ANOVA/regression, verify the effect
  size, test statistic, and df are mutually consistent (e.g. `F(df1,df2)` implies a specific
  partial eta-squared / R^2). Mismatch = miscomputed or mistyped.

**p-hacking and selection screens**
- **Caliper test.** Compare the count of p-values in [.045, .05) against [.04, .045). A
  bulge of results *just* under .05 across the paper (or a literature) is the classic
  p-hacking signature; run a binomial test on the caliper split.
- **p-curve intuition.** A set of *true* effects produces right-skewed p-curves (many small
  p's); a flat or left-skewed curve near .05 suggests selection or no true effect.
- **Terminal-digit / Benford screen.** For a large table of reported values, check
  last-digit uniformity (or Benford's law for naturally-scaled quantities). Strong
  departures are a fabrication screen, not proof, but they license a closer look.

**Correlations and regressions**
- **Fisher-z CI on r.** Convert r to z = atanh(r), CI = z +/- 1.96/sqrt(n-3), back-transform.
  Report the CI on any headline correlation; a "strong" r = 0.6 at n = 10 has a CI of
  roughly [0.0, 0.88], i.e. barely excludes zero.
- **Compare two correlations / two slopes** with the proper test (Fisher-z difference for
  independent r's), not by noting one is significant and the other isn't.
- **Attenuation & range restriction.** A correlation is bounded by the reliability of its
  measures; range restriction shrinks it. If a claim rests on a *small* r, ask whether
  measurement noise could explain the ceiling.
- **Multicollinearity (VIF).** For a regression with correlated predictors, high VIF makes
  individual coefficients unstable and sign-flippy; a confidently-signed beta under high VIF
  is fragile (ties to Gate 4 confounds).
- **Winner's curse / regression to the mean.** The top-ranked effect among many (best ROI,
  best layer, best seed) is upward-biased by selection; the honest estimate is shrunk.
  Expect the "peak" to regress on replication.

**Multiple testing, done quantitatively**
- **Expected false discoveries.** After BH-FDR at level q with R rejections, expected false
  positives ~ `q*R`. State it. After Bonferroni, family-wise error <= `m*alpha`.
- **Effective number of tests (correlated).** For correlated tests (neighboring ROIs,
  layers), naive Bonferroni over-corrects; estimate the effective number via the eigenvalues
  of the correlation matrix (Nyholt/Li-Ji) and correct against that instead.
- **Positive predictive value of a "discovery."** With pre-study odds R (prior), power
  1-beta, and alpha, `PPV = (1-beta)*R / [(1-beta)*R + alpha]`. In a low-prior search (most
  ROIs/genes/heads are null), even a significant hit is more likely false than true. Compute
  it - it reframes "we found a significant effect" honestly.

**Design-integrity checks**
- **Sample-ratio mismatch (SRM).** For randomized/allocated designs, chi-square the observed
  group sizes against the intended ratio. A significant SRM means the randomization or logging
  is broken and *every* downstream comparison is suspect.
- **Pseudo-replication / clustering.** Are repeated measures or clustered observations treated
  as independent? The effective N is deflated by the design effect `1 + (m-1)*ICC`; ignoring it
  inflates significance. Recompute the effective N and re-read the p.
- **Outlier leverage (leave-one-out).** Recompute the headline correlation/mean dropping each
  point; if significance hinges on one observation, it's fragile (report the LOO range).
- **Simpson's paradox / aggregation.** Could the pooled effect reverse or vanish within
  subgroups? Check at least one obvious stratification.

**Evidence-strength translation (beyond the star)**
- **Minimum Bayes factor from p (Sellke-Berger).** A bound on the evidence: `BF >= -e*p*ln(p)`.
  For p = .05 this is ~ 0.41, i.e. at best ~2.5:1 against the null - weak. Use it to puncture
  "p = .05 means strong evidence."
- **s-value.** `-log2(p)` bits of surprise; p = .05 ~ 4.3 bits ~ four coin flips.
- **E-value (observational/causal claims).** For an association argued as causal, the E-value
  is how strong an unmeasured confounder would need to be to explain it away. A small E-value
  means a modest confound suffices - demand the control (ties to Gate 4/5).

Pick the checks the paper's own numbers make possible, do the arithmetic, and show it. The
goal is that a real Reviewer 2 finds nothing left to compute that you didn't already compute.

## How this pass reports

Add a short **Error Analysis** block to the review (fold into Elrond's objection and
the Evidence log). For each central quantitative claim, state:

1. The dominant error risk here (**Type I** or **Type II**), and why.
2. The number that bounds it: the `m x alpha` expectation, the binomial tail, the
   surviving-after-correction count, the MDES, or the fragility index.
3. The one recomputation or additional statistic that would settle it (often the
   "what would change the verdict" line for a stats-limited paper).

The bar: a reader should be able to see *how improbable the result is under the null*
and *how much the design could have missed*, in actual numbers, not adjectives.
