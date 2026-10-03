---
name: ls-context-index
description: Use when building, querying, or refreshing the LocalSetup context index with hybrid SQLite retrieval, deterministic freshness/worklist surfaces, and agent-preflight checks.
metadata:
  version: "0.1"
---

# Context Index

Use this skill for LocalSetup's file-retrieval cache and its separately owned, opt-in central memory. File search is derived from files and requires freshness checks; explicit memory records are authoritative, revisioned state with declared provenance.

## Required Agent Flow

1. Run `context-index agent-preflight --scope <scope>` or `context-index freshness --scope <scope>`.
2. If `read_direct_paths` is non-empty, read those files directly before trusting search results for those paths.
3. Use `context-index search "query" --scope repo --top-k 10` for fresh indexed context.
4. Use `lookup --chunk-id UUID` before relying on a specific result.
5. Use `worker nudge` or `refresh` when the worklist has pending items.
6. Use plan/apply operations only after reviewing the plan JSON and passing its returned `plan_id` to apply as `--plan "<REVIEWED_PLAN_ID>"`.

## Commands

```bash
localsetup context-index doctor
localsetup context-index agent-preflight --scope repo
localsetup context-index freshness --scope repo
localsetup context-index worklist --scope repo
localsetup context-index stats --scope repo
localsetup context-index ingest --scope repo
localsetup context-index search "how are workflows registered" --scope repo --top-k 10
localsetup context-index lookup --chunk-id UUID
localsetup context-index worker nudge --scope repo
localsetup context-index vector-rebuild plan --scope repo
localsetup context-index prune plan --scope repo
```

## Durable memory and replication

Run `context-index config init --scope repo` before memory operations: a repository-local stable `identity.memory_uuid` is required even when storage is global. Preserve that verified UUID in each replica's repository config; a newly generated UUID selects a different context, while copying another repo's UUID deliberately merges identities. Use `context-index memory record|update|delete|get|search|export|import --database global` for explicit source-grounded memory; see [README](README.md) for bounded stdin JSON/query and private snapshot commands. A record requires `content` and `source` with declared `type`, `ref`, and `sha256`; the caller must verify the claimed source before recording it. Update/delete require the current revision and preserve tombstones. Never infer memory from a file-index hit or treat an imported snapshot as an authenticated message. The central writer is mutable; imported replicas are read-only. Export/import transfers no data by itself: move private snapshots only after authorization of the exact destination and authenticated confidential transport. Snapshot hashes and bounded record lineage detect corruption/forks, not sender authenticity.

The default `local_hash` embedding downloads nothing but has limited semantic recall; memory search combines it with FTS. An explicitly configured loopback embedding service can improve retrieval, but remote content disclosure and model installation are outside this workflow. Derived index reset/rebuild/prune must not delete durable memory.

## Query Contract

Before retrieval, validate configuration and scope, confirm privacy exclusions are active, and interpret `safe_to_use_index`, `read_direct_paths`, and the worklist rather than relying on top-level `ok` alone. Search results must identify the selected scope/context, path, line range, chunk ID, source and chunk hashes, and freshness state. Use `lookup` and then read the source file directly before exact edits or citations.

## Refresh Contract

Choose lifecycle actions from observed freshness and worklist state: no work means no-op; changed or unindexed paths use refresh/worker execution; embedding-only drift uses vector rebuild; a contaminated or explicitly clean index uses rebuild; tombstoned sources use prune. `worker nudge` only queues eligible work. After any action, rerun preflight, freshness, or worklist and retain the input, selected action, command JSON, and verification JSON as decision evidence.

## Scope Model

- `repo`: repo-local docs, code, workflows, `.agentlens`, and selected structured files in the repo DB by default.
- `framework`: LocalSetup docs, skills, workflows, and generated catalogs in the global DB.

Derived index tables use UUIDv7 row IDs and context identity for scope separation. Durable memory uses its repository-local stable UUID in a separate context and separate tables, with a central writer identity, revision/sequence, per-record hash lineage, vector profile, and tombstones; read-only replicas import bounded snapshots without sharing a live SQLite database across hosts.

## Security Rules

Do not request secret values from the index or record them in memory. Default file inventory excludes `.env`, key, certificate, KeePass `.kdbx`, token, credential, secret-looking, log, cache, build, venv, and dependency folders. Explicit memory text and exported snapshots may themselves be private data: keep the central DB and snapshots owner-only, do not put content on argv or in logs, and do not send it to another server without exact authorization. Secret aliases intentionally present in documentation may be indexed, but resolved values must not be.

## Important Docs

- [README](README.md)
- [Architecture](docs/architecture.md)
- [Agent Usage](docs/agent-usage.md)
- [Security And Privacy](docs/security-and-privacy.md)
- [Platform Evaluation](docs/platform-evaluation.md)
- [Source Ledger](docs/source-ledger.md)
- [Config Schema](schemas/config.schema.json)
