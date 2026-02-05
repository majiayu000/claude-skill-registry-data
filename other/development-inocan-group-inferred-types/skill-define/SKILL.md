---
name: Skill Define
description: Validate and register new Claude Code Skill manifests (.skill.yaml) to ensure structure, inputs/outputs, and dependencies are correct.
---

# skill.define

## Overview

**skill.define** is the compiler and registrar for Betty Framework skills. It ensures each `skill.yaml` conforms to schema and governance rules before registration.

## Purpose

Acts as the quality gate for all skills in the Betty ecosystem:
- **Schema Validation**: Ensures all required fields are present
- **Manifest Parsing**: Validates YAML structure and syntax
- **Registry Integration**: Delegates to `registry.update` for registration
- **Error Reporting**: Provides detailed validation errors for troubleshooting

## Usage

### Basic Usage

```bash
python skills/skill.define/skill_define.py <path_to_skill.yaml>
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| manifest_path | string | Yes | Path to the skill manifest file (skill.yaml) |

## Required Skill Manifest Fields

A valid skill manifest must include:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Unique skill identifier | `api.validate` |
| `version` | string | Semantic version | `0.1.0` |
| `description` | string | What the skill does | `Validates API specifications` |
| `inputs` | array | Input parameters | `["spec_path", "guideline_set"]` |
| `outputs` | array | Output artifacts | `["validation_report"]` |
| `dependencies` | array | Required skills/deps | `["context.schema"]` |
| `status` | string | Skill status | `active` or `draft` |

### Optional Fields

- **entrypoints**: CLI command definitions
- **tags**: Categorization tags
- **permissions**: Required filesystem/network permissions

## Behavior

1. **Load Manifest**: Reads and parses the YAML file
2. **Validate Structure**: Checks for all required fields
3. **Validate Format**: Ensures field types and values are correct
4. **Delegate Registration**: Calls `registry.update` to add skill to registry
5. **Return Results**: Provides JSON response with validation status

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "registered",
  "errors": [],
  "path": "skills/workflow.validate/skill.yaml",
  "details": {
    "valid": true,
    "missing": [],
    "path": "skills/workflow.validate/skill.yaml",
    "manifest": {
      "name": "workflow.validate",
      "version": "0.1.0",
      "description": "Validates workflow YAML definitions",
      "inputs": ["workflow.yaml"],
      "outputs": ["validation_result.json"],
      "dependencies": ["context.schema"],
      "status": "active"
    },
    "status": "registered",
    "registry_updated": true
  }
}
```

### Failure Response (Missing Fields)

```json
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Missing required fields: version, outputs"
  ],
  "path": "skills/my-skill/skill.yaml",
  "details": {
    "valid": false,
    "missing": ["version", "outputs"],
    "path": "skills/my-skill/skill.yaml"
  }
}
```

### Failure Response (Invalid YAML)

```json
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Failed to parse YAML: mapping values are not allowed here"
  ],
  "path": "skills/broken/skill.yaml",
  "details": {
    "valid": false,
    "error": "Failed to parse YAML: mapping values are not allowed here",
    "path": "skills/broken/skill.yaml"
  }
}
```

## Examples

### Example 1: Validate a Complete Skill

**Skill Manifest** (`skills/api.validate/skill.yaml`):

```yaml
name: api.validate
version: 0.1.0
description: "Validate OpenAPI and AsyncAPI specifications against enterprise guidelines"

inputs:
  - name: spec_path
    type: string
    required: true
    description: "Path to the API specification file"
  - name: guideline_set
    type: string
    required: false
    default: zalando
    description: "Which API guidelines to validate against"

outputs:
  - name: validation_report
    type: object
    description: "Detailed validation results"
  - name: valid
    type: boolean
    description: "Whether the spec is valid"

dependencies:
  - context.schema

status: active
tags: [api, validation, openapi]
```

**Validation Command**:

```bash
$ python skills/skill.define/skill_define.py skills/api.validate/skill.yaml
{
  "ok": true,
  "status": "registered",
  "errors": [],
  "path": "skills/api.validate/skill.yaml",
  "details": {
    "valid": true,
    "status": "registered",
    "registry_updated": true
  }
}
```

### Example 2: Detect Missing Fields

