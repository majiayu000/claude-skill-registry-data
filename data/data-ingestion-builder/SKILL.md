---
name: data-ingestion-builder
description: Build new data ingestion providers following the FF Analytics registry pattern. This skill should be used when adding new data sources (APIs, files, databases) to the data pipeline. Guides through creating provider packages, registry mappings, loader functions, storage integration, primary key tests, and sampling tools following established patterns.
---

# Data Ingestion Provider Builder

Create complete data ingestion providers for the Fantasy Football Analytics project following established patterns. This skill automates the process of adding new data sources with proper structure, metadata, testing, and integration.

## When to Use This Skill

Use this skill proactively when:

- Adding a new data source to the pipeline (API, file, database)
- User mentions integrating data from a new provider
- User asks about "adding a provider" or "new data source"
- User references specific APIs or data sources to integrate (e.g., "add ESPN API", "integrate PFF data")
- Expanding data coverage for analytics

## Provider Integration Philosophy

The FF Analytics project follows these principles for data ingestion:

1. **Registry Pattern** - Central mapping of datasets to loaders
2. **Storage Abstraction** - Uniform Parquet output with metadata sidecars
3. **Metadata-First** - Every load produces `_meta.json` with lineage
4. **Testable Samples** - Primary key validation on sample data
5. **Local & Cloud** - Same code works for local paths and `gs://` URIs

## Provider Building Workflow

Follow this six-step process to create a complete provider:

### Step 1: Understand the Data Source

Before coding, gather information about the provider:

**Ask clarifying questions:**

- What datasets does this provider offer?
- What is the API/file format?
- What are the authentication requirements?
- What are the primary keys for each dataset?
- Are there rate limits or ToS considerations?
- What is the update frequency?

**Research existing documentation:**

- API documentation URLs
- Data schemas and field descriptions
- Authentication methods
- Rate limiting policies

**Output**: Clear understanding of:

- Dataset names and descriptions
- Primary keys for each dataset
- Authentication approach
- Any special considerations

### Step 2: Design the Registry

Map datasets to loader functions and define metadata.

**Use `assets/registry_template.py` as starting point.**

**For each dataset, define:**

- `name`: Logical dataset name (lowercase, descriptive)
- `loader_function`: Function name in loader.py
- `primary_keys`: Tuple of columns that uniquely identify rows
- `description`: Brief description of dataset contents
- `notes`: Special considerations, dependencies, or caveats

**Example registry design:**

```python
REGISTRY = {
    "players": DatasetSpec(
        name="players",
        loader_function="load_players",
        primary_keys=("player_id",),
        description="Player biographical and career data",
        notes="Updates daily. Includes active and retired players."
    ),
    "stats": DatasetSpec(
        name="stats",
        loader_function="load_stats",
        primary_keys=("player_id", "game_id", "stat_type"),
        description="Game-level player statistics",
        notes="Grain: one row per player per game per stat type"
    )
}
```

**Quality checks:**

- Primary keys are truly unique for the grain
- Dataset names are descriptive and consistent
- Loader function names follow `load_{dataset_name}` pattern

### Step 3: Create Provider Package Structure

Create the directory structure following the template.

**See `assets/package_structure.md` for complete structure.**

**Create directories:**

```bash
mkdir -p src/ingest/{provider}
mkdir -p tests
mkdir -p samples/{provider}
```

**Create files:**

- `src/ingest/{provider}/__init__.py` (empty or with exports)
- `src/ingest/{provider}/registry.py` (from Step 2)
- `src/ingest/{provider}/loader.py` (will implement in Step 4)
- `tests/test_{provider}_samples_pk.py` (will implement in Step 5)

**Naming:**

- Provider name: lowercase, underscore-separated
- Example: `nflverse`, `espn_api`, `my_provider`

### Step 4: Implement Loader Functions

Create loader functions using storage helper pattern.

**Use `assets/loader_template.py` as starting point.**

**For each dataset in registry:**

1. **Create loader function** following signature:

   ```python
   def load_{dataset_name}(
       out_dir: str = "data/raw/{provider}",
       **kwargs
   ) -> dict[str, Any]:
   ```

2. **Implement data fetching:**
   - API calls with proper authentication
   - File parsing (CSV, JSON, XML, etc.)
   - Database queries
   - Handle pagination, retries, error cases

3. **Convert to DataFrame:**
   - Prefer Polars for performance
   - Pandas acceptable for compatibility
   - Ensure consistent column types

