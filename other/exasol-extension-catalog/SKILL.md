---
name: exasol-extension-catalog
description: "Catalog and selection guide for Exasol tools, extensions, connectors, integrations, and architecture patterns. Use when the primary intent is comparison, discovery, support-status research, or architecture selection rather than executing a workflow; hand operational work to the selected dedicated skill. Covers deploy, load, explore, enrich, surface, and scale capability families, including named products with no dedicated skill of their own such as Lakehouse Turbo, the Exasol MCP Server, Governed SQL / Text-to-SQL MCP Server, Agent Control Plane, Extension Manager, Terraform and Ansible tooling, and BI, ETL, and warehouse integrations such as Databricks, SAP, Kafka, Power BI, and Tableau."
---

# Exasol Extension Catalog Skill

Last reviewed: 2026-08-12.

Use this skill to discover or compare Exasol capability families. It helps the
user choose a tool, extension, connector, integration, or architecture pattern;
it is not an alternate execution guide for workflows that already have a
dedicated skill.

If the request asks to execute, configure, or troubleshoot a dedicated workflow
such as Text AI, Transformers, Cloud Storage Extension, native import/export,
JDBC or document virtual schemas, adapter development, BucketFS, UDF/SLC,
distributed ML, notebook-connector setup, or Exasol Personal setup, use that
specialized skill. Keep comparison and selection requests in this catalog even
when they name one or more of those options, then hand off after the choice.

The catalog organizes Exasol capabilities into six categories:

- **DEPLOY**: provision, install, package, configure, schedule, and operate Exasol.
- **LOAD**: ingest, import, federate, stream, move, or query external data.
- **EXPLORE**: inspect schemas, query data, use notebooks, BI tools, catalogs, and agentic query interfaces.
- **ENRICH**: add AI, ML, UDFs, text processing, semantic interpretation, agents, and custom computation.
- **SURFACE**: expose Exasol to humans, applications, BI, APIs, low-code tools, and agents.
- **SCALE**: improve scale-out, performance, reliability, governance, observability, testing, repeatability, and enterprise operations.

## Important Use Rules

1. Prefer official Exasol docs or GitHub repositories when giving installation or configuration instructions.
2. Distinguish between Exasol-owned or Exasol-maintained tools, Exasol Labs/community tools, and third-party ecosystem integrations.
3. For customer-facing recommendations, state support level when known. If support level is not explicit in the reference, verify the linked source before presenting it as supported.
4. For current versions, latest releases, security status, or support status, check the linked source before answering.
5. For destructive operations, deployment changes, credential management, RBAC, Terraform, or agent automation, include safety and rollback guidance.
6. For agentic workflows, prefer governed patterns: MCP Server, Agent Control Plane, semantic layer, SQL guardrails, audit logs, and least-privilege credentials.

## Category Selection

The trigger phrases below choose a *reference file within this catalog*; they do
not decide that this skill runs. That decision is made by intent: a request to
compare options, discover what exists, check support status, or select an
architecture belongs here, while a request to execute, configure, or
troubleshoot a named product belongs to that product's dedicated skill.

Choose the narrowest matching category and load only the matching reference
files. If multiple categories apply, load all relevant references before
answering. Once the user chooses a concrete workflow, hand off to its dedicated
skill instead of repeating operational instructions here.

1. **Run Exasol somewhere or operate deployment tooling**
   - Trigger phrases: `deploy`, `install`, `Exasol SaaS`, `Exasol Personal`, `Exasol Local`, `exasol-local-vm`, `STACKIT`, `Docker DB`, `Terraform`, `OpenTofu`, `Ansible`, `scheduler`, `public keys`, `artifact verification`, `Extension Manager`
   - Load: `references/deploy.md`

2. **Bring data into Exasol or query data elsewhere**
   - Trigger phrases: `load`, `ingest`, `import`, `federate`, `Virtual Schema`, `Databricks`, `SAP HANA`, `Snowflake`, `Oracle`, `PostgreSQL`, `Kafka`, `Kinesis`, `Spark`, `Glue`, `Azure Data Factory`, `migration`, `driver`, `ODBC`, `JDBC`, `PyExasol`
   - Load: `references/load.md`

3. **Understand data or query it interactively**
   - Trigger phrases: `explore`, `MCP`, `Text-to-SQL`, `VS Code`, `AI Lab`, `Notebook Connector`, `SQL client`, `catalog`, `semantic layer`, `metadata`
   - Load: `references/explore.md`

4. **Add AI, ML, UDFs, text analytics, or agents**
   - Trigger phrases: `AI`, `ML`, `transformers`, `sentiment`, `entity extraction`, `SageMaker`, `MLflow`, `model UDF`, `foundation model`, `Agent Control Plane`, `Rust UDF`, `Metadata Agent`
   - Load: `references/enrich.md`

5. **Expose Exasol to apps, BI, APIs, users, or agents**
   - Trigger phrases: `BI`, `dashboard`, `Dash`, `Plotly`, `dash-server`, `Grafana`, `Tableau`, `Power BI`, `Superset`, `REST API`, `ERA`, `Power Apps`, `low-code`, `application driver`, `CData`, `Denodo`, `Trino`
   - Load: `references/surface.md`

6. **Improve scale, governance, performance, observability, repeatability, or reliability**
   - Trigger phrases: `scale`, `performance`, `governance`, `RBAC`, `observability`, `CloudWatch`, `telemetry`, `SBOM`, `testing`, `CI`, `pytest-slc`, `SLC testing`, `change management`, `data protection`, `warehouse automation`
   - Load: `references/scale.md`

## Related Skills

- Use **exasol-database** for direct SQL, exapump, table design, and query profiling after choosing the relevant tool family.
- Use **exasol-import** for direct native `IMPORT`, local CSV or Parquet loading, connection objects for import, and native Parquet loading behavior.
- Use **exasol-export** for direct native `EXPORT`, local file export, and connection objects for export.
- Use **exasol-cloud-storage-extension** for Cloud Storage Extension import/export workflows after choosing that extension family.
- Use **exasol-jdbc-virtual-schemas** for JDBC/database-source virtual schema usage after choosing that federation family.
- Use **exasol-document-virtual-schemas** for document-file virtual schema usage (S3, GCS, Azure object storage) after choosing that federation family.
- Use **exasol-virtual-schema-adapter-development** for custom virtual schema adapter implementation, packaging, and adapter-side debugging after choosing that a maintained adapter is not enough.
- Use **exasol-bucketfs** for BucketFS file upload, download, list, and delete workflows.
- Use **exasol-udfs** for UDF and Script Language Container implementation details.
- Use **exasol-notebook-connector-config** and **exasol-notebook-connections** for notebook-connector configuration and Python connection helpers.
- Use **exasol-itde** for notebook-connector's local Docker database lifecycle after choosing that development environment.
- Use **exasol-text-ai** for Text AI Extension deployment, extraction, and validation.
- Use **exasol-transformers** for Transformers Extension deployment and inference.
- Use **exasol-distributed-ml** for in-database model training, inference, GPU, and iterative ML workflows.
- Use **exasol-setup-personal** for guided Exasol Personal deployment.
