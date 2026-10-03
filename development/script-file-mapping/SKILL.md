---
name: script-file-mapping
description: Use when you have edited core algorithm scripts in the Core-Match GitHub
  repository and need to integrate those changes into a locally installed LipidMatch-4.2
  distribution (downloaded from innovativeomics.com). The trigger is the presence
  of modified .
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - R
  - LipidMatch
  - FluoroMatch
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1007/s00216-021-03392-7
  title: FluoroMatch 2.0
evidence_spans:
- put Modular.r into two directories
- 'put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution`'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fluoromatch_2_0_cq
    doi: 10.1007/s00216-021-03392-7
    title: FluoroMatch 2.0
  dedup_kept_from: coll_fluoromatch_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-021-03392-7
  all_source_dois:
  - 10.1007/s00216-021-03392-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the script-file placement layout into the LipidMatch-4.2 distribution directories

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Maps edited R script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) from a development repository to their correct target locations within both Flow and Modular versions of the LipidMatch-4.2 distribution to integrate developer changes into the installed software framework.

## When to use

You have edited core algorithm scripts in the Core-Match GitHub repository and need to integrate those changes into a locally installed LipidMatch-4.2 distribution (downloaded from innovativeomics.com). The trigger is the presence of modified .r files that must replace existing code in specific subdirectories for both the Flow workflow version and the Modular interactive version.

## When NOT to use

- You are downloading LipidMatch-4.2 for the first time as an end user; use the stable release directly from innovativeomics.com/software instead of integrating developer scripts.
- Your edited scripts are not in the R language or do not match the four core file names (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R).
- You have not yet installed the base LipidMatch-4.2 distribution locally and lack the target directory structure to validate against.

## Inputs

- Modular.r (edited R script file)
- genEIC.r (edited R script file)
- MS1Spectragen.r (edited R script file)
- Stats.R (edited R script file)
- LipidMatch-4.2 distribution directory (installed locally from innovativeomics.com)

## Outputs

- Script placement manifest (CSV or JSON mapping source files to target paths)
- Directory tree or layout document showing final file placement structure
- Updated LipidMatch-4.2 distribution with integrated script files

## How to apply

First, identify the four edited script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) from your development work. Next, consult the LipidMatch-4.2 distribution directory structure installed locally from innovativeomics.com. Modular.r must be placed into two separate directories to replace existing code: `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular`. The remaining three scripts (genEIC.r, MS1Spectragen.r, Stats.R) must all be placed into the shared library scripts directory: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`. Create a manifest file (CSV or JSON) that maps each source script to its target path(s). Validate that all target directories exist in your distribution before copying files. Generate a directory tree showing the final placement to confirm the layout matches the expected structure.

## Related tools

- **LipidMatch** (Target software framework into which edited scripts are integrated; both Flow and Modular versions require specific script file placement.) — https://github.com/InnovativeOmics/Core-Match
- **FluoroMatch** (Companion software distribution sharing the Modular version directory structure; Modular.r must be placed in FluoroMatch_Modular directory.) — https://github.com/InnovativeOmics/Core-Match
- **R** (Language and runtime environment for the script files being mapped and integrated.)

## Evaluation signals

- All four source scripts (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) are successfully copied to their respective target paths without errors.
- Modular.r exists in both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular` directories (replacing existing code).
- genEIC.r, MS1Spectragen.r, and Stats.R all reside in `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`.
- Directory tree or manifest document lists all target paths and confirms file count matches expected placement (2 copies of Modular.r + 3 copies of other scripts = 5 total file placements).
- LipidMatch-4.2 software launches successfully with FLOW parameter toggled correctly (FLOW <- FALSE for Modular; FLOW <- TRUE for Flow) and recognizes the integrated scripts without errors.

## Limitations

- The mapping process assumes the target LipidMatch-4.2 distribution directory structure already exists locally; if directories are missing, they must be created or obtained from innovativeomics.com.
- No changelog is provided in the Core-Match repository documentation, so developers must manually track which scripts were edited and by whom.
- Manual file copying is required; no automated build or deployment script is documented for integrating changes into the distribution.

## Evidence

- [readme] developers should edit main algorithms in the github repository, then integrate code by placing edited code in correct directory from downloaded distribution: "**Developers can edit the main algorithms here on github** as a team. Then the code needs to be integrated by placing the edited code in the correct directory from the downloaded distribution"
- [readme] Modular.r must replace existing code in two specific directories: "If edited, put Modular.r into two directories (replace existing code):

`LipidMatch-4.2\Flow\LipidMatch_Distribution`

`LipidMatch-4.2\FluoroMatch_Modular`"
- [readme] genEIC.r, MS1Spectragen.r, and Stats.R must be placed in the LipidMatch_Libraries/Scripts directory: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into:

`LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [readme] installation and integration workflow begins with downloading from InnovativeOmics.com: "Install FluoroMatch or LipidMatch from InnovativeOmics.com"
