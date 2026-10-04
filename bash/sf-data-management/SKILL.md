---
name: sf-data-management
description: Moving records in and out of a Salesforce org - choosing between sObject tree seeding, Bulk API 2.0 and synchronous composite calls by volume, the sf data command surface (import bulk, export bulk, upsert bulk, delete bulk, import tree, export tree, query, resume), external ids and upsert keys, load ordering for parent-child data, Bulk API 2.0 limits and allocations, hard delete and the Recycle Bin, CSV shaping and field caps, scratch org and sandbox seeding, and data-loss safety on destructive schema changes. Use when seeding a scratch org, migrating or backfilling records, writing a data load script, extracting production-shaped test data, or planning a schema change that moves or drops data.
---

# Data Management

## When to use

- Seeding a scratch org or a developer sandbox so the feature under test has records to work on.
- Backfilling a new field, migrating records between orgs, or extracting a sample of real data.
- Planning a schema change that moves, reshapes or drops data.
- A deploy is blocked because a field cannot be deleted while data still references it.

This skill covers moving **records**. Moving **metadata** is skill `sf-deployment-strategies`;
`sfdx-project.json` and package directories are skill `sf-project-structure`.

## Pick the mechanism by volume

| Records | Mechanism | Command |
| --- | --- | --- |
| A handful, hand-written, relationships by reference | sObject tree | `sf data import tree` |
| 1 to a few hundred, ad hoc | Single-record commands | `sf data create record`, `sf data update record`, `sf data delete record` |
| Under 2,000 | Bulkified synchronous REST (Composite) or SOAP | Outside the CLI, or `sf data import bulk` anyway |
| Over 2,000 | **Bulk API 2.0** | `sf data import bulk`, `sf data upsert bulk`, `sf data update bulk`, `sf data delete bulk` |
| Reading over 10,000 | **Bulk API 2.0 query** | `sf data export bulk` |
| Reading under 10,000 | Synchronous query | `sf data query` |

The 2,000 threshold is the guide's own: "Any data operation that includes more than 2,000 records
is a good candidate for Bulk API 2.0. Jobs with fewer than 2,000 records should involve bulkified
synchronous calls in REST (for example, Composite) or SOAP."

The 10,000 threshold is the CLI's own advice: if `sf data query` would return more than 10,000
records, use `sf data export bulk` instead.

## Core patterns

### 1. Seed a scratch org from a tree plan

Export a shaped sample once, commit it, replay it forever:

```bash
sf data export tree \
  --query "SELECT Id, Name, Industry, (SELECT FirstName, LastName, Email FROM Contacts) FROM Account WHERE Industry != null LIMIT 20" \
  --plan --prefix seed --output-dir data/seed \
  --target-org acme-uat
```

`--plan` writes one JSON file per sObject plus a plan definition file. Import it into a fresh org:

```bash
sf data import tree --plan data/seed/seed-Account-Contact-plan.json --target-org my-scratch
```

Two facts that decide whether you use `--plan` or `--files`:

- Files listed in a **plan** may contain **more than 200 records**; the CLI batches them to respect
  the API's 200-record limit. Files passed with `--files` may not.
- **Order matters.** A file whose records have lookups into another file must be listed *after* it.
  Accounts before Contacts.

Plan schema: `items` (one entry per sObject type), each with `sobject` (the type name; child file
references must have roots of this type) and `files` (an array of file paths, in load order).

### 2. Load volume with Bulk API 2.0

```bash
sf data import bulk \
  --file data/accounts.csv \
  --sobject Account \
  --wait 10 \
  --target-org acme-uat
```

Without `--wait` the command starts the job, prints the id and hands the terminal back. Resume with:

```bash
sf data import resume --use-most-recent --wait 10 --target-org acme-uat
sf data bulk results --job-id <id> --target-org acme-uat
```

`--wait 0` is the default. In a script, either wait or record the job id - a fire-and-forget load
that nobody checks is a load that silently half-failed.

### 3. Upsert on an external id, never on a guessed match

