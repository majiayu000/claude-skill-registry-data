---
name: adf
description: "Azure Data Factory specialist for cloud-based data integration pipelines. Deep expertise in pipelines, activities, data flows, integration runtimes, triggers, CI/CD, and migration patterns. WHEN: \"Azure Data Factory\", \"ADF\", \"ADF pipeline\", \"copy activity\", \"data flow\", \"mapping data flow\", \"integration runtime\", \"self-hosted IR\", \"SHIR\", \"ADF trigger\", \"tumbling window\", \"ADF linked service\", \"ADF dataset\", \"ADF CI/CD\", \"adf_publish\", \"ADF monitoring\", \"ADF vs Synapse\", \"ADF vs Fabric\", \"ADF migration\", \"ADF CDC\", \"metadata-driven pipeline\"."
license: MIT
---

# Azure Data Factory

This skill covers Azure Data Factory (ADF), Microsoft's fully managed, serverless cloud data integration service. ADF is a managed service with no user-facing version numbers -- all factories run the latest platform release. It provides deep knowledge of:

- Pipeline and activity design (Copy, Data Flow, control flow, 90+ connectors)
- Integration Runtime architecture (Azure IR, Self-hosted IR, Azure-SSIS IR)
- Mapping Data Flows (visual Spark-based transformations)
- Trigger types (schedule, tumbling window, storage event, custom event)
- CI/CD with Git integration and ARM template deployment
- Monitoring, alerting, and cost optimization
- Migration paths from SSIS and toward Fabric Data Factory

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Architecture / pipeline design** -- Load `references/architecture.md` for IR types, pipeline execution model, data flow Spark backend, and managed VNET
   - **Performance / best practices** -- Load `references/best-practices.md` for Copy optimization, data flow tuning, CI/CD, security, and cost
   - **Troubleshooting / diagnostics** -- Load `references/diagnostics.md` for connectivity failures, IR issues, performance tuning, and cost analysis
   - **SSIS migration** -- See the `ssis` skill for SSIS-specific context, then apply ADF Azure-SSIS IR guidance
   - **Synapse Pipelines overlap** -- See the `synapse-pipelines` skill for Synapse-specific differences
   - **Cross-tool comparison** -- See the `integration` skill for ADF vs NiFi, Fivetran, Glue, etc.

2. **Gather context** -- Determine:
   - What does the pipeline do? (movement, transformation, orchestration, CDC)
   - What IR type? (Azure IR, Self-hosted IR, Azure-SSIS IR, Managed VNET)
   - Is this dev, test, or production?
   - Does the factory use Git integration?

3. **Analyze** -- Apply ADF-specific reasoning. Consider IR selection, connector capabilities, trigger semantics, expression language, and cost implications.

4. **Recommend** -- Provide actionable guidance with specific ADF configurations, expressions, and Azure CLI/PowerShell commands where appropriate.

5. **Verify** -- Suggest validation steps (pipeline debug runs, Data Flow data preview, Monitor Hub inspection, Azure Monitor KQL queries).

## Core Architecture

### Pipeline-Activity-Dataset-LinkedService Model

```
┌─────────────────────────────────────────────┐
│  Pipeline                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Lookup   │──│ ForEach  │──│  Copy    │  │
│  │ Activity │  │ Activity │  │ Activity │  │
│  └──────────┘  └──────────┘  └────┬─────┘  │
│                                   │         │
│                            ┌──────▼──────┐  │
│                            │  Dataset    │  │
│                            └──────┬──────┘  │
│                            ┌──────▼──────┐  │
│                            │Linked Svc   │  │
│                            └──────┬──────┘  │
└───────────────────────────────────┼─────────┘
                                    │
                          ┌─────────▼─────────┐
                          │Integration Runtime│
                          └─────────┬─────────┘
                                    │
                          ┌─────────▼─────────┐
                          │   Data Source      │
                          └───────────────────┘
```

**Pipelines** are the top-level orchestration container. Each pipeline contains activities, receives parameters from triggers, and produces a run with a unique Run ID. Pipelines can invoke child pipelines via Execute Pipeline activity.

**Activities** fall into three categories:
- **Data Movement**: Copy Activity (primary mechanism, 90+ connectors, format conversion, DIU-based parallelism)
- **Data Transformation**: Data Flow, Databricks Notebook/JAR/Python, HDInsight, Stored Procedure, Azure ML, Custom (.NET)
- **Control Flow**: If Condition, ForEach, Until, Switch, Wait, Web, Lookup, Get Metadata, Set Variable, Append Variable, Filter, Execute Pipeline, Validation, Webhook, Fail

**Datasets** are named views of data pointing to a location within a linked service (table, folder, file). Parameterize datasets for dynamic resolution at runtime.

