---
name: constraint-discovery
description: Spawn 5 parallel Explore agents to discover project constraints. TRIGGERS - constraint scan, degrees of freedom, /ralph:start Step 1.4.5, project memory analysis.
allowed-tools: Task, TaskOutput, Bash, Read, Grep, Glob
---

# Constraint Discovery Skill

Spawn 5 parallel Explore agents to discover constraints that limit Claude's degrees of freedom.

## When to Use

- Invoked by `/ralph:start` Step 1.4.5 via Skill tool
- User asks to analyze project constraints
- User mentions "degrees of freedom" or "constraint scan"
- Standalone constraint analysis needed

## Agents

### Agent 1: Project Memory & Philosophy Constraints

```
Task tool parameters:
  description: "Analyze project memory constraints"
  subagent_type: "Explore"
  run_in_background: true
  prompt: |
    DEEP DIVE into project memory files AND FOLLOW ALL @ LINKS to discover constraints.

    STEP 1 - READ THESE FILES FIRST:
    - CLAUDE.md (project instructions, philosophy, forbidden patterns)
    - .claude/ directory (memories, settings, agents/*.md)
    - .claude/agents/*.md (agent definitions with @ references)
    - ROADMAP.md (P0/P1 priorities, explicit scope limits)
    - docs/adr/ (Architecture Decision Records)

    STEP 2 - FOLLOW ALL @ LINKS (UNLIMITED DEPTH):
    Parse each file for @ link patterns:
    - @path/to/file.md (relative to project root)
    - @ai_context/PHILOSOPHY.md (ai_context directory)
    - @projectname/path/to/file.md (project prefix)
    - @AGENTS.md, @README.md (root files)

    For EACH @ link found:
    1. Read the linked file
    2. Parse it for more @ links
    3. Recursively follow until no new @ links found

    STEP 3 - EXTRACT CONSTRAINTS FROM ALL FILES:
    - "Do NOT modify X" instructions
    - Philosophy rules (e.g., "prefer simplicity over features")
    - Explicit forbidden patterns
    - Scope limits from ROADMAP

    Return NDJSON: {"source":"agent-memory","severity":"CRITICAL|HIGH|MEDIUM","description":"...","file":"...","linked_from":"...","recommendation":"Ralph should avoid..."}
```

### Agent 2: Architecture & Coupling Constraints

```
Task tool parameters:
  description: "Analyze architectural constraints"
  subagent_type: "Explore"
  run_in_background: true
  prompt: |
    Analyze architectural patterns that constrain safe modification.

    STEP 1 - READ THESE FILES:
    - pyproject.toml, setup.py (package structure, entry points)
    - Core module __init__.py files (public API surface)
    - docs/adr/ (past architectural decisions)
    - docs/reference/interfaces.md (if exists)

    STEP 2 - FOLLOW @ LINKS (UNLIMITED DEPTH):
    Parse for @ link patterns in ADRs and docs:
    - @docs/reference/*.md, @docs/architecture/*.md
    - @ai_context/*.md (philosophy files)
    Recursively follow until no new @ links found.

    STEP 3 - EXTRACT CONSTRAINTS:
    - Circular imports, tightly coupled modules
    - Public API that cannot change without breaking users
    - Package structure assumptions
    - Cross-layer dependencies

    Return NDJSON: {"source":"agent-arch","severity":"HIGH|MEDIUM|LOW","description":"...","modules":["A","B"],"linked_from":"...","recommendation":"..."}
```

### Agent 3: Research Session Lessons Learned

```
Task tool parameters:
  description: "Extract research session constraints"
  subagent_type: "Explore"
  run_in_background: true
  prompt: |
    Analyze past research sessions to find lessons learned and forbidden patterns.

    STEP 1 - READ THESE FILES:
    - outputs/research_sessions/*/research_summary.md (most recent 3)
    - outputs/research_sessions/*/research_log.md (if exists)
    - outputs/research_sessions/*/production_config.yaml
    - Any "lessons_learned" or "warnings" sections

    STEP 2 - FOLLOW @ LINKS:
    Research summaries may reference:
    - @strategies/*.yaml (strategy configs that failed)
    - @docs/guides/*.md (guides with constraints)
    Recursively follow until no new @ links found.

    STEP 3 - EXTRACT CONSTRAINTS:
    - Failed experiments (don't repeat these)
    - Hyperparameter ranges that caused issues
    - Strategies that were abandoned and why
    - Explicit warnings from past sessions
    - "Do not explore below X" thresholds

    Return NDJSON: {"source":"agent-research","severity":"HIGH|MEDIUM","description":"Past session found: ...","session":"...","linked_from":"...","recommendation":"Avoid..."}
```

