---
name: naming-tagging-standards
description: Enforces enterprise naming conventions (snake_case, table prefixes, approved abbreviations), dual-purpose COMMENT formats for tables/columns/TVFs/metric views/dashboards/Genie Spaces, and config-aware tagging standards. Scans context/ for customer tagging standards in any format (YAML, CSV, Markdown, JSON, TXT); derives meaningful smart defaults when none supplied. Uses Databricks Data Classification class.* system governed tags for PII (always inferred from column names + customer declarations). Ensures tag consistency across all project assets. Triggers on "naming", "comment", "COMMENT", "schema COMMENT", "tag", "PII", "cost_center", "snake_case", "dim_", "fact_", "governed tag", "budget policy", "class.*", "data classification", "dashboard", "metric view", "Genie Space".
metadata:
  author: prashanth subrahmanyam
  version: "3.1"
  domain: common
  role: shared
  used_by_stages: [1, 2, 3, 4, 5, 6, 7, 8, 9]
  clients: [ide_cli, genie_code]   # naming/tagging is client-agnostic intent; deploy via databricks-asset-bundles (the spine)
  deploy_verb: "bundle deploy --target dev"
  deploy_note: "naming/COMMENT/tag standards — authored as intent; applied via deploy-time bundle resources (RULE_10)"
  coverage: all_stages
  called_by:
    - gold/00-gold-layer-design
    - bronze/00-bronze-layer-setup
    - silver/00-silver-layer-setup
    - gold/01-gold-layer-setup
    - planning/00-project-planning
    - semantic-layer/00-semantic-layer-setup
    - monitoring/00-observability-setup
    - ml/00-ml-pipeline-setup
    - genai-agents/00-course-orchestrator
  last_verified: "2026-06-02"   # M2 closeout re-verify: capability block compliant, no SKILL.md-body flags
  volatility: low
  upstream_sources: []  # Internal naming convention
---

# Naming, Comment & Tagging Standards

Enterprise-wide standards for Databricks asset naming, SQL comments, and cost/governance tagging.

## Essential Rules (Retain in Working Memory)

After reading this skill, retain these 5 rules and release the full content:

1. **snake_case everywhere** — all object names: tables, columns, functions, schemas
2. **`dim_`/`fact_` prefixes** — Gold tables prefixed by entity type; Bronze/Silver by layer
3. **Dual-purpose COMMENT pattern** — `[Definition]. Business: [context]. Technical: [details].`
4. **Mandatory tags** — `layer`, `domain`, `PII` (via `class.*` governed tags) on every table; `team`, `cost_center`, `environment` on every workflow
5. **Budget policy tag** — all serverless resources must use approved budget policies

## Naming Quick Test (5-Point Gate)

Before generating ANY DDL, YAML, or Asset Bundle resource, verify all 5:

1. **Layer prefix?** — `bronze_`, `silver_`, `dim_`, `fact_`, `bridge_`, `agg_`
2. **snake_case?** — No camelCase, PascalCase, SCREAMING_CASE, kebab-case, or spaces
3. **Schema COMMENT?** — Every schema has a COMMENT via `COMMENT ON SCHEMA`
4. **Table/column COMMENTs?** — Dual-purpose format on every table and column
5. **PII governed tags?** — Scanned column names for `class.*` tag candidates

**If ANY answer is NO, stop and fix before proceeding.**

## Golden Rules

| ID | Rule | Severity |
|----|------|----------|
| **NC-01** | All object names use `snake_case` | Critical |
| **NC-02** | Tables prefixed by layer (`bronze_`, `silver_`) or entity type (`dim_`, `fact_`) | Critical |
| **NC-03** | No abbreviations except approved list | Required |
| **CM-01** | SQL block comments (`/* */`) for all DDL operations | Required |
| **CM-02** | Table COMMENT follows dual-purpose format | Critical |
| **CM-03** | Column COMMENT required for all columns | Critical |
| **CM-04** | TVF COMMENT follows v3.0 structured format | Critical |
| **TG-00** | Scan `context/` for customer tagging standards (any format); derive smart defaults if absent | Critical |
| **TG-01** | All workflows must have required tags (`team`, `cost_center`, `environment`) | Critical |
| **TG-02** | Use Databricks Data Classification `class.*` governed tags for PII columns | Critical |
| **TG-03** | Use UC governed tags for catalogs, schemas, and tables | Critical |
| **TG-04** | Serverless resources must use approved budget policies | Critical |