**Linked Services** define connection strings, authentication methods, and endpoint details for external data stores and compute. Support managed identity, service principal, Key Vault references, and SAS tokens.

### Integration Runtime Types

The IR is the compute bridge between ADF and data sources:

| IR Type | Use Case | Network | Compute |
|---|---|---|---|
| **Azure IR** | Cloud-to-cloud data movement, data flows | Public or Managed VNET with private endpoints | Serverless, auto-scaling |
| **Self-hosted IR** | On-premises sources, private networks, firewalls | Outbound HTTPS only (443), no inbound ports | Windows machine or Azure VM, multi-node HA |
| **Azure-SSIS IR** | Run SSIS packages natively in Azure | Optional VNet join for on-premises access | Managed cluster, per-node billing |

**Azure IR** options: auto-resolve (region closest to source), fixed-region (compliance), Managed VNET (private endpoints with data exfiltration prevention).

**Self-hosted IR** can be shared across multiple data factories. Supports high availability via active-active multi-node. Communicates outbound only.

**Azure-SSIS IR** supports SSISDB on Azure SQL Database or Managed Instance, custom setup scripts, and Enterprise tier for advanced components.

### Data Flows

Mapping Data Flows are visually designed transformations executed on managed Apache Spark clusters:

- **Transformations**: Source, Sink, Derived Column, Filter, Select, Join, Lookup, Exists, Union, Conditional Split, Aggregate, Pivot, Unpivot, Window, Rank, Surrogate Key, Alter Row, Assert, Flowlet, Parse, Stringify, Flatten, External Call
- **Schema drift**: Handles dynamically changing schemas without breaking pipelines
- **Debug mode**: Interactive testing with live data preview on a warm Spark cluster
- **Flowlets**: Reusable parameterized sub-flows to reduce duplication
- **Expression language**: Rich function library (string, math, date/time, conversion, logical, aggregate) with IntelliSense in ADF Studio

Wrangling Data Flows (Power Query-based) were deprecated in 2024. Use Mapping Data Flows or migrate to Fabric Dataflow Gen2.

**Performance levers**: Cluster compute type (General Purpose / Compute Optimized / Memory Optimized), core count, Time-to-Live for warm clusters, partition strategy, broadcast joins, logging level.

### Triggers

| Trigger Type | Semantics | Pipeline Relationship | State |
|---|---|---|---|
| **Schedule** | Cron-like wall-clock schedule | Many-to-many | Stateless (no built-in retry) |
| **Tumbling Window** | Fixed-size non-overlapping intervals with backfill | One-to-one | Stateful (retry, dependencies) |
| **Storage Event** | Blob created/deleted (Event Grid) | Many-to-many | Event-driven |
| **Custom Event** | Event Grid custom topics | Many-to-many | Event-driven |

**Tumbling Window** is the most powerful trigger type: retains state, supports backfill of historical periods, has built-in retry policies, and supports trigger-to-trigger dependencies for chaining time-slice processing.

**Storage Event** triggers use Event Grid subscriptions and filter on blob path prefix/suffix. Expect 1-2 minute latency from file arrival to pipeline start.

### Monitoring

- **Monitor Hub** in ADF Studio: Pipeline runs, activity runs, trigger runs with status, duration, error details, and resource consumption
- **Azure Monitor**: Diagnostic settings to Log Analytics, custom KQL dashboards, alert rules on failure/duration/IR health
- **Copy Activity details**: Rows read/written, data volume, throughput (MB/s), DIU usage, duration per stage
- **Data Flow details**: Spark execution metrics, partition counts, stage times, cluster utilization
- **Rerun**: Failed pipelines can be rerun from the point of failure or from the beginning

### Source Control and CI/CD

**Git integration**: Native support for Azure Repos and GitHub. Only the development factory connects to Git. Feature branches for development, collaboration branch (typically `main`) for stable code. ADF Studio loads 10x faster with Git.

**Deployment workflow**:
1. Merge feature branch to collaboration branch
2. CI pipeline validates ADF resources and generates ARM templates (using `@microsoft/azure-data-factory-utilities` NPM package)
3. CD pipeline deploys ARM template to test, then production, with environment-specific parameter files
4. Pre-deployment: stop triggers. Post-deployment: start triggers, clean up removed resources.

**Key rule**: Never make manual changes to test or production factories. All changes flow through Git and CI/CD.

### Change Data Capture

ADF provides a native CDC resource for continuous (non-batch) data capture:
- Guided setup in ADF Studio: select source, destination, optional transformations
- Runs continuously, tracking changes at the source and applying incrementally
- Supports SQL Server, Azure SQL, Oracle, PostgreSQL sources
- SAP CDC via ODP framework for delta extraction

For batch-style incremental loads, use watermark patterns with Lookup + Copy Activity or tumbling window triggers with window start/end parameters.

