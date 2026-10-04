---
name: playbook-installer
description: Guide adoption of AI-Engineering-Playbook governance files in a portable, repeatable way across repositories.
metadata:
  short-description: Onboard repositories to the playbook safely
---

# playbook-installer

## Purpose During Development

Use this skill when a repository needs to adopt AI-Engineering-Playbook governance files in a portable, repeatable way.

This is a development-time onboarding skill. It must not create runtime coupling to application code.

## When To Apply

- setting up a new repository for Codex governance
- standardizing `AGENTS.md` and `skills/` layout across multiple repos
- migrating a repository from ad hoc prompts to playbook-based workflows

## What To Inspect

- repository root for an existing `AGENTS.md`
- repository root for an existing `skills/` directory
- existing governance or contributing docs that may conflict
- any repo-specific boundaries that must be preserved during adoption

## Rules To Enforce

- treat governance artifacts as non-runtime files
- prefer additive adoption first, then tighten rules iteratively
- preserve repository-specific boundaries while importing generic playbook rules
- avoid overwriting existing governance files without explicit confirmation

## Common Anti-Patterns To Catch

- adding playbook guidance into runtime source directories
- copying templates verbatim without repo-specific customization
- enabling strict-mode requirements without updating team-facing docs
- introducing slash aliases without clarifying what performs installation actions

## Expected Output From The Agent

- adoption plan with ordered steps
- file-level changes required for onboarding
- compatibility and migration risks
- minimal validation checklist after adoption

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Use playbook-installer to onboard this repo to AI-Engineering-Playbook."

"Install governance files and create a safe migration plan for existing AGENTS guidance."
