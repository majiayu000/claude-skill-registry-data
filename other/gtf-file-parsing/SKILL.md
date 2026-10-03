---
name: gtf-file-parsing
description: Use when you have a GTF-formatted genome annotation file and need to generate alternative splicing events (exon skipping, intron retention, alternative splice sites, mutually exclusive exons) or transcript-isoform inclusion levels (PSIs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3097
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0199
  tools:
  - SUPPA2
derived_from:
- doi: 10.1186/s13059-018-1417-1
  title: suppa2
evidence_spans:
- 'SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_suppa2
    doi: 10.1186/s13059-018-1417-1
    title: suppa2
  dedup_kept_from: coll_suppa2
schema_version: 0.2.0
---

# gtf-file-parsing

## Summary

Parse a genome annotation GTF file to extract transcript structures, exon coordinates, and gene–transcript relationships for downstream alternative splicing event generation. This skill is essential for initializing splicing analysis workflows that require systematic decomposition of transcript isoforms into discrete AS events.

## When to use

You have a GTF-formatted genome annotation file and need to generate alternative splicing events (exon skipping, intron retention, alternative splice sites, mutually exclusive exons) or transcript-isoform inclusion levels (PSIs). Use this skill when your input is raw GTF and your goal is to create indexed event or isoform catalogs before quantification or differential analysis.

## When NOT to use

- Input annotation is already an indexed event catalog (ioe/ioi files); re-parsing would be redundant.
- Your splicing analysis operates at the junction level or read-alignment level rather than transcript-annotation level.
- GTF file lacks gene_id or transcript_id attributes in the ninth column; preprocessing is required before parsing.

## Inputs

- GTF annotation file (genome annotation in GTF format with exon features and gene_id, transcript_id attributes)

## Outputs

- ioe file (input-output events: event identifier, event coordinates, transcripts in numerator, transcripts in denominator)
- ioi file (input-output isoforms: transcript identifier, all transcripts in gene for PSI calculation)
- gtf file (local alternative splicing event coordinates, UCSC browser-compatible with track header)

## How to apply

Load the GTF file into SUPPA2's generateEvents subcommand, which parses only the 'exon' feature lines and extracts gene_id and transcript_id attributes from the ninth column to reconstruct transcript structures. The parser identifies all exonic boundaries and their coordinates for each transcript within a gene. It then systematically identifies local alternative splicing event boundaries (exon skip regions, intron retention zones, alternative 5'/3' splice site pairs, mutually exclusive exon groups, and alternative first/last exon boundaries). The output is written to three indexed files: ioe (input-output events, mapping events to transcripts contributing to inclusion and exclusion forms), ioi (input-output isoforms, mapping transcripts to gene-level isoform sets for PSI denominator calculation), and gtf (coordinates of local events only, ready for UCSC browser visualization). Validate that all exon lines contain both gene_id and transcript_id tags and that transcripts within each gene share consistent strand and chromosome information.

## Related tools

- **SUPPA2** (Parses GTF exon features and generates indexed ioe, ioi, and local-event GTF files via the generateEvents subcommand) — https://github.com/comprna/SUPPA

## Examples

```
python3 suppa.py generateEvents -i genome_annotation.gtf -o splicing_events
```

## Evaluation signals

- All exon lines in the input GTF were successfully parsed and assigned to their corresponding gene and transcript identifiers.
- ioe file contains no duplicate event identifiers and all transcript accessions in numerator/denominator subsets exist in the annotation.
- ioi file maps each transcript to a non-empty set of isoforms from its parent gene; no orphaned transcripts.
- gtf output file contains only coordinates of identified local AS events (SE, RI, A5/A3, MX, AF, AL types) with valid strand and chromosome fields.
- Number of ioe events and event types (SE, RI, A5/A3, etc.) match expected counts for the input organism/annotation version.

## Limitations

- Only exon feature lines are parsed; other GTF features (CDS, start_codon, stop_codon, UTR) are ignored, so UTR-only isoforms may be incorrectly merged.
- Transcripts without explicitly matched gene_id or transcript_id attributes in column 9 will be skipped silently.
- Variable boundary mode (-b V) allows ±10 nt flexibility in some event coordinates to incorporate near-boundary exons, potentially inflating event redundancy; careful downstream filtering may be needed.
- Complex splicing patterns that cannot be encapsulated in simple local event types (e.g., coordinated exon skipping across distant regions) are not captured; transcript-level isoform events (ioi) should be used as a complementary approach.

## Evidence

- [readme] The method reads transcript and gene information solely from the 'exon' lines in the GTF: "The method reads transcript and gene information solely from the "exon" lines in the GTF. It then generates the events and outputs an ioe file"
- [readme] ioe file provides for each AS event the transcripts that describe either form of the event, contributing to numerator and denominator of PSI: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [readme] ioi file provides for each transcript the set of all transcripts from that gene for relative abundance calculation: "The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated."
- [readme] For local AS events, generateEvents produces a GTF file with calculated events and track header ready for UCSC browser visualization: "For local AS events, this command also generates a GTF file with the calculated events and with a track header ready to be uploaded into the UCSC browser for visualization"
- [readme] gene_id and transcript_id tags are required in the attributes field for proper parsing: "For that purpose "gene_id" and "transcript_id" tags are required in the attributes field (column 9)."
