---
name: exasol-import
description: "Use Exasol `IMPORT` and `IMPORT INTO` SQL plus `exapump upload` local file workflows for moving data into Exasol. Covers CSV, FBV, and Parquet, `CREATE CONNECTION` connection objects for import, cloud credential patterns for S3, Azure Blob Storage, and Google Cloud Storage (GCS), reject handling, and staging-based import workflows. Native IMPORT does not read Avro, ORC, or Delta — those object-storage formats need the Cloud Storage Extension instead."
---

# Exasol Import Skill

This skill covers only workflows that move data into Exasol.

## Step 0: Establish Connection

Ensure a working `exapump` profile before giving terminal workflows that use
`exapump upload`:

1. If the user names a profile, test it with `exapump sql --profile <name> "SELECT 1"`; always place `--profile` after the subcommand. Otherwise test the default profile with `exapump sql "SELECT 1"`.
2. On success, proceed — and keep the same `--profile <name>` after the subcommand on every later command, such as `exapump upload --profile <name> <file> --table <schema.table>`.
3. On failure, run `exapump profile list` to see which profiles exist.
4. If profiles exist, present them and ask which to use, then inspect that one with `exapump profile show <name>` — it masks credentials — to confirm the required fields are set. **Never read, `cat`, or print `~/.exapump/config.toml`; it stores credentials in clear text.** If a credential value does appear in any command output, do not repeat it in the conversation.
5. If no usable profile exists, have the user create one locally with `exapump profile add <name>` (omit `--password` and exapump prompts on a hidden line) or `exapump profile init`, then retry step 1. Never ask the user to paste a password into the conversation, and never pass one as a command-line argument.

Trigger when the user mentions **IMPORT**, **IMPORT INTO**, **upload CSV**, **upload Parquet**, **local file load**, **exapump upload**, **S3 import**, **Azure Blob import**, **GCS import**, **Parquet import**, or **CREATE CONNECTION** together with import or object-store loading intent.

## Routing Algorithm

1. **Local files on the user machine**
   - Trigger phrases: `upload csv`, `upload parquet`, `exapump upload`, `from local`
   - Load: `references/import.md`

2. **Remote or cloud files reachable by Exasol**
   - Trigger phrases: `IMPORT`, `IMPORT INTO`, `S3`, `Azure Blob`, `GCS`, `FTP`, `SFTP`, `HTTP`, `HTTPS`, `CREATE CONNECTION` with import or object-store loading intent
   - Load: `references/import.md`

3. **Parquet-specific behavior**
   - Trigger phrases: `parquet`, `SOURCE COLUMN NAMES`, `SkipCols`, `MaxConnections`, `MaxConcurrentReads`
   - Load: `references/import.md`

## Notes

- Use this skill only for direct data movement into Exasol.
- Use **exasol-export** for native `EXPORT`, local export workflows, and `CREATE CONNECTION` questions tied to export target setup.
- Use **exasol-database** for general `CREATE CONNECTION` questions, SQL, schema inspection, and table design.
- Use **exasol-cloud-storage-extension** when the user explicitly wants extension-based object-storage loading. Use **exasol-document-virtual-schemas** for federated read-only object or file storage access or **exasol-jdbc-virtual-schemas** for federated read-only database access. Use **exasol-extension-catalog** only when the user is still choosing among those families.
