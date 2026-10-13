---
name: asset-audit
description: "Audits artifacts for compliance. Game: art/audio/VFX asset naming, budgets, formats, and pipeline requirements. Product: build artifacts, API schemas, docs assets, release bundles, and package outputs."
argument-hint: "[category|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep
# Read-only diagnostic skill — no specialist agent delegation needed
---

## User Guide

- When to use: Audits artifacts for compliance. Game: art/audio/VFX asset naming, budgets, formats, and pipeline requirements. Product: build artifacts, API schemas, docs assets, release bundles, and package outputs.
- Inputs: Command arguments: `/asset-audit [category|all]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before auditing:
- `design/cdd/game-concept.md` -> **[Game]** audit game assets: art, audio, VFX, shaders, naming, formats, size budgets, and engine import readiness.
- `design/cdd/product-concept.md` -> **[Product]** audit product artifacts: build outputs, packaged assets, API schemas, CLI help/manpage assets, docs screenshots, OpenAPI files, migration files, and release bundles.
- If unclear, ask whether the audit target is a game asset pipeline or a product artifact/release pipeline.

Keep all existing game asset checks. Add product artifact checks only when the product branch is selected.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, art bible, asset manifest/specs, technical preferences, CLAUDE naming conventions, asset directories | Product Concept, module index, product artifact specs, technical preferences, architecture/ADRs, release docs, API/CLI/docs/package/migration/deployment directories |
| Steps | Scan art/audio/VFX/shader/data assets, check naming/formats/budgets, find orphaned and missing assets | Scan schemas, CLI help, docs assets, config samples, migrations, build/package outputs, release bundles; check contracts, examples, packaging, secrets, orphaned/missing artifacts |
| Outputs | Asset Audit Report with COMPLIANT/WARNINGS/NON-COMPLIANT verdict | Product Artifact Audit Report with contract/package/docs/config/migration verdicts |
| Next steps | Fix naming/format/size gaps, review orphaned assets, `/content-audit`, `/asset-spec` | Fix contract/package/docs/config/migration gaps, `/code-review`, `/test-evidence-review`, `/release-checklist` |

## Phase 1: Read Standards

Read the art bible or asset standards from the relevant design docs and the CLAUDE.md naming conventions.

---

## Phase 2: Scan Asset Directories

Scan the target asset directory using Glob:

- `assets/art/**/*` for art assets
- `assets/audio/**/*` for audio assets
- `assets/vfx/**/*` for VFX assets
- `assets/shaders/**/*` for shaders
- `assets/data/**/*` for data files

---

## Phase 3: Run Compliance Checks

**Naming conventions:**
- Art: `[category]_[name]_[variant]_[size].[ext]`
- Audio: `[category]_[context]_[name]_[variant].[ext]`
- All files must be lowercase with underscores

**File standards:**
- Textures: Power-of-two dimensions, correct format (PNG for UI, compressed for 3D), within size budget
- Audio: Correct sample rate, format (OGG for SFX, OGG/MP3 for music), within duration limits
- Data: Valid JSON/YAML, schema-compliant

**Orphaned assets:** Search code for references to each asset file. Flag any with no references.

**Missing assets:** Search code for asset references and verify the files exist.

---

## Phase 3b: Product Artifact Compliance Checks

Run this branch when `design/cdd/product-concept.md` exists or the user selected
the Product route. Keep the game asset checks above available for game projects;
this branch is the product-equivalent artifact audit.

**Product standards to read:**
- `design/cdd/product-concept.md` for product promise, target users, platform, and artifact categories
- `design/cdd/module-index.md` for modules that should expose APIs, CLI commands, migrations, UI screens, data flows, or documentation
- `standards/technical-preferences.md` for language, framework, build system, package manager, naming conventions, and deployment target
- `docs/architecture/architecture.md` and ADRs for public contracts, migration rules, packaging constraints, and release boundaries
- `production/releases/` for expected release bundle shape, if present

**Product directories to scan:**
- API schemas and contracts: docs API folders, OpenAPI files, schema folders, source files named like schema, and source contract folders
- CLI artifacts: docs CLI folders, source command folders, source CLI folders, generated help/manpage files
- Build/package outputs: `dist/**/*`, `build/**/*`, `target/**/*`, `packages/**/*`, `release/**/*`
- Config samples: `*.example`, `*.sample`, `.env.example`, `config/**/*`
- Migrations and seed data: `migrations/**/*`, `db/migrations/**/*`, `seeds/**/*`
- Documentation assets: `docs/**/*.{png,jpg,jpeg,svg,gif,webp}`, `docs/examples/**/*`, SDK examples, onboarding snippets

**Product compliance checks:**
- Public API schemas are present for documented endpoints and match documented request/response names.
- CLI commands documented in UX specs or docs have matching help output, examples, and exit/error behavior.
- Config samples contain all required keys, no secrets, and placeholders that match the configured stack.
- Migration files are ordered, reversible or explicitly irreversible, and mapped to the module or release that needs them.
- Build and package artifacts use the expected naming/version pattern and do not include local-only files, credentials, caches, or test fixtures.
- Documentation images, screenshots, examples, and SDK snippets are referenced from docs and are not stale, orphaned, or missing.
- Release bundles include changelog/release notes, migration notes, and rollback/deployment instructions where the product architecture requires them.

**Product orphan/missing checks:**
- Search docs, source, package manifests, and release notes for every Product artifact reference.
- Flag unreferenced generated artifacts as review-needed rather than deleting them automatically.
- Search for documented endpoints, commands, config keys, and migrations that have no matching implementation or artifact file.

---

## Phase 4: Output Audit Report

For game projects, use the existing Asset Audit Report format below.

```markdown
# Asset Audit Report -- [Category] -- [Date]

