---
name: newbrain-brain-layering
description: Enforce BRAIN repository layering and NewBrain alignment rules—shared identical cross-platform code versus per-OS overlays, materialize workflow, and import/sync ownership. Use when working in the BRAIN repo, aligning BRAIN to NewBrain, extracting shared desktop/agentd/protocol/plugin code, editing platforms/windows|macos|ubuntu overlays, running materialize/import-upstream/verify-layout, or deciding whether a change belongs in shared/ or platforms/<os>/.
---

# NewBrain BRAIN Layering

Apply this skill for every BRAIN change and every BRAIN ↔ NewBrain alignment. Do not invent a different split.

## Ownership rule (mandatory)

公共部分 → shared/
各系统行为一致、文件内容也相同的功能代码（desktop/agentd/protocol/插件等）。

各系统独有 / 兼容差异 → platforms/<系统>/

Windows：platforms/windows/（MSI、ulit、PATH/编码、Windows 专用脚本等）
macOS：platforms/macos/common/ + 必要时 arm64/x64（签名、entitlements、DMG、mac PATH 等）
Ubuntu：platforms/ubuntu/common/ + arm64/x64（AppImage/deb、Bash 默认等）
生成可运行工程时：先铺 shared/，再用对应系统目录整文件覆盖同名路径。
所以：公共能力一处维护，系统兼容和打包差异放在各自目录。

## Classification

1. Same relative path and identical file bytes across the platforms being synced → `shared/<relative-path>`.
2. Any content difference, or a file that exists on only one OS → that OS overlay under `platforms/<os>/...` as a **complete file** (no line-level patches).
3. Never keep the same relative path in both `shared/` and a platform overlay. Run `pnpm verify:layout` after moves.
4. Divergent files that later become identical → move into `shared/` and delete every overlay copy.
5. A shared file that must diverge → copy into each needed overlay first, then delete the shared copy.

## Relationship to NewBrain

- **NewBrain** is the upstream product tree (`mac/`, `windows/`, optional Ubuntu).
- **BRAIN** is the layered source: `shared/` + `platforms/*`.
- Runnable workspaces are generated only via materialize into `.materialized/<target>`. Never hand-edit `.materialized/`.

Alignment target: after materialize, BRAIN’s generated tree matches NewBrain’s corresponding platform tree for managed source (normalize CRLF→LF when comparing). Ignore local junk (`node_modules`, `release`, diagnostic `apps/desktop/_*.txt`, temp locks).

## Align / import workflow

1. Treat a deliberate NewBrain snapshot as the source of truth unless the user says otherwise.
2. Full refresh: `node scripts/import-upstream.mjs <newbrain-root>` (rebuilds `shared/`, `platforms/macos/common/`, `platforms/windows/`).
3. Preserve BRAIN-only infra (`scripts/materialize.mjs`, `scripts/verify-layout.mjs`, `docs/architecture/`, arch `newbrain.arch.json`, Ubuntu overlays) and then remove any Ubuntu paths that collide with the new `shared/`.
4. Incremental edits: change only the owning layer (`shared/` vs the specific overlay).
5. Materialize and verify:
   - `pnpm materialize:windows` / `pnpm materialize:macos-arm64` / `pnpm materialize:macos-x64` / Ubuntu targets as needed
   - `pnpm verify:layout`
   - Content compare of `.materialized/<target>` vs `NewBrain/<platform>` with LF normalization
6. Do not use `git reset --hard` or broad `git clean` to “fix layering” unless the user explicitly requests destructive recovery.

## Edit checklist

Before editing a file, answer:

- [ ] Is behavior identical on every target OS **and** should the bytes stay identical? → `shared/`
- [ ] Is this packaging, native integration, PATH/shell/encoding, installer, or OS-only script? → matching `platforms/<os>/`
- [ ] CPU-specific macOS/Ubuntu native or arch metadata? → `arm64` / `x64` overlay
- [ ] Will this create a shared/overlay path collision? → resolve ownership first

## Anti-patterns

- Putting Windows MSI/ulit or mac entitlements/DMG logic into `shared/`
- Duplicating the same identical source under multiple overlays instead of `shared/`
- Line-level patches across platforms instead of whole-file overlays
- Editing `.materialized/` as if it were source
- Aligning by raw hashes only without normalizing line endings

## Related

- Repo rules: `docs/architecture/repository-layout.md`
- Product process/layer guard: `$newbrain-architecture-guard`
- After substantial product changes: `$newbrain-quality-gate`
