---
name: mbg-setup
description: Sets up this repository on a new machine — the Python environment, the GF180MCU PDK, the EDA tools (Magic, netgen, KLayout), the shell integration in $HOME/.mbg, and the OpenCode / Claude Code / Codex agent integrations, repo-scoped or for the whole user account — then verifies the result. Use when someone has just cloned the repository, when imports fail, when the PDK or EDA tools cannot be found, when `mbg check` or a `/mbg-*` command does not work, or when a teammate asks how to install. Do not use it to design or verify a circuit.
class: MUTATING
owner: jabir
capabilities: [setup_environment, install_agents]
platforms: [opencode, claude, codex]
---

# MBG Setup

## Purpose

Get a clone working, then get it working *from anywhere*. One script,
`./install.sh`, does all of it in six stages. This is the skill to reach for on
a fresh machine, and the one Codex users invoke by name since Codex has no
slash commands.

## When to Use

- A fresh clone, or a new machine.
- `import mbg` fails, or a version error mentions `references`, `get_polygons`
  or `float_`.
- The PDK, ngspice, Magic, netgen or KLayout cannot be found.
- `mbg check` is not a command, or `$MBG_HOME` is unset in a new shell.
- A `/mbg-*` slash command is missing, stale, or only works inside the clone.
- Someone asks how to install the skills for their agent.

## When Not to Use

- Generating layout, running verification, or debugging a design.
- Adding a new skill or workflow — that is `mbg-extension-authoring`.

## Required Inputs

None. Every stage discovers the repository root itself. Nothing is hard-coded
to a particular user or home directory.

## Preconditions

- Linux. Debian/Ubuntu, Fedora/RHEL-like, Arch-like and openSUSE are detected.
- A Python 3.10–3.12 interpreter. gdsfactory 7 and numpy 1 have no wheels for
  3.13+, and `install.sh` selects a supported one automatically. Pin one with
  `MBG_PYTHON=/path/to/python3.11`.
- Roughly 2 GB of disk, most of it the GF180MCU PDK.
- No Docker and no root. Building Magic, netgen or KLayout from source needs a
  C toolchain, Tcl/Tk, Cairo and X11 headers — `./install.sh --deps` prints the
  exact package list for the detected distribution, and `--deps --yes` installs
  it. That is the only step that asks for sudo, and it is never silent.

## The six stages

`./install.sh` with no arguments runs all of them in dependency order. Run one
at a time with `--stage <name>` when a fresh machine fails and you need to know
which layer broke.

| Stage | What it does |
| :--- | :--- |
| `python` | `.venv`, pinned dependencies, `pip install -e .` |
| `pdk` | GF180MCU via volare into `$PDK_ROOT` |
| `eda` | Magic, netgen and **KLayout** into `$MBG_TOOLS_ROOT` — only what is missing or incompatible |
| `shell` | `$MBG_HOME/activate.sh`, the `mbg` launchers, one `~/.bashrc` line |
| `agents` | repo-scoped `/mbg-*` adapters + the Codex plugin *(optional)* |
| `global` | `/mbg-*` for the whole user account *(optional)* |

## Where things land

Three directories, all overridable, none hard-coded:

| Variable | Default | Holds |
| :--- | :--- | :--- |
| `MBG_VENV` | `<repo>/.venv` | the Python environment |
| `MBG_TOOLS_ROOT` | `$HOME/.local/mbg-tools` | EDA builds |
| `MBG_HOME` | `$HOME/.mbg` | activation script and launchers |

Nothing is written to `/usr`, `/usr/local` or the system package database
unless `--deps --yes` is used.

## Workflow

1. **Install**

   ```bash
   ./install.sh              # all six stages
   ./install.sh --list       # show the stages and stop
   ./install.sh --check      # full preflight, installs nothing
   ```

2. **Pick up the environment**

   After the `shell` stage, a *new* shell already has it — that stage writes
   `$MBG_HOME/activate.sh` and adds one idempotent block to `~/.bashrc` (and
   `~/.zshrc` if present), between `# >>> Microelectronic Block Generator >>>`
   and `# <<< Microelectronic Block Generator <<<`. Re-running replaces the
   block, never appends.

   In the current shell, or when working inside the clone:

   ```bash
   source scripts/activate_mbg.sh   # delegates to $MBG_HOME/activate.sh
   ```

   That sets `MBG_HOME`, `MBG_ROOT`, `MBG_VENV`, the four GF180 variables
   (`PDK_ROOT`, `PDK`, `PDKPATH`, `STD_CELL_LIBRARY`), `MBG_TOOLS_ROOT`, and
   pins each EDA tool by **absolute path** in `MBG_MAGIC`, `MBG_NETGEN`,
   `MBG_KLAYOUT` and `MBG_NGSPICE`. Every assignment defers to a value that is
   already exported, so a user's own setting wins.

   Pinning by absolute path is deliberate. Several distributions ship no
   `klayout` package at all, so the working binary often lives somewhere `PATH`
   never looks — and without it there is no foundry-deck DRC and no sign-off.

   **The virtualenv is deliberately not activated.** Activating it in a login
   file would change what `python` and `pip` mean in every unrelated shell.
   Instead `$MBG_HOME/bin` goes on `PATH` with launchers that name MBG's
   interpreter explicitly:

   ```bash
   mbg check          # environment preflight — same report as ./install.sh --check
   mbg version
   mbg python x.py    # run a script with MBG's interpreter
   mbg shell          # interactive Python with mbg importable
   mbg-python -c ...
   ```

   Pass `--with-venv` to the `shell` stage if the user would rather have the
   venv active everywhere.

