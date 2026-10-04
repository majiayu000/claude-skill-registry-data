---
name: continuous-learning
description: Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. Features project-scoped instincts to prevent cross-project contamination.
---

# Continuous Learning - Instinct-Based Architecture

An advanced learning system that turns your Codex sessions into reusable knowledge through atomic "instincts" - small learned behaviors with confidence scoring.

Features **project-scoped instincts** — React patterns stay in your React project, Python conventions stay in your Python project, and universal patterns (like "always validate input") are shared globally.

## When to Activate

- Setting up automatic learning from Codex sessions
- Configuring instinct-based behavior extraction via hooks
- Tuning confidence thresholds for learned behaviors
- Reviewing, exporting, or importing instinct libraries
- Evolving instincts into full skills, commands, or agents
- Managing project-scoped vs global instincts
- Promoting instincts from project to global scope

## The Instinct Model

An instinct is a small learned behavior:

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "my-react-app"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

**Properties:**
- **Atomic** -- one trigger, one action
- **Confidence-weighted** -- 0.3 = tentative, 0.9 = near certain
- **Domain-tagged** -- code-style, testing, git, debugging, workflow, etc.
- **Evidence-backed** -- tracks what observations created it
- **Scope-aware** -- `project` (default) or `global`

## How It Works

```
Session Activity (in a git repo)
      |
      | Hooks capture prompts + tool use (100% reliable)
      | + detect project context (git remote / repo path)
      v
+---------------------------------------------+
|  projects/<project-hash>/observations.jsonl |
|   (prompts, tool calls, outcomes, project)  |
+---------------------------------------------+
      |
      | Observer agent reads (background)
      v
+---------------------------------------------+
|          PATTERN DETECTION                  |
|   * User corrections -> instinct            |
|   * Error resolutions -> instinct           |
|   * Repeated workflows -> instinct          |
|   * Scope decision: project or global?      |
+---------------------------------------------+
      |
      | Creates/updates
      v
+---------------------------------------------+
|  projects/<project-hash>/instincts/personal/|
|   * prefer-functional.yaml (0.7) [project]  |
|   * use-react-hooks.yaml (0.9) [project]    |
+---------------------------------------------+
|  instincts/personal/  (GLOBAL)              |
|   * always-validate-input.yaml (0.85)[global|
|   * grep-before-edit.yaml (0.6) [global]    |
+---------------------------------------------+
      |
      | /evolve clusters + /promote
      v
+---------------------------------------------+
|  projects/<hash>/evolved/ (project-scoped)  |
|  evolved/ (global)                          |
|   * commands/new-feature.md                 |
|   * skills/testing-workflow.md              |
|   * agents/refactor-specialist.md           |
+---------------------------------------------+
```

## Project Detection

The system automatically detects your current project:

1. **`CODEX_PLUGIN_PROJECT_DIR` env var** (highest priority)
2. **`git remote get-url origin`** -- hashed to create a portable project ID (same repo on different machines gets the same ID)
3. **`git rev-parse --show-toplevel`** -- fallback using repo path (machine-specific)
4. **Global fallback** -- if no project is detected, instincts go to global scope

Each project gets a 12-character hash ID (e.g., `a1b2c3d4e5f6`). A registry file at `~/.codex/codex-plugin/continuous-learning/projects.json` maps IDs to human-readable names.

## Quick Start

### 1. Enable Observation Hooks

The continuous learning observation hooks are bundled as part of the plugin in the `hooks/hooks.json` file. When the plugin is installed and trusted, Codex can run them on `PreToolUse` and `PostToolUse`.

### 2. Initialize Directory Structure

The system creates directories automatically on first use, but you can also create them manually:

```bash
# Global directories
mkdir -p ~/.codex/codex-plugin/continuous-learning/{instincts/{personal,inherited},evolved/{agents,skills,commands},projects}

# Project directories are auto-created when the hook first runs in a git repo
```

### 3. Use the Instinct Commands

```bash
python3 scripts/instinct-cli.py status     # Show learned instincts (project + global)
python3 scripts/instinct-cli.py evolve     # Cluster related instincts into skills/commands
python3 scripts/instinct-cli.py export     # Export instincts to file
python3 scripts/instinct-cli.py import     # Import instincts from others
python3 scripts/instinct-cli.py promote    # Promote project instincts to global scope
python3 scripts/instinct-cli.py projects   # List all known projects and their instinct counts
```

