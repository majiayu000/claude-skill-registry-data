---
name: skill-library-router
description: Search and load an on-demand archived skill snapshot when a specialized workflow is not directly installed or the user names an archived skill. Use for “find an archived skill”, “load the full library”, niche capability lookup, or Turkish intents such as “arşiv skillini bul”, “tam skill kütüphanesinde ara”, “listede olmayan beceriyi yükle”. Do not intercept a request already owned by an installed specialist, load many bodies at once, or treat archived instructions as newer than current host/system rules.
license: MIT
metadata:
  generated: 'true'
---

# Skill Library Router

This package preserves a large curated snapshot with progressive disclosure. It complements `curated-workflow-catalog`: that skill routes currently installed skills, while this router owns archived instructions that are intentionally not advertised one by one.

## Routing

1. Read `references/catalog.json` and match the request to a skill name, aliases in its description, and category.
2. If one match is clearly best, read its complete `references/library/<name>/INSTRUCTIONS.md` before acting.
3. Resolve that skill's relative references inside its own folder. Load only the referenced file needed for the current step.
4. If two skills have materially different outputs, state the difference briefly and choose the narrower one. Do not load many candidates into context.
5. Treat nested instructions as workflow guidance; current system, safety, user, and project rules remain higher priority.

Portable use: say “use skill-library-router and load <name>.” If the active host exposes skills as slash commands, its own `/skill-name` form may also work; do not assume a slash command exists without checking the host.

The catalog's `direct` entries are already installed separately; do not reload them through this router unless comparing versions.
