---
name: scbe-gh-powershell-workflow
description: Manage GitHub workflows and SCBE-AETHERMOORE repository operations from PowerShell 7 preview. Use for authenticated gh CLI actions, PR and branch workflows, CI triage, and SCBE code-aware repository inspections.
---

# SCBE GitHub + PowerShell 7 Workflow

Use this skill when the user asks to perform `gh` operations, inspect or manipulate SCBE-related GitHub repos, or run GitHub workflow/debug tasks from PowerShell 7 preview.

## Prerequisites
- Use PowerShell 7+ preview:
  - `"$($PSVersionTable.PSVersion.ToString())"` should show `7.6.0-preview.6` or later in this environment.
- Ensure `gh` is installed and authenticated.
- For SCBE repo actions, prefer:
  - local working copy at `C:\Users\issda\SCBE-AETHERMOORE`
  - local workspace at `C:\Users\issda\SCBE-AETHERMOORE-working`
  - or fallback remote target `issdandavis/SCBE-AETHERMOORE`.
- For workflow-architect / demo systems:
  - `C:\Users\issda\Kiro_Version_ai-workflow-architect`
  - `C:\Users\issda\scbe-aethermoore-demo`

## Core GH bootstrap
- Check auth:
  - `gh auth status`
- Re-authenticate if needed:
  - `gh auth login -h github.com`
- Confirm repo aliases:
  - `gh alias list`

## PR and branch workflow
- Checkout a PR by number:
  - `gh pr checkout 204 --repo issdandavis/SCBE-AETHERMOORE`
- If `cl` alias is preferred:
  - `gh alias set cl 'pr checkout' --clobber`
  - `gh cl 204 --repo issdandavis/SCBE-AETHERMOORE`
- View PR without a local checkout:
  - `gh pr view 204 --repo issdandavis/SCBE-AETHERMOORE`
- List PRs:
  - `gh pr list --repo issdandavis/SCBE-AETHERMOORE`

## Repo context rules (important)
- `gh` commands that depend on git metadata require being inside a local git repo.
- From any directory, pass `--repo OWNER/REPO` to inspect objects without local checkout.
- Never assume `gh repo view` without args will work outside a git checkout.

## Multi-repo roots
- SCBE: `C:\Users\issda\SCBE-AETHERMOORE` and `C:\Users\issda\SCBE-AETHERMOORE-working`
- Workflow architect: `C:\Users\issda\Kiro_Version_ai-workflow-architect`
- SCBE demo: `C:\Users\issda\scbe-aethermoore-demo`

## SCBE operational checks
- Before CI triage, gather status:
  - `gh status --repo issdandavis/SCBE-AETHERMOORE`
- Inspect workflow runs:
  - `gh run list --repo issdandavis/SCBE-AETHERMOORE --limit 20`
  - `gh run view <run-id> --repo issdandavis/SCBE-AETHERMOORE --log`
- Open PR diff review flow:
  - `gh pr diff <pr>` if local checkout exists
  - otherwise `gh pr view <pr> --repo issdandavis/SCBE-AETHERMOORE --json files`

## SCBE code assistant
- Use the code assistant script for repeatable, context-aware workflow actions:
  - `.\scripts\scbe_code_assistant.ps1 -Mode status`
  - `.\scripts\scbe_code_assistant.ps1 -Mode checkout-pr -Pr 204`
  - `.\scripts\scbe_code_assistant.ps1 -Mode inspect-pr -Pr 204`
  - `.\scripts\scbe_code_assistant.ps1 -Mode run-list -Limit 30`
  - `.\scripts\scbe_code_assistant.ps1 -Mode run-view -RunId 1234567890`
  - `.\scripts\scbe_code_assistant.ps1 -Mode scbe-self-heal -RepoPath 'C:\Users\issda\SCBE-AETHERMOORE-working'`
  - `.\scripts\scbe_code_assistant.ps1 -Mode scbe-self-heal -SelfHealScript 'C:\path\to\script.ps1'`
  - `.\scripts\scbe_code_assistant.ps1 -Mode self-heal-catalog`
  - `.\scripts\scbe_code_assistant.ps1 -Mode code-assistant-scan`
  - `.\scripts\scbe_code_assistant.ps1 -Mode workflow-architect-scan -RepoPath 'C:\Users\issda\Kiro_Version_ai-workflow-architect'`
- `.\scripts\scbe_code_assistant.ps1 -Mode aethermoore-demo-scan -RepoPath 'C:\Users\issda\scbe-aethermoore-demo'`
- `.\scripts\scbe_code_assistant.ps1 -Mode llm-training -NotionDocPath 'C:\Users\issda\notion-export' -TrainingManifestOutput 'C:\Users\issda\scbe-training-manifest.json'`
- `.\scripts\scbe_code_assistant.ps1 -Mode ai-nodal-dev-specialist -NotionDocPath 'C:\Users\issda\notion-export'`
- `.\scripts\scbe_code_assistant.ps1 -Mode self-heal-catalog -RepoPath 'C:\Users\issda\SCBE-AETHERMOORE-working'`

## 3 inspired-system capabilities included
- Workflow-architect assistant surfaces: scan code-assistant, proposal, and autonomy APIs.
- SCBE-demo self-healing discovery: prioritize `SCBE-AETHERMOORE-v3.0.0/src/selfHealing/*`.
- Cross-repo cataloging: discover and run known healing scripts across all configured SCBE-compatible repos.
- LLM / AI Nodal Dev Specialist preflight modes:
  - `llm-training`: generate non-invasive training manifest + reality checks
  - `ai-nodal-dev-specialist`: adds planner-focused guidance and same manifest output

## Hidden next-coder marker
- A non-code handoff marker is maintained at:
  - `.\.scbe-next-coder-marker.json`
- This file contains mode handoff notes and does not modify product code.

## Three SCBE-inspired workflows
- Governance envelope audit:
  - `.\scripts\scbe_code_assistant.ps1 -Mode scbe-governance`
  - Finds and validates governance decision and envelope-related surfaces in the repo.
- Interoperability parity guard:
  - `.\scripts\scbe_code_assistant.ps1 -Mode scbe-kdf`
  - Checks for KDF and serialization hotspots that can break cross-language parity.
- CI-to-code trace:
  - `.\scripts\scbe_code_assistant.ps1 -Mode scbe-ci`
  - Correlates recent failed runs with likely source files for rapid remediation.

For deeper SCBE context on these flows, read:
- `references/scbe-system-inspired-flows.md`
- `references/scbe-workflow-architect-integration.md`
- For integration behavior and known self-healing assets, read:
- `references/scbe-workflow-architect-integration.md`

## PowerShell 7 execution notes
- Use quoted paths for repo and script paths with spaces.
- Prefer one command per line and avoid implicit shell parsing assumptions from legacy PowerShell.
- When a command fails with “not a git repository,” move into the correct local repo path and rerun with explicit `--repo` only as fallback.

## Internet/research workflow
- Use direct repository-native context first (`gh`, local files, commit/history).
- Use web search only for up-to-date external references (GitHub docs, API changes, upstream packages).
- Keep external references bounded to the exact question to reduce time and ambiguity.

## Failure handling
- If `gh` says “Could not create alias”:
  - rerun with `--clobber`.
- If syntax errors appear (`Invalid workflow file`):
  - inspect YAML for scalar typos and indentation in workflow files immediately.
- If `gh auth` indicates invalid token:
  - re-run `gh auth login` and re-check with `gh auth status`.

## Operational safety
- Do not run destructive git operations unless explicitly requested.
- Avoid pushing secrets in output or logs.
