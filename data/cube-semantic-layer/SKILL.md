---
name: cube-semantic-layer
description: ALWAYS USE when building semantic layer, working with metrics/dimensions, or integrating dbt with Cube consumption APIs. Use IMMEDIATELY when working with Cube REST API, GraphQL queries, or Postgres wire protocol (psycopg2 connections). Provides research steps for data modeling, dbt integration, MEASURE() syntax, and API validation.
---

# Cube Semantic Layer Development (Research-Driven)

## Philosophy

This skill does NOT prescribe specific semantic models or API patterns. Instead, it guides you to:
1. **Research** the current Cube version and capabilities
2. **Discover** existing Cube data models and dbt integrations
3. **Validate** your implementations against Cube documentation
4. **Verify** integration with dbt models and consumption applications

## Pre-Implementation Research Protocol

### Step 1: Verify Runtime Environment

**ALWAYS run this first**:
```bash
# Check if Cube is installed
cube --version 2>/dev/null || echo "Cube CLI not found"

# Check if running locally
curl -s http://localhost:4000/readyz || echo "Cube API not reachable"
```

**Critical Questions to Answer**:
- Is Cube running locally or remotely?
- What version is available?
- What database connection is configured?
- Is dbt integration enabled?

### Step 2: Research SDK State (if unfamiliar)

**When to research**: If you encounter unfamiliar Cube features or need to validate patterns

**Research queries** (use WebSearch):
- "Cube [feature] documentation 2025" (e.g., "Cube dbt integration 2025")
- "Cube REST API query format 2025"
- "Cube data modeling metrics dimensions 2025"

**Official documentation**: https://cube.dev/docs

**Key documentation sections**:
- Data Modeling: https://cube.dev/docs/product/data-modeling
- dbt Integration: https://cube.dev/docs/product/data-modeling/recipes/dbt
- REST API: https://cube.dev/docs/product/apis-integrations/rest-api
- cube_dbt package: https://cube.dev/docs/product/data-modeling/reference/cube_dbt

### Step 3: Discover Existing Patterns

**BEFORE creating new Cube models**, search for existing implementations:

```bash
# Find Cube model files
find . -name "*.yml" -path "*/model/*" -o -name "*.yaml" -path "*/model/*"
find . -name "*.js" -path "*/model/*"

# Find dbt integration usage
rg "cube_dbt|from_dbt" --type yaml --type py

# Find REST API usage
rg "cube.*api|/cubejs-api" --type py --type js
```

**Key questions**:
- What Cube models (cubes) already exist?
- Is dbt integration configured? (`cube_dbt` package usage)
- What metrics and dimensions are defined?
- What API endpoints are exposed?

### Step 4: Validate Against Architecture

Check architecture docs for integration requirements:
- Read `/docs/` for consumption layer requirements
- Understand dbt model → Cube cube mapping
- Verify API requirements for downstream applications
- Check governance metadata propagation

## Implementation Guidance (Not Prescriptive)

### Cube Data Model Concepts

**Core concepts**: Cubes, measures, dimensions, joins, pre-aggregations

**Entity hierarchy**:
```
Cube Project
├── Cubes (semantic models on top of tables/views)
│   ├── Measures (metrics: SUM, COUNT, AVG, etc.)
│   ├── Dimensions (attributes for grouping/filtering)
│   ├── Joins (relationships between cubes)
│   └── Pre-aggregations (materialized rollups)
└── Views (organize cubes for consumers)
```

**Research questions**:
- What cubes should be created? (one per dbt model? logical grouping?)
- What measures are needed? (KPIs, aggregations)
- What dimensions? (time, categorical, hierarchical)
- What joins between cubes?

### dbt Integration (`cube_dbt` package)

**Core concept**: Generate Cube models from dbt manifest.json

**Research questions**:
- Should Cube models be generated from dbt? (vs hand-written)
- Where is dbt manifest.json located?
- What dbt models should be exposed in Cube?
- How should dbt model metadata be enriched in Cube?

