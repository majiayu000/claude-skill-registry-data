---
name: config-migrations
description: Migrate AICP config schema across versions — rename keys, change shapes (string → list, scalar → object), deprecate keys, add required keys with safe defaults, validate operator config files post-upgrade. Distinct from `config-env` (env var lifecycle) and `config-deploy` (deploy-time selection); this skill is the SCHEMA EVOLUTION track. Loads when the operator says "AICP changed config shape" / "migrate config X" / "upgrade config to new schema" / "add required key Y to all configs" / "rename config key".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# config-migrations

Manage AICP config SCHEMA evolution. When AICP renames a config key, changes
its shape, deprecates a feature, or requires a new key — operator config
files (`config/default.yaml`, `config/profiles/*.yaml`, `~/.aicp/config.yaml`,
`<project>/.aicp/config.yaml`) all need migration. This skill is the
operational lifecycle for those changes.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "AICP changed config shape", "migrate
  config X", "upgrade config to new schema", "add required key Y to all
  configs", "rename config key"
- **Post-upgrade validation**: operator upgraded AICP and wants to verify
  config files still parse correctly under the new schema
- **Schema design**: AICP team is changing config shape and needs to
  release notes + migration tooling
- **Deprecation**: a config key is being removed; need to warn operators
  ahead of removal

Do NOT load when:

- The concern is per-environment config values (load `config-env`)
- The concern is choosing which profile to deploy (load `config-deploy`)
- The concern is feature toggles (load `config-feature-flags`)
- The concern is secrets specifically (load `config-secrets`)

## Operations

### Operation 1 — Plan a config schema change

**When**: AICP team wants to evolve config shape (rename / restructure /
add required key).

**Process**:

1. Identify the change category:
   - **Rename**: `cluster.auto_route` → `routing.fleet_enabled`
   - **Restructure**: `models: [a, b, c]` → `models: {gpu: [a, b], cpu: [c]}`
   - **Add required**: new `version: 2` key required at config root
   - **Deprecate**: `legacy_mode: true` is going away
2. Choose the migration strategy:
   - Backward-compatible: old key still read, new key takes precedence
     when present (preferred — rolling upgrade safe)
   - One-shot: bump a `version:` field; loader rejects old version with
     migration instructions
3. Document the change in `wiki/decisions/00_inbox/<change>-config-migration.md`
   per Knowledge Evolution Standards
4. Update `aicp/config/loader.py` to emit deprecation warnings for old
   keys (so operators see the change before it breaks)

**Quality bar**: NEVER make a config schema change without an in-loader
deprecation warning. Operators need a release-cycle window to migrate
their YAMLs.

### Operation 2 — Migrate operator config files in place

**When**: a schema change has shipped; operator wants to update their
config files to the new shape.

**Process**:

1. Identify which files need migration:
   - `config/default.yaml` (project-shipped — usually already updated)
   - `config/profiles/*.yaml` (project-shipped — should be updated by
     AICP team)
   - `~/.aicp/config.yaml` (operator's user-global — needs operator action)
   - `<project>/.aicp/config.yaml` (operator's per-project — needs action)
2. For each file with the old key:
   - If backward-compatible migration: optional update, but eventually
     required
   - If breaking migration: required update before next AICP run
3. Apply the rename/restructure with `Edit` (NEVER bulk `sed` — operator
   files often have comments and structure that bulk edits damage)
4. Run `aicp --profile-cmd validate` to confirm migrated files are
   schema-valid

**Quality bar**: NEVER skip the validate step after migration. Schema-valid
doesn't mean semantically correct, but it's the floor.

### Operation 3 — Add a `version:` field for one-shot migrations

**When**: AICP needs a hard schema break (no backward-compat possible).

**Process**:

1. Add a `version: <N>` key at the root of `config/default.yaml`
2. In `aicp/config/loader.py`, check the version on load:
   - Missing or older than expected: emit clear error with migration
     instructions (point to a migration script or doc)
   - Matches expected: proceed normally
3. Provide a migration utility (e.g., `aicp --config-migrate <old.yaml>
   <new.yaml>`) that operator can run to auto-upgrade their file
4. Document the version bump in CHANGELOG and CLAUDE.md

**Quality bar**: a hard schema break needs (a) clear error message naming
the version mismatch, (b) the migration utility, (c) docs explaining the
rationale (per Knowledge Evolution Standards — link a decision page).

### Operation 4 — Deprecate a config key

**When**: a feature is being removed; its config key needs to go too.

**Process**:

1. Phase 1 (current release): emit `DeprecationWarning` when the key is
   read; document removal plan in CHANGELOG
2. Phase 2 (next release): remove the key from `config/default.yaml`;
   loader still accepts but warns louder
3. Phase 3 (release after that): loader rejects the key with error
4. Document each phase in `wiki/decisions/00_inbox/<key>-deprecation.md`
   so the timeline is operator-visible

**Quality bar**: NEVER skip Phase 1 (deprecation warning). Operators
configure once and rarely re-read; warnings give them a chance to update
ahead of the breaking removal.

## Gotchas

- **Detection**: agent renames a config key without a deprecation period.
  **Rule**: every rename gets at least one release of backward-compat
  with a deprecation warning.
  **Reasoning**: operator configs aren't test-covered; renames break
  silently if not flagged ahead of the break.

- **Detection**: agent uses bulk `sed` to migrate operator YAML files.
  **Rule**: use `Edit` per-occurrence. YAML files contain comments and
  structure that bulk regex can damage.
  **Reasoning**: bulk edits often produce malformed YAML or destroy
  operator comments documenting why a value was set.

- **Detection**: agent migrates only `config/default.yaml` and forgets profile YAMLs.
  **Rule**: profile YAMLs are derived from default.yaml + overrides;
  schema changes propagate to BOTH.
  **Reasoning**: profiles inherit default's schema; if default changes
  shape, profiles' overrides may target nonexistent keys.

- **Detection**: agent skips `aicp --profile-cmd validate` after migration.
  **Rule**: every migrated file must validate before declaring done.
  **Reasoning**: schema validation is the floor — semantic correctness
  is harder, but at minimum the YAML must parse against the schema.

- **Detection**: agent treats deprecation as instant (skip Phase 1).
  **Rule**: deprecation is a multi-release process: warn → louder warn →
  remove.
  **Reasoning**: operators may not redeploy frequently; instant removal
  breaks production for slow-cycle teams.

## Reference exemplars

- `aicp/config/loader.py` `validate_config()` — schema validation entry point
- `config/default.yaml` — schema source of truth
- `wiki/decisions/01_drafts/aicp-active-state-mechanism-for-hooks.md` —
  example of a schema decision documented (state.yaml shape)
- AICP changelog (if maintained) — migration history reference

## Domain context

AICP's config is a 5-tier overlay
(`default.yaml → profile → user → project → CLI`). Schema changes need
to coordinate with this overlay — a key rename in `default.yaml` must
also rename in profiles, and operators with their own user/project
config files need a migration path. The cost of getting this wrong is
operator-visible: configs that worked yesterday error today.

## Related skills

| Skill | When to use |
|-------|-------------|
| `config-env` | When the lifecycle is env var management generally |
| `config-deploy` | When the concern is which profile activates per environment |
| `config-feature-flags` | When the concern is per-feature toggle (different from schema) |
| `pm-changelog` | When documenting a config migration in release notes |
| `evolve-migrate` | When the migration is broader (data + config + code, not just config) |
