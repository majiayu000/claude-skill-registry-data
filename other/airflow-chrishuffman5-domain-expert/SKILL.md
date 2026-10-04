---
name: airflow
description: "Expert skill for Apache Airflow across all versions. Provides deep expertise in DAG design, TaskFlow API, executors, scheduling, operators, XCom, deployment, and pipeline orchestration. WHEN: \"Airflow\", \"airflow DAG\", \"DAG not running\", \"TaskFlow\", \"XCom\", \"@task decorator\", \"Airflow operator\", \"Airflow sensor\", \"Airflow executor\", \"CeleryExecutor\", \"KubernetesExecutor\", \"Airflow scheduler\", \"MWAA\", \"Cloud Composer\", \"Astronomer\", \"airflow.cfg\", \"DAG parsing\", \"Airflow provider\", \"Airflow connection\", \"Airflow pool\", \"deferrable operator\", \"dynamic task mapping\", \"DAG bundle\", \"Airflow asset\", \"Airflow dataset\"."
license: MIT
---

# Airflow

This skill covers Apache Airflow across all supported versions (2.x through 3.x). It provides deep knowledge of:

- DAG design patterns (TaskFlow API, traditional operators, dynamic task mapping)
- Scheduler architecture (DAG parsing, task lifecycle, trigger rules, timetables)
- Executor types (Local, Celery, Kubernetes, Edge, multiple executors)
- XCom patterns (size limits, serialization, custom backends, reference-not-data)
- Operator and sensor ecosystem (80+ provider packages, deferrable operators)
- Deployment models (Docker, Kubernetes Helm chart, managed services, DAG bundles)
- Connection and secrets management (secrets backends, environment variables)
- Monitoring and observability (StatsD, Prometheus/Grafana, Deadline Alerts)
- Testing strategies (DAG validation, unit testing task logic, integration tests)
- Migration between major versions (2.x to 3.x)

When a question is version-specific, read the appropriate version reference below. When the version is unknown, provide general guidance and note where behavior differs across versions.

## When to Use This Skill's General Guidance vs. a Version Reference

**Use the general guidance in this file when:**
- The question applies across versions (DAG design, XCom patterns, executor selection)
- The version is unknown or the user needs guidance choosing a version
- Troubleshooting common issues (zombie tasks, scheduler delays, parsing errors)
- Architecture decisions (executor choice, deployment model, monitoring setup)
- Best practices (idempotency, testing, connection management, performance tuning)

**Read a version reference when:**
- The user specifies a version or the question involves version-specific features
- Airflow 2.x: `references/versions/2.x.md` -- TaskFlow API origin, smart sensors, datasets, grid view, EOL migration
- Airflow 3.x: `references/versions/3.x.md` -- API Server, DAG versioning, DAG bundles, Assets, HITL, asset partitioning

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for zombie tasks, scheduler delays, parsing errors, executor issues, DB maintenance
   - **Architecture / design** -- Load `references/architecture.md` for scheduler loop, executor types, metadata DB, DAG parsing, task lifecycle
   - **Best practices** -- Load `references/best-practices.md` for DAG design, TaskFlow API, XCom patterns, testing, monitoring, connection management, performance
   - **Deployment** -- Cover Docker, Kubernetes Helm chart, managed services (MWAA, Cloud Composer, Astronomer), DAG bundles
   - **Migration** -- Determine source and target versions, load both version agents and diagnostics

2. **Identify version** -- Determine which Airflow version the user runs. Key version gates:
   - TaskFlow API (`@task`): 2.0+
   - Deferrable operators: 2.2+
   - Dynamic task mapping: 2.3+
   - Data-aware scheduling (Datasets): 2.4+
   - Multiple executors: 2.10+ / 3.x
   - DAG versioning, API Server, Assets, DAG bundles: 3.0+
   - HITL workflows, Deadline Alerts: 3.1+
   - Asset partitioning, multi-team: 3.2+
   - If version is unclear, ask.

3. **Load context** -- Read the relevant reference file for deep technical detail.

4. **Analyze** -- Apply Airflow-specific reasoning. Consider executor type, deployment model, DAG complexity, data volume.

5. **Recommend** -- Provide actionable guidance with Python code examples and CLI commands.

6. **Verify** -- Suggest validation steps (`airflow dags test`, `airflow dags list-import-errors`, UI checks).