**SDK features to research**:
- `cube_dbt` package: dbt integration utilities
- `cube_dbt.load_dbt_project()`: Load dbt metadata
- `cube_dbt.dbt_model_to_cube()`: Convert dbt model to Cube cube
- manifest.json parsing: Extract dbt model metadata
- dbt meta tags: Propagate to Cube dimensions/measures

### Cubes (Semantic Models)

**Core concept**: Cubes define the semantic layer on top of physical tables

**Research questions**:
- What is the SQL definition? (table, view, subquery)
- What measures should be exposed?
- What dimensions?
- What joins to other cubes?
- What pre-aggregations for performance?

**SDK features to research**:
- Cube definition: YAML or JavaScript
- `sql` property: Define data source (table, view, SQL)
- Measures: `type` (sum, count, avg, min, max, count_distinct, etc.)
- Dimensions: `type` (string, number, time, boolean, geo)
- Joins: `relationship` (one_to_one, one_to_many, many_to_one)
- Pre-aggregations: Materialized rollups for performance

### Measures (Metrics)

**Core concept**: Measures are aggregatable metrics

**Research questions**:
- What KPIs need to be calculated?
- What aggregation type? (sum, count, average, distinct count)
- Are there calculated measures? (ratios, percentages)
- What filters apply to measures?

**SDK features to research**:
- Measure types: `sum`, `count`, `avg`, `min`, `max`, `count_distinct`, `number`
- Calculated measures: `sql` property with expressions
- Filters: `filters` property on measures
- Rollup measures: Aggregating pre-aggregations

### Dimensions (Attributes)

**Core concept**: Dimensions are attributes for grouping and filtering

**Research questions**:
- What categorical dimensions? (status, category, region)
- What time dimensions? (date, timestamp, granularity)
- What hierarchical dimensions? (geography, org structure)
- Should dimensions be hidden or exposed?

**SDK features to research**:
- Dimension types: `string`, `number`, `time`, `boolean`, `geo`
- Time dimensions: `granularities` (day, week, month, year)
- Subquery dimensions: Complex SQL expressions
- Case expressions: Conditional logic in dimensions

### Joins (Relationships)

**Core concept**: Joins define relationships between cubes

**Research questions**:
- What relationships exist? (user → orders, product → sales)
- What join type? (one-to-one, one-to-many, many-to-one)
- What join SQL?
- Are joins bidirectional?

**SDK features to research**:
- Join definition: `relationship`, `sql` property
- Join types: `one_to_one`, `one_to_many`, `many_to_one`
- Join SQL: Foreign key relationships
- Many-to-many: Through tables

### Pre-aggregations (Performance)

**Core concept**: Pre-aggregations are materialized rollups for query performance

**Research questions**:
- What queries are slow?
- What aggregations are common? (daily rollups, by category)
- What materialization schedule?
- What storage for pre-aggregations?

**SDK features to research**:
- Pre-aggregation definition: Specify measures, dimensions, granularity
- Refresh strategies: `every`, `update_window`
- Partitioning: Time-based partitions
- External storage: Store in data warehouse

### REST API (Consumption)

**Core concept**: Cube exposes REST API for data queries

**Research questions**:
- What API endpoints are needed?
- What authentication?
- What query patterns? (measures + dimensions, filters, time ranges)
- How should API be consumed? (Python, JavaScript, BI tools)

**SDK features to research**:
- Query format: JSON with `measures`, `dimensions`, `filters`, `timeDimensions`
- Authentication: JWT tokens, API keys
- Response format: `data` (result set) + `schema` (column metadata)
- Pagination: `limit`, `offset`

### GraphQL API (Consumption)

**Core concept**: Cube exposes GraphQL API for flexible querying

**Research questions**:
- What queries are supported?
- What mutations? (none - read-only)
- What authentication?
- How to query multiple cubes?

**SDK features to research**:
- Endpoint: `/cubejs-api/graphql` (NOT `/graphql`)
- Query format: `cube` query with `measures`, `dimensions`, `filters`
- Authentication: Same as REST API (JWT, API keys)
- Introspection: Schema discovery via `__schema` query

