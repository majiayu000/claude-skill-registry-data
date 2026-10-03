---
name: yq-windows-trash-cleaner
description: Windows C盘、项目垃圾、Docker/WSL、Git worktree、CodeGraph、Agent 会话或内存异常需要安全审计、清理和验证时使用。
compatibility: Windows 10 or Windows 11 x64 with PowerShell 5.1 or newer. Optional Git, Docker, WSL, package-manager, and CodeGraph checks run only when those tools or artifacts exist.
---

# YQ Windows Trash Cleaner

Run an evidence-first Windows maintenance workflow that is safe to invoke at any time and is not tied to one project, drive, application, or prior incident.

## Route the request

Distinguish storage from RAM before collecting data:

- Storage intent: C drive/full disk, rapid GB growth, caches, projects, worktrees, Docker/WSL images, backups, sessions, compression, or cleanup.
- RAM intent: processes consuming memory, paged/nonpaged pool, pool tags, startup storms, long-running workload growth, Fast Startup, or suspected leaks.
- Mixed intent: run the storage and memory tracks separately and reconcile them only in the final report.

Classify authorization:

- `AUDIT_ONLY`: inspect and report. Phrases such as “哪些可以删” do not authorize deletion.
- `PLAN_ONLY`: produce exact manifest IDs, commands, recovery, and predicted impact without changing state.
- `APPLY_APPROVED`: execute only the candidate IDs the user explicitly approved or an exact safe-clean scope the user explicitly requested after seeing the classification.

Scanning is always read-only. A report, HTML button, color, ignored status, or large size is never authorization.

## Safety contract

Protect user work before reclaiming space:

- Never delete documents, downloads, sessions, databases, credentials, models, evidence, backups, dirty/unmerged worktrees, release artifacts, Docker volumes, system files, or unknown directories by category name alone.
- Do not run whole-repository `git clean -fdX`, blanket `docker volume prune`, or raw recursive worktree deletion.
- Do not hand-delete WinSxS, DriverStore, Windows Installer, pagefile, hiberfil, recovery data, or VSS data.
- Do not follow reparse points while measuring or deleting. Resolve every target and reject a target equal to an approved root, outside it, or sharing only a text prefix.
- Keep active projects protected. Read repository instructions and current-state documents; check Git state, worktrees, running processes, locks, manifests, lockfiles, evidence paths, and regeneration commands.
- Prefer semantic maintenance: package-manager prune commands, `git worktree remove`, Docker object IDs, official DISM analysis/cleanup, transactional SQLite maintenance, or moving a review item to the Recycle Bin.
- Hard deletion is off by default. It requires a fresh explicit decision, exact paths/IDs, full preflight, and an action log.

## Run layout

Create a timestamped run directory outside all scanned or cleaned targets:

```text
run/
  scope.json
  baseline/
  projects/projects.json
  storage/storage.json
  memory/
  cleanup-manifest.json
  changes/action-log.jsonl
  verification/
  report.html
  final-report.md
```

Record timestamps, boot time, scan roots, excluded roots, access failures, commands and exit codes, tool availability, free bytes, and whether sizes are logical, allocated, compressed, sparse, or unknown.

## Whole-computer storage workflow

### 1. Establish current volume state and historical delta

Enumerate fixed volumes, capacity, filesystem, free bytes, BitLocker visibility when available, and prior trustworthy snapshots. Do not call normal variation “rapid growth” without a before/after delta.

Run `scripts/Get-ComputerProjectInventory.ps1` with explicit scan roots. Start with every known development root, registered Git worktree root, user Documents/Desktop, temporary development roots, and additional fixed-volume workspace roots. Avoid broad Windows and application-install roots unless the evidence points there.

For one repository or a small set of known repositories, run `scripts/Get-ProjectCleanupAudit.ps1` first. It adds `git clean -ndX` and `git clean -nd` previews, release/evidence summaries, active-owner evidence without exporting command lines, and explicit `review_required_ignored_paths`. This is still an audit: it never deletes or stops processes. Read [project-cleanup-classification.md](references/project-cleanup-classification.md).

Run `scripts/Get-ComputerStorageInventory.ps1` for system and user storage candidates. Use `scripts/Measure-PathUsage.ps1` for exact follow-up measurements. Record inaccessible trees instead of silently treating them as zero.

Default root discovery is heuristic, not proof of complete-computer coverage. For a whole-computer claim, explicitly enumerate all fixed volumes, known workspace roots, and every path returned by `git worktree list --porcelain`; list excluded and inaccessible roots in the report.

