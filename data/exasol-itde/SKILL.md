---
name: exasol-itde
description: "Use notebook-connector's itde_manager to run a local Docker-based Exasol database. Covers bring_itde_up, get_itde_status, restart_itde, take_itde_down, and how ITDE populates notebook-connector configuration automatically."
---

# Exasol ITDE Skill

Trigger when the user mentions **ITDE**, **docker-db**, **local Exasol Docker database**, **bring_itde_up**, **restart_itde**, **take_itde_down**, or **local notebook-connector database setup**.

## Routing Algorithm

1. **Start local Docker DB**
   - Trigger phrases: `bring_itde_up`, `start local exasol`, `docker-db`
   - Load: `references/itde-lifecycle.md`
   - Use scripts from: `scripts/`

2. **Check status / restart / tear down**
   - Trigger phrases: `get_itde_status`, `restart_itde`, `take_itde_down`, `container status`
   - Load: `references/itde-lifecycle.md`
   - Use scripts from: `scripts/`

3. **Config not present yet**
   - Activate **exasol-notebook-connector-config**

## Validation

Use the lifecycle scripts to validate the stored ITDE setup:

- run `scripts/check_itde_status.py` after setup changes
- after `bring_itde_up`, expect `ItdeContainerStatus.READY`
- if the next step is the shared **exasol-notebook-connector-config** validation flow, save `storage_backend=onprem` first because `bring_itde_up(...)` does not populate that key itself
- set `db_schema` yourself before handing off to schema-dependent workflows such as SQLAlchemy, Ibis, TE, or TXAIE validation
- after teardown, expect `ABSENT` or a clean no-container state

Expected failure mode:

- `scripts/restart_itde.py` should raise a runtime error if the Docker-DB container does not exist yet
- shared setup validation can fail with missing `storage_backend` or `db_schema` even when ITDE itself is healthy, because those keys are not written by `bring_itde_up(...)`
- if status checks fail because the store is missing, switch back to **exasol-notebook-connector-config**

## Notes

- ITDE is the easiest local development database path for notebook-connector.
- `bring_itde_up` populates the secure config store with the generated DB and BucketFS connection details automatically.
- `bring_itde_up` does not populate `storage_backend` or `db_schema`.
- After ITDE is ready, other notebook-connector connection APIs can be used without manual DB/BucketFS entry.
