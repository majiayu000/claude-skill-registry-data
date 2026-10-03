---
name: manage-skills
description: >-
  Create, update, restructure, rename, merge, or retire portable agent skills. Use when changing a
  skill's activation contract, SKILL.md, reference cards, scripts, assets, evals, discovery
  metadata, or package navigation. Includes standalone canonical templates, optional OpenAI
  metadata, deterministic validation, and safe update rules. Do not use for installing third-party
  skills or unrelated agent configuration.
license: Apache-2.0
metadata:
  author: AutanaSoft
  version: '1.2.0'
---

# Manage Skills

Create and modify skills entirely from package-relative resources. The bundled authoring contract is
the operational authority when host documentation is absent; host rules are stricter overlays only.

## When to Apply

Use this skill when:

- Creating or changing a portable skill package
- Renaming, merging, replacing, retiring, validating, or synchronizing skill content

## How to Use

Resolve these paths relative to this `SKILL.md`, never the current working directory:

```text
references/authoring-contract.md
assets/skill-template.md
assets/reference-card-template.md
scripts/init_skill.py
scripts/generate_openai_yaml.py
scripts/quick_validate.py
```

Read `references/authoring-contract.md` before any create or update. It owns detailed authoring
decisions; this file owns only execution order and resource navigation.

## Workflow

1. Read applicable host instructions and inventory the full existing package or target inventory.
2. Define capability, activation, boundaries, inputs, outputs, and concrete requests; select create
   or update based on equivalence evidence.
3. For create, explicitly decide optional frontmatter, categories, references, and host metadata,
   then run `scripts/init_skill.py --help` and pass only applicable flags. Never initialize an
   existing path.
4. For update, classify behavior as preserved, moved, superseded, or intentionally removed. Change
   narrow owners and preserve unrelated content.
5. Add cards, scripts, assets, README, metadata, and evals only under their contract boundaries.
6. Run the bundled validator and portable scripts/tests in temporary directories. Complete the
   contract's mandatory manual review.
7. Run applicable host formatting, linting, validators, evals, links, registry, diff, and repository
   checks. Synchronize host copies only after the source passes.

Optional OpenAI metadata is requested explicitly during initialization:

```bash
python <skill-root>/scripts/init_skill.py <name> \
  --path <parent> \
  --description <activation-contract> \
  --title <display-title> \
  --overview <purpose-scope-organization> \
  --trigger <first-trigger> \
  --trigger <second-trigger> \
  --openai-metadata \
  --display-name <display-name> \
  --short-description <25-to-64-character-summary> \
  --default-prompt <prompt-containing-$name>
```

Omit the four metadata flags when the host does not require `agents/openai.yaml`. Use
`--categories`, `--references`, `--license`, `--allowed-tools`, `--author`, `--version`, and
`--compatibility` only after explicitly deciding they apply.

## Output Contract

Return:

- `status`: `created`, `updated`, `blocked`, or `failed`
- `executive_summary`: outcome and key design choice
- `artifacts`: exact created, changed, removed, and synchronized paths
- `commands`: exact validations and results
- `manual_review`: semantic rules reviewed manually and unresolved findings
- `next_recommended`: most useful next action, or `none`
- `risks`: unresolved risks and omitted validation, or `none`
- `skill_resolution`: create/update choice, resolved name/path, and equivalence evidence
