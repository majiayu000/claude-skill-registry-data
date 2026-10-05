---
name: rudder-data-graphs
description: Produces Data Graph YAML from RETL sources for Audiences. Use when designing Data Graphs, mapping RETL to entities/events, or assessing customer fit for Audiences.
allowed-tools: "Bash(rudder-cli *), Read, Write, Edit"
---

# RETL Connection Analysis & Data Graph Design

## What this skill produces

Given a customer name (or workspace / org identifier), this skill produces five deliverables, in order:

1. **Source Inventory** — every relevant RETL source categorized as entity / event / audience / supporting-only.
2. **Untapped Segment List** — realistic, filterable business dimensions the customer has not yet expressed as audiences.
3. **Data Graph YAML** — one per workspace / domain, ready for validation in `rudder-cli` or the visual builder.
4. **Demo Warehouse Spec** — tables, key columns, joins, and known / inferred schema details needed to mock the graph.
5. **Action Items** — priority-ordered next steps, including the upgrade narrative and any assumptions to confirm.

The end-to-end flow is: find workspaces → list RETL sources → shortlist relevant sources → fetch full configs for the shortlist → categorize → design graph → validate → hand off. Each step below says what to do and *why*, so you can adapt when the customer doesn't match the common shapes.

---

## Step 1 — Find the customer's workspaces

1. `admin_search_organizations(company_name=...)` to get the `org_id`.
2. `admin_search_workspaces(search_by=organizationId)` using that id.
3. Keep only `status=ACTIVE` workspaces. *Why:* inactive workspaces often have stale or disconnected configs and will produce misleading source lists.
4. Note the likely warehouse-backed workspaces, but **do not assume you already have the correct `accountId` at this stage**. *Why:* the Data Graph YAML embeds `account_id`, and that value is the warehouse account the graph runs against. The most authoritative source for it is `rudder-cli workspace accounts list --json` (see Step 4a); a RETL source config is a convenient secondary hint when one already exists, but it is not a prerequisite.

---

## Step 2 — Discover sources, anchored on audiences

Run `list_sources(workspace_id=..., retl_type=all, includeConfig=false)` per workspace. *Why `includeConfig=false`:* full configs blow the context budget on large workspaces; start broad, then fetch detail only for sources you actually need.

**Important:** `includeConfig=false` is a discovery pass only. You cannot extract `filterSpec`, SQL, join hints, or reliable `accountId` values from that response alone. After shortlisting sources, fetch full config for the shortlisted source ids before making graph decisions.

**Audience sources are the anchor signal.** *Why:* this skill exists to build Audiences. Audience RETL sources are the customer's own pre-validated statements about what they segment on. A workspace can have hundreds of table sources but only a handful of audiences, and the audiences point directly at the entities that matter for activation.

**Discovery order:**

1. **List every audience source first** from the discovery pass.
2. **Fetch full config for those audience sources** and extract:
   - `config.filterSpec.filterGroups[].filters[].fieldName` — the fields the customer actually filters on.
   - The underlying table/model reference — this is the anchor entity for that audience.
   - `primaryKey` and any source-level `accountId` if present.
3. **Pull in the tables/models that back those audiences.** Fetch full config for those backing sources too. These are non-negotiable: you need their schema shape to size the entity properly and to compute untapped segments in Step 6.
4. **Scan remaining tables/models for supporting roles:**
   - **Event candidates** — tables/models with a real business-time timestamp (`ordered_at`, `sent_at`, `opened_at`, etc.) and a clear relationship back to an entity. Pull these in; events are a major Data Graph unlock that audiences alone can't surface.
   - **FK targets** — tables/models referenced by foreign keys from anchor entities (e.g., if the anchor `contact` has a `branch_id`, pull in `branch`). Pull these in.
   - **Everything else** — keep in the Source Inventory for completeness, but do not force into the Data Graph unless it materially improves segmentation or the customer asks. Noise suppression matters on large workspaces.
5. **Resolve `accountId` only after the shortlist exists.** Cross-check the warehouse account id from the specific RETL source configs you are actually using in the graph against `rudder-cli workspace accounts list` (see Step 4a). If shortlisted sources disagree on `accountId`, stop and flag it; one graph should not span multiple warehouse accounts.

**What to extract, by sourceType:**