### Agent 4: Testing & Validation Constraints

```
Task tool parameters:
  description: "Find testing constraints"
  subagent_type: "Explore"
  run_in_background: true
  prompt: |
    Find testing gaps and validation requirements that constrain safe changes.

    STEP 1 - READ THESE FILES:
    - tests/ directory structure
    - pytest.ini, pyproject.toml [tool.pytest] section
    - CI/CD workflows (.github/workflows/)
    - docs/development/testing.md (if exists)

    STEP 2 - FOLLOW @ LINKS:
    Testing docs may reference:
    - @docs/development/*.md (dev guides)
    - @ai_context/*.md (philosophy that affects testing)
    Recursively follow until no new @ links found.

    STEP 3 - EXTRACT CONSTRAINTS:
    - Modules with zero test coverage (risky to modify)
    - Integration tests that must pass
    - Validation thresholds (e.g., min Sharpe ratio, max drawdown)
    - Pre-commit hooks and their requirements
    - "Tests must pass before X" gates

    Return NDJSON: {"source":"agent-testing","severity":"HIGH|MEDIUM|LOW","description":"...","location":"...","linked_from":"...","recommendation":"..."}
```

### Agent 5: Degrees of Freedom Analysis

```
Task tool parameters:
  description: "Analyze degrees of freedom"
  subagent_type: "Explore"
  run_in_background: true
  prompt: |
    Find explicit and implicit limits on what Ralph can explore.

    STEP 1 - READ THESE FILES:
    - CLAUDE.md (explicit instructions)
    - .claude/ralph-config.json (previous session guidance)
    - .claude/agents/*.md (agent definitions)
    - Config files (*.yaml, *.toml) for hardcoded limits

    STEP 2 - FOLLOW ALL @ LINKS (UNLIMITED DEPTH):
    Parse each file for @ link patterns:
    - @ai_context/IMPLEMENTATION_PHILOSOPHY.md
    - @ai_context/MODULAR_DESIGN_PHILOSOPHY.md
    - @docs/reference/*.md
    - @DISCOVERIES.md, @ai_working/decisions/
    Recursively follow until no new @ links found.

    STEP 3 - EXTRACT FREEDOM CONSTRAINTS:
    - Hard gates (if not X, skip silently)
    - One-way state transitions
    - Configuration that cannot be overridden at runtime
    - Feature flags and their current state
    - Philosophy constraints (e.g., "ruthless simplicity")
    - Escape hatches (--skip-X flags, override mechanisms)

    Return NDJSON: {"source":"agent-freedom","severity":"CRITICAL|HIGH|MEDIUM","description":"...","gate":"...","linked_from":"...","recommendation":"..."}
```

## Execution

**MANDATORY: Spawn ALL 5 Task tools in a SINGLE message** (parallel execution).

Use `run_in_background: true` for all agents.

## Blocking Gate

After spawning, use TaskOutput with `block: true` and `timeout: 30000` for each agent:

```
For EACH agent spawned:
  TaskOutput(task_id: "<agent_id>", block: true, timeout: 30000)
```

**Wait for ALL 5 agents** (or timeout after 30s each).

## Aggregation

Merge agent findings into constraint scan file:

```bash
/usr/bin/env bash << 'AGENT_MERGE_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
SCAN_FILE="$PROJECT_DIR/.claude/ralph-constraint-scan.jsonl"

# Claude MUST append each agent's NDJSON findings here:
# For each constraint JSON from agent output:
#   echo '{"_type":"constraint","source":"agent-env","severity":"HIGH","description":"..."}' >> "$SCAN_FILE"

echo "=== AGENT FINDINGS MERGED ==="
echo "Constraints in scan file:"
wc -l < "$SCAN_FILE" 2>/dev/null || echo "0"
AGENT_MERGE_SCRIPT
```

## Output

Each agent returns NDJSON with:
- `source`: Which agent found it (agent-memory, agent-arch, agent-research, agent-testing, agent-freedom)
- `severity`: CRITICAL, HIGH, MEDIUM, or LOW
- `description`: Human-readable constraint description
- `linked_from`: Which file the constraint was discovered from (for @ link tracing)
- `recommendation`: What Ralph should avoid or be careful about