### 2. Inventory every project semantically

For each discovered Git repository, worktree, or manifest-backed project, record:

- canonical root, remote/default branch, branch/HEAD, dirty and untracked state;
- registered worktrees and whether each HEAD is contained in the verified remote default branch;
- active process command lines that point inside the root;
- project instructions and current-state/evidence documents;
- manifests and lockfiles that prove a cache can be rebuilt;
- generated candidates such as `node_modules`, `.venv`, `target`, `.next`, test caches, browser output, CodeGraph databases, and build directories;
- ambiguous data such as `output`, `dist`, `release`, datasets, models, reports, validation runs, and agent context.

Do not infer that `dist`, `build`, `output`, `.runtime`, `.codex`, `.claude`, or `.codegraph` is disposable. Classify their contents and role first. Read [whole-computer-project-audit.md](references/whole-computer-project-audit.md).

### 3. Inventory cross-project and application storage

Inspect, when present:

- npm, pnpm, yarn, Bun, pip, uv, Cargo, NuGet, Gradle, Maven, browser, model, and updater caches;
- Codex/Claude/other agent sessions, runtimes, plugins, managed caches, and worktrees;
- Docker logical objects separately from VHDX physical allocation;
- WSL distributions and VHDX files;
- Temp, Recycle Bin, WER/dumps, update delivery, driver installers, application backups, and databases;
- pagefile, hiberfil, component store, DriverStore, Installer cache, Reserved Storage, VSS, and restore points as system-managed or official-tool-only categories.

Use package managers' own inventory/prune operations. A cache's total size is an upper bound, not guaranteed reclaimable space. Read [storage-classification.md](references/storage-classification.md) and [docker-storage.md](references/docker-storage.md).

### 4. Classify decisions, not just directories

Use stable machine classes; colors may mirror them in the human report but never grant permission:

- `SAFE_REBUILDABLE`: exact generated object with a proven regeneration path, inactive owner, contained target, and no evidence/user data.
- `REVIEW_REQUIRED`: useful history, project dependencies, clean but unverified clones, backups, sessions, installers, downloads, models, inactive Docker objects, or anything with judgement cost.
- `KEEP_USER_OR_EVIDENCE`: source, dirty work, current/archived evidence, databases, restore volumes, current sessions, and unknown ownership.
- `SYSTEM_MANAGED_DO_NOT_DELETE`: protected Windows files, component/installer/driver/recovery stores, or storage whose official analysis is unavailable.
- `ADMIN_EVIDENCE_REQUIRED`: DISM, VSS, restore-point, Reserved Storage, VHDX compaction, or other facts not visible without elevation.

The detailed deletion gates are also summarized in [cleanup-classification.md](references/cleanup-classification.md).

Every candidate needs a confidence level, current bytes, owner, activity check, deletion impact, recovery/regeneration, exact action, expected verification, and approval state.

### 5. Produce both JSON and a local report

Keep scan data separate from analysis. Generate a local static report with `scripts/New-StorageAuditReport.ps1` after classifications are present. Use this reading order:

1. volume overview and coverage gaps;
2. top space consumers;
3. recommended priority;
4. candidates by class;
5. retained risks and long-term prevention.

The report may contain private project names and absolute paths. Keep it local by default and redact before sharing. It must not expose direct hard-delete controls. The report information architecture has documented design provenance; see [design-provenance.md](references/design-provenance.md).

## Manifest and controlled execution

Create `cleanup-manifest.json` before any state change:

```json
{
  "id": "project-cache-001",
  "class": "SAFE_REBUILDABLE",
  "action": "pnpm-store-prune",
  "target": "C:\\absolute\\path-or-object-id",
  "expected_command_path": "C:\\absolute\\path\\to\\pnpm.cmd",
  "bytes": 123,
  "owner": "tool-or-project",
  "preconditions": ["path-contained", "size-rechecked", "owner-inactive"],
  "recovery": "documented regeneration command",
  "approved": false
}
```

Before applying an approved item:

1. Resolve and contain the exact target; reject reparse escapes.
2. Recheck size, owner, Git state, process state, and other drift fields.
3. Confirm the action type is compatible with the class.
4. Capture the pre-action free bytes and relevant backup/status evidence.
5. Execute only this ID. Stop on drift or unexpected output; never widen scope.
6. Record exit status, released bytes, recovery status, and post-action verification.

