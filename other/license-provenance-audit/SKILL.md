---
name: license-provenance-audit
description: Inventory code provenance and license notices for metisa without making legal conclusions or changing third-party terms.
---

# License and Provenance Audit

## Use when

Preparing a repository release, adding dependencies, changing license metadata, or encountering third-party source/assets.

## Procedure

1. Read the repository `LICENSE` and `THIRD_PARTY_NOTICES.md` first.
2. Inspect each component's source headers, bundled license files, package metadata, and upstream URL.
3. Record the exact evidence, file scope, version, and unresolved contradictions. Keep original notices intact.
4. Distinguish copyright ownership, license grant, trademark, patent, and product-protection questions.
5. Escalate compatibility, assignment, jurisdiction, utility-model, and enforceability decisions to qualified counsel and relevant rights holders.

## Constraints

- Do not tell the user that a license is worldwide watertight or that they own inherited code without evidence.
- Do not replace upstream GPL/LGPL/MIT/BSD/other notices with a metisa-only restriction.
- Do not publish or redistribute as legally cleared while the rights chain is unresolved.
- This skill is provenance organization, not legal advice.

## Done when

The inventory is evidence-based and every unresolved rights question is visibly gated; no license conclusion exceeds the documents inspected.