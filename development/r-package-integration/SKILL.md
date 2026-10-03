---
name: r-package-integration
description: Use when when you have a functional R package with core statistical or
  computational logic that needs to be made accessible to non-R users, or when you
  want to streamline a multi-step analytical workflow (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R package Amanida
  - R
  - Shiny
  - Amanida R package
  - webchem R package
  - Shiny Server / shinyapps.io
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1002/jrsm.1713
  title: Easy-Amanida
evidence_spans:
- implements the R package Amanida
- R package Amanida
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_easy_amanida_cq
    doi: 10.1002/jrsm.1713
    title: Easy-Amanida
  dedup_kept_from: coll_easy_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/jrsm.1713
  all_source_dois:
  - 10.1002/jrsm.1713
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Package Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Wrapping an existing R package (e.g., Amanida for metabolomic meta-analysis) into an interactive web application using Shiny, exposing its statistical and data-processing functions through a user-friendly browser interface with reactive input controls and downloadable outputs.

## When to use

When you have a functional R package with core statistical or computational logic that needs to be made accessible to non-R users, or when you want to streamline a multi-step analytical workflow (e.g., metabolomic compound harmonization + meta-analysis aggregation) into a single interactive application with visual feedback and result export.

## When NOT to use

- The R package has no public API or poorly documented function signatures — integration becomes opaque and unmaintainable.
- The workflow is a single, non-interactive computation with no iterative parameter tuning — overhead of Shiny development outweighs benefit.
- Real-time data streaming or high-performance computing is required — Shiny's reactive model may introduce latency bottlenecks.

## Inputs

- R package source code (installed and loaded)
- User-uploaded metabolomic datasets (aggregate statistics: p-values, fold-change values)
- Configuration parameters from web form inputs (meta-analysis settings, compound name harmonization rules)
- Sample/demo data for testing

## Outputs

- Interactive Shiny web dashboard
- Meta-analysis results (tables of harmonized compound statistics)
- Publication-ready plots (e.g., forest plots, volcano plots)
- Downloadable result files (CSV, images)
- Deployed web application URL

## How to apply

Clone the source repository to inspect the package's API and existing Shiny UI/server structure. Install the target R package (e.g., Amanida) and its dependencies, then load both the package and Shiny in your R environment. Map Shiny reactive input handlers (e.g., file upload, parameter sliders) to the package's core functions, ensuring data flows from UI inputs → package computation → reactive output displays. Implement output rendering for tables, plots, and downloadable results (e.g., CSV, images). Test locally with sample datasets (e.g., p-values and fold-change metadata for metabolomics), then deploy to a Shiny Server or hosted platform (e.g., shinyapps.io) to verify functionality.

## Related tools

- **Shiny** (Web application framework that exposes R package functions through reactive UI controls and renders outputs (plots, tables, downloads) in an interactive browser interface)
- **Amanida R package** (Core statistical package for metabolomic meta-analysis; Easy-Amanida wraps its functions to enable aggregation of p-values and fold-change across studies)
- **webchem R package** (Companion package used within Easy-Amanida for automated compound name harmonization during meta-analysis)
- **Shiny Server / shinyapps.io** (Deployment platform for hosting and serving the Shiny web application) — http://brui.shinyapps.io/easy-amanida

## Examples

```
shiny::runApp('~/easy-amanida'); # or deploy via rsconnect::deployApp('~/easy-amanida')
```

## Evaluation signals

- Shiny application runs without errors when launched locally (e.g., `shinyApp(ui, server)` executes and opens browser interface).
- File upload controls accept sample datasets and pass them successfully to underlying R package functions without data type mismatches.
- Reactive outputs (tables, plots) update when input parameters are modified, confirming data flow from UI → package → display.
- Downloaded result files (CSV, images) are non-empty, match expected schema, and contain correct computed values from the R package.
- Deployed application URL is accessible and responsive to user interactions on a public or private Shiny Server instance.

## Limitations

- The integration is only as robust as the underlying R package's error handling; unexpected input formats or edge cases in the package are not automatically caught by Shiny and may crash the app.
- Shiny's reactive model can introduce latency for computationally expensive R package functions; large metabolomic datasets may cause UI freezing if server-side computation is not optimized.
- No changelog was documented in the repository, making it difficult to track breaking changes or maintain backward compatibility if the wrapped R package is updated.

## Evidence

- [readme] Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida.: "Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida."
- [readme] Easy-Amanida is a new tool that combines two R packages, `amanida` and `webchem`, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds naming harmonization.: "combines two R packages, `amanida` and `webchem`, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds naming harmonization."
- [other] Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays.: "Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays."
- [other] Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard.: "Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard."