| `sourceType` | Fields to read | What you can trust from it |
|---|---|---|
| `audience` | `config.filterSpec.filterGroups[].filters[].fieldName`, underlying table/model ref, `primaryKey`, `accountId` if present | fields already used for segmentation, anchor entity, graph account hint |
| `table` | `config.table`, `config.schema`, `primaryKey`, `accountId` if present | physical table identity and PK |
| `model` | `config.sql`, `primaryKey`, `accountId` if present | model intent and projected columns/aliases; not guaranteed types |

### Fallback — customer has no audience sources yet

This is common. RETL Audiences is recent; many customers have extensive table/model sources but zero audiences. *Don't stop* — this is the exact customer who most needs the Data Graph pitch.

When audiences are absent, switch the anchor:

1. **Ask the customer (or infer from destination mappings) which entities they currently activate on.** If `dim_contact` is synced to HubSpot, contacts are an activation entity. Treat those tables/models as anchor entities.
2. **Apply the same "pull in FK targets and event candidates" rules** around those anchors.
3. **Frame Step 6 differently:** this is not "unused audience fields" anymore. It becomes "high-value segment ideas available from the entity's business dimensions and related events."
4. **State this explicitly in Step 7:** the customer is being introduced to the feature, not shown gaps in an already-mature audience program.

---

## Step 3 — Categorize into entity / event / audience

Every shortlisted source becomes one of:

- **Entity** — stable single-row business object with a durable primary key. Examples: users, branches, contacts, accounts, products.
- **Event** — row semantics are "something happened at time X" and the row has a true business timestamp. Examples: orders, leads sent, page views.
- **Audience overlay** — an audience source is *not* a new entity in the Data Graph; it is a saved filter over an existing entity or model.
- **Supporting-only** — useful for analysis or demo context but not worth modeling directly in the graph.

**Edge cases** (these come up often enough to call out):

- **Composite primary key** — do not casually pick one component and do not silently concatenate unless that synthetic id is stable, documented, and actually unique. Prefer an upstream model that exposes a deliberate single-column id for the graph.
- **No primary key** — usually an event, aggregate, or throwaway helper table. Confirm before modeling it as an entity.
- **SCD2 / row-versioned dimensions** — if a dimension carries a surrogate row-version key (`*_KEY`), a stable business id, and effective/end-date columns, use the **surrogate `*_KEY` as `primary_id`** — that is the column fact tables join on; the business id is usually absent from facts. The graph includes every version row unless you filter to current rows (`is_current = true`) at the model layer, so unfiltered SCD2 entities over-count.
- **Templated SQL in model sources** — render it with the current context before parsing columns; raw template text will miss projected fields.
- **Ingestion-metadata timestamps (`snapshot_date` / `loaded_at` / `_etl_timestamp` / `created_at`)** — *not* true event timestamps. They record when the row was written, not when the business event happened. Do not classify the source as an event unless a real business-time column exists — and when one does (e.g. `event_at`, `ordered_at`), use it for the event's `timestamp`, never the ingestion column.
- **Soft-deleted rows** — if the table has an `is_deleted` / `deleted_at` column, the Data Graph will include them unless filtered. Note this; the customer may want a filter at the model layer.
- **Multi-tenant columns** — if the warehouse is multi-tenant (e.g., `tenant_id`), surface that column in the entity shape and call out scoping expectations.
- **Audience wraps a model that joins multiple tables** — the model is the entity shape; the audience is just a saved filter on top. Use the model for the Data Graph node, not the base tables unless you are intentionally decomposing the model.

---

## Step 4 — Design the Data Graph

**One Data Graph per workspace / domain / warehouse account.** *Why:* cross-workspace joins are not supported, and mixing domains (e.g., Consumer + B2B) in one graph muddies the builder UX. Also, all models in a graph must resolve to the same warehouse account.

**Entity selection:**
- **Root entity** — the primary "who" being activated (users, branches, contacts). Mark it in YAML with `root: true` on the entity model (entity-only field). **Multiple roots are valid** — each `root: true` entity is an independent audience-builder anchor, so a graph may have one or several. The validator does *not* enforce a count (zero, one, or many all pass), so set `root` deliberately on whichever entities the builder should start from rather than relying on a default.
- **Related entities** — supporting objects with foreign-key relationships to the root.
- **Events** — timestamped activity tables tied back to an entity.

**Relationship direction — common footgun:**
- `source_join_key` is the column on the *current* model (the one declaring the relationship).
- `target_join_key` is the column on the *target* model.
- Cardinality describes how many target rows exist per source row: `branch → contacts` is `one-to-many` from the branch's perspective.
- **Declare each relationship once, on one side only.** Do not also declare the inverse on the target model — the graph traverses it both ways. A double-declaration collides on `display_name` (which must be unique across all relationships) and inflates the relationship count.

