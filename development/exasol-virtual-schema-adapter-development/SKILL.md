---
name: exasol-virtual-schema-adapter-development
description: "Build, install, validate, and debug custom Exasol virtual schema adapters. Covers source-specific JDBC dialect implementation with `virtual-schema-common-jdbc` including `SqlDialect`, metadata reader behavior, type mapping, and pushdown capabilities, custom document-file adapter code boundaries, custom adapter properties, JAR packaging, BucketFS deployment, adapter script setup, `EXPLAIN VIRTUAL` validation, and adapter-side remote debugging workflows."
---

# Exasol Virtual Schema Adapter Development Skill

Trigger when the user mentions **build a custom virtual schema adapter**, **virtual-schema-common-jdbc**, **remote debugging for a virtual schema adapter**, **new SQL dialect adapter**, **source-specific JDBC dialect**, **custom document-file adapter implementation**, **custom adapter properties**, **pushdown capabilities**, **type mapping**, **metadata reader**, or **adapter JAR packaging**.

## Routing Algorithm

1. **Build or customize an adapter**
   - Trigger phrases: `custom adapter`, `build virtual schema adapter`, `new SQL dialect`, `source-specific JDBC dialect`, `custom document-file adapter`, `virtual-schema-common-jdbc`, `SqlDialect`, `AdapterFactory`, `VirtualSchemaAdapter`, `metadata reader`
   - Load: `references/adapter-development.md`

2. **Design adapter behavior**
   - Trigger phrases: `custom adapter properties`, `pushdown capabilities`, `type mapping`, `identifier quoting`, `literal rendering`, `function pushdown`, `custom dialect tests`, `adapter integration tests`
   - Load: `references/adapter-development.md`

3. **Install or update adapter artifacts**
   - Trigger phrases: `adapter JAR`, `driver JAR`, `BucketFS`, `JAVA ADAPTER SCRIPT`, `deploy adapter`
   - Load: `references/adapter-development.md`

4. **Validate and debug adapter behavior**
   - Trigger phrases: `EXPLAIN VIRTUAL`, `connection validation`, `remote debugging for virtual schema adapters`, `pushdown debugging`, `adapter-side issue`
   - Load: `references/adapter-development.md`

## Notes

- Use this skill when the work is about adapter code, packaging, installation, or adapter-side debugging.
- Use **exasol-jdbc-virtual-schemas** or **exasol-document-virtual-schemas** when the user only needs to create, refresh, or query an existing virtual schema.
- Use **exasol-extension-catalog** first when the user is still choosing which existing adapter family or maintained extension to use.
- Use **exasol-bucketfs** if the task is specifically about generic BucketFS file management outside the adapter deployment flow.
