---
name: config-auditor
description: Cross-reference all CLAUDE.md files, memory files, skill descriptions, and project registries for contradictions, stale data, and inconsistencies. Trigger on "check for contradictions", "audit configs", "config consistency", "are my configs consistent", or any request to verify configuration coherence across Project Swarm.
triggers:
  - contradictions
  - audit configs
  - config consistency
  - config audit
  - check configs
  - are my configs consistent
---

# Config Auditor — Cross-Configuration Consistency Checker

## When to Trigger

- "check for contradictions" / "audit configs" / "config consistency"
- After major infrastructure changes (hardware swaps, new hosts, repo changes)
- During skill-updater runs (call this as a sub-check)
- When config was updated in one place but might be stale elsewhere

## What to Check

### 1. Hardware Specs (VERIFY FROM MACHINE)
```bash
# ALWAYS SSH and check before asserting specs
ssh -o ConnectTimeout=5 <host> "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader"
ssh -o ConnectTimeout=5 <host> "lscpu | grep 'Model name\|Socket\|Core'"
ssh -o ConnectTimeout=5 <host> "free -h | head -2"
```
Cross-reference against:
- `~/.claude/CLAUDE.md` (Cluster Infrastructure section)
- `~/.claude/projects/*/memory/user_admin_user.md`
- `~/.claude/skills/ai-cluster-knowledge/SKILL.md` description
- Each host's memory file (project_<hostname>_server.md, etc.)

### 2. Repo Inventory
```bash
gh repo list your-github-user --limit 50 --json name,visibility,isPrivate
```
Cross-reference against:
- `project_repo_status.md` memory
- `project-management/SKILL.md` Repos section
- `CLAUDE.md` GitHub section (visibility claims)

### 3. Skill Count
```bash
ls ~/.claude/skills/ | wc -l
```
Cross-reference against:
- `project_skill_updates.md` memory

### 4. Port Assignments
Grep all CLAUDE.md files for port numbers, check for conflicts:
```bash
grep -rn "port [0-9]\|:[0-9][0-9][0-9][0-9]" /opt/*/CLAUDE.md ~/.claude/CLAUDE.md
```

### 5. ChromaDB Collection Prefixes
Cross-reference CLAUDE.md claims against actual collections:
```bash
# On GPU host:
curl -s http://127.0.0.1:<chromadb-port>/api/v2/collections | python3 -c 'import json,sys; ...'
```

### 6. NVIDIA Driver Version
```bash
ssh <host> "nvidia-smi --query-gpu=driver_version --format=csv,noheader"
```
vs all files that mention driver version.

### 7. Service Versions (Monero)
```bash
monerod --version
```
vs memory files.

### 8. Model Inventory
```bash
curl -s http://127.0.0.1:<ollama-port>/api/tags
```
vs model evaluation doc, ai-cluster-knowledge skill.

### 9. Project Phase Status
Cross-reference:
- `project-management/SKILL.md` Project Registry table
- Each project's CLAUDE.md
- Each project's plans/*.md

## Output Format

Table of contradictions found:
```
| # | Issue | File A says | File B says | Fix |
```

Fix all non-ambiguous contradictions automatically. Ask about ambiguous ones.

## Key Rule
**NEVER update hardware specs without SSHing to the machine first.**
