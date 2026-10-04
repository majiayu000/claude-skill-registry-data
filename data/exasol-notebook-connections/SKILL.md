---
name: exasol-notebook-connections
description: "Use notebook-connector's Python connection helpers for Exasol, BucketFS, SQLAlchemy, and Ibis. Covers open_pyexasol_connection, open_sqlalchemy_connection, open_ibis_connection, open_bucketfs_bucket, open_bucketfs_location, get_backend, and related helper functions."
---

# Exasol Notebook Connector Connections Skill

Trigger when the user mentions **open_pyexasol_connection**, **open_sqlalchemy_connection**, **open_ibis_connection**, **open_bucketfs_bucket**, **BucketFS location**, **get_backend**, **connection helper**, or **use notebook-connector from Python**.

## Routing Algorithm

1. **Database Connection Helpers**
   - Trigger phrases: `pyexasol`, `sqlalchemy`, `ibis`, `open connection`
   - Load: `references/connections-api.md`
   - Use scripts from: `scripts/`

2. **BucketFS Object Helpers**
   - Trigger phrases: `open_bucketfs_bucket`, `open_bucketfs_location`, `bucket path`
   - Load: `references/connections-api.md`
   - Use scripts from: `scripts/`

3. **Config Not Set Up Yet**
   - Activate **exasol-notebook-connector-config**

## Validation

Validate the configured connection helpers in this order:

- run `scripts/check_backend.py` first to confirm the store resolves the expected backend
- if helpers fail due to missing keys or placeholder values, activate **exasol-notebook-connector-config** and run its `scripts/validate_config.py`
- then run `scripts/open_pyexasol.py`, `scripts/open_sqlalchemy.py`, `scripts/open_ibis.py`, or `scripts/open_bucketfs.py` for the helper family the user needs

Success signals:

- `open_pyexasol.py` can run `SELECT 1`
- `open_sqlalchemy.py` can open an engine and execute a minimal statement
- `open_ibis.py` can list tables
- `open_bucketfs.py` can resolve the bucket object and UDF-visible path

Expected failure mode:

- if the config still contains placeholder hostnames, PATs, or database IDs, these checks should fail until the real values are present

## Notes

- This skill assumes the secure config store is already populated.
- Prefer these helpers over ad hoc connection construction when the user is already using notebook-connector.