For the built-in semantic allowlist, run `scripts/Invoke-ApprovedCleanupManifest.ps1` first without `-Apply` and pass the exact `-ApprovedId` values. Record its `PreflightToken`. Apply only after the entire batch passes, using the same manifest and IDs plus `-Apply -PreflightToken <token>`; the executor reruns all preflights and rejects a stale token before the first mutation. Package actions must bind `target` to the cache path reported by the owning tool and bind `expected_command_path` to the reviewed `.exe` or `.cmd`. The executor intentionally rejects arbitrary commands, raw recursive deletion, string booleans, unapproved items, non-`SAFE_REBUILDABLE` classes, active or ambiguous owners, reparse paths, and unverified worktrees. Unsupported actions remain manual review items; never broaden the script's allowlist during a cleanup run merely to make an item pass.

For multiple IDs, complete preflight for the entire batch before the first mutation, then execute in smallest-risk order. A failed later item does not make earlier actions transactional; the action log must say exactly what happened.

## Special storage rules

### Docker and WSL

Run `scripts/Get-DockerStorageAudit.ps1`. Keep logical objects separate from VHDX physical storage. Do not start an auto-restarting container fleet only to obtain inventory without considering impact. VHDX compaction requires a current logical inventory, all consumers stopped, `wsl --shutdown`, detached/no-handle proof, and administrator access. Never promise the arithmetic sparse difference. Read [docker-storage.md](references/docker-storage.md).

### Git worktrees and temporary clones

A worktree becomes eligible only when it is registered, clean including untracked files, inactive, and its HEAD is contained in the verified remote default branch. Remove it with `git worktree remove`, then prune metadata. A standalone temporary clone also needs clean status and remote containment; prefer recoverable removal when value is uncertain.

### CodeGraph

Treat `.codegraph` as rebuildable only after verifying it is an index, not project evidence, and that the project has no active indexing transaction. Separate the main database from WAL/SHM. Prefer fixing `codegraph.json` exclusions and rebuilding rather than repeatedly deleting a growing WAL. Exclusions change semantic search coverage, not project build inputs, unless project code explicitly reads that configuration.

### Sessions, backups, databases, and models

Retain by default. Consider transparent compression or retention review before deletion. Database maintenance requires owner shutdown, a verified recovery copy, integrity checks, transactional changes, and post-checks. Keep at least one current backup and one pre-maintenance recovery point unless the user approves a different retention policy.

## Memory workflow

Run `scripts/Collect-WindowsHealthSnapshot.ps1` at clean login, during representative workload, after it ends, and at long-run milestones. Separate processes, paged/nonpaged kernel pool, pool tags, cache/standby, and pagefile. Never join trends across different boot times.

Use `scripts/Get-LongRunMemoryAssessment.ps1` and these outcome labels:

- `VERIFIED_FIXED`: representative workload plus valid 48-hour same-boot coverage, no warning/critical sample, no sustained pool growth, and functional gates pass.
- `HEALTHY_SO_FAR_PENDING_LONG_RUN`: healthy evidence but less than 48 hours or incomplete representative workload.
- `ROOT_CAUSE_NOT_PROVEN`: abnormal growth exists but no reproducible component/driver A/B proves ownership.
- `WARNING_REVIEW_REQUIRED`: thresholds or sustained growth are exceeded.
- `ROLLBACK_REQUIRED`: a change caused functional or event-log regression.

Fast Startup affects shutdown plus power-on, not Restart. It can preserve a leaking kernel session but does not create the leak. Restore it only after 24/48-hour stability evidence and an explicit experience tradeoff. Do not disable Defender, storage, network, audio, graphics, or other drivers from one sample or a tag-name association. Read [memory-diagnosis.md](references/memory-diagnosis.md) and [quality-gates.md](references/quality-gates.md).

## Verification and outcome

Measure actual volume free-byte change; do not sum candidate logical sizes as released bytes. Re-run affected project status, worktree lists, package/cache status, Docker/WSL inventory, database checks, and application smoke tests. For system changes, verify networking/VPN, audio/microphone, OneDrive, input/Fn controls, search, and touched vendor software.

Lead with the outcome and use these sections:

- Verified facts
- Cleanup actions taken
- Actual released bytes
- Retained and protected items
- Unverified/admin-blocked items
- Rollback or regeneration
- Next maintenance milestone

Never call an audit a cleanup, a candidate size released space, or healthy current memory a proven root-cause fix.
