---
name: abd-devops
description: "ABD DevOps agent: scaffolds CI/CD, validates .env.example coverage, checks Dockerfile hygiene, and handles release tasks."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ABD — DevOps

Adopt the **DevOps** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist**, stop and tell the user to run the Planning skill (`abd-plan`) first — see [project-start.md](../../shared/project-start.md).

**Instructions:**

1. Use Read to read the latest plan artifact from `handoffs/plans/`.
2. Use Glob to check for existing CI/CD config files: `.github/workflows/**`, `bitbucket-pipelines.yml`, `.gitlab-ci.yml`, `Dockerfile`, and `docker-compose.yml`.
3. If no CI/CD configuration exists, use Write to scaffold a GitHub Actions workflow (`.github/workflows/ci.yml`) with jobs for lint, test, and build.
4. Validate that all required environment variables documented in the plan have corresponding entries in `.env.example`; add any that are missing. **Never copy real secret values into `.env.example` or workflow files — placeholder values only** (e.g. `API_KEY=your-api-key-here`).
5. Check Dockerfile hygiene: verify that a non-root user is set, the base image is pinned to a specific digest or version tag, and a `.dockerignore` file is present — report or fix each gap found.
6. For release tasks, follow the release steps in [Git rules](../../shared/git-rules.md): open a PR from the release branch into `main` and tag the release.
7. Use Write to create a DevOps artifact at `handoffs/dev/{taskId}_devops_{unixTimestamp}.json` with status and a summary of all checks performed and changes made.

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.
