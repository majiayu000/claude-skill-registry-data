---
name: talend
description: "Talend (Qlik Talend Cloud) specialist for Java-based enterprise data integration. Deep expertise in job design, tMap transformations, components, routines, context variables, Remote Engines, TMC, CI/CD with Maven, and migration from Open Studio. WHEN: \"Talend\", \"Qlik Talend\", \"Talend Cloud\", \"Talend Studio\", \"tMap\", \"tFileInput\", \"tRunJob\", \"Talend job\", \"Talend component\", \"Talend context\", \"context variable\", \"Talend routine\", \"tLogCatcher\", \"tStatCatcher\", \"Talend joblet\", \"Remote Engine\", \"Remote Engine Gen2\", \"Talend Management Console\", \"TMC\", \"Talend CI/CD\", \"Talend Maven\", \"CI Builder\", \"Talend ESB\", \"Talend Open Studio\", \"Talend bulk load\", \"tBulkExec\", \"Talend pipeline designer\", \"Talend execution plan\"."
license: MIT
---

# Talend (Qlik Talend Cloud)

This skill covers Talend, an enterprise data integration platform now branded as Qlik Talend Cloud following the May 2023 acquisition. Talend generates native Java code from visual job designs, supporting batch ETL, real-time streaming, API integration, data quality, and data governance. The current major version is **Talend 8.0** with monthly cumulative patches (R2026-xx). It provides deep knowledge of:

- Eclipse RCP-based Talend Studio with 1,000+ pre-built components
- Job design (Standard DI, Big Data Batch/Streaming, Routes, Services, Joblets)
- tMap transformation engine (lookups, filtering, expressions, multi-output routing)
- Context variables and context groups for environment management
- Remote Engines (Classic and Gen2) for customer-managed execution
- Talend Management Console (TMC) for scheduling, monitoring, and RBAC
- CI/CD with Maven, Talend CI Builder Plugin, and Nexus/Artifactory
- Java 17 requirement (as of R2025-02) and migration considerations
- Error handling (tLogCatcher, tStatCatcher, tWarn, tDie)
- Qlik acquisition impact, Open Studio discontinuation, and platform roadmap

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Architecture / job design** -- Load `references/architecture.md` for Studio, jobs, components, routines, metadata, TMC, Remote Engines, repository, and deployment tiers
   - **Performance / best practices** -- Load `references/best-practices.md` for job design patterns, performance optimization, error handling, deployment strategy, CI/CD, and reusable components
   - **Troubleshooting / diagnostics** -- Load `references/diagnostics.md` for job failures, performance bottlenecks, Remote Engine issues, memory management, and monitoring
   - **Open Studio migration** -- Consult features reference for Open Studio vs Cloud comparison and migration path
   - **Cross-tool comparison** -- See the `integration` skill for Talend vs ADF, NiFi, Informatica, etc.

2. **Gather context** -- Determine:
   - What is the job doing? (batch ETL, real-time streaming, API integration, ESB routing)
   - Where does it execute? (Talend Studio, Remote Engine, Cloud Engine)
   - Is this development, test, or production?
   - Java version? (Java 17 mandatory as of R2025-02)

3. **Analyze** -- Apply Talend-specific reasoning. Consider component selection, tMap configuration, context variable design, bulk loading opportunities, JVM sizing, and CI/CD pipeline structure.

4. **Recommend** -- Provide actionable guidance with specific component names, tMap expressions, JVM flags, Maven goals, and TMC configuration where appropriate.

5. **Verify** -- Suggest validation steps (tStatCatcher output review, tLogCatcher error analysis, TMC monitoring dashboards, Remote Engine log inspection).

## Core Architecture

### Studio-Job-Component Model

```
┌─────────────────────────────────────────────────┐
│  Talend Studio (Eclipse RCP)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │tMysqlInput│─│   tMap   │──│tMysqlOutput  │ │
│  │          │  │(transform)│  │              │ │
│  └──────────┘  └──────────┘  └──────────────┘ │
│       │             │              │           │
│  [Row Flow]   [Lookup Flow]  [Reject Flow]    │
│                     │                          │
│              ┌──────▼──────┐                   │
│              │ tLogCatcher │                   │
│              │(error flow) │                   │
│              └─────────────┘                   │
└─────────────────────────────────────────────────┘
                      │
              Code Generation
                      │
              ┌───────▼───────┐
              │  Java JAR     │
              │  (executable) │
              └───────┬───────┘
                      │
              ┌───────▼───────┐
              │ Remote Engine │
              │ or Cloud Engine│
              └───────────────┘
```

