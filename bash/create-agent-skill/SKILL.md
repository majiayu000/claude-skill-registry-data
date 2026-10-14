---
name: create-agent-skill
description: Guides the creation of new Agent Skills following the AgentSkills.io specification. Covers required frontmatter (name, description), optional metadata, directory structure (SKILL.md, references/, scripts/, assets/), progressive disclosure principles, and naming conventions. Use when creating a new skill from scratch, adding project-specific agent knowledge, defining reusable patterns for AI coding assistants, or structuring domain expertise as a skill. Triggers on "create skill", "new skill", "add skill", "write a skill", "skill template", "SKILL.md", "agent skill".
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Authoring meta-skill — guides SKILL.md creation; no deployed resource and no deploy verb. Client-agnostic. On Genie Code, write the new skill folder under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`), not a bare relative path — relative paths resolve against the page CWD (see `skills/genie-code-environment` §8)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: admin
  role: utility
  standalone: true
  source: AgentSkills.io Specification
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Internal convention (AgentSkills.io spec)
---

# Create Agent Skills

A guide for creating new Agent Skills following the [AgentSkills.io specification](https://agentskills.io/specification). Agent Skills are portable, structured knowledge units that give AI coding assistants specialized capabilities.

## When to Use

- Creating a brand-new skill from scratch
- Adding domain-specific knowledge for an AI agent
- Structuring reusable patterns, workflows, or best practices as a skill
- Defining how the agent should handle a specific technology or task

---

## Quick Start: Minimal Skill

```bash
SKILL_NAME="my-skill-name"
mkdir -p "data_product_accelerator/skills/admin/${SKILL_NAME}"
```

Then create `SKILL.md`:

```markdown
---
name: my-skill-name
description: What this skill does. When to use it. Trigger phrases and scenarios.
---

# My Skill Title

Brief overview.

## When to Use

- Scenario 1
- Scenario 2

## Instructions

Step-by-step guidance.

## Examples

Concrete examples.
```

---

## Required Fields

### `name` (Required)

| Rule | Detail |
|------|--------|
| Max length | 64 characters |
| Characters | `a-z`, `0-9`, `-` only |
| No leading/trailing hyphens | `my-skill` OK, `-my-skill-` BAD |
| No consecutive hyphens | `my-skill` OK, `my--skill` BAD |
| Must match directory name | `my-skill/SKILL.md` → `name: my-skill` |

### `description` (Required)

| Rule | Detail |
|------|--------|
| Max length | 1024 characters |
| Must be non-empty | Cannot be blank |
| Third person voice | "Provides guidance..." not "I provide..." |
| Include WHAT + WHEN | Describe what the skill does AND when to use it |
| Include trigger phrases | Keywords that should activate this skill |

**Good example:**
```yaml
description: Provides patterns for creating Databricks Delta Live Tables (DLT) pipelines with data quality expectations. Covers streaming ingestion, quarantine patterns, and expectation configuration. Use when building Silver layer pipelines, adding data quality checks, or configuring DLT expectations. Triggers on "DLT", "expectations", "streaming", "quarantine".
```

---

## Optional Fields

```yaml
license: Apache-2.0                    # SPDX license identifier
metadata:
  author: your-name                    # Author or team
  version: "1.0.0"                     # Semantic version (quoted)
  domain: admin                        # Domain category
  source: "Description of origin"      # Where the knowledge came from
```

---

## Directory Structure

```
my-skill/
├── SKILL.md              # REQUIRED — Main instructions (<500 lines)
├── references/           # OPTIONAL — Detailed docs loaded on demand
│   ├── api-reference.md
│   └── advanced-patterns.md
├── scripts/              # OPTIONAL — Executable utilities
│   └── validate.py
└── assets/
    └── templates/        # OPTIONAL — Starter files to copy
        └── config.yaml
```

### When to Create Each Directory

| Directory | Create When... |
|-----------|----------------|
| `references/` | SKILL.md would exceed 500 lines without splitting |
| `scripts/` | Reusable code blocks exceed 10 lines |
| `assets/templates/` | Templates, configs, or starter files exist |

---

## Progressive Disclosure

**Core principle:** Keep SKILL.md lightweight. Move details to subdirectories.

### What Stays in SKILL.md (~1-2K tokens)

- Overview and purpose
- Critical rules (the "never do X" type)
- Quick reference tables
- Links to references, scripts, assets
- Decision guides

### What Moves to references/

- Comprehensive API docs
- Extended pattern libraries
- Validation checklists
- Troubleshooting guides
- Edge case documentation

### What Moves to scripts/

- Validation utilities
- Setup automation
- Code generation tools
- Data extraction helpers

### What Moves to assets/templates/

- YAML configuration templates
- SQL DDL templates
- Job configuration starters
- Skeleton files to copy

### Working Memory (Orchestrators Only)

Orchestrator skills with 3+ phases must include a `## Working Memory Management` section. Workers must end with a `## [Domain] Notes to Carry Forward` section and a `## Next Step` section. See [Progressive Disclosure Patterns](references/progressive-disclosure.md) for Strategy 4 details.

---

## Naming and Organization

### Skill Location

Place skills under `data_product_accelerator/skills/{domain}/`:

```
skills/
├── admin/            # Administrative skills
├── bronze/           # Bronze layer patterns
├── silver/           # Silver layer patterns
├── gold/             # Gold layer patterns
├── common/           # Cross-cutting concerns
├── semantic-layer/   # Metric views, TVFs, Genie
├── monitoring/       # Monitoring, dashboards, alerts
├── ml/               # Machine learning patterns
├── planning/         # Project planning
└── exploration/      # Ad-hoc analysis
```

### File Naming

- Directories: `kebab-case` (e.g., `my-skill-name/`)
- SKILL.md: Always `SKILL.md` (exact casing)
- References: `kebab-case.md` (e.g., `api-reference.md`)
- Scripts: `snake_case.py` or `kebab-case.sh`
- Templates: `kebab-case.yaml`, `kebab-case.sql`

---

## Skill Quality Checklist

Before finalizing a new skill:

### Structure
- [ ] `name` matches directory name, max 64 chars, valid characters
- [ ] `description` includes WHAT + WHEN + trigger phrases, max 1024 chars
- [ ] SKILL.md is under 500 lines
- [ ] References are one level deep (no nested references)

### Content
- [ ] Instructions are actionable (agent can follow them)
- [ ] Examples are concrete, not abstract
- [ ] Correct and incorrect patterns shown where applicable
- [ ] Links to references/ files use relative paths

### Discovery
- [ ] Description has clear trigger keywords
- [ ] Skill is registered in skill-navigator (update Tier 3 table + routing table + directory map)
- [ ] Domain index in navigator references/ is updated

---

## After Creating a Skill

**Always update the skill-navigator:**

1. Add to Tier 3 table in `skill-navigator/SKILL.md`
2. Add routing keywords to the Task Detection & Routing Table
3. Add to the Complete Skill Directory Map
4. Update the appropriate domain index in `skill-navigator/references/domain-indexes.md`

---

## Additional Resources

- [AgentSkills.io Specification](https://agentskills.io/specification) — Official format specification
- [Progressive Disclosure Patterns](references/progressive-disclosure.md) — How to split large skills
- [Skill Examples](references/skill-examples.md) — Annotated examples of well-structured skills
