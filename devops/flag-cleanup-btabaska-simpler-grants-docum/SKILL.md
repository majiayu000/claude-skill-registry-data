---
name: Feature Flag Cleanup
description: "Workflow for safely removing a fully-rolled-out feature flag from the codebase. Identifies all flag check points across all surfaces (Terraform, API, frontend), removes them while preserving the enabled behavior, updates tests, and verifies nothing broke. Use when a release gate has been fully rolled out and it's time to remove the flag."
model: inherit
---

## When to Use

Invoke this skill when:
- A release gate feature flag has been fully rolled out and is ready for removal
- A kill switch is no longer needed
- Technical debt cleanup of old feature flags

## Step-by-Step Instructions

### Step 1: Identify the Flag

1. Get the flag name from the developer
2. Search for all references across the codebase:
   - Terraform SSM parameters: `infra/` directory
   - API service layer: `api/src/services/` and `api/src/`
   - Frontend hooks: `frontend/src/hooks/useFeatureFlag`
   - Frontend components: conditional rendering based on the flag
   - Tests: flag-dependent test branches
   - Environment configs: `.env` files, Docker configs
3. Document every file containing a flag reference in the blast radius template

### Step 2: Verify Flag State

1. Confirm the flag is currently ENABLED in production
2. Confirm the flag has been enabled long enough (ask the developer)
3. Confirm no active incidents related to the flagged feature
4. If the flag is a kill switch, confirm the team agrees it's no longer needed

### Step 3: Plan the Removal

For each flag reference, determine what happens when the flag is removed:
- **Conditional code blocks**: Keep the "enabled" branch, remove the "disabled" branch
- **Test branches**: Keep tests for the enabled behavior, remove flag-specific test splits
- **Terraform SSM parameter**: Mark for deletion
- **Environment variables**: Mark for removal from all configs

Use `cleanup-checklist.md` and `blast-radius-template.md` to track.

### Step 4: Execute the Removal

Follow this order:
1. **Frontend**: Remove flag checks, keep enabled UI
2. **API**: Remove flag checks, keep enabled logic
3. **Tests**: Remove flag-conditional test branches, keep enabled-path tests
4. **Terraform**: Remove SSM parameter (or mark for next deploy)
5. **Config files**: Remove env vars

### Step 5: Verify

1. Run full test suite (API + Frontend)
2. Run linting and type checking
3. Verify no remaining references to the flag name
4. Run `/check-conventions` on all modified files
5. Run the Quality Gate Pipeline skill

## Conventions and Best Practices

- Always remove from application code first, infrastructure last
- Keep the "enabled" behavior — that's the production behavior
- Search for the flag name as a string literal, variable name, AND comment reference
- Check both camelCase and snake_case variants of the flag name
- Update any documentation that references the flag
