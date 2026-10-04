---
name: apple-project-governance
description: "Create, repair, or audit Xcode and Swift package configuration. Use for targets, schemes, resources, generated projects, entitlements, build settings, and configuration drift."
---

# Apple project governance

## Inputs

Identify the affected products, targets, schemes, build configurations, generator inputs, dependencies, and CI path. Read current repository instructions before changing the project graph.

## Rules

- **PROJ-001 — Edit the owner.** Change generator manifests or source configuration, not only their generated output. Inspect regeneration for unrelated churn.
- **PROJ-002 — Verify membership.** Code, resources, models, privacy manifests, and extensions must reach each intended product and no unintended product.
- **PROJ-003 — Preserve identity.** Reconcile bundle IDs, groups, containers, associated domains, and shared constants without renaming durable storage keys for cosmetic consistency.
- **PROJ-004 — Inspect effective configuration.** Source declarations express intent; resolved build settings, bundled resources, and signed entitlements establish what shipped.
- **PROJ-005 — Separate failure classes.** Configuration, compilation, signing, destination availability, and infrastructure require different corrections.

## Workflow

1. Map each changed value to its source owner and downstream targets.
2. Edit the narrow source of truth and regenerate when applicable.
3. Inspect discovered schemes, destinations, and resolved settings for the exact build context.
4. Build the affected target graph; inspect the actual product for resource and capability claims.
5. Review source and generated diffs together.

## Verify

Prove target membership, shared scheme selection, dependency exposure, deployment settings, built Info.plist/resources, and signed entitlements where relevant. Do not treat destination discovery as proof of effective settings.

## Output

Report the owning files, affected products, generated changes, exact build context, and remaining configuration or signing blockers.

## References

Read the [playbook](references/project-governance-patterns.md) for decisions, failure cases, and source links.

For generated inputs, toolchains, and target membership, read the [focused reference](references/build-and-generated-inputs.md).
