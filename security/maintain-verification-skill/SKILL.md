---
name: maintain-verification-skill
description: "Audit and update a project-local Roblox verification skill when code, Rojo mappings, tests, remotes, data schemas, or authored contracts change."
---

# Maintain a Roblox verification skill

Compare the verification skill with current repository instructions, project mappings, scripts, tests, security boundaries, persistence contracts, and authored-context requirements.

Update only proven drift. Remove stale commands and claims. Add missing checks only when they are repeatable and scoped. Run each non-playtest check after editing. Keep Studio execution modes aligned with the Roblox engineering contract and preserve the explicit ban on playtesting controls. Report which checks are automated, which are source assertions, which are Studio-fallback edits, and which still require the user's Studio playtest.
