---
name: manage-modules
description: Create, enable, disable or remove modules, or manage registered systems.
---

1. Run `yarn studio status` and `yarn studio list`. Read [Modules](../../context/modules.md), the affected README and CLI help. Shared changes require an Admin.
2. Use create-module, enable, disable or remove. Preview before --yes where supported; enable and disable apply immediately. Keep content unless deletion was requested. Required modules remain installed and enabled. Treat installed code as trusted executable code; inspect its source before adopting it.
3. When you remove a module, also remove its tests: they live in `tests/`, not in the module, so they stay behind and fail. Find them with `grep -rl "src/modules/<id>" tests`, by name (`tests/*/<id>-*.test.ts`) and by their fixtures in `tests/fixtures/`. Delete files that test only that module; in shared files, remove only the cases that need it. Then run `yarn test`.
4. For system creation, rename, archive, restore or deletion, consult the enabled systems module README and use its implemented commands. Preserve prototypes and pending rebuild originals. Dependency changes use yarn; edit canonical declarations rather than generated adapters or lockfiles.
5. Run sync, restart the recorded dev server when availability changes, and verify the affected routes and surviving content. Report changes and any unavailable command instead of inventing an alternative distribution workflow.
