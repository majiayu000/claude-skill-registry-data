---
name: infra-storage
description: Manage AICP's storage surfaces — model GGUF files (`models/` host volume mounted into LocalAI container), config YAMLs (`config/` source-controlled), runtime state (`~/.aicp/dlq/`, `~/.aicp/history/`, `.aicp/state.yaml`), KB vector store (LocalAI Collections at `localhost:8090/app/collections`), per-model prompt caches. AICP has no SQL database — storage is files + LocalAI Collections. Loads when the operator says "where does AICP store X" / "disk usage growing" / "back up state" / "move models to bigger disk" / "migrate to faster storage".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# infra-storage

Manage AICP's storage surfaces. AICP doesn't use a SQL database — storage
is a mix of:

1. **Model GGUF files** — `models/` directory on host, volume-mounted
   into the LocalAI container at `/models`. Largest disk consumer (4-30GB
   per model).
2. **Config YAMLs** — `config/` source-controlled, small.
3. **Runtime state** — `~/.aicp/` (gitignored): `dlq/<UTC-date>.jsonl`,
   `history/...jsonl`, `metrics/`, `prometheus_snapshot.json`, plus
   per-project `.aicp/state.yaml`.
4. **KB vector store** — LocalAI Collections at
   `localhost:8090/app/collections` (chromem-backed, persistent inside
   LocalAI container at `/app/collections`).
5. **Prompt caches** — per-model cache files inside LocalAI container
   (per `infra-cache` skill).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "where does AICP store X", "disk usage
  growing", "back up state", "move models to bigger disk", "migrate to
  faster storage"
- **Inventory**: post-incident audit of what disk AICP touches
- **Backup planning**: identifying backup-worthy state vs ephemeral state
- **Storage upgrade**: moving from one disk to another (e.g., HDD → SSD
  for model files)

Do NOT load when:

- The concern is the DLQ runtime ops (load `aicp-ops-dlq`)
- The concern is prompt cache tuning (load `infra-cache`)
- The concern is config schema (load `config-env`/`config-migrations`)

## Operations

### Operation 1 — Inventory storage surfaces and disk usage

**When**: pre-cleanup audit or storage upgrade planning.

**Process**:

1. Models: `du -sh models/` (host) — usually 5-50GB depending on count
2. Config: `du -sh config/` — small (kilobytes)
3. Runtime state: `du -sh ~/.aicp/` — DLQ + history + metrics
4. LocalAI Collections: `docker exec aicp-localai du -sh /app/collections`
   — KB embeddings + indices
5. Prompt caches inside container: `docker exec aicp-localai du -sh
   /tmp/cache` (or wherever prompt_cache_path resolves)
6. Build inventory table: surface × path × size × backup-worthy?

**Quality bar**: NEVER assume storage usage without measuring. Models
dominate disk; everything else is small in comparison.

### Operation 2 — Move model GGUFs to a different disk

**When**: host disk is full or operator wants faster I/O for model loading.

**Process**:

1. Identify source: `models/` (volume-mounted into container at `/models`)
2. Move data to new location:
   `mv models/ /new/disk/models/ && ln -s /new/disk/models models`
   (symlink preserves the relative path used by docker-compose.yaml)
3. OR: update `docker-compose.yaml` volume mount to point at new path
   directly (cleaner; symlink is the quick option)
4. Restart LocalAI: `docker compose restart localai`
5. Verify: `aicp --models list` shows all models still discoverable
6. If model load fails, the volume mount in docker-compose.yaml needs
   updating to the new path

**Quality bar**: NEVER `cp` then forget to delete the source — duplicates
silently waste disk. Use `mv` (or `cp` then verify, then `rm` source).

### Operation 3 — Back up runtime state

**When**: operator wants to preserve `~/.aicp/` before reformatting,
upgrading, or migrating to a new machine.

**Process**:

