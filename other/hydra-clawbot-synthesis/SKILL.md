---
name: hydra-clawbot-synthesis
description: Synthesize HYDRA terminal browsing, multi-agent orchestration, Playwright smoke checks, Airtable/Hugging Face dataset handoff, and Obsidian command-lane publishing for Clawbot/OpenClaw operations.
---

# Hydra Clawbot Synthesis

Use this skill when you need one operational loop that combines:
- HYDRA deterministic browsing evidence
- OpenClaw/Clawbot execution against SCBE services
- Playwright reliability checks
- Airtable + Hugging Face dataset routing
- Obsidian command-lane publishing

## Mission Packets

1. `packet_hydra_browse`
- Run terminal-first browse evidence for target URLs.
- Use: `node C:\Users\issda\.codex\skills\hydra-node-terminal-browsing\scripts\hydra_terminal_browse.mjs --url "https://example.com" --out "artifacts\page_evidence.json"`

2. `packet_playwright_smoke`
- Validate `n8n + bridge + browser` stack health.
- Use: `python scripts/system/full_system_smoke.py --bridge-url http://127.0.0.1:8002 --browser-url http://127.0.0.1:8012 --n8n-url http://127.0.0.1:5680 --probe-webhook --output artifacts/system_smoke/synthesis_smoke.json`

3. `packet_hydra_armor_ingest`
- Run Notion/GitHub connector goals and governed swarm workflow.
- Use: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_hydra_armor_bridge.ps1`

4. `packet_dataset_and_table_sync`
- Route approved artifacts to Hugging Face dataset and Airtable.
- HF path: use `hf-publish-workflow` or `hf upload` for staged outputs in `training-data/`.
- Airtable path: use Airtable connector goal (`airtable-funnel-sync`) or Airtable MCP tools.

5. `packet_obsidian_lanes`
- Write deterministic shell lanes to Obsidian for operator reuse.
- Reference: `references/command-lanes.md`

## Fast Start

```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_synthesis_pipeline.ps1
```

## Output Contract

- `artifacts/system_smoke/synthesis_smoke.json`
- `artifacts/page_evidence/synthesis_terminal_browse.json`
- `artifacts/system_smoke/hydra_armor_bridge_run.json`
- Obsidian note update in `AI Workspace/SCBE Internet Navigation Command Lanes 2026-02-27.md`