**Verify join keys before writing the YAML.** A wrong join key passes `validate` but silently returns the wrong audience population. If you have direct warehouse access (an MCP server, a CLI like `snowsql`/`bq`/`psql`, or an IDE connection), confirm every `source_join_key` and `target_join_key` exists on its table with one batched introspection query — RETL config alone does not catch typos or renamed columns:

| Warehouse | One-shot query |
|---|---|
| Snowflake | `SELECT TABLE_NAME, COLUMN_NAME FROM <DB>.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '<schema>' AND TABLE_NAME IN (...)` |
| BigQuery | `SELECT table_name, column_name FROM <project>.<dataset>.INFORMATION_SCHEMA.COLUMNS WHERE table_name IN (...)` |
| Postgres / Redshift | `SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = '<schema>' AND table_name IN (...)` |
| Databricks | `SELECT table_name, column_name FROM system.information_schema.columns WHERE table_catalog = '<catalog>' AND table_schema = '<schema>' AND table_name IN (...)`, or `DESCRIBE TABLE <catalog>.<schema>.<table>` |

If you have no warehouse access, fall back to the rule in **Validation & handoff**: flag every inferred join key and require confirmation before `apply`.

**Minimal skeleton:**

```yaml
version: "rudder/v1"
kind: "data-graph"
metadata:
  name: "<customer>-<domain>-data-graph"
spec:
  id: "<customer>-<domain>-data-graph"
  account_id: "<warehouse-account-id>"
  models:
    - id: "<root-entity>"
      type: "entity"
      primary_id: "<pk-column>"
      relationships: [...]
    - id: "<related-entity>"
      type: "entity"
      primary_id: "<pk-column>"
    - id: "<event-model>"
      type: "event"
      timestamp: "<timestamp-column>"
```

For the full annotated template (every field, relationship examples, worked example on Property-vertical data), read `references/data-graph-yaml-template.md`.

For vertical-specific starting shapes (Property / E-commerce / SaaS), read `references/industry-patterns.md` — only load the section matching the customer's vertical.

---

## Step 4a — Resolve the warehouse `account_id`

`spec.account_id` must be the id of the **warehouse account** the graph runs against. The account only needs to *exist* — it does not need to be selected in the Data Graph UI first, and you do not need a RETL source to obtain its id.

**The authoritative lookup is the CLI:**

```bash
# --json is required in agent/non-interactive contexts; the plain
# table output needs a TTY and fails when piped.
rudder-cli workspace accounts list --category source --json
```

Each line is an account object. Use the **`id`** field as `account_id`; use `name` and `options` (`account`, `dbname`, `warehouse`, `schema`) to pick the right one when several accounts exist. `--category source` lists exactly the RETL-source warehouse accounts that are valid for a Data Graph; drop the filter or use `--type snowflake|databricks|...` to widen.

**Why the CLI and not the MCP:** `rudder-mcp` can only locate accounts reachable through a **RETL source or a destination**. Accounts created through the **Data Graph UI** or a standalone **warehouse connection** are invisible to the MCP — but they *do* appear in `rudder-cli workspace accounts list`. When the MCP cannot surface the account, fall back to the CLI (or accept an `account_id` the user states explicitly).

### Building from scratch — no RETL source yet

Common for demo-environment builds (e.g. provisioning a workspace end-to-end before any audience or RETL source exists). There is no RETL source config to read the id from, and the obvious "create a dummy RETL source just to expose the account" step is unnecessary:

1. Ensure the warehouse account exists (created via the dashboard, Terraform, or the Data Graph UI).
2. `rudder-cli workspace accounts list --category source --json` → take the matching `id`.
3. Put that id in `spec.account_id` and proceed to validate / apply.

> **Note:** creating a warehouse *destination* alone does not always surface a usable account id through every path. The reliable path in all cases is the CLI account list above.

---

## Step 5 — Compile the demo warehouse spec

For every model or table referenced in the Data Graph, produce:

- Full table or model name (`schema.table` or model identifier).
- Key columns with short descriptions.
- Known types where you can verify them.
- Join keys to other tables.
- Row-count estimate (or a mock-data guidance note).
- Explicit assumptions for anything inferred.

Schema guidance by RETL source type:

