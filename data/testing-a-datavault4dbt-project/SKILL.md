---
name: testing-a-datavault4dbt-project
description: Adds Data Vault 2 technical tests to a datavault4dbt project — hashkey uniqueness and not-null, link-to-hub referential integrity, and satellite key+load-date uniqueness — as dbt soft-constraint tests in YAML. Use when adding or reviewing tests for hubs, links, or satellites, or validating raw vault integrity.
allowed-tools: "Bash(dbt *), Read, Write, Edit, Glob, Grep"
user-invocable: false
metadata:
  author: scalefree
---

# Testing a datavault4dbt project

Turn the Primary-Key and Foreign-Key assumptions of Data Vault 2 into dbt tests. In DV2 these are
**soft constraints** — implemented as dbt tests that warn (and let you investigate) rather than
hard database constraints that would silently drop "bad and ugly" raw data you still want to capture.

**Default to soft constraints (dbt tests).** Only use hard database constraints if you accept the risk
of losing non-conforming raw data and have an Error Mart to catch it.

## Where these tests live

Add `data_tests` in the model's YAML file (colocated with the `.sql`). Generic tests `unique` and
`not_null` are built in; `relationships` covers FK integrity. For multi-column uniqueness (satellites)
use `dbt_utils.unique_combination_of_columns` (add the `dbt_utils` package) or an equivalent.

## The technical test matrix

| Entity | Column(s) | Test |
|--------|-----------|------|
| Hub | hashkey | `not_null`, `unique` |
| Link | link hashkey | `not_null`, `unique` |
| Link | each foreign hashkey | `relationships` to its connected hub's hashkey |
| Satellite v0 | hashkey + load date | unique combination of columns |
| Satellite v0 | hashkey | `relationships` to parent hub/link |
| Non-historized link | link hashkey | `not_null`, `unique` |
| Non-historized link | each foreign hashkey | `relationships` to connected hubs |
| Non-historized satellite v0 | hashkey | `not_null`, `unique`, `relationships` to parent NH-link |
| Multi-active satellite v0 | hashkey + load date + multi-active key(s) | unique combination of columns |
| Multi-active satellite v0 | hashkey | `relationships` to parent hub/link |
| Record-tracking satellite | hashkey + load date | unique combination of columns |
| Record-tracking satellite | hashkey | `relationships` to parent hub/link |
| Reference hub | reference key(s) | `unique`, `not_null` |
| Reference satellite v0 | reference key(s) + load date | unique combination of columns |

(Authoritative source: `dbt_packages/datavault4dbt/docs/26_general-usage-notes/40_testing-a-data-vault`.)

## Examples

Hub — hashkey is the PK:

```yaml
models:
  - name: customer_h
    columns:
      - name: hk_customer_h
        data_tests: [unique, not_null]
      - name: CUSTOMER_ID
        data_tests: [not_null]
```

Link — hashkey unique + each FK references its hub:

```yaml
models:
  - name: contract_customer_l
    columns:
      - name: hk_contract_customer_l
        data_tests: [unique, not_null]
      - name: hk_contract_h
        data_tests:
          - not_null
          - relationships: {to: ref('contract_h'), field: hk_contract_h}
      - name: hk_customer_h
        data_tests:
          - not_null
          - relationships: {to: ref('customer_h'), field: hk_customer_h}
```

Satellite v0 — hashkey + load date is the grain; hashkey references the parent:

```yaml
models:
  - name: customer_s_v0
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [hk_customer_h, ldts]
    columns:
      - name: hk_customer_h
        data_tests:
          - not_null
          - relationships: {to: ref('customer_h'), field: hk_customer_h}
```

> A satellite hashkey is **not** unique on its own (it has history). Test uniqueness on
> `hashkey + ldts` (and the multi-active key[s] for MA-sats), never the hashkey alone.

## Running

```bash
dbt build --select <model>+      # build a model and run its tests, downstream too
dbt test --select tag:raw_vault  # run only the raw-vault tests
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `unique` on a satellite hashkey | Satellites are historized — test `hashkey + ldts` uniqueness instead |
| Skipping link→hub `relationships` | Add a relationship test per foreign hashkey; this catches orphaned links |
| Hard DB constraints on the RDV | Use soft constraints (tests); hard constraints can drop raw data |
| Forgetting the multi-active key in MA-sat uniqueness | Grain is `hashkey + ldts + multi_active_key(s)` |
| Using `unique_combination_of_columns` without `dbt_utils` | Install `dbt_utils` (or use an equivalent multi-column uniqueness test) |
