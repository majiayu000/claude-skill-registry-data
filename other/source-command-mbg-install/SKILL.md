---
name: "source-command-mbg-install"
description: "Set up this repository for AI-agent use — Python environment, then the OpenCode / Codex / Codex integrations — and verify the result."
---

# source-command-mbg-install

Use this skill when the user asks to run the migrated source command `mbg-install`.

## Command Template

<!-- GENERATED FILE — do not edit by hand. Source: .ai/workflows/mbg-install.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

Set up the Microelectronic Block Generator for use on this machine.

Run the two setup scripts in order and report what each one says. Do not
paraphrase a failure as a success.

## 1. Python environment

```bash
./scripts/setup_env.sh
```

This creates `.venv`, installs `mbg` in editable mode with the dev and
notebook extras, then reports the Python packages, the EDA toolchain
(ngspice / Magic / netgen, supplied by IIC-OSIC-TOOLS) and the PDK.

Use `--locked` to reproduce the exact pinned versions from
`requirements-lock.txt`, or `--check` to report status without installing.

## 2. Agent integrations

```bash
./scripts/install_agents.sh
```

- OpenCode and Codex read `.opencode/` and `.Codex/` straight from the
  clone, so they need no registration.
- Codex has no repo-scoped skills, so its plugin is registered once per
  machine. That step writes to `~/.codex/config.toml` and asks first.

## 3. Verify

```bash
python3 scripts/validate_agent_integrations.py
python3 tests/test_all_designs.py
```

Report the real output: the validator's PASS/FAIL summary, and how many of the
four reference designs pass DRC and LVS.

## Troubleshooting

- **No Python 3.10–3.12.** gdsfactory 7 and numpy 1 have no wheels for 3.13+.
  Install a supported interpreter; `setup_env.sh` picks one automatically.
- **PDK not found.** Set `PDK_ROOT=/foss/pdks` inside the container, or install
  it on the host with volare.
- **Codex still shows old skills.** The plugin is cached at install time; re-run
  `./scripts/install_agents.sh --only codex` to refresh it.