## Summary
- **Total assets scanned**: [N]
- **Naming violations**: [N]
- **Size violations**: [N]
- **Format violations**: [N]
- **Orphaned assets**: [N]
- **Missing assets**: [N]
- **Overall health**: [CLEAN / MINOR ISSUES / NEEDS ATTENTION]

## Naming Violations
| File | Expected Pattern | Issue |
|------|-----------------|-------|

## Size Violations
| File | Budget | Actual | Overage |
|------|--------|--------|---------|

## Format Violations
| File | Expected Format | Actual Format |
|------|----------------|---------------|

## Orphaned Assets (no code references found)
| File | Last Modified | Size | Recommendation |
|------|-------------|------|---------------|

## Missing Assets (referenced but not found)
| Reference Location | Expected Path |
|-------------------|---------------|

## Recommendations
[Prioritized list of fixes]

## Verdict: [COMPLIANT / WARNINGS / NON-COMPLIANT]
```

This skill is read-only — it produces a report but does not write files.

For product projects, use this equivalent report:

```markdown
# Product Artifact Audit Report -- [Target] -- [Date]

## Summary
- **Artifacts scanned**: [N]
- **Contract violations**: [N]
- **Package/release violations**: [N]
- **Docs/example violations**: [N]
- **Config/migration violations**: [N]
- **Orphaned artifacts**: [N]
- **Missing artifacts**: [N]
- **Overall health**: [CLEAN / MINOR ISSUES / NEEDS ATTENTION]

## Contract Violations
| Artifact | Expected Contract | Issue |
|----------|-------------------|-------|

## Package and Release Violations
| Artifact | Expected Pattern | Issue |
|----------|------------------|-------|

## Documentation and Example Violations
| Artifact | Reference Location | Issue |
|----------|--------------------|-------|

## Config and Migration Violations
| Artifact | Expected Requirement | Issue |
|----------|----------------------|-------|

## Orphaned Product Artifacts
| File | Last Modified | Size | Recommendation |
|------|---------------|------|----------------|

## Missing Product Artifacts
| Requirement Source | Expected Artifact |
|--------------------|-------------------|

## Recommendations
[Prioritized fixes: contract first, then migration/config, then docs/package hygiene]

## Verdict: [COMPLIANT / WARNINGS / NON-COMPLIANT]
```

---

## Phase 5: Next Steps

- Fix naming violations using the patterns defined in CLAUDE.md.
- Delete confirmed orphaned assets after manual review.
- Run `/content-audit` to cross-check asset counts against GDD-specified requirements.

## Phase 5b: Product Next Steps

- Fix contract violations before release; run `/code-review` on any affected API/CLI/schema implementation.
- Run `/test-evidence-review` on contract, migration, packaging, and docs evidence before closing the release story.
- Run `/content-audit` in Product mode to cross-check documented surfaces against implemented endpoints, commands, workflows, and examples.
- Run `/release-checklist` when package, deployment, migration, and rollback artifacts are ready for final validation.
