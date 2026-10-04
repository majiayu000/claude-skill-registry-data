---
name: druid
description: "Apache Druid technology expert. Deep expertise in real-time analytics, columnar ingestion, segment management, query types, multi-stage query engine, and cluster operations. WHEN: \"Druid\", \"Apache Druid\", \"druid.io\", \"Druid SQL\", \"segment\", \"datasource\", \"ingestion spec\", \"Druid Coordinator\", \"Druid Broker\", \"Druid Historical\", \"Druid Overlord\", \"Druid Router\", \"rollup\", \"Druid MSQ\"."
license: MIT
---

# Apache Druid

This skill covers Apache Druid across all supported versions (31.x through 36.x). It covers Druid internals -- real-time OLAP architecture, segment storage, streaming and batch ingestion, the multi-stage query (MSQ) engine, Dart query engine, Druid SQL, native JSON queries, rollup and pre-aggregation, compaction, approximate algorithms, and distributed cluster operations. For version-specific detail, see the matching file under `references/versions/`.

## When to Use This Skill vs. Version-Specific Guidance

**Use this agent when the question spans versions or is version-agnostic:**
- "How does Druid's segment architecture work?"
- "Design a schema for a high-volume real-time event analytics workload"
- "Tune a Druid cluster for sub-second query latency"
- "Set up Kafka ingestion with exactly-once semantics"
- "Compare rollup strategies for time-series data"
- "Troubleshoot segment unavailability or ingestion lag"
- "Optimize a slow groupBy query on billions of rows"

**See the matching version reference when the question is version-specific:**
- "Druid 36.x cost-based autoscaling" --> `references/versions/36.x.md`
- "Druid 31.x Dart engine and projections" --> `references/versions/31.x.md`

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Architecture/internals** -- Load `references/architecture.md`
   - **Performance diagnostics** -- Load `references/diagnostics.md`
   - **Configuration/operations** -- Load `references/best-practices.md`
   - **Version-specific feature** -- See the matching `references/versions/<v>.md` file
   - **Comparison with other databases** -- see the `overview` skill

2. **Determine version** -- Ask if unclear. Behavior differs across versions (e.g., Dart engine in 31+, V10 segment format in 36+, cost-based autoscaling in 36+).

3. **Analyze** -- Apply Druid-specific reasoning. Reference segment architecture, column storage, partition granularity, rollup mechanics, query routing through Broker nodes, and ingestion pipeline design as relevant.

4. **Recommend** -- Provide actionable guidance with specific ingestion specs, SQL queries, REST API calls, runtime properties, or common.runtime.properties parameters.

5. **Verify** -- Suggest validation steps (system tables, REST API endpoints, supervisor status, segment metadata, Druid metrics).

## Core Expertise

### Real-Time OLAP Architecture

Apache Druid is a distributed, column-oriented, real-time analytics database designed for sub-second OLAP queries on event-driven data. It combines ideas from data warehousing, timeseries databases, and search systems.

**Key architectural principles:**
- **Column-oriented storage** -- Data is stored column-by-column in compressed segments, enabling high compression ratios and fast analytical scans
- **Inverted indexes** -- Druid builds bitmap indexes on string dimensions for fast filtering
- **Immutable segments** -- Data is organized into immutable segments that are time-partitioned and versioned
- **Scatter-gather query model** -- Brokers distribute queries to Historical and real-time nodes, merge results
- **Separation of ingestion and query paths** -- Ingestion (Overlord/MiddleManager) and querying (Broker/Historical) are independent, preventing resource contention
- **Pre-aggregation (rollup)** -- Data can be rolled up at ingestion time, dramatically reducing storage and query cost

### Node Types and Cluster Architecture

Druid operates as a cluster of specialized processes organized into three server types:

**Master Server:**
| Process | Port | Role |
|---|---|---|
| Coordinator | 8081 | Manages segment availability, load balancing, compaction, retention rules |
| Overlord | 8090 | Controls ingestion task assignment, maintains task queue, manages supervisors |

**Query Server:**
| Process | Port | Role |
|---|---|---|
| Broker | 8082 | Receives queries, routes to appropriate data nodes, merges results |
| Router | 8888 | Optional API gateway, routes requests to Brokers/Coordinators/Overlords, hosts web console |

