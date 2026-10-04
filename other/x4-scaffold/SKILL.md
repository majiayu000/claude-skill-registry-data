---
name: x4-scaffold
description: Scaffold the complete cross-file footprint for new X4 content (ware, and basic ship/module) modelled on a vanilla analogue, then auto-validate with x4validate. Use when adding new content so you start complete instead of forgetting files.
allowed-tools: Read, Write, Glob, Grep, Bash
---

Scaffold new content modelled on a vanilla analogue, then validate.

**Inputs:** content type (`ware`/`ship`/`module`), the new id, the target mod's dev folder, and a vanilla analogue id (e.g. `ore`).

Steps:
1. **Study the analogue** in the reference tree (`$X4_REFERENCE`) (`libraries\wares.xml`, etc.). Read its full footprint: definition, name/description `{page,t}`, price, production, `<component ref>`, owner, restriction.
2. **Generate diff stubs** into the mod's dev folder, mirroring game paths (diff patches for existing files; complete files only for brand-new files):
   - `libraries/wares.xml` — `<add sel="//wares">` the new `<ware>` with the SAME kinds of children as the analogue (placeholder values to fill in).
   - `t/0001.xml` — `<add sel="/language">` a new `<page>` (pick a high unique id ≥ 20000 to avoid collisions) with name + description `<t>` entries.
   - For `ship`/`module`: wire `<component ref="..._macro">` and note the macro/component/index files the user must provide. DO NOT fabricate meshes — flag those as manual steps.
3. **Validate completeness:**
   `cd $CLAUDE_PROJECT_DIR/tools/x4validate && uv run --python 3.13 x4validate <mod-dir> --entity <type>:<id> --like <type>:<analogue>`

   ⚠ **This compares `<ware>`-WRAPPER fields only** — definition, name/description
   strings, price, production, `<component ref>`, owner, restriction. For a ship or
   module it does **NOT** open the macro: physics, connections/hardpoints,
   engine/shield/turret slots, storage, hull, software and steering curves are never
   inspected. **A clean result here does NOT mean the ship is complete.** The run
   prints this as a NOT CHECKED entry — read it, don't skip past it.
4. **Report** what was created and any remaining manual steps. For ships/modules the
   macro interior and mesh/asset files are ALWAYS manual — say so explicitly rather
   than letting a clean completeness result imply the work is done.

Honor CLAUDE.md: confirm before writing `content.xml`; review the full change list first.
