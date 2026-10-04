---
name: octoarms-hydra-model-swarm
description: Coordinate OctoArmor, HYDRA swarm extensions, Hugging Face model deployment, and governed multi-agent task completion across browser, deep-research, Colab bridge, universal synthesis, and Spiralverse intent-auth lanes.
---

# Octo Arms Hydra Model Swarm

Use this skill when a task needs one governed control layer over:
- OctoArmor model routing
- HYDRA browser or research swarms
- Hugging Face model selection, deployment, or push lanes
- Colab bridge handoff into automation or training
- Sacred Tongues routing and Spiralverse intent-auth
- reproducible action maps, evidence packets, and return contracts

This is an orchestration skill. It should compose the existing skills named below rather than replacing them.

## Trigger Conditions

Use this skill when the user asks to:
- launch or coordinate a multi-agent HYDRA or OctoArmor swarm
- route tasks across local models, Hugging Face models, and browser agents
- deploy or test Hugging Face-backed agent lanes for real task completion
- connect Colab compute into governed agent workflows
- run one task through multiple SCBE skills with a single command plan
- enforce Sacred Tongues or Spiralverse intent-auth before execution
- turn a large task into bounded arms, packets, and return contracts

## Skill Composition

Load these skills in this order unless the task is narrower:
1. `$scbe-universal-synthesis` for skill inventory and Sacred Tongues routing.
2. `$scbe-spiralverse-intent-auth` for ALLOW, QUARANTINE, or DENY packet logic.
3. `$hydra-node-terminal-browsing` when deterministic browse evidence is needed.
4. `$hydra-clawbot-synthesis` when the workflow crosses browser, dataset, Airtable, HF, or Obsidian lanes.
5. `$hydra-deep-research-self-healing` when the job should run continuously or recover automatically.
6. `$scbe-n8n-colab-bridge` when a Colab runtime or local notebook bridge is part of the execution path.

Read [skill-composition.md](./references/skill-composition.md) when you need the lane-by-lane handoff contract.
Read [repo-surfaces.md](./references/repo-surfaces.md) when you need the concrete repo commands, files, and services.

## Fast Start

Use the bundled helper when you want packetize + dispatch in one call.

```powershell
python C:\Users\issda\.codex\skills\octoarms-hydra-model-swarm\scripts\octoarms_dispatch.py --repo-root C:/Users/issda/SCBE-AETHERMOORE --task "route a governed multi-agent task" --lane octoarmor-triage
python C:\Users\issda\.codex\skills\octoarms-hydra-model-swarm\scripts\octoarms_dispatch.py --repo-root C:/Users/issda/SCBE-AETHERMOORE --task "research governed browser agents" --lane hydra-swarm --dry-run
```

The helper always:
- generates a flow plan
- packetizes the task into bounded arms
- applies a low-cost OctoArmor routing overlay
- optionally launches the selected lane
## Core Workflow

### 1. Establish the control plane

Start from the repo root and verify the operator shell is live.

```powershell
cd C:\Users\issda\SCBE-AETHERMOORE
.\scripts\install_hydra_quick_aliases.ps1
issac-help
hstatus
hqueue
```

If OctoArmor or HYDRA surfaces are missing, use the command-center aliases in [repo-surfaces.md](./references/repo-surfaces.md).

### 2. Choose the execution lane

Use the smallest lane that can finish the task.

- OctoArmor routing only:
  - inspect `src/aetherbrowser/router.py`
  - use `octo-serve` for the model gateway
- HYDRA browser swarm:
  - use `python -m hydra.cli_swarm --dry-run ...` first
- HYDRA terminal evidence:
  - use the Node browse script for deterministic JSON
- Deep research:
  - use the self-healing loop only for multi-cycle or continuous jobs
- Colab or training bridge:
  - use `scbe.py colab ...` or the Colab bridge skill before execution
- Hugging Face model lane:
  - pass a specific model id when using `--provider hf`

Default preference:
- low-complexity or cheap checks -> local
- bounded remote specialist run -> Hugging Face
- browser-heavy evidence gathering -> HYDRA browse lanes
- long-form resilient research -> self-healing lane

### 3. Apply governed intent routing

Before live execution, produce an intent packet and gate decision.

Minimum contract:
- choose a tongue or tongue sequence
- state task intent
- define recipients or runtime lane
- set a return artifact path

If the governance decision is not `ALLOW`, do not execute the live action. Fall back to dry-run, planning, or a reduced-scope packet.

### 4. Execute in bounded arms

Treat each arm as a bounded worker packet with:
- `task_id`
- `objective`
- `lane`
- `provider`
- `dependencies`
- `artifacts_out`
- `return_contract`

Good examples:
- Arm 1: route with OctoArmor, return selected provider snapshot
- Arm 2: run deterministic browse evidence on target URLs
- Arm 3: run HYDRA swarm with `--dry-run`, then live if clean
- Arm 4: sync approved outputs to HF or Colab bridge
- Arm 5: emit action-map and cross-talk packet

### 5. Capture proof

Persist evidence whenever the task matters.

Recommended outputs:
- browse JSON artifact
- swarm result JSON
- action-map run id
- Colab bridge status
- model id and provider used
- final governance decision packet

### 6. Close the loop

Return:
- what lane ran
- what model/provider ran
- whether intent-auth allowed it
- where artifacts were saved
- what the next bounded action is

## Quick Commands

### OctoArmor and HYDRA

```powershell
octo-serve
python -m hydra.cli_swarm --status
python -m hydra.cli_swarm --dry-run "research governed browser agents"
python -m hydra.cli_swarm --provider hf --model HuggingFaceTB/SmolLM2-1.7B-Instruct "summarize target system"
```

### Deterministic browse evidence

```powershell
node C:\Users\issda\.codex\skills\hydra-node-terminal-browsing\scripts\hydra_terminal_browse.mjs --url "https://example.com" --out "artifacts\page_evidence.json"
```

### Deep-research recovery loop

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\issda\SCBE-AETHERMOORE\scripts\system\run_deep_research_self_healing.ps1 -Topic "governed model swarm" -Continuous -SleepSeconds 120 -UsePlaywriter -RunCiTriage
```

### Colab bridge

```powershell
python scbe.py colab bridge-status --name pivot
python scbe.py colab bridge-set --name pivot --backend-url "http://127.0.0.1:8888/?token=..." --probe
python scbe.py colab bridge-probe --name pivot
```

### Universal synthesis refresh

```powershell
python C:/Users/issda/SCBE-AETHERMOORE/scripts/system/refresh_universal_skill_synthesis.py
```

## Operational Rules

1. Prefer `--dry-run` before any live browser swarm action.
2. Prefer the cheapest valid provider first; escalate only when the task needs it.
3. Never hardcode tokens, model secrets, or Colab tokens into skill files or output artifacts.
4. Do not execute live actions when intent-auth returns `QUARANTINE` or `DENY`.
5. Keep work packets bounded. If a job is too big for one arm, packetize it instead of improvising.
6. Record the selected model, provider, lane, and artifact paths for every meaningful run.
7. Use deep-research self-healing only for jobs that truly need recovery logic.

## References

- [repo-surfaces.md](./references/repo-surfaces.md): concrete repo files, aliases, and command lanes
- [skill-composition.md](./references/skill-composition.md): how the named skills compose into one governed flow

## Resources

### scripts/
- `scripts/octoarms_dispatch.py`
  Packetizes a task with `scbe-system flow plan` and `flow packetize`, scores it with OctoArmor, then launches one selected lane: triage, HYDRA swarm, browse evidence, or Colab bridge status/probe.
