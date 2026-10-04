---
name: exasol-document-virtual-schemas
description: "Use Exasol document-file virtual schemas for federated read-only access to object and file storage — S3, Google Cloud Storage, Azure Blob Storage, and Azure Data Lake Storage Gen2 document files. Covers document-file adapter family selection, the EDML `MAPPING` definition, `CREATE VIRTUAL SCHEMA` usage, refresh workflows, and query-side troubleshooting."
---

# Exasol Document Virtual Schemas Skill

Trigger when the user mentions **document virtual schema**, **document virtual schemas**, **document files virtual schema**, **document-file virtual schema adapter**, **EXPLAIN VIRTUAL** for document-file/object-storage virtual schema troubleshooting, **S3 document files**, **Google Cloud Storage document files**, **Azure Blob document files**, **Azure Data Lake Gen2 document files**, or **Azure Data Lake Storage Gen2 document files**.

## Routing Algorithm

1. **Create and query a virtual schema**
   - Trigger phrases: `document files virtual schema`, `S3 document files`, `Google Cloud Storage document files`, `Azure Blob document files`, `Azure Data Lake Gen2 document files`, `Azure Data Lake Storage Gen2 document files`, `query object storage`
   - Load: `references/document-virtual-schemas.md`

2. **Refresh, debugging, and troubleshooting**
   - Trigger phrases: `document files virtual schema`, `S3 document files`, `Google Cloud Storage document files`, `Azure Blob document files`, `Azure Data Lake Gen2 document files`, `Azure Data Lake Storage Gen2 document files`, `REFRESH`, `partial refresh`, `connection validation`, `pushdown`, `EXPLAIN VIRTUAL` for document-file/object-storage virtual schema troubleshooting
   - Load: `references/document-virtual-schemas.md`

3. **Choose the right document-file adapter family**
   - Trigger phrases: `document virtual schema`, `document virtual schemas`, `document-file virtual schema`, `document files virtual schema`, `S3 document files`, `Google Cloud Storage document files`, `Azure Blob document files`, `Azure Data Lake Gen2 document files`, `Azure Data Lake Storage Gen2 document files`
   - Load: `references/document-virtual-schemas.md`

## Notes

- Use this skill for federated read-only access through virtual schemas.
- Use **exasol-import** or **exasol-cloud-storage-extension** when the user wants to copy data into Exasol instead of querying it in place.
- Use **exasol-jdbc-virtual-schemas** when the source is a JDBC database rather than object or file storage.
- Use **exasol-virtual-schema-adapter-development** when maintained document-file adapters are insufficient and the user needs custom adapter code, packaging, or adapter-side debugging.
- Use **exasol-extension-catalog** when the source or integration family is still undecided.
- Use **exasol-bucketfs** if the task is specifically about uploading the adapter JAR into BucketFS.
