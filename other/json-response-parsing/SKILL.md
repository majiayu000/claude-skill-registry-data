---
name: json-response-parsing
description: Use when you receive a JSON response from a REST API endpoint (e.g., TensorFlow Serving /model/metadata) and need to extract and validate specific fields such as model input names, signatures, or outputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3473
  tools:
  - tensorflow serving
  - TensorFlow Serving
derived_from:
- doi: 10.1186/s13321-023-00738-4
  title: DeepSAT
evidence_spans:
- We pass through tensorflow serving at this url
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_deepsat
schema_version: 0.2.0
---

# json-response-parsing

## Summary

Parse JSON responses from REST API endpoints to extract structured data such as model metadata, input field names, and validation signatures. This skill is essential when integrating with machine learning serving infrastructure that exposes metadata via HTTP endpoints.

## When to use

Apply this skill when you receive a JSON response from a REST API endpoint (e.g., TensorFlow Serving /model/metadata) and need to extract and validate specific fields such as model input names, signatures, or outputs. Trigger on receiving HTTP responses that contain nested JSON structures with expected API contract fields.

## When NOT to use

- Input is a non-JSON response (e.g., XML, plain text, binary) from the endpoint
- Model metadata is already cached locally and validation is not required
- The API endpoint is unavailable or the HTTP request fails before receiving a response

## Inputs

- HTTP endpoint URL (TensorFlow Serving instance with /model/metadata path)
- Expected API contract specification (required fields: signature, inputs, outputs)
- Expected input field names (e.g., '1H', '13C' for spectroscopy data)

## Outputs

- Extracted model input names (JSON array or object)
- Validation status report (JSON object with fields present/absent)
- Output JSON file documenting parsed metadata and validation results

## How to apply

Execute an HTTP GET request to the target endpoint (e.g., /model/metadata on a TensorFlow Serving instance), receive the JSON response, and parse it to extract required fields. Identify the structure containing model input names (e.g., '1H', '13C' headers expected in SMART 3), and validate that the response contains the expected fields (signature, inputs, outputs) matching the documented API contract. Write the extracted input names and validation status to an output JSON file. Document any discrepancies between expected input names and observed names, as changes require corresponding code updates.

## Related tools

- **TensorFlow Serving** (REST API server providing /model/metadata endpoint for querying model input names and signatures)

## Examples

```
import json; import requests; response = requests.get('http://tensorflow-serving-instance:8501/v1/models/smart3:metadata'); metadata = response.json(); input_names = list(metadata.get('metadata', {}).get('signature_def', {}).get('serving_default', {}).get('inputs', {}).keys()); print(json.dumps({'inputs': input_names, 'validation': 'ok' if '1H' in input_names and '13C' in input_names else 'mismatch'}))
```

## Evaluation signals

- JSON response is successfully parsed without syntax errors and contains the expected top-level fields (signature, inputs, outputs)
- Extracted input names match the documented expected field names ('1H', '13C' for SMART 3) or any deviations are explicitly flagged in the validation status
- Output JSON file is well-formed and contains both the extracted input names and a boolean or status field indicating validation success/failure
- If input names differ from expected names, the validation status clearly indicates this mismatch and prompts code review
- The HTTP GET request completes successfully (HTTP 200 or expected status code) and response time is within acceptable latency bounds

## Limitations

- If model input names change upstream in the TensorFlow Serving instance, the code that uses these names must be manually updated to reflect the new field names
- No changelog or version history is typically available to track when and why input names were modified
- The skill assumes the API contract is stable; breaking changes to the response schema structure may cause parsing to fail
- Network failures or TensorFlow Serving instance downtime will prevent metadata retrieval entirely

## Evidence

- [intro] HTTP endpoint query mechanism: "We pass through tensorflow serving at this url: /model/metadata"
- [other] Required fields in response schema: "Parse the JSON response to extract model input names (e.g., '1H', '13C' headers expected). 4. Validate that the response contains required fields (signature, inputs, outputs) matching the expected"
- [intro] Input field names and expected values: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] Maintenance burden from field changes: "If the model input names change, then we need to change it in the code"