**Example GraphQL query**:
```graphql
query {
  cube(
    measures: ["Orders.count", "Orders.totalAmount"]
    dimensions: ["Orders.status"]
    filters: [{ dimension: "Orders.status", operator: "equals", values: ["completed"] }]
  ) {
    Orders {
      count
      totalAmount
      status
    }
  }
}
```

### SQL API (Postgres Wire Protocol)

**Core concept**: Cube exposes SQL API via Postgres wire protocol for BI tool integration

**Research questions**:
- What port is SQL API on? (default: 15432)
- What authentication? (user/password)
- What SQL dialect? (Postgres-compatible with Cube extensions)
- What BI tools are supported? (Tableau, Looker, Metabase, psycopg2)

**SDK features to research**:
- Port: `CUBEJS_PG_SQL_PORT` (default 15432)
- Authentication: `CUBEJS_SQL_USER`, `CUBEJS_SQL_PASSWORD`
- Connection: Standard Postgres clients (psycopg2, JDBC, etc.)
- Query syntax: Use `MEASURE()` function for aggregates
- Read-only: INSERT/UPDATE/DELETE not supported

**CRITICAL - Cube SQL syntax differs from standard SQL**:
```sql
-- Cube SQL API syntax (NOT standard Postgres)
SELECT
    MEASURE(count) AS order_count,
    MEASURE(total_amount) AS total
FROM Orders
WHERE status = 'completed'
GROUP BY 1

-- Dimensions referenced directly (no quotes)
SELECT status, MEASURE(count) FROM Orders GROUP BY 1

-- Time dimensions with granularity
SELECT
    DATE_TRUNC('month', created_at) AS month,
    MEASURE(count)
FROM Orders
GROUP BY 1
```

**Python psycopg2 example**:
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=15432,
    user="cube",
    password="cube_password",
    database="cube"
)
cursor = conn.cursor()
cursor.execute("SELECT MEASURE(count) FROM Orders")
results = cursor.fetchall()
```

**Docker configuration**:
```yaml
environment:
  CUBEJS_PG_SQL_PORT: "15432"
  CUBEJS_SQL_USER: ${CUBEJS_SQL_USER:-cube}
  CUBEJS_SQL_PASSWORD: ${CUBEJS_SQL_PASSWORD:-cube_password}
