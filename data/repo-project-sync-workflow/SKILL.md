---
name: repo-project-sync-workflow
description: "When editing KINTSUGI notebook modules (Kdecon, Kstitch, Kreg, etc.), always edit the main repo first then sync to project folders"
author: Claude Code
date: 2025-12-17
---

# KINTSUGI Repository-to-Project Sync Workflow

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-17 |
| **Goal** | Establish correct workflow for editing shared notebook modules |
| **Environment** | KINTSUGI multi-project setup with shared codebase |
| **Status** | Success |

## Context
KINTSUGI uses a shared codebase model where:
- **Main repo**: `/blue/maigan/smith6jt/KINTSUGI/` contains the source code
- **Project folders**: `/blue/maigan/smith6jt/KINTSUGI_Projects/.../notebooks/` contain working copies

Project folders sync FROM the main repo. If you edit a project folder directly, those changes will be **overwritten** when the user syncs from the main repo.

## Verified Workflow

### CORRECT: Edit Main Repo First
```bash
# 1. Make edits to the main repo
/blue/maigan/smith6jt/KINTSUGI/notebooks/Kdecon/deconvolution.py

# 2. User syncs to project folder (or you can do it)
cp /blue/maigan/smith6jt/KINTSUGI/notebooks/Kdecon/*.py \
   /blue/maigan/smith6jt/KINTSUGI_Projects/.../notebooks/Kdecon/
```

### Key Paths
| Component | Main Repo Path | Project Folder Path |
|-----------|---------------|---------------------|
| KDecon | `KINTSUGI/notebooks/Kdecon/` | `KINTSUGI_Projects/.../notebooks/Kdecon/` |
| Kstitch | `KINTSUGI/notebooks/Kstitch/` | `KINTSUGI_Projects/.../notebooks/Kstitch/` |
| Kreg | `KINTSUGI/notebooks/Kreg/` | `KINTSUGI_Projects/.../notebooks/Kreg/` |
| Kview2 | `KINTSUGI/notebooks/Kview2/` | `KINTSUGI_Projects/.../notebooks/Kview2/` |
| src/kintsugi | `KINTSUGI/src/kintsugi/` | N/A (installed package) |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Editing project folder first | User synced from main repo, overwriting all changes | Always edit main repo first |
| Copying project→main after edit | Creates confusion about source of truth | Main repo is ALWAYS the source |

## Key Insights
- The main repo (`/blue/maigan/smith6jt/KINTSUGI/`) is the **single source of truth**
- Project folders are working copies that get synced FROM main repo
- After editing main repo, remind user to sync OR sync for them
- When user reports a fix "didn't work", check if they synced (overwriting your changes)
- Jupyter kernels cache imports - remind user to restart kernel after sync

## Trigger Conditions
This skill applies when:
- Editing any file in `KINTSUGI/notebooks/` subdirectories (Kdecon, Kstitch, Kreg, Kview2, etc.)
- User mentions syncing or copying files between repos
- A fix "doesn't work" after being applied
- Working with KINTSUGI_Projects folders

## References
- KINTSUGI CLAUDE.md development workspace section
- VS Code multi-root workspace: `kintsugi-dev.code-workspace`