**Data Server:**
| Process | Port | Role |
|---|---|---|
| Historical | 8083 | Stores and serves immutable segment data from deep storage cache |
| MiddleManager | 8091 | Manages Peon processes for ingestion tasks |
| Indexer | 8091 | Alternative to MiddleManager, runs tasks in threads instead of separate JVMs |

**Process interaction flow:**
```
Client --> Router --> Broker --> [Historical nodes + MiddleManager/Peon real-time tasks]
                                        |
                Coordinator <-- Metadata Store (MySQL/PostgreSQL/Derby)
                                        |
                Overlord --> MiddleManager --> Peon tasks
                                        |
                        Deep Storage (S3/HDFS/GCS/local)
                                        |
                        ZooKeeper (coordination/service discovery)
```

### Segment Architecture

The segment is the fundamental storage unit in Druid:

- **Time-partitioned** -- Each segment covers a specific time interval (hour, day, month, etc.)
- **Immutable** -- Once created, segments are never modified (compaction creates new segments)
- **Versioned** -- New data for the same interval creates a new version, atomically replacing the old
- **Self-contained** -- Each segment contains column data, indexes, and metadata

**Segment internal structure:**
```
segment_file.zip (smooshed file format)
  ├── version.bin               -- Segment format version (V9 or V10)
  ├── __time/                   -- Timestamp column (compressed long array)
  ├── dim_columns/
  │   ├── <dimension>.column    -- Dictionary-encoded, bitmap-indexed
  │   ├── <dimension>.dict      -- String dictionary (sorted)
  │   └── <dimension>.bitmap    -- Inverted bitmap index per value
  ├── met_columns/
  │   └── <metric>.column       -- Compressed numeric arrays or sketch objects
  ├── index.drd                 -- Segment metadata (dimensions, metrics, intervals)
  └── metadata.drd              -- Aggregator metadata for rollup
```

**Segment sizing best practices:**
- Target **3-5 million rows** per segment (most important guideline)
- Target **300-700 MB** per segment on disk
- Segments too small: excessive per-segment overhead in metadata, queries touch too many segments
- Segments too large: slow to load, poor query parallelism, expensive compaction

**Segment lifecycle:**
1. Ingestion task creates segments (real-time or batch)
2. Task pushes segments to deep storage (S3/HDFS/GCS)
3. Task publishes segment metadata to the metadata store
4. Coordinator assigns segments to Historical nodes based on load rules
5. Historical nodes download segments from deep storage and cache locally
6. Broker routes queries to Historical nodes serving the relevant segments
7. Retention rules or manual operations can mark segments as unused
8. Coordinator's kill task removes unused segments from deep storage

### Ingestion

Druid supports three primary ingestion methods:

**1. Streaming Ingestion (Kafka/Kinesis):**
```json
{
  "type": "kafka",
  "spec": {
    "ioConfig": {
      "type": "kafka",
      "consumerProperties": {
        "bootstrap.servers": "kafka-broker:9092"
      },
      "topic": "events",
      "inputFormat": { "type": "json" },
      "useEarliestOffset": true,
      "taskDuration": "PT1H",
      "completionTimeout": "PT30M"
    },
    "tuningConfig": {
      "type": "kafka",
      "maxRowsPerSegment": 5000000,
      "maxRowsInMemory": 1000000,
      "intermediatePersistPeriod": "PT10M"
    },
    "dataSchema": {
      "dataSource": "events",
      "timestampSpec": { "column": "timestamp", "format": "auto" },
      "dimensionsSpec": {
        "dimensions": [
          "event_type",
          { "type": "string", "name": "country" },
          { "type": "long", "name": "user_id" }
        ]
      },
      "granularitySpec": {
        "segmentGranularity": "HOUR",
        "queryGranularity": "MINUTE",
        "rollup": true
      },
      "metricsSpec": [
        { "type": "count", "name": "count" },
        { "type": "longSum", "name": "total_duration", "fieldName": "duration_ms" },
        { "type": "doubleSum", "name": "total_revenue", "fieldName": "revenue" },
        { "type": "HLLSketchBuild", "name": "unique_users", "fieldName": "user_id" }
      ]
    }
  }
}
```

