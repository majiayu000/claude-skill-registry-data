---
name: project-metadata-builder
description: Build and update project metadata registry in ${CLAUDE_PROJECTS_YML_PATH}. Use when starting a session, after project analysis, when user says "update project metadata", "refresh projects", "register project", or when project-analysis agent completes analysis.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Project Metadata Builder

Build comprehensive project metadata and maintain a global registry at `${CLAUDE_PROJECTS_YML_PATH}`.

## Activation Triggers

- After `project-analysis` agent completes analysis
- User says: "update project metadata", "refresh projects", "register project"
- Session start with `auto_update_on_session: true` in config

## Execution

Run the builder script for a project:

```bash
cd ${CLAUDE_SKILLS_PATH}/project-metadata-builder && \
uv run python -m scripts.builder <project_path> [--session-id <id>]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `project_path` | Yes | Path to the project directory |
| `--session-id` | No | Current session ID for history tracking |
| `--debug` | No | Enable debug logging |

## Output

Updates `${CLAUDE_PROJECTS_YML_PATH}` with:

- **Identity**: Name, slug, description
- **Git**: Remote URL, branch, last commit (hash, message, author, date), total commits
- **Languages**: Primary language, all languages with percentages
- **Frameworks**: Detected frameworks (react, docker, playwright, etc.)
- **Dependencies**: Python (from pyproject.toml) and Node (from package.json)
- **Structure**: Project type, key directories, entry points
- **Runtime**: Docker services, MCP servers
- **Activity**: Status (active/stale/archived), timestamps
- **Sessions**: Last N sessions with commits and files changed

## Configuration

Settings in `${CLAUDE_PATH}/config.yml` (project root):

```yaml
project_metadata:
  session_history_limit: 10      # Keep last N sessions
  auto_update_on_session: true   # Auto-update on session start
  periodic_refresh_hours: 24     # Periodic refresh (0 = disabled)
  stale_project_days: 30         # Mark stale after N days inactive
  activity_threshold_commits: 5  # Min commits for "active" status
  projects_file: ${CLAUDE_PROJECTS_YML_PATH}
  log_level: INFO
```

## Example Output (projects.yml)

```yaml
projects:
  /workspace/projects/personal/claude-sandbox:
    name: claude-sandbox
    slug: claude-sandbox
    description: "Docker-ized development environment for Claude Code CLI"
    git:
      remote_url: git@github.com:brianclaridge/claude-sandbox.git
      branch: main
      last_commit:
        hash: abc123def456
        message: "feat: add project-metadata-builder skill"
        author: Brian Claridge
        date: "2025-12-11T15:00:00"
      total_commits: 42
    languages:
      primary: Python
      all:
        - "Python: 45%"
        - "Shell: 30%"
        - "Markdown: 15%"
    frameworks:
      - docker
      - playwright
      - structlog
    dependencies:
      python:
        - "playwright>=1.40.0"
        - "loguru>=0.7.0"
    structure:
      type: monorepo
      key_directories:
        - ".claude/agents/"
        - ".claude/skills/"
        - ".claude/hooks/"
      entry_points:
        - "docker-compose.yml"
        - "Taskfile.yml"
    runtime:
      docker:
        compose_file: ".claude/docker-compose.yml"
        services:
          - claude
      mcp_servers:
        - context7
        - playwright
    activity:
      status: active
      first_seen: "2025-12-01T10:00:00"
      last_updated: "2025-12-11T15:30:00"
    sessions:
      - id: session_abc123
        started: "2025-12-11T14:00:00"
        ended: "2025-12-11T15:30:00"
        commits: 3
        files_changed: 12
```

## Integration with project-analysis Agent

After completing project analysis, invoke this skill:

```markdown
## Post-Analysis

1. Run project-metadata-builder skill
2. Pass current project path
3. Include session_id if available from environment
```

## Logs

Logs written to: `~/.claude/.data/logs/project-metadata-builder/builder.log`

## Collectors

| Collector | Source Files | Data Extracted |
|-----------|--------------|----------------|
| `git_collector` | `.git/` | Remote, branch, commits |
| `lang_collector` | `*.*` | Language percentages |
| `deps_collector` | `pyproject.toml`, `package.json` | Dependencies |
| `docker_collector` | `docker-compose.yml` | Services, compose config |
| `mcp_collector` | `.mcp.json`, `settings.json` | MCP servers |
