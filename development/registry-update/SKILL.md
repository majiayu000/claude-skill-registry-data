---
name: Registry Update
description: Updates the Betty Framework Skill Registry when new skills are created or validated.
---

# registry.update

## Purpose

The `registry.update` skill centralizes all changes to `/registry/skills.json`.
Instead of each skill writing to the registry directly, they call this skill to ensure consistency, policy enforcement, and audit logging.

## Usage

### Basic Usage

```bash
python skills/registry.update/registry_update.py <path_to_skill.yaml>
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| manifest_path | string | Yes | Path to the skill manifest file (skill.yaml) |

## Behavior

1. **Policy Enforcement**: Runs `policy.enforce` skill (if available) to validate the manifest against organizational policies
2. **Load Manifest**: Reads and parses the skill manifest YAML
3. **Update Registry**: Adds or updates the skill entry in `/registry/skills.json`
4. **Thread-Safe**: Uses file locking to ensure safe concurrent updates
5. **Audit Trail**: Records all registry modifications

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "success",
  "errors": [],
  "path": "skills/api.validate/skill.yaml",
  "details": {
    "skill_name": "api.validate",
    "version": "0.1.0",
    "action": "updated",
    "registry_file": "/registry/skills.json",
    "policy_enforced": true
  }
}
```

### Failure Response (Policy Violation)

```json
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Policy violations detected:",
    "  - Skill name must follow domain.action pattern",
    "  - Description must be at least 20 characters"
  ],
  "path": "skills/bad-skill/skill.yaml"
}
```

## Policy Enforcement

Before updating the registry, this skill runs `policy.enforce` (if available) to validate:

- **Naming Conventions**: Skills follow `domain.action` pattern
- **Required Fields**: All mandatory fields present and valid
- **Dependencies**: Referenced dependencies exist in registry
- **Version Conflicts**: No version conflicts with existing skills

If policy enforcement fails, the registry update is **blocked** and errors are returned.

## Thread Safety

The skill uses file locking via `safe_update_json` to ensure:
- Multiple concurrent updates don't corrupt the registry
- Atomic read-modify-write operations
- Proper error handling and rollback on failure

## Integration

### With skill.define

`skill.define` automatically calls `registry.update` after validation:

```bash
# This validates AND updates registry
python skills/skill.define/skill_define.py skills/my.skill/skill.yaml
```

### With skill.create

`skill.create` scaffolds a skill and registers it:

```bash
python skills/skill.create/skill_create.py my.skill "Does something"
# Internally calls skill.define which calls registry.update
```

### Direct Usage

For manual registry updates:

```bash
python skills/registry.update/registry_update.py skills/custom.skill/skill.yaml
```

## Registry Structure

The `/registry/skills.json` file has this structure:

```json
{
  "registry_version": "1.0.0",
  "generated_at": "2025-10-23T12:00:00Z",
  "skills": [
    {
      "name": "api.validate",
      "version": "0.1.0",
      "description": "Validate OpenAPI specifications",
      "inputs": ["spec_path", "guideline_set"],
      "outputs": ["validation_report", "valid"],
      "dependencies": ["context.schema"],
      "status": "active",
      "entrypoints": [...],
      "tags": ["api", "validation"]
    }
  ]
}
```

## Files Modified

- **Registry**: `/registry/skills.json` – Updated with skill entry
- **Logs**: Registry updates logged to Betty's logging system

## Exit Codes

- **0**: Success (registry updated)
- **1**: Failure (policy violation or update failed)

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Manifest file not found" | Path incorrect or file doesn't exist | Check the path to skill.yaml |
| "Policy violations detected" | Skill doesn't meet requirements | Fix policy violations listed in errors |
| "Invalid YAML in manifest" | Malformed YAML syntax | Fix YAML syntax errors |

## Best Practices

1. **Use via skill.define**: Don't call directly unless needed
2. **Policy Compliance**: Ensure skills pass policy checks before registration
3. **Version Control**: Keep registry changes in git for full history
4. **Atomic Updates**: The skill handles thread safety automatically

## See Also

- **skill.define** – Validates manifests before calling registry.update ([skill.define SKILL.md](../skill.define/SKILL.md))
- **policy.enforce** – Enforces organizational policies (if configured)
- **Betty Architecture** – [Five-Layer Model](../../docs/betty-architecture.md)

## Status

**Active** – Production-ready, core infrastructure skill

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with policy enforcement and thread-safe updates
