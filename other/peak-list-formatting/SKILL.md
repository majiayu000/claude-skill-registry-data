---
name: peak-list-formatting
description: Use when after successfully resolving a USI string to a specific mass
  spectrum scan, and before performing spectral matching, library search, or comparative
  analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - GNPS LCMS Visualization Dashboard
  - GNPS Data Repository API
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01339-5
  all_source_dois:
  - 10.1038/s41592-021-01339-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-list-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert resolved mass spectrometry scan data into structured peak lists (m/z and intensity pairs) for downstream analysis, export, or integration with other tools. This skill bridges raw spectrum retrieval and machine-readable output formats suitable for annotation, quantification, or comparison workflows.

## When to use

After successfully resolving a USI string to a specific mass spectrum scan, and before performing spectral matching, library search, or comparative analysis. Apply this skill when you have retrieved raw spectrum metadata and peak data from GNPS, MassIVE, or MetaboLights repositories and need to extract, validate, and export the peak list in a format compatible with downstream tools (CSV, JSON, or mzML).

## When NOT to use

- The input is already a feature table or quantification matrix; this skill formats individual scans, not aggregated or normalized matrices.
- You are working with centroided data that has already been exported and does not require re-export or reformatting.
- The workflow requires real-time visualization rather than static file export; use the GNPS LCMS Visualization Dashboard directly instead.

## Inputs

- Resolved mass spectrum scan data (m/z–intensity pairs from a GNPS analysis task, MassIVE dataset, or MetaboLights project)
- Scan metadata (scan number, precursor m/z, MS level, scan type from USI or GNPS LCMS Dashboard)
- Target output format specification (CSV, JSON, or mzML)

## Outputs

- Structured peak list file (CSV or JSON format with m/z and intensity columns/fields)
- Optionally: annotated peak list with retention time, scan identifier, and metadata headers
- Validation report (peak count, m/z range, intensity statistics)

## How to apply

Once a USI has been resolved to extract spectrum metadata and scan data (via GNPS LCMS Visualization Dashboard or programmatic API), parse the peak data to isolate m/z (mass-to-charge) and intensity pairs. Format these pairs as a structured table or JSON object with consistent decimal precision and intensity normalization. Validate that peak counts and m/z ranges match the scan header metadata (e.g., scan number, precursor m/z, scan type). Export the formatted peak list to CSV (tab- or comma-delimited) or JSON, ensuring all rows/objects conform to the chosen schema. Apply quality filters if specified by the downstream workflow (e.g., intensity threshold, m/z range restriction).

## Related tools

- **GNPS LCMS Visualization Dashboard** (Retrieve spectrum metadata and peak data from resolved USI; visualize and validate peaks before export) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard
- **GNPS Data Repository API** (Programmatic access to fetch spectrum scans and metadata; alternative to dashboard for batch export)

## Evaluation signals

- Peak list contains exactly one m/z and one intensity value per row/object, with no null or malformed entries.
- All m/z values fall within the expected range for the instrument and scan type (e.g., 50–2000 m/z for small-molecule metabolomics).
- Peak count and m/z extrema match the scan header metadata retrieved from the resolved USI.
- Intensity values are numeric and non-negative; check for proper normalization if claimed (e.g., base peak at 999 or 100).
- Output file schema conforms to the chosen format (CSV headers match expected columns; JSON objects have consistent keys).

## Limitations

- Peak list formatting does not perform deisotoping, deconvolution, or feature detection; it exports raw centroided peaks as retrieved.
- Intensity values depend on the instrument vendor and data processing applied upstream; no standardization across GNPS, MassIVE, or MetaboLights sources is enforced by this skill.
- Large-scale batch export of thousands of scans may require custom scripting or API calls; the GNPS LCMS Dashboard is designed for interactive single- or few-file workflows.
- Retention time and MS/MS annotation are only included if present in the resolved scan metadata; not all USI sources provide complete metadata.

## Evidence

- [other] Fetch the peak list (m/z and intensity pairs) from the resolved scan. 4. Format and export the peak list as a structured output file (CSV or JSON).: "Fetch the peak list (m/z and intensity pairs) from the resolved scan. 4. Format and export the peak list as a structured output file (CSV or JSON)."
- [readme] mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171: "mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171"
- [readme] We aim to provide several APIs to programmatically get data.: "We aim to provide several APIs to programmatically get data."