**2. SQL-Based Batch Ingestion (MSQ Engine):**
```sql
-- INSERT: append data
INSERT INTO events
SELECT
  TIME_PARSE("timestamp") AS __time,
  event_type,
  country,
  user_id,
  duration_ms
FROM TABLE(
  EXTERN(
    '{"type":"s3","uris":["s3://bucket/data/events/*.json"]}',
    '{"type":"json"}',
    '[{"name":"timestamp","type":"string"},{"name":"event_type","type":"string"},
      {"name":"country","type":"string"},{"name":"user_id","type":"long"},
      {"name":"duration_ms","type":"long"}]'
  )
)
PARTITIONED BY DAY
CLUSTERED BY event_type;

-- REPLACE: overwrite a time range
REPLACE INTO events
OVERWRITE WHERE __time >= TIMESTAMP '2026-04-01' AND __time < TIMESTAMP '2026-04-08'
SELECT
  __time,
  event_type,
  country,
  COUNT(*) AS "count",
  SUM(duration_ms) AS total_duration
FROM events
WHERE __time >= TIMESTAMP '2026-04-01' AND __time < TIMESTAMP '2026-04-08'
GROUP BY 1, 2, 3
PARTITIONED BY DAY
CLUSTERED BY event_type;
```

**3. Classic Batch Ingestion (Parallel Index Task):**
- Native JSON-based ingestion specs submitted to the Overlord
- Supports local files, S3, GCS, HDFS, HTTP sources
- Parallel task with supervisor/worker model for scalability

### Druid SQL

Druid SQL translates SQL queries into native Druid queries via Apache Calcite:

```sql
-- Time-series aggregation
SELECT
  FLOOR(__time TO HOUR) AS "hour",
  COUNT(*) AS events,
  SUM(duration_ms) AS total_duration,
  APPROX_COUNT_DISTINCT_DS_HLL(user_id) AS unique_users
FROM events
WHERE __time >= CURRENT_TIMESTAMP - INTERVAL '24' HOUR
GROUP BY 1
ORDER BY 1 DESC;

-- TopN-style query
SELECT
  country,
  COUNT(*) AS events,
  AVG(duration_ms) AS avg_duration
FROM events
WHERE __time >= CURRENT_TIMESTAMP - INTERVAL '7' DAY
  AND event_type = 'purchase'
GROUP BY country
ORDER BY events DESC
LIMIT 100;

-- Window functions (Druid 31+)
SELECT
  __time,
  event_type,
  duration_ms,
  AVG(duration_ms) OVER (
    PARTITION BY event_type
    ORDER BY __time
    ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
  ) AS rolling_avg
FROM events
WHERE __time >= CURRENT_TIMESTAMP - INTERVAL '1' HOUR;

-- Multi-value dimension handling
SELECT
  MV_TO_ARRAY(tags) AS tag_array,
  COUNT(*) AS cnt
FROM events
WHERE MV_CONTAINS(tags, 'important')
GROUP BY 1;
```

### Native Queries

Druid's native query language is JSON over HTTP, posted to `/druid/v2`:

**Timeseries** -- fastest for time-bucketed aggregations without dimension grouping:
```json
{
  "queryType": "timeseries",
  "dataSource": "events",
  "intervals": ["2026-04-01/2026-04-08"],
  "granularity": "hour",
  "aggregations": [
    { "type": "count", "name": "events" },
    { "type": "longSum", "name": "total_duration", "fieldName": "duration_ms" }
  ]
}
```

**TopN** -- optimized for single-dimension top-k with aggregation:
```json
{
  "queryType": "topN",
  "dataSource": "events",
  "intervals": ["2026-04-01/2026-04-08"],
  "granularity": "all",
  "dimension": "country",
  "metric": "events",
  "threshold": 100,
  "aggregations": [
    { "type": "count", "name": "events" }
  ]
}
```

**GroupBy** -- most flexible, supports multi-dimension grouping:
```json
{
  "queryType": "groupBy",
  "dataSource": "events",
  "intervals": ["2026-04-01/2026-04-08"],
  "granularity": "day",
  "dimensions": ["event_type", "country"],
  "aggregations": [
    { "type": "count", "name": "events" },
    { "type": "HLLSketchMerge", "name": "unique_users", "fieldName": "unique_users" }
  ],
  "having": { "type": "greaterThan", "aggregation": "events", "value": 1000 }
}
```

