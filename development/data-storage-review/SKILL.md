---
name: data-storage-review
description: Review a repository or local folder with a focus on how data is stored, retrieved, transformed, retained, and protected. Use when Codex needs to inspect databases, files, object stores, caches, queues, schemas, persistence layers, migrations, or storage-related trust boundaries, risks, and architectural assumptions.
---

# Data Storage Review

## Overview

Use this skill to build a focused, evidence-based review of how a codebase stores and manages data. Trace what data is persisted, where it lives, how it is structured, how it is accessed, and which components are trusted to read, write, migrate, cache, or delete it.

Prefer one concrete storage path or subsystem over a broad but shallow survey. Make uncertainty explicit and label inferred edges clearly.

## Workflow

### 1. Establish the review scope

Choose the smallest meaningful storage slice before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious storage entrypoints such as ORM setup, repositories, model definitions, migrations, schema files, storage clients, file writes, cache configuration, queue consumers, or data export jobs

If the folder or codebase is large, choose one of these scopes and say which one you chose:

- one request or job path that persists data
- one database or schema area
- one file or object storage integration
- one caching or queue-backed subsystem

### 2. Identify storage boundaries

Identify the main storage systems and trust boundaries:

- relational databases, document stores, key-value stores, search indexes, graph stores
- local files, shared volumes, object stores, blob stores, backups, exports
- caches, session stores, queue backlogs, event logs
- migrations, seeders, retention jobs, archival paths, restore paths
- secrets, encryption keys, credentials, and privileged storage access

Prefer code search over assumptions. Follow concrete configuration, client initialization, repository wiring, and persistence call sites.

### 3. Trace the primary storage path

Trace data from input to durable or semi-durable storage and back out again. Look for:

- inbound data sources
- validation and normalization before persistence
- serialization, mapping, and schema translation
- write paths, update paths, and delete paths
- retrieval, hydration, filtering, and projection
- caching, replication, backup, export, and retention behavior
- cleanup, expiry, compaction, or migration paths

Capture where data changes format, ownership, or trust level.

### 4. Review the key functions

For every important function in the chosen flow, review the function instead of only naming it. Capture:

- file path
- function or method name
- role in the storage flow
- direct callers and important callees, if visible
- expected inputs
- written, returned, or deleted data
- validation, normalization, or sanitization performed
- state changes or side effects
- failure modes, consistency assumptions, and security concerns

Prioritize functions that:

- define schemas or data models
- open storage connections or clients
- perform writes, deletes, upserts, or bulk imports
- materialize caches or derive secondary indexes
- move data across trust boundaries or storage tiers
- bypass usual persistence abstractions

### 5. Surface storage findings

Call out issues that materially affect how much the storage design can be trusted, especially:

- missing validation before persistence
- inconsistent schema handling or weak migrations
- unsafe file paths, object keys, or bucket selection
- hidden writes, surprising fan-out, or shared mutable state
- missing transactions, rollback gaps, or partial-write risks
- unbounded retention, weak deletion semantics, or unclear archival behavior
- sensitive data stored without sufficient protection
- excessive trust in cached or replicated data
- backup, restore, or export paths that bypass normal safeguards
- storage credentials, privileged access, or encryption assumptions that are easy to miss

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. High-level storage flow
3. Step-by-step function review
4. Findings and open questions

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for storage signals such as `model`, `schema`, `migration`, `repository`, `dao`, `orm`, `sql`, `query`, `insert`, `update`, `delete`, `upsert`, `transaction`, `commit`, `rollback`, `redis`, `cache`, `bucket`, `blob`, `s3`, `gcs`, `file`, `write`, `read`, `persist`, `storage`
- framework-specific files such as `models`, `entities`, `migrations`, `repositories`, `db`, `storage`, `cache`, `seeds`, `prisma`, `typeorm`, `sequelize`, `alembic`, `django`, `hibernate`

Prioritize these signals:

- files where data first becomes durable
- functions that translate in-memory data into stored form
- code that deletes, archives, expires, or replicates stored data
- code that handles sensitive, high-volume, or cross-system data

## Output Rules

Be explicit about evidence quality:

- say `confirmed` when the code directly shows the path
- say `inferred` when the path is likely but not fully wired in the inspected files
- say `not verified` when an external service, generated layer, or managed storage system is missing

Do not present general business logic concerns as storage findings unless they affect persistence, integrity, confidentiality, availability, or retention.

When presenting the flow, prefer real functions and files over generic labels like "data layer".

## Example Requests

- Review this repo and explain how customer data is stored and retrieved.
- Inspect this codebase and map the write path from API request to database and cache.
- Review this folder with a focus on file storage, object storage, and retention behavior.
- Trace how this background job persists derived data and call out consistency or storage risks.
