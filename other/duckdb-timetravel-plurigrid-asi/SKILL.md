---
name: duckdb-timetravel
description: ' Layer 3: Temporal Versioning and ACSet Schema Generation for DuckDB'
version: 1.0.0
---


# duckdb-timetravel

> Layer 3: Temporal Versioning and ACSet Schema Generation for DuckDB

**Version**: 1.0.0  
**Trit**: 0 (Ergodic - coordinates data flow)  
**Bundle**: database  

## Overview

DuckDB-timetravel provides temporal versioning for interaction data, enabling queries across historical states. It integrates with ACSets for schema generation and supports DuckLake-style snapshots.

## Capabilities

### 1. temporal-query

Query data at specific points in time.

```sql
-- DuckLake-style time travel
SELECT * FROM interactions 
AT (VERSION => 3);

-- Snapshot at specific timestamp
ATTACH 'ducklake:interactions.db' 
  (SNAPSHOT_TIME '2024-11-30 00:00:00');

-- Query historical state
SELECT * FROM interactions
WHERE created_at < '2024-11-30'
AS OF TIMESTAMP '2024-11-15';
```

### 2. version-management

Create and manage temporal versions.

```python
from duckdb_timetravel import VersionManager

vm = VersionManager("interactions.duckdb")

# Create checkpoint
version_id = vm.checkpoint(
    message="Before pattern training",
    seed=0xf061ebbc2ca74d78
)

# List versions
versions = vm.list_versions()
# [
#   {id: 1, timestamp: "2024-11-01", message: "Initial import"},
#   {id: 2, timestamp: "2024-11-15", message: "Added network data"},
#   {id: 3, timestamp: "2024-11-30", message: "Before pattern training"}
# ]

# Restore to version
vm.restore(version_id=2)
```

### 3. acset-schema-gen

Generate DuckDB schemas from ACSet definitions.

```python
from duckdb_timetravel import ACSsetSchemaGenerator

gen = ACSsetSchemaGenerator()

# From ACSet category definition
schema = gen.from_acset("""
@acset ThreadOperad begin
    Thread::Ob
    Concept::Ob
    touches::Hom(Thread, Concept)
    parent::Hom(Thread, Thread)
    trit::Attr(Thread, Int)
    color_h::Attr(Thread, Float)
end
""")

# Generates:
# CREATE TABLE threads (
#     id VARCHAR PRIMARY KEY,
#     parent_id VARCHAR REFERENCES threads(id),
#     trit INT CHECK (trit IN (-1, 0, 1)),
#     color_h FLOAT CHECK (color_h >= 0 AND color_h < 360)
# );
# CREATE TABLE concepts (id VARCHAR PRIMARY KEY, name VARCHAR);
# CREATE TABLE thread_concepts (thread_id VARCHAR, concept_id VARCHAR);
```

### 4. diff-versions

Compare data between versions.

```python
diff = vm.diff(from_version=2, to_version=3)

# Returns:
# {
#   added: [{table: "interactions", count: 150}],
#   modified: [{table: "users", count: 12}],
#   deleted: [{table: "temp_cache", count: 1}],
#   schema_changes: []
# }
```

### 5. color-stream-history

Track GF(3) color stream evolution over time.

```sql
CREATE TABLE color_stream_history (
    stream VARCHAR,           -- 'LIVE', 'VERIFY', 'BACKFILL'
    index_position INT,
    thread_id VARCHAR,
    h FLOAT,                  -- Hue
    trit INT,                 -- -1, 0, +1
    timestamp TIMESTAMP,
    version_id INT,
    PRIMARY KEY (stream, index_position, version_id)
);

-- Query color evolution
SELECT stream, index_position, h, trit, timestamp
FROM color_stream_history
WHERE thread_id LIKE '%T-019b44%'
ORDER BY stream, index_position;
```

## DuckDB Schema Templates

### Thread Operad Schema

```sql
-- Core tables
CREATE TABLE thread_nodes (
    thread_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    message_count INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    trit INT CHECK (trit IN (-1, 0, 1)),
    color_h FLOAT,
    color_s FLOAT DEFAULT 0.7,
    color_l FLOAT DEFAULT 0.5,
    parent_thread_id VARCHAR,
    depth INT DEFAULT 0
);

-- GF(3) sibling verification view
CREATE VIEW gf3_sibling_triplets AS
SELECT 
    t1.thread_id as thread_1,
    t2.thread_id as thread_2,
    t3.thread_id as thread_3,
    (t1.trit + t2.trit + t3.trit) % 3 as sum_mod_3,
    CASE WHEN (t1.trit + t2.trit + t3.trit) % 3 = 0 
         THEN 'CONSERVED' ELSE 'VIOLATION' END as status
FROM thread_nodes t1
JOIN thread_nodes t2 ON t1.parent_thread_id = t2.parent_thread_id
JOIN thread_nodes t3 ON t2.parent_thread_id = t3.parent_thread_id
WHERE t1.thread_id < t2.thread_id 
  AND t2.thread_id < t3.thread_id;
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | clj-kondo-3color | Validates schema/queries |
| 0 | **duckdb-timetravel** | Coordinates temporal data |
| +1 | rama-gay-clojure | Generates data streams |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Configuration

```yaml
# duckdb-timetravel.yaml
database:
  path: "interactions.duckdb"
  wal_mode: true
  checkpoint_interval: 100

versioning:
  auto_checkpoint: true
  max_versions: 50
  compression: zstd

acset:
  schema_prefix: "acset_"
  generate_views: true
  gf3_verification: true

reproducibility:
  seed: 0xf061ebbc2ca74d78
```

## Justfile Recipes

```makefile
# Initialize database with schema
discohy-init-db:
    duckdb thread_operad.duckdb -c ".read db/thread_operad_schema.sql"

# Query thread tree
discohy-tree:
    duckdb thread_operad.duckdb -c "SELECT * FROM thread_tree ORDER BY depth, path"

# Check GF(3) conservation
discohy-gf3:
    duckdb thread_operad.duckdb -c "SELECT * FROM gf3_sibling_triplets"

# Time travel to version
discohy-restore version="1":
    duckdb thread_operad.duckdb -c "CALL restore_version({{version}})"

# View color stream history
discohy-stream-history thread_id:
    duckdb thread_operad.duckdb -c "SELECT stream, index_position, h, trit, timestamp FROM color_stream_history WHERE thread_id LIKE '%{{thread_id}}%' ORDER BY stream, index_position"
```

## Related Skills

- `acsets` - ACSet category definitions
- `clj-kondo-3color` - Schema validation
- `gay-mcp` - Color stream generation
- `entropy-sequencer` - Temporal arrangement



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Dataframes
- **polars** [○] via bicomodule
  - High-performance dataframes

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
duckdb-timetravel (+) + SDF.Ch4 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch6: Layering

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.

## Forward Reference

- unified-reafference (cross-universe coordination)


## Patterns That Work

- Temporal versioning with Bumpus sheaves
- ACSet schema generation from categories
- Cross-universe session alignment

## Patterns to Avoid

- Timestamp mixing without epoch conversion
- Queries without GF(3) conservation checks