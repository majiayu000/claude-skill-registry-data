---
name: java-migration-skill-registry
description: >-
  Registry of version-scoped migration recipes (jade-recipe-*) and auto-generated
  migration skills produced by the Skill-Creator agent. Each subdirectory holds
  versioned skills/recipes for a specific version jump. Recipes here are transform
  scripts + docs, NOT first-class agent skills — they are nested below the
  skills/*/SKILL.md discovery depth and are invoked only by jade-core-rule-dispatcher
  via recipe-registry.json. Not a command — background knowledge only.
user-invocable: false
disable-model-invocation: true
---

# Java Migration Skill Registry

Version-scoped migration recipes and auto-generated skills live here, organized by
version jump. Hand-authored pipeline (core) skills live in sibling directories under
`.claude/skills/`.

## What lives here

Two kinds of content share this registry:

1. **Recipes (`jade-recipe-*`)** — deterministic transform scripts + their docs.
   They are invoked as subprocesses by `jade-core-rule-dispatcher` (never as skills).
   Nested below the version-jump directory, so they are NOT auto-discovered into the
   agent skill inventory (OpenCode only discovers `skills/*/SKILL.md`, one level deep).
2. **Auto-generated skills** — improvements produced by the Skill-Creator agent,
   benchmarked against `eval_cases.json` before acceptance.

## Structure

```
java-migration-skill-registry/
├── 1.5-to-1.6/          ← Java 1.5 → 1.6 recipes
│   ├── jade-recipe-1.5-1.6-arrays-copyof/
│   │   ├── SKILL.md          ← docs + agent-fallback instructions
│   │   └── scripts/apply.py  ← deterministic transform
│   ├── ...
│   └── README.md
├── 1.7/                ← Java 1.7 recipes
├── shared/             ← version-agnostic pipeline recipes (noop fallback, dummy E2E)
├── scripts/register_recipe.py   ← canonical recipe scaffold + registry updater
└── SKILL.md            ← this file
```

Each recipe directory keeps its `SKILL.md` (human/agent docs) and `scripts/apply.py`.
The `SKILL.md` filename is retained for readability and consistency; because recipes
sit two levels under `.claude/skills/`, they are outside OpenCode's
`skills/*/SKILL.md` discovery pattern and never enter the agent's skill list.

## How recipes are wired

`jade-core-rule-dispatcher/recipe-registry.json` maps `rule_id` to the recipe script
path (relative to repo root). The dispatcher runs
`python <script> --file <path> --line <N>` as a subprocess — it never loads the
`SKILL.md`. The `SKILL.md` only matters for humans and for subagents that need
fallback instructions when a deterministic transform defers a case.

## Registering a recipe

Use the deterministic scaffold and registry updater:

```text
python .claude/skills/java-migration-skill-registry/scripts/register_recipe.py \
  --recipe-name example --bucket 1.7 --rule-id EXAMPLE_RULE \
  --description "Apply the example transform"
```

The helper validates safe path segments, refuses duplicates unless `--force` is
given, creates `SKILL.md` and `scripts/apply.py`, and atomically updates the
dispatcher registry. Use `--source-dir` to copy an existing recipe's two files.

## How skills enter this registry

1. Tester agent collects failure patterns from a migrated workspace
2. Skill-Creator generates or improves a skill for the pattern
3. Skill is benchmarked against `benchmarks/<version>/eval_cases.json`
4. Pass rate must exceed the previous version's rate to be committed here

## Current status

The 1.5→1.6 and 1.7 recipes are hand-authored and live here. The
`shared/` bucket holds the version-agnostic `noop` fallback and `dummy` E2E recipes.
No auto-generated (Skill-Creator) skills have been committed yet. The registry
remains the source of truth for dispatcher script paths.
