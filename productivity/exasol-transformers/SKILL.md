---
name: exasol-transformers
description: "Deploy and use the Exasol Transformers Extension (TE) for NLP inference inside Exasol with notebook-connector. Covers `initialize_te_extension`, `deploy_scripts`, `PYTHON3_TE` language-container activation SQL, Hugging Face model-installation workflows, and the current TE SQL UDF surface."
---

# Exasol Transformers Extension Skill

Trigger when the user mentions **Transformers Extension**, **TE extension**, **initialize_te_extension**, **deploy_scripts**, **Hugging Face models in Exasol**, **TE UDF**, **PYTHON3_TE**, or NLP inference inside Exasol.

## Purpose

This skill routes notebook-connector Transformers Extension tasks to the
reference material that covers TE setup, activation, validation, and the
current TE SQL UDF surface.

Use this skill after notebook-connector configuration already exists in the
SCS (secure config store). If the required DB or BucketFS values are still missing,
activate **exasol-notebook-connector-config** first.

## Routing Algorithm

1. **Extension setup and model handling**
   - Trigger phrases: `initialize_te_extension`, `deploy_scripts`, `install_model`, `huggingface_token`
   - Load: `references/transformers-extension.md`

2. **SQL UDF usage and validation**
   - Trigger phrases: `TE_TEXT_GENERATION_UDF`, `TE_DELETE_MODEL_UDF`, `get_activation_sql`, `transformers sql udf`
   - Load: `references/transformers-extension.md`

Multiple routes can apply. Load the reference before responding.

## Prerequisites

The secure config store must already contain complete DB and BucketFS values. If
not, activate **exasol-notebook-connector-config** first.

- DB values: `db_host_name`, `db_port`, `db_user`, `db_password`, `db_schema`
- BucketFS values: `bfs_host_name`, `bfs_port`, `bfs_service`, `bfs_bucket`, `bfs_user`, `bfs_password`
- optional: `huggingface_token` for gated or private models

## Validation

Validate setup with the reference flow after loading
`references/transformers-extension.md`.

Success signals:

- the returned activation SQL is present and non-empty
- the TE setup or validation step from the reference completes without language-activation errors
- at least one TE UDF call returns rows instead of missing-language or missing-script errors

Expected failure mode:

- if DB, BucketFS, or Hugging Face settings are incomplete, initialization or UDF execution should fail until **exasol-notebook-connector-config** has been completed with real values

## Guidance

- Use **exasol-notebook-connector-config** when secure config store, DB, or BucketFS values are still missing.
- Use **exasol-bucketfs** when the user needs to inspect or manipulate the uploaded SLC or model files directly.
- Use **exasol-udfs** when the task is about language activation or custom UDF work beyond the packaged TE surface.
