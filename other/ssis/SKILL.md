---
name: ssis
description: "Expert skill for SQL Server Integration Services (SSIS) across all versions (2014-2025). Provides deep expertise in control flow and data flow design, SSISDB catalog management, package deployment, performance optimization, Azure-SSIS IR, and migration planning. WHEN: \"SSIS\", \"Integration Services\", \"DTSX\", \".dtsx\", \"SSISDB\", \"SSIS package\", \"Data Flow Task\", \"Control Flow\", \"Execute Package Task\", \"OLE DB\", \"SSIS catalog\", \"SQL Agent SSIS\", \"SSIS deployment\", \"Azure-SSIS IR\", \"SSIS performance\", \"SSIS error\", \"Flexible File Task\", \"SSIS migration\", \"SSIS to ADF\", \"SSIS to Fabric\"."
license: MIT
---

# SSIS

This skill covers SQL Server Integration Services (SSIS) across all supported versions (2014 through 2025). It provides deep knowledge of:

- Control flow engine: task orchestration, precedence constraints, containers, event handlers, transactions, checkpoints
- Data flow engine: buffer-based pipeline, execution trees, synchronous vs asynchronous transformations, error outputs
- SSISDB catalog: project deployment, parameterization, environments, execution logging, catalog views
- Package design: master-child patterns, naming conventions, modular architecture
- Data flow optimization: buffer sizing, lookup caching, source query tuning, destination fast load
- Connection managers: OLE DB, ADO.NET, ODBC, Flat File, Excel, Flexible File (Azure Blob/ADLS)
- Deployment: project model (.ispac) vs legacy package model, CI/CD with SSIS DevOps Tools
- Azure-SSIS Integration Runtime: lift-and-shift, custom setup, VNet integration, cost management
- Security: protection levels, parameterized credentials, SSISDB encryption, proxy accounts
- Script extensibility: Script Task (control flow) and Script Component (data flow) in C#/VB.NET
- Expression language: property expressions, Derived Column, Conditional Split, variable evaluation
- Migration planning: SSIS to Azure Data Factory, Microsoft Fabric, Airflow, dbt

When a question is version-specific, read the appropriate version reference below. When the version is unknown, provide general guidance and note where behavior differs across versions.

## When to Use This Skill's General Guidance vs. a Version Reference

**Use the general guidance in this file when:**
- The question applies across SSIS versions (architecture, design patterns, optimization, deployment)
- The user's SSIS version is unknown
- The request involves migration planning or platform comparison
- The request is about SSISDB catalog management, CI/CD, or security best practices

**Read a version reference when:**
- The question involves version-specific features (e.g., Flexible File Task in 2019+, Entra ID in 2025)
- The question involves version-specific deprecations or breaking changes
- The user explicitly names a version ("SSIS 2025 package fails after upgrade")

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for common errors, performance bottlenecks, SSISDB monitoring queries, Azure-SSIS IR issues
   - **Architecture / package design** -- Load `references/architecture.md` for engine internals, buffer management, execution trees, connection managers, expression language
   - **Best practices** -- Load `references/best-practices.md` for design patterns, optimization, error handling, CI/CD, security, migration patterns
   - **Performance tuning** -- Load both `references/architecture.md` (buffer mechanics) and `references/best-practices.md` (optimization techniques)
   - **Deployment / CI/CD** -- Load `references/best-practices.md` for deployment models, DevOps tooling, multi-environment promotion
   - **Migration** -- Load `references/best-practices.md` for migration patterns to ADF, Fabric, Airflow, dbt

2. **Identify version** -- Determine which SQL Server / SSIS version the user runs. Key version gates:
   - Flexible File Task / Parquet support: 2019+
   - AutoAdjustBufferSize: 2016+
   - SSIS Scale Out: 2017+
   - ADO.NET with Microsoft.Data.SqlClient / Entra ID: 2025+
   - 32-bit deprecation: 2025
   - Attunity CDC removal: 2025
   If version is unclear, ask.

3. **Load context** -- Read the relevant reference file for deep technical detail.

4. **Analyze** -- Apply SSIS-specific reasoning. Consider engine type (control flow vs data flow), transformation blocking behavior, buffer impact, deployment model, and connection manager selection.

5. **Recommend** -- Provide actionable guidance. Include SSISDB catalog queries for monitoring, property settings for tuning, and step-by-step instructions for deployment or configuration.

6. **Verify** -- Suggest validation steps (execute in SSDT with data viewers, check SSISDB execution reports, review catalog.event_messages, test in non-production environment first).

## Core Architecture

### Two-Engine Design

SSIS separates concerns across two distinct engines:

