---
name: llms-dashboard
description: Generate and update HTML dashboards for LLM usage (Claude, Gemini, Kiro, VS code, Cline, etc). Use when the user wants to visualize their AI coding assistant usage statistics, view metrics in a web interface, or analyze historical trends.
---

# LLMs Dashboard Generator

**Why?** AI coding assistants like Claude and Gemini store usage data in local JSON/Protobuf files. This skill transforms that raw data into beautiful, interactive HTML dashboards with charts and insights.

Generate visual HTML dashboards from Claude Code and Gemini usage data.

## Quick Start

### Claude Dashboard

```bash
# Step 1: Aggregate all session history (~/.claude/projects/)
python3 ~/.claude/skills/llms-dashboard/scripts/aggregate_claude_history.py

# Step 2: Generate dashboard
python3 ~/.claude/skills/llms-dashboard/scripts/update_claude_dashboard.py

# Step 3: Open in browser
open ~/.claude/skills/llms-dashboard/claude_dashboard.html
```

### Gemini Dashboard

```bash
# Step 1: Aggregate all session history (~/.gemini/tmp/)
python3 ~/.claude/skills/llms-dashboard/scripts/aggregate_gemini_history.py

# Step 2: Generate dashboard
python3 ~/.claude/skills/llms-dashboard/scripts/update_gemini_dashboard.py

# Step 3: Open in browser
open ~/.claude/skills/llms-dashboard/gemini_dashboard.html
```

### VS Code Dashboard

```bash
# Step 1: Aggregate all session history (Logs, History, Storage)
python3 ~/.claude/skills/llms-dashboard/scripts/aggregate_vscode_data.py

# Step 2: Generate dashboard
python3 ~/.claude/skills/llms-dashboard/scripts/update_vscode_dashboard.py

# Step 3: Open in browser
open ~/.claude/skills/llms-dashboard/vscode_dashboard.html
```

### Kiro Dashboard

```bash
# Step 1: Aggregate all session history (.chat files, logs, settings)
python3 ~/.claude/skills/llms-dashboard/scripts/aggregate_kiro_history.py

# Step 2: Generate dashboard
python3 ~/.claude/skills/llms-dashboard/scripts/update_kiro_dashboard.py

# Step 3: Open in browser
open ~/.claude/skills/llms-dashboard/kiro_dashboard.html
```

### Cline Dashboard

```bash
# Step 1: Aggregate task history from VS Code extension
python3 ~/.claude/skills/llms-dashboard/scripts/aggregate_cline_history.py

# Step 2: Generate dashboard
python3 ~/.claude/skills/llms-dashboard/scripts/update_cline_dashboard.py

# Step 3: Open in browser
open ~/.claude/skills/llms-dashboard/cline_dashboard.html
```

> [!NOTE]
> The `open` command works on macOS. For Linux, use `xdg-open` instead.

## Requirements

| Dashboard | Required Data Source |
|-----------|---------------------|
| Claude | `~/.claude.json` (created after first Claude Code session) |
| Gemini | `~/.gemini/tmp/` with chat history files |
| VS Code | `~/Library/Application Support/Code/` (macOS) or `~/.config/Code/` (Linux) |
| Kiro | `~/Library/Application Support/Kiro/User/globalStorage/kiro.kiroagent/**/*.chat` (macOS) |
| Cline | `~/Library/Application Support/Code/User/globalStorage/asbx.amzn-cline/state/taskHistory.json` (macOS) |

> [!WARNING]
> Always run the **aggregate** script before the **update** script, otherwise charts will be empty.

## What It Does

This skill reads usage statistics from local configuration files (read-only) and generates interactive HTML dashboards with:

- **Claude Dashboard:**
    - Usage statistics from `~/.claude.json`
    - Historical trends from `~/.claude/projects/*.jsonl`
    - Token usage, costs, and cache efficiency

- **Gemini Dashboard:**
    - Usage statistics from `~/.gemini/tmp/**/chats/*.json`
    - Token usage (including thought tokens)
    - Model breakdown and session activity

