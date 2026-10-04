---
name: exasol-bucketfs
description: "Exasol BucketFS file system management via the `exapump bucketfs` CLI. Covers listing, uploading, downloading, and deleting files and directories in BucketFS, the `bfsdefault` service and other bucket services, bucket structure, `bfs_*` profile settings, the `/buckets/<service>/<bucket>/<path>` UDF path, and staging JARs, models, and Script Language Containers for UDFs."
---

# Exasol BucketFS Skill

BucketFS is Exasol's synchronous distributed file system: whatever is written to
a bucket is replicated to every cluster node and mounted read-only inside UDFs
at `/buckets/<service>/<bucket>/<path>`. Replication takes time, and recognised
archives are extracted on top of it, so a fresh upload becomes usable only once
synchronisation finishes. This skill covers moving files in and out of BucketFS
and referencing them from scripts.

## Routing Algorithm

Choose the narrowest matching route. If several apply, load all matching
references before answering.

1. **Run a BucketFS operation** — list, upload, download, delete, or configure the connection
   - Trigger phrases: `exapump bucketfs`, `ls`, `cp`, `rm`, `upload`, `download`, `delete`, `--bfs-host`, `--bfs-bucket`, `bfs_write_password`, `config.toml`, `exapump profile add`
   - Load: `references/exapump-bucketfs-cli.md`

2. **Stage a file for a UDF or SLC** — JARs, pickled models, containers, and the SQL that points at them
   - Trigger phrases: `upload jar`, `%jar`, `upload model`, `load model in UDF`, `upload SLC`, `activate container`
   - Load: `references/bucketfs-udf-usage.md`

3. **Understand BucketFS itself** — services, buckets, path forms, replication, durability
   - Trigger phrases: `what is BucketFS`, `bfsdefault`, `service`, `bucket structure`, `replication`, `backup`, `atomic write`, `size limit`
   - Load: `references/bucketfs-concepts.md`

An upload for a UDF usually needs routes 1 and 2 together: the command form
comes from the CLI reference, the path spelling in the SQL from the usage
reference.

## Step 0: Establish Connection

Ensure a working exapump profile — BucketFS uses the profile's `bfs_*`
fields — before running any command:

1. If the user names a profile, test it with `exapump bucketfs ls --profile <name>`; always place `--profile` after the subcommand. Otherwise test the default profile with `exapump bucketfs ls`.
2. On success, proceed — and keep the same `--profile <name>` after the subcommand on every later command, such as `exapump bucketfs cp --profile <name> <local-file> <bucket-path>`.
3. On failure, run `exapump profile list` to see which profiles exist.
4. If profiles exist, present them and ask which to use, then inspect that one with `exapump profile show <name>` — it masks credentials — to confirm the required fields are set. **Never read, `cat`, or print `~/.exapump/config.toml`; it stores credentials in clear text.** If a credential value does appear in any command output, do not repeat it in the conversation.
5. If no usable profile exists, have the user create one locally with `exapump profile add <name>` (omit `--password` and exapump prompts on a hidden line) or `exapump profile init`, then retry step 1. Never ask the user to paste a password into the conversation, and never pass one as a command-line argument.

## Safety Rules

- Before `rm`, show the exact bucket, path, and profile, then obtain explicit
  confirmation. BucketFS is not part of database backups, so a deletion is not
  recoverable from a database restore.
- Before a `cp` that would overwrite an existing BucketFS or local file, inspect
  the target and obtain confirmation.
- Never print profile passwords or pass them as command-line arguments when a
  profile can hold them securely. Inspect a profile with
  `exapump profile show <name>`, never by reading `~/.exapump/config.toml`.

## Related Skills

- **exasol-udfs**: creating UDF scripts that read BucketFS files, and building the Script Language Containers staged here.
- **exasol-database**: SQL-level operations and database connectivity.
