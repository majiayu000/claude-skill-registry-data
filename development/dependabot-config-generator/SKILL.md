---
name: dependabot-config-generator
description: Generate Dependabot configuration for GitHub automated dependency updates. Triggers on "create dependabot config", "generate dependabot configuration", "dependabot setup", "github dependency updates".
---

# Dependabot Config Generator

Generate GitHub Dependabot configuration for automated dependency updates.

## Output Requirements

**File Output:** `.github/dependabot.yml`
**Format:** Valid Dependabot YAML configuration
**Standards:** GitHub Dependabot v2

## When Invoked

Immediately generate a complete Dependabot configuration for the project.

## Example Invocations

**Prompt:** "Create dependabot config for npm and GitHub Actions"
**Output:** Complete `.github/dependabot.yml` with npm and actions updates.