## Core Architecture

### How Airflow Works

```
              ┌───────────────┐
              │   DAG Files   │  Python (.py)
              └───────┬───────┘
                      │ parses
              ┌───────▼───────┐
              │   Scheduler   │  Orchestration engine
              │  (+ DAG Proc) │
              └───────┬───────┘
                      │ queues tasks
         ┌────────────┼────────────┐
         │            │            │
  ┌──────▼──────┐ ┌───▼────┐ ┌────▼─────┐
  │   Executor  │ │Trigger │ │API Server│  (Airflow 3)
  │ Local/Celery│ │  er    │ │ /Webserv │  or Webserver (2.x)
  │ /Kubernetes │ │(async) │ │  er      │
  └──────┬──────┘ └────────┘ └────┬─────┘
         │                        │
  ┌──────▼──────┐          ┌──────▼──────┐
  │   Workers   │          │  Metadata   │
  │  (execute   │          │  Database   │
  │   tasks)    │          │ (PostgreSQL)│
  └─────────────┘          └─────────────┘
```

1. **Parse** -- Scheduler reads DAG files (from local dirs, Git bundles, or S3 bundles in 3.x), serializes DAG structures into the Metadata Database
2. **Schedule** -- Scheduler evaluates dependencies, trigger rules, schedules, and pools to determine which tasks are ready
3. **Queue** -- Ready tasks are sent to the configured Executor
4. **Execute** -- Workers run the task code (as subprocesses, Celery workers, or Kubernetes Pods)
5. **Report** -- Task state transitions are recorded in the Metadata Database; XCom values stored for downstream tasks

### Scheduler

The central orchestration engine. Continuously parses DAG files, determines task readiness, queues tasks, manages state transitions, detects zombie tasks, and handles backfills (scheduler-managed in 3.x).

Key knobs: `parallelism`, `max_active_runs_per_dag`, `max_active_tasks_per_dag`, `min_file_process_interval`, `dag_dir_list_interval`.

### Executors

| Executor | How It Works | Best For | Trade-offs |
|---|---|---|---|
| **LocalExecutor** | Subprocess on scheduler machine | Dev, small-medium workloads | Single machine, no isolation |
| **CeleryExecutor** | Distributed via message broker (Redis/RabbitMQ) | Medium-large, horizontal scaling | Broker infra, workers need all deps |
| **KubernetesExecutor** | Each task in its own Pod | Heterogeneous workloads, isolation | Pod startup latency, K8s required |
| **Edge Executor** (3.x) | Tasks on edge/remote devices | IoT, hybrid cloud | New, limited ecosystem |
| **Multiple** (2.10+/3.x) | Combine executors per-task | Mixed workload profiles | Routing complexity, known bugs in 3.0.x |

### Metadata Database

PostgreSQL 13+ recommended (MySQL 8.0+ also supported). Stores DAG definitions, run/task states, XCom values, connections, variables, pools, users, and audit logs. In Airflow 3, workers access the DB exclusively through the API Server (no direct DB access from tasks).

### Task Lifecycle

```
none -> scheduled -> queued -> running -> success
                                      \-> failed -> up_for_retry -> scheduled ...
                                      \-> skipped
                                      \-> deferred -> scheduled ...
                                      \-> upstream_failed
```

Key states: `scheduled` (ready to run), `queued` (sent to executor), `running` (on a worker), `deferred` (waiting via Triggerer), `up_for_retry` (failed with retries remaining).

## Operators, Sensors, and Hooks

### Operators

Operators define what a task does. Categories:
- **Action operators** -- Perform work (BashOperator, PythonOperator, EmailOperator)
- **Transfer operators** -- Move data between systems (S3ToRedshiftOperator, GCSToBigQueryOperator)
- **Sensor operators** -- Wait for conditions (FileSensor, ExternalTaskSensor, HttpSensor)

In Airflow 3, common operators moved to `apache-airflow-providers-standard`. The broader ecosystem includes 80+ provider packages for AWS, GCP, Azure, Snowflake, dbt, Slack, and more.

### Sensors and Deferrable Operators

Sensors wait for external conditions. Three execution modes:
- **poke** -- Occupies a worker slot, periodically checking (resource-intensive)
- **reschedule** -- Releases the worker slot between checks (better for long waits)
- **Deferrable** -- Hands off to the Triggerer process for async waiting (most efficient, 2.2+)

