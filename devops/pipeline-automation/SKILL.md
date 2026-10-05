---
name: pipeline-automation
displayName: Pipeline Automation
tagline: Automate CI/CD pipelines with build, test, and deployment workflows.
description: |
  Creates and optimizes CI/CD pipeline configurations for GitHub Actions,
  Jenkins, or other CI systems. Generates workflow files with build, test,
  lint, and deploy stages. Implements caching strategies, parallel jobs,
  and conditional deployments to reduce build times and improve reliability.
department:
  - Engineering
  - DevOps
use_cases:
  - CI/CD
  - Build Automation
  - Deployment
tools_required:
  - GitHub MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Set up a CI/CD pipeline for a Next.js app deployed to Vercel.
  Include linting, type checking, unit tests, and preview deployments.
exampleOutput: |
  CI/CD Pipeline — Next.js + Vercel

  STAGES
  1. Lint & Format    (30s)  — ESLint + Prettier check
  2. Type Check       (45s)  — TypeScript strict mode
  3. Unit Tests       (2m)   — Jest with coverage >80%
  4. Build            (3m)   — Next.js production build
  5. Preview Deploy   (1m)   — Vercel preview on PRs
  6. Production Deploy (1m)  — Vercel prod on main merge

  OPTIMIZATIONS
  - Dependency caching: ~60% faster installs
  - Parallel stages: lint + type check + tests run together
  - Skip deploy: on docs-only changes

  Generated: .github/workflows/ci.yml
---

# Pipeline Automation

Automate CI/CD pipelines with build, test, and deployment workflows.

**Integrations:** GitHub

## When to Use

- The user wants to set up or optimize CI/CD pipelines
- Build times need to be reduced with caching or parallelization
- The user mentions "CI/CD", "pipeline", "GitHub Actions", or "deployment"

## Steps

### Step 1: Define Pipeline Stages

Determine build, test, and deploy stages based on the project stack.

### Step 2: Generate Workflow Configuration

Create CI/CD workflow files with optimized caching and parallelism.

### Step 3: Add Quality Gates

Configure coverage thresholds, lint rules, and approval requirements.

## Output

Deliver:
- CI/CD workflow configuration files
- Caching and optimization recommendations
- Pipeline performance metrics
