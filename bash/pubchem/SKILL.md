---
name: pubchem
description: Use when an agent needs PubChem PUG REST lookups for names, CIDs, formulas, synonyms, properties, or public analog search without depending on ChemQA runtime state.
---

# PubChem

## Overview

Resolve compound identities and basic compound metadata through PubChem PUG REST.
Each script is provider-scoped and writes a stable JSON result file in the
requested output directory.

## When to Use

Use this skill when:
- a prompt contains a common name, synonym, formula, or PubChem CID
- an agent needs PubChem synonyms or compound properties
- a public similarity lookup against PubChem analogs is useful
- a compact provider-only compound profile is enough for the next step

Do not use this skill for structural validation. After PubChem returns a
structure, hand it to the `rdkit` skill for canonicalization or validation.

## Execution

```bash
python scripts/run_skill.py \
  --workspace-root . \
  --execution-cwd "$PWD" \
  --script skills/pubchem/scripts/name_to_cid.py -- \
  --request-json /path/to/request.json \
  --output-dir /tmp/pubchem-out \
  --json
```

Read `references/contracts.md` for request fields, output structure, timeout
behavior, and per-script request examples.
