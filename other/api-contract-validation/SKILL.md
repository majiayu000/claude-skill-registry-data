---
name: api-contract-validation
description: Use when integrating with an external API (such as TensorFlow Serving) where changes to the response schema could break dependent code, or when model metadata must be extracted and verified before being used in downstream analysis steps.
license: CC-BY-4.0
metadata:
  edam_topics: []
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

# api-contract-validation

## Summary

Validate that an API endpoint's response conforms to an expected schema contract by verifying the presence and structure of required fields. This skill ensures downstream code can safely parse API responses without encountering missing or malformed data.

## When to use

Apply this skill when integrating with an external API (such as TensorFlow Serving) where changes to the response schema could break dependent code, or when model metadata must be extracted and verified before being used in downstream analysis steps.

## When NOT to use

- The API endpoint is known to be stable and has never changed its response schema (validation becomes redundant overhead).
- Input names and their structure are already hardcoded or cached elsewhere and do not require runtime verification.

## Inputs

- TensorFlow Serving instance URL
- Model name and version identifier
- Expected API contract schema (list of required fields and their types)

## Outputs

- JSON document containing extracted model input names
- Validation status (pass/fail)
- Error details if validation failed

## How to apply

Construct an HTTP GET request to the target API endpoint (e.g., /model/metadata on a TensorFlow Serving instance), execute the request and retrieve the JSON response, then parse the JSON and validate that all required fields (signature, inputs, outputs) are present and match the expected API contract. Extract the needed values (e.g., model input names such as '1H' and '13C' headers) and write both the extracted data and validation status to an output JSON file. If validation fails, document which fields were missing or malformed so that code changes can be made to handle the new schema.

## Related tools

- **TensorFlow Serving** (Hosts the model and exposes the /model/metadata endpoint that returns JSON containing model signature, input names, and output names)

## Examples

```
curl -X GET http://tensorflow-serving-host:8501/v1/models/smart3/metadata | jq '.model_spec, .metadata.signature_def' && python -c "import json; resp = json.load(open('metadata.json')); assert 'inputs' in resp and '1H' in resp['inputs'] and '13C' in resp['inputs']"
```

## Evaluation signals

- HTTP request to /model/metadata endpoint succeeds and returns status 200.
- Returned JSON is valid and parseable without errors.
- All required fields (signature, inputs, outputs) are present in the response.
- Extracted input names match the expected set (e.g., '1H' and '13C' are both present).
- Output JSON is written with validation status set to 'pass' when all checks succeed.

## Limitations

- The skill assumes the TensorFlow Serving instance is reachable and responding; network failures or service downtime will cause validation to fail.
- Changes to the API response schema (e.g., renaming or removing fields) will cause validation to fail, requiring manual code updates to reflect the new contract.
- No changelog tracking is available to warn users of schema changes in advance, so validation failures may occur without prior notice.

## Evidence

- [intro] Check model metadata via /model/metadata endpoint: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] Extract and validate input names from metadata response: "Classify programmatically. You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] Model input names require code updates when they change: "If the model input names change, then we need to change it in the code"
- [other] Validate response contains required API contract fields: "Validate that the response contains required fields (signature, inputs, outputs) matching the expected API contract."
