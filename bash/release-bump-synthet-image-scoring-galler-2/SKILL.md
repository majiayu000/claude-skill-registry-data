---
name: release-bump
description: Use when cutting a release, bumping project version, promoting the changelog Unreleased section, tagging release prep, or applying a semver rubric. Includes verification steps before committing release changes.
capability: "release-bump agent asset workflow"
side_effect_level: local_write
approval_required: false
requires_tools: "python scripts/harness.py; git log; project verify commands"
output_schema: "Harness JSON/summary with current/proposed version, Unreleased bullets, verify commands"
risk_class: medium
---

# Release bump (compiled harness)

Thin bootloader. Deterministic work lives in the harness; you only decide the semver level.

## Invoke

```bash
# Inspect current version + Unreleased bullets (no writes)
python scripts/harness.py --json

# After choosing major|minor|patch, apply VERSION + CHANGELOG
python scripts/harness.py --level minor --apply --json
```

## LLM judgment slots

1. **Choose bump level** from `git log <last-tag>..HEAD` and harness `unreleased_bullets`:
   - **major** — breaking API/config/schema/CLI change
   - **minor** — backward-compatible capability
   - **patch** — bugfix, docs, internal refactor
2. State the level and 1–2 justifying changes, then pass `--level`.

## Human authority

Do **not** commit, tag, or push unless the user explicitly asks. Suggest
`chore(release): vX.Y.Z` and annotated tag only after verify commands succeed.

## Verify

Run every command listed in harness `verify_commands` (or the self-verify set in `README.md`)
before any release commit.

Resolve helper paths from this skill directory. Run project commands from the target workspace.
