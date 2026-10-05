---
name: brand
description: Create, update, apply, and audit brand strategy, voice, messaging, visual identity, asset rules, and governance. Use for brand guidelines, tone of voice.
---

# Brand

Treat brand as a governed system of decisions. Preserve approved identity and record intentional changes.

## Route the request

- Brand foundation: voice, audience, positioning, values, and messaging.
- Visual identity: logo use, color, typography, imagery, and layout behavior.
- Asset governance: naming, folders, versions, approval, and provenance.
- Compliance review: compare an artifact with approved rules and report deviations.
- Update: change one controlled source, then propagate and verify dependents.

Read only the relevant file under references/. Use templates/brand-guidelines-starter.md when the user wants a new durable guideline document.

## Workflow

1. Locate the source of truth.
   - Prefer the user's existing guideline, tokens, logo files, and approved examples.
   - Separate confirmed rules from inferred patterns.

2. Define the audience and communication job.
   - Identify who should think, feel, or do what.
   - Keep positioning, promise, proof, and tone distinct.

3. Build or update the system.
   - Use semantic names for colors and tokens.
   - Define voice with observable do/don't rules and examples.
   - Specify logo clear space, minimum size, backgrounds, and prohibited treatments.
   - Define asset ownership, approval status, version, and source provenance.

4. Apply consistently.
   - Reuse approved tokens and assets.
   - Adapt tone to channel without changing brand character.
   - Record deviations required by accessibility, platform, or legal constraints.

5. Validate.
   - Run node "<skill-dir>/scripts/validate-asset.cjs" <asset-path> for supported asset checks.
   - Use references/consistency-checklist.md and references/approval-checklist.md for manual review.
   - Check contrast and readability even when an approved color combination is supplied.

6. Synchronize only when requested.
   - node "<skill-dir>/scripts/sync-brand-to-tokens.cjs" --dry-run previews brand-to-token changes.
   - Review the diff before writing generated token files.

## Output contract

State:

- source-of-truth files used;
- confirmed rules and inferred recommendations;
- changes or violations by severity;
- affected assets or channels;
- validation performed;
- approvals still required.

## Guardrails

- Do not silently rebrand an existing product.
- Do not overwrite master assets or approved guidelines without authorization and a backup.
- Do not infer legal trademark clearance.
- Do not weaken accessibility to preserve a visual rule; propose a compliant variant.
- Do not hardcode an AI provider, model, or host-specific skill path.
