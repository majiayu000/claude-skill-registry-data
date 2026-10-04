---
name: mbg-setup
description: Sets up this repository on a new machine — the Python environment, then the OpenCode / Codex / Codex agent integrations — and verifies the result. Use when someone has just cloned the repository, when imports fail, when the PDK or EDA tools cannot be found, or when a teammate asks how to install. Do not use it to design or verify a circuit.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-setup/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Setup

## Purpose

Get a clone working: Python environment first, then the agent integrations,
then a verification pass. This is the skill to reach for on a fresh machine,
and the one Codex users invoke by name since Codex has no slash commands.

## When to Use

- A fresh clone, or a new machine.
- `import mbg` fails, or a version error mentions `references`, `get_polygons`
  or `float_`.
- The PDK or ngspice / Magic / netgen cannot be found.
- Someone asks how to install the skills for their agent.

## When Not to Use

- Generating layout, running verification, or debugging a design.
- Adding a new skill or workflow — that is `mbg-extension-authoring`.

## Required Inputs

None. Every script discovers the repository root itself.

## Preconditions

- A Python 3.10–3.12 interpreter. gdsfactory 7 and numpy 1 have no wheels for
  3.13+, and `setup_env.sh` selects a supported one automatically.
- For real DRC/LVS, the IIC-OSIC-TOOLS container (or a host install of
  ngspice, Magic, netgen) and the GF180MCU PDK.

## Workflow

1. **Python environment**

   ```bash
   ./scripts/setup_env.sh            # create .venv, install mbg editable
   ./scripts/setup_env.sh --check    # report only
   ./scripts/setup_env.sh --locked   # exact pinned versions
   ```

2. **Agent integrations**

   ```bash
   ./scripts/install_agents.sh
   ```

   OpenCode and Codex read the clone directly and need no registration.
   Codex has no repo-scoped skills, so its plugin is registered once per
   machine; that writes to `~/.codex/config.toml` and asks first. Because Codex
   caches the plugin at install time, re-run
   `./scripts/install_agents.sh --only codex` after any change under `.ai/`.

3. **Verify**

   ```bash
   python3 scripts/validate_agent_integrations.py
   python3 tests/test_all_designs.py
   ```

## Outputs

- `.venv/` with `mbg` importable and `mbg-sync` / `mbg-validate` on PATH.
- Registered agent integrations for whichever CLIs are installed.
- A validator summary and a DRC/LVS result for the four reference designs.

## Failure Modes

- **No supported interpreter.** Install Python 3.10–3.12; do not force 3.13+,
  the wheels do not exist.
- **PDK missing.** Inside the container `PDK_ROOT=/foss/pdks`; on a host, use
  volare. The script reports which it found.
- **Codex marketplace add fails** with *"local marketplace source must be a
  directory, not a file"* — pass the repository root, not the manifest path.
- **Editable install fails.** The script falls back to `requirements.txt` and
  says so; the package will not be importable outside the repo in that case.

## Reporting Rules

Report what the scripts actually printed. Never describe a missing tool or a
failed install as success, and use `PASS` / `FAIL` / `PARTIAL` / `NOT RUN` /
`NOT AVAILABLE` for status.