---

## Tagging Configuration Resolution

**Before applying ANY tags, the agent MUST follow this resolution order:**

### Step 1: Scan `context/` for Customer-Supplied Tagging Standards

Search the `context/` directory for **any** file containing tagging standards. The customer supplies their standards in **whatever format they already have** — the agent adapts to them, not the other way around.

| Format | Detection Pattern | How to Parse |
|--------|-------------------|--------------|
| **YAML/JSON** | `*tag*`, `*tagging*`, `*governance*`, `*standards*` | Parse key-value structure directly |
| **CSV** | Files with columns like `tag_name`, `tag_value`, `scope`, `object_type` | Parse rows as tag definitions |
| **Markdown** | Files with tagging tables or bullet lists | Extract tag names and values from tables/lists |
| **Plain text** | `*tag*`, `*tagging*` with `.txt` | Parse `key: value` or `key = value` lines |
| **Free-form** | Any file mentioning tags, cost center, PII, classification | Extract intent — the agent understands natural language |

**Parsing rules:**
- Look for recognizable tag keys: `team`, `cost_center`, `business_unit`, `data_owner`, `data_classification`, `project`, `pii`, `class.*`, or any custom keys
- Normalize all keys to `snake_case`
- Accept any reasonable structure — the agent interprets **intent**, not rigid schema
- If multiple files match, merge them (later file wins on conflicts)

### Step 1b: Normalize to Canonical Internal Schema

After parsing the customer file, the agent normalizes **all** extracted values into the canonical schema defined in [references/canonical-tagging-schema.yaml](references/canonical-tagging-schema.yaml). This schema is never shown to the user — it is the agent's internal working format.

**Normalization examples (any input → canonical schema):**

| Customer Input (any format) | Canonical Field |
|---|---|
| `team = platform-engineering` | `workflow_tags.team` |
| CSV row: `workflow,all,cost_center,CC-9901` | `workflow_tags.cost_center` AND `governed_tags.catalog.cost_center` |
| MD bullet: `- dim_guest.email → class.email_address` | `pii_columns.dim_guest[0].class_tag` |
| Prose: "Our data owner is data-platform@acme.com" | `governed_tags.schema.data_owner` |
| Table: `| data_classification | confidential | dim_guest |` | `governed_tags.table_overrides.dim_guest.data_classification` |

The agent fills any fields not provided by the customer using smart defaults (Step 2 below).

### Step 2: Derive Smart Defaults (No Customer Config Found, or Gaps in Config)

If **no** tagging file is found in `context/`, OR the customer file has **gaps** (e.g., they specify `team` and `cost_center` but not `data_owner`), the agent fills missing fields with **meaningful** values derived from project context:

| Tag | Derivation Strategy | Example (Wanderbricks) |
|-----|--------------------|------------------------|
| `team` | `"data-engineering"` (universal default — most common team name) | `data-engineering` |
| `cost_center` | **Cannot infer** — use `"REVIEW-REQUIRED"` + `# TODO` comment | `REVIEW-REQUIRED` |
| `environment` | Always `${bundle.target}` (non-negotiable) | `dev`, `staging`, `prod` |
| `project` | Extract from schema CSV schema name, catalog name, or repo folder | `wanderbricks` |
| `business_unit` | Infer domain from schema/table names (e.g., hospitality, retail, sales) | `hospitality` |
| `data_owner` | `"{project}-data-team"` pattern | `wanderbricks-data-team` |
| `data_classification` | `"internal"` (safe default for all tables) | `internal` |
| **PII columns** | **Infer from column names** using pattern matching (see PII Inference below) | `class.email_address` |

**Key difference from v1:** Only `cost_center` gets a placeholder — all other tags get real derived values.

### Step 3: PII Column Inference (Always Active)