**Talend Studio** is the Eclipse RCP-based development environment with visual job designer, code generation engine, palette of 1,000+ components, repository browser, and debugging perspectives. Java 17 is required as of Talend 8.0 (R2025-02).

**Jobs** are the fundamental execution unit. Each job compiles to a self-contained JAR with all dependencies. Job types:
- **Standard DI Jobs**: Traditional batch ETL
- **Big Data Batch Jobs**: Spark-based batch processing
- **Big Data Streaming Jobs**: Spark Streaming for real-time
- **Route Jobs (ESB)**: Mediation routes based on Apache Camel
- **Service Jobs (ESB)**: RESTful or SOAP web service implementations
- **Joblets**: Reusable sub-job fragments shared across multiple jobs

**Components** are the building blocks placed on the canvas. Each component encapsulates specific functionality:

| Category | Key Components |
|---|---|
| **Database** | tMysqlInput/Output, tOracleInput/Output, tPostgresqlInput/Output, tSnowflakeInput/Output, tBigQueryOutput |
| **File** | tFileInputDelimited, tFileOutputDelimited, tFileInputExcel, tFileOutputExcel |
| **Cloud** | tS3Connection, tSnowflakeInput, tBigQueryOutput |
| **Messaging** | tKafkaInput, tJMSOutput |
| **API** | tRESTClient, tSOAP |
| **Transformation** | tMap, tJoin, tUnite, tNormalize, tDenormalize, tAggregate, tSort, tUniqRow, tFilterRow, tFilterColumns, tReplicate |
| **Orchestration** | tRunJob, tParallelize, tLoop, tIterateToFlow, tPreJob, tPostJob |
| **Bulk Operations** | tBulkExec, tMysqlBulkExec, tPostgresqlBulkExec, tOracleBulkExec |
| **Quality** | tMatchGroup, tFuzzyMatch, tPatternCheck, tDataMasking |
| **Error Handling** | tLogRow, tLogCatcher, tStatCatcher, tWarn, tDie, tFlowToIterate |

### tMap -- The Central Transformation Engine

tMap is the primary transformation component:
- **Lookups**: Load All (small lookups, in-memory), Reload at Each Row (dynamic), Flow to Stream (large lookups, streaming)
- **Filtering**: Expression-based filtering in tMap rather than separate tFilterRow
- **Multi-output routing**: Route records to multiple outputs based on conditions
- **Reject flows**: Route unmatched lookup records to error handling
- **Expression language**: Java-based expressions within tMap cells
- **Inner/outer joins**: Configure join type per lookup for matching behavior

### Context Variables and Environment Management

**Context Variables** externalize all environment-specific values (database URLs, file paths, API endpoints, credentials). **Context Groups** define variable sets per environment (DEV, QA, STAGING, PROD).

- Never hardcode environment-specific values in job logic
- Use implicit context loading from `.properties` files or database tables for runtime flexibility
- TMC context parameters override Studio-defined defaults at execution time

### Remote Engines

| Engine Type | Architecture | Executes |
|---|---|---|
| **Remote Engine (Classic)** | Customer-managed server (Linux/Windows) | Standard DI Jobs and Routes |
| **Remote Engine Gen2** | Docker-based containers | Pipeline Designer artifacts |
| **Cloud Engine** | Qlik-managed | Cloud-native tasks |

Remote Engines communicate with TMC via outbound HTTPS only. Classic engines use Nexus for artifact retrieval. Gen2 engines use Docker Compose with Component Server and Livy (Spark execution). TMC considers Gen2 connection broken after 180 seconds without heartbeat.

### Talend Management Console (TMC)

