---
name: asset-provenance-audit
description: Audit website images, videos, models, textures, audio, generated media, and VFX for source records, commercial rights, attribution, manifests, and secret-safe public documentation.
---

# Asset Provenance Audit

Read:

- `creative-production/standards/provenance.md`
- `assets/manifests/asset-manifest.schema.json`
- `creative-production/catalog.json`

## For every asset

Verify:

- source type
- provider or creator
- exact source URL
- exact license or active plan class
- commercial-use status
- attribution requirement
- verification date
- safe receipt or generation reference
- production edits
- public outputs
- mobile and reduced-motion variants
- budget overrides

## Block release when

- commercial use is unresolved
- required attribution is absent
- a free-plan generation is assumed to inherit later paid rights
- a marketplace summary replaces the item license
- a source asset is redistributed as a competing standalone asset
- the repository contains API keys, signed URLs, personal billing data, or confidential paths

## Run

```bash
npm run assets
npm run catalogs
```

The script checks structure and public-file safety. It cannot make a legal judgment. Escalate restricted, geographic, enterprise, trademark, likeness, or editorial-use questions.
