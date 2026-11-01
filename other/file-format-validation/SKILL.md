---
name: file-format-validation
description: Use when when you have authored a custom .csv lipid library and need to confirm it adheres to LipidMatch's documented schema before placing it in the designated library directory and running the library integration/loading step.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - LipidMatch
  - Text editor or spreadsheet application (e.g., LibreOffice Calc, Excel)
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
---

# Validate .csv lipid library file format for LipidMatch integration

## Summary

Verify that a user-authored .csv lipid library conforms to LipidMatch's manual format specification before integration into the matching workflow. This ensures custom lipid entries with annotated m/z fragmentation patterns are correctly recognized and registered into the active library index.

## When to use

When you have authored a custom .csv lipid library and need to confirm it adheres to LipidMatch's documented schema before placing it in the designated library directory and running the library integration/loading step. Use this skill to prevent malformed entries from failing silent registration or producing incorrect candidate matches in downstream MS/MS analyses.

## When NOT to use

- The library is already in LipidMatch's native in-silico format (not a user-authored .csv import).
- You are validating MS/MS peak picking output (e.g., from MZmine, XCMS, MS-DIAL) rather than a lipid library source file.
- The .csv file is intended for a different lipidomics tool (e.g., LIPID MAPS, LipidBlast) with different schema requirements.

## Inputs

- .csv file with custom lipid entries
- LipidMatch manual (format specification documentation)
- Text editor or spreadsheet software for file review

## Outputs

- Validated .csv lipid library file ready for integration
- Validation report (pass/fail for schema compliance)
- Reformatted .csv (if corrections were needed)

## How to apply

Obtain the LipidMatch manual from the GitHub repository (GarrettLab-UF/LipidMatch) and review the documented .csv format specification. Author your test .csv lipid library to include at least 3–5 custom lipid entries, each with annotated m/z fragmentation patterns conforming to the manual's column structure and data types. Before integration, validate the .csv file structure: verify column headers match the specification, confirm all required fields are populated for each lipid entry, and check that m/z values are numeric and within physically plausible ranges for your instrument (e.g., Q-Exactive orbitrap, Q-TOF). Only after validation passes should you place the file in the LipidMatch library directory and execute the library integration step.

## Related tools

- **LipidMatch** (Target software that consumes the validated .csv library; defines the format specification and performs library integration/registration) — https://github.com/GarrettLab-UF/LipidMatch
- **Text editor or spreadsheet application (e.g., LibreOffice Calc, Excel)** (Tool for authoring, viewing, and manually inspecting .csv file structure before submission to LipidMatch)

## Evaluation signals

- All required columns named in the LipidMatch manual are present in the .csv header row with correct spelling and order.
- Every custom lipid entry row is complete: no missing or null fields in mandatory columns (e.g., lipid name, m/z, fragment ions).
- All m/z values are numeric, properly formatted (e.g., float with appropriate decimal precision), and within the expected mass range for the instrument(s) used in your workflow (e.g., 50–2000 m/z for Q-Exactive, 50–1700 m/z for Q-TOF).
- After LipidMatch library integration and a test matching run on a sample MS/MS dataset, at least one custom library entry appears in the output candidate list, confirming successful registration.
- No parsing errors or warnings are reported by the LipidMatch integration/loading step when the validated .csv is placed in the library directory.

## Limitations

- LipidMatch does not currently support Waters instrument files, so validation of a library for Waters data will still fail at the matching stage even if the .csv format is correct.
- The manual format specification is not version-controlled in the provided context; updates to the specification may not be reflected in older GitHub releases or documentation snapshots.
- Validation of .csv syntax does not confirm biological accuracy or fragmentation chemistry; entries may pass schema validation but produce incorrect or spurious matches if m/z patterns are incorrectly annotated.

## Evidence

- [other] Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns.: "Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns."
- [readme] LipidMatch allows for facile integration of user generated libraries for unique applications.: "LipidMatch allows for facile integration of user generated libraries for unique applications."
- [other] Place the .csv library file in the designated library directory within the LipidMatch installation.: "Place the .csv library file in the designated library directory within the LipidMatch installation."
- [other] Parse and inspect the output candidate list to confirm that at least one custom library entry appears ranked among the matching candidates.: "Parse and inspect the output candidate list to confirm that at least one custom library entry appears ranked among the matching candidates."
