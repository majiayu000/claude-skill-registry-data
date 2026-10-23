---
name: design-forensics
description: Inspect live websites, screenshots, motion references, or structured design files and convert the evidence into normalized Design DNA without copying source expression.
---

# Design Forensics

Use this skill before asking an agent to apply inspiration from an existing design.

## Default order

1. Prefer a live public URL.
2. Capture desktop, tablet, and mobile evidence.
3. Record DOM hierarchy, geometry, computed styles, interactions, media, animations, responsive changes, and errors.
4. Generate `design-dna.json` and `report.html`.
5. Mark uncertain dimensions explicitly.
6. Stop before implementation unless the task also invokes reference synthesis.

## Command

```bash
node scripts/inspire.mjs add <url-or-file> --label <name>
```

For a screenshot, video, Figma export, or other file, provide a structured annotation when exact browser evidence is unavailable:

```bash
node scripts/inspire.mjs add reference.png --analysis reference-design-dna.json
```

## Evidence rules

- A URL may support high-confidence structure, type, material, interaction, media, and motion evidence.
- A screenshot cannot prove hidden states, breakpoints, exact fonts, DOM order, accessibility, or animation timing.
- A motion clip cannot prove source code, interaction semantics, or responsive behavior.
- Do not infer exact implementation details that the evidence does not support.
- Never store authenticated or private references without explicit authority.
- Keep local captures under `.aigent/inspiration`; do not commit third-party screenshots or extracted private data.

## Output contract

Every source must have:

- source identity and origin
- capture timestamp
- source kind
- evidence list
- confidence by dimension
- structure, typography, material, motion, interaction, media, and responsive DNA
- copy fingerprint, not copied copy
- human-readable report

The output describes a design. It does not authorize reuse of source assets or expression.
