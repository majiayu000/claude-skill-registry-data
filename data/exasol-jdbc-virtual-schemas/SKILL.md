---
name: exasol-jdbc-virtual-schemas
description: "Use Exasol JDBC-based virtual schemas for federated read-only access to external databases such as PostgreSQL, Oracle, MySQL, SQL Server, and DB2. Covers database-source adapter selection, `CREATE VIRTUAL SCHEMA`, `ALTER VIRTUAL SCHEMA`, `EXPLAIN VIRTUAL`, metadata refresh, and query-side troubleshooting."
---

# Exasol JDBC Virtual Schemas Skill

Use this skill only for JDBC or database-source virtual schemas where Exasol queries external data in place.

Trigger when the user mentions **JDBC virtual schema**, **database-source federation**, **query external database through a virtual schema**, **JDBC source adapter**, **supported JDBC dialect**, or **EXPLAIN VIRTUAL** together with a JDBC/database-source virtual schema context.

## Routing Algorithm

1. **Create or query a JDBC virtual schema**
   - Trigger phrases: `JDBC virtual schema`, `query external database`, `database-source virtual schema`, `JDBC source adapter`
   - Load: `references/jdbc-virtual-schemas.md`

2. **Refresh, explain, or troubleshoot a JDBC virtual schema**
   - Trigger phrases: `EXPLAIN VIRTUAL` with JDBC context, `ALTER VIRTUAL SCHEMA` with JDBC context, `REFRESH TABLES`, `partial refresh`, `connection validation`, `pushdown`
   - Load: `references/jdbc-virtual-schemas.md`

3. **Choose a JDBC adapter family**
   - Trigger phrases: `supported JDBC dialect`, `dedicated adapter`, `PostgreSQL virtual schema`, `Oracle virtual schema`, `SQL Server virtual schema`, `MySQL virtual schema`, `DB2 virtual schema`
   - Load: `references/jdbc-virtual-schemas.md`

## Notes

- Use this skill for federated access through JDBC/database-source virtual schemas.
- Use **exasol-import** or **exasol-cloud-storage-extension** when the user wants to efficiently bulk-copy data into Exasol instead of querying it in place.
- Use **exasol-export** when the user wants to move Exasol data out to another system.
- Use **exasol-virtual-schema-adapter-development** when no maintained JDBC dialect fits and the user needs custom dialect code, packaging, or adapter-side debugging.
- Use **exasol-extension-catalog** when the source is not clearly JDBC/database-based or the user is still choosing between Virtual Schema, extension, connector, or integration families.
- Use **exasol-bucketfs** when the task is specifically about uploading, listing, or removing adapter and driver JARs in BucketFS.
