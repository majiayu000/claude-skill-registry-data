# Claude Skill Registry (Data)

<p align="center">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry%2Fstats.json&query=%24.archive_skill_md_count_raw&label=SKILL.md%20files%20(raw)&color=blueviolet&style=flat-square" alt="SKILL.md files (raw)">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry%2Fstats.json&query=%24.archive_metadata_count_raw&label=metadata.json%20files%20(raw)&color=0a7ea4&style=flat-square" alt="metadata.json files (raw)">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry%2Fstats.json&query=%24.updated_at&label=Updated%20UTC&color=2ea043&style=flat-square" alt="Updated UTC">
</p>

This repo contains the **archived skill contents** (the heavy, browsable skill files).

**Canonical layout**
- Category folders at repo root (e.g. `development/`, `documents/`, `data/`, ...)
- Each skill lives under a category: `<category>/<skill>/metadata.json`, plus `SKILL.md` when its license is an open-source license
- Skills with no license, `NOASSERTION`, proprietary, non-commercial or no-derivatives terms keep `metadata.json` with the source link only. See [NOTICE](NOTICE).
- Case conflicts are resolved with `{name}-{owner}-{repo}` suffixes (fallback: `-{short-hash}`).

**Archive status**
- Live badges above are sourced from the public registry site’s `stats.json`.
- Counts in this README are intentionally dynamic, not hardcoded.
- If the badges look stale, refresh the `core` build/index pipeline rather than editing numbers here.

**Where the index + site live**
- Core repo: https://github.com/majiayu000/claude-skill-registry-core
- Main repo (merged publish artifact): https://github.com/majiayu000/claude-skill-registry

Browse the [public skill search and installation guides](https://majiayu000.github.io/claude-skill-registry/) for discovery. This archive is consumed by the core pipeline; it is not a standalone installer.

## Trace an archived skill

Open `<category>/<skill>/metadata.json`. Use `repo` and
`path` to locate the original file, then follow `source_url` to check the current
upstream version. `downloaded_at` describes the archived copy's timestamp, not a
promise that it matches today's upstream content.

Read `author`, `license`, `permission_note` and `distribution` before reuse.
The registry maintainer is not necessarily the skill author. `NOASSERTION` means
no license assertion was established; `restricted` is not permission to reuse
or redistribute. The pipeline's MIT license does not relicense archived skills.

For example, [`development/0-claude/metadata.json`](development/0-claude/metadata.json)
points to `brixtonpham/claude-config`, records `NOASSERTION`, and marks
distribution as `restricted`, so the archive keeps no copy of its `SKILL.md`.
Follow its `source_url` and the upstream permission terms rather than treating
it as a first-party majiayu000 skill.

Use the [public catalog](https://majiayu000.github.io/claude-skill-registry/) to
find installation guidance instead of installing this archive as one skill.
Report skill behavior problems upstream; send attribution or removal requests
through the [core procedure](https://github.com/majiayu000/claude-skill-registry-core/blob/main/REMOVAL.md).
