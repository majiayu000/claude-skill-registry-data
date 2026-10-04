---
name: exasol
description: Top-level router for Exasol work. Use for any Exasol database, exapump, SQL, BucketFS, extension, integration, UDF, Script Language Container, or Exasol Personal setup task, then route to the narrowest specialized Exasol skill.
---

# Exasol Router Skill

Use this skill whenever the user asks about Exasol. The user does not need to know internal skill names. Treat `/exasol <task>` and natural-language Exasol requests as the public interface.

Choose the narrowest skill whose front-matter `description` matches the request.
When several match, apply the precedence rules below; when several genuinely
apply, load them in dependency order.

## Precedence Rules

**Cloud Storage Extension over native import and export.** When a request
mentions `FROM SCRIPT CLOUD_STORAGE_EXTENSION`, `INTO SCRIPT
CLOUD_STORAGE_EXTENSION`, `CLOUD_STORAGE_EXTENSION.IMPORT_PATH`, or
`CLOUD_STORAGE_EXTENSION.EXPORT_PATH`, prefer
**exasol-cloud-storage-extension** over **exasol-import** or **exasol-export**.

**Object-storage formats that only the extension reads.** When a request
mentions importing `Avro`, `ORC`, or `Delta` from object storage such as S3,
Azure Blob Storage, Azure Data Lake, Google Cloud Storage, HDFS, or Alluxio,
prefer **exasol-cloud-storage-extension** unless the user clearly asks for
native `IMPORT`. Native import handles CSV, FBV, and Parquet; it does not read
those three formats, so a description match on "import from S3" alone routes
the request wrongly.

**Import and export over general database work.** When a request mentions
`IMPORT`, `IMPORT INTO`, or `exapump upload`, prefer **exasol-import** over
**exasol-database** even if the wording also contains generic terms such as
`SQL` or `query`. When it mentions `EXPORT`, `EXPORT INTO`, or `exapump export`,
prefer **exasol-export** the same way. A bare `CREATE CONNECTION` with no
import, export, or object-store file-movement intent belongs to
**exasol-database**.

**Adapter development over adapter use.** When a request mentions custom
virtual schema adapter implementation, source-specific JDBC dialect code,
custom document-file adapter code, `virtual-schema-common-jdbc`, adapter JAR
packaging, custom adapter properties, type mapping, pushdown capabilities,
metadata reader behavior, or adapter-side remote debugging, prefer
**exasol-virtual-schema-adapter-development** over
**exasol-jdbc-virtual-schemas** and **exasol-document-virtual-schemas**.

**Document-file virtual schemas over JDBC virtual schemas.** A virtual schema
over files in object storage — S3, Google Cloud Storage, Azure Blob Storage,
Azure Data Lake Storage Gen2 — is **exasol-document-virtual-schemas**. A
virtual schema over a database source such as PostgreSQL, Oracle, MySQL, SQL
Server, or DB2 is **exasol-jdbc-virtual-schemas**. Do not route a bare
`Virtual Schema` mention to the JDBC skill unless the source is clearly
database-based; ask which source is meant instead.

**Dedicated skills over the catalog.** Route to **exasol-extension-catalog**
only when the primary intent is comparison, discovery, support-status research,
or architecture selection — "which tool should I use", "what are the options
for", "is this supported". A request that names a product, extension, or
integration and asks to execute, configure, or troubleshoot it goes to that
product's dedicated skill, not to the catalog. In particular, Text AI Extension
and `TXAIE` work goes to **exasol-text-ai**, and Transformers Extension work
goes to **exasol-transformers**. Once the catalog has helped the user choose,
hand off.

**Container activation over container staging.** Activating or building a
Script Language Container belongs to **exasol-udfs** — that covers the
`SCRIPT_LANGUAGES` activation statements, flavors, and container builds. Getting
the container, JAR, or model file into a bucket belongs to **exasol-bucketfs**. A
request that uploads and then activates needs both: **exasol-bucketfs** to
stage the file, then **exasol-udfs** to activate it.

**Deployment intent is required for Exasol Personal.** Route to
**exasol-setup-personal** only when the user wants to install, deploy, or set up
Exasol itself. A bare cloud-provider or storage token such as `Azure Blob`,
`S3`, or `AWS` is not deployment intent — those belong to the import, export,
and document virtual schema skills. Deployment intent alone does not settle
which skill: a Docker-based database on the current machine is
**exasol-itde**, while a Mac VM or a deployment into the user's own AWS, Azure,
Exoscale, or STACKIT account is **exasol-setup-personal**. When the user asks
only for a "local" database, ask which of the two is meant.

## Dependency Order

When setup and usage both apply, resolve prerequisites first:

1. Exasol Personal or external database availability
2. Tool, extension, connector, or architecture selection
3. Virtual schema adapter selection when external federation is required
4. Custom virtual schema adapter implementation or packaging when a maintained adapter is not enough
5. Notebook-connector configuration when required
6. Local Docker database lifecycle or helper-level connectivity validation
7. Extension-specific TXAIE or Transformers workflow
8. SQL, data movement, BucketFS, UDF, SLC, or integration task
9. Distributed ML, data mining, or iterative HPC task (depends on UDF/SLC and BucketFS)

## User Interaction Rules

- Do not ask the user to choose a sub-skill.
- Infer the route from the task.
- If the task is ambiguous, ask one concrete question about the desired outcome, not about internal skill names.
- Prefer `/exasol <task>` in examples.
- Do not expose implementation labels such as **exasol-database** unless the user is contributing to this repo.

## Safety Rules

- Before executing a destructive operation, show the exact target and obtain
  confirmation.
- Never expose credentials, tokens, customer data, or secret configuration in
  commands, output, or generated files.
- Never read files that hold credentials, such as `~/.exapump/config.toml`. Use
  the tool's own masking commands instead, such as
  `exapump profile show <name>`.
- Follow any stricter safety or validation rules in the selected specialized
  skill.
