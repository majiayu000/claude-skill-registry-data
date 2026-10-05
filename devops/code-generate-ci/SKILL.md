---
name: code-generate-ci
description: Generate or update CI/CD pipeline configuration. Use when asked to add or change GitHub Actions, GitLab CI, Jenkins, or other pipeline config.
---

Generate minimal CI/CD configurations matching existing project conventions.

## Process

### Step 1 - Identify Context

- If code changes are involved, run `jj diff -s` for changed files, then `jj diff -- path` to restrict scope.
- Focus on specified provider, platform, branch policy, deployment target, or commands.
- Identify the pipeline goal (e.g., lint, check, test, build, release, or deploy).

### Step 2 - Research and Plan

Apply a researcher lens to research current official CI provider syntax, action versions, permission requirements, and cache patterns for {provider}:

- Prefer official documentation over blog posts.
- Cite sources with URLs.
- Separate confirmed facts from plausible interpretations.
- Note version requirements.
- Lead with the single most actionable recommendation.

Apply a planner lens to design a minimal CI pipeline for the requested goal using existing commands and conventions:

- Prefer simple, boring solutions.
- Preserve existing project patterns.
- Make tradeoffs and assumptions explicit.
- Scope the plan to the current problem.

Apply a reviewer lens to review the proposed CI design for secret leaks, script injection, unsafe permissions, insecure pull-request handling, and unnecessary complexity:

- Ground findings in file paths and line numbers.
- Prioritize the requested lens.
- Distinguish confirmed findings from speculative risks.
- Explain why each issue matters.

### Step 3 - Inspect Conventions

- Locate existing CI/CD config files, task runners, and instruction files (`README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `GEMINI.md`, `CODEX.md`).
- Ensure syntax, action versions, permissions, and cache patterns align with current official provider guidelines.

### Step 4 - Generate CI Config

- Generate a minimal pipeline for the goal (typically lint/check → test → build → deploy only when required).
- Prefer existing wrapper scripts and documented task-runner commands.
- Use least-privilege permissions; avoid exposing secrets; mitigate script injection, unsafe pull-request handling, and poor cache keys.

### Step 5 - Verify

- Run YAML formatting, schema validation, provider-specific checks, or dry-run tools when available.
- If local validation is unavailable, explain manual verification steps and platform-specific risks.

### Step 6 - Report

Report the following:

1. **Pipeline Goal**
2. **Conventions Detected**
3. **CI/CD Config Added / Files Changed**
4. **Verification Results**
5. **Remaining Follow-up**