```bash
sf data upsert bulk \
  --file data/accounts.csv \
  --sobject Account \
  --external-id Legacy_Id__c \
  --wait 10 \
  --target-org acme-uat
```

`--external-id` is **required** and accepts either a custom external id field or `Id`. An upsert
inserts when the key does not match and updates when it does. That is the only safe way to make a
load re-runnable.

Design the external id field with **External ID** and **Unique** set. Without unique, a duplicate
key makes the upsert ambiguous and the row fails.

### 4. Relate records without knowing Ids

In an sObject tree file, `referenceId` names a record and `@ref` points at it:

```json
{
  "records": [
    {
      "attributes": { "type": "Account", "referenceId": "acme" },
      "Name": "Acme",
      "Industry": "Manufacturing"
    },
    {
      "attributes": { "type": "Contact", "referenceId": "ada" },
      "LastName": "Lovelace",
      "AccountId": "@acme"
    }
  ]
}
```

In a CSV load, the equivalent is a relationship column keyed on the parent's external id:

```csv
LastName,Account.Legacy_Id__c
Lovelace,LEG-1001
```

That avoids a two-pass load entirely: no query for parent ids between the two files.

### 5. Extract volume out

```bash
sf data export bulk \
  --query "SELECT Id, Name, Account.Name FROM Contact" \
  --output-file out/contacts.csv \
  --result-format csv \
  --wait 10 \
  --target-org acme-uat
```

`--all-rows` includes soft-deleted records. `--query-file` reads the SOQL from a file, which keeps a
long query out of shell quoting. Resume a timed-out export with `sf data export resume`.

### 6. Delete, and decide about the Recycle Bin

```bash
sf data delete bulk --sobject Account --file data/delete.csv --wait 10 --target-org acme-uat
```

The CSV must have **one column, `Id`**, and one record id per line.

`--hard-delete` marks the records immediately eligible for deletion instead of sending them to the
Recycle Bin. Hard delete is not reversible. The vibe-force Bash guard blocks destructive data
operations against a production alias unless `VF_ALLOW_PROD=1` is set - that guard exists because
this flag exists.

### 7. Query in a script

```bash
sf data query \
  --query "SELECT COUNT(Id) total FROM Account WHERE Legacy_Id__c != null" \
  --target-org acme-uat --json | jq '.result.records[0].total'
```

`--result-format` takes `human` (default), `csv` or `json`; `--json` overrides it. `--use-tooling-api`
switches to Tooling objects. Post-deploy verification queries live in skill
`sf-post-deploy-verification`.

## Limits that shape the plan

| Item | Bulk API 2.0 |
| --- | --- |
| Batch allocation | 15,000 batches per rolling 24 hours, **shared** with Bulk API 1.0. Only ingest jobs consume batches; query jobs do not |
| Records uploaded per 24 hours | 150,000,000 |
| Maximum file size per job | 150 MB of base64-encoded content. Upload data stays under **100 MB** to leave room for the roughly 50% base64 increase |
| Maximum characters in a field | 131,072 |
| Maximum fields in a record | 5,000 |
| Maximum characters in a record | 400,000 |
| Job lifespan | Terminal-state jobs older than 7 days are deleted; non-terminal jobs are periodically cleaned up |
| Maximum time a job can stay open | 24 hours (ingest jobs only) |
| Results lifespan | Retrievable within 7 days of job completion unless the job is deleted |
| Retries | Handled automatically. "Retried more than 20 times" on ingest means use a smaller file; "more than 15 times" on query means add filter criteria |
| Query results timeout | 20 minutes |

Batches are created for you in Bulk API 2.0. In Bulk API 1.0 you create them yourself, at up to
10,000 records and 10 MB each - which is why 1.0 is the one that runs out of the shared 15,000-batch
allocation first.

Full tables including Bulk API 1.0 and query-job specifics:
[references/bulk-api-limits.md](references/bulk-api-limits.md).

## Data-loss safety

No destructive metadata change without a backout path. The rules that matter:

| Change | Risk | Required handling |
| --- | --- | --- |
| Deleting a field | Data in it is gone | Stop writing it in one release, delete it in a later one. Export the column first |
| Changing a field type | Silent truncation or conversion failure | Export, change, re-import, verify counts |
| Converting a master-detail relationship | **Cannot be converted once data exists** | Rebuild the relationship as a controlled migration |
| Changing an org-wide default to more restrictive | Records disappear from users' views | Verify with a query as an affected user before and after |
| Hard delete | Not reversible | `--hard-delete` never runs against production without `VF_ALLOW_PROD=1` |

Always take a count before and after:

```bash
sf data query --query "SELECT COUNT(Id) c FROM Account" --target-org acme-uat --json | jq '.result.records[0].c'
```

A load that reports success and changes no counts did not do what you think.

## Anti-patterns

### Loading with `Id` as the upsert key from another org

Record ids are not portable between orgs. An upsert on `Id` against a target org where those ids do
not exist inserts duplicates. Use a real external id field.

### A CSV with no external id at all

The load works once. The re-run creates a second copy of everything. Every repeatable load needs a
unique, indexed external id.

### Children before parents

```bash
sf data import tree --files Contact.json,Account.json   # wrong order
```

The Contact lookups have nothing to resolve against. List Accounts first, or use a plan file with
the items in dependency order.

### `sf data query` for a migration extract

Over 10,000 records it is the wrong tool; the CLI says so itself. Use `sf data export bulk`.

### Fire-and-forget bulk jobs in CI

```bash
sf data import bulk --file big.csv --sobject Account --target-org acme-uat
echo "loaded"    # nothing was verified; --wait defaults to 0
```

Either `--wait` and check the exit code, or capture the job id and poll `sf data bulk results`.

### Using Apex to load volume

A migration inside Apex spends the 10,000-DML-row per-transaction limit and the CPU budget for
nothing. Bulk API 2.0 exists so the load happens outside a transaction. See skill
`sf-governor-limits`.

### Seeding with production data unfiltered

Real records carry real personal data. Extract a shaped sample with a `LIMIT` and a `WHERE`, scrub
the columns that matter, and commit *that*. Record-level access rules for the data once loaded are
in skill `sf-security-model`.

## Verification

```bash
# The load itself
sf data import bulk --file data/accounts.csv --sobject Account --wait 10 --target-org <alias>
sf data bulk results --job-id <id> --target-org <alias>

# Counts before and after
sf data query --query "SELECT COUNT(Id) c FROM Account" --target-org <alias> --json | jq '.result.records[0].c'

# Rows that failed to match their parent
sf data query --query "SELECT COUNT(Id) c FROM Contact WHERE AccountId = null" --target-org <alias> --json

# Org storage and API capacity before a big job
sf org list limits --target-org <alias>

# The vibe-force post-deploy gate, which runs verification queries
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org <alias>
```

## References

- [references/bulk-api-limits.md](references/bulk-api-limits.md) - Bulk API 2.0 and 1.0 limits and allocations
- [references/cli-data-commands.md](references/cli-data-commands.md) - every `sf data` command with its required flags
- [references/load-recipes.md](references/load-recipes.md) - seeding, migration, backfill and extract recipes end to end

Sibling skills: `sf-cli-operations` (auth, config, JSON output conventions),
`sf-scratch-orgs-sandboxes` (org lifecycle and what seeding runs against),
`sf-project-structure` (`sfdx-project.json`, where seed data lives in the repo),
`sf-soql-sosl-optimization` (selective queries for extracts),
`sf-governor-limits` (why volume does not belong in Apex),
`sf-deployment-strategies` (destructive metadata changes and backout),
`sf-security-model` (access to the data once it is loaded),
`sf-post-deploy-verification` (verification queries after a release).

Sources: Salesforce Developer Limits and Allocations Quick Reference, "Bulk API and Bulk API 2.0
Limits and Allocations"; Bulk API 2.0 and Bulk API Developer Guide; Salesforce CLI command
reference for `sf data`. All Summer '26 / API version 67.0.