**Scan** -- raw row retrieval without aggregation:
```json
{
  "queryType": "scan",
  "dataSource": "events",
  "intervals": ["2026-04-07/2026-04-08"],
  "columns": ["__time", "event_type", "country", "user_id"],
  "filter": { "type": "selector", "dimension": "event_type", "value": "error" },
  "limit": 1000
}
```

**Performance hierarchy:** Timeseries > TopN > GroupBy > Scan. Always use the most specific query type.

### Rollup (Pre-Aggregation)

Rollup collapses rows with identical dimension values and timestamp (at the query granularity) during ingestion:

```
-- Raw data (3 rows, same minute):
2026-04-07T10:05:23Z | click | US | user_42 | 150ms
2026-04-07T10:05:45Z | click | US | user_43 | 200ms
2026-04-07T10:05:59Z | click | US | user_42 | 100ms

-- After rollup with queryGranularity=MINUTE:
2026-04-07T10:05:00Z | click | US | 3 (count) | 450 (sum_duration) | 2 (HLL_users)
```

**Rollup configuration in ingestion spec:**
```json
{
  "granularitySpec": {
    "segmentGranularity": "DAY",
    "queryGranularity": "MINUTE",
    "rollup": true
  },
  "metricsSpec": [
    { "type": "count", "name": "count" },
    { "type": "longSum", "name": "total_duration", "fieldName": "duration_ms" },
    { "type": "HLLSketchBuild", "name": "unique_users", "fieldName": "user_id", "lgK": 12 }
  ]
}
```

**When to use rollup:**
- High-cardinality timestamp data where per-second granularity is unnecessary
- Aggregation-heavy query patterns (counts, sums, averages, distinct counts)
- Storage reduction is critical (rollup can reduce data 10-100x)

**When NOT to use rollup:**
- Need to query individual raw events (user sessions, transaction logs)
- All dimensions are high-cardinality (rollup provides little compression)
- Need exact distinct counts on non-sketch columns

### Data Modeling

**Dimensions vs. Metrics:**
- **Dimensions** -- Columns you filter and group by. String dimensions get dictionary encoding and bitmap indexes. Numeric dimensions are supported but lack bitmap indexes by default.
- **Metrics** -- Columns you aggregate. Can store raw values or pre-aggregated sketch objects (HLL, Theta, Quantile).
- **__time** -- The mandatory primary timestamp column. All data is partitioned by time.

**Schema design principles:**
1. **Minimize dimension cardinality** -- Lower cardinality = better rollup = smaller segments
2. **Use appropriate types** -- `long` for numeric IDs, `string` for categorical data, `double` for measurements
3. **Pre-aggregate with sketches** -- Use HLLSketchBuild for distinct counts, thetaSketchBuild for set operations, quantilesDoublesSketchBuild for percentiles
4. **Choose segment granularity wisely** -- HOUR for real-time streaming, DAY for batch, MONTH for low-volume or historical data
5. **Choose query granularity for rollup** -- MINUTE for operational dashboards, HOUR for trend analysis, DAY for executive reports

### Deep Storage and Metadata

**Deep storage** is the permanent home of segments. Supported backends:
- **S3** -- Most common in AWS deployments
- **HDFS** -- Common in Hadoop-adjacent environments
- **GCS** -- Google Cloud deployments
- **Azure Blob Storage** -- Azure deployments
- **Local filesystem** -- Development/testing only

**Metadata store** (MySQL, PostgreSQL, or Derby):
- Stores segment metadata (datasource, interval, version, dimensions, metrics, size)
- Stores ingestion task state and supervisor configuration
- Stores data source rules (retention, replication, tiering)
- Stores audit history and configuration

**ZooKeeper** (required for cluster coordination):
- Service discovery (nodes register themselves)
- Leader election (Coordinator, Overlord)
- Segment load/drop protocol between Coordinator and Historical
- Internal communication protocol

### Lookups

Lookups provide key-value dimension enrichment at query time:

