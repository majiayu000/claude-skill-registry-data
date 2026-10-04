---
name: gcp-onboarding
description: Maintain this repository's GCP onboarding documentation. Use when changes touch Google Cloud setup, OAuth consent or clients, Google API scopes, Secret Manager, Cloud Run, GitHub Pages deployment configuration, backend environment variables, or frontend environment flags that a new project/environment must configure.
---

# GCP Onboarding

When implementing changes that affect environment setup, inspect and maintain:

- `docs/guidelines/gcp-onboarding.md`
- `projects/frontend/README.md`
- `projects/backend/README.md`
- `.github/copilot-instructions.md`

Keep onboarding docs concise and task-oriented. Prefer checklists, exact config names, and copy-pasteable commands. Avoid duplicating the full guide in multiple READMEs; link to `docs/guidelines/gcp-onboarding.md` from local setup sections.

Required checks:

1. If OAuth origins, scopes, consent screen requirements, Google APIs, environment flags, secrets, Cloud Run settings, or deployment commands changed, update `docs/guidelines/gcp-onboarding.md`.
2. If the setup change is not straightforward enough to document safely, add a short note in the PR or implementation summary that onboarding docs need confirmation.
3. Keep existing documentation and links intact unless they are stale.
4. Never include real secrets, private client secrets, or production-only secret values in documentation.
