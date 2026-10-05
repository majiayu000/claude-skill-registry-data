---
name: slot-scaffolder
description: >-
  Generate a domain data-build slot from OpenAPI files: new business-domain
  pack, scaffold a data-build skill, or add an enterprise custom domain.
  Internal helper of the parent pack; reach this through codexqa-testdata-generator.
license: Apache-2.0
metadata:
  version: "1.0"
---

# Slot scaffolder

Bundled sub-skill of `codexqa-testdata-generator`: turn an OpenAPI directory plus a
domain name into a slot that matches [../slots/SLOT_SPEC.md](../slots/SLOT_SPEC.md),
the single copy of that contract.

## Inputs

`domain` and `openapi` are the prerequisite **materials**. If either is missing, or the OpenAPI directory has no `.yaml` / `.yml` / `.json` files, **stop and ask**. Do not invent operations or scaffold an empty slot. After the user provides them, generate the slot. Do not collect executor fields.

| Field | Meaning | Required |
|---|---|---|
| `domain` | Short English slug (`payments`, `logistics`) | yes |
| `openapi` | Directory of OpenAPI YAML/JSON files (at least one spec) | yes |
| `output` | Destination directory (default `../slots/<domain>`) | no |

## Run

```bash
node scripts/scaffold_slot.ts \
  --domain <domain> \
  --openapi <openapi-dir> \
  --output <output-dir>
```

The script writes `slot.yaml` (the one config), executor stubs, generated `SKILL.md` / `tools-guide.md`, and copies OpenAPI into `assets/openapi/`.

Slots under `./slots/<domain>` are discovered automatically. If the skill lives elsewhere, add one line:

```yaml
workspace:
  slot_roots:
    - /path/to/company-slots
```

## After generation

1. Implement each stub `main(params)` against `DATA_BUILD_API_BASE` (timeouts; never `shell: true`; missing required IDs must fail)
2. Add `scenes` (and optional `aliases` / `invokeParams`) in `slot.yaml` only. List more specific entities before generic ones
3. Refresh generated docs: `node ../scripts/sync_slot.ts --dir <slot>`  
   Hand-written `SKILL.md` is left alone unless it is `generated-from: slot.yaml` or you pass `--force`
4. Smoke-test: `node ../scripts/search_data_build.ts --keywords <domain> --json`

Do **not** add `skill_marketplace.paths` or `api_catalog.paths`. Search, OpenAPI index, and case-pipeline bind all read `slots/` + `workspace.slot_roots`. If `slot.yaml` is omitted, entities are inferred from `scripts/executors/*` and `assets/openapi` operationIds.

Human operators: [../HOW_IT_WORKS.md](../HOW_IT_WORKS.md#appendix-add-a-new-scene). Agents stay on this file and [../slots/SLOT_SPEC.md](../slots/SLOT_SPEC.md).
