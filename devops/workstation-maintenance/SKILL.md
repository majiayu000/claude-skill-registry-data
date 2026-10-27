---
name: workstation-maintenance
description: Inventory and tidy local Windows drives without breaking anything. Use when asked to clean up or organize drives or folders, plan file moves in small approval batches, move cluttered top-level folders of a drive behind junctions, or undo an earlier move. The folders to protect come from the user's config.json; nothing moves without an approved batch ID and a rollback manifest.
license: Apache-2.0
---

# Workstation Maintenance

Use this skill to inventory Windows drives, propose file moves in small batches, move
only the batches the user approves, and roll them back on request. A second mode moves
cluttered top-level folders of a drive into `<drive>\_Organized\<Bucket>\_RootDirs\`
and leaves a junction at the old path, so existing absolute paths keep working.

## Setup: config.json

Everything specific to the machine lives in `config.json` next to this file. It is
git-ignored. If it is missing, copy `config.example.json`, ask the user which folders
must never move, and fill it in before any live run. A live inventory and the
drive-root scripts refuse to run without a config. `-ConfigPath` or
`$env:WORKSTATION_MAINTENANCE_CONFIG` can point at a config elsewhere. Paths may use
environment variables such as `%USERPROFILE%`.

| Key | Meaning |
| --- | --- |
| `protected_roots` | Never scanned, never moved, never a destination. |
| `infrastructure_roots` | Agent and tool installs. Recorded, never moved. |
| `project_roots` | Active project folders. Recorded, never moved. |
| `inventory_roots` | What to scan when `-Roots` is not given. |
| `organized_root` | Where file-level moves go when `-TargetRoot` is not given. |
| `coursework_patterns` | Extra filename regexes treated as coursework (kept in place). |
| `drive_root_rules` | `{ "pattern", "category" }` pairs: regexes on top-level folder names mapped to a drive-root bucket. |

Agent folders in the user profile (`.codex`, `.claude`, `.openhands`, opencode state)
are always treated as infrastructure.

## Hard boundaries

- Never move, delete, or open anything under a `protected_roots` entry, including when
  it is reached through a junction, symlink, relative path, or different casing.
- The Windows folder, Program Files, ProgramData, AppData, package caches, browser
  profiles, auth/session/db/log folders, git worktrees and reparse points are never moved.
- `infrastructure_roots` and `project_roots` stay in place unless the user asks for a
  migration of that one folder.
- Never delete files. At most, write a list of deletion candidates for the user.
- Classify by path and filename only. Do not open documents.
- No physical move without an inventory manifest, a move plan, a batch ID the user
  approved, and rollback data.

## Workflow

1. Preflight
   - Check that `config.json` exists and protects what the user cares about.
   - Note uncommitted changes in any repos under the roots and leave them alone.
2. Inventory
   - Run `scripts/New-WorkstationInventory.ps1`. Keep its JSON/Markdown output in a local
     folder that is not committed; it contains private filenames.
   - Confirm there are zero entries under protected roots and zero move-eligible
     reparse points, directories, or git worktrees.
3. Plan
   - Run `scripts/New-MovePlan.ps1` on the inventory manifest.
   - Executable batches include only low-risk files older than 30 days; newer ones are
     deferred so normal use is not disrupted.
   - Batches are grouped by file type and capped at 100 items, so the user approves
     small, understandable units. Duplicate destinations get a stable item-ID suffix.
   - For drive-root organization, run `scripts/New-DriveRootOrganizationPlan.ps1 -DriveRoot <drive>`
     instead. It classifies the immediate children of the drive only.
4. Approval gate
   - Stop before moving anything.
   - `scripts/New-ApprovalPacket.ps1` writes a summary of batch IDs, counts and sizes,
     without filenames. `scripts/Test-MovePlanBatches.ps1` preflights every batch.
   - Ask the user to approve batch IDs. If they approve all currently passing low-risk
     batches at once, run them without asking again for each one, stopping at the first failure.
   - Only then run `scripts/Invoke-ApprovedMoveBatch.ps1 -Approved` (or
     `Invoke-DriveRootOrganizationPlan.ps1 -Approved`).
5. Rollback and validation
   - Every applied batch writes an applied manifest with rollback fields.
   - Undo with `scripts/Invoke-RollbackBatch.ps1`, or
     `Invoke-DriveRootOrganizationPlan.ps1 -RollbackManifestPath <applied.json>`.
   - Run `scripts/Test-WorkstationMaintenance.ps1` after changing any script.
6. Report
   - Summarize what moved by bucket, count and size. Do not paste private filenames into
     chat logs, notes, or commits.

## Categories

`Protected-NoMove`, `AgentInfrastructure`, `ActiveProject`, `CourseworkArchive`,
`PersonalSensitive`, `MediaAssets`, `Downloads`, `TempCache`, `VendorSystemToolchain`,
`UnknownReview`. Drive-root buckets: `Downloads`, `Temp-Review`, `Media`, `Coursework`,
`Documents-Private`, `Games`, `Tools-Review`.

## Commands

Run from this folder. `powershell -NoProfile -ExecutionPolicy Bypass -File <script> ...`
works the same if the execution policy blocks `.\scripts\...`.

```powershell
$out = Join-Path $env:TEMP "workstation-maintenance"
.\scripts\New-WorkstationInventory.ps1 -OutputDir $out
.\scripts\New-MovePlan.ps1 -ManifestPath "<inventory.json>"
.\scripts\Test-MovePlanBatches.ps1 -MovePlanPath "<move-plan.json>"
.\scripts\New-ApprovalPacket.ps1 -MovePlanPath "<move-plan.json>"
```

`New-MovePlan.ps1` defaults to `-MinimumAgeDays 30 -MaxItemsPerBatch 100`. Lower the age
gate only when the user accepts the risk of moving recent files.

After the user names a batch ID:

```powershell
.\scripts\Invoke-ApprovedMoveBatch.ps1 -MovePlanPath "<move-plan.json>" -BatchId "batch-downloads-archives-old" -PreflightOnly
.\scripts\Invoke-ApprovedMoveBatch.ps1 -MovePlanPath "<move-plan.json>" -BatchId "batch-downloads-archives-old" -Approved
.\scripts\Invoke-RollbackBatch.ps1 -AppliedManifestPath "<applied-batch.json>"
```

Drive-root organization (`<drive>` is a drive root such as the one the user named):

```powershell
.\scripts\New-DriveRootOrganizationPlan.ps1 -DriveRoot "<drive>" -OutputDir $out
.\scripts\Invoke-DriveRootOrganizationPlan.ps1 -PlanPath "<drive-root-plan.json>" -PreflightOnly
.\scripts\Invoke-DriveRootOrganizationPlan.ps1 -PlanPath "<drive-root-plan.json>" -Approved -SkipIds @("dr_0016")
```

Folders that fail because of ACLs or open handles stay where they are: pass their IDs
through `-SkipIds`, report them, and retry after the lock is gone. Never leave a folder
half moved.

## References

- `references/safety-boundaries.md`
- `references/batch-move-workflow.md`
- `references/manifest-schema.md`