4. **Write with storage helper:**

   ```python
   from ingest.common.storage import write_parquet_any, write_text_sidecar

   # Write Parquet
   write_parquet_any(df, parquet_file)

   # Write metadata sidecar
   metadata = {
       "dataset": dataset_name,
       "asof_datetime": datetime.now(UTC).isoformat(),
       "loader_path": "src.ingest.{provider}.loader.load_{dataset}",
       "source_name": "{PROVIDER}",
       "source_version": version,
       "output_parquet": parquet_file,
       "row_count": len(df)
   }
   write_text_sidecar(json.dumps(metadata, indent=2), f"{partition_dir}/_meta.json")
   ```

5. **Return manifest:**

   ```python
   return {
       "dataset": dataset_name,
       "partition_dir": partition_dir,
       "parquet_file": parquet_file,
       "row_count": len(df),
       "metadata": metadata
   }
   ```

**Reference examples:**

- `references/example_loader.py` - Complete nflverse loader
- `references/example_storage.py` - Storage helper implementation

**Common patterns:**

- Use `datetime.now(UTC)` for all timestamps
- Generate UUIDs for file names: `uuid.uuid4().hex[:8]`
- Partition by date: `dt=YYYY-MM-DD`
- Handle both local paths and `gs://` URIs uniformly

### Step 5: Create Primary Key Tests

Validate sample data quality with automated tests.

**Use `assets/test_template.py` as starting point.**

**Test structure:**

```python
@pytest.mark.parametrize("dataset_name,spec", REGISTRY.items())
def test_{provider}_primary_keys(dataset_name, spec):
    # 1. Find sample files
    # 2. Read with Polars
    # 3. Check PK columns exist
    # 4. Check PK uniqueness
    # 5. Report duplicates if found
```

**What to test:**

- Primary key columns exist in dataset
- Primary key uniqueness (no duplicates)
- Sample data is non-empty
- Metadata sidecars exist and are valid

**Run tests:**

```bash
pytest tests/test_{provider}_samples_pk.py -v
```

### Step 6: Integrate with Project Tooling

Connect the provider to existing workflows.

**Update `tools/make_samples.py`:**

Add provider-specific sampling logic:

```python
# In make_samples.py argument parser
elif args.provider == "{provider}":
    from ingest.{provider}.loader import load_{dataset}

    # Provider-specific argument parsing
    datasets = args.datasets or ["default_dataset"]

    for dataset in datasets:
        result = load_{dataset}(
            out_dir=args.out,
            **provider_kwargs
        )
        print(f"✓ Sampled {dataset}: {result['row_count']} rows")
```

**Update documentation:**

- `src/ingest/CLAUDE.md` - Add provider-specific notes
- Root `CLAUDE.md` - If architecturally significant
- `README.md` - If user-facing

**Create sample data:**

```bash
uv run python tools/make_samples.py {provider} --datasets {dataset1} {dataset2} --out ./samples
```

**Validate:**

```bash
# Check sample data created
ls -la samples/{provider}/

# Run PK tests
pytest tests/test_{provider}_samples_pk.py -v

# Check metadata
cat samples/{provider}/{dataset}/dt=*/_meta.json | jq .
```

## Resources Provided

### references/

Provider implementation examples from codebase:

- **example_registry.py** - Complete registry from nflverse with 10+ datasets
- **example_loader.py** - Nflverse shim loader with Python/R fallback pattern
- **example_storage.py** - Storage helper with local and GCS support

Load these references when implementing a new provider to see proven patterns.

### assets/

Templates for creating new providers:

- **registry_template.py** - Registry.py skeleton with placeholders
- **loader_template.py** - Loader function template with storage helpers
- **test_template.py** - Primary key test template with pytest
- **package_structure.md** - Complete directory structure and integration guide

Use these templates directly when generating provider code.

## Best Practices

### Registry Design

1. **Accurate primary keys** - Test with real data to verify uniqueness
2. **Descriptive names** - Use clear, consistent dataset names
3. **Document grain** - Notes should explain row-level granularity
4. **Consider joins** - Design PKs to enable joins with other datasets

### Loader Implementation

1. **Handle failures gracefully** - Return empty DataFrames with metadata on errors
2. **Include traceability** - Capture input parameters in metadata
3. **Respect rate limits** - Add delays, implement exponential backoff
4. **Validate before writing** - Check schema, row counts, nulls
5. **Use storage helpers** - Don't reimplement Parquet writing

### Testing

1. **Test with real samples** - Use actual provider data, not mocks
2. **Cover all datasets** - Parametrize tests across registry
3. **Check metadata completeness** - Validate all required fields
4. **Document expected failures** - If some rows expected to fail PK tests

### Integration

1. **Update make_samples.py** - Enable easy sample generation
2. **Document requirements** - Note authentication, dependencies, setup
3. **Add to CLAUDE.md** - Help future developers understand the provider
4. **Consider CI/CD** - Add to GitHub Actions if automated refresh needed

## Common Patterns

