---
name: install-toolkit-skills
description: Install skills from the claude-code-plugins-plus-skills catalog to the current project via interactive selection. Use when the user asks to add skills, browse the skill catalog, install toolkit skills, or says "install toolkit skills". Covers all 519 skills across 21 categories.
allowed-tools: Bash, Read
version: 2.0.0
author: Intent Solutions IO <jeremy@intentsolutions.io>
license: MIT
compatibility: Designed for Claude Code
tags: [skills, installation, catalog, toolkit]
---

# Install Toolkit Skills

**Install any of 519 skills from the claude-code-plugins-plus-skills catalog into the current project.**

## Live Catalog Summary

!`ccpi skills list --json 2>/dev/null | python3 -c "import json,sys; skills=json.load(sys.stdin); cats={}; [cats.setdefault(s['category'],[]).append(s) for s in skills]; total=len(skills); installed=sum(1 for s in skills if s['installed']); print(f'Total: {total} skills across {len(cats)} categories ({installed} installed in current surface)'); [print(f'  {cat}: {len(ss)} skills') for cat,ss in sorted(cats.items())]" 2>/dev/null || echo "Run ccpi skills list to see the full catalog"`

## Skill Categories

The catalog has 21 categories. Use `ccpi skills list --category <name>` to explore each:

| #   | Category              | Coverage                                                    |
| --- | --------------------- | ----------------------------------------------------------- |
| 01  | devops-basics         | Bash, CI/CD, containers, git workflows                      |
| 02  | devops-advanced       | Kubernetes, Terraform, observability                        |
| 03  | security-fundamentals | API keys, CORS, injection, JWT, secrets                     |
| 04  | security-advanced     | Penetration testing, threat modeling                        |
| 05  | frontend              | React, CSS, accessibility, performance                      |
| 06  | backend               | APIs, databases, auth, caching                              |
| 07  | data-engineering      | ETL, pipelines, Spark, data quality                         |
| 08  | ml-and-ai             | Model training, MLOps, LLM workflows                        |
| 09  | testing               | Unit, integration, e2e, load testing                        |
| 10  | architecture          | System design, patterns, ADRs                               |
| 11  | cloud-aws             | EC2, S3, Lambda, EKS, IAM                                   |
| 12  | cloud-gcp             | GKE, Cloud Run, BigQuery, Vertex                            |
| 13  | cloud-azure           | AKS, Functions, Cosmos, DevOps                              |
| 14  | mobile                | iOS, Android, React Native, Flutter                         |
| 15  | documentation         | READMEs, API docs, changelogs                               |
| 16  | productivity          | Workflows, automation, scripts                              |
| 17  | code-quality          | Linting, refactoring, code review                           |
| 18  | collaboration         | PRs, reviews, team workflows                                |
| 19  | monitoring            | Logging, alerting, dashboards                               |
| 20  | enterprise-workflows  | Compliance, governance, release mgmt                        |
| 21  | toolkit               | Claude docs, hooks, skill management, Apple, design systems |

## Trigger Matching

When a user request matches any skill topic above:

1. **Check if the skill is installed** in `<workspace>/.claude/skills/`
2. **If installed** → The skill handles the request
3. **If NOT installed** → Offer: _"The `<skill-name>` skill covers this — want me to install it?"_
4. **If user says yes** → Run the installation workflow below

## Installation Workflow

### Step 1: Find Workspace Root

```bash
WORKSPACE_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

### Step 2: Show the Catalog

Show the full catalog grouped by category, with installation status:

```bash
ccpi skills list --surface project
```

Or filter to a specific area:

```bash
ccpi skills list --category security --surface project
ccpi skills list --category devops --surface project
```

Or search by keyword:

```bash
ccpi search kubernetes
ccpi search "api testing"
```

Let the user pick by number, name, category keyword, or shortcut.

**Common shortcuts:**

- `"all"` → install all 519 skills
- `"devops"` → install all devops skills (01 + 02)
- `"security"` → install all security skills (03 + 04)
- `"docs"` → install claude-docs-skill, openrouter-docs-skill, warp-docs-skill, gemini-docs-skill
- Numbers or ranges → `1,3,5` or `1-5`

### Step 3: Install Selected Skills

```bash
# Project-local install (recommended)
ccpi skills install <skill-name> --surface project

# Global install (available in every project)
ccpi skills install <skill-name> --surface claude

# Install all in a category
ccpi skills install --category security --surface project

# Install all skills at once
ccpi skills install --all --surface project
```

**If `ccpi` is not installed**, use the raw symlink fallback:

```bash
CATALOG_DIR="$HOME/Projects/Dev_projects/Claude_SDK/claude-code-plugins-plus-skills/skills"
# Find the skill's category first:
find "$CATALOG_DIR" -name "SKILL.md" -path "*/<skill-name>/SKILL.md"
# Then symlink it:
ln -sfn "$CATALOG_DIR/<category>/<skill-name>" "$WORKSPACE_ROOT/.claude/skills/<skill-name>"
```

### Step 4: Report Results

```markdown
## Skills Installed

**Workspace:** {workspace_root}
**Method:** symlinked from claude-code-plugins-plus-skills/skills/<category>/

### Installed:

- {list of installed skills with categories}

Skills are immediately available via Claude Code hot-reload.
To uninstall: `ccpi skills remove <skill-name> --surface project`
```

## Notes

- Skills are **symlinked** to `<workspace>/.claude/skills/` — NOT copied
- Source: `~/Projects/Dev_projects/Claude_SDK/claude-code-plugins-plus-skills/skills/<category>/<skill-name>/`
- Claude Code discovers skills automatically (hot-reload, no restart needed)
- Doc skills have large reference files (24MB+) — symlinks prevent duplication
- To list all skills: `ccpi skills list`
- To search: `ccpi search <query>`
- To uninstall: `ccpi skills remove <skill-name> --surface project`
- Tutorials: `ccpi tutorials` (11 Jupyter notebooks on skills, plugins, and orchestration)