**Always prefer deferrable sensors** for production workloads. They use asyncio to efficiently monitor many conditions concurrently without consuming worker slots.

### Hooks

Hooks abstract connection management for external systems. Operators use hooks internally. Examples: PostgresHook, S3Hook, HttpHook. Build custom hooks for reusable integrations, then build operators on top.

### Pools

Pools limit concurrent task instances across all DAGs:
- Create pools per external system (database connection pools, API rate limits)
- Set pool sizes based on the target system's capacity
- Tasks consume configurable `pool_slots` (default: 1)
- Use `priority_weight` to control which tasks get pool slots first

## TaskFlow API

The recommended way to write DAGs in Airflow 2.0+ (and especially 3.x):

```python
from airflow.sdk import dag, task  # Airflow 3.x imports

@dag(schedule="@daily")
def sales_pipeline():
    @task
    def extract():
        return {"path": "s3://bucket/sales/raw.parquet"}

    @task
    def transform(metadata):
        # metadata automatically pulled from XCom
        return {"path": "s3://bucket/sales/clean.parquet", "rows": 1500}

    @task
    def load(metadata):
        print(f"Loading {metadata['rows']} rows from {metadata['path']}")

    raw = extract()
    clean = transform(raw)
    load(clean)

sales_pipeline()
```

Benefits: implicit XCom handling, cleaner Python-native syntax, better type hints (3.x), automatic dependency inference. Mix freely with traditional operators.

## Dynamic Task Mapping

Create variable numbers of task instances at runtime:

```python
@task
def get_tables():
    return ["customers", "orders", "products"]

@task
def sync_table(table_name):
    extract_and_load(table_name)

tables = get_tables()
sync_table.expand(table_name=tables)  # 3 parallel task instances
```

Use `.partial()` for constant parameters and `.expand()` for varying ones. Supports mapping over task groups for complex per-item pipelines.

## XCom Patterns

XCom enables inter-task data exchange. Critical rules:

- **Pass references, not data** -- Store large outputs in S3/GCS, pass the path via XCom
- **Keep values small** -- Under 48 KB for reliability; over 1 MB causes performance degradation
- **JSON-serializable only** (Airflow 3 default backend) -- Pickling disabled for security
- **Never pass DataFrames or binary** -- Use object storage and pass file paths
- Use `multiple_outputs=True` for structured return values
- Custom XCom backends (S3, GCS) available for teams needing larger payloads

## Deployment Options

### Docker / Docker Compose
- Official image: `apache/airflow`
- Good for development, testing, and small deployments

### Kubernetes (Helm Chart)
- Official Helm chart from Airflow PMC (requires K8s 1.30+)
- Supports all executor types, Git-sync (2.x) or DAG bundles (3.x)
- Production-grade with log persistence and scaling

### Managed Services

| Service | Provider | Key Characteristics |
|---|---|---|
| **MWAA** | AWS | Fully managed, VPC integration, S3 for DAGs |
| **Cloud Composer** | GCP | GKE-based, integrated with GCP services |
| **Astronomer** | Astronomer | Full control, Helm-based, Astro CLI |

### DAG Bundles (Airflow 3.x)

Native DAG file sourcing replacing git-sync sidecars:
- **Local bundles** -- Traditional local directories
- **Git bundles** -- Native Git repo integration (replaces git-sync)
- **S3 bundles** -- Load DAGs from S3 (no versioning)
- Configured via `dag_bundle_config_list`

## Scheduling

| Method | When to Use |
|---|---|
| Cron expressions | Fixed time-based schedules (`"0 6 * * *"`) |
| Timetables | Custom scheduling logic (business days, market hours) |
| Data-aware (Assets/Datasets) | Trigger when upstream data is updated |
| Event-driven (3.x) | React to external events (SQS, asset watchers) |
| Manual-only (`schedule=None`) | On-demand or externally triggered DAGs |

## Connection Management

- **Development** -- Environment variables (`AIRFLOW_CONN_*`)
- **Production** -- Secrets backends (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager)
- Never hardcode credentials in DAG files
- Test connections via UI or CLI before deploying DAGs
- Use connection extras (JSON) for provider-specific parameters

## Testing

### DAG Validation (CI/CD)

