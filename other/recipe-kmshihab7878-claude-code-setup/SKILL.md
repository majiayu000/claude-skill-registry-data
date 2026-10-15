---
name: recipe
description: Parameterized YAML workflow recipes — create, run, list, and compose shareable automation packages with typed inputs, sub-recipes, and extension bundling (inspired by Goose)
type: skill
triggers:
  - /recipe
  - When user asks to create, run, or manage workflow recipes
  - When user wants to package a repeatable workflow
---

# Recipe System for Claude Code

Recipes are parameterized, composable, shareable YAML workflow definitions.
They package instructions + required tools + typed parameters + sub-recipes into portable automation units.

## Recipe Schema

```yaml
version: "1.0"
title: "Human-readable recipe name"
description: "What this recipe does"
author: "creator name"
tags: ["domain", "category"]

# Typed parameters — resolved before execution
parameters:
  - key: param_name
    input_type: string | number | boolean | select | file
    description: "What this parameter controls"
    requirement: required | optional
    default: "default value"
    options: ["a", "b", "c"]  # only for select type

# MCP servers and skills required
requires:
  mcp_servers: ["github", "filesystem"]
  skills: ["security-review"]
  cli_tools: ["ruff", "trivy"]

# Sub-recipes — composable building blocks
sub_recipes:
  - name: "step_name"
    path: "./sub/step.yaml"
    params:
      inherited_param: "{{ parent_param }}"

# Agent routing — which agent should execute
routing:
  agent: "security-engineer"
  authority: "L2"
  risk_tier: "T1"
  fallback: "code-reviewer"

# The prompt template — Jinja-style {{ param }} interpolation
prompt: |
  Execute the following workflow:
  Target: {{ target }}
  Depth: {{ depth }}
  
  Steps:
  1. First do X
  2. Then do Y
  3. Finally verify Z
```

## Recipe Directory

All recipes stored in `~/.claude/recipes/`:
```
~/.claude/recipes/
  lib/              # Shared utilities (recipe-runner.sh)
  sub/              # Reusable sub-recipes
  security/         # Security domain recipes
  engineering/      # Engineering domain recipes
  trading/          # Trading domain recipes
  README.md         # Recipe catalog
```

## Commands

### Create a Recipe
```
/recipe create <name>
```
Interactive recipe builder:
1. Ask for title, description, tags
2. Ask for parameters (name, type, required/optional, default)
3. Ask for required MCP servers and skills
4. Ask for agent routing preferences
5. Ask for the prompt template
6. Write YAML to `~/.claude/recipes/<domain>/<name>.yaml`

### Run a Recipe
```
/recipe run <name> [--param key=value ...]
```
Execution flow:
1. Load recipe YAML from `~/.claude/recipes/`
2. Validate all required parameters are provided (prompt for missing ones)
3. Resolve `{{ param }}` placeholders in prompt
4. Verify required MCP servers are available
5. Verify required skills exist
6. Load sub-recipes recursively (max depth 3)
7. Route to specified agent or execute directly
8. Track execution in `~/.claude/recipes/lib/history.jsonl`

### List Recipes
```
/recipe list [--domain <domain>] [--tag <tag>]
```
Show all available recipes with their parameters and descriptions.

### Convert Skill to Recipe
```
/recipe convert <skill-name>
```
Read an existing SKILL.md file and generate a parameterized recipe YAML from it:
1. Extract the skill's triggers and description
2. Identify implicit parameters (things the skill expects the user to provide)
3. Map skill's MCP server usage to `requires.mcp_servers`
4. Generate the recipe YAML
5. Preserve the original skill (recipes complement, don't replace)

## Execution Rules

1. **Parameter validation first** — never execute with missing required params
2. **Tool verification** — confirm MCP servers are active before running
3. **Sub-recipe depth limit** — max 3 levels of nesting
4. **History tracking** — log every execution with params, duration, outcome
5. **Template safety** — sanitize parameter values before interpolation (no command injection)
6. **Composability** — sub-recipes can reference other sub-recipes
7. **Idempotency** — recipes should be safe to re-run (document exceptions)

## Parameter Resolution Order

1. CLI `--param key=value` arguments (highest priority)
2. Recipe `default` values
3. Interactive prompt for missing required params
4. Environment variables matching `RECIPE_<KEY>` pattern

## Example: Security Audit Recipe

```yaml
version: "1.0"
title: "Security Audit Pipeline"
description: "Full security audit: dependency scan, SAST, secrets detection, container scan"
author: "<your-name>"
tags: ["security", "audit", "ci"]

parameters:
  - key: target_path
    input_type: string
    description: "Path to scan (relative or absolute)"
    requirement: required
    default: "."
  - key: scan_depth
    input_type: select
    description: "How thorough the scan should be"
    requirement: optional
    default: "standard"
    options: ["quick", "standard", "deep"]
  - key: fix_issues
    input_type: boolean
    description: "Auto-fix safe issues"
    requirement: optional
    default: false

requires:
  mcp_servers: ["filesystem"]
  skills: ["security-review"]
  cli_tools: ["trivy", "gitleaks", "semgrep", "ruff"]

routing:
  agent: "security-engineer"
  authority: "L2"
  risk_tier: "T1"
  fallback: "security-auditor"

prompt: |
  Run a {{ scan_depth }} security audit on {{ target_path }}.
  
  Steps:
  1. Dependency vulnerability scan: `trivy fs {{ target_path }}`
  2. Secret detection: `gitleaks detect --source={{ target_path }}`
  3. SAST analysis: `semgrep --config=auto {{ target_path }}`
  4. Python lint (if applicable): `ruff check {{ target_path }}`
  {% if fix_issues %}
  5. Auto-fix safe issues where possible
  {% endif %}
  
  Report findings by severity (Critical > High > Medium > Low).
  For each finding: file, line, description, remediation.
```
