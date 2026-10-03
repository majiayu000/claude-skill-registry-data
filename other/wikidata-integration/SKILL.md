---
name: wikidata-integration
description: Use when when building or maintaining a local natural-product reference
  database that requires current Wikidata entries, or when preparing metadata for
  mass-spectrometry queries that need enriched compound annotations (e.g., alternative
  names, chemical classifications, source organisms).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3407
  tools:
  - prepare_wikidata_lotus_prefect.py
  - jobs.py
  - metadata_cleanup_prefect.py
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-025-02813-0
  title: MSnLib
evidence_spans:
- run `prepare_wikidata_lotus_prefect.py` for updating the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msnlib_cq
    doi: 10.1038/s41592-025-02813-0
    title: MSnLib
  dedup_kept_from: coll_msnlib_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02813-0
  all_source_dois:
  - 10.1038/s41592-025-02813-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# wikidata-integration

## Summary

Integration of Wikidata natural-product records into a local LOTUS database file for metadata-enriched compound queries. This skill enables dynamic updates of curated natural-product annotations by fetching and processing Wikidata entries, ensuring downstream metadata queries have current, validated compound information.

## When to use

When building or maintaining a local natural-product reference database that requires current Wikidata entries, or when preparing metadata for mass-spectrometry queries that need enriched compound annotations (e.g., alternative names, chemical classifications, source organisms). Use this skill if the LOTUS database file is stale or does not exist, and you need to regenerate it from Wikidata sources.

## When NOT to use

- Input metadata already contains complete, validated natural-product annotations from a curated source (e.g., manually reviewed compounds); Wikidata integration may introduce redundant or conflicting data.
- Network connectivity to Wikidata is unavailable and no pre-existing LOTUS file is available; the skill will fail and block downstream workflows.
- Downstream analysis requires real-time or streaming natural-product updates; this skill produces a static file snapshot and is not designed for live synchronization.

## Inputs

- Wikidata API endpoint (live)
- Optional: pre-existing LOTUS database file (fallback)
- jobs.py configuration (to enable/disable Wikidata fetching)

## Outputs

- Updated LOTUS natural-product database file (CSV or structured format with columns: compound ID, structure, metadata fields)
- Validation report (record count, schema compliance)

## How to apply

Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products into a structured LOTUS database file. The script integrates with Prefect 2 for orchestration and requires internet access to Wikidata. After execution, validate that the regenerated file contains expected columns (minimum: compound identifiers, structure information, metadata fields) and record counts match or exceed the previous version. If the script fails or network access is unavailable, fall back to a pre-existing LOTUS file provided with the repository. Save the validated output file to a location accessible to downstream query operations (e.g., metadata-matching workflows).

## Related tools

- **prepare_wikidata_lotus_prefect.py** (Fetches and processes Wikidata entries for natural products; regenerates the LOTUS database file for downstream queries.) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file to enable/disable Wikidata fetching and set it to False if local LOTUS file is preferred.) — https://github.com/corinnabrungs/msn_tree_library
- **metadata_cleanup_prefect.py** (Prefect 2 orchestration flow that manages the deployment and execution of prepare_wikidata_lotus_prefect.py.) — https://github.com/corinnabrungs/msn_tree_library

## Examples

```
python prepare_wikidata_lotus_prefect.py
```

## Evaluation signals

- Regenerated LOTUS file exists at the expected output path and file size is ≥ pre-existing version or matches expected baseline.
- Output file schema validation: all required columns (compound ID, structure information, metadata fields) are present with no NULL values in critical fields.
- Record count in regenerated file is consistent with or exceeds previous version; spot-check 5–10 random entries against Wikidata source to verify data integrity.
- Prefect flow execution log shows zero errors or retries; if retries occur, confirm fallback to pre-existing file was triggered.
- Downstream metadata queries (e.g., PubChem name search, DrugBank matching) successfully match compounds using the regenerated LOTUS file without schema errors.

## Limitations

- Requires internet connectivity to Wikidata API; no offline mode is mentioned. Network failures will trigger fallback to pre-existing file, potentially leaving data stale.
- No changelog is provided, making it unclear which Wikidata fields or records have changed between updates; traceability of data lineage is limited.
- Relies on Wikidata data quality and curation; erroneous or incomplete entries in Wikidata will propagate into the LOTUS file without validation.
- The script is tailored for natural products; integration with other compound databases (DrugBank, PubChem, DrugCentral) is handled by separate extraction scripts and may require manual schema alignment.

## Evidence

- [other] The prepare_wikidata_lotus_prefect.py script is executed to update the LOTUS natural-product database file; if this update is not performed, a pre-existing provided file can be used as an alternative.: "The prepare_wikidata_lotus_prefect.py script is executed to update the LOTUS natural-product database file; if this update is not performed, a pre-existing provided file can be used as an alternative."
- [other] Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products. Validate that the regenerated LOTUS database file contains the expected columns and records. Save the updated LOTUS data file for downstream query operations.: "Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products. Validate that the regenerated LOTUS database file contains the expected columns and records. Save"
- [readme] LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file): "LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file)"
- [readme] For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py: "For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py"
- [readme] Please use the [template] for your metadata for having same column names and minimum needed information for the query.: "Please use the [template] for your metadata for having same column names and minimum needed information for the query."
