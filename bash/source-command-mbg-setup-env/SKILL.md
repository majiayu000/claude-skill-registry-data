---
name: "source-command-mbg-setup-env"
description: "Create or repair the Python environment for this repository and report exactly what is installed, what is missing, and what the PDK looks like."
---

# source-command-mbg-setup-env

Use this skill when the user asks to run the migrated source command `mbg-setup-env`.

## Command Template

<!-- GENERATED FILE — do not edit by hand. Source: .ai/workflows/mbg-setup-env.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

Set up or diagnose the Python environment.

```bash
./scripts/setup_env.sh --check     # report only, change nothing
./scripts/setup_env.sh             # create .venv and install mbg editable
./scripts/setup_env.sh --locked    # reproduce the pinned known-good versions
./scripts/setup_env.sh --freeze    # rewrite requirements-lock.txt from this env
```

Report the three sections the script prints — Python environment, EDA
toolchain, PDK — without softening anything it marks as missing.

## Version constraints that matter

These upper bounds are load-bearing, not caution:

- **gdsfactory `>=7.7,<8`** — version 8 moved to a kfactory backend and drops
  `Component.references`, `ref.get_polygons(by_spec=True)` and
  `gf.Port(center=...)`, all of which this code uses.
- **numpy `>=1.24,<2`** — numpy 2 removed `np.float_`, which gdsfactory 7 still
  expects.

If someone reports an import error mentioning `references`, `get_polygons` or
`float_`, check the installed versions first — it is almost always one of these.

## What this does not install

The EDA tools (ngspice, Magic, netgen) and the GF180MCU PDK come from the
IIC-OSIC-TOOLS container, not from pip. The script reports whether it can see
them; it does not try to install them.
