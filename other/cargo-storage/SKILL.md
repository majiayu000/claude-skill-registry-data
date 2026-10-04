---
name: cargo-storage
description: "Work with the data inside a Cargo workspace — models (Companies, Contacts, Deals…), datasets, columns, relationships, records, and SQL over workspace storage. Triggers: \"what models do I have\", \"show me the schema\", \"add a column for\", \"how many contacts do I have\", \"SELECT … FROM\", \"query my companies table\", \"join contacts to companies\", \"what is the DDL\", \"set up a webhook-fed model\", \"where does this field live\", \"import this into a model\", \"unify these models\", \"merge duplicate accounts\", \"link contacts to companies\", \"set up a relationship between\". Skip when: querying run or batch telemetry rather than business data — use cargo-orchestration; naming a reusable filtered audience — use cargo-segmentation."
version: "1.2.3"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Storage

Data layer management: inspecting and modifying models, datasets, columns, relationships, unification, and records, and running SQL queries against workspace storage.

> See `references/response-shapes.md` for full JSON response structures.
> See `references/troubleshooting.md` for common errors and how to fix them.
> See `references/examples/models.md` for model CRUD, DDL inspection, and schema discovery examples.
> See `references/examples/datasets.md` for dataset listing and navigation examples.
> See `references/examples/columns.md` for column creation and management examples.
> See `references/examples/queries.md` for `storage query execute` / `storage query download` SQL examples (WHERE, aggregations, joins, pagination, exports).
> See `references/examples/ingest-webhook.md` for ingest (webhook-fed) models — deriving the webhook URL and POSTing records.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Discover resources first

Always list before inspecting or modifying.

```bash
cargo-ai storage dataset list              # all datasets (uuid, slug)
cargo-ai storage model list                # all models (uuid, name, slug, columns, datasetUuid)
# `model list` takes no flags — filter its output instead:
cargo-ai storage model list | jq '[.models[] | select(.datasetUuid == "<uuid>")]' 
```

**Retrieve in the UI:** models live at `app.getcargo.io/workspaces/<WORKSPACE_UUID>/models/<MODEL_UUID>`. Get `<WORKSPACE_UUID>` from `cargo-ai whoami` under `workspace.uuid`.

## Quick reference

```bash
cargo-ai storage model list
cargo-ai storage model get <model-uuid>
cargo-ai storage model get-ddl <model-uuid>
cargo-ai storage dataset list
cargo-ai storage column list --model-uuid <uuid>
cargo-ai storage relationship list
cargo-ai storage record list --model-uuid <uuid>
cargo-ai storage query execute "SELECT * FROM default.companies LIMIT 10"
cargo-ai storage query download --query "SELECT * FROM default.companies"
```

## Models

Models are structured tables in your workspace (e.g. Companies, Contacts).

```bash
# List all models
cargo-ai storage model list

# List models in a dataset — every model carries `datasetUuid`, and
# `model list` has no flags of its own, so filter client-side
cargo-ai storage model list | jq '[.models[] | select(.datasetUuid == "<uuid>")]' 

# Get a single model (includes columns)
cargo-ai storage model get <model-uuid>

# Get the DDL (full schema, table name and SQL dialect)
cargo-ai storage model get-ddl <model-uuid>
# → Useful for column discovery and SQL dialect (BigQuery vs Snowflake) before writing queries

# Create a model
cargo-ai storage model create \
  --slug contacts \
  --name "Contacts" \
  --dataset-uuid <uuid> \
  --extractor-slug <extractor-slug> \
  --config '{}'

# Update a model
cargo-ai storage model update --uuid <model-uuid> --name "New Name"

# Remove a model
cargo-ai storage model remove <model-uuid>
```

