---
name: curated-workflow-catalog
description: "Discover and route broad requests across the currently installed skill library when no single specialist is obvious. Use for current capability discovery, installed-skill lookup, or Turkish intents such as ‘hangi skill uygun’, ‘hangi beceriyi kullan’, ‘kurulu becerilerde ara’, ‘uygun iş akışına yönlendir’. Do not intercept a clean specialist match or search the archived full library; use skill-library-router for an archived or uninstalled workflow."
license: MIT
---

# Curated Workflow Catalog

Route from current skill metadata rather than a duplicated static catalog.

## Routing

1. Prefer the host's current skill/plugin metadata when it is available. Initial routing should use only each skill's `name` and `description`.
2. In a filesystem-backed skill library, use `scripts/list_skill_metadata.py` to enumerate sibling `SKILL.md` frontmatter without loading full bodies.
3. Rank only a small candidate set by task intent, required output, domain, and explicit user wording.
4. Load the full instructions for the best matching installed skill only after selection. Load a second candidate only when the first leaves a material ambiguity.
5. If the requested workflow is not installed, say so and route to the closest available capability; never claim that archived or unavailable instructions were loaded.
6. Current system, safety, user, project, and installed-skill instructions always outrank catalog metadata.

## Trigger discipline

Use this router when discovery itself is needed. Do not intercept a request that already cleanly matches a specialist skill.

Useful Turkish discovery wording includes `hangi skill uygun`, `hangi beceriyi kullan`, `skill kataloğunda ara`, `uygun workflow bul`, and equivalent natural phrasing.

## Output

Normally route silently. When the user explicitly asks what was selected, return the chosen skill name plus a one-line reason and mention any close alternative only if it materially differs.