Whether or not customer config is supplied, the agent **always** scans column names from the schema CSV (or YAML designs) and applies [Databricks Data Classification](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/data-classification#supported-classification-tags) `class.*` system governed tags using column name pattern matching:

| Column Name Pattern | Databricks Classification Tag | Examples |
|--------------------|-----------------------------|----------|
| `*email*` | `class.email_address` | `email`, `customer_email`, `contact_email` |
| `*phone*`, `*mobile*`, `*cell*` | `class.phone_number` | `phone_number`, `mobile_phone`, `work_phone` |
| `*_name` (person context: `first_name`, `last_name`, `guest_name`, `host_name`, `customer_name`) | `class.name` | `first_name`, `last_name`, `guest_name` |
| `*address*`, `*street*` (physical, not email) | `class.location` | `street_address`, `mailing_address` |
| `*ssn*`, `*social_security*`, `*tax_id*` | `class.us_ssn` | `ssn`, `social_security_number` |
| `*passport*` | `class.us_passport` | `passport_number` |
| `*driver_license*`, `*license_number*` | `class.us_driver_license` | `driver_license_number` |
| `*credit_card*`, `*card_number*`, `*cc_number*` | `class.credit_card` | `credit_card_number` |
| `*ip_address*`, `*ip_addr*` | `class.ip_address` | `client_ip_address` |
| `*iban*` | `class.iban_code` | `iban_code`, `bank_iban` |

**Rules for PII inference:**
- **Always apply** inferred PII tags regardless of whether customer config exists
- If customer config **explicitly declares** PII columns, those take **precedence** over inference (customer may override or suppress)
- Use `class.*` system governed tags (not custom `pii`/`pii_type` tags) for compatibility with Databricks Data Classification
- Customer can suppress a false positive by adding `exclude_pii: [column_name]` in their config
- Also **recommend enabling Databricks Data Classification** on the catalog for automated AI-powered scanning beyond column name patterns

### Step 4: Environment Tag (Always Automatic)

The `environment` tag is **always** `${bundle.target}` — never hardcoded. This is non-negotiable regardless of config.

### Step 4b: Job / Pipeline Name Prefix (Non-Negotiable)

Every job and pipeline `name:` field **MUST** begin with the user-prefixed token
`[${bundle.target} ${var.user_prefix}]` — this is the single canonical prefix
across all layers (Bronze, Silver, Gold, ML, semantic, monitoring). Rules:

- The bundle **MUST** declare the `user_prefix` variable (default
  `${workspace.current_user.short_name}`), so dev renders `[dev jsmith] …`.
- Do **NOT** rely on `mode: development` auto-prefixing; set
  `presets.name_prefix: ""` on the dev target so the explicit token is the sole
  authority (prevents `[dev jsmith] [dev jsmith] …` doubling).
- Prod keeps names clean by setting `user_prefix: ""` in the prod target.
- The project/domain token stays in the name after the prefix (e.g.
  `[dev jsmith] Wanderbricks Bronze Layer - Clone`).

Authoritative definition: `skills/databricks-asset-bundles/SKILL.md` →
"Shared Workspace Naming".

### Step 5: Consistency Enforcement

All tags must be **consistent** across all assets in the project:

| Rule | Enforcement |
|------|-------------|
| Same `team` on every job, pipeline, and dashboard | Agent verifies before generating |
| Same `cost_center` on workflows AND catalog governed tags | Must match |
| Same `project` across all Asset Bundle resources | Derived once, used everywhere |
| `data_classification` must be set on **every** Gold table | Default `"internal"` if not specified |
| PII `class.*` tags must be consistent across all layers | Same column tagged in Bronze, Silver, and Gold |

### Internal Reference

The canonical schema the agent normalizes to is defined in [references/canonical-tagging-schema.yaml](references/canonical-tagging-schema.yaml). This file is an **agent-internal reference** — the user never sees or fills it in. The user simply drops their tagging standards into `context/` in whatever format they prefer.

---

## Part 1: Naming Conventions

### Object Naming Patterns

| Object | Format | Example |
|--------|--------|---------|
| Catalog | `{env}_{domain}_catalog` | `prod_sales_catalog` |
| Schema | `{layer}` or `{domain}_{layer}` | `bronze`, `sales_gold` |
| Table | `{prefix}_{entity}` | `dim_customer`, `fact_orders` |
| Column | `{descriptive_name}` | `customer_id`, `order_date` |
| Constraint | `{type}_{table}[_{column}]` | `pk_dim_customer`, `fk_orders_customer` |
| Function | `get_{entity}_{action}` | `get_daily_sales` |
| Job | `[${bundle.target} ${var.user_prefix}] {Domain} - {Action} {Entity}` | `[dev jsmith] Sales - Merge Orders` |
| Pipeline | `[${bundle.target} ${var.user_prefix}] {Layer} {Domain} Pipeline` | `[dev jsmith] Silver Sales Pipeline` |
| Dashboard | `{Domain} - {Report Type}` | `Sales - Revenue Overview` |
| Metric View | `mv_{domain}_{entity}` | `mv_billing_cost_summary` |
| Genie Space | `{Domain} {Description} Space` | `Hospitality Booking Analytics Space` |

**Never use:** `camelCase`, `PascalCase`, `SCREAMING_CASE`, `kebab-case`, or spaces.

### Table Prefixes

| Layer/Type | Prefix | Example |
|------------|--------|---------|
| Bronze | `bronze_` | `bronze_raw_orders` |
| Silver | `silver_` | `silver_orders` |
| Gold Dimension | `dim_` | `dim_customer` |
| Gold Fact | `fact_` | `fact_sales` |
| Bridge | `bridge_` | `bridge_customer_product` |
| Aggregate | `agg_` | `agg_daily_sales` |
| Staging | `stg_` | `stg_customer_updates` |
| Quarantine | `_quarantine` suffix | `silver_orders_quarantine` |
| History | `_history` suffix | `dim_customer_history` |

### Approved Abbreviations (Use ONLY These)

`id`, `ts`, `dt`, `amt`, `qty`, `pct`, `num`, `cnt`, `avg`, `min`, `max`, `pk`, `fk`, `dim`, `fact`, `agg`, `stg`

**Forbidden:** `cust`, `prod`, `inv`, `trans`, `ord`, `emp` -- spell these out.

### Column Patterns

| Pattern | Format | Example |
|---------|--------|---------|
| Primary Key | `{entity}_id` or `{entity}_key` | `customer_id`, `store_key` |
| Foreign Key | Same as referenced PK | `customer_id` |
| Business Key | `{entity}_{identifier}` | `customer_number` |
| Surrogate Key | `{entity}_key` | `customer_key` (MD5) |
| Date | `{event}_date` | `order_date` |
| Timestamp | `{event}_timestamp` or `{event}_ts` | `created_ts` |
| Boolean | `is_{condition}` or `has_{thing}` | `is_active`, `has_discount` |
| Amount | `{type}_amount` or `{type}_amt` | `total_amount` |
| Count | `{thing}_count` or `{thing}_cnt` | `order_count` |
| SCD2 | `effective_from`, `effective_to`, `is_current` | Standard names |

For detailed naming examples, see [references/naming-conventions.md](references/naming-conventions.md).

---

## Part 2: Comment Conventions

### CM-01: SQL Block Comments

All DDL must include `/* */` block comments with purpose, grain, and source:

```sql
/*
 * Table: dim_customer
 * Layer: Gold | Domain: Sales
 * Grain: One row per customer per effective period.
 * Source: Silver layer silver_customers table.
 */
```

### CM-02: Table COMMENT (Dual-Purpose Format)

```
[One-line description]. Business: [use cases, consumers]. Technical: [grain, source, update frequency].
```

> **Note:** Square brackets `[]` above are placeholders — replace with actual content. Do not include literal brackets in the output.

Examples:

```sql
-- Gold Dimension
COMMENT ON TABLE gold.dim_customer IS
'Customer dimension with SCD Type 2 history tracking. Business: Primary customer reference for segmentation and cohort analysis. Technical: MD5 surrogate key, is_current flag, daily merge from Silver.';

-- Gold Fact
COMMENT ON TABLE gold.fact_orders IS
'Daily order facts at customer-product-day grain. Business: Primary source for revenue reporting and sales dashboards. Technical: Composite PK, incremental merge, CDF enabled.';
```

### CM-03: Column COMMENT (Dual-Purpose Format)

```
[Brief definition]. Business: [how it's used]. Technical: [data type notes, source, calculation].
```

```sql
customer_key STRING NOT NULL
COMMENT 'Surrogate key for SCD Type 2 versioning. Business: Used for joining fact tables. Technical: MD5 hash of customer_id + effective_from.';

total_amount DECIMAL(18,2)
COMMENT 'Total order amount after discounts in USD. Business: Primary revenue metric. Technical: SUM(quantity * unit_price * (1 - discount_pct)).';
```

### CM-04: TVF COMMENT (v3.0 Structured Format)

```sql
COMMENT '
• PURPOSE: [One-line description of what the function returns].
• BEST FOR: [Query type 1] | [Query type 2] | [Query type 3]
• NOT FOR: [What to use instead] (use [alternative] instead)
• RETURNS: [PRE-AGGREGATED or DETAIL rows]
• PARAMS: [param1 (format)], [param2 (format)]
• SYNTAX: SELECT * FROM function_name(''param1'', ''param2'')
• NOTE: [Critical usage notes]
'
```

### Metric View COMMENT Format (YAML)

```yaml
comment: >
  PURPOSE: Cost analytics for billing analysis.
  BEST FOR: Total spend by workspace | Cost by SKU | Daily trends
  NOT FOR: Commit tracking (use commit_tracking) | Real-time alerts (use TVF)
  DIMENSIONS: usage_date, workspace_name, sku_name
  MEASURES: total_cost, total_dbus, tag_coverage_pct
  SOURCE: fact_usage (billing domain)
  JOINS: dim_workspace, dim_sku
  NOTE: Costs are list prices. Actual billed amounts may differ.
```

For complete comment examples, see [references/comment-templates.md](references/comment-templates.md).

---

## Part 3: Tagging Standards

> **Config-aware:** Tag values come from customer-supplied config (any format) when available. When absent, the agent derives meaningful defaults from project context. See [Tagging Configuration Resolution](#tagging-configuration-resolution) above.

### TG-01: Workflow Tags (Asset Bundles)

All jobs and pipelines **must** include:

| Tag | Required | With Customer Config | Without Config (Smart Default) |
|-----|----------|---------------------|-------------------------------|
| `team` | Yes | From customer file | `"data-engineering"` |
| `cost_center` | Yes | From customer file | `"REVIEW-REQUIRED"` + `# TODO` |
| `environment` | Yes | Always `${bundle.target}` | Always `${bundle.target}` |
| `project` | Recommended | From customer file | Inferred from schema/catalog/repo name |
| `layer` | Recommended | Auto-derived | Auto-derived from pipeline layer |
| `job_type` | Recommended | Auto-derived | Auto-derived from job purpose |

**With customer config (values sourced from customer file in `context/`):**

```yaml
resources:
  jobs:
    gold_merge_job:
      tags:
        team: platform-engineering         # From customer tagging standards
        cost_center: CC-9901               # From customer tagging standards
        environment: ${bundle.target}      # Always automatic
        project: wanderbricks              # From customer tagging standards
        layer: gold                        # Auto-derived
        job_type: merge                    # Auto-derived
```

**Without customer config (meaningful defaults):**

```yaml
resources:
  jobs:
    gold_merge_job:
      tags:
        team: data-engineering             # Default — add tagging config to context/ to customize
        cost_center: REVIEW-REQUIRED       # TODO: Add tagging config to context/ with cost_center
        environment: ${bundle.target}      # Always automatic
        project: wanderbricks              # Inferred from schema CSV (samples.wanderbricks)
        layer: gold                        # Auto-derived
        job_type: merge                    # Auto-derived
```

### TG-02: Databricks Data Classification Tags (PII Columns)

Use [Databricks Data Classification](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/data-classification#supported-classification-tags) `class.*` **system governed tags** for PII — not custom `pii`/`pii_type` tags.

**Supported `class.*` tags (global):**

| Tag | Description | Column Pattern Match |
|-----|-------------|---------------------|
| `class.email_address` | Email addresses | `*email*` |
| `class.phone_number` | Phone numbers | `*phone*`, `*mobile*`, `*cell*` |
| `class.name` | Person names | `first_name`, `last_name`, `*_name` (person context) |
| `class.location` | Physical locations | `*address*`, `*street*` (not email) |
| `class.credit_card` | Credit card numbers | `*credit_card*`, `*card_number*` |
| `class.us_ssn` | US Social Security | `*ssn*`, `*social_security*` |
| `class.us_passport` | US Passport | `*passport*` |
| `class.us_driver_license` | US Driver License | `*driver_license*` |
| `class.ip_address` | IP addresses | `*ip_address*`, `*ip_addr*` |
| `class.iban_code` | Bank account (IBAN) | `*iban*` |
| `class.url` | URLs | `*_url`, `*website*` |

**PII tags are always inferred** from column names AND from customer config (if supplied). Customer config takes precedence — they can add, override, or suppress inferred tags.

```sql
-- Applied to columns based on name pattern inference + customer config
ALTER TABLE gold.dim_guest ALTER COLUMN email SET TAGS ('class.email_address' = '');
ALTER TABLE gold.dim_guest ALTER COLUMN phone_number SET TAGS ('class.phone_number' = '');
ALTER TABLE gold.dim_guest ALTER COLUMN guest_name SET TAGS ('class.name' = '');

-- Also recommend enabling automated Data Classification on the catalog:
-- Navigate to catalog > Details > Data Classification toggle > Enable
```

### TG-03: Unity Catalog Governed Tags (Catalogs, Schemas, Tables)

| Tag | Apply To | With Customer Config | Without Config (Smart Default) |
|-----|----------|---------------------|-------------------------------|
| `cost_center` | Catalogs | From customer file | `"REVIEW-REQUIRED"` + `# TODO` |
| `business_unit` | Catalogs | From customer file | Inferred from domain (e.g., `"hospitality"`) |
| `data_owner` | Schemas | From customer file | `"{project}-data-team"` pattern |
| `data_classification` | Tables | From customer file | `"internal"` (safe default for all tables) |

**With customer config:**

```sql
ALTER CATALOG wanderbricks SET TAGS ('cost_center' = 'CC-9901', 'business_unit' = 'Hospitality');
ALTER SCHEMA wanderbricks.gold SET TAGS ('data_owner' = 'data-platform@wanderbricks.com');
ALTER TABLE gold.dim_guest SET TAGS ('data_classification' = 'confidential');
ALTER TABLE gold.fact_bookings SET TAGS ('data_classification' = 'internal');
```

**Without customer config (meaningful defaults):**

```sql
ALTER CATALOG wanderbricks SET TAGS ('cost_center' = 'REVIEW-REQUIRED');  -- TODO: Add tagging config to context/
ALTER CATALOG wanderbricks SET TAGS ('business_unit' = 'hospitality');     -- Inferred from domain
ALTER SCHEMA wanderbricks.gold SET TAGS ('data_owner' = 'wanderbricks-data-team');  -- Derived from project
ALTER TABLE gold.dim_guest SET TAGS ('data_classification' = 'internal');  -- Safe default
```

### TG-04: Serverless Budget Policies

Serverless compute resources require budget policies with `team`, `cost_center`, and `environment` tags. If a named policy is specified in the customer config, reference it in Asset Bundles.

For tag query patterns and serverless cost attribution, see [references/tagging-patterns.md](references/tagging-patterns.md).

---

## Validation Checklist

### Tagging Config Resolution
- [ ] Scanned `context/` for customer tagging files in any format (YAML, CSV, MD, JSON, TXT)
- [ ] If config found: parsed and applied customer values (all tag keys normalized to `snake_case`)
- [ ] If config absent: derived meaningful defaults from project context (not lazy placeholders)
- [ ] Only `cost_center` uses `REVIEW-REQUIRED` placeholder (everything else gets a real derived value)
- [ ] `environment` tag is `${bundle.target}` (never hardcoded)

### PII / Data Classification
- [ ] Column names scanned for PII patterns and `class.*` system governed tags applied
- [ ] Used `class.*` tags (NOT custom `pii`/`pii_type` tags)
- [ ] Customer PII declarations (if any) take precedence over inference
- [ ] Recommended enabling Databricks Data Classification on the catalog

### Naming
- [ ] All objects use `snake_case`
- [ ] Tables have correct prefix (`dim_`, `fact_`, `bronze_`, `silver_`)
- [ ] Only approved abbreviations used
- [ ] Columns follow standard patterns (PK, FK, boolean, SCD2)
- [ ] Jobs/pipelines follow naming format
- [ ] Every job/pipeline `name:` starts with `[${bundle.target} ${var.user_prefix}]` and the bundle declares the `user_prefix` variable (dev renders `[dev <short_name>] …`)

### Comments
- [ ] DDL includes `/* */` block comments
- [ ] All tables have dual-purpose COMMENT
- [ ] All columns have dual-purpose COMMENT
- [ ] TVFs have v3.0 structured COMMENT
- [ ] Metric views have structured comment in YAML

### Tags
- [ ] All jobs have `team`, `cost_center`, `environment` tags
- [ ] All pipelines have required tags
- [ ] Catalogs tagged with `cost_center` and `business_unit`
- [ ] Schemas tagged with `data_owner`
- [ ] Confidential tables tagged with `data_classification`
- [ ] PII columns tagged with `class.*` governed tags (inferred + customer-declared)
- [ ] Tag values consistent across all project assets (same team, cost_center, project everywhere)

---

## Additional Resources

- For detailed naming conventions and forbidden patterns, see [references/naming-conventions.md](references/naming-conventions.md)
- For complete comment templates with examples, see [references/comment-templates.md](references/comment-templates.md)
- For tagging patterns and cost query SQL, see [references/tagging-patterns.md](references/tagging-patterns.md)