## ADF vs Synapse Pipelines vs Fabric Data Factory

| Dimension | ADF | Synapse Pipelines | Fabric Data Factory |
|---|---|---|---|
| **Engine** | ADF engine | Same engine as ADF | ADF core + Fabric additions |
| **Hosting** | Standalone service | Inside Synapse workspace | Inside Fabric workspace |
| **Connectors** | 90+ (broadest) | Subset of ADF | Expanding (OneLake native) |
| **Unique features** | SSIS IR, broadest connectors, longest feature history | Tight Synapse SQL/Spark pool integration, Synapse Link | OneLake, Copilot AI, Dataflow Gen2, copy jobs, mirroring |
| **CI/CD** | Mature ARM template pipeline | ARM template (Synapse-specific) | Git integration (evolving) |
| **Cost** | Per-activity + DIU | Per-activity + pool cost | Fabric capacity-based |
| **Strategic direction** | Stable, fully supported, no new features since mid-2024 | Stable within Synapse | Microsoft's primary investment target |

**Guidance**: ADF for existing investments, standalone ETL, on-premises heavy workloads, and mature CI/CD. Synapse Pipelines for Synapse-centric analytics. Fabric Data Factory for greenfield projects and organizations adopting Microsoft Fabric. Migration assistant (ADF/Synapse to Fabric) entered public preview March 2026.

## Anti-Patterns

1. **Using Data Flows for simple copies** -- Data Flows spin up Spark clusters (3-5 min cold start, vCore-hour billing). Use Copy Activity for straightforward data movement.
2. **Hardcoding values in pipelines** -- Externalize all configuration into parameters, global parameters, and metadata tables. A parameterized pipeline handles hundreds of sources.
3. **One pipeline per table** -- Build metadata-driven pipelines with Lookup + ForEach instead of creating hundreds of identical pipelines.
4. **Ignoring DIU tuning** -- Default 4 DIU is too low for large data volumes. Test incrementally (4 -> 8 -> 16 -> 32 -> 64) and monitor throughput gain.
5. **No TTL on frequent Data Flows** -- Without TTL, every execution pays 3-5 minutes of Spark cold start. Set TTL proportional to scheduling frequency.
6. **Manual changes to non-dev factories** -- All changes must flow through Git and CI/CD. Manual edits to test/prod factories cause drift and deployment failures.
7. **Oversized Azure-SSIS IR left running** -- Azure-SSIS IR charges per node based on uptime. Stop when not in use; schedule start/stop for SSIS execution windows.
8. **Ignoring data exfiltration prevention** -- In regulated environments, enable Managed VNET with data exfiltration prevention to restrict outbound traffic to approved private endpoints only.

## Metadata-Driven Pipeline Pattern

The most scalable ADF design pattern -- a single parameterized pipeline handles integration for hundreds of sources:

1. **Control table** stores configuration: source object, target, load type (full/incremental), key columns, watermark column, active flag
2. **Lookup activity** reads the control table at runtime
3. **ForEach activity** iterates over results, executing a child pipeline per source
4. **Parameterized datasets and linked services** resolve connection details dynamically
5. **Copy Activity** source query, sink table, and column mapping are all driven by metadata

Adding a new source becomes a configuration row, not a pipeline change.

## Reference Files

- `references/architecture.md` -- IR deep dive (Azure IR auto-resolve vs Managed VNET, SHIR networking, Azure-SSIS IR provisioning), pipeline execution model, data flow Spark backend, managed VNET and private endpoints, connector ecosystem
- `references/best-practices.md` -- Pipeline design patterns (metadata-driven, parent-child, incremental load), Copy Activity optimization (DIU, parallel copy, staging, partitioning), data flow performance tuning, error handling, CI/CD workflow, security hardening, cost optimization
- `references/diagnostics.md` -- Connectivity failures, IR troubleshooting (SHIR offline, Azure-SSIS startup), data type mapping errors, Copy/Data Flow performance issues, trigger problems, debugging workflows, cost analysis

## Diagnostic Scripts

Ready-made Az PowerShell scripts (Az.DataFactory module, Reader role) in `scripts/`, numbered by investigation order. All read-only; placeholders are `__UPPER_SNAKE__` tokens.

- `scripts/01-pipeline-runs-summary.ps1` -- 7-day run status/duration summary per pipeline
- `scripts/02-failed-activity-runs.ps1` -- Activity-level errors for a failed run (root-cause activity)
- `scripts/03-trigger-status.ps1` -- Trigger runtime states (stopped triggers = silent staleness)

## Cross-References

- `ssis` skill -- SSIS migration context (Azure-SSIS IR lift-and-shift, package execution)
- `synapse-pipelines` skill -- Synapse Pipelines overlap and differences
- `overview` skill -- Cross-tool comparisons and paradigm routing
