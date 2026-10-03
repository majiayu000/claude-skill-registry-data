---
name: topic-modeling-lda
description: Use when after generating a corpus/features JSON file from raw MS2 fragmentation
  spectra or similar document-term data, when the goal is unsupervised discovery of
  latent topics (e.g., metabolite families or spectral motifs) without ground-truth
  labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2995
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# topic-modeling-lda

## Summary

Infer latent topics from a preprocessed document-term corpus using gensim's Latent Dirichlet Allocation (LDA) model, producing topic distributions and term weights suitable for unsupervised characterization of high-dimensional spectroscopy data. This skill transforms a corpus JSON file into an LDA result JSON containing topic-document and topic-term associations.

## When to use

Apply this skill after generating a corpus/features JSON file from raw MS2 fragmentation spectra or similar document-term data, when the goal is unsupervised discovery of latent topics (e.g., metabolite families or spectral motifs) without ground-truth labels. Use it as the second step in the ms2lda workflow, after corpus generation and before database insertion.

## When NOT to use

- Input corpus is already a fitted LDA model or serialized gensim model object — use model loading instead of re-inference.
- Document-term matrix contains raw (non-normalized) counts without preprocessing; corpus generation must precede LDA inference.
- Supervised classification or strongly-labeled data is available and preferred — LDA is unsupervised and may not align with external labels.

## Inputs

- corpus JSON file (preprocessed document-term representations from MS2 spectra or similar high-dimensional data)

## Outputs

- LDA result JSON file (containing topic-document distributions, topic-term weights, and model metadata)

## How to apply

Load the preprocessed corpus JSON file (containing document-term representations) into gensim's LDA inference engine via the run_gensim.py script with the 'gensim' mode. The script accepts the input corpus path and a target output path for the LDA result JSON. gensim infers topic distributions (topic-document and topic-term associations) using variational inference on the corpus. The resulting JSON file contains topic metadata, term weights per topic, and document-topic distributions. Success is verified by checking that the output JSON is well-formed, contains non-zero topic probabilities for sampled documents, and that the number of inferred topics and vocabulary size match the model hyperparameters.

## Related tools

- **gensim** (LDA model training and topic inference engine; reads corpus JSON and outputs topic distributions and term weights) — https://github.com/RaRe-Technologies/gensim
- **Python** (Scripting language in which run_gensim.py is implemented)
- **run_gensim.py** (Command-line wrapper script that orchestrates corpus loading, LDA inference, and JSON serialization) — https://github.com/glasgowcompbio/ms2ldaviz

## Examples

```
./run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json
```

## Evaluation signals

- Output JSON file is valid JSON and parses without error.
- Output JSON contains 'topics', 'term_weights', and 'doc_topic_dist' (or equivalent) keys with non-empty arrays.
- All topic probabilities (doc_topic_dist entries) sum to ~1.0 per document (within floating-point precision).
- Number of inferred topics matches model hyperparameter (e.g., 50 topics yields 50 entries in topics array).
- Term weights are normalized per topic and identify high-frequency terms associated with each topic (interpretable spectral motifs or compound families).

## Limitations

- LDA is unsupervised; inferred topics may not align with external chemical or biological labels; post-hoc manual curation or validation against reference standards is often needed.
- Model hyperparameters (number of topics, alpha, beta) must be chosen in advance; the script does not perform automatic hyperparameter tuning or model selection.
- Convergence and quality depend on corpus size and preprocessing; small or poorly preprocessed corpora may yield uninformative or unstable topics.
- No built-in cross-validation or held-out test set evaluation; perplexity or coherence metrics are not automatically computed by the script.

## Evidence

- [other] The gensim LDA step accepts a corpus JSON file as input and produces an LDA result JSON file as output via the command './run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json'.: "Execute the gensim LDA model using ./run_gensim.py with arguments 'gensim', input corpus path, and output result path to infer topics from the corpus"
- [intro] Topics inferred from Latent Dirichlet Allocation can be used to assist in unsupervised characterisation of fragmented LC-MS-MS metabolomics data.: "topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
- [readme] The ms2lda workflow performs 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db.: "Performs 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db"
- [other] Save the LDA result as a JSON file (myexp.ldaresult.json) containing topic distributions, term weights, and model metadata.: "Save the LDA result as a JSON file (myexp.ldaresult.json) containing topic distributions, term weights, and model metadata"
- [readme] A web application developed in Django+D3 to visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data.: "visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
