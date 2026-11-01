---
name: genome-sequence-mining
description: Use when you have assembled genomic DNA sequences (contigs in FASTA format, not antiSMASH or BOA output) and corresponding LC-MS/MS data (in MGF, mzXML, mzML, or mzData format) from the same organism, and you want to identify novel RiPPs by linking gene cluster predictions to observed mass spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3460
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - NPDtools
  - joblib
  - SPAdes
  - ProteoWizard msconvert
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
- uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
---

# genome-sequence-mining

## Summary

Apply metabologenomic mining to raw nucleotide sequences (FASTA format) or genome assembly output to identify biosynthetic gene clusters (BGCs) and predict novel ribosomally synthesized and post-translationally modified peptides (RiPPs) that can be matched against tandem mass spectrometry data. This skill bridges genomic and metabolomic data to discover natural products.

## When to use

You have assembled genomic DNA sequences (contigs in FASTA format, not antiSMASH or BOA output) and corresponding LC-MS/MS data (in MGF, mzXML, mzML, or mzData format) from the same organism, and you want to identify novel RiPPs by linking gene cluster predictions to observed mass spectra. This is especially valuable when standard database search fails and you need to construct hypothetical RiPP structures from genomic evidence.

## When NOT to use

- Input sequences are from antiSMASH (.final.gbk or .gbk) or BOA (.annotated.txt) output—use raw contigs.fasta instead, as MetaMiner fails with genome mining tool output.
- Spectra are not centroided or are in proprietary binary formats without conversion to MGF or mzML.
- You are searching for non-peptidic metabolites; use Dereplicator+ with a chemical structure database instead of MetaMiner.

## Inputs

- genomic nucleotide sequences (FASTA format, raw contigs preferred)
- LC-MS/MS spectra (MGF, mzXML, mzML, or mzData format, centroided)
- RiPP class specification (e.g., 'lantibiotic', 'thiopeptide')
- optional reference sequence database (RefSeq IDs prefixed with '#RefSeq:' auto-download)

## Outputs

- significant_matches.tsv (tab-separated compound identifications with FragmentSeq, ModifiedSeq, scoring metrics)
- putative RiPP structure database (intermediate)
- spectral network visualization (if matplotlib and networkx installed; otherwise plain text)
- identified BGCs and precursor peptide predictions

## How to apply

Prepare raw nucleotide sequences as FASTA files and ensure spectra are centroided and in an open format (MGF preferred; use ProteoWizard's msconvert utility to convert other formats). Run MetaMiner with the nucleotide sequence(s) and spectra directory or files, specifying the RiPP class (e.g., '-c lantibiotic' for lantibiotics) and output directory. The pipeline identifies BGCs via genome mining, constructs post-translationally modified RiPP structure databases, and matches them against the spectra using Dereplicator scoring. Parse the tab-separated significant_matches.tsv output to extract compound identifications, verifying presence by matching FragmentSeq to the expected core peptide sequence and checking ModifiedSeq for characteristic mass shifts (e.g., dehydrobutyrine/dehydroalanine T-18 and S-18 shifts for lantibiotics). Enable parallel processing with joblib for multiple spectra or sequence files.

## Related tools

- **MetaMiner** (metabologenomic pipeline that integrates genomic data with tandem mass spectra to identify novel RiPPs) — https://github.com/ablab/npdtools
- **NPDtools 2.5.0** (toolkit containing MetaMiner executable and dependencies for RiPP discovery) — https://github.com/ablab/npdtools/releases
- **Dereplicator** (matches constructed post-translationally modified RiPP structures against tandem mass spectra) — https://github.com/ablab/npdtools
- **SPAdes** (assembles raw DNA short reads (FASTQ) into nucleotide contigs (FASTA) for input to MetaMiner)
- **ProteoWizard msconvert** (converts spectra in mzML, mzData, and other formats to MGF for MetaMiner input) — http://proteowizard.sourceforge.net/tools/msconvert.html
- **joblib** (Python library enabling parallel processing of multiple spectra or sequence files)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -c lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Output significant_matches.tsv contains identified compounds with non-null FragmentSeq and ModifiedSeq columns matching expected core peptide and modification patterns.
- For known reference peptides (e.g., AmfS with core TGSQVSLLVCEYSSLSVVLCTP), verify presence in output with correct amino acid sequence and characteristic post-translational modifications (dehydrobutyrine/dehydroalanine shifts).
- Raw FASTA input (contigs.fasta) produces successful identifications, whereas antiSMASH or BOA output does not (indicating input format dependency).
- Spectral networks show connected components for related RiPP variants, indicating spectral propagation enrichment beyond direct matches.
- Parallelization with joblib produces identical results to single-threaded execution (deterministic output regardless of thread count).

## Limitations

- MetaMiner fails when using genome mining tool output (antiSMASH .final.gbk, .gbk, or BOA .annotated.txt) as input; raw nucleotide FASTA format is required for lantibiotic and other RiPP discovery.
- Spectral networking visualization requires matplotlib and networkx Python libraries; output defaults to plain text format if these are absent.
- Performance scales with number of spectra and sequence files; joblib parallelization requires installation, otherwise all processing occurs in a single thread.
- RiPP class specification must be correct (e.g., 'lantibiotic') to construct the appropriate post-translational modification database; incorrect class selection may miss valid identifications.
- Centroided spectra are required; profile-mode data must be pre-processed or converted using external tools.

## Evidence

- [methods] Finding indicates input format dependency for lantibiotic discovery: "MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic"
- [methods] Core method: prepare FASTA and spectra files, run MetaMiner with RiPP class specification: "Run MetaMiner via 'python metaminer.py <spectra_directory_or_files> -s <path_to_S.griseus_fragment.fasta> -c lantibiotic -o <output_directory>', using default parameters (lantibiotic RiPP class,"
- [methods] Output parsing methodology for verification: "Parse the tab-separated significant_matches.tsv output file to extract compound identifications, verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq"
- [methods] MetaMiner's role in metabologenomic pipeline: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [readme] Supported input formats for metabologenomic pipelines: "The metabologenomic pipelines (currently MetaMiner only) require either raw genome nucleotide sequences or output of specific genome mining tools."
- [readme] Spectra format requirements and ProteoWizard utility: "Spectra files must be centroided and be in an open spectrum format (MGF, mzXML, mzML or mzData). NPDtools natively supports MGF and mzXML/mzData (our parser is based on RAMP). We use msconvert"
- [readme] Parallel processing requirement and dependency: "For parallel processing of multiple spectra files, NPDtools also requires joblib Python library. If not installed, everything would be processed in a single thread."
