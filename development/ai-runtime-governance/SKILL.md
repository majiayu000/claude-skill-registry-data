---
name: ai-runtime-governance
description: Unified governance for local AI tools and developer runtimes. Use this skill to inventory installed AI models, CLIs, and IDEs, map skill/MCP/rules/agent settings and storage paths, run backup and audit workflows, and apply single or global path/config changes with rollback records.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/ai-runtime-governance/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/ai-runtime-governance/SKILL.md`
> Source of truth: `registry/skills/ai-runtime-governance/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# AI Runtime Governance

Use this skill when the user asks to:
- Inventory local AI tooling, models, CLI, IDE, update channels, and config storage
- Normalize or migrate settings/paths across Codex, Claude, Gemini, GitHub CLI, VS Code, Windsurf, and related tools
- Make single-program or global changes with backup, audit trail, and rollback points
- Detect drift (out-of-band manual changes) after governance rollout

## Core Policy

- Default to simulation first
- Always create backup before change
- Record every operation to governance log
- Generate rollback instructions for every applied change
- Do not treat inferred previews as real tool output

## Runtime Workflow

1. Run inventory scan
2. Build change plan (single program, global, or all)
3. Backup target config and path objects
4. Simulate and preview impact
5. Apply changes only with explicit `-Apply`
6. Verify expected post-state
7. Write audit report and rollback metadata
8. Run drift check baseline update

## Commands

### 1) Inventory

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\inventory.ps1
```

### 2) Backup only

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\backup.ps1 -Scope all
```

### 3) Simulate unification (no system changes)

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\apply-path-unify.ps1 -Scope all
```

### 4) Apply unification (real changes)

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\apply-path-unify.ps1 -Scope all -Apply
```

### 5) Drift audit

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\audit-drift.ps1
```

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\audit-drift.ps1 -UpdateBaseline
```

### 6) Change one setting key

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\set-setting.ps1 -Program codex -Key model_reasoning_effort -Value medium
```

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\set-setting.ps1 -Program codex -Key model_reasoning_effort -Value medium -Apply
```

### 7) Enable governance guard (scheduled drift audit)

```powershell
pwsh -File C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\install-guard-task.ps1 -Mode enable
```

## Scope Modes

- `-Scope single -Program codex|claude|gemini|gh|vscode|windsurf`
- `-Scope global` for user-level shared paths and baseline
- `-Scope all` for end-to-end multi-program changes

## Governance Convention

To enforce centralized governance by process:
- Require all future config edits to be executed through this skill's scripts
- Treat drift findings as policy violations until reconciled
- Keep immutable operation history under `C:\Dev\AI_UNIFIED\ops\history`

This does not hook kernel/file-system enforcement. It enforces through operational policy, audit logs, and drift detection.

## References

- Read [references/program-map.md](references/program-map.md) for default path map and update behavior
- Read [references/change-contract.md](references/change-contract.md) for report contract and rollback checklist