- **Table sources** → use `config.schema` + `config.table` + warehouse schema lookup when available.
- **Model sources** → parse rendered `config.sql` to recover projected column names / aliases and relationship hints, but **do not pretend SQL parsing gives you reliable types**. If a type cannot be verified from warehouse metadata, materialization metadata, or explicit docs, mark it as `unknown` or `inferred`.
- **Audience sources** → use `config.filterSpec.filterGroups[].filters[].fieldName` only as evidence of fields already used in segmentation, not as a substitute for full schema.

If you cannot verify a column type, say so. A clearly labeled draft spec is better than invented precision.

---

## Step 6 — Identify untapped segments

Do **not** treat every unused column as an opportunity. The goal is to find realistic segmentation levers, not to diff audience filters against raw schema mechanically.

For each anchor entity, compile candidate segment dimensions from:

- Existing audience `filterSpec` fields.
- Verified business columns on the underlying entity/model.
- Related entities included in the draft graph.
- Event models and their business timestamps.

Prioritize columns that are typically segmentable:

- lifecycle stage
- plan / tier
- status
- region / market / branch / owner
- product category
- monetary bands or usage bands
- tenure or recency derived from real business timestamps

Usually exclude or de-prioritize:

- raw ids / foreign keys by themselves
- ingestion metadata (`loaded_at`, `_etl_*`, `snapshot_date`)
- high-cardinality free text
- opaque JSON blobs
- sensitive fields unless the customer already uses them intentionally

Output each untapped segment as an idea with a short rationale, for example:
- "Contacts by role" because `role` exists on `dim_contact` and no current audience references it.
- "Branches with no leads in the last 30 days" because `lead_sent_at` exists on a related event model and current audiences are single-table only.

*Why this matters:* this is the strongest upgrade narrative when grounded in the customer's own data model, but it only works if the suggestions are credible.

---

## Step 7 — Frame the upgrade conversation

Pair the deliverables above with a capability-gap narrative: what the customer can do today on RETL Audiences vs. what opens up with Data Graph. For the comparison table and talking points for each row, read `references/capability-comparison.md`.

Ground the framing in:

- the **untapped segments** from Step 6
- the **multi-entity joins** they currently cannot express cleanly
- the **event and time-window filters** already latent in their data

Specifics beat abstract feature lists. Name the first two or three audiences the customer could build immediately after migration.

---

## Validation & handoff

Before handing the YAML to the customer:

1. **Validate** — run the YAML through `rudder-cli` or import it into the visual builder preview.
2. **If you cannot validate, label the output clearly as an unvalidated draft.** Do not call it ready-to-use unless a validation step actually happened.
3. **Confirm every join key with the customer.** Inferred joins are guesses. A wrong join key produces audiences that silently return the wrong population.
4. **Flag assumptions explicitly.** Any inferred cardinality, guessed account id, unresolved type, or event-timestamp assumption should be called out in the handoff note.

---

## Common gotchas

- **`includeConfig=false` is not enough** for audience extraction, SQL parsing, or `accountId` resolution. Always fetch full config for shortlisted sources.
- **Warehouse account IDs** come from `rudder-cli workspace accounts list --category source --json` (the `id` field). Don't require a RETL source to exist first, and don't rely on the MCP — it can't see DG-UI or warehouse-connection accounts. See Step 4a.
- **Templated model SQL** must be rendered before column extraction.
- **SQL parsing recovers names, not guaranteed types.** Mark unverifiable types as unknown / inferred.
- **Soft-deleted rows** are included unless filtered at the model layer.
- **Multi-tenant schemas** need the tenant column surfaced so Audiences can scope correctly.
- **Device-mode destinations** bypass RudderStack servers; they will not explain warehouse-side RETL source shape.
- **Date/time dimensions are not graph nodes.** Do not model `DIM_DATES` / `DIM_TIME` or join them at audience time. An event model's `timestamp` column already encodes the moment, and time-window filters operate on it directly.

---

## Reference files

- `references/data-graph-yaml-template.md` — full annotated YAML + worked example + troubleshooting.
- `references/industry-patterns.md` — Property, E-commerce, SaaS starting shapes with segment examples.
- `references/capability-comparison.md` — RETL Audiences vs. Data Graph table with talking points.

## External docs

- Audiences Overview: https://www.rudderstack.com/docs/audiences/overview/
- Data Graph: https://www.rudderstack.com/docs/audiences/data-graph/
- Data Graph YAML reference: https://www.rudderstack.com/docs/audiences/data-graph/cli-reference/
- Visual builder: https://www.rudderstack.com/docs/audiences/data-graph/create-data-graph/
- RETL Audiences (existing): https://www.rudderstack.com/docs/data-pipelines/reverse-etl/features/audiences/
