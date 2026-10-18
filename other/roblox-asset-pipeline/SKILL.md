---
name: roblox-asset-pipeline
description: Plan and execute Roblox asset workflows. Use for Creator Store search, inventory/group/universe assets, inserting assets, generated meshes, generated materials, procedural models, uploaded images, thumbnails, icons, decals, style consistency, import security audits, and asset performance budgets.
---

# Roblox Asset Pipeline

## Goal

Choose assets that fit the game fantasy, load reliably, and stay within mobile performance budgets.

## Selection Order

1. Search existing assets with `search_asset`.
2. Before inserting Creator Store or third-party model/package assets, plan a `roblox-creator-store-security-audit` pass.
3. Insert selected assets with `insert_asset`.
4. Generate custom meshes with `generate_mesh` only when existing assets do not fit.
5. Generate custom materials with `generate_material` for unique surface treatments.
6. Generate procedural models with `generate_procedural_model` when configurable primitive-based models are useful.
7. Use `store_image` or `upload_image` for local or web images that need to become Roblox assets.

## Cross-Owner Caution

When an inventory asset belongs to a different owner than the current place, ask for explicit user consent before inserting it. Name the source owner and destination.

## Security Audit Requirement

Creator Store and third-party model/package imports can include scripts. After inserting any third-party model, package, UI, gameplay asset, or plugin-like asset, use `roblox-creator-store-security-audit` before trusting it or leaving its scripts enabled. Prefer visual-only assets when possible. Treat obfuscated code, suspicious `require` calls, dynamic asset loading, HTTP usage, DataStore mutation, remote creation, hidden scripts, and deceptive names as high risk.

## Art Direction

- Keep a consistent silhouette language, scale, color palette, and material style.
- Make important interactables visually louder than background props.
- Design icons and thumbnails for click clarity at small sizes.
- Avoid dark, noisy, or over-detailed first-area assets that obscure gameplay.

## Performance Budgets

- Prefer low-to-moderate poly meshes for mobile.
- Watch texture size, transparency, particles, dynamic lighting, and physics complexity.
- Anchor decorative props unless they must simulate.
- Convert repeated decorative objects into cheaper reusable patterns where possible.
- Run performance review for large asset drops.

## MCP Workflow

1. Search or generate the asset.
2. Insert third-party assets into a controlled quarantine folder or workspace location.
3. Inspect with `inspect_instance`.
4. Run an import security audit for third-party model/package/gameplay/UI assets.
5. Use `screen_capture` for visual fit.
6. Playtest if the asset affects collision, navigation, UI, or interaction.
7. Check `get_console_output`.

## Output

Return:

- Asset source or generation method.
- Placement and ownership notes.
- Security audit result for third-party imports.
- Visual-fit notes.
- Performance risks.
- Verification performed.

## Next

Audit any imported third-party asset with `roblox-creator-store-security-audit` before trusting it, and check its cost with `roblox-performance-optimization`.
