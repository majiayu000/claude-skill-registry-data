---
name: r-cmd-check-validation
description: Use when after installing an R package from a non-CRAN repository (such as r-universe) to confirm the package build is sound, dependencies resolve correctly, and no warnings or errors are introduced. Use it as a gate before relying on the package for downstream analysis or distribution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - R
  - R-CMD-check
  - GitHub Actions
  - r-universe
  - install.packages()
  - library()
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
evidence_spans:
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima
schema_version: 0.2.0
---

# r-cmd-check-validation

## Summary

Automated validation of R package build integrity and CRAN compliance using the R-CMD-check test suite, typically run via GitHub Actions CI/CD workflows. This skill verifies that a package installs successfully, loads without errors, and passes all checks against the CRAN submission checklist.

## When to use

Apply this skill after installing an R package from a non-CRAN repository (such as r-universe) to confirm the package build is sound, dependencies resolve correctly, and no warnings or errors are introduced. Use it as a gate before relying on the package for downstream analysis or distribution.

## When NOT to use

- Package is already on CRAN; use CRAN's native check infrastructure instead.
- Package installation has not yet been attempted; first confirm basic install.packages() works before running R-CMD-check.
- Local development environment lacks R development tools (Rtools on Windows, build-essential on Linux) needed for R-CMD-check.

## Inputs

- R package source code (GitHub repository)
- Package repository URL (e.g., r-universe registry)
- GitHub Actions workflow configuration (.github/workflows/R-CMD-check.yaml)

## Outputs

- R-CMD-check test report (pass/fail status)
- CI badge status (displayed in README)
- Installation verification (no error/warning log)
- Package load confirmation (library() call succeeds)

## How to apply

First, configure R to use the r-universe repository as a package source by specifying the repository URL in install.packages(). Install the target package (e.g., tima) using install.packages() with the configured repository, then load it into the R environment with library(package_name) and verify no errors occur. Finally, run R-CMD-check on the installed package to validate against the CRAN submission checklist. The R-CMD-check workflow should be configured in the package's GitHub Actions (typically in .github/workflows/R-CMD-check.yaml) and the results tracked via a CI badge in the README. A passing check indicates all tests pass and the package meets CRAN standards.

## Related tools

- **R-CMD-check** (Automated test harness validating package build, dependencies, and CRAN compliance) — https://github.com/r-lib/rcmdcheck
- **GitHub Actions** (CI/CD workflow engine executing R-CMD-check on every commit/PR and publishing badge status) — https://github.com/features/actions
- **r-universe** (Package repository providing pre-built binaries and automated R-CMD-check results) — https://r-universe.dev
- **install.packages()** (R base function to download and install package from specified repository)
- **library()** (R base function to load installed package into environment and verify no load-time errors)

## Examples

```
install.packages("tima", repos = c("https://taxonomicallyinformedannotation.r-universe.dev", "https://bioconductor.org/packages/release/bioc", "https://cloud.r-project.org")); library(tima)
```

## Evaluation signals

- R-CMD-check workflow in GitHub Actions completes successfully (all checks pass) with green status badge visible in README.
- install.packages(package_name, repos=c('r-universe_url', ...)) completes without errors or unresolved dependency warnings.
- library(package_name) executes without errors or critical warnings in R console.
- No unexpected NOTE, WARNING, or ERROR messages appear in R-CMD-check report logs.
- Package version badge from r-universe updates in sync with repository releases, confirming automated build pipeline is active.

## Limitations

- R-CMD-check validates against CRAN standards but does not guarantee functional correctness or scientific validity of the package's algorithms.
- CI workflows depend on GitHub Actions availability and correct .yaml configuration; misconfigured workflows may report false negatives.
- r-universe automatic builds require the repository to be registered and may lag behind local development if CI/CD is not actively configured.
- Tests passed on GitHub Actions (Linux container) do not guarantee cross-platform compatibility on Windows or macOS without explicit platform-specific workflow steps.

## Evidence

- [other] research_question: "Does the tima R package install successfully from the r-universe repository and pass its R-CMD-check test suite?"
- [other] workflow_confirmation: "Install the TIMA package using install.packages() with the configured repository. 3. Load the installed package into the R environment using library(tima) and confirm no errors occur. 4. Run"
- [readme] installation_instruction: "As the package is not (yet) available on CRAN, you will need to install with: install.packages( "tima", repos = c( "https://taxonomicallyinformedannotation.r-universe.dev","
- [readme] load_verification: "Then, you should be able to install the rest with: tima::install_tima()"
- [readme] ci_badge_confirmation: "[![R-CMD-check](https://github.com/taxonomicallyinformedannotation/tima/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/taxonomicallyinformedannotation/tima/actions/workflows/R-CMD-c"