3. **Agent integrations**

   ```bash
   ./install.sh --stage agents    # repo-scoped
   ./install.sh --stage global    # the whole user account
   ```

   `agents` makes `/mbg-*` work when the agent is started **inside this
   checkout**. OpenCode and Claude Code read `.opencode/` and `.claude/`
   straight from the clone and need no registration. Codex has no repo-scoped
   skills, so its plugin is registered once per machine; that writes to
   `~/.codex/config.toml` and asks first. Because Codex caches the plugin at
   install time, re-run this stage after any change under `.ai/`.

   `global` installs for the **current user**, so `/mbg-full-auto` works from
   any directory:

   | Platform | Installed to |
   | :--- | :--- |
   | Claude Code | `~/.claude/skills/mbg-*`, `~/.claude/commands/mbg-*.md` |
   | OpenCode | `~/.config/opencode/skills/mbg-*`, `~/.config/opencode/commands/mbg-*.md` |
   | Codex | the plugin registered by the `agents` stage |

   It uses **symlinks**, so a `sync_agent_tools.py` run reaches the global
   install immediately. A copied skill silently goes stale and the slash
   command ends up invoking last week's instructions. Use `--copy` only when
   the setup cannot follow symlinks, and re-run after every sync. Only `mbg-*`
   entries are created or removed; other projects' skills in those directories
   are never touched.

4. **Verify**

   ```bash
   ./install.sh --check                            # or: mbg check
   python3 scripts/validate_agent_integrations.py
   python3 tests/test_all_designs.py
   ```

   `--check` and `--uninstall` both accept `--stage`, so a single layer can be
   inspected or undone:

   ```bash
   ./install.sh --check --stage shell      # exactly one rc block? tools pinned?
   ./install.sh --check --stage global     # is the global install current?
   ./install.sh --uninstall --stage global # remove only the mbg-* entries
   ```

## Outputs

- `.venv/` with `mbg` importable and `mbg-sync` / `mbg-validate` on PATH.
- `$MBG_HOME/activate.sh`, `$MBG_HOME/bin/mbg`, `$MBG_HOME/bin/mbg-python`,
  and one block in the user's rc file.
- EDA tools under `$MBG_TOOLS_ROOT`, each pinned by absolute path.
- Registered agent integrations for whichever CLIs are installed, repo-scoped
  and optionally user-wide.
- A validator summary and a DRC/LVS result for the seven reference designs.

## Failure Modes

- **No supported interpreter.** Install Python 3.10–3.12; do not force 3.13+,
  the wheels do not exist.
- **PDK missing.** `--stage pdk` installs it with volare. Inside the
  IIC-OSIC-TOOLS container it is already at `PDK_ROOT=/foss/pdks`.
- **KLayout missing.** DRC sign-off reports `CONFIGURATION_FAILURE`, never
  PASS — a missing checker must not look like a clean run. The `klayout` pip
  package is **not** sufficient: it ships no executable and cannot run the
  GF180 deck's Ruby DSL. Point at a real binary with `MBG_KLAYOUT=/path/to/klayout`.
- **`mbg` is not a command.** The `shell` stage has not run, or the shell
  predates it. Run `./install.sh --stage shell` and open a new shell.
- **`/mbg-*` works in the clone but not elsewhere.** The `global` stage has not
  run.
- **A `/mbg-*` command runs stale instructions.** The global install was made
  with `--copy`; re-run it, or reinstall without `--copy` so it symlinks.
- **Codex marketplace add fails** with *"local marketplace source must be a
  directory, not a file"* — pass the repository root, not the manifest path.
- **Optional stage did not complete.** `agents` and `global` are optional: the
  install still succeeds, because MBG itself works without the agent layer.
  Report it as `PARTIAL`, not as failure.

## Reporting Rules

Report what the script actually printed, including which stage failed. Never
describe a missing tool or a failed install as success, and use `PASS` /
`FAIL` / `PARTIAL` / `NOT RUN` / `NOT AVAILABLE` for status.
