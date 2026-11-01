---
name: juicer-cli-tool-execution
description: Use when you have a pre-generated .hic contact map file (from Juicer pipeline or external source) and need to systematically call chromatin loops, detect topologically associating domains, or annotate other structural features without re-running the full alignment and contact matrix construction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3179
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - juicer_cli_tools
  - Juicer (CLI tools suite)
  - Juicer 1.6
  - Juicer 2
  - ENCODE Hi-C uniform processing pipeline
  - Java Runtime Environment (JRE)
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans:
- Juicer is a platform for analyzing kilobase resolution Hi-C data
- command line tools for feature annotation on the Hi-C maps
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

# juicer-cli-tool-execution

## Summary

Execute Juicer command-line tools to annotate structural features (loops, domains) on pre-generated .hic contact maps. This skill bridges the gap between raw Hi-C map generation and downstream feature discovery by applying Juicer's post-processing CLI suite to identify and output genomic loop coordinates and topologically associating domain (TAD) boundaries.

## When to use

You have a pre-generated .hic contact map file (from Juicer pipeline or external source) and need to systematically call chromatin loops, detect topologically associating domains, or annotate other structural features without re-running the full alignment and contact matrix construction pipeline. This skill is appropriate when Hi-C data has already been processed to the contact map stage and feature annotation is the isolated requirement.

## When NOT to use

- Input is raw FASTQ sequence data—use the Juicer pipeline generation step first to create the .hic file.
- Contact map already includes feature annotations—re-annotation risks overwriting or conflicting with existing calls.
- Analysis requires real-time interaction with the map visualization—use Juicebox (the GUI) instead of CLI tools for exploratory work.

## Inputs

- .hic contact map file (pre-generated from Juicer pipeline or compatible source)
- genome identifier or reference file (e.g., 'hg19', 'mm10', or custom chrom.sizes)
- tool-specific parameters (e.g., resolution, p-value thresholds, GPU availability for HiCCUPS)

## Outputs

- annotated feature file in bedpe format (for loop coordinates: chr1, start1, end1, chr2, start2, end2, feature_id, score)
- annotated feature file in bed format (for domain boundaries: chr, start, end, domain_id, score)
- optional: feature statistics or confidence scores

## How to apply

Load the .hic file into Juicer command-line tools (which require Java >= 1.8 installed). Select the appropriate post-processing tool from the CLI suite—common tools include HiCCUPS for loop calling or Arrowhead for domain detection. Execute the chosen annotation tool with the .hic file as primary input, specifying kilobase resolution and any tool-specific parameters (e.g., peak-calling thresholds for HiCCUPS). The tool will scan the contact matrix for statistically significant peaks or domain boundaries and output results in a standardized coordinate format (typically bedpe for loops or bed for domains). Validate output by checking coordinate consistency with input map dimensions and confirming feature counts align with biological expectations for the organism and resolution.

## Related tools

- **Juicer (CLI tools suite)** (Core post-processing engine for feature annotation on Hi-C maps; provides loop-calling (HiCCUPS), domain detection (Arrowhead), and other structural annotation algorithms) — https://github.com/aidenlab/juicer
- **Juicer 1.6** (Stable release of Juicer with tested CLI tool implementations; recommended for production pipelines) — https://github.com/aidenlab/juicer/releases/tag/1.6
- **Juicer 2** (In-development version of Juicer with active feature additions; cloned by default from main repository) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline** (Cloud-optimized Juicer-based pipeline wrapper (Cromwell/WDL) for running Juicer including CLI tool stages; recommended for cloud/scalable execution) — https://github.com/ENCODE-DCC/hic-pipeline
- **Java Runtime Environment (JRE)** (Required runtime dependency for executing Juicer CLI tools; version >= 1.8 minimum) — https://www.java.com/download

## Examples

```
java -jar juicer_tools.jar hiccups -m 500 -r 10000 -k KR input.hic output_loops.bedpe
```

## Evaluation signals

- Output file format conforms to expected schema (bedpe for loops: 7+ tab-separated columns with valid genomic coordinates; bed for domains: 6+ columns with monotonic intervals)
- Coordinate ranges fall within the bounds of the input .hic map (e.g., all loop anchors map to chromosomes present in the reference and within chromosome length limits)
- Feature counts are consistent with biological expectations (e.g., mammalian genomes typically yield 5,000–10,000 loops and ~2,000–4,000 TADs at 40 kb resolution)
- Confidence scores or p-values in output show expected distributions (e.g., loop strength scores correlate with visual prominence in contact maps; domain boundaries coincide with regions of elevated intra-domain vs. inter-domain contact)
- Tool completes without Java exceptions or memory errors, and stderr logs indicate successful feature detection passes

## Limitations

- CLI tools require Java >= 1.8; older or beta Java versions may cause runtime failures or numerical instability.
- HiCCUPS loop calling requires a GPU (NVIDIA CUDA 7.0 or 7.5) for optimal performance; CPU fallback exists but is significantly slower.
- Juicer 2 is under active development and may introduce breaking changes; Juicer 1.6 is the stable release for production use.
- Output feature calls are resolution-dependent; features detected at 40 kb resolution will not directly translate to 5 kb or 10 kb resolutions.
- No changelog is available in the main repository, making it difficult to track CLI tool API changes between versions.

## Evidence

- [intro] command line tools for feature annotation on the Hi-C maps: "In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps"
- [readme] Juicer includes tools designed for feature annotation with output in standardized formats: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature"
- [readme] Java is the minimum software requirement for running Juicer tools: "The minimum software requirement to run Juicer is a working Java installation (version >= 1.8) on Windows, Linux, and Mac OSX."
- [readme] Version 1.6 is the last stable release; Juicer 2 is under active development: "To access Juicer 1.6 (last stable release), please see [the Github Release](https://github.com/aidenlab/juicer/releases/tag/1.6). If you clone the Juicer repo directly from Github, it will clone"
- [readme] CUDA is required for HiCCUPS peak calling with GPU acceleration: "You must have an NVIDIA GPU to install CUDA... The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5."
