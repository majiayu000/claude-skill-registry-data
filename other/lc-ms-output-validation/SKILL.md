---
name: lc-ms-output-validation
description: Use when after executing a Nextflow-based LC-HRMS metabolomics workflow with Docker or Singularity containerization on .mzML LC-MS data, before proceeding to downstream statistical or visualization analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Docker
  - Singularity
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- containerized workflow MS-DIAL -> MSFLO
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial
schema_version: 0.2.0
---

# LC-MS output validation

## Summary

Verification that containerized LC-HRMS metabolomics workflows have completed all pipeline stages without error and produced expected output artifacts with correct format and content. This skill ensures data integrity and reproducibility when using Docker or Singularity-containerized MS-DIAL → MSFLO processing pipelines on .mzML LC-MS datasets.

## When to use

After executing a Nextflow-based LC-HRMS metabolomics workflow with Docker or Singularity containerization on .mzML LC-MS data, before proceeding to downstream statistical or visualization analyses. Use this skill to confirm that peak detection, chromatogram alignment, and metabolite identification stages all completed successfully and produced the expected feature tables and aligned data matrices in the designated output directory.

## When NOT to use

- Input dataset is not in .mzML or .abf format—convert with ProteoWizard msConvert or Reifycs Abf Converter first
- Workflow executed without Docker or Singularity containerization—validation signals depend on containerized environment reproducibility
- Output files have already been validated and used for downstream analyses—re-validation is redundant unless workflow re-execution or data integrity concern arises

## Inputs

- .mzML LC-MS raw data files (input dataset)
- Nextflow execution logs (execution.log, execution_report.html, execution_timeline.html)
- Designated results output directory from containerized workflow run
- MS-DIAL and MS-FLO configuration files (msdial_params.txt, msflo_params.ini)
- MS1 and MS2 reference libraries (ms1_lib.txt, ms2_lib.msp)

## Outputs

- Validated feature tables (.tsv format, converted from .msdial files)
- Aligned data matrices (.tsv files with aligned peak intensities across samples)
- Processed metabolite annotations with identifications
- Execution validation report (confirmation of all pipeline stages completion)

## How to apply

Monitor workflow execution logs (execution.log) and the execution_report.html for completion status and resource usage metrics. Verify presence of all expected output files in the results directory, checking for feature tables, aligned data matrices (.tsv files converted from .msdial), and processed metabolite annotations. Validate file integrity by opening output .tsv files in spreadsheet software and confirming expected columns (m/z, retention time, intensity values, metabolite names) and row counts matching the input sample count. Cross-reference the execution_timeline.html to ensure each pipeline process (peak detection, alignment, identification) completed without timeout or resource exhaustion. If any process was skipped or error.txt is present, trace failures to input file format, missing reference libraries (ms1_lib.txt, ms2_lib.msp), or misconfigured MS-DIAL/MS-FLO parameter files before re-execution.

## Related tools

- **Nextflow** (Workflow orchestration and execution monitoring; generates execution_report.html, execution_timeline.html, and logs for validation) — https://www.nextflow.io/
- **MS-DIAL** (Peak detection, alignment, and metabolite identification; produces .msdial output files that must be validated and converted to .tsv)
- **MSFLO** (Post-processing and annotation refinement after MS-DIAL; produces final feature tables and aligned matrices)
- **Docker** (Container runtime for reproducible local execution of MS-DIAL → MSFLO pipeline; enables validation of containerized environment consistency) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC execution; used for validation on systems like HiPerGator) — https://www.sylabs.io/guides/3.0/user-guide/

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log; grep -i 'error\|failed' logs/execution.log; ls -lh results/
```

## Evaluation signals

- Execution logs (execution.log) show completion of all pipeline stages without error messages; error.txt is absent or empty
- All expected output files are present in the results directory with non-zero file sizes (.tsv feature tables, aligned data matrices, annotation files)
- Output .tsv files open correctly in spreadsheet software and contain expected columns (m/z, retention time, intensity values, metabolite identifications) with row counts matching input sample count
- execution_report.html shows successful completion status and resource usage within allocated limits; execution_timeline.html displays all processes with green completion status
- File naming conventions follow expected pattern (sample IDs match input .mzML file names); no special characters present in processed filenames that would indicate skipped processing

## Limitations

- No explicit statement of reproducibility validation or testing is provided in the initial release; validation relies on log inspection and output file presence rather than formal test suites
- No version information provided for MS-DIAL or MSFLO tools in workflow configuration, making it difficult to verify tool-specific parameter compatibility across software updates
- Special characters in input file names cause processing failures; workflow silently skips affected samples without explicit error reporting, requiring manual filename inspection before re-execution
- High-performance computing environments may report CPU allocation mismatches (e.g., 'Process requirement exceed available CPUs') if --max_cpus is not correctly configured in the HPC profile, requiring adjustment before revalidation

## Evidence

- [other] Validate presence and integrity of expected output files (feature tables, aligned data matrices, processed annotations) in the designated output directory.: "Validate presence and integrity of expected output files (feature tables, aligned data matrices, processed annotations) in the designated output directory."
- [readme] The file extensions for produced `.msdial` files have been changed to `.tsv` so the files can be opened in spreadsheet software such as Microsoft Excel.: "The file extensions for produced `.msdial` files have been changed to `.tsv` so the files can be opened in spreadsheet software such as Microsoft Excel."
- [readme] Example execution logs are stored in the `logs` folder.: "`execution_report.html` summarizes workflow runtime and computational resource usage. `execution_timeline.html` shows the execution timeline for each process."
- [readme] To avoid unexpected errors, do not use special characters in file names.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [other] Monitor workflow execution logs and verify that all pipeline stages complete without error.: "Monitor workflow execution logs and verify that all pipeline stages complete without error."
