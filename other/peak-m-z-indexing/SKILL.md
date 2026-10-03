---
name: peak-m-z-indexing
description: Use when when you have LC-MS-MS metabolomics data in MGF format and need
  to prepare it for unsupervised analysis (e.g., topic modeling with LDA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - gensim
  - run_gensim.py
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- pipenv --python 2.7
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_substructure_discovery_mass2motif_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_substructure_discovery_mass2motif_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-m-z-indexing

## Summary

Convert MS2 fragmentation spectra from MGF format into indexed peak features (m/z values) and build a dictionary mapping peaks to feature indices for corpus representation. This is the feature extraction foundation for topic modeling of metabolomics data.

## When to use

When you have LC-MS-MS metabolomics data in MGF format and need to prepare it for unsupervised analysis (e.g., topic modeling with LDA). Apply this skill as the first step before any statistical modeling of MS2 spectra, to convert raw mass-to-charge ratios into a structured bag-of-words feature space.

## When NOT to use

- Input is already a pre-computed feature matrix or corpus (e.g., already in gensim or Bag-of-Words format); skip directly to modeling
- Data is in non-MGF formats (e.g., mzML, mzXML) without prior conversion to MGF
- Spectra have already been processed and normalized by another tool; verify format compatibility before re-indexing

## Inputs

- MGF-format MS2 file (mass spectrometry data with fragmentation spectra)

## Outputs

- JSON corpus file in gensim format (bag-of-words representation of spectra)
- Feature index dictionary (m/z peak to integer index mapping)

## How to apply

Load the MGF file using gensim's corpus generation module and parse MS2 fragmentation spectra to extract mass-to-charge ratio (m/z) peaks as discrete features. Build a dictionary that maps each unique peak (m/z value) to a unique feature index. Serialize this indexed representation as a JSON corpus file in gensim's bag-of-words format, where each spectrum is represented as a list of (feature_index, count) tuples. The resulting corpus becomes the direct input to gensim's LDA modeling step. Verify correctness by confirming that the JSON corpus contains valid gensim corpus format and that feature indices are consecutive integers starting from 0.

## Related tools

- **gensim** (Corpus generation module for parsing MGF and building dictionary; serializes indexed peaks into JSON corpus format) — https://github.com/RaRe-Technologies/gensim
- **run_gensim.py** (Command-line wrapper that orchestrates corpus generation from MGF files using gensim backend) — https://github.com/glasgowcompbio/ms2ldaviz
- **Python** (Language for implementing corpus generation logic and gensim API calls)

## Examples

```
./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json
```

## Evaluation signals

- Output JSON file is valid gensim corpus format (list of documents, each a list of [feature_index, count] tuples)
- All feature indices in the corpus are non-negative integers and correspond to entries in the peak dictionary
- Dictionary size equals the number of unique m/z peaks extracted from all input spectra
- Each spectrum in the corpus preserves the original MS2 fragmentation data without loss of intensity/count information
- Corpus and dictionary are co-indexed: no gaps in feature indices and all indices in corpus reference valid dictionary entries

## Limitations

- MGF parser may not handle non-standard or corrupted MGF headers; validation of input file format is required
- Peak indexing strategy (binning, exact mass matching, or tolerance windows) is not explicitly documented; users should verify whether m/z values are matched exactly or within a mass tolerance
- No built-in normalization or intensity filtering of peaks; weak or noise peaks are preserved and may degrade downstream topic inference
- Memory consumption scales with the number of unique m/z values; very large metabolomics datasets may require peak filtering or binning before indexing

## Evidence

- [other] Load the MGF file using gensim's corpus generation module. Parse MS2 fragmentation spectra and extract mass-to-charge ratio (m/z) peaks as features. Build a dictionary mapping peaks to feature indices. Serialize the corpus as a JSON file containing the bag-of-words representation of each spectrum using the gensim corpus format.: "Parse MS2 fragmentation spectra and extract mass-to-charge ratio (m/z) peaks as features. Build a dictionary mapping peaks to feature indices. Serialize the corpus as a JSON file containing the"
- [other] The corpus generation step accepts an MGF-format MS2 file and outputs a JSON corpus representation via the command: `./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json`, which serves as input to the subsequent gensim LDA modeling step.: "The corpus generation step accepts an MGF-format MS2 file and outputs a JSON corpus representation via the command: `./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json`"
- [readme] Performs 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db: "Generate corpus/features from MS2 file"
- [readme] visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data: "unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
