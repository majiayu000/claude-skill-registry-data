---
name: ecosim-lange-bias-adjustment
description: Apply and cross-validate Lange (2019) ISIMIP3BASD climate bias adjustment using tower or other measured reference data, then prepare EcoSIM forcing. Use for trend-preserving distribution correction of NLDAS, ERA5 or climate-model weather; distinguish published daily processing from an explicitly validated hourly adaptation.
---

# Lange climate bias adjustment for EcoSIM

Produce a separate bias-adjusted forcing candidate, out-of-sample evaluation,
and an auditable method configuration. Skill creation alone does not authorize
changing an active case or launching a simulation.

Read [method and engine](references/method-and-engine.md) before selecting or
running a backend. Read [hourly adaptation and validation](references/hourly-and-validation.md)
for tower/EcoSIM applications. Use the authoritative implementation rather than
recreating a simplified mapping and calling it ISIMIP3BASD.
For a worked case and its rejected corrections, read
[US-Ne1 application lessons](references/us-ne1-application.md). Its thresholds
and accepted fields are case evidence, not defaults for other sites.

## Choose the scientific scope

- **Published daily method:** match daily reference and source support; use the
  documented variable options, monthly processing and trend treatment. This is
  the reference against which an implementation is verified.
- **Hourly tower adaptation:** explicitly label the altered temporal scale,
  reference footprint, missing-data treatment and hourly reconstruction. A
  grid-cell-to-tower adjustment is a site adaptation, not the paper's spatial
  statistical downscaling. Do not invoke that downscaling for a single site.
- Mean offsets, monthly scaling and ordinary empirical quantile mapping are
  useful baselines, not implementations of Lange's full method.

## Prepare the inputs

Invoke `../ecosim-data-readiness/SKILL.md` for the actual site, variables and
period. Establish coordinates, measurement heights, units, timezone, interval
bounds, native point/mean/accumulation semantics and QC before fitting. Freeze
source hashes. Use measured reference samples for primary calibration and
validation; show gap-filled sensitivity separately. Preserve missingness and
coverage by year, month, hour and variable.

Do not calibrate rain against reanalysis-filled tower precipitation or a single
site MAP. Leave that field unchanged when measured precipitation is unavailable,
and retain the shared precipitation-budget audit. Resolve height/domain
mismatches before treating them as statistical bias. In particular, distinguish
surface pressure from the paper's sea-level pressure and EcoSIM actual vapor
pressure `DWPTH` from dewpoint or VPD.

## Fit, evaluate, then assemble

1. Define held-out contiguous year blocks before inspecting correction scores.
   Use the bundled `scripts/make_year_folds.py` to produce a reproducible split
   manifest when useful. Choose sample requirements and diagnostics appropriate
   to each variable; the helper does not establish sample sufficiency.
2. Run the pinned engine using training observations only. Keep held-out
   observations inaccessible to fitting, parameter selection, upper-bound
   estimation and hourly reconstruction. Application-period *source* statistics
   may be used by this distributional method; document that transductive use.
3. Compare raw, a simple seasonal baseline, and Lange candidates on identical
   held-out observations. Report hourly, daily and annual performance, quantiles,
   extremes, diurnal cycles, dependencies, and retained quantile change signals.
   Do not claim skill from in-sample distribution agreement.
4. Select corrections by variable using held-out evidence and physical
   consistency. Preserve raw inputs for unsupported/failed variables and state
   which fields were retained. Check annual anomalies and coupled humidity
   diagnostics before promotion, even when hourly RMSE improves. Record any
   review criterion introduced after seeing results as a post hoc decision;
   do not describe the resulting selected-product score as an independent test
   of that selection. Fit accepted configurations to eligible training
   observations for the final candidate; mark unobserved years as extrapolation.
5. Write a new EcoSIM NetCDF with reader-compatible year/day/hour/grid axes,
   leap-day handling and unchanged calendar/interval registration. Preserve
   reference heights consistent with the adjusted target domain, annual
   chemistry/solar-noon fields and documented carry-forwards. If wind is adjusted
   to tower-height values, its height metadata must change consistently.
6. Read back the final file, run `../ecosim-climate-readiness/SKILL.md` against a
   validation namelist, and recompute precipitation budgets. Changing active
   case inputs additionally requires the whole-case preflight. Neither check
   establishes scientific correctness of the adjustment.

For a forcing-only model experiment, preserve the selected parameter values and
management, identify cold-start versus restart state inheritance, and limit the
configured period to joint forcing/management/GHG coverage. Use the
`../ameriflux-namelist-generator/SKILL.md` workflow for case assembly and checks;
a bias-adjusted weather file alone does not establish run readiness.

## Deliverables and limits

Save input identities/QC masks, train/application dates, engine archive or commit
hash, dependency versions, commands, all per-variable settings, random seeds,
fit/fallback diagnostics, fold scores, and a raw-versus-corrected comparison.
Separate the published algorithm, modifications, and unverified assumptions.
For an HTML deliverable include coverage, yearly bias/RMSE, distribution tails,
mean cycles and a fixed multiweek hourly window, with red warning/conflict titles.
Retain the uncertainty that distribution adjustment cannot recover missing
weather-event timing or guarantee cross-variable physical consistency.

The skill provides a workflow and fold helper; the upstream BASD numerical
engine is an external dependency, not bundled or implicitly installed. Report
an unavailable backend accurately and continue preparation/evaluation work that
is independent of it.

## Local validation

```bash
python -m unittest discover -s .agents/skills/ecosim-lange-bias-adjustment/tests -v
python .agents/skills/ecosim-lange-bias-adjustment/scripts/make_year_folds.py \
  --start-year 2001 --end-year 2024 --block-years 6 \
  --output result/US-Ne1/bias_adjustment/year_folds.json
```