**Querying:** Use `cargo-ai storage query execute "<sql>"` (or `storage query download --query "<sql>"` for full exports) to run SQL against storage. Tables are referenced as `<datasetSlug>.<modelSlug>` (e.g. `default.companies`) and rewritten to the underlying storage table under the hood. See [Query with SQL](#query-with-sql) below.

## Ingest models (webhook-fed)

A model whose extractor has `mode.kind === "ingest"` — `http.listenHook` and
friends — is filled by **pushing** records to Cargo. The app shows a "Webhook URL"
on the model settings screen; **no CLI command or API field returns it**, but it's
assembled from values the CLI already exposes:

```
<baseUrl>/v1/models/<model-uuid>/records/ingest?token=<api-token>
```

```bash
MODEL_UUID=<model-uuid>
BASE=$(cargo-ai whoami | jq -r '.baseUrl')
TOKEN=$(cargo-ai workspaceManagement token list | jq -r '.tokens[0].token')
echo "$BASE/v1/models/$MODEL_UUID/records/ingest?token=$TOKEN"
```

**Not for workflows.** A Cargo workflow writes to a model with the native
`modelUpsert` / `modelInsert` action (see `cargo-orchestration` →
`references/nodes.md` → "Storage"). An HTTP node calling this URL costs an extra node,
a payload script, and an API token pasted into the node config. The webhook is for
systems outside Cargo.

Check the extractor's mode first — when it reports `"autoIngest": true` (calendly,
smartlead, instantlyV2, heyReach, cargo signals) Cargo registers the
hook with the provider itself and the URL must **not** be handed out. Full flow,
payload shapes, and limits: `references/examples/ingest-webhook.md`.

## Datasets

Datasets are logical groupings of models.

```bash
# List all datasets
cargo-ai storage dataset list

# Get a single dataset
cargo-ai storage dataset get <dataset-uuid>
```

## Columns

Columns define the schema of a model.

```bash
# List columns for a model
cargo-ai storage column list --model-uuid <uuid>

# Create a column
cargo-ai storage column create \
  --model-uuid <uuid> \
  --column '{"slug":"my_column","type":"string","label":"My Column","kind":"custom"}'

# Update a column (pass the full column object — columns are identified by slug, not UUID)
cargo-ai storage column update \
  --model-uuid <uuid> \
  --column '{"slug":"my_column","type":"string","label":"Updated Label","kind":"custom"}'

# Remove a column
cargo-ai storage column remove --model-uuid <uuid> --column-slug <slug>

# Reorder a column (move to a specific index)
cargo-ai storage column reorder --model-uuid <uuid> --column-slug <slug> --to-index 2
```

Column types: `string`, `number`, `boolean`, `date`, `object`, `array`, `vector`, `any`.

Column kinds: `custom` (user-defined), `computed` (expression over other columns), `metric` (aggregated from a related model), `lookup` (single field pulled from a related model via a join).

## Preview what you built

A column list doesn't tell the user whether the model is right — rows do. Two checkpoints (the pack-wide convention lives in [`../cargo/references/interaction.md`](../cargo/references/interaction.md) §4):

**1. Right after `model create` / `column create` — show the schema, not rows.** A new model is empty; a `LIMIT 10` here returns nothing and reads as failure. Echo the columns as a compact table instead (column, type, what will fill it).

**2. As soon as data lands — show the rows.** After a batch, play, or import writes into the model, preview it:

```bash
cargo-ai storage query execute \
  "SELECT * FROM <dataset-slug>.<model-slug> LIMIT 10"
```

Show ~10 rows and only the columns that carry meaning. Storage queries are free, so this costs nothing but a few lines of output — and it's the first moment the user can actually see what they built. When a play fills a *new* column, preview that column next to the record's identifying fields (`name`, `domain`) so filled vs. empty is obvious.

If the preview comes back empty or all-null when it shouldn't, that's a finding — surface it rather than reporting the write as a success. See [`cargo-diagnostics`](../cargo-diagnostics/SKILL.md) to trace why.

## Relationships

Relationships link models together (e.g. Contacts belong to Companies). They are
authored from the CLI, not just the UI.

`relationship list` takes **no flags** — it returns every relationship in the
workspace. Filter client-side on `fromModelUuid` / `toModelUuid`.

```bash
cargo-ai storage relationship list
```

**`relationship set` replaces the dataset's whole relationship set.** It takes a
dataset and the complete list that should exist within it: entries carrying a
`uuid` are updated, entries without one are created, and **any existing
relationship whose `uuid` is absent from the payload is deleted**. Sending one
relationship to a dataset that has five removes the other four. Always `list`
first, then send back the full array with your addition:

```bash
cargo-ai storage relationship set \
  --dataset-uuid <dataset-uuid> \
  --relationships '[
    {"uuid":"<existing-uuid>","fromModelUuid":"<contacts-uuid>","fromColumnSlug":"account_id","toModelUuid":"<companies-uuid>","toColumnSlug":"id","relation":"manyToOne"},
    {"fromModelUuid":"<deals-uuid>","fromColumnSlug":"company_id","toModelUuid":"<companies-uuid>","toColumnSlug":"id","relation":"manyToOne"}
  ]'
```

