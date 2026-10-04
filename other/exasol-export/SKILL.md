---
name: exasol-export
description: "Use Exasol `EXPORT` and `EXPORT INTO` SQL plus `exapump export` local file workflows for moving data out of Exasol. Covers native CSV/FBV export, local CSV/Parquet exports with exapump, `CREATE CONNECTION` connection objects for export, FTP, SFTP, HTTP, HTTPS, and cloud targets on S3, Azure Blob Storage, and Google Cloud Storage (GCS), reject limits, and export credential patterns."
---

# Exasol Export Skill

This skill covers only workflows that move data out of Exasol.

## Step 0: Establish Connection

Ensure a working `exapump` profile before giving terminal workflows that use
`exapump export`:

1. If the user names a profile, test it with `exapump sql --profile <name> "SELECT 1"`; always place `--profile` after the subcommand. Otherwise test the default profile with `exapump sql "SELECT 1"`.
2. On success, proceed — and keep the same `--profile <name>` after the subcommand on every later command, such as `exapump export --profile <name> --table <schema.table> --output <file> --format <format>`.
3. On failure, run `exapump profile list` to see which profiles exist.
4. If profiles exist, present them and ask which to use, then inspect that one with `exapump profile show <name>` — it masks credentials — to confirm the required fields are set. **Never read, `cat`, or print `~/.exapump/config.toml`; it stores credentials in clear text.** If a credential value does appear in any command output, do not repeat it in the conversation.
5. If no usable profile exists, have the user create one locally with `exapump profile add <name>` (omit `--password` and exapump prompts on a hidden line) or `exapump profile init`, then retry step 1. Never ask the user to paste a password into the conversation, and never pass one as a command-line argument.

Trigger when the user mentions **EXPORT**, **EXPORT INTO**, **export table**, **export local file**, **exapump export**, **export CSV**, **export Parquet**, **export to S3**, **export to Azure Blob**, **export to GCS**, **export to FTP**, **export to SFTP**, **export to HTTP**, **export to HTTPS**, **REJECT LIMIT** with export intent, or **CREATE CONNECTION** together with export target setup intent.

## Routing Algorithm

1. **Local files on the user machine**
   - Trigger phrases: `export local file`, `into local`, `to local`, `exapump export`
   - Load: `references/export.md`

2. **Remote or cloud files reachable by Exasol**
   - Trigger phrases: `EXPORT`, `EXPORT INTO`, `S3`, `Azure Blob`, `GCS`, `FTP`, `SFTP`, `HTTP`, `HTTPS`, `REJECT LIMIT`, `CREATE CONNECTION` with export target setup intent
   - Load: `references/export.md`

3. **Connection-object export setup**
   - Trigger phrases: `CREATE CONNECTION` with export target setup intent, `ALTER CONNECTION`, `temporary credentials`, `SESSION TOKEN`
   - Load: `references/export.md`

4. **Script-based export target**
   - Trigger phrases: `EXPORT INTO SCRIPT`, `export script`, `custom export script`
   - Load: `references/export.md`

## Notes

- Use this skill for direct data movement out of Exasol.
- Use **exasol-import** for native `IMPORT`, local upload workflows, Parquet import, reject handling, and staging-based loading into Exasol.
- Use **exasol-cloud-storage-extension** for explicit extension-based Parquet export. Use **exasol-extension-catalog** only when the user is still choosing among native export, extension, connector, or integration families.