```
Package (.dtsx)
├── Control Flow Engine (Runtime Engine)
│   ├── Tasks (Execute SQL, Script, File System, etc.)
│   ├── Containers (Sequence, For Loop, Foreach Loop)
│   ├── Precedence Constraints (Success/Failure/Completion + expressions)
│   ├── Event Handlers (OnError, OnWarning, OnPreExecute, etc.)
│   └── Transactions and Checkpoints
│
└── Data Flow Engine (Pipeline Engine)
    ├── Sources (OLE DB, Flat File, Excel, Flexible File, etc.)
    ├── Transformations (Derived Column, Lookup, Sort, Merge Join, etc.)
    ├── Destinations (OLE DB, Flat File, Raw File, etc.)
    └── Buffer Manager (in-memory row buffers, execution trees)
```

**Control flow** manages what runs and in what order. **Data flow** manages how data moves and transforms within a Data Flow Task.

### Buffer Architecture (Data Flow)

The data flow engine uses in-memory buffers for high throughput:

- Data flows through **buffers** (configurable via `DefaultBufferMaxRows` and `DefaultBufferSize`)
- Buffers are organized into **execution trees** from source (or async output) to next async transformation or destination
- Each execution tree gets its own worker thread

**Transformation types by buffer behavior:**

| Type | Behavior | Examples | Impact |
|---|---|---|---|
| Synchronous | Reuses input buffer, row-by-row | Derived Column, Conditional Split, Data Conversion, Multicast | Best performance |
| Semi-blocking | Requires subset of rows, creates new buffers | Merge, Merge Join, Union All | Moderate -- new buffers |
| Fully blocking | Must read ALL input before ANY output | Sort, Aggregate | Worst -- entire dataset in memory |

### SSISDB Catalog

The SSISDB catalog (project deployment model, 2012+) provides centralized management:

```
SSISDB
├── Folders
│   ├── Projects (.ispac deployments)
│   │   ├── Packages
│   │   └── Parameters
│   ├── Environments
│   │   └── Environment Variables (Dev/QA/Prod values)
│   └── Environment References
```

**Key capabilities:** deployment versioning, parameterized execution, automatic logging, built-in SSMS reports, catalog views for custom monitoring.

### Deployment Models

| Model | Unit | Target | Configuration | Status |
|---|---|---|---|---|
| **Project** (recommended) | .ispac (all packages) | SSISDB catalog | Parameters + environments | Current |
| **Package** (legacy) | Individual .dtsx files | File system / MSDB | .dtsConfig XML files | Deprecated in 2025 |

## Package Design

### Master-Child Pattern

Use a master package to orchestrate child packages via Execute Package Task:
- Master handles sequencing, error notification, logging
- Each child is a self-contained unit (one per source system or target table)
- Pass values via project parameters or parent package variables
- Benefits: modularity, parallel development, independent testing, reusability

### Naming Conventions

| Element | Pattern | Example |
|---|---|---|
| Tasks | Type prefix + description | `SQL_LoadCustomers`, `DFT_TransformOrders`, `SCR_ValidateInput` |
| Data flow components | Type prefix + source/target | `SRC_ODS_Customers`, `LKP_DimProduct`, `DST_DW_FactSales` |
| Variables | `User::v` prefix | `User::vFilePath`, `User::vRowCount` |
| Connection managers | Environment + system | `DEV_ODS_OleDb`, `PROD_DW_OleDb` |

### Complexity Guidelines

- One data flow per logical operation -- avoid monolithic data flows
- Group related tasks in Sequence Containers for shared error handling or transactions
- If a package exceeds ~50 tasks, split into multiple child packages
- Annotate business rules directly in the package designer

## Data Flow Optimization

### Buffer Tuning

| Property | Default | Guidance |
|---|---|---|
| `DefaultBufferMaxRows` | 10,000 | Increase for narrow rows; monitor memory |
| `DefaultBufferSize` | 10 MB | Increase up to 100 MB for wide rows |
| `AutoAdjustBufferSize` | false | Set true (2016+) to auto-calculate from row count |
| `EngineThreads` | 10 | Increase for data flows with many execution trees |

### Key Optimization Rules

1. **Prefer synchronous transformations** -- Derived Column, Conditional Split, Data Conversion reuse buffers
2. **Eliminate Sort/Aggregate in data flow** -- Push to source query (ORDER BY, GROUP BY) wherever possible
3. **Lookup: use full cache mode** with indexed reference tables and only needed columns
4. **Fast Load for destinations** -- OLE DB Destination with BULK INSERT; tune `MaxInsertCommitSize`
5. **Filter at source** -- Use SQL queries with WHERE clauses, not table mode
6. **Remove columns early** -- Drop unnecessary columns before expensive transformations
7. **Network packet size** -- Increase from 4 KB to 32 KB on OLE DB connection manager for large transfers

## Azure-SSIS Integration Runtime

Azure-SSIS IR is a managed cluster of Azure VMs in Azure Data Factory for running SSIS packages:

- **Lift-and-shift**: Run existing packages without rewriting
- **SSISDB hosting**: Azure SQL Database or Azure SQL Managed Instance
- **Scaling**: Configure node size and count (1-10+)
- **Custom setup**: Install drivers, components, assemblies on IR nodes
- **VNet integration**: Access on-premises data via VPN/ExpressRoute
- **Cost management**: Start/stop IR on schedule to avoid idle costs
- **Cold start**: ~20-30 minutes to provision/start