- **VS Code Dashboard:**
    - Usage statistics from `~/Library/Application Support/Code/logs`
    - Historical reconstruction from `~/Library/Application Support/Code/User/History`
    - Project identification from `~/Library/Application Support/Code/User/globalStorage/storage.json`

- **Kiro Dashboard:**
    - Session data from `~/Library/Application Support/Kiro/User/globalStorage/kiro.kiroagent/**/*.chat`
    - Log sessions from `~/Library/Application Support/Kiro/logs/`
    - Settings from `~/.kiro/settings/cli.json`
    - Powers registry from `~/.kiro/powers/registry.json`
    - CLI history from `~/.kiro/.cli_bash_history`

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This documentation |
| `scripts/update_claude_dashboard.py` | Generates `claude_dashboard.html` |
| `scripts/aggregate_claude_history.py` | Scans Claude logs, creates `data/claude_history.json` |
| `templates/claude_template.html` | Template for Claude dashboard |
| `claude_dashboard.html` | Generated Claude output |
| `scripts/update_gemini_dashboard.py` | Generates `gemini_dashboard.html` |
| `scripts/aggregate_gemini_history.py` | Scans Gemini logs, creates `data/gemini_history.json` |
| `templates/gemini_template.html` | Template for Gemini dashboard |
| `gemini_dashboard.html` | Generated Gemini output |
| `scripts/update_vscode_dashboard.py` | Generates `vscode_dashboard.html` |
| `scripts/aggregate_vscode_data.py` | Scans VS Code data, creates `data/vscode_data.json` |
| `templates/vscode_template.html` | Template for VS Code dashboard |
| `vscode_dashboard.html` | Generated VS Code output |
| `scripts/update_kiro_dashboard.py` | Generates `kiro_dashboard.html` |
| `scripts/aggregate_kiro_history.py` | Scans Kiro data, creates `data/kiro_history.json` |
| `templates/kiro_template.html` | Template for Kiro dashboard |
| `kiro_dashboard.html` | Generated Kiro output |
| `scripts/update_cline_dashboard.py` | Generates `cline_dashboard.html` |
| `scripts/aggregate_cline_history.py` | Scans Cline data, creates `data/cline_history.json` |
| `templates/cline_template.html` | Template for Cline dashboard |
| `cline_dashboard.html` | Generated Cline output |

## Expected Output

Each dashboard generates a standalone HTML file with:

- **Summary Cards**: Total usage metrics (cost, tokens, sessions)
- **Interactive Charts**: Daily activity trends, model breakdown, token usage over time
- **Project Statistics**: Per-project breakdown with sortable tables
- **Cache Metrics**: Cache hit ratio and efficiency (Claude only)
- **Session Analysis**: Session length distribution and patterns

> [!TIP]
> Dashboards use Chart.js and TailwindCSS via CDN. Open directly in any browser—no server required.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `FileNotFoundError: ~/.claude.json` | Claude Code not installed or never run | Install Claude Code and run at least once |
| `FileNotFoundError: ~/.gemini/tmp` | Gemini CLI not used yet | Run Gemini CLI at least once to create history |
| Empty charts in dashboard | Aggregate script not run | Run the aggregate script first, then update |
| `Permission denied` | Protected directories | Check file permissions on data directories |
| VS Code data missing on Linux | Different path on Linux | Data is at `~/.config/Code/` instead of `~/Library/...` |
| Charts not rendering | Browser blocking CDN | Use a browser with internet access for Chart.js CDN |

## Testing

To verify the skill works correctly:

```bash
# 1. Check data sources exist
ls ~/.claude.json          # Should exist for Claude dashboard
ls ~/.gemini/tmp/          # Should exist for Gemini dashboard

# 2. Run aggregate + update
python3 ~/.claude/skills/llms-dashboard/scripts/aggregate_claude_history.py
python3 ~/.claude/skills/llms-dashboard/scripts/update_claude_dashboard.py

# 3. Verify output
ls -la ~/.claude/skills/llms-dashboard/claude_dashboard.html  # Should be recent
open ~/.claude/skills/llms-dashboard/claude_dashboard.html    # Should show charts
```

**Success indicators:**
- Dashboard HTML file is generated with recent timestamp
- Summary cards show non-zero values
- Charts render with data points
- No Python errors during script execution
