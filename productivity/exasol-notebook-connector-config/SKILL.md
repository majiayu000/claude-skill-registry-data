---
name: exasol-notebook-connector-config
description: "Set up notebook-connector configuration for Exasol AI workflows through the Secrets Python API. Covers secure config store (`scs`) creation, the `AILabConfig` and `StorageBackend` key sources, backend-specific config values such as `db_host_name`, `db_schema`, `storage_backend`, and `huggingface_token`, Python validation, and handoff to downstream notebook-connector skills."
---

# Exasol Notebook-Connector Config Skill

Trigger when the user mentions **notebook-connector**, **secure config store**, **Secrets**, **configure notebook-connector**, **set up credentials for TE**, **set up credentials for TXAIE**, **first-time notebook-connector setup**, or similar setup tasks.

## Purpose

This skill establishes the Python-managed secure configuration that later
notebook-connector skills depend on.

After configuration is complete:

- activate **exasol-itde** for local Docker DB lifecycle
- activate **exasol-notebook-connections** for Python DB and BucketFS helper APIs
- activate **exasol-transformers** for Transformers Extension setup and usage
- activate **exasol-text-ai** for Text AI Extension setup and usage
- activate **exasol-bucketfs** or **exasol-udfs** only for deeper BucketFS or SLC work beyond notebook-connector setup

## Routing Algorithm

Choose the narrowest path that matches the user request:

1. **Python-based configuration**
   - Trigger phrases: `Secrets`, `AILabConfig`, `StorageBackend`, `save config in python`, `notebook cell`, `script`
   - Load: `references/secrets-python.md`
   - Use scripts from: `scripts/`

2. **Validation / smoke tests**
   - Trigger phrases: `check config`, `verify connection`, `validate notebook-connector`, `smoke test`
   - Load: `references/validation.md`
   - Use scripts from: `scripts/`

3. **Downstream notebook-connector work**
   - Trigger phrases: `bring_itde_up`, `open_pyexasol_connection`, `open_sqlalchemy_connection`, `open_ibis_connection`, `open_bucketfs_bucket`, `initialize_te_extension`, `initialize_text_ai_extension`, `deploy_license`
   - Hand off to **exasol-itde**, **exasol-notebook-connections**, **exasol-transformers**, or **exasol-text-ai** after setup validation succeeds

Multiple routes can apply. Load all matching references before responding.

## Default Guidance

- Prefer the Python path when the user wants notebook cells, automation, or agent-generated code.
- Before handing off to DB helpers, BucketFS helpers, TE, or TXAIE work, run `scripts/validate_config.py` to confirm the `Secrets` store is populated for the expected backend.
- Use `AILabConfig` as the source of the common key names stored in `Secrets`.

## Validation

After writing or updating config, verify it before handing off to downstream skills:

- run `scripts/validate_config.py`

Success signals:

- the backend resolves to the expected value (`onprem` or `saas`)
- the required setup values for this skill are present in the store so downstream notebook-connector workflows can proceed

Expected failure mode:

- if required setup values for this skill such as `storage_backend`, `db_schema`, backend-specific connection values, or real credentials are missing, or the store still contains template values such as `my-db-host` or placeholder SaaS IDs/PATs, setup validation should fail until the user replaces them with real values

## Safety Rules

- Do not guess SaaS account IDs, PATs, passwords, or BucketFS credentials.
- Do not read secrets from config files unless the user explicitly provides them.
