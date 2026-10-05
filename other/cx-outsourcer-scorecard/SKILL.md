---
name: cx-outsourcer-scorecard
description: Use to compare BPO sites, vendors or partner teams fairly, adjusting for the work mix each is given before concluding anything about performance. Trigger for "compare our BPO sites", "which vendor is performing best", "site A scores lower than site B", outsourcer QBR packs, partner MI reporting, or setting contractual quality targets with a vendor.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Comparing outsourcers and sites

A vendor comparison has money and contracts attached, so it gets argued about in a way
an internal team comparison does not. The vendor will find any methodological weakness,
and they will usually be right about it — because the naive comparison is genuinely
unfair.

**The default finding of an unadjusted vendor comparison is "the site given the harder
work performs worse".** That is not a finding.

## Adjust for mix before comparing anything

Sites are rarely given identical work. Differences that move quality and handle time
independently of how well the site operates:

- **Contact-driver mix.** A site handling disputes and closures will score below one
  handling password resets, whatever its capability.
- **Channel mix**, which has the widest baseline spread of anything.
- **Language and market.** Includes whether they are working in agents' first language.
- **Tenure profile.** A site mid-ramp after a hiring wave is not comparable to a stable
  one, and this is often the entire explanation for a gap.
- **Hours covered.** Overnight and weekend shifts carry a different mix, thinner
  support, and less access to escalation.
- **Systems access.** Vendors are frequently given narrower tool access than internal
  teams, then measured on resolution.

Adjust by **comparing within like-for-like strata** — same contact driver, same
channel, same language — and then weighting back to a common mix. Report both the
unadjusted and adjusted figures with the mix difference shown, because a vendor whose
raw score is worse and whose adjusted score is better has a legitimate grievance and
will make it.

Where a stratum exists at only one site, it cannot contribute to the comparison. Say
so, and say how much volume that removed.

## Make sure the instrument is fair

**Check grader agreement per site before comparing scores.** If the rubric is applied
less reliably to one site's work — a different language, a channel with worse
transcription, graders unfamiliar with that market — then the sites are being measured
with different instruments and the comparison is not valid at all. This check comes
before the comparison, not after it is disputed.

Also verify:

- **Coverage parity.** Are sites evaluated at the same rate? A site sampled at twice
  the rate has a more precise score, and if the sampling rate rose after concerns were
  raised, the comparison looks targeted.
- **Who grades.** If each vendor grades itself, the scores are not comparable at all.
  Calibrate across graders on a shared gold set and report the agreement.
- **Same scorecard version** across sites and across the whole window.

## Report distributions, not just averages

A site average hides the shape, and the shape is where the operational finding is:

- Two sites with the same mean and different variance are different problems. High
  variance means inconsistent execution — usually training or supervision — and the
  fix is different from a uniformly low mean.
- **Report the bottom decile.** A site with a good mean and a bad tail has a
  concentrated problem that is cheaper to fix than a general one.
- **Report per-agent intervals.** A site with 200 agents and 4 evaluations each has no
  usable per-agent data, and a QBR that ranks individuals on it will not survive
  contact with the vendor's own analysis.

## Contractual measures need extra care

If numbers feed a service credit or a penalty, treat them as a contract, not a report:

- **Define every term in the contract**, not in a dashboard: the date field, the status
  filter, the exclusions, the small-cell rule, the restatement policy. Ambiguity here
  becomes a dispute later, and the vendor will read it more carefully than you wrote it.
- **State the measurement error.** A monthly score with a ±5-point interval should not
  trigger a penalty at a 2-point miss. Build a tolerance band in deliberately, or you
  are penalising sampling noise.
- **Agree the sample design in advance**, including who draws it and the seed.
- **Define what happens when volume is too low** to measure a period.
- **Agree a dispute process** with a defined adjudication route, and expect it to be
  used.

**Do not let a metric that was designed for internal coaching become a contractual
gate without redesigning it.** Coaching metrics tolerate noise; contracts do not.

## What to compare beyond quality scores

A quality score alone is a thin picture of a vendor and easy to argue with. Add:

- **Repeat contact rate** on comparable work — harder to game than a QA score.
- **Escalation rate**, split by cause. High authority-escalation usually reflects the
  access you granted, not their capability.
- **Attrition and tenure**, which predict next quarter's scores better than this
  quarter's scores do.
- **Coverage and adherence to agreed volumes.**
- **Complaint rate** on comparable work.

## Traps

- **Reading a ramping site as a failing site.** Check the tenure profile first, every
  time.
- **Comparing across a scorecard change**, or across a period when one site changed
  scope.
- **Ranking sites on a single month.** Monthly variation on realistic sample sizes is
  large; use a rolling window and show the interval.
- **Ignoring what you control.** Access, documentation, training and the routing that
  hands them the work are yours. If a vendor's escalation rate is high because they
  cannot see the system, that is your finding.
- **Presenting a league table.** It produces defensiveness and gaming, and it obscures
  that the fix is usually specific and per-driver.

## Present results to the user

1. **Mix comparison first** — how the work differs across sites, before any performance
   number.
2. **Instrument fairness** — grader agreement per site, coverage parity, grader
   identity, scorecard version.
3. **Unadjusted and mix-adjusted results side by side**, with distributions and
   intervals, not just means.
4. **Volume excluded** because a stratum existed at only one site.
5. **The wider measure set** — repeat contact, escalation by cause, tenure, complaints.
6. **What is attributable to the vendor and what is attributable to you** — access,
   documentation, routing, work allocation. Separate these explicitly.
7. **If numbers are contractual**: the exact definitions, the tolerance band, and the
   dispute route.
