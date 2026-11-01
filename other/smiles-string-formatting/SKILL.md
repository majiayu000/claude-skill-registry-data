---
name: smiles-string-formatting
description: Use when you have a set of chemical structures (as SMILES strings or convertible to SMILES) and need to submit them programmatically to the NP Classifier /classify endpoint for batch or automated classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3174
  tools:
  - Python
  - Docker
  - Docker Compose
  - TensorFlow Serving
  - NP-Classifier
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassifier
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier
schema_version: 0.2.0
---

# SMILES String Formatting for Chemical Classification API Queries

## Summary

Format organic molecule structures as SMILES (Simplified Molecular Input Line Entry System) strings to enable programmatic queries against the NP Classifier REST API endpoint. This skill is essential when you need to submit chemical structures for automated natural product classification without manual web interface interaction.

## When to use

Use this skill when you have a set of chemical structures (as SMILES strings or convertible to SMILES) and need to submit them programmatically to the NP Classifier /classify endpoint for batch or automated classification. Specifically, when you require structured JSON responses containing classification output rather than interactive web browsing, or when integrating chemical classification into a computational workflow.

## When NOT to use

- When your chemical structures are not available in or easily convertible to SMILES format; use alternative input formats if the API supports them or convert offline first.
- When you require real-time, low-latency responses and the Docker-based local deployment introduces unacceptable overhead; consider pre-computed or cached classifications instead.
- When analyzing structures where the input layer specifications (input_2048, input_4096) are not compatible with your feature representation; verify model architecture alignment before submission.

## Inputs

- SMILES string (chemical structure notation as a URL query parameter)
- NP Classifier server endpoint URL (http://localhost or equivalent)

## Outputs

- JSON response object with 'output' field containing classification results
- HTTP status code 200 indicating successful classification

## How to apply

Obtain or generate SMILES string representations of your target chemical structures. Construct an HTTP GET request targeting the NP Classifier /classify endpoint with the SMILES string as a query parameter (format: /classify?smiles=<SMILES_string>). Optionally append a cached flag parameter to retrieve pre-computed results and improve query speed. Send the request to a running NP Classifier server instance (deployed via Docker Compose). Capture and parse the returned JSON response, which will contain an 'output' field with the classification result. Validate that the HTTP response status is 200 and that the JSON structure is well-formed before downstream processing.

## Related tools

- **Docker** (Container orchestration for running NP Classifier server and TensorFlow Serving inference backend)
- **Docker Compose** (Multi-container orchestration to bring up both NP Classifier web server and TensorFlow Serving in coordinated deployment)
- **TensorFlow Serving** (Backend inference service that processes SMILES inputs through trained neural network models with input layers 'input_2048' and 'input_4096')
- **NP-Classifier** (Web server providing the /classify REST API endpoint that accepts SMILES strings and returns classification responses) — https://github.com/mwang87/NP-Classifier

## Examples

```
curl -X GET 'http://localhost:5000/classify?smiles=CC(=O)Oc1ccccc1C(=O)O&cached=true'
```

## Evaluation signals

- HTTP response status code is exactly 200 with no error or redirect codes
- Returned JSON is well-formed and contains the 'output' field with non-null classification result
- Response metadata or schema references expected input layer names 'input_2048' and 'input_4096'
- Identical SMILES inputs produce identical output when cached flag is used, confirming result reproducibility
- Response latency is reduced when the cached flag parameter is appended to repeated queries

## Limitations

- SMILES string format must be syntactically valid; malformed SMILES will result in classification errors or null responses.
- The NP Classifier models are optimized for natural product and drug-like molecules; performance on highly non-standard or synthetic chemical scaffolds is not characterized.
- Local Docker deployment requires sufficient compute resources (CPU/GPU, memory) to run both server and TensorFlow Serving; remote deployments may have network latency.
- Model input layer names ('input_2048', 'input_4096') are fixed; any change to the underlying model architecture requires code modifications in the classifier.

## Evidence

- [readme] Input layer names specification: "Input layers' names should be "input_2048" and "input_4096""
- [readme] Output field specification: "Output layer's name should be "output""
- [readme] Cached parameter optimization: "You can also provide cached flag to the params to get the cached version so make it faster"
- [readme] API endpoint description: "Classify programmatically"
- [readme] Docker deployment requirement: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose."