### Authentication

**Environment variables:**

```python
import os

api_key = os.environ.get("{PROVIDER}_API_KEY")
if not api_key:
    raise ValueError("Set {PROVIDER}_API_KEY environment variable")
```

**OAuth flow:**

```python
from requests_oauthlib import OAuth2Session

oauth = OAuth2Session(client_id, token=token)
response = oauth.get(endpoint)
```

### Pagination

**Offset-based:**

```python
all_data = []
offset = 0
limit = 100

while True:
    response = fetch(offset=offset, limit=limit)
    data = response.json()
    all_data.extend(data)

    if len(data) < limit:
        break
    offset += limit
```

**Cursor-based:**

```python
all_data = []
cursor = None

while True:
    response = fetch(cursor=cursor)
    data = response.json()
    all_data.extend(data["results"])

    cursor = data.get("next_cursor")
    if not cursor:
        break
```

### Rate Limiting

**Simple delay:**

```python
import time

for dataset in datasets:
    result = load_dataset()
    time.sleep(1)  # 1 second between requests
```

**Exponential backoff:**

```python
import time
from requests.exceptions import HTTPError

max_retries = 3
for attempt in range(max_retries):
    try:
        response = fetch()
        response.raise_for_status()
        break
    except HTTPError as e:
        if e.response.status_code == 429:  # Rate limit
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        else:
            raise
```

## Output Format

When helping user create a provider:

1. **After Step 2 (Registry Design):**

   ```text
   ✅ Registry Designed: {provider}

   Datasets defined:
   - {dataset1}: {description} (PK: {pk_columns})
   - {dataset2}: {description} (PK: {pk_columns})

   Ready to create package structure (Step 3)?
   ```

2. **After Step 4 (Loader Implementation):**

   ```text
   ✅ Loaders Implemented

   Created loader functions:
   - load_{dataset1}() - Fetches from {source}
   - load_{dataset2}() - Fetches from {source}

   All loaders use storage helpers and write metadata sidecars.

   Ready to create tests (Step 5)?
   ```

3. **After Step 6 (Integration Complete):**

  ```text
  ✅ Provider Integration Complete: {provider}

  Created:
  - Registry: src/ingest/{provider}/registry.py ({N} datasets)
  - Loaders: src/ingest/{provider}/loader.py
  - Tests: tests/test_{provider}_samples_pk.py
  - Samples: samples/{provider}/ ({N} datasets)

  Integration:
  - ✓ Added to tools/make_samples.py
  - ✓ Updated documentation
  - ✓ Primary key tests passing ({N}/{N})

  To use:

    ```bash
    # Generate samples
    uv run python tools/make_samples.py {provider} --datasets all --out ./samples

    # Run tests
    pytest tests/test_{provider}_samples_pk.py -v

    # Use in production
    from ingest.{provider}.loader import load_{dataset}
    result = load_{dataset}(out_dir="gs://ff-analytics/raw/{provider}")
    ```

   ```

## Handling User Scenarios

### Scenario: User wants to add a specific API

**User says:** "Add integration for the ESPN Fantasy API"

**Response:**

1. Begin Step 1 (Understand the Data Source)
2. Ask clarifying questions about ESPN API
3. Guide through all 6 steps to complete integration

### Scenario: User has API docs, needs implementation

**User says:** "I have the API docs for PFF, help me integrate it"

**Response:**

1. Ask user to share key details (datasets, auth, PKs)
2. Begin Step 2 (Design Registry)
3. Proceed through implementation steps

### Scenario: User wants to fix existing provider

**User says:** "The nflverse loader is missing a dataset"

**Response:**

1. Read existing provider registry and loaders
2. Add new dataset to registry (Step 2)
3. Implement loader for new dataset (Step 4)
4. Update tests and samples (Steps 5-6)

## Troubleshooting

**Issue:** Primary key tests failing

- Review data grain - are PKs actually unique?
- Check for null values in PK columns
- Verify sample data represents full population
- Consider composite keys if single column insufficient

**Issue:** Storage helper fails with GCS

- Check `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- Verify GCS bucket permissions
- Test with local path first, then GCS
- Review `references/example_storage.py` for patterns

**Issue:** Loader returns empty data

- Check authentication credentials
- Verify API endpoint URLs
- Review rate limiting and retries
- Add debug logging to data fetching

**Issue:** Make_samples.py not finding provider

- Ensure provider package in `src/ingest/{provider}/`
- Check PYTHONPATH includes src/
- Verify imports in make_samples.py
- Run from repo root directory

## Integration with Other Skills

This skill works well with:

- **dbt-model-builder** - After ingestion, create staging models for the provider
- **data-quality-test-generator** - Add comprehensive tests beyond primary keys
