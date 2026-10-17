---
name: runbook-automator
description: "Runbook automator: generates a deployment runbook from docker-compose.yml, package.json scripts, CI/CD config, healthcheck endpoints, Dockerfile, and README shell commands. Collector scans all five surfaces; LLM assembles a structured runbook with setup, dev workflow, deployment, healthcheck, crash recovery, CI/CD description, and troubleshooting. Read-only. Audience: Both. Trigger: /runbook"
trigger: /runbook
---

## What this is for

Deployment runbooks are always out of date. This skill regenerates one from the live source of truth: docker-compose.yml defines services/ports/volumes, package.json defines dev/build/test/lint workflow, CI config defines pipeline stages, Dockerfile defines the build, healthcheck endpoints define what liveness looks like, and README contains the tribal-knowledge shell commands.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/runbook-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. Generate a structured runbook with these sections:

### Step 5

- **Setup steps:** prerequisites, docker-compose up, .env template, dependency installation

### Step 6

- **Dev workflow:** how to run dev server, run tests, lint, typecheck, build

### Step 7

- **Deployment procedure:** pipeline stages, build artifact, deploy commands, rollback

### Step 8

- **Healthcheck procedure:** endpoint URLs, expected status codes, what each endpoint validates

### Step 9

- **Crash recovery:** container restart policy, healthcheck failure action, log locations, dump locations

### Step 10

- **CI/CD pipeline description:** trigger events, job dependency graph, what each job does

### Step 11

- **Troubleshooting:** extracted README commands for common operations, port conflicts, volume issues

### Step 12

5. Write `runbook.md` to the working directory.

## Usage

```
/runbook                           # interactive
/runbook <dir>                     # scan project
/runbook -help                     # show usage
```

Returns JSON with `services[]`, `scripts[]`, `ci[]`, `docker{}`, `endpoints[]`, `healthcheckPaths[]`, `readmeCommands[]` plus summary counts.
