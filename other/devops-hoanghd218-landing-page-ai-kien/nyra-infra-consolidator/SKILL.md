---
name: nyra-infra-consolidator
description: Consolidate MetaMCP/gateway/docker compose into a single, validated Windows stack (no WSL).
tags: [infra, docker, windows, mcp, compose, consolidation]
category: development
---

# NYRA Infra Swarm (Windows)
**Workspace Root:** `C:\Dev\DevProjects\Personal-Projects\Project-Nyra`

## Goal
Unify scattered MetaMCP/gateway compose files into `infra/compose/compose.metamcp.yml`, standardize `env_file: ["../.env"]`, and validate with `docker compose config`.

## Constraints / Guardrails
- **Default model:** Claude 3.5 Haiku for scans/diffs/YAML edits & quick commands (<30s).
- **Escalate to Sonnet** only if:
  1) `docker compose config` fails **twice** for the same file, or
  2) a single diff > **500 lines**, or
  3) unresolved merge conflict after one retry.
- All file mutations must be **atomic with backup** to `archive/<DATE>-repo-cleanup/` (hooks already back up).
- Never inline secrets; read from `infra/.env`.
- Validate every compose edit with `docker compose -f <file> config --env-file infra/.env`.

## Tools you may run (PowerShell)
- `docker compose -f <file> config --env-file infra/.env`
- `docker compose -f infra/compose/compose.metamcp.yml --env-file infra/.env up -d metamcp`
- `docker compose -f <file> logs --tail=200 <svc>`
- `docker network create nyra-network` (idempotent)
- `git checkout -b infra/cleanup-mcp`
- `git mv <file> archive/<DATE>-repo-cleanup/<same>`
- `git add -A && git commit -m "<message>"`

## Tasks
1) **Inventory**: list all `docker-compose*.yml` and `*compose*.yml` that mention `mcp`, `gateway`, or `metamcp`. Output exact paths.
2) **Unify**: write `infra/compose/compose.metamcp.yml` with:
   - service: `metamcp`, network: `nyra-network`, port `12008:12008`, `env_file: ["../.env"]`.
   - prefer local gateway at `infra/metamcp-gateway` if present; else leave as-is for image use.
3) **Normalize**: ensure all other compose files add `env_file: ["../.env"]` under relevant services.
4) **UI Patches**: change any UI compose references from `http://localhost:8080` to `http://metamcp:12008`.
5) **Scripts**: update `infra/tasks/nyra-envfile-injector.ps1` and `infra/tasks/nyra-metamcp-doctor.ps1` idempotently if needed.
6) **Validate & Run**:
   - `docker network create nyra-network` (ignore exists)
   - `docker compose -f infra/compose/compose.metamcp.yml --env-file infra/.env up -d metamcp`
   - probe APP_URL from `infra/.env` (Bearer and anon).
7) **Git staging**:
   - branch `infra/cleanup-mcp`
   - move old scattered compose/config to `archive/<DATE>-repo-cleanup/`
   - commit with a summary + bullet list of relocated files

## Outputs
- explicit diffs for each file
- commands executed (ordered)
- final status for port 12008 and probes
- short "how to run" snippet
