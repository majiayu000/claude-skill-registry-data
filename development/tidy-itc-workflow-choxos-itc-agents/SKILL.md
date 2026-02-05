---
name: tidy-itc-workflow
description: Master tidy modelling patterns for ITC analyses following TMwR principles. Covers workflow structure, consistent interfaces, reproducibility best practices, and data validation. Use when setting up ITC analysis projects or building pipelines.
---

# Tidy ITC Workflow

Apply tidy modelling principles from "Tidy Modeling with R" (TMwR) to indirect treatment comparison analyses for consistent, reproducible, and maintainable code.

## When to Use This Skill

- Setting up a new ITC analysis project
- Building reproducible analysis pipelines
- Creating standardized interfaces across ITC methods
- Ensuring code quality and maintainability
- Reviewing code for tidy modelling compliance

## Core Principles from TMwR

### 1. The "Pit of Success" Philosophy
- Software should facilitate proper usage by design
- Users should "fall into winning practices" naturally
- Interface must protect users from methodological errors

### 2. Workflow-Centric Architecture
Every ITC analysis follows this structure:
```
Data → Validation → Preparation → Analysis → Diagnostics → Reporting
```

### 3. Consistent Interfaces
All ITC functions should have predictable patterns:
```r
# Standard function signature pattern
itc_function(
  data,                    # Primary data input
  outcome_var,             # Outcome variable name
  treatment_var,           # Treatment variable name
  covariates = NULL,       # Optional covariates
  method = "default",      # Method specification
  alpha = 0.05,           # Significance level
  seed = NULL,            # For reproducibility
  verbose = TRUE,         # Progress messages
  ...                      # Additional method-specific args
)

# Standard return structure
list(
  results = tibble(...),   # Main results as tibble
  diagnostics = list(...), # Model diagnostics
  model = fitted_model,    # Raw model object
  data_summary = list(...),# Data summary
  call = match.call(),     # Original call
  parameters = list(...)   # Analysis parameters
)
```

## ITC Workflow Structure

### Step 1: Project Setup
```r
# Recommended project structure
project/
├── R/
│   ├── 01_data_prep.R
│   ├── 02_analysis.R
│   ├── 03_sensitivity.R
│   └── 04_reporting.R
├── data/
│   ├── raw/
│   └── processed/
├── output/
│   ├── figures/
│   └── tables/
├── renv.lock          # Package versions
└── _targets.R         # Pipeline definition (optional)
```

### Step 2: Environment Setup
```r
# Load packages with explicit namespacing preference
library(tidyverse)
library(meta)       # Pairwise MA
library(netmeta)    # NMA
library(maicplus)   # MAIC
library(stc)        # STC
library(multinma)   # ML-NMR

# Set global options
options(
  dplyr.summarise.inform = FALSE,
  mc.cores = parallel::detectCores() - 1
)

# Set seed for reproducibility
set.seed(12345)
```

### Step 3: Data Validation
```r
# Validate IPD structure
validate_ipd <- function(data, outcome_var, treatment_var, covariates = NULL) {
  errors <- character()
  warnings <- character()


  # Check required columns exist
  required_cols <- c(outcome_var, treatment_var)
  if (!is.null(covariates)) required_cols <- c(required_cols, covariates)

  missing_cols <- setdiff(required_cols, names(data))
  if (length(missing_cols) > 0) {
    errors <- c(errors, paste("Missing columns:", paste(missing_cols, collapse = ", ")))
  }

  # Check outcome type
  if (outcome_var %in% names(data)) {
    outcome_vals <- unique(data[[outcome_var]])
    if (all(outcome_vals %in% c(0, 1, NA))) {
      message("Detected binary outcome")
    } else if (is.numeric(data[[outcome_var]])) {
      message("Detected continuous outcome")
    }
  }

  # Check treatment levels
  if (treatment_var %in% names(data)) {
    n_trt <- length(unique(data[[treatment_var]]))
    if (n_trt < 2) {
      errors <- c(errors, "Treatment variable must have at least 2 levels")
    }
    message(sprintf("Found %d treatment levels", n_trt))
  }

  # Check for missing values
  if (any(is.na(data[required_cols]))) {
    n_missing <- sum(!complete.cases(data[required_cols]))
    warnings <- c(warnings, sprintf("%d observations with missing values", n_missing))
  }

  list(
    valid = length(errors) == 0,
    errors = errors,
    warnings = warnings,
    n_obs = nrow(data),
    n_complete = sum(complete.cases(data[required_cols]))
  )
}
```

### Step 4: Data Preparation (Recipe Pattern)
```r
# Create preparation recipe
create_itc_recipe <- function(data, outcome_var, treatment_var, covariates) {
  recipe <- list(
    # Step 1: Handle missing values
    handle_missing = function(d) {
      d[complete.cases(d[c(outcome_var, treatment_var, covariates)]), ]
    },

    # Step 2: Factor treatment
    factor_treatment = function(d) {
      d[[treatment_var]] <- factor(d[[treatment_var]])
      d
    },

    # Step 3: Center covariates (for STC/MAIC)
    center_covariates = function(d, centers = NULL) {
      if (is.null(centers)) {
        centers <- sapply(d[covariates], mean, na.rm = TRUE)
      }
      for (cov in covariates) {
        d[[paste0(cov, "_centered")]] <- d[[cov]] - centers[[cov]]
      }
      attr(d, "covariate_centers") <- centers
      d
    }
  )

  class(recipe) <- c("itc_recipe", "list")
  recipe
}

# Apply recipe
prep_itc_data <- function(data, recipe) {
  result <- data
  for (step_name in names(recipe)) {
    result <- recipe[[step_name]](result)
  }
  result
}
```

