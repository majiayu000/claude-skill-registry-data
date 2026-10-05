---
name: deployment-management
displayName: Deployment Management
tagline: Manage deployments with rollback strategies, canary releases, and environment promotion.
description: |
  Manages application deployments across environments with strategies like
  blue-green, canary, and rolling updates. Tracks deployment history,
  provides rollback capabilities, and monitors health checks post-deploy.
  Ensures safe and reliable releases to production.
department:
  - Engineering
  - DevOps
use_cases:
  - Deployment
  - Release Management
  - Infrastructure
tools_required:
  - GitHub MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Set up a canary deployment strategy for our API service.
  Promote from staging -> canary (10%) -> production.
exampleOutput: |
  Deployment Strategy — API Service

  ENVIRONMENTS
  Staging:     Auto-deploy on develop branch
  Canary:      10% traffic, 30min observation
  Production:  Promote after canary health check

  HEALTH CHECKS
  - Error rate < 0.1%
  - P99 latency < 500ms
  - No crash loops in 30 minutes

  ROLLBACK PLAN
  Automatic:   If health checks fail during canary
  Manual:      One-command rollback to previous version
  History:     Last 10 deployments tracked
---

# Deployment Management

Manage deployments with rollback strategies, canary releases, and environment promotion.

**Integrations:** GitHub

## When to Use

- The user wants to set up safe deployment strategies
- Production deployments need canary or blue-green approaches
- The user mentions "deployment", "rollback", or "canary release"

## Steps

### Step 1: Define Environments

Configure staging, canary, and production environments.

### Step 2: Set Health Checks

Define metrics that determine deployment success or failure.

### Step 3: Configure Rollback

Set up automatic and manual rollback procedures.

## Output

Deliver:
- Deployment strategy configuration
- Health check definitions
- Rollback procedures and history tracking
