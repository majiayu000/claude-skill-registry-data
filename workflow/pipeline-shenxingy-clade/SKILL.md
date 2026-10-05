---
name: pipeline
description: Check health of registered background pipelines across all projects. Shows HEALTHY/DEGRADED/DEAD status. Run /pipeline [project-name] to filter.
when_to_use: "check pipeline, pipeline health, background pipeline status"
argument-hint: '[project-name] [watch]'
user_invocable: true
---

# Pipeline Skill

Checks the health of all registered background pipelines and displays a status dashboard.

## What it does

1. Reads `~/.claude/pipeline-registry.yml` for registered project paths
2. For each project, reads `PROJECT/.claude/pipeline.yml` for pipeline definitions
3. Runs health checks (systemd, port, process, logfile)
4. Displays a clean dashboard with HEALTHY / DEGRADED / DEAD indicators

## Usage

```
/pipeline                    # Check all registered projects
/pipeline deepfake            # Filter to projects matching "deepfake"
/pipeline watch               # Instructions for continuous watch mode
```
