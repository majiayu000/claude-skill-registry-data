---
name: project-intelligence
description: Global project intelligence & memory system for one-time discovery, persistent context, token-efficient navigation, and automatic incremental change refresh across any software project.
risk: low
source: local
source_type: builtin
date_added: 2026-09-17
---

# Project Intelligence & Memory Skill

## When to Use

Use this skill whenever entering a new software project, resuming work on an existing project, or finishing a development modification task.

It maintains a persistent, token-efficient navigation and context layer in `<PROJECT_ROOT>/.agent/project-memory/` (or `.agents/project-memory/`).

### Core Invariants

1. **Memory is Navigation, Source Code is Truth**: Never trust memory if source code contradicts it.
2. **Zero Full-Repo Scans for Known Projects**: Read `PROJECT-CONTEXT.md` first, then inspect only the relevant subsystem files.
3. **Always Refresh on Completion**: Detect added, modified, and deleted files and update project memory automatically.
4. **Zero Secret Exposure**: Never write API keys, passwords, bearer tokens, or sensitive values into memory documents.

---

## Commands & Workflows

The skill operates via the native CLI:
```bash
/Users/subhajkar/Developer/AI-Dev-Team/scripts/project-memory <command> [target_path] [options]
# Or through the central runner:
ai-team memory <command> [target_path] [options]
```

### 1. Project Detection
```bash
ai-team memory detect [path]
```
Detects project root, identity, git remote, commit, and primary framework indicators.

### 2. Initial Discovery (New Project)
```bash
ai-team memory discover [path]
```
Executes structured non-destructive discovery and creates the persistent memory documents:
- `PROJECT-CONTEXT.md`: Compact executive summary and navigation index.
- `PROJECT-MAP.json`: Subsystem and directory graph.
- `METADATA.json`: Machine-readable file hashes, commands, and tech stack.
- `ARCHITECTURE.md`: Layer boundaries and component relationships.
- `DEPENDENCIES.md`: Runtime and dev dependencies.
- `DATA-FLOW.md`: Input -> Processing -> Storage -> Output lifecycle.
- `API-MAP.md`: Documented HTTP routes, handlers, and methods.
- `TEST-MAP.md`: Test suites, runners, and regression commands.
- `DECISIONS.md`: Architectural Decision Records (ADRs).
- `CHANGELOG.md`: Chronological agent task change history.

### 3. Loading Context Token-Efficiently
```bash
# Load high-level executive context (<150 lines)
ai-team memory load [path]

# Load specific subsystem context
ai-team memory load [path] --subsystem api
ai-team memory load [path] --subsystem test
ai-team memory load [path] --subsystem architecture
ai-team memory load [path] --subsystem dependencies
ai-team memory load [path] --subsystem data-flow
ai-team memory load [path] --subsystem decisions
```

### 4. Automatic Incremental Refresh (Post-Task)
After modifying code, running tests, or adding/deleting files:
```bash
ai-team memory refresh [path] --summary "Implemented user authentication middleware"
```
Change levels automatically classified:
- **Level 1 (Content)**: Documentation, comments, minor styling -> updates metadata & changelog.
- **Level 2 (Code)**: Component/service logic modifications -> updates file index & hashes.
- **Level 3 (Structural)**: Added/removed files, new routes, added dependencies -> updates maps, API/test architecture.
- **Level 4 (Major Architecture)**: Framework replacements, database rewrites -> targeted deep rescan.

### 5. Integrity & Health Check
```bash
ai-team memory check [path]
```
Verifies if memory is `CLEAN`, `STALE` (drift detected), `INCOMPLETE`, or `CORRUPTED`.

### 6. Self-Healing & Memory Recovery
```bash
ai-team memory recover [path]
```
Reconstructs memory documents from source code if files were deleted or JSON was corrupted.

---

## Multi-Agent Integration
- **AgentTeam (SQLite `~/.agent-team/team.db`)**: Automatically syncs project summaries and ADRs into `projects`, `project_summaries`, and `decisions` tables.
- **Claude Code / Gemini CLI / Codex**: Portable standard Markdown and JSON structure readable by any LLM agent.