### Step 5: Analysis Workflow
```r
# Unified analysis interface
run_itc_analysis <- function(
  method = c("pairwise_ma", "nma", "maic", "stc", "ml_nmr"),
  ...
) {
  method <- match.arg(method)

  # Dispatch to appropriate function
  result <- switch(method,
    pairwise_ma = run_pairwise_ma(...),
    nma = run_nma(...),
    maic = run_maic(...),
    stc = run_stc(...),
    ml_nmr = run_ml_nmr(...)
  )

  # Add common metadata
  result$method <- method
  result$timestamp <- Sys.time()
  result$session_info <- sessionInfo()

  class(result) <- c("itc_result", class(result))
  result
}
```

### Step 6: Result Standardization
```r
# Standard result tibble format
standardize_itc_results <- function(result) {
  tibble::tibble(
    comparison = result$comparison,
    effect_measure = result$effect_measure,
    estimate = result$estimate,
    ci_lower = result$ci_lower,
    ci_upper = result$ci_upper,
    se = result$se,
    p_value = result$p_value,
    method = result$method,
    n_studies = result$n_studies %||% NA_integer_,
    n_patients = result$n_patients %||% NA_integer_,
    heterogeneity_i2 = result$i2 %||% NA_real_,
    heterogeneity_tau2 = result$tau2 %||% NA_real_
  )
}
```

## Reproducibility Best Practices

### 1. Seed Management
```r
# Set and document seed
ANALYSIS_SEED <- 12345

# Use in all stochastic operations
set.seed(ANALYSIS_SEED)
bootstrap_result <- boot::boot(..., R = 1000)

# For parallel operations
library(doRNG)
registerDoRNG(ANALYSIS_SEED)
```

### 2. Package Version Control
```r
# Use renv for package management
renv::init()
renv::snapshot()

# Document versions in output
cat("Package versions:\n")
packageVersion("meta")
packageVersion("netmeta")
packageVersion("maicplus")
```

### 3. Session Documentation
```r
# At end of analysis
sink("session_info.txt")
sessionInfo()
sink()

# Or more detailed
writeLines(capture.output(devtools::session_info()), "session_info.txt")
```

## Data Validation Patterns

### Binary Outcomes
```r
validate_binary_outcome <- function(data, outcome_var) {
  vals <- data[[outcome_var]]
  if (!all(vals %in% c(0, 1, NA))) {
    stop("Binary outcome must contain only 0, 1, or NA")
  }
  if (all(vals == 0, na.rm = TRUE) || all(vals == 1, na.rm = TRUE)) {
    warning("All outcomes are identical - check data")
  }
  invisible(TRUE)
}
```

### Survival Outcomes
```r
validate_survival_outcome <- function(data, time_var, event_var) {
  if (any(data[[time_var]] < 0, na.rm = TRUE)) {
    stop("Survival times must be non-negative")
  }
  if (!all(data[[event_var]] %in% c(0, 1, NA))) {
    stop("Event indicator must be 0, 1, or NA")
  }
  invisible(TRUE)
}
```

### Aggregate Data
```r
validate_agd <- function(agd, required_fields) {
  missing <- setdiff(required_fields, names(agd))
  if (length(missing) > 0) {
    stop(sprintf("Missing AgD fields: %s", paste(missing, collapse = ", ")))
  }

  # Check numeric fields are positive
  numeric_fields <- c("n_total", "n_events", "mean", "sd")
  for (field in intersect(numeric_fields, names(agd))) {
    if (any(agd[[field]] < 0, na.rm = TRUE)) {
      stop(sprintf("Field '%s' contains negative values", field))
    }
  }
  invisible(TRUE)
}
```

## Result Tibble Standards

All ITC results should return tibbles with consistent column naming:

| Column | Type | Description |
|--------|------|-------------|
| comparison | character | "A vs B" format |
| effect_measure | character | "OR", "HR", "MD", etc. |
| estimate | numeric | Point estimate |
| ci_lower | numeric | Lower CI bound |
| ci_upper | numeric | Upper CI bound |
| se | numeric | Standard error |
| p_value | numeric | P-value |
| method | character | Analysis method |

## Common Anti-Patterns to Avoid

### 1. Hardcoded Values
```r
# Bad
data <- data[data$age > 65, ]

# Good
AGE_THRESHOLD <- 65
data <- data[data$age > AGE_THRESHOLD, ]
```

### 2. Missing Validation
```r
# Bad
result <- maic_anchored(weights, ipd, pseudo_ipd)

# Good
stopifnot(inherits(weights, "maicplus_estimate_weights"))
stopifnot(nrow(ipd) > 0)
result <- maic_anchored(weights, ipd, pseudo_ipd)
```

### 3. Unreproducible Operations
```r
# Bad
bootstrap_ci <- boot::boot.ci(boot_result)

# Good
set.seed(12345)
boot_result <- boot::boot(data, statistic, R = 1000)
bootstrap_ci <- boot::boot.ci(boot_result)
```

## Resources

- TMwR Book: https://www.tmwr.org/
- tidymodels: https://www.tidymodels.org/
- NICE DSU TSD 18: Population-adjusted indirect comparisons