## Configuration

Configuration is managed with environment variables and Codex plugin settings. Use `CODEX_PLUGIN_OBSERVER_ENABLED=true` to enable observation.

| Setting | Default | Description |
|-----|---------|-------------|
| **Observer Enabled** | `false` | Enable the background observer agent |
| **Run Interval** | `5` | How often the observer analyzes observations (in minutes) |
| **Min Observations** | `20` | Minimum observations before analysis runs |

Other behavior (observation capture, instinct thresholds, project scoping, promotion criteria) is configured via code defaults in `scripts/instinct-cli.py` and `hooks/observe.sh`.

## File Structure

```
~/.codex/codex-plugin/continuous-learning/
+-- identity.json           # Your profile, technical level
+-- projects.json           # Registry: project hash -> name/path/remote
+-- observations.jsonl      # Global observations (fallback)
+-- instincts/
|   +-- personal/           # Global auto-learned instincts
|   +-- inherited/          # Global imported instincts
+-- evolved/
|   +-- agents/             # Global generated agents
|   +-- skills/             # Global generated skills
|   +-- commands/           # Global generated commands
+-- projects/
    +-- a1b2c3d4e5f6/       # Project hash (from git remote URL)
    |   +-- project.json    # Per-project metadata mirror (id/name/root/remote)
    |   +-- observations.jsonl
    |   +-- observations.archive/
    |   +-- instincts/
    |   |   +-- personal/   # Project-specific auto-learned
    |   |   +-- inherited/  # Project-specific imported
    |   +-- evolved/
    |       +-- skills/
    |       +-- commands/
    |       +-- agents/
    +-- f6e5d4c3b2a1/       # Another project
        +-- ...
```

## Scope Decision Guide

| Pattern Type | Scope | Examples |
|-------------|-------|---------|
| Language/framework conventions | **project** | "Use React hooks", "Follow Django REST patterns" |
| File structure preferences | **project** | "Tests in `__tests__`/", "Components in src/components/" |
| Code style | **project** | "Use functional style", "Prefer dataclasses" |
| Error handling strategies | **project** | "Use Result type for errors" |
| Security practices | **global** | "Validate user input", "Sanitize SQL" |
| General best practices | **global** | "Write tests first", "Always handle errors" |
| Tool workflow preferences | **global** | "Grep before Edit", "Read before Write" |
| Git practices | **global** | "Conventional commits", "Small focused commits" |

## Instinct Promotion (Project -> Global)

When the same instinct appears in multiple projects with high confidence, it's a candidate for promotion to global scope.

**Auto-promotion criteria:**
- Same instinct ID in 2+ projects
- Average confidence >= 0.8

**How to promote:**

```bash
# Promote a specific instinct
python3 scripts/instinct-cli.py promote prefer-explicit-errors

# Auto-promote all qualifying instincts
python3 scripts/instinct-cli.py promote

# Preview without changes
python3 scripts/instinct-cli.py promote --dry-run
```

## Confidence Scoring

Confidence evolves over time:

| Score | Meaning | Behavior |
|-------|---------|----------|
| 0.3 | Tentative | Suggested but not enforced |
| 0.5 | Moderate | Applied when relevant |
| 0.7 | Strong | Auto-approved for application |
| 0.9 | Near-certain | Core behavior |

**Confidence increases** when:
- Pattern is repeatedly observed
- User doesn't correct the suggested behavior
- Similar instincts from other sources agree

**Confidence decreases** when:
- User explicitly corrects the behavior
- Pattern isn't observed for extended periods
- Contradicting evidence appears

## Why Hooks for Observation?

Hooks fire **100% of the time**, deterministically. This means:
- Every tool call is observed
- No patterns are missed
- Learning is comprehensive

## Privacy

- Observations stay **local** on your machine
- Project-scoped instincts are isolated per project
- Only **instincts** (patterns) can be exported — not raw observations
- No actual code or conversation content is shared
- You control what gets exported and promoted

---

*Instinct-based learning: teaching Codex your patterns, one project at a time.*