Run in CI to catch errors before deployment:
```python
from airflow.models import DagBag

def test_no_import_errors():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert len(dagbag.import_errors) == 0, f"Errors: {dagbag.import_errors}"
```

### Unit Testing Task Logic

Extract business logic into pure functions and test independently of Airflow. Use `dag.test()` for end-to-end DAG testing in development.

### Migration Readiness

```bash
ruff check dags/ --select AIR301,AIR302  # Find Airflow 3 breaking changes
```

## Version-Specific Guidance

| Version | Reference | What's Version-Specific |
|---|---|---|
| Airflow 2.x | `references/versions/2.x.md` | TaskFlow API origin, smart sensors, Datasets, grid view, EOL (April 2026) migration path |
| Airflow 3.x | `references/versions/3.x.md` | API Server, DAG versioning, DAG bundles, Assets, HITL workflows, Deadline Alerts, asset partitioning |

## Provider Packages

Airflow's integration ecosystem is modular via provider packages:
- 80+ providers for AWS, GCP, Azure, Snowflake, dbt, Slack, databases, and more
- Providers are versioned independently from Airflow core
- **Airflow 3:** Core operators (BashOperator, PythonOperator, FileSensor) moved to `apache-airflow-providers-standard`
- Install only the providers you need to minimize dependency surface

## Monitoring

Key metrics to track (via StatsD or OpenTelemetry):
- `scheduler.scheduler_loop_duration` -- Scheduler health (increasing = overload)
- `scheduler.tasks.starving` -- Tasks waiting for pool/executor slots
- `executor.open_slots` / `executor.queued_tasks` -- Executor capacity
- `dag.duration.<dag_id>` -- Pipeline SLA tracking

Typical stack: Airflow -> StatsD -> Prometheus -> Grafana -> Alertmanager.

## Anti-Patterns

1. **Using Airflow as a compute engine** -- Running heavy Pandas/PySpark transformations inside Airflow workers. Airflow is an orchestrator. Delegate heavy processing to Spark, dbt, or warehouse SQL.
2. **Passing large data through XCom** -- Storing DataFrames, query results, or binary files in XCom. Pass file paths or object storage references instead.
3. **Top-level I/O in DAG files** -- Database queries, API calls, or file reads at module level. All logic must be inside task functions. Module-level code runs every scheduler parse cycle.
4. **God DAGs** -- A single DAG that extracts, transforms, validates, and loads everything. Break into focused DAGs with clear responsibilities and use Assets/Datasets for cross-DAG dependencies.
5. **Non-idempotent tasks** -- Tasks that produce different results when rerun with the same inputs. Use MERGE/upsert, partition overwrite, or deterministic file naming.
6. **Sensors in poke mode** -- Long-running sensors that occupy worker slots while waiting. Use deferrable sensors or reschedule mode instead.
7. **Hardcoded connections** -- Credentials in DAG code. Use Airflow Connections with secrets backends.
8. **Ignoring metadata DB growth** -- Never cleaning the metadata database. Run `airflow db clean` regularly to prevent scheduler performance degradation.

## Reference Files

- `references/architecture.md` -- Scheduler loop, executor internals, metadata DB schema, DAG parsing, task lifecycle, trigger rules, timetables, data-aware scheduling, security model
- `references/best-practices.md` -- DAG design patterns, TaskFlow API vs operators, XCom patterns, testing strategies, dynamic DAGs, monitoring, connection management, performance tuning, code organization
- `references/diagnostics.md` -- Zombie tasks, scheduler delays, DAG parsing errors, import errors, executor-specific issues, database maintenance, migration troubleshooting

## Diagnostic Scripts

Ready-made metadata-DB SQL (PostgreSQL, read-only) in `scripts/`, numbered by investigation order. Airflow 3 note: prefer the REST API for programmatic access, but these read-only queries remain valid against the same tables.

- `scripts/01-failed-tasks-recent.sql` -- Failures by DAG/task, last 7 days (code defect vs infra event pattern)
- `scripts/02-dag-run-durations.sql` -- DAG duration trend, avg/p95/max (SLA drift detection)
- `scripts/03-scheduler-lag.sql` -- Queued-to-started latency (executor/scheduler saturation)
- `scripts/04-stuck-tasks.sql` -- Zombie/stuck running and queued tasks holding pool slots
- `scripts/05-top-longest-tasks.sql` -- Slowest tasks by average duration (optimization targets)
