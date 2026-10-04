---
name: exasol-text-ai
description: "Deploy and use the Exasol Text AI Extension (TXAIE) with notebook-connector. Covers `deploy_license`, `initialize_text_ai_extension`, the `PYTHON3_TXAIE` language container, the Extraction API classes `StandardExtractor`, `NamedEntityExtractor`, `TopicClassifierExtractor`, `PipelineExtractor`, and `BranchExtractor`, named-entity, zero-shot classification, and feature extraction runs, default-model installation, and result-table querying such as `TXAIE_AUDIT_LOG`."
---

# Exasol Text AI Extension Skill

Trigger when the user mentions **Text AI Extension**, **TXAIE**, **deploy_license**, **initialize_text_ai_extension**, **Extraction**, **named entity extraction**, **zero-shot classification**, **feature extraction**, **StandardExtractor**, **TopicClassifierExtractor**, **CO_OCCURRENCE**, **TXAIE_AUDIT_LOG**, or **PYTHON3_TXAIE**.

## Purpose

This skill routes notebook-connector Text AI Extension tasks to the reference
material that covers license deployment, TXAIE setup, extraction workflows,
and validation.

Use this skill after notebook-connector configuration already exists in the
secure config store. If the required DB or BucketFS values are still missing,
activate **exasol-notebook-connector-config** first. The schema name saved in `db_schema` must
also exist as a real schema in Exasol before the Text AI setup or extraction
flow can succeed.

## Routing Algorithm

1. **License and extension setup**
   - Trigger phrases: `deploy_license`, `initialize_text_ai_extension`, `txaie`
   - Load: `references/text-ai-extension.md`

2. **Extraction workflows and validation**
   - Trigger phrases: `Extraction`, `NamedEntityExtractor`, `PipelineExtractor`, `BranchExtractor`, `StandardExtractor`, `TopicClassifierExtractor`, `feature extraction`, `zero-shot classification`, `TOPIC_CLASSIFIER_VIEW`, `TOPICS_VIEW`, `NAMED_ENTITY_VIEW`, `KEYWORD_SEARCH_VIEW`, `CO_OCCURRENCE`, `TXAIE_AUDIT_LOG`
   - Load: `references/text-ai-extension.md`

Multiple routes can apply. Load the reference before responding.

## Prerequisites

The secure config store must already contain complete DB and BucketFS values. If
not, activate **exasol-notebook-connector-config** first.

`db_schema` is only a stored configuration value. Create that schema in Exasol
before running the Text AI flow if it does not already exist.

## Validation

Validate setup with the reference flow after loading
`references/text-ai-extension.md`.

Success signals:

- license deployment completes
- initialization completes and the language/container setup is persisted
- a small extraction run writes output rows without missing-license or missing-language errors

Expected failure mode:

- if the configured schema does not exist yet, setup or extraction should fail until the schema is created in Exasol
- if the source tables, DB config, BucketFS config, or extension assets are missing, extraction should fail until **exasol-notebook-connector-config** and the required DB objects are in place
- on the first run, initialization can take time because notebook-connector downloads the TXAIE language container and default models

## Guidance

- Use **exasol-notebook-connector-config** when secure config store, DB, or BucketFS values are still missing.
- For local ITDE-style runs, make sure the stored DB and BucketFS host values are reachable from the notebook process.
- Keep simple TXAIE-specific inspection here, including the SQL examples in this skill's reference and small Python snippets tied directly to TXAIE result objects such as `TXAIE_AUDIT_LOG`.
- Use **exasol-notebook-connections** when the user wants broader notebook-connector connection-helper work beyond these TXAIE-specific inspection patterns.
- Use **exasol-bucketfs** when the user needs to inspect the uploaded SLC or model assets.
- Use **exasol-udfs** when the task moves beyond the packaged Text AI extraction API into lower-level UDF or SLC work.

## Safety Rules

- Prefer the built-in community license or a local license file over embedding real license content inline.
- Do not share real license content.
- Do not guess DB, BucketFS, or model-related configuration values.