`relation` is `oneToOne`, `manyToOne`, or `oneToMany`. Both models must live in
the dataset you pass — relationships never span datasets, so `fromDatasetUuid`
and `toDatasetUuid` on the response always equal `--dataset-uuid`.

Failure reasons: `datasetNotFound`; `invalidRelationships` (a column slug or
model UUID that doesn't resolve, or a duplicate — including the same pair stated
in reverse); `modelNotCompatible` (see below).

**Unify models refuse manual relationships.** In the native dataset, a unify
model's relationships are generated during sync, so naming one as `fromModelUuid`
or `toModelUuid` returns `modelNotCompatible`. Those auto-generated rows are also
excluded from the replace above, so a `set` call cannot delete them.

## Unification

Unification is what merges records from several source models into one canonical
account/contact — and it is **configurable from the CLI**, via `--unification` on
`model update`. Pass `null` to clear it.

```bash
# Connector-driven: the integration decides how records unify
cargo-ai storage model update --uuid <model-uuid> --unification '{"source":"integration"}'

# Custom: you name the type, the matching keys, and optionally a parent
cargo-ai storage model update --uuid <model-uuid> --unification '{
  "source": "custom",
  "type": "account",
  "uniqueColumns": [{"slug":"domain","reference":"domain"}],
  "selectedColumnSlugs": ["name","industry","employee_count"],
  "parent": {"kind":"model","columnSlug":"account_id","parentModelUuid":"<accounts-uuid>"}
}'
```

| Field | Applies to | Meaning |
|---|---|---|
| `source` | both | `integration` (connector-defined) or `custom` |
| `type` | custom | `account`, `contact`, `accountEvent`, `contactEvent` |
| `uniqueColumns` | custom | Match keys — `{slug, reference}` per column. This is what decides which rows are the same entity |
| `selectedColumnSlugs` | custom | Columns carried into the unified model. Omit for all |
| `timeColumnSlug` | custom | Event timestamp — for the two `*Event` types |
| `parent` | custom | Links contacts/events to their account: `{"kind":"model","columnSlug":…,"parentModelUuid":…}` or `{"kind":"reference","columnSlug":…,"reference":…}` |
| `filter` | custom | Segmentation filter restricting which rows unify — same `conjonction` shape as segments |

**Writing the config does not recompute anything.** The unified rows are rebuilt
by the model's sync run, so follow the update with a run and poll it:

```bash
cargo-ai storage run create --model-uuid <model-uuid>
cargo-ai storage run list --model-uuid <model-uuid>
```

Get the current config from `storage model get <uuid>` → `unification` (`null`
when the model doesn't unify). Once the run finishes, check the row count with
`storage query execute` before treating the change as done — a too-narrow
`uniqueColumns` under-merges and a too-broad one collapses distinct entities, and
both look like a successful run.

## Records

```bash
# List records in a model
cargo-ai storage record list --model-uuid <uuid>
```

For advanced record queries (filtering, sorting, pagination), use `segmentation segment fetch` from the `cargo-orchestration` skill.

## Query with SQL

Run SQL against workspace storage with `storage query execute`. Tables are referenced as `<datasetSlug>.<modelSlug>` (e.g. `default.companies`) and rewritten to the underlying storage table under the hood — no DDL lookup is needed for the table name.

```bash
cargo-ai storage query execute \
  "SELECT name, domain FROM default.companies LIMIT 10"
# → { "rows": [...] } on success; non-zero exit with { "errorMessage": "..." } on error
```

For full exports, use `storage query download` — it returns a signed URL to a CSV (default) or Parquet file:

```bash
cargo-ai storage query download \
  --query "SELECT name, domain, revenue FROM default.companies ORDER BY revenue DESC"

cargo-ai storage query download \
  --query "SELECT * FROM default.companies" --format parquet
```

Get column slugs from `storage column list --model-uuid <uuid>` (or run `storage model get-ddl <model-uuid>` for the full schema and SQL dialect). Page through large result sets with `LIMIT` / `OFFSET` directly in the SQL.

See `references/examples/queries.md` for WHERE clauses, aggregations, joins, date queries, pagination, and the failure shapes returned on error.

## Help

Every command supports `--help`:

```bash
cargo-ai storage model list --help
cargo-ai storage column create --help
cargo-ai storage relationship set --help
cargo-ai storage query execute --help
cargo-ai storage query download --help
```
