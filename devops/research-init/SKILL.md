---
name: research-init
description: "Use when installing, attaching, initializing, repairing, or validating ARC in a research workspace."
---

# Research init

Bring one target workspace to a verified ARC setup state. Treat setup as
infrastructure work, not research intent. Stop with a precise handoff to
`research-onboard`, `research-brainstorm`, or `research-package`.

Read [references/setup-contract.md](references/setup-contract.md) before a
protocol merge, external `RESEARCH_ROOT`, or skill-path repair.

## Boundary

Own setup orchestration only:

- inspect the toolbox, target workspace, research root, protocol files, skill
  links, interface, and Server;
- install or repair repository-backed skill symlinks;
- attach `AGENTS.md` and `CLAUDE.md` through managed blocks without replacing
  project-owned text;
- initialize an empty managed root through `lib.research_state`;
- validate the current managed state;
- build the interface and start or reuse a healthy Dashboard Server by default;
- report the resolved roots, mutations, Server URL, health, and next skill.

Do not infer or commit Project, Direction, or Experiment intent. Do not create
a Package, launch a Run, modify source/data/environments, write management
events directly, adopt unsupported legacy roots, or commit Git changes.

## Procedure

### 1. Inspect before mutation

Run the read-only classifier:

```bash
python3 skills/research-init/scripts/research_init.py \
  --workspace <workspace> \
  inspect \
  --agent codex
```

Use `--agent claude` or `--agent both` when requested. Resolve script paths
through the installed `research-init` symlink in a target project.

Interpret the state exactly:

- `ABSENT`: safe greenfield setup candidate.
- `CURRENT`: reconcile protocols, skills, interface, and Server.
- `INVALID`: stop. Legacy data, an unknown version, or an unversioned managed
  root is unsupported; do not adopt or rewrite it by guessing.

### 2. Review protocol conflicts

If either protocol is `UNMANAGED`, show the target file and the proposed
managed block. Obtain user confirmation before passing `--merge-protocols`.
Never overwrite project-owned text. A symlink, directory, or malformed managed
block is a hard conflict.

### 3. Set up a greenfield or current workspace

```bash
python3 skills/research-init/scripts/research_init.py \
  --workspace <workspace> \
  setup \
  --agent codex
```

The command installs all repository skills for the selected agent, attaches
the protocols, initializes `.research` only when absent, builds the interface,
and starts or reuses the Dashboard Server. Use `--merge-protocols` only after
step 2. Use `--no-serve` only when the user explicitly requests a headless or
CI setup.

### 4. Validate and report

```bash
python3 skills/research-init/scripts/research_init.py \
  --workspace <workspace> \
  check \
  --agent codex
```

Report all of the following:

- `workspace`, `research_root`, and managed `VERSION`;
- skill installation roots and any repaired links;
- protocol actions and confirmation that project-owned prefixes remain;
- interface root and Dashboard Server action, `started` or `reused`;
- Dashboard URL, host, port, health, and SSH forwarding command;
- the exact Dashboard stop command;
- `READY_NO_PROJECT`, `READY_WITH_PROJECT`, or `REPAIR_REQUIRED`;
- the single next action.

Use `research-onboard` when no active Project exists. With an active Project,
use `research-brainstorm` for a vague Direction or `research-package` for a
ready plan.

## Bootstrap note

An agent must discover `research-init` before this skill can install its
siblings. Keep one minimal bootstrap command in the toolbox README. After the
skill is available, route all setup, attach, and setup-repair work
through this skill.
