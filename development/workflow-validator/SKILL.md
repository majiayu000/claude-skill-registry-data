---
name: workflow-validator
description: |
  This skill should be used when the user wants to validate a looplia workflow output,
  check if an artifact meets validation criteria, or debug validation failures. Use when
  someone says "validate this looplia output", "check if the workflow output is valid",
  "verify the artifact JSON", or "debug why validation failed".

  Runs deterministic validation scripts against JSON artifacts. Primarily used for manual
  retry/debugging since automatic validation is handled by PostToolUse hooks. Part of
  looplia's one step → one skill-executor → multiple skills architecture.
---

# Workflow Validator Skill

Validates JSON artifacts against validation criteria using deterministic script execution.

## Automatic Validation via Hook (v0.6.0)

As of v0.6.0, the `PostToolUse:Write` hook **automatically** calls this validation script whenever an artifact is written to `sandbox/*/outputs/*.json`.

**You typically don't need to manually invoke this skill** - the hook handles it.

### When to Manually Use This Skill

Use this skill only in these scenarios:
- **Retrying after validation failure** - when the hook blocked a write and you need to debug
- **Debugging validation issues** - to see detailed check results
- **Checking artifacts outside the normal workflow** - for ad-hoc validation
- **Pre-checking before write** - to validate data before writing to sandbox

## What This Skill Does

- Reads validation criteria from `sandbox/{id}/validation.json`
- Runs deterministic validation script (no LLM tokens consumed)
- Returns pass/fail status with detailed check results
- Enables workflow completion verification

## Validation Process

### Step 1: Read Validation Criteria

Read the validation manifest at `sandbox/{id}/validation.json`:

```json
{
  "workflow": "writing-kit",
  "version": "1.0.0",
  "sandboxId": "article-2025-12-18-xk7m",
  "steps": {
    "summary": {
      "output": "outputs/summary.json",
      "validate": {
        "required_fields": ["contentId", "headline", "tldr", "keyThemes"],
        "min_quotes": 3,
        "min_key_points": 5
      },
      "validated": false
    }
  }
}
```

### Step 2: Run Validation Script

Execute the validation script with artifact path and criteria:

```bash
bun scripts/validate.ts <artifact-path> '<criteria-json>'
```

Example:
```bash
bun scripts/validate.ts sandbox/podcast-2024-12-08-ai/outputs/summary.json '{"required_fields":["contentId","headline"],"min_quotes":3}'
```

### Step 3: Parse Results

The script returns JSON with pass/fail and individual checks:

```json
{
  "passed": true,
  "checks": [
    { "name": "has_contentId", "passed": true, "message": "OK" },
    { "name": "has_headline", "passed": true, "message": "OK" },
    { "name": "min_quotes", "passed": true, "message": "Found 5 quotes (min: 3)" }
  ]
}
```

### Step 4: Handle Results

**If validation passes:**
- Update `validation.json` to set `validated: true` for this output
- Continue to next workflow step

**If validation fails:**
- Review failed checks
- Either retry the subagent with feedback
- Or report the issue to the user

## Validation Criteria Reference

### required_fields
Array of field names that must exist in the artifact:
```json
"required_fields": ["contentId", "headline", "tldr"]
```

### min_quotes
Minimum number of items in `importantQuotes` array:
```json
"min_quotes": 3
```

### min_key_points
Minimum number of items in `bullets` or key points array:
```json
"min_key_points": 5
```

### min_outline_sections
Minimum number of outline sections:
```json
"min_outline_sections": 4
```

### has_hooks
Requires `hooks` array with at least one item:
```json
"has_hooks": true
```

## Output Format

The validation script returns:

```json
{
  "passed": boolean,
  "checks": [
    {
      "name": "check_name",
      "passed": boolean,
      "message": "Human-readable result"
    }
  ]
}
```

## Important Rules

- **Automatic validation via hook** - Hook handles validation on write; manual use only for retry/debugging
- **Script is deterministic** - No LLM context consumed
- **Update validation.json** - Mark steps validated when passed (v0.6.0 uses `.steps` not `.outputs`)
- **Retry on failure** - Give subagent feedback on what failed
- **Check dependencies** - Ensure required steps are validated before dependent steps
- **Use exact paths** - Artifact paths are relative to workspace root

## Script Location

The validation script is at:
```
.claude/skills/workflow-validator/scripts/validate.ts
```

Run with Bun for TypeScript execution:
```bash
bun .claude/skills/workflow-validator/scripts/validate.ts <artifact> '<criteria>'
```
