---
name: install-and-maintain
description: Analyze any codebase and generate workspace-aware Claude Code configuration with justfile, hooks, and project-local skills. Use when setting up Claude Code in a new project, generating a justfile, or configuring hooks and workspace automation.
---

# Install and Maintain Skill

**Analyze any codebase and generate complete Claude Code configuration with three execution modes.**

## Overview

This skill analyzes your project and generates:

- **justfile** with setup/maintain commands (works from any subfolder)
- **.claude/hooks/** with project-specific init and maintenance scripts
- **.claude/commands/** with agentic and interactive setup prompts
- **.claude/skills/** with selected skills from claude-toolkit (at workspace root)

## Workflow

Execute the following phases in order:

### Phase 1: Analyze Codebase

**Run these detection steps:**

1. **Find workspace root:**

```bash
git rev-parse --show-toplevel
```

2. **Detect tech stack** - Check for these files at root and in subdirectories:

| File                          | Stack      | Setup Command                     |
| ----------------------------- | ---------- | --------------------------------- |
| `pyproject.toml` + `uv.lock`  | Python/uv  | `uv sync`                         |
| `pyproject.toml` (no uv.lock) | Python/pip | `pip install -e .`                |
| `requirements.txt`            | Python/pip | `pip install -r requirements.txt` |
| `pnpm-lock.yaml`              | Node/pnpm  | `pnpm install`                    |
| `package-lock.json`           | Node/npm   | `npm install`                     |
| `bun.lockb`                   | Node/bun   | `bun install`                     |
| `Cargo.toml`                  | Rust       | `cargo build`                     |
| `go.mod`                      | Go         | `go mod download`                 |
| `src-tauri/`                  | Tauri      | Rust + Node hybrid                |

3. **Detect workspace type:**

| Type           | Indicators                                                                                |
| -------------- | ----------------------------------------------------------------------------------------- |
| **Monorepo**   | Has `apps/`, `packages/`, `services/`, or workspace config in pyproject.toml/package.json |
| **Single App** | Single package config at root, no workspace folders                                       |

4. **Scan subdirectories** for additional stacks (max depth 3):

```bash
find . -maxdepth 3 -name "pyproject.toml" -o -name "package.json" -o -name "Cargo.toml" -o -name "go.mod"
```

5. **Check existing configuration:**

- `.claude/` folder exists?
- `justfile` exists?
- `CLAUDE.md` exists?

6. **Write analysis to** `setup_docs/codebase_analysis.md`

### Phase 2: Interactive Questions

Use `AskUserQuestion` to ask the user:

**Question 1: Confirm Analysis**

```
header: "Analysis"
question: "I detected the following stack. Is this correct?"
options:
  - label: "Yes, proceed"
    description: "Continue with detected configuration"
  - label: "Let me adjust"
    description: "I'll provide corrections"
```

**Question 2: Existing Configuration**
(Only if .claude/ or justfile exists)

```
header: "Existing Config"
question: "Found existing configuration. How should I handle it?"
options:
  - label: "Merge (Recommended)"
    description: "Add new config, preserve existing hooks/commands"
  - label: "Replace"
    description: "Overwrite with fresh configuration"
  - label: "Skip"
    description: "Don't modify existing configuration"
```

**Question 3: Skills Selection**

```
header: "Skills"
question: "Which skills would you like to install for this project?"
multiSelect: true
options:
  - label: "claude-docs-skill"
    description: "Claude API and CLI documentation"
  - label: "openrouter-docs-skill"
    description: "OpenRouter models and pricing (345+ models)"
  - label: "warp-docs-skill"
    description: "Warp terminal documentation"
  - label: "architecture"
    description: "Codebase architecture analysis"
```

**Question 4: Additional Commands**

```
header: "Commands"
question: "Generate project-specific commands in justfile?"
options:
  - label: "Yes (Recommended)"
    description: "Add dev, build, test commands based on detected stack"
  - label: "No"
    description: "Only generate setup/maintain commands"
```

### Phase 3: Generate Configuration

Based on analysis and user choices, generate these files:

#### 1. justfile

Use template at `skills/install-and-maintain/templates/justfile.template`

**Key patterns:**

- `WORKSPACE_ROOT := \`git rev-parse --show-toplevel\``
- All commands use `cd {{WORKSPACE_ROOT}}` to work from any subfolder
- Three setup modes: `setup`, `setup-report`, `setup-guide`
- Two maintain modes: `maintain`, `maintain-report`

#### 2. .claude/settings.json

```json
{
  "hooks": {
    "Setup": [
      {
        "matcher": "init",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/setup_init.py",
            "timeout": 180
          }
        ]
      },
      {
        "matcher": "maintenance",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/setup_maintenance.py",
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

#### 3. .claude/hooks/setup_init.py

Use template at `skills/install-and-maintain/templates/setup_init.py.template`

Fill in:

- `PROJECT_NAME` - from directory name
- `WORKSPACE_TYPE` - monorepo/single
- `SETUP_ACTIONS` - list of (command, working_dir) tuples from stack detection
- `ENV_VARS` - environment variables to set

#### 4. .claude/hooks/setup_maintenance.py

Use template at `skills/install-and-maintain/templates/setup_maintenance.py.template`

Fill in:

- `MAINTENANCE_ACTIONS` - upgrade commands for each detected stack

#### 5. .claude/commands/setup.md

Use template at `skills/install-and-maintain/templates/commands/setup.md.template`

#### 6. .claude/commands/setup-guide.md

Use template at `skills/install-and-maintain/templates/commands/setup-guide.md.template`

#### 7. .claude/commands/maintain.md

Use template at `skills/install-and-maintain/templates/commands/maintain.md.template`

### Phase 4: Install Skills

Copy selected skills from claude-toolkit to workspace root:

```bash
TOOLKIT_DIR="$HOME/Projects/Dev_projects/Claude_SDK/claude-toolkit/skills"
WORKSPACE_ROOT=$(git rev-parse --show-toplevel)

# Create skills directory at workspace root
mkdir -p "$WORKSPACE_ROOT/.claude/skills"

# Symlink each selected skill (never copy — doc skills are 24MB+)
ln -sfn "$TOOLKIT_DIR/claude-docs-skill" "$WORKSPACE_ROOT/.claude/skills/"
ln -sfn "$TOOLKIT_DIR/architecture" "$WORKSPACE_ROOT/.claude/skills/"
# ... etc
```

### Phase 5: Report Results

Output summary:

```
## Setup Complete!

**Workspace:** {workspace_root}
**Type:** {workspace_type}
**Stack:** {detected_stacks}

### Generated Files:
- justfile
- .claude/settings.json
- .claude/hooks/setup_init.py
- .claude/hooks/setup_maintenance.py
- .claude/commands/setup.md
- .claude/commands/setup-guide.md
- .claude/commands/maintain.md

### Installed Skills:
- claude-docs-skill
- architecture

### Next Steps:

1. **Quick setup:** `just setup`
2. **Guided setup:** `just setup-guide`
3. **With report:** `just setup-report`

All commands work from any directory in the workspace!
```

---

## Templates Location

All templates are in `skills/install-and-maintain/templates/`:

```
templates/
├── justfile.template
├── settings.json.template
├── setup_init.py.template
├── setup_maintenance.py.template
└── commands/
    ├── setup.md.template
    ├── setup-guide.md.template
    └── maintain.md.template
```

---

## Non-Destructive Behavior

- **Never overwrite** without asking
- **Merge mode** preserves existing hooks and commands
- **Backup** existing files to `.claude/backup/` before replacing
- **Skip** files that already exist if user chooses

---

## Workspace-Aware Paths

All generated files use patterns that work from any subfolder:

```just
# In justfile - always finds workspace root
WORKSPACE_ROOT := `git rev-parse --show-toplevel`

setup:
    cd {{WORKSPACE_ROOT}} && claude --dangerously-skip-permissions --init
```

```python
# In hooks - use CLAUDE_PROJECT_DIR or find git root
import subprocess
workspace_root = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True, text=True
).stdout.strip()
```

---

## File Locations

**This skill:** `~/.claude/skills/install-and-maintain/` (global, for invoking anywhere)

**Generated output:** `<workspace-root>/.claude/` (project-local)

**Copied skills:** `<workspace-root>/.claude/skills/` (project-local)
