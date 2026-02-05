---
name: changesets-config-generator
description: Generate Changesets configuration for managing versioning and changelogs in monorepos. Triggers on "create changesets config", "generate changeset configuration", "changesets setup", "versioning config".
---

# Changesets Config Generator

Generate Changesets configuration for semantic versioning and changelog management.

## Output Requirements

**File Output:** `.changeset/config.json`
**Format:** Valid JSON configuration
**Standards:** Changesets 2.x

## When Invoked

Immediately generate a complete Changesets configuration for the monorepo.

## Example Invocations

**Prompt:** "Create changesets config for monorepo"
**Output:** Complete `.changeset/config.json` with versioning rules.