### Limitations

- No SSIS Scale Out support in Azure-SSIS IR
- Custom setup adds to startup time
- 64-bit only (no 32-bit providers)
- Cost: multi-node IR running 24/7 is expensive vs serverless ADF activities

## Version-Specific Guidance

| Version | Reference | What's Version-Specific |
|---|---|---|
| SSIS 2019 | `references/versions/2019.md` | Flexible File Task, Parquet/ORC/Avro support, Azure connectors |
| SSIS 2022 | `references/versions/2022.md` | Maintenance release, minimal SSIS changes, VS 2022 tooling |
| SSIS 2025 | `references/versions/2025.md` | Entra ID, TLS 1.3, deprecations (32-bit, legacy service, Attunity CDC) |

## Anti-Patterns

1. **Monolithic mega-package** -- A single package that extracts, transforms, and loads everything. Breaks modularity, blocks parallel development, and makes debugging painful. Use master-child pattern.

2. **Sort/Aggregate in data flow on large datasets** -- Fully blocking transformations hold the entire dataset in memory. Push to source query (ORDER BY / GROUP BY) or stage and use T-SQL.

3. **No-cache Lookup on high-volume data flows** -- Issues a query per row. Use full cache mode with indexed reference tables. Reserve no-cache for tiny or volatile reference sets.

4. **Hard-coded connection strings** -- Embeds server names, credentials, file paths directly in packages. Use project parameters mapped to SSISDB environment variables.

5. **EncryptSensitiveWithUserKey in production** -- Only the creating user can decrypt. Use DontSaveSensitive with parameters and SSISDB environment variables (ServerStorage encryption).

6. **Ignoring error output configuration** -- Leaving all components on "Fail component" for errors. Configure error outputs to redirect failed rows for investigation while allowing the pipeline to continue.

7. **SELECT * in source queries** -- Pulls unnecessary columns into buffers, wasting memory and reducing rows per buffer. Specify only needed columns.

8. **Using package deployment model for new projects** -- Legacy model lacks parameterization, environment management, and automatic logging. The package deployment model is deprecated in SSIS 2025. Use project deployment model.

### SSIS Future and Deprecation Awareness

SSIS remains fully supported through SQL Server 2025's lifecycle, but Microsoft is signaling a transition:

- **SSIS 2025 was announced on the Microsoft Fabric Blog**, not the SQL Server blog
- Only one new feature in 2025 (ADO.NET with Microsoft.Data.SqlClient); the rest was deprecations and removals
- Microsoft positions Fabric as the next-generation unified analytics platform
- **Invoke SSIS Package activity** in Fabric (preview) provides a bridge for existing packages
- No EOL date announced; SQL Server 2022 extended support runs through January 2033

**Practical guidance:**
- Existing packages: no immediate action; begin planning migration on a package-by-package basis
- New projects: prefer ADF, Fabric, or open-source alternatives unless on-premises SQL Server is required
- Hybrid: use Azure-SSIS IR or Fabric's Invoke SSIS Package while building new workloads on modern platforms
- Prioritize migrating packages that use removed components (Attunity CDC, Oracle connector, Hadoop tasks)

## Cross-Domain References

| Technology | Reference | When |
|---|---|---|
| SQL Server | The database plugin's `sql-server` skill | SQL Server platform context, Always Encrypted, T-SQL optimization for source queries |
| ETL domain | `overview` skill | Cross-platform comparison, tool selection, ETL vs ELT decision framework |
| Azure Data Factory | `adf` skill | ADF pipeline design, Azure-SSIS IR configuration, migration target |
| Airflow | `airflow` skill | Airflow as migration target, DAG-based orchestration alternative |

## Reference Files

- `references/architecture.md` -- Buffer management, execution trees, connection managers, expression language, Script Task vs Script Component, error handling mechanics, deployment models, SSISDB structure, Azure integration
- `references/best-practices.md` -- Package design patterns, data flow optimization, error handling strategy, CI/CD deployment, security, performance tuning, testing, migration patterns to ADF/Fabric/Airflow/dbt
- `references/diagnostics.md` -- Common errors (type conversion, truncation, connection timeout, lookup failure, validation, 32/64-bit), performance bottlenecks, SSISDB monitoring queries, debugging techniques, Azure-SSIS IR troubleshooting

## Diagnostic Scripts

Ready-made T-SQL against the SSISDB catalog in `scripts/`, numbered by investigation order. All read-only; run in SSMS on the catalog instance.

- `scripts/01-recent-executions.sql` -- 7-day execution summary by package with status mix
- `scripts/02-failed-execution-errors.sql` -- Error messages from failed executions (first error = root cause)
- `scripts/03-package-duration-trend.sql` -- 30-day duration trend (batch-window drift detection)
- `scripts/04-longest-executables.sql` -- Slowest tasks/containers inside packages (the bottleneck locator)
