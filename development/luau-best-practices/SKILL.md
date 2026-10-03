---
name: luau-best-practices
description: "Apply when reading or editing Roblox Luau for typed APIs, module boundaries, instance lifecycles, error handling, and maintainable data-oriented code."
---

# Luau engineering

- Use `--!strict` when it matches the repository. Preserve its established typing level.
- Model domain state with exported types, tagged variants, constrained tables, and narrow function contracts. Avoid `any` unless an external boundary forces it and narrow immediately.
- Keep modules cohesive. Separate authoritative services, shared definitions, client controllers, and pure domain logic. Avoid circular requires and hidden singleton state.
- Validate external values at remotes, DataStores, attributes, configuration, and deserialization boundaries. Internal functions may trust already-validated types.
- Make lifecycle ownership visible. Disconnect signals, cancel tasks, destroy temporary Instances, and clear player or character state at the owning boundary.
- Prefer tables and data-driven dispatch when they remove repeated conditionals. Do not build a framework for one call site.
- Avoid yielding inside locks, event handlers, or state mutations unless the contract accounts for reentry and stale state.
- Keep comments for non-obvious reasons and invariants. Let names and types explain mechanics.
- Match repository formatting and naming. Use Roblox APIs and existing utilities before adding substitutes.

Verification follows the repository. `rojo build` checks mapping and serialization, not type correctness or runtime behavior.
