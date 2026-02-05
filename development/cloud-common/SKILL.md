---
name: cloud-common
description: Shared utilities for faber-cloud plugin - configuration loading, pattern resolution, auto-discovery
model: claude-haiku-4-5
allowed-tools: Bash, Read
---

# Cloud Common

Shared utilities used across all faber-cloud skills.

## Purpose

This skill provides:
- Configuration loading from `.fractary/plugins/faber-cloud/config.json` **(in project working directory)**
- Backward compatibility with `faber-cloud.json` and `devops.json` (deprecated)
- Pattern substitution (`{project}`, `{environment}`, etc.)
- Auto-discovery fallbacks when config is missing
- Validation and error handling

**CRITICAL**: Always load config from the **project working directory**, NOT the plugin installation directory.

## Configuration Loading

**Primary config file**: `.fractary/plugins/faber-cloud/config.json` (relative to project root / current working directory)

**Common Mistake**: Do NOT look in `~/.claude/plugins/marketplaces/fractary/plugins/faber-cloud/` - that's the plugin installation directory, not the project config location.

**Automatic migration** (seamless upgrade):
- If `config.json` exists: use it (current standard)
- If `faber-cloud.json` exists: automatically rename to `config.json`
- If `devops.json` exists: show warning to migrate manually

**Migration is automatic and preserves all configuration settings.**

## Components

### scripts/config-loader.sh

Core configuration management:

**Main Functions:**
- `load_faber_cloud_config()` - Load configuration from file or auto-discover (with backward compatibility)
- `resolve_pattern(pattern, environment)` - Substitute placeholders in patterns
- `get_aws_profile(environment)` - Get AWS profile for environment
- `get_config_value(key)` - Get specific config value
- `show_config()` - Display current configuration

**Usage:**
```bash
# Source the loader
source "${SKILL_DIR}/../cloud-common/scripts/config-loader.sh"

# Load configuration (checks config.json, auto-migrates from faber-cloud.json if needed)
load_faber_cloud_config

# Use configuration variables
echo "Project: $PROJECT_NAME"
echo "Provider: $PROVIDER"
echo "IaC Tool: $IAC_TOOL"

# Resolve patterns
USER_NAME=$(resolve_pattern "$USER_NAME_PATTERN" "test")
# Result: corthuxa-core-test-deploy

# Get AWS profile
AWS_PROFILE=$(get_aws_profile "test")
# Result: corthuxa-core-test-deploy
```

**Exported Variables:**
- `PROJECT_NAME` - Project name
- `NAMESPACE` - Project namespace
- `ORGANIZATION` - Organization name
- `PROVIDER` - Cloud provider (aws, gcp, azure)
- `IAC_TOOL` - IaC tool (terraform, pulumi, cdk)
- `AWS_REGION` - AWS region
- `TERRAFORM_DIR` - Terraform directory path
- `IAM_POLICIES_DIR` - IAM policies directory path
- `PROFILE_DISCOVER`, `PROFILE_TEST`, `PROFILE_PROD` - AWS profiles
- `USER_NAME_PATTERN`, `POLICY_NAME_PATTERN` - IAM naming patterns
- `RESOURCE_PREFIX` - Resource naming prefix

### templates/faber-cloud.json.template

Template for generating `.fractary/plugins/faber-cloud/config.json`:
- Placeholders: `{{PROJECT_NAME}}`, `{{NAMESPACE}}`, etc.
- Used by `/fractary-faber-cloud:init` command
- Includes sensible defaults
- Template filename remains `faber-cloud.json.template` for compatibility, generates `config.json`

## Auto-Discovery

When configuration file doesn't exist, auto-discovers:
- Project name from Git repository
- Organization from Git remote
- AWS account ID from credentials
- Provider and IaC tool from installed tools

## Pattern Substitution

Supported placeholders:
- `{project}` - Project name
- `{namespace}` - Project namespace
- `{organization}` - Organization name
- `{environment}` - Current environment (test, prod, etc.)
- `{prefix}` - Resource prefix

Example:
```
Pattern: "{prefix}-{environment}-bucket"
Result: "corthuxa-test-bucket"
```

## Configuration Schema

See `/docs/specs/fractary-faber-cloud-plugin-spec.md` for complete schema.

## Used By

**Infrastructure Skills:**
- infra-architect
- infra-engineer
- infra-validator
- infra-previewer
- infra-deployer
- infra-permission-manager
- infra-tester
- infra-debugger

**Operations Skills:**
- ops-monitor
- ops-investigator
- ops-responder
- ops-auditor

**Handler Skills:**
- handler-hosting-aws
- handler-iac-terraform

**Note:** Previously used by deprecated agents (devops-deployer, devops-debugger, devops-permissions) - now superseded by Phase 1-4 architecture. See `.archive/pre-phase-architecture/` for historical reference.
