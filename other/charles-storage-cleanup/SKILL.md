---
name: charles-storage-cleanup
description: Investigate Mac disk usage, find rarely used apps and overlooked storage, and clean authorized disposable caches, runtimes, devices, research artifacts, and development files while preserving active work.
---

# Storage Cleanup

Recover space from confirmed disposable artifacts, explain recent growth, and preserve active work. Measure success with free bytes on the actual data volume.

## Scope and authorization

When the request authorizes removing unused files, delete confirmed disposable candidates without repeated confirmation. An inventory-only request stays read-only. Skill discovery alone grants no deletion permission. Carry forward the user's selected items, exclusions, age limits, and recent-use conditions across passes; a request to inspect more locations does not revoke a previous keep instruction.

Keep active apps, builds, Git writers, and emulators running. Do not cancel a job to turn its files into deletion candidates. Preserve source, uncommitted work, credentials, unique research/media, current releases, and persistent VM/container data unless their removal is explicitly authorized. A generic request to clear unused files does not supply that authorization. An old modification time, ignored Git status, or absent open handle alone does not establish disposability. Skip uncertain candidates and continue useful cleanup elsewhere.

## Choose the depth

- For a named deletion, inspect that selection and its dependencies, then complete the authorized cleanup. A whole-app uninstall includes its own helpers and startup registrations; cache-only cleanup does not.
- For general cleanup, unused-app reviews, "what else," or "search more extensively," use [the discovery checklist](references/discovery.md). Cover installed software, both Library trees, hidden package stores, runtimes, developer/research output, devices, media/downloads, and OS-managed storage. Do not stop at the largest project or `~/Library/Caches`.
- When explaining a large folder, break it into source, generated output, installed environments, Git history, and unique assets. Describe what the largest payloads actually contain and why they exist before recommending removal.

## Workflow

1. **Baseline and map the machine.** Record local time, data-volume free bytes, recent cleanup receipts, mounts, and active work. Store audits privately outside repositories, under `~/Library/Logs/storage-cleanup/`. Start with filesystem-bounded directory sizes, including hidden directories and shared/system application data; deepen large branches with bounded probes.
2. **Cover overlooked families.** In a broad audit, work through the discovery checklist and record each family as measured, absent, excluded, or not fully inspected. Follow configured cache/SDK locations and sibling or agent workspaces. Revisit newly exposed smaller contributors after large removals. Previously deleted paths and old measurements are not new opportunities.
3. **Establish disposability and inactivity.** Identify reconstruction inputs, an obsolete duplicate, or a documented cache purpose. Distinguish the eligible subset from an entire installation or cache pool. Independently inspect relevant processes, arguments/cwd, open files, and running devices. Refresh checks before deletion. A failed or truncated usage probe leaves use unknown. Missing app-use metadata means unknown use.
4. **Remove in measured batches.** Log exact paths, sizes, reasons, reconstruction metadata, and methods. Prefer supported SDK/device/package-manager commands. For direct removal, validate the specific path, avoid symlink targets, and preserve nonstandard data or local patches. Name each target by its literal absolute path: agent safety checks refuse recursive removals built from shell variables, and an empty variable can widen one to a parent. Do not use blanket repository cleaning. Finish all eligible user-level work and prepare one reviewable exact batch before requesting necessary administrator authentication; verify the child job's result rather than only the authorization helper's exit status.
5. **Investigate recurrence.** If free space falls again, compare observations and trace writers. Repeated abandoned Git packs warrant checking background `git add` and generated payloads. Use a backed-up, scoped machine-local exclusion only for confirmed generated material; verify tracked files and useful new reports/scripts remain visible. Do not blindly copy another project's ignore patterns.
6. **Verify and report.** Check removed paths, retained active resources, unchanged dependency lockfiles, and readable Git commits where relevant. After runtime removal, verify retained dependent environments and the default executable. After an uninstall, check the app, its selected remnants, and its own services. Report current free space, measured recovery, concurrent growth, reinstall requirements, unresolved items, and coverage gaps. Folder allocations and deletion totals are not physical recovery estimates.

For an opportunity list, give stable numbers, exact paths or selectors, measured eligible sizes, contents/purpose, use evidence, and the condition for safe removal. Separate regenerable caches, optional installed software, and data needing a user decision. Do not inflate savings with overlapping parents/children, all versions when one must remain, empty device registrations, sparse-disk maximum capacity, or personal artifacts labeled as cache. If fewer than the requested number of useful verified candidates remain, report that and the uninspected areas instead of padding the list.

| Candidate | Evidence needed in addition to inactivity |
| --- | --- |
| Dependencies/builds | Known generated installation/output; retained lockfiles, build inputs, or environment metadata; no tracked/custom content lost |
| APK/IPA/installers | Obsolete or redundant artifact; retain current release/reviewer builds and any unique analysis evidence |
| Emulators/simulators | Known disposable QA device with no current task/data dependency; shutdown alone is insufficient |
| Git temporary packs | Git garbage classification, stable separate observations, no live writer/handle, valid history preserved |
| Model/package caches | Re-downloadable contents; preserve authentication, installed environments, active models, and persistent data |
| Rarely used apps/extensions | Bundle or extension identity, measured payload, current activity, and recorded last use or an explicit unknown; retained user data and shared components |
| Old/duplicate runtimes | Architecture, version, default selection, executable links, dependent environments, and embedded app runtimes; pool size is not all removable |
| Downloads/history/logs | The user's exact age and recent-use criteria, supported record timestamps where applicable, and no unique required content or live writer |

## Tools and conditional details

Use [the discovery checklist](references/discovery.md) for broad audits. Read the relevant sections of [macOS cleanup notes](references/macos.md) before app/runtime uninstalls, privileged cleanup, Git objects, devices/SDKs, or compression. They also cover activity probes, APFS sharing, and virtual DeviceFS accounting.

The bundled helper inventories **metadata only**; it never decides what to delete or removes files. It skips symlinks and child filesystems, deduplicates hardlinks per root, and compares earlier snapshots. Paths below assume the default personal skill location; resolve relative to this skill if installed elsewhere.

```bash
cleanup_audit="$HOME/Library/Logs/storage-cleanup/$(date +%Y%m%d-%H%M%S)"
umask 077
mkdir -p "$cleanup_audit"
python3 "<this skill's folder>/scripts/inventory.py" \
  --root "$HOME/Developer" --output "$cleanup_audit/inventory.json"
```

Use `--help` for additional roots, output limits, and `--compare`. `--max-depth` limits directory summaries, not traversal: scan selected roots progressively and bound expensive probes. Broad scans can take time; keep the user updated and inspect compact summaries rather than dumping inventories. A partial scan must remain labeled partial.