```

## Validation Workflow

### Before Implementation
1. ✅ Verified Cube availability (local or remote)
2. ✅ Searched for existing Cube models and dbt integration
3. ✅ Read architecture docs for consumption layer requirements
4. ✅ Identified dbt models to expose in semantic layer
5. ✅ Researched unfamiliar Cube features

### During Implementation
1. ✅ Using `cube_dbt` for dbt integration (if applicable)
2. ✅ Proper cube definitions with measures and dimensions
3. ✅ Joins correctly defined between cubes
4. ✅ Pre-aggregations for performance optimization
5. ✅ Metadata from dbt propagated to Cube
6. ✅ Governance metadata (classifications) exposed

### After Implementation
1. ✅ Verify Cube models load without errors
2. ✅ Test REST API queries (`/cubejs-api/v1/load`)
3. ✅ Test GraphQL API queries (`/cubejs-api/graphql`)
4. ✅ Test SQL API queries (port 15432, `MEASURE()` syntax)
5. ✅ Verify measures calculate correctly
6. ✅ Test dimension filtering and grouping
7. ✅ Check pre-aggregation materialization
8. ✅ Validate integration with downstream apps (BI tools, dashboards)

## Context Injection (For Future Claude Instances)

When this skill is invoked, you should:

1. **Verify runtime state** (don't assume):
   ```bash
   cube --version
   curl -s http://localhost:4000/readyz
   ```

2. **Discover existing patterns** (don't invent):
   ```bash
   find . -name "*.yml" -path "*/model/*"
   rg "cube_dbt" --type yaml
   ```

3. **Research when uncertain** (don't guess):
   - Use WebSearch for "Cube [feature] documentation 2025"
   - Check official docs: https://cube.dev/docs

4. **Validate against architecture** (don't assume requirements):
   - Read relevant architecture docs in `/docs/`
   - Understand dbt model mapping to Cube cubes
   - Check consumption API requirements

5. **Check dbt integration** (if applicable):
   - Verify dbt manifest.json location
   - Check `cube_dbt` package usage
   - Understand dbt meta tag propagation

## Quick Reference: Common Research Queries

Use these WebSearch queries when encountering specific needs:

- **dbt integration**: "Cube dbt integration cube_dbt package 2025"
- **Data modeling**: "Cube data modeling cubes measures dimensions 2025"
- **Measures**: "Cube measures metrics types documentation 2025"
- **Dimensions**: "Cube dimensions time dimensions 2025"
- **Joins**: "Cube joins relationships between cubes 2025"
- **Pre-aggregations**: "Cube pre-aggregations materialization 2025"
- **REST API**: "Cube REST API query format 2025"
- **GraphQL API**: "Cube GraphQL API query format endpoint 2025"
- **SQL API**: "Cube SQL API Postgres wire protocol MEASURE syntax 2025"
- **SQL API psycopg2**: "Cube SQL API Python psycopg2 connection 2025"
- **Python client**: "Cube Python REST API client 2025"
- **Integration tests**: "Cube integration testing pytest httpx 2025"

## Integration Points to Research

### dbt → Cube Integration

**Key question**: How are dbt models exposed in Cube semantic layer?

Research areas:
- `cube_dbt` package installation and configuration
- manifest.json loading (`load_dbt_project()`)
- dbt model → Cube cube conversion
- dbt meta tags → Cube dimensions/measures metadata
- Selective model exposure (which dbt models to include)

### Cube → Consumption Applications

**Key question**: How do applications query the Cube semantic layer?

Research areas:
- REST API query format (JSON)
- SQL API for BI tools (Tableau, Looker, Metabase)
- GraphQL API for frontend apps
- JavaScript SDK for web applications
- Authentication and access control

### Governance Metadata Propagation

**Key question**: How should governance metadata flow to Cube?

Research areas:
- dbt meta tags → Cube dimension metadata
- Classification exposure in Cube API
- Access control (row-level, column-level)
- Audit logging for API queries

## Cube Development Workflow

### Local Development
```bash
# Install Cube CLI
npm install -g cubejs-cli

# Create new Cube project (if needed)
cubejs create my-cube-project -d postgres

# Start Cube development server
npm run dev

# Access Cube Playground
open http://localhost:4000
```

### Using dbt Integration
```yaml
# Install cube_dbt in Cube project
# In model/schema.yml
cubes:
  - name: my_cube
    public: true
    sql: >
      SELECT * FROM {{ dbt.ref('my_dbt_model') }}
    measures:
      - name: count
        type: count
    dimensions:
      - name: id
        sql: id
        type: number
```

### REST API Query
```python
import requests

# Query Cube REST API
response = requests.post(
    "http://localhost:4000/cubejs-api/v1/load",
    json={
        "query": {
            "measures": ["orders.count", "orders.total_amount"],
            "dimensions": ["orders.status"],
            "timeDimensions": [{
                "dimension": "orders.created_at",
                "granularity": "day",
                "dateRange": "last 30 days"
            }]
        }
    },
    headers={"Authorization": "Bearer <token>"}
)

data = response.json()
print(data["data"])  # Result set
print(data["annotation"])  # Schema metadata
```

## References

- [Cube Documentation](https://cube.dev/docs): Official documentation
- [dbt Integration](https://cube.dev/docs/product/data-modeling/recipes/dbt): Using Cube with dbt
- [cube_dbt package](https://cube.dev/docs/product/data-modeling/reference/cube_dbt): dbt integration reference
- [REST API Reference](https://cube.dev/docs/product/apis-integrations/rest-api/reference): REST API documentation
- [GitHub Repository](https://github.com/cube-js/cube): Cube source code
- [cube_dbt GitHub](https://github.com/cube-js/cube_dbt): dbt integration package

---

**Remember**: This skill provides research guidance, NOT prescriptive semantic models. Always:
1. Verify Cube availability and version
2. Discover existing Cube models and dbt integration patterns
3. Research Cube capabilities when needed (use WebSearch liberally)
4. Validate against actual consumption API requirements
5. Test REST API queries and measure calculations before considering complete
6. Understand dbt → Cube integration for metadata propagation
