---
name: scbe-shopify-money-flow
description: Execute revenue-focused Shopify operations using SCBE and HYDRA command lanes with deterministic evidence, cross-talk dispatch, and workflow tuning. Use when the goal is to improve Shopify conversion, publish or refresh digital offers, coordinate monetization agents, or run pre-launch smoke checks before live store actions.
---

# SCBE Shopify Money Flow

## Workflow

1. Validate browser lane readiness.
```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE
python scripts/system/browser_chain_dispatcher.py --domain admin.shopify.com --task navigate --engine playwriter
playwriter session new
playwriter session list
```

2. Navigate and capture Shopify evidence (read-only baseline).
```powershell
python scripts/system/playwriter_lane_runner.py --session <SESSION_ID> --task navigate --url "https://admin.shopify.com"
python scripts/system/playwriter_lane_runner.py --session <SESSION_ID> --task title
python scripts/system/playwriter_lane_runner.py --session <SESSION_ID> --task snapshot
```

3. Run synthesis health checks before monetization changes.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_synthesis_pipeline.ps1
```

4. Run store launch pack (copy, media, score, optional publish).
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_shopify_store_launch_pack.ps1 -Store "aethermore-code.myshopify.com" -RunBothSideTest
```

5. Dispatch monetization swarm assignments to other agents.
```powershell
python scripts/system/dispatch_monetization_swarm.py --sender "agent.codex" --codename "Revenue-Swarm-01"
python scripts/system/monetization_swarm_status.py --limit 500
```

6. Tune internet workflow profile for repeatable scaling.
```powershell
python C:/Users/issda/.codex/skills/scbe-internet-workflow-synthesis/scripts/synthesize_pipeline_profile.py --repo-root C:/Users/issda/SCBE-AETHERMOORE --output training/internet_workflow_profile.json --force
python C:/Users/issda/.codex/skills/scbe-internet-workflow-synthesis/scripts/run_e2e_pipeline.py --repo-root C:/Users/issda/SCBE-AETHERMOORE --profile training/internet_workflow_profile.json
```

## Output Contract

Persist and review these artifacts each run:
- `artifacts/system_smoke/synthesis_smoke.json`
- `artifacts/system_smoke/synthesis_summary.json`
- `artifacts/page_evidence/synthesis_terminal_browse.json`
- `artifacts/agent_comm/<YYYYMMDD>/monetization-swarm-dispatch-*.json`
- `artifacts/agent_comm/<YYYYMMDD>/monetization-swarm-status-*.json`
- `training/internet_workflow_profile.json`
- `training/internet_workflow_profile.tuned.json`
- `artifacts/internet_workflow_tuning_report.json`

## Guardrails

- Keep `skip_core_check=false` for production runs.
- Do not run live publish actions without explicit instruction.
- Keep secrets in env/secret store; never log tokens in artifacts.
- Treat browser session capture as evidence; keep snapshots and title checks for audit.

## Resources

- `references/money-flow-command-lanes.md`: copy/paste lanes for daily operations.
- `scripts/`: add wrappers for repetitive campaign ops if the same sequence is run more than twice.
