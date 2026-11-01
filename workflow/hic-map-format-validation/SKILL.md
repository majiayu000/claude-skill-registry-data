---
name: hic-map-format-validation
description: Use when after running the ENCODE Hi-C uniform processing pipeline or Juicer on FASTQ input data and generating a .hic output file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)
  - GNU coreutils (md5sum, sha256sum)
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_juicer
    doi: 10.1016/j.cels.2016.07.002
    title: juicer
  dedup_kept_from: coll_juicer
schema_version: 0.2.0
---

# hic-map-format-validation

## Summary

Validate Hi-C contact map output files against format specifications and reference checksums to confirm pipeline reproducibility and data integrity. This skill verifies that .hic binary format files produced by Hi-C processing pipelines conform to ENCODE reference standards and have not been corrupted during processing.

## When to use

After running the ENCODE Hi-C uniform processing pipeline or Juicer on FASTQ input data and generating a .hic output file. Use this skill whenever you need to verify that the generated Hi-C map file matches the expected format specification and matches a known-good reference output, particularly in contexts where reproducibility and data integrity are critical (e.g., ENCODE submissions, quality assurance workflows, or collaborative analyses).

## When NOT to use

- Input file is not a .hic binary format (e.g., if output is in BAM, SAM, or text-based contact matrix formats instead)
- No reference checksum is available or accessible for comparison
- Pipeline parameters or input FASTQ datasets intentionally differ from the reference, making bit-identical reproduction impossible

## Inputs

- .hic binary file (Hi-C contact map output from ENCODE Hi-C uniform processing pipeline or Juicer)
- ENCODE reference .hic file checksum (MD5 or SHA256 hash)

## Outputs

- Computed checksum for the generated .hic file
- Checksum comparison result (match/mismatch)
- Validation report confirming format and integrity status

## How to apply

First, ensure the output Hi-C map is in the expected .hic binary format produced by the encode_hic_pipeline wrapper or Juicer's Hi-C file creation step. Compute a checksum or cryptographic hash (e.g., MD5, SHA256) of the generated .hic file using standard GNU coreutils (md5sum or sha256sum). Compare the computed checksum against the ENCODE reference output checksum for the same input dataset. If checksums match exactly, the pipeline output is reproducible and the file has not been corrupted. If checksums differ, investigate whether pipeline parameters, tool versions, or input data differ from the reference run. This approach leverages the fact that Juicer's deterministic processing should produce bit-identical outputs when given identical inputs and parameters.

## Related tools

- **Juicer** (Pipeline that generates Hi-C maps from fastq raw data files, producing the .hic binary file to be validated) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)** (ENCODE-specific wrapper around Juicer that standardizes Hi-C map generation and produces reference output for validation) — https://github.com/ENCODE-DCC/hic-pipeline
- **GNU coreutils (md5sum, sha256sum)** (Compute cryptographic checksums of .hic files for integrity verification) — https://www.gnu.org/software/coreutils/

## Examples

```
md5sum output.hic && echo 'Compare with reference: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'
```

## Evaluation signals

- Computed checksum matches the ENCODE reference checksum exactly, indicating bit-identical reproducibility
- .hic output file is readable and conforms to the binary format specification (e.g., can be opened by Juicer Tools)
- File size and creation timestamp are consistent with expected pipeline runtime
- No corruption indicators such as truncated file size or invalid binary headers detected
- Checksum mismatch with reference can be traced to intentional differences in pipeline parameters or input data

## Limitations

- Checksum validation requires a known-good reference output; for new datasets or parameter configurations without reference checksums, validation must rely on format compliance checks instead
- Bit-identical reproducibility is sensitive to differences in tool versions (Juicer 1.6 vs. Juicer 2), cluster software (SLURM, LSF, UGER), and computational environment; the README notes that Juicer 2 is under active development and may produce different outputs
- No changelog is available for Juicer releases, making it difficult to trace what changes between versions might affect reproducibility
- Validation only confirms format and file integrity; it does not verify the biological correctness or quality of the Hi-C contact map itself (e.g., coverage, resolution, or presence of artifacts)

## Evidence

- [other] Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash. Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness.: "Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash. Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline"
- [other] Juicer includes a pipeline for generating Hi-C maps from fastq raw data files, which forms the basis for ENCODE's Hi-C uniform processing pipeline.: "Juicer includes a pipeline for generating Hi-C maps from fastq raw data files, which forms the basis for ENCODE's Hi-C uniform processing pipeline."
- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps: "pipeline for generating Hi-C maps from fastq raw data files"
- [readme] The main repository on Github is now focused on the Juicer 2.0 release and is under active development.: "The main repository on Github is now focused on the Juicer 2.0 release and is under active development."
- [readme] The minimum software requirement to run Juicer is a working Java installation (version >= 1.8) on Windows, Linux, and Mac OSX.: "The minimum software requirement to run Juicer is a working Java installation (version >= 1.8)"