1. Identify backup-worthy:
   - `~/.aicp/dlq/` — failed tasks (re-runnable)
   - `~/.aicp/history/` — task history (audit trail)
   - `~/.aicp/metrics/`, `prometheus_snapshot.json` — metrics state
   - per-project `.aicp/state.yaml` (ephemeral, per-operator — usually
     not worth backing up)
2. Create archive: `tar czf aicp-state-$(date +%F).tar.gz ~/.aicp/`
3. Store off-machine (cloud sync, USB, etc.)
4. To restore: `tar xzf aicp-state-<date>.tar.gz -C /`

**Quality bar**: backup verifies restorability — test the restore on a
scratch machine before relying on the backup.

### Operation 4 — Migrate KB Collections to a different LocalAI instance

**When**: moving AICP from one LocalAI deployment to another (e.g., for
fleet rollout).

**Process**:

1. Source: KB collections live in LocalAI's `/app/collections` directory
2. Stop the source LocalAI: `docker compose stop localai`
3. Tar the collections: `docker run --rm -v aicp_localai_data:/data
   alpine tar czf - /data/collections > kb-snapshot.tar.gz`
4. On target host: extract into the target LocalAI's volume
5. Start target LocalAI; verify: `aicp --kb status` shows the same
   chunk count

**Quality bar**: KB migration is a STATEFUL operation — NEVER do it on
a running LocalAI (writes during the snapshot can corrupt the migrated
DB).

## Gotchas

- **Detection**: agent assumes AICP uses a SQL database.
  **Rule**: AICP has no SQL DB. Storage is files + LocalAI Collections.
  **Reasoning**: setting expectations correctly avoids wasted time
  searching for nonexistent migrations or schema files.

- **Detection**: agent treats `~/.aicp/` as project-state.
  **Rule**: `~/.aicp/` is OPERATOR-state (per-machine); per-project state
  lives in `<project>/.aicp/state.yaml`.
  **Reasoning**: backup scope differs — operator state is per-machine;
  per-project state is per-checkout (and gitignored).

- **Detection**: agent moves models with `cp` and forgets to delete source.
  **Rule**: use `mv` (atomic), or `cp + verify + rm`. Never leave
  duplicates.
  **Reasoning**: model files are 4-30GB each; duplicates silently consume
  disk.

- **Detection**: agent backs up KB collections from a running LocalAI.
  **Rule**: stop LocalAI before snapshotting Collections (or use the
  LocalAI export API if available).
  **Reasoning**: live snapshot of a write-active DB can produce a
  corrupted backup.

- **Detection**: agent thinks symlinking models will break the container.
  **Rule**: docker volume mounts follow symlinks; symlink is a valid
  quick relocate option. Updating docker-compose.yaml is cleaner long-term.
  **Reasoning**: volume mounts resolve through symlinks at mount time;
  this is well-supported.

## Reference exemplars

- `docker-compose.yaml` — `models/` volume mount (line ~XX, search for
  `volumes:`)
- `aicp/core/dlq.py` `_dlq_dir()` — `~/.aicp/dlq/` location
- `aicp/core/history.py` — `~/.aicp/history/` location
- `aicp/core/state.py` `STATE_DIR` — `<project>/.aicp/` location
- `wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md` —
  why per-day JSONL was chosen (operator-inspectable, no daemon)

## Domain context

AICP's storage strategy mirrors its operational philosophy: file-based
where reasonable (models, DLQ, history, config), service-managed where
necessary (LocalAI Collections for KB embeddings). Per CLAUDE.md
`## Tech Stack`, no SQL DB; storage is filesystem + LocalAI's
self-managed stores. This trades schema flexibility for operator
inspection (`cat`, `grep`, `du`).

## Related skills

| Skill | When to use |
|-------|-------------|
| `aicp-ops-dlq` | When the concern is DLQ runtime ops (CLI workflow) |
| `infra-cache` | When the concern is prompt/KV cache specifically |
| `ops-backup` | When the concern is backup procedure (broader than just identifying state) |
| `evolve-scale` | When migrating to fleet-scale storage |
| `infra-monitoring` | When alerting on disk usage growth |
