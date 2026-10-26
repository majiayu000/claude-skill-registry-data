---
name: r
description: Use when analysing data with R — monthly time series with seasonality, moving averages and outlier detection, tidy data with dplyr or base R, ggplot2 charts, testthat tests, renv for reproducibility and running scripts in Docker. Also use when an analysis gives different numbers on another machine, or when dependency update bots do not support R.
---

# R

Default: current R release, `renv` for package versions, scripts run with `Rscript`, base `stats` for time series (`ts`, `stl`, `decompose`), ggplot2 for charts, testthat for tests, a `rocker/r-ver` image pinned to the R version for reproducible runs.

## Setup

1. `renv::init()` in the project, commit `renv.lock`; collaborators run `renv::restore()`.
2. Put analysis code in functions under `R/` and keep top-level scripts short (`Rscript run.R input.csv`).
3. Pin the Docker base image to the same R version as `renv.lock`. Automated dependency bots do not read `renv.lock`, so let them track the base image tag instead and update packages deliberately.

## Monthly time series

- Build a complete monthly index first; missing months must be explicit `NA`, not absent rows, or seasonal lags shift.
- `ts(x, frequency = 12, start = c(year, month))`, then `stl(x, s.window = "periodic")` for trend + seasonal + remainder (needs at least two full years and no `NA` — impute or trim first).
- A centred 2×12 moving average (`stats::filter(x, c(1/24, rep(1/12, 11), 1/24), sides = 2)`) shows trend without seasonality; a plain 12-term window is off-centre by half a month.
- Flag outliers on the **remainder**, not the raw series (e.g. |remainder| > 3 × MAD); a winter peak is not an outlier.
- Report each flag with the month, value, expected value and the rule that fired.

## Data handling

- Read with explicit column types (`readr::read_csv(col_types = ...)` or `colClasses`); check `problems()`.
- Dates with `as.Date(x, format = "%Y-%m-%d")`; avoid locale-dependent month names.
- Keep data tidy (one row per observation) before plotting or modelling.

## Charts

- `ggplot2` with explicit scales and units in axis titles; save with `ggsave(width, height, dpi)` so output is identical across machines.

## Testing

- `testthat` for functions: complete-index creation, imputation, outlier rule on a synthetic series with a planted spike.
- Set seeds (`set.seed`) wherever randomness is used, and record them.

## Verification loop

1. `Rscript -e 'renv::status()'` reports a consistent library.
2. `Rscript -e 'testthat::test_dir("tests")'`.
3. Run the script in the pinned container and compare outputs with the local run.

## Pitfalls

- **Factors from strings:** older code and some readers convert strings to factors; check `str(df)`.
- **`NA` propagation:** `mean(x)` is `NA` if any value is missing; decide between `na.rm = TRUE` and imputation explicitly.
- **1-based indexing and recycling:** vectors of different lengths recycle silently, often with only a warning.
- **`sapply` return types** change with input; use `vapply` with a declared type.
- **Floating comparisons:** use `all.equal` or a tolerance, not `==`.
