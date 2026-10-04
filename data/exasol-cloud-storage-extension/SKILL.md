---
name: exasol-cloud-storage-extension
description: "Use Exasol Cloud Storage Extension workflows for moving structured object-storage files through extension UDFs. Covers setup prerequisites, the fixed `CLOUD_STORAGE_EXTENSION.IMPORT_PATH` and `CLOUD_STORAGE_EXTENSION.EXPORT_PATH` entrypoints used with `FROM SCRIPT` and `INTO SCRIPT`, Parquet, Avro, ORC, and Delta files on S3, Google Cloud Storage, Azure Blob Storage, Azure Data Lake, HDFS, and Alluxio, connection-object credential patterns, and routing away from native IMPORT or EXPORT when the extension path is the right fit."
---

# Exasol Cloud Storage Extension Skill

Trigger when the user mentions **Cloud Storage Extension**, **FROM SCRIPT CLOUD_STORAGE_EXTENSION**, **INTO SCRIPT CLOUD_STORAGE_EXTENSION**, **CLOUD_STORAGE_EXTENSION.IMPORT_PATH**, **CLOUD_STORAGE_EXTENSION.EXPORT_PATH**, **Avro/ORC/Delta object-storage import**, **extension-based object-storage loading**, **extension-based Parquet reader**, **Avro through Cloud Storage Extension**, **ORC through Cloud Storage Extension**, **Delta through Cloud Storage Extension**, **extension-based Parquet export**, or **extension-based file reader**.

## Routing Algorithm

1. **Object storage and file-reader extension workflows**
   - Trigger phrases: `Cloud Storage Extension`, `FROM SCRIPT CLOUD_STORAGE_EXTENSION`, `INTO SCRIPT CLOUD_STORAGE_EXTENSION`, `CLOUD_STORAGE_EXTENSION.IMPORT_PATH`, `CLOUD_STORAGE_EXTENSION.EXPORT_PATH`, `Avro from object storage`, `ORC from object storage`, `Delta from object storage`, `ORC from S3`, `Avro from S3`, `Delta from S3`, `extension-based object-storage loading`, `extension-based Parquet reader`, `ORC through Cloud Storage Extension`, `Avro through Cloud Storage Extension`, `Delta through Cloud Storage Extension`, `extension-based Parquet export`
   - Load: `references/cloud-storage-extension.md`

## Notes

- Use this skill when the user needs the Cloud Storage Extension UDF path rather than direct native `IMPORT` or `EXPORT`.
- Use **exasol-import** for direct local-file and native SQL import behavior.
- Use **exasol-export** for direct native SQL export behavior and local `exapump export`.
- Use **exasol-bucketfs** when the user needs to upload, list, or remove the extension JAR in BucketFS.
- Use **exasol-document-virtual-schemas** for federated read-only access to object or file storage.
- Use **exasol-extension-catalog** only when the user is still comparing federation, copy, connector, or extension families.
