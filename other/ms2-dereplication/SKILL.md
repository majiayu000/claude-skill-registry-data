---
name: ms2-dereplication
description: Use when you have MS2 tandem mass spectrometry data in .mzML format and
  need to match unknown spectra against a reference library (GNPS, HMDB, MassBank)
  to identify which known compounds are present in your sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Spectra
  - R
  - SIRIUS
  - MetFrag
  - GNPS
  - HMDB
  - MassBank
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-023-00695-y
  title: MAW
evidence_spans:
- performs spectral database dereplication using R Package
- spectral database dereplication using R Package Spectra
- workflow takes MS2 .mzML format data files as an input in R
- compound database dereplication using SIRIUS OR MetFrag
- compound database dereplication using SIRIUS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  dedup_kept_from: coll_maw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00695-y
  all_source_dois:
  - 10.1186/s13321-023-00695-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 spectral database dereplication

## Summary

Identifies and ranks matching spectra from MS2 .mzML input files against reference spectral libraries using the Spectra R package, producing a ranked table of spectral matches with similarity scores and metadata. This is the first step in untargeted metabolomics annotation that filters noise and establishes spectral identity before compound structure prediction.

## When to use

You have MS2 tandem mass spectrometry data in .mzML format and need to match unknown spectra against a reference library (GNPS, HMDB, MassBank) to identify which known compounds are present in your sample. Apply this skill when spectral similarity matching is a prerequisite for downstream compound annotation or when you want to prioritize high-confidence spectral hits before more computationally expensive structure prediction steps.

## When NOT to use

- Input data is already in a format other than .mzML (e.g., .raw, .d, or pre-processed feature tables); use format conversion tools first.
- You have no reference spectral library available or your target compounds are novel/not present in public databases; in this case skip to in silico structure prediction.
- Your goal is qualitative presence/absence only and you do not need ranked similarity scores or metadata enrichment; simpler spectral matching approaches may suffice.

## Inputs

- MS2 .mzML format data files (mass spectrometry data with fragmentation spectra)
- Reference spectral library objects in R format (e.g., gnps.rda, hmdb.rda, mbankNIST.rda)
- Precursor mass tolerance parameter (ppm, e.g., 15 ppm)

## Outputs

- Spectral match results CSV file (e.g., spectral_results.csv) with columns: matched spectrum ID, reference library ID, similarity score, collision energy, and other metadata
- Per-spectrum matched candidate list ranked by similarity score
- Directory structure with per-library subdirectories (GNPS, HMDB, MassBank) containing detailed match information

## How to apply

Load MS2 .mzML format data files into R using the Spectra package. Execute spectral database dereplication against reference spectral libraries (GNPS, HMDB, MassBank) using Spectra's matching functions with a precursor mass tolerance (typically 15 ppm as used in MAW). For each query spectrum, rank candidate matches by cosine similarity or other spectral similarity metrics. Generate and export a table of spectral matches with match scores, database identifiers, collision energy metadata, and supporting information. The matched spectra serve as input for subsequent compound database dereplication via SIRIUS or MetFrag.

## Related tools

- **Spectra** (Performs spectral database matching and dereplication against reference libraries; core tool that loads .mzML files and ranks spectral similarity) — https://rformassspectrometry.github.io/Spectra/
- **R** (Runtime environment in which Spectra is executed and spectral matching workflow is orchestrated)
- **GNPS** (Reference spectral library database (pre-loaded as gnps.rda R object) against which query spectra are matched)
- **HMDB** (Reference spectral library database (pre-loaded as hmdb.rda R object) used for spectral matching)
- **MassBank** (Reference spectral library database (pre-loaded as mbankNIST.rda R object) used for spectral matching)

## Examples

```
Rscript --no-save --no-restore --verbose Workflow_R_Script_all_MetFrag.r sample.mzML gnps.rda hmdb.rda mbankNIST.rda 15 TRUE
```

## Evaluation signals

- Output CSV file has expected columns: reference library identifier, query spectrum ID, similarity/match score, and collision energy metadata; file is not empty and contains ≥1 matched spectrum per precursor mass queried.
- Spectral match scores (e.g., cosine similarity) fall within expected range (0–1 or 0–100%) and are sorted in descending order within each spectrum group.
- Each query spectrum has ≥1 matched candidate from at least one reference library; check that precursor mass tolerance (15 ppm) was correctly applied by verifying matched mass differences are within tolerance.
- Output directory structure mirrors reference library organization (GNPS/, HMDB/, MassBank/ subdirectories populated); verify no empty directories or missing metadata columns.
- Downstream compound database dereplication (SIRIUS/MetFrag) successfully accepts the spectral match output file as input without schema errors.

## Limitations

- Matching quality depends on reference library coverage and spectral similarity threshold; novel or poorly ionized compounds may not be matched despite being present.
- Spectral noise, variable collision energies, and instrument differences can reduce matching sensitivity; recommend quality filtering of input spectra (signal-to-noise ratio, peak counts) before dereplication.
- The workflow uses pre-computed, static database snapshots (e.g., GNPS saved 2023-01-09, HMDB v5.0, MassBank 2022.12); updates to public databases require re-downloading and re-running the workflow.
- CWL version of MAW supports MetFrag downstream but SIRIUS integration is only available in Docker containers; this constrains deployment flexibility if you require SIRIUS.
- Large .mzML files (>10 precursor masses) may require HPC resources and SLURM batch submission; single-machine execution on large files is slow (≈2 minutes per precursor mass on 64 GB Ubuntu system).

## Evidence

- [intro] performs spectral database dereplication using R Package Spectra and compound database dereplication using SIRIUS OR MetFrag: "performs spectral database dereplication using R Package Spectra and compound database dereplication using SIRIUS OR MetFrag"
- [other] workflow takes MS2 .mzML format data files as input in R and performs spectral database dereplication using the Spectra R package: "The workflow takes MS2 .mzML format data files as input in R and performs spectral database dereplication using the Spectra R package."
- [other] Execute spectral database dereplication against a reference spectral library using Spectra to identify and rank matching spectra: "Execute spectral database dereplication against a reference spectral library using Spectra to identify and rank matching spectra."
- [readme] 15 = ppm for spectral database dereplication precursor matches: "15 = ppm for spectral database dereplication precursor matches"
- [readme] with CWL, only MetFrag version of MAW is available at the moment: "with CWL, only MetFrag version of MAW is available at the moment"
- [readme] one precursor mass takes 2 minutes on an Ubuntu system with 64GB RAM to run Workflow_R_Script_all_MetFrag.r: "one precursor mass takes 2 minutes on an Ubuntu system with 64GB RAM to run Workflow_R_Script_all_MetFrag.r"