TMC is the cloud-based administration and operations platform:
- **Task management**: Create, schedule, and manage executable tasks from deployed artifacts
- **Scheduling**: 15+ trigger types including cron, Once, Daily, Weekly, Monthly, webhooks; Plan Builder for complex scenarios
- **Execution monitoring**: Real-time dashboards showing status, history, logs, errors
- **Execution Plans**: Multi-task orchestration with dependencies, sequencing, conditional execution
- **Environment management**: Logical separation of DEV, QA, STAGING, PROD
- **RBAC**: Granular permissions for projects, environments, and engines
- **REST API**: TMC API for programmatic task management and monitoring

### Version Control and CI/CD

**Git integration**: Talend Studio integrates natively with Git. Project items (jobs, routines, metadata, context groups) are stored and versioned in Git. Feature branches for development, merge to main for promotion.

**CI/CD Pipeline**:
1. Developer commits to Git feature branch
2. Code review and merge to integration branch
3. CI server triggers Maven build: `mvn deploy -Pnexus` using Talend CI Builder Plugin
4. Artifact published to Nexus Snapshot repository
5. QA deploys from Snapshot to test Remote Engine
6. After approval, promote to Nexus Release repository
7. Production deployment from Release repository via TMC

**Key Maven goals**: `mvn clean install` (local build), `mvn deploy -Pnexus` (Nexus), `mvn deploy -Pcloud-publisher` (Talend Cloud), `mvn deploy -Pdocker` (Docker image).

## Qlik Acquisition and Current State

- **Branding**: Now "Qlik Talend Cloud" across the product portfolio
- **Documentation**: Migrated from help.talend.com to help.qlik.com/talend
- **Open Studio discontinued**: Free tier ended January 31, 2024. No automated migration path; requires rebuild or manual adaptation (2-4 hours per complex job).
- **Java 17 mandatory** (R2025-02): Java 8 support ended. All builds and executions require Java 17.
- **QVD file generation** (R2025-05): New component bridges Talend ETL with Qlik analytics.
- **2026 roadmap**: Open lakehouse architectures, AI-driven data readiness, data products, no-code pipelines.

## Anti-Patterns

1. **Deep parent/child nesting** -- More than 3 levels of tRunJob nesting causes memory overhead and complexity. Keep hierarchies shallow with clear single-responsibility child jobs.
2. **tLogRow in production** -- Console output adds significant overhead. Remove or disable tLogRow components in production jobs. Set log level to ERROR or WARN.
3. **In-memory lookups for large tables** -- tMap "Load All" mode loads the entire lookup table into memory. For tables exceeding available heap, use database joins or tHashOutput/tHashInput staging.
4. **Sorting in Talend when the database can sort** -- tSort loads data into memory. Push ORDER BY to the source SQL query whenever possible.
5. **Hardcoded file paths and connection strings** -- Use context variables and context groups. Hardcoded values break when jobs move between environments.
6. **Auto-terminating error flows** -- Ignoring reject flows on tMap, database outputs, and quality components silently drops bad records. Always route rejects to error handling with tLogCatcher.
7. **Default JVM settings for production** -- Default `-Xms256M -Xmx1024M` is insufficient for production data volumes. Size to 2-8 GB based on workload.
8. **Full refreshes when incremental is possible** -- Scanning entire source tables every run does not scale. Use timestamp-based watermarks, CDC, or partition-based incremental loading.

## Reference Files

- `references/architecture.md` -- Studio IDE, job types and lifecycle, component architecture (1,000+ components), tMap internals, routines, metadata, TMC, Remote Engines (Classic and Gen2), repository and Git integration, CI/CD deployment tiers
- `references/best-practices.md` -- Modular job design (parent/child, joblets), tMap optimization, performance tuning (bulk loading, parallel execution, JVM sizing), error handling (three-tier model, reject flows, retry), deployment strategy, CI/CD pipeline (Maven, Nexus), reusable components
- `references/diagnostics.md` -- Job failure categories (compilation, connection, data, resource, Studio-vs-server), performance bottleneck identification (tStatCatcher, database I/O, transformation, parallelization), Remote Engine troubleshooting (Classic and Gen2), memory management (JVM tuning, GC, leak detection), monitoring

## Cross-References

- `integration` skill -- Talend vs ADF, NiFi, Informatica comparisons
- `overview` skill -- Cross-tool comparisons and paradigm routing
