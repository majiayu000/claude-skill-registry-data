---
name: safe-cleanup
description: Reclaim disk space safely on Windows, macOS or Linux with a hash-approved deletion plan; the packaged helper deletes only the exact files the user approved and reports what was and was not removed.
priority: P0
category: productivity
status: builtin-guidance
---

# Safe Cleanup: reclaim disk space without collateral deletion

Use this Skill before any AI-initiated disk cleanup, recursive deletion, cache purge or storage-reclamation task through Remote Arc. **Freeing space is the goal.** Moving files to the Recycle Bin/Trash or a quarantine folder on the same volume usually frees **no** space, so do not promise otherwise.

A Skill guides the calling AI. It is **not** an OS sandbox, backup or permission grant. The device Safety Guard refuses terminal deletes that would reach roots, home, personal, system or credential folders or whose target is ambiguous, but it cannot see paths a script computes at run time. Trusted Write Locations do **not** confine shell side effects, and **Local Undo cannot restore shell or helper deletions**.

## Device and permission gates

Work only on the user's authorized device, with existing `computer:read` and, for deletion, `computer:write` plus terminal access (`start_process`). Do not escalate privileges, use hidden credentials, upload data, disable Safety Guard or enable terminal access yourself. If terminal access is off, deliver a read-only cleanup plan and stop there.

## Packaged helper: plan, approve, execute

All recursive or bulk deletion goes through `scripts/safe-cleanup.mjs` (Node 18.15+, no dependencies). Arc: `prepare_skill {id:"safe-cleanup",deviceId,workspace}`. Connect: `read_skill` id `safe-cleanup`, path `scripts/safe-cleanup.mjs`, follow `nextOffset` to null, save the exact chunks with `write_file` and verify bytes and SHA-256 against the manifest. Check `node --version` first.

1. **Inspect (read-only).** Confirm device, volume and free space. Find candidates with bounded size checks. Pick the narrowest folders that are clearly disposable (app/package caches, temp, build output). Do not infer that large personal files are disposable.
2. **Plan (no deletion):**

       node "<helper>/scripts/safe-cleanup.mjs" plan --target "<absolute folder>" [--target "<another>"] [--older-than-days 2] --output "<workspace>/.safe-cleanup/plan-<UTC time>.json"

   Pass each path as its own double-quoted argument straight to `start_process`. Do not use nested `cmd /c` or PowerShell wrapping, wildcards, `%VAR%`, `$VAR` or `~`; the helper rejects them. The plan scans without following symlinks/junctions or crossing mounted volumes, skips `.git`/`.hg`/`.svn` and `.remotearc` (Undo store) subtrees, and refuses drive or volume roots, home, personal and cloud-sync folders, credential and browser-profile stores, system directories, project roots, non-build folders inside projects, UNC/network paths and the ancestors of any of these. Use `--older-than-days` for shared temp folders so files in active use stay.
3. **Preview and approval.** Show the user each root path, total files and bytes, the largest entries, the skipped reasons (`link-not-followed`, `nested-repository`, `newer-than-cutoff`...), the hard-link note and the plan hash. State that deletion is **permanent** and Local Undo cannot restore it. Ask for an explicit yes to *this* plan. If `recognizedCacheLocation` is false, the user must confirm that exact folder is disposable. A generic "free up space" request does not approve a plan.
4. **Optional check:** `execute --plan "<plan>" --hash <hash> --dry-run` re-verifies every entry and deletes nothing.
5. **Execute exactly what was approved:**

       node "<helper>/scripts/safe-cleanup.mjs" execute --plan "<plan>" --hash <full 64-char hash>

   Run it with `background: true` and poll `process_status`, so the 5 s default timeout cannot kill it mid-run. The helper refuses a changed, rehashed, expired (>60 min), foreign-device or already-executed plan. It refuses the whole plan if a root was replaced or now resolves elsewhere. It deletes a file only if its parent still resolves to the planned folder and its identity, size and modification time are unchanged. It removes a folder only if it is empty and unchanged. Files created after the preview, files that changed, locked or denied files and redirected folders are **kept and listed**, never "fixed" by widening the action.
6. **Cancel:** `node "<helper>/scripts/safe-cleanup.mjs" cancel --plan "<plan>"` stops before the next entry. If the process was killed, `<plan>.journal.jsonl` lists every path already removed.
7. **Report from `<plan>.report.json`:** status (`completed`, `partial`, `cancelled`, `timed_out`), files, folders and bytes removed, `notRemoved` reasons with sample paths, entries not attempted, and free bytes before and after on the same volume. Freed space can be smaller than the bytes removed because of hard links, open handles, snapshots or compression. Never say "saved for recovery" and "space freed" about the same data.

To clean again, make a new plan. Never edit a plan file or reuse a hash.

## Without the helper

If Node is unavailable or the helper refuses a target, **do not** fall back to `rd /s /q`, `Remove-Item -Recurse`, `rm -rf`, `del /s` or wildcard deletes. Instead:
- Prefer the owning tool's documented cleanup: `npm cache clean --force`, `pnpm store prune`, `pip cache purge`, `docker system prune` (show what it removes first), `brew cleanup`, Xcode DerivedData via Xcode, Windows Storage Sense/Disk Cleanup, or an app's own "clear cache" setting.
- To delete one exact, verified file, use a structured file API if one exists. Otherwise give the user exact on-device steps and let them do it.
- For a refused target (personal folders, project sources, system folders), explain why and let the user decide manually. A user's general permission does not waive these boundaries; erasing a disk or root needs a separate, manual OS workflow.

## Choosing a method

1. **Disposable cache/temp/build data (preferred):** helper plan, approval, then permanent deletion. This really frees space.
2. **Uncertain or personal data:** inspect and describe; the user decides and deletes manually. Size alone never makes data disposable.
3. **Recoverable alternative:** offer Recycle Bin/Trash only if the user wants a recovery window **instead of** freed space. A backup on a different volume frees the source only after deletion, uses the destination's space and needs approval.
4. **Lower-risk options:** uninstall through the package manager, rotate a known log, or move future caches and downloads to another drive.

## 中文提醒

用户说"清理 C 盘/D 盘、腾空间、删缓存、永久删除"时，先只读排查，选准**具体的缓存/临时/构建目录**，然后用随技能附带的 `safe-cleanup.mjs` 生成删除计划（plan）。把目录、文件数、大小、跳过原因和计划哈希给用户看，明确说明删除是**永久**的，Local Undo 无法恢复。用户明确同意这一份计划后，才用同一个哈希执行（execute）。执行时只删计划里且未变化的文件：新出现的、被修改的、被占用的文件，以及被换成链接的目录，一律保留并写进报告，绝不扩大删除范围。不要用 `rd /s /q`、`rm -rf` 或通配符兜底；遇到盘符根目录、个人文件夹、项目源码、系统目录或网络路径，停下并说明原因。
