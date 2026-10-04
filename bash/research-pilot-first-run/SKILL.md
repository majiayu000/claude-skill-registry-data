---
name: research-pilot-first-run
description: Use when a new user wants an agent to start Research Pilot from scratch, create or inspect a local workspace, create the first project, or begin project tracking.
argument-hint: "[workspace path] [project id]"
---

# Research Pilot First Run

Guide a user from natural chat intent to a working local Research Pilot workspace and first project.

Primary user intent:

```text
Use Research Pilot to track this project.
```

## Goal

Create the minimum working research memory loop:

```text
workspace exists
-> research-pilot.db exists
-> first project exists
-> initial project brief or UnderstandingUpdate exists
-> dashboard can observe the project
-> agent continues through natural chat
```

Do not require Zotero setup, D* delta review, graph events, or manual read-model rebuilds for normal first-run value.

## State Detection

Before suggesting next actions, run:

```bash
python3 "$PLUGIN_ROOT/tools/research_pilot_status.py" --repo "$WORKSPACE_PATH" --json
```

Summarize the returned stage in product terms. Do not expose command mechanics unless diagnosis is needed.

Use returned stage values:

- `plugin_repo`: current directory contains plugin source. Explain repo vs workspace and ask for/infer a workspace path.
- `plain_directory`: no workspace markers. Ask whether to initialize this directory or another path.
- `empty_workspace`: workspace exists without projects. Create or import first project.
- `project_shell`: project shell exists. Record initial project brief/update if missing.
- `read_models_stale`: read models may need internal rebuild before dashboard observation.
- `project_has_graph`: project graph exists. Treat graph as existing strict-review/advanced structure, not mandatory first-run path.

## First-Run Flow

### 1. Initialize or confirm workspace

If workspace does not exist, run:

```bash
python3 "$PLUGIN_ROOT/tools/research_pilot_init.py" "$WORKSPACE_PATH"
```

Resolve `PLUGIN_ROOT` in this order:

```text
~/.research-pilot/repo
~/.research-pilot-plugin
current directory, only if it is the plugin repo
```

### 2. Explain the boundary once

Use concise language:

```text
Research Pilot repo = plugin source and agent tools.
Your workspace = private local project memory.
research-pilot.db = primary workspace dataset.
Dashboard = read-only observer.
Chat = control surface.
Strict graph review = optional advanced mode.
Zotero = optional source adapter.
```

### 3. Collect minimum project intake

Ask only for missing essentials:

- project name or short id;
- one-sentence research direction;
- first question, uncertainty, source, note, or experiment result.

Do not ask for Zotero status unless the user gives a Zotero source or asks for Zotero setup.

### 4. Create project memory

Create or select project in the workspace dataset. Create compatibility project shell files through:

```bash
python3 "$PLUGIN_ROOT/tools/project_shell_cli.py" --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --title "$TITLE" --direction "$DIRECTION" --seed-question "$QUESTION" --json
```

Do not hand-create a divergent compatibility file list. The compatibility shell may include legacy `experiment-proposals/.gitkeep`.

Record an initial project brief or UnderstandingUpdate. Use `human_review: pending` for unapproved claims and explicit status labels for uncertainty.

Actual experiment records belong in `research-pilot.db` through `ProjectDatasetWriter.write_project_update`. Dashboard experiments read DB or `wiki/projects/<ProjectId>/experiments/experiments.json` when imported/exported.

### 5. Dashboard readiness

If the user asks to see the dashboard, start or reuse the dashboard server through the dashboard runbook. Do not require the user to run build or server commands.

### 6. Strict review only when requested

If the user asks for strict review or a formal graph update:

```text
draft D*
-> dry-run
-> summarize effect
-> wait for accept/reject/park/revise
-> append accepted event only after explicit approval
```

Normal first-run does not require this.

### 7. Completion response

End with:

```text
Workspace:
Project:
Initial memory:
Dashboard:
Strict review:
Next natural prompts:
```

Offer at most three natural chat prompts, for example:

- read a source and record what matters;
- open the dashboard;
- use strict review for a specific claim.

## Stop Points

Stop for human approval before:

- accepting a strict-review graph delta;
- marking a paper project-core or global-core;
- changing research direction as a decision;
- interpreting experiment results as confirmed project evidence;
- writing Zotero status mirrors with `--apply`.
