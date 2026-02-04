---
name: gomplate-manager
description: Validate gomplate templates against best practices (Rule 095). Use when user says "/gomplate", "validate templates", "check gomplate", "template best practices".
tools: Read, Glob, Grep, Bash, AskUserQuestion
---

# Gomplate Manager Skill

Validate gomplate templates and configuration against Rule 095 best practices.

## Activation Triggers

- User invokes `/gomplate` command
- User says "validate templates", "check gomplate"
- User says "template best practices", "audit templates"

## Workflow

### Step 1: Locate Configuration

Find gomplate.yaml in the project:

```bash
# Check standard locations
.claude/config/gomplate.yaml
./config/gomplate.yaml
```

### Step 2: Run Python Validator

Execute the validation script:

```bash
# Run validation (text output)
uv run --directory ${CLAUDE_SKILLS_PATH}/gomplate-manager python -m scripts .claude/config/gomplate.yaml

# Run validation (JSON output)
uv run --directory ${CLAUDE_SKILLS_PATH}/gomplate-manager python -m scripts .claude/config/gomplate.yaml --format json

# Strict mode (treat warnings as errors)
uv run --directory ${CLAUDE_SKILLS_PATH}/gomplate-manager python -m scripts .claude/config/gomplate.yaml --strict

# Dry-run with current environment
uv run --directory ${CLAUDE_SKILLS_PATH}/gomplate-manager python -m scripts .claude/config/gomplate.yaml --dry-run
```

### Step 3: Report Results

Present the validation report to the user with:
- Errors (must fix) - syntax errors, missing variables
- Warnings (should fix) - best practice violations
- Info (optional improvements) - style suggestions

### Step 4: Offer Fixes

If violations found, ask user if they want:
- Detailed fix suggestions
- Automatic fixes applied
- Test render with mock environment

## Validation Rules

| Rule ID | Severity | Description |
|---------|----------|-------------|
| `config-syntax` | ERROR | Valid YAML |
| `config-structure` | ERROR | Required fields present |
| `template-syntax` | ERROR | Valid Go template |
| `env-access-style` | WARNING | Use .Env.VAR (not getenv) |
| `output-path-absolute` | WARNING | Absolute paths |
| `template-whitespace` | INFO | Spaced delimiters |

## Example Output

```
Gomplate Validation Report
==========================
Config: .claude/config/gomplate.yaml

Configuration:
  YAML syntax: VALID
  Input directory: templates/
  Output mapping: CONFIGURED

Templates:
  ansible.cfg: VALID (no variables)
  bashrc.sh: VALID (no variables)
  claude_settings.json: VALID (17 .Env references)
  mcp.json: VALID (1 .Env reference)
  pwsh_profile.ps1: VALID (no variables)
  ssh_config.cfg: VALID (no variables)

Summary: 0 errors, 0 warnings, 0 info
Status: PASSED
```

## Integration

This skill is invoked by:
- `/gomplate` command
- `gomplate-manager` agent
- Direct skill invocation
