---
name: rehashing-datavault4dbt-entities
description: Recalculates hashkeys and hashdiffs across an existing raw vault with datavault4dbt's rehashing macros after a change to the hash algorithm, datatype, trimming, or case sensitivity — including the v1→v2.0.0 upgrade. Use when changing hash global variables, migrating hash logic, or upgrading datavault4dbt without dropping history.
allowed-tools: "Bash(dbt *), Read, Write, Edit, Glob, Grep"
user-invocable: false
metadata:
  author: scalefree
---

# Rehashing datavault4dbt entities

When you change anything that affects hash output — the algorithm (`MD5`→`SHA2`), `hash_datatype`,
`hashdiff_use_trim`, or case-sensitivity vars — every hashkey and hashdiff in the Raw Data Vault must
change too, or referential integrity breaks. You have two options:

1. **Full refresh** the RDV (only if the full source history is still available to reload), or
2. **Rehash** existing entities in place with the package's rehashing macros (when history is *not*
   reloadable).

This skill is about option 2.

> **v1 → v2.0.0 upgrade.** v2.0.0 unifies/corrects hash standardization: with default settings,
> hashkeys are now `UPPER`-normalized and hashdiffs are no longer `UPPER`-normalized, plus
> adapter-specific changes (Oracle/Redshift concat-string alignment, BigQuery MD5 fix, Fabric/Exasol
> standardization). Hash values differ from v1, so crossing this boundary on an existing vault requires
> a full refresh or a rehash.

## The safe workflow (always)

1. **Start small** — rehash one test entity first and verify the configuration and logic.
2. **Overwrite, don't drop** — set `overwrite_hash_values: true` and keep `drop_old_values: false`.
   The macros rename the old columns with a `_deprecated` suffix instead of deleting them.
3. **Validate** — compare the new hash columns against the `_deprecated` columns.
4. **Clean up** — only after validation, drop the deprecated columns. The dbt log prints the dict of
   columns to drop; use it to build a cleanup model or call
   `datavault4dbt.custom_alter_relation_add_remove_columns`.

## Single-entity rehash (surgical)

Run a one-off operation against a single hub/link/satellite:

```bash
dbt run-operation rehash_single_hub --args '{
    hub: customer_h,
    hashkey: HK_CUSTOMER_H,
    business_keys: C_CUSTKEY,
    overwrite_hash_values: true
}'
```

## Bulk rehash by entity type (YAML-driven)

Create a dedicated model that calls the bulk macro with YAML metadata:

```sql
-- models/rehash/rehash_hubs.sql
{{ config(materialized='view') }}
{% set hub_yaml %}
config:
    overwrite_hash_values: true
hubs:
    - name: customer_h
      hashkey: hk_customer_h
      business_keys: [c_custkey]
    - name: order_h
      hashkey: hk_order_h
      business_keys: [order_id]
{% endset %}

{{ datavault4dbt.rehash_hubs(hub_yaml=hub_yaml, drop_old_values=false) }}

SELECT 'success' as status
```

```bash
dbt run -s rehash_hubs
```

The hub then holds both the new hashkey and the `_deprecated` old one, so you can validate before
cleanup.

## Full RDV rehash (ordered)

`rehash_all_rdv_entities` processes the whole vault in the correct order — **hubs first**, then
**links** (aligned to the new hub hashkeys), then **satellites** (standard, multi-active,
non-historized; recalculating hashkeys and hashdiffs):

```sql
-- models/rehash/rehash_entire_rdv.sql
{{ config(materialized='view') }}
{% set entity_yaml %}
config:
    overwrite_hash_values: true
hubs:
  - name: customer_h
    hashkey: hk_customer_h
    business_keys: [c_custkey]
links:
  - name: customer_order_l
    link_hashkey: hk_customer_order_l
    hub_config:
        - hub_name: customer_h
          hub_hashkey: hk_customer_h
          business_keys: [c_custkey]
satellites:
  - name: customer_s
    hashkey: hk_customer_h
    hashdiff: hd_customer_s
    parent_entity: customer_h
    payload: [c_name, c_address]
{% endset %}

{{ datavault4dbt.rehash_all_rdv_entities(entity_yaml=entity_yaml, drop_old_values=false) }}

SELECT 'success' as status
```

```bash
dbt run -s rehash_entire_rdv
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `drop_old_values: true` on the first pass | Keep `false`; validate against `_deprecated` columns before dropping |
| Rehashing the whole vault before testing | Start with one entity to confirm config |
| Rehashing links before hubs | Use `rehash_all_rdv_entities` (handles order) or run hubs → links → satellites |
| Forgetting hashdiffs | Satellites need both hashkey and hashdiff recalculated — provide `hashdiff` + `payload` |
| Reloading instead of rehashing when history is gone | If you can't reload full history, rehash; don't truncate |

Authoritative reference: `dbt_packages/datavault4dbt/docs/26_general-usage-notes/41_rehashing`.