**Incomplete Manifest** (`skills/incomplete/skill.yaml`):

```yaml
name: incomplete.skill
description: "This skill is missing required fields"
inputs: []
```

**Validation Result**:

```bash
$ python skills/skill.define/skill_define.py skills/incomplete/skill.yaml
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Missing required fields: version, outputs, dependencies, status"
  ],
  "path": "skills/incomplete/skill.yaml",
  "details": {
    "valid": false,
    "missing": ["version", "outputs", "dependencies", "status"],
    "path": "skills/incomplete/skill.yaml"
  }
}
```

## Integration

### With skill.create

The `skill.create` skill automatically generates a valid manifest and runs `skill.define` to validate it:

```bash
python skills/skill.create/skill_create.py \
  my.skill \
  "Does something useful" \
  --inputs input1,input2 \
  --outputs output1
# Internally runs skill.define on the generated manifest
```

### With Workflows

Skills can be validated as part of a workflow:

```yaml
# workflows/create_and_register.yaml
steps:
  - skill: skill.create
    args: ["workflow.validate", "Validates workflow definitions"]

  - skill: skill.define
    args: ["skills/workflow.validate/skill.yaml"]
    required: true

  - skill: registry.update
    args: ["skills/workflow.validate/skill.yaml"]
```

### With Hooks

Automatically validate skill manifests when they're edited:

```bash
# Create a hook to validate on save
python skills/hook.define/hook_define.py \
  --event on_file_save \
  --pattern "skills/*/skill.yaml" \
  --command "python skills/skill.define/skill_define.py {file_path}" \
  --blocking true
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Manifest file not found" | File path is incorrect | Check the path and ensure file exists |
| "Failed to parse YAML" | Invalid YAML syntax | Fix YAML syntax errors (indentation, quotes, etc.) |
| "Missing required fields: X" | Manifest missing required field(s) | Add the missing field(s) to the manifest |
| "registry.update skill not found" | Registry updater not available | Ensure `registry.update` skill exists in `skills/` directory |

## Relationship with registry.update

`skill.define` **validates** manifests but **delegates registration** to `registry.update`:

1. **skill.define**: Validates the manifest structure
2. **registry.update**: Updates `/registry/skills.json` with the validated skill

This separation of concerns follows Betty's single-responsibility principle.

## Files Read

- **Input**: Skill manifest at specified path (e.g., `skills/my.skill/skill.yaml`)
- **Registry**: May read existing `/registry/skills.json` via delegation to `registry.update`

## Files Modified

- **None directly** – Registry updates are delegated to `registry.update` skill
- **Indirectly**: `/registry/skills.json` updated via `registry.update`

## Exit Codes

- **0**: Success (manifest valid, registration attempted)
- **1**: Failure (validation errors or file not found)

## Logging

Logs validation steps using Betty's logging infrastructure:

```
INFO: Validating manifest: skills/api.validate/skill.yaml
INFO: ✅ Manifest validation passed
INFO: 🔁 Delegating registry update to registry.update skill...
INFO: Registry update succeeded
```

## Best Practices

1. **Run Before Commit**: Validate skill manifests before committing changes
2. **Use with skill.create**: Let `skill.create` generate manifests to ensure correct structure
3. **Check Dependencies**: Ensure any skills listed in `dependencies` exist in the registry
4. **Version Properly**: Follow semantic versioning for skill versions
5. **Complete Descriptions**: Write clear descriptions for inputs, outputs, and the skill itself
6. **Set Status Appropriately**: Use `draft` for development, `active` for production-ready skills

## See Also

- **skill.create** – Generate new skill scaffolding with valid manifest ([skill.create SKILL.md](../skill.create/SKILL.md))
- **registry.update** – Update the skill registry ([registry.update SKILL.md](../registry.update/SKILL.md))
- **Betty Architecture** – Understanding the skill layer ([Five-Layer Model](../../docs/betty-architecture.md))
- **Skill Framework** – Overview of skill categories and design ([Skill Framework](../../docs/skills-framework.md))

## Dependencies

- **registry.update**: For updating the skill registry (delegated call)
- **betty.validation**: Validation utility functions
- **betty.config**: Configuration constants

## Status

**Active** – This skill is production-ready and core to Betty's skill infrastructure.

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with manifest validation and registry delegation
