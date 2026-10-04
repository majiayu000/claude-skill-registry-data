---
name: git-workflow-guardrails
description: 'Git and githooks workflow for safe delivery on ndestates-io. Use when committing, pushing, tagging, releasing, or preparing PR. Enforces security checklist before commit/push, tests, clear commits, branch promotion (feature->develop->master), annotated tags.'
argument-hint: 'Scope of change, branch name, and desired tag (if any)'
user-invocable: true
disable-model-invocation: false
---

# Git Workflow Guardrails

The full Git Workflow Guardrails instructions are contained in this SKILL.md (originally sourced from the project's .github/skills/ for dual Copilot/Grok compatibility). Follow the complete workflow, preflight, gates, commit, push, promotion, and tagging steps exactly as documented above and in the body of this file.

## Grok execution notes (ndestates-io)
- Always load `.github/prompts/load-project-cache-first.prompt.md` or relevant TODO/CONCERNS before starting delivery flow.
- Use DDEV for all test/security steps (see ddev-local-runtime).
- Confirm branch aligns with TODO (branch-context if needed).
- Run `ddev exec bash scripts/ci_security_checklist.sh` as the mandatory pre-commit/push gate.
- Update TODO via specialist after delivery steps.
- Follow copilot-instructions.md for DDEV lifecycle, data safety, TODO carry at shutdown.

All steps produce user progress updates. No shortcuts on gates.
