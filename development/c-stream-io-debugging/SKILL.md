---
name: c-stream-io-debugging
description: Use when when a C++ program writes records to an output stream (e.g., SAM alignment file) and the final output file contains fewer records than expected based on upstream counts (e.g., salmon's NumReads total in quant.sf exceeds SAM record count), indicating buffered data loss at stream closure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0099
  tools:
  - pufferfish
  - salmon
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- pufferfish's SSHash k-mer lookup, now fixed upstream
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_salmon
    doi: 10.1038/nmeth.4197
    title: salmon
  dedup_kept_from: coll_salmon
schema_version: 0.2.0
---

# C++-stream-IO-debugging

## Summary

Diagnose and fix output stream buffer flushing bugs in C++ programs where buffered records are lost at stream closure, causing incomplete output files. This skill detects the symptom (output record count mismatches quantification totals) and applies the fix (explicit ostream buffer flush before close) to ensure all in-flight data reaches disk.

## When to use

When a C++ program writes records to an output stream (e.g., SAM alignment file) and the final output file contains fewer records than expected based on upstream counts (e.g., salmon's NumReads total in quant.sf exceeds SAM record count), indicating buffered data loss at stream closure.

## When NOT to use

- The output file already contains the expected number of records — no bug is present.
- The program uses synchronous I/O or memory-mapped output where buffering is not a concern.
- The record count mismatch is due to filtering, error thresholds, or intentional data loss, not buffer overflow.

## Inputs

- C++ source code with ostream_sink or similar output stream initialization
- Output file written by the program (SAM, BAM, or line-delimited text format)
- Upstream quantification/mapping summary reporting expected record count (e.g., quant.sf NumReads)

## Outputs

- Corrected source code with force_flush=true or explicit ostream.flush() call
- Rebuilt binary executable
- Complete output file with record count matching expected total

## How to apply

First, compare the expected record count (from upstream quantification or mapping reports) against the actual line count in the output file using tools like `wc -l` or record-parsing code. If a discrepancy exists, locate the ostream_sink initialization in the source code (e.g., src/util/QuantOptionsUtils.cpp for salmon) and check whether force_flush is set to false. Change force_flush to true in the sink configuration to ensure the ostream buffer is explicitly flushed before the stream closes. Rebuild the program with the corrected setting, re-run on test data (a small, well-characterized dataset like ERR458493 yeast reads), and re-count the output records to verify the count now matches the expected total. This fix is crucial for streaming output modes where the program may hold buffered records in memory at program exit.

## Related tools

- **salmon** (C++ quantification tool where the writeMappings ostream sink exhibits the buffer flush bug) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (Underlying indexing and k-mer lookup library used by salmon that may depend on stream I/O) — https://github.com/COMBINE-lab/pufferfish

## Examples

```
wc -l mappings.sam && grep '^NumReads' quant.sf && salmon quant -i salmon_index -l A -1 reads.fastq.gz -z -o quant_out && wc -l quant_out/mappings.sam
```

## Evaluation signals

- Output file record count matches the NumReads total from upstream quantification (e.g., quant.sf)
- No segmentation faults or warnings about incomplete writes during program shutdown
- On re-runs with identical input, output file size and record count are reproducible and complete
- Byte-level diff shows no truncation at the end of the output file; final records are intact
- Sampling multiple test datasets (e.g., ERR458493 yeast, GEUVADIS human) produces consistent, complete output across all

## Limitations

- This skill applies specifically to C++ programs; Java, Rust, or Python stream-based programs may have different buffering semantics.
- The fix assumes the underlying filesystem and I/O subsystem do not drop writes; network filesystems or corrupted storage may still lose data despite explicit flush.
- If the record loss is due to filtering logic upstream of the output stream, rather than buffering, explicit flush will not recover those records.
- Some high-throughput applications may incur a small performance penalty from explicit flushing; batched flush strategies should be considered for extreme throughput scenarios.

## Evidence

- [other] The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost.: "The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost."
- [other] Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.: "Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by"
- [other] Locate the SAM output stream initialization in src/util/QuantOptionsUtils.cpp where the ostream_sink_mt is created with force_flush = false. Modify the sink configuration to set force_flush = true to ensure mapping records are flushed to disk before stream closure.: "Locate the SAM output stream initialization in src/util/QuantOptionsUtils.cpp where the ostream_sink_mt is created with force_flush = false. Modify the sink configuration to set force_flush = true"
- [other] Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary.: "Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index)"
- [other] Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count.: "Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count."
