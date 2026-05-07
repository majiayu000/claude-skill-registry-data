# Claude Skill Registry (Data)

<p align="center">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry-core%2Fstats.json&query=%24.archive_skill_md_count_raw&label=SKILL.md%20files%20(raw)&color=blueviolet&style=flat-square" alt="SKILL.md files (raw)">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry-core%2Fstats.json&query=%24.archive_metadata_count_raw&label=metadata.json%20files%20(raw)&color=0a7ea4&style=flat-square" alt="metadata.json files (raw)">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry-core%2Fstats.json&query=%24.updated_at&label=Updated%20UTC&color=2ea043&style=flat-square" alt="Updated UTC">
</p>

This repo contains the **archived skill contents** (the heavy, browsable skill files).

**Canonical layout**
- Category folders at repo root (e.g. `development/`, `documents/`, `data/`, ...)
- Each skill lives under a category: `<category>/<skill>/SKILL.md` + `<category>/<skill>/metadata.json`
- Case conflicts are resolved with `{name}-{owner}-{repo}` suffixes (fallback: `-{short-hash}`).

**Archive status**
- Live badges above are sourced from `claude-skill-registry-core` `stats.json`.
- Counts in this README are intentionally dynamic, not hardcoded.
- If the badges look stale, refresh the `core` build/index pipeline rather than editing numbers here.

**Where the index + site live**
- Core repo: https://github.com/majiayu000/claude-skill-registry-core
- Main repo (merged publish artifact): https://github.com/majiayu000/claude-skill-registry

## Tooling

Local validation and stats helpers live under `tools/`. They have no third-party
dependencies in default mode (pure stdlib); installing `jsonschema` enables the
full Draft 2020-12 validator path.

- `schemas/skill-metadata.schema.json` — JSON Schema for per-skill `metadata.json`.
- `tools/validate_metadata.py` — schema, filesystem-agreement and SKILL.md
  cross-checks. Use `--sample N` for a quick smoke run, `--paths a/b/metadata.json`
  to limit a check to a few files (used by CI for changed-only PR validation),
  and `--json out.json` to dump a machine-readable report.
- `tools/repo_stats.py` — coverage and category statistics in `text`,
  `markdown` or `json` format. Useful for refreshing README tables or feeding
  the upstream `core` `stats.json` pipeline.

Run the unit tests with `python3 -m unittest discover tools/ -v`.

CI runs the same tools on every push to `main` and on every pull request that
touches `metadata.json`, `SKILL.md`, `schemas/` or `tools/` — see
`.github/workflows/validate.yml`.
