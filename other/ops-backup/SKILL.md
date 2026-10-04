---
name: ops-backup
description: Set up or execute backup + restore procedures for AICP/fleet runtime state — `~/.aicp/` (DLQ + history + state.yaml), config YAMLs, KB Collections, model GGUF inventory, sister-project Plane DBs. Authors backup scripts, runs them, verifies integrity, documents restore, tests restore in a safe environment. Loads when the operator says "back up X", "set up backups", "restore from backup", "what if we lose Y".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# ops-backup

The operations skill that authors and exercises backup + restore procedures. AICP-specific scope: runtime state lives in files (no SQL DB), so backups are filesystem-based — but the procedures must be testable, reproducible, and gated on integrity verification.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No backup procedure exists**: project has no documented backup, no `make backup` target, no scheduled snapshot.
- **Direct verb**: operator says "back up X", "set up backups", "restore from backup", "what if we lose Y".
- **Disaster scenario**: just had a near-miss (disk filling, accidental delete) and operator wants the safety net before next time.
- **Migration prep**: about to move data between hosts/disks; need a restore-able snapshot to fall back to.

Do NOT load when:

- Backup exists; you're running an ad-hoc backup — just run the existing `make backup` (no skill needed).
- The ask is "save my git work" — that's `git push`, not backup.
- The ask is to migrate to a new disk — load `infra-storage` (storage migration) which uses backup as one step.
- Operator wants point-in-time DB restore (AICP has no SQL DB) — flag the mismatch and clarify what they actually want.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Identify backup scope

**Trigger**: skill loaded.

**Process**:

1. Read [docs/architecture/post-anthropic-mission.md](../../../docs/architecture/post-anthropic-mission.md) (or equivalent) to understand what state matters. AICP-domain canonical scope:
   - **Runtime state**: `~/.aicp/dlq/`, `~/.aicp/history/`, `.aicp/state.yaml` (workflow task pointer).
   - **Config YAMLs**: `config/default.yaml`, `config/profiles/*.yaml`, `config/models/*.yaml` — already in git, but a snapshot is useful for "what config did I run on date X" questions.
   - **KB Collections**: LocalAI Collections at `localhost:8090/app/collections` (chromem-backed). Backed up via LocalAI's own export endpoint OR by snapshotting the `models/collections/` directory.
   - **Model GGUF inventory**: NOT the weights themselves (large; redownloadable from HF) — the inventory manifest at `/mnt/models/.inventory.json`.
   - **Sister projects**: Plane DB (Postgres, has its own backup tool), OpenFleet board state (`openfleet/board.json`).
2. Categorize by criticality:
   - **Critical** (lose = lose work): DLQ, history, state.yaml, Plane DB.
   - **Reproducible** (regenerable): KB Collections (re-sync from `docs/kb/`), model weights (re-download).
   - **Versioned** (in git): config YAMLs, code.
3. Decide cadence per category. Critical → daily snapshot, retain 7 days + monthly retention. Reproducible → weekly. Versioned → no extra backup beyond git.
4. Decide destination. AICP storage tiers (per [docs/STORAGE.md](../../../docs/STORAGE.md)): T2 archive (`/mnt/f/Backups/...`) is the canonical backup target. Don't put backups on the same disk as the source.

**Quality bar (Operation 1 done when)**:

- [ ] All state surfaces enumerated (no implicit "and other stuff").
- [ ] Each surface categorized as critical / reproducible / versioned.
- [ ] Cadence + retention decided per category.
- [ ] Destination on a different physical disk from source (T2 archive, not the same NVMe).

### Operation 2: Author backup script

**Trigger**: Operation 1 scope confirmed.

**Process**:

1. Author `scripts/backup.sh` (or equivalent). AICP-domain template:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   TS=$(date -u +%Y%m%dT%H%M%SZ)
   DEST="/mnt/f/Backups/aicp/${TS}"
   mkdir -p "${DEST}"

   # Critical state
   tar -czf "${DEST}/aicp-state.tar.gz" -C "${HOME}" .aicp/dlq .aicp/history .aicp/state.yaml 2>/dev/null || true
   cp -p .aicp/state.yaml "${DEST}/state.yaml" 2>/dev/null || true

   # Config snapshot (separate from git for "what was running" point-in-time)
   tar -czf "${DEST}/config.tar.gz" config/

   # KB Collections via LocalAI export
   curl -sS -m 30 -o "${DEST}/kb-collections.json" http://localhost:8090/app/collections/aicp-kb/export || echo "(KB export skipped — LocalAI not reachable)"

   # Inventory manifest
   cp -p /mnt/models/.inventory.json "${DEST}/inventory.json" 2>/dev/null || true

   # Integrity manifest
   (cd "${DEST}" && sha256sum *.tar.gz *.json *.yaml 2>/dev/null > MANIFEST.sha256)

   # Retention prune (keep last 7 days)
   find /mnt/f/Backups/aicp -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

   echo "Backup complete: ${DEST}"
   ```
2. Add Makefile target:
   ```make
   backup:        ; bash scripts/backup.sh
   backup-list:   ; ls -lh /mnt/f/Backups/aicp/ | tail -10
   ```
3. Author a verification step inside the script: every tarball gets a `sha256sum` line in `MANIFEST.sha256`. Restore relies on this manifest to confirm no corruption.
4. Don't include weights or other regenerable data — bloats the backup, slows the cycle.
5. For Plane / external services: document HOW to back them up (their own tooling), not WHAT to back up (out of AICP scope to actually invoke).

**Quality bar (Operation 2 done when)**:

- [ ] Backup script exists, exits 0 on a successful run.
- [ ] Critical state captured in tarballs.
- [ ] SHA256 manifest generated alongside tarballs.
- [ ] Retention prune logic present (don't fill T2 indefinitely).
- [ ] Makefile target wraps the script.
- [ ] No weights / regenerable data included.

### Operation 3: Document + test restore

**Trigger**: Operation 2 backup script runs cleanly.

**Process**:

1. Author `docs/restore.md` with explicit step-by-step:
   ```markdown
   # AICP Restore Procedure

   ## Prerequisites
   - Backup directory at `/mnt/f/Backups/aicp/<TS>/` exists.
   - LocalAI running (for KB re-import).

   ## Steps
   1. Verify integrity:
      cd /mnt/f/Backups/aicp/<TS> && sha256sum -c MANIFEST.sha256
   2. Restore runtime state:
      tar -xzf aicp-state.tar.gz -C ~
   3. Restore config snapshot (only if reverting to a known-good config):
      tar -xzf config.tar.gz -C <repo-root>
   4. Re-import KB Collections:
      curl -X POST -d @kb-collections.json http://localhost:8090/app/collections/aicp-kb/import
   5. Verify:
      aicp --check
      aicp --dlq-status
   ```
2. **Test the restore** in a safe environment:
   ```bash
   # Use a tmp HOME to avoid clobbering your real ~/.aicp
   mkdir -p /tmp/restore-test
   HOME=/tmp/restore-test bash -c 'tar -xzf /mnt/f/Backups/aicp/<latest>/aicp-state.tar.gz -C $HOME'
   ls /tmp/restore-test/.aicp/   # should show dlq/, history/, state.yaml
   ```
3. Run an end-to-end drill once at setup time: take a backup → wipe a non-critical file from `~/.aicp/history/` → restore → verify the file is back.
4. Schedule the backup. Per CLAUDE.md "IaC only" — use cron or systemd timer, not "remember to run it":
   ```
   # crontab
   0 3 * * * /home/jfortin/devops-expert-local-ai/scripts/backup.sh >> ~/.aicp/logs/backup.log 2>&1
   ```

**Quality bar (Operation 3 done when)**:

- [ ] `docs/restore.md` exists with explicit step-by-step.
- [ ] Restore drill done at least once; succeeded.
- [ ] Backup scheduled (cron / timer / similar) — not relying on operator memory.
- [ ] Restore script verifies integrity (sha256) BEFORE applying.

### Operation 4: Document the safety contract

**Trigger**: Operation 3 verifications pass.

**Process**:

1. Document in README or `docs/operations.md`:
   - What's backed up, what isn't, what the cadence is.
   - Where backups live.
   - Recovery time objective (RTO): how long restore takes (drill data).
   - Recovery point objective (RPO): max data loss in a worst-case (cadence-bounded).
2. Note explicit gaps: "Plane DB is backed up by Plane's own tool, not by this script — see openfleet/plane-backup.md."
3. Suggest the next skill if applicable: `incident-cycle` (if backup was set up reactively to an incident), `infra-monitoring` (alert if backups stop running).

**Quality bar (Operation 4 done when)**:

- [ ] Documented: scope, cadence, location, RTO, RPO.
- [ ] Gaps explicit (what we DON'T back up, with reason).
- [ ] Next-step skill suggested.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Backups on the same disk

`backup.sh` writes to `/home/jfortin/.aicp-backup/` — same NVMe as `~/.aicp/`. Disk fails; both source and backup are gone.

**The rule**: backups go to a DIFFERENT physical disk. AICP-domain canonical: `/mnt/f/Backups/` (T2 USB archive). Verify with `df` that source and dest are different filesystems.

### Gotcha 2: No integrity verification

Tarball gets corrupted mid-write (disk full, process killed). Backup directory has the file; no manifest. Three months later operator restores; tarball is unreadable. Discovered when it matters.

**The rule**: every backup writes a SHA256 manifest. Restore script ALWAYS verifies BEFORE applying. If checksum fails, restore aborts; operator knows the backup is bad and falls back to an earlier one.

### Gotcha 3: Untested restore = no backup

Backup runs nightly for 6 months. Operator has never tested restore. Disaster strikes; restore fails because the format changed, the path is wrong, the LocalAI endpoint moved. Operator has 6 months of "backups" that don't work.

**The rule**: drill the restore at setup time, then every quarter. Schedule a `make restore-drill` that tests against a tmp dir. If that ever fails, the backup is broken — fix before the next critical loss.

### Gotcha 4: Backing up regenerable data

Backup includes `/mnt/models/*.gguf` (318GB of K2.6 weights). Each backup takes 60+ minutes and 318GB of T2 space. After a week, T2 is full of redundant copies of the same weights.

**The rule**: don't back up what you can re-download or re-generate. Weights → no. Configs (in git) → no (separate snapshot is for point-in-time, not loss recovery). KB Collections → yes (cheap to back up; expensive to re-sync). Runtime state → yes (operator-specific, irreplaceable).

### Gotcha 5: No retention prune

Backups accumulate forever. T2 fills up. Future backups silently fail (no space) but errors go to a log nobody reads.

**The rule**: every backup script has retention logic — keep N daily, M weekly, K monthly. AICP-domain default: 7 daily + 4 weekly. Manual prune doesn't scale; bake it in.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP-specific runtime state surfaces (per [docs/architecture/intelligent-infrastructure.md](../../../docs/architecture/intelligent-infrastructure.md)):

- DLQ at `~/.aicp/dlq/<UTC-date>.jsonl` (per-day JSONL retry queue).
- History at `~/.aicp/history/` (one JSON per task).
- Workflow state at `.aicp/state.yaml` (active task pointer).

Backup destination per [docs/STORAGE.md](../../../docs/STORAGE.md): T2 archive on USB drive (`/mnt/f/Backups/`).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| ops-rollback | Roll back a deployment to last-good | Rollback is for deployment artifacts; backup is for state |
| infra-storage | Migrate state to a new disk | Storage migration uses backup as one step; this skill is the backup itself |
| ops-incident | Active incident with potential data loss | Incident response may invoke restore; this skill is the procedure |
| infra-monitoring | Alert if backups stop running | Adds monitoring; this skill creates the backup |
| ops-maintenance | Routine ops including backup verification | Broader scope; backup is one of several routine items |
