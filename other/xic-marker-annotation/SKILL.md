---
name: xic-marker-annotation
description: Use when when you have a resolved spectrum file (mzML, mzXML) and need
  to visualize where MS2 precursor scans occur on an XIC display.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3694
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - GNPS LCMS Visualization Dashboard
  techniques:
  - LC-MS
  - CE-MS
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

# xic-marker-annotation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Overlay MS2 precursor scan positions as markers on extracted ion chromatograms (XICs) by parsing MS/MS metadata and annotating retention times or scan identifiers. This skill enables visual inspection of tandem mass spectrometry fragmentation events at their chromatographic positions.

## When to use

When you have a resolved spectrum file (mzML, mzXML) and need to visualize where MS2 precursor scans occur on an XIC display. Use this skill when the show_ms2_markers parameter is enabled and you want to cross-reference MS/MS fragmentation events with their chromatographic retention times or scan indices to validate data quality or support targeted ion tracking.

## When NOT to use

- Input spectrum contains only MS1 data with no MS2 scans — there are no precursor positions to mark.
- The ms2_identifier parameter is None or unspecified — markers cannot be anchored to specific MS2 events.
- Visualization does not require cross-referencing fragmentation events with chromatographic positions — simpler XIC display suffices.

## Inputs

- mzML spectrum file
- mzXML spectrum file
- MS2 identifier parameter (scan ID or retention time)
- show_ms2_markers flag (boolean)

## Outputs

- XIC chromatogram with MS2 marker overlays
- Structured marker position file (JSON, CSV, or TSV format)
- Annotated visualization with retention time / scan ID coordinates

## How to apply

Load the spectrum file into memory and parse MS/MS scan metadata to extract precursor scan indices and their associated retention times or scan identifiers. Filter and validate precursor positions to ensure they correspond to actual MS2 events in the spectrum file. Compile marker positions (retention time + scan ID pairs or single identifiers per precursor) into a structured output format (JSON, CSV, or TSV) compatible with XIC visualization. Pass the ms2_identifier parameter to the GNPS LCMS Visualization Dashboard with show_ms2_markers set to True to render the markers on the chromatogram overlay.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Renders XIC chromatograms with MS2 marker overlays when show_ms2_markers=True and ms2_identifier parameter is supplied) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Examples

```
https://gnps-lcms.ucsd.edu/?usi=mzspec%3AGNPS%3ATASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87%2Fdata%2FYao_Streptomyces%2Froseosporus%2F0518_s_BuOH.mzXML%3Ascan%3A171&xicmz=841.3170166%3B842.3170166&xic_tolerance=0.5&show_ms2_markers=1&ms2_identifier=MS2%3A1176
```

## Evaluation signals

- Marker positions align with actual MS2 scan indices in the spectrum metadata — verify via direct scan lookup in mzML/mzXML.
- Retention time coordinates of markers correspond to observed precursor peaks in the XIC trace — visual inspection confirms co-location.
- All MS2 events present in the spectrum file appear as markers when show_ms2_markers=True — no missing or spurious markers.
- Structured output file (JSON/CSV/TSV) contains valid retention time and scan ID pairs with no null or malformed entries.
- Dashboard URL rendering includes show_ms2_markers=True and a valid ms2_identifier without query errors.

## Limitations

- Marker overlay requires a valid ms2_identifier parameter; if None or missing, no markers are rendered.
- Spectrum file must be in mzML, mzXML, or equivalent format with accessible MS2 metadata; unsupported formats will fail during parsing.
- Retention time accuracy depends on instrument calibration and file export fidelity; mismatches between file metadata and actual scan timing may produce shifted markers.
- Large spectrum files with thousands of MS2 scans may incur rendering latency on the dashboard; performance degrades with dataset size.

## Evidence

- [other] When show_ms2_markers is set to True, the dashboard accepts an ms2_identifier parameter to mark MS2 precursor positions on the XIC display: "When show_ms2_markers is set to True, the dashboard accepts an ms2_identifier parameter to mark MS2 precursor positions on the XIC display"
- [other] Parse MS/MS (MS2) scan metadata to extract precursor scan indices and associated retention times or scan identifiers: "Parse MS/MS (MS2) scan metadata to extract precursor scan indices and associated retention times or scan identifiers"
- [other] Compile the set of marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output file (JSON, CSV, or TSV) suitable for XIC annotation: "Compile the set of marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output file (JSON, CSV, or TSV) suitable for XIC annotation"
- [other] Load the resolved spectrum file (mzML, mzXML, or equivalent format) into memory: "Load the resolved spectrum file (mzML, mzXML, or equivalent format) into memory"
- [other] Filter and validate precursor positions to ensure they correspond to actual MS2 events in the spectrum: "Filter and validate precursor positions to ensure they correspond to actual MS2 events in the spectrum"
- [readme] show_ms2_markers=1&ms2_identifier=MS2%3A1176: "show_ms2_markers=1&ms2_identifier=MS2%3A1176"