```json
POST /druid/coordinator/v1/lookups/config
{
  "__default": {
    "country_names": {
      "version": "2026-04-07",
      "lookupExtractorFactory": {
        "type": "map",
        "map": { "US": "United States", "UK": "United Kingdom", "DE": "Germany" }
      }
    }
  }
}
```

```sql
-- Use lookup in SQL
SELECT
  LOOKUP(country_code, 'country_names') AS country_name,
  COUNT(*) AS events
FROM events
GROUP BY 1;
```

**Lookup types:**
- **Map** -- In-memory key-value from static map or URI (JSON/CSV/TSV)
- **Cached** -- Polled periodically from a remote source
- **JDBC** -- Loaded from a database table
- **Kafka** -- Continuously updated from a Kafka topic

### Approximate Algorithms

See `references/advanced-features.md#approximate-algorithms` — HLL, Theta Sketch, Quantiles (KLL), Tuple Sketch, and Bloom Filter extensions with their SQL functions and trade-offs.

### Compaction

Compaction rewrites existing segments to optimize them:

```json
POST /druid/coordinator/v1/compaction/config
{
  "dataSource": "events",
  "taskPriority": 25,
  "inputSegmentSizeBytes": 419430400,
  "maxRowsPerSegment": 5000000,
  "skipOffsetFromLatest": "PT1H",
  "tuningConfig": {
    "type": "index_parallel",
    "maxRowsInMemory": 1000000,
    "partitionsSpec": {
      "type": "hashed",
      "numShards": null,
      "partitionDimensions": ["event_type"]
    }
  },
  "granularitySpec": {
    "segmentGranularity": "DAY",
    "queryGranularity": "MINUTE"
  }
}
```

**Compaction benefits:**
- Merge small segments into optimally-sized ones (3-5M rows)
- Change partition scheme (dynamic to hash/range for perfect rollup)
- Add or change rollup (apply aggregation to older data)
- Change segment granularity (e.g., HOUR to DAY for cold data)
- Reorder dimensions for better compression
- Remove unused columns

### Query Caching

Druid supports multiple cache layers:
- **Broker-level result cache** -- Caches per-segment query results at the Broker
- **Historical-level segment cache** -- Caches per-segment results on the data node
- **Whole-query result cache** -- Caches entire query results (Druid 0.20+)

```properties
# Broker cache (common.runtime.properties)
druid.broker.cache.useCache=true
druid.broker.cache.populateCache=true
druid.cache.type=caffeine
druid.cache.sizeInBytes=2000000000

# Historical cache
druid.historical.cache.useCache=true
druid.historical.cache.populateCache=true
druid.cache.type=caffeine
druid.cache.sizeInBytes=5000000000
```

### Multi-Value Dimensions

See `references/advanced-features.md#multi-value-dimensions` — MV_CONTAINS, MV_TO_ARRAY/UNNEST expansion, and MV_FILTER_ONLY for querying multi-value string dimensions.

## Troubleshooting Playbooks

See `references/troubleshooting.md` — diagnostics and resolution steps for ingestion lag (Kafka/Kinesis), segment unavailability, query timeouts, out-of-memory errors, and compaction debt.

## Version Matrix

| Version | Release Date | Status (April 2026) | Key Features |
|---|---|---|---|
| 36.0.0 | Feb 2026 | Current | Cost-based autoscaling, V10 segment format, cgroup v2, Dart query reports |
| 35.0.1 | Dec 2025 | Supported | Performance improvements, stability fixes |
| 34.0.0 | Aug 2025 | Supported | Various enhancements |
| 33.0.0 | Apr 2025 | Supported | Stability and performance |
| 32.0.1 | Mar 2025 | Supported | Enhancements and fixes |
| 31.0.2 | Mar 2025 | Supported | Dart engine, projections, concurrent append/replace GA, MSQ window functions |

**Versioning convention:** Druid uses major.minor.patch semantic versioning. Each major release may contain breaking changes. Patch releases contain only bug fixes.

**Recommendation:** Use the latest stable release (36.0.0) for production. For organizations requiring proven stability, 35.0.x or 34.0.0 are solid choices. Version 31.x introduced foundational features (Dart, projections) that continue to mature in later releases.
