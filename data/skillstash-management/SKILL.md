---
name: skillstash-management
description: How to create, validate, and manage skills in this skillstash instance
---

# Skillstash Management

This skill tells you how to work with this repository. Use it whenever you need to create, modify, or manage skills.

## When to Use This Skill

- Creating a new skill
- Modifying an existing skill
- Understanding the repo structure
- Running validation
- Pushing skills for review

## Repository Structure

```text
skillstash/
├── skills/                    # All skills live here
│   └── my-skill/
│       ├── SKILL.md           # Required - skill definition
│       ├── references/        # Optional - docs, specs
│       ├── scripts/           # Optional - executable helpers
│       └── assets/            # Optional - templates, configs
├── .skillstash/
│   └── config.yml             # Skillstash configuration
├── docs/                      # Skillstash documentation
├── scripts/                   # Skillstash automation
└── .agents/                   # Agent instructions
```

## Creating a Skill

### 1. Create the Directory

```bash
mkdir -p skills/my-skill-name
```

Use **kebab-case** for directory names.

### 2. Create SKILL.md

Every skill requires a `SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill-name
description: Brief one-line description of what this skill does
---

# My Skill Name

## When to Use This Skill

Describe trigger conditions.

## What This Skill Does

Step-by-step instructions.

## Examples

Concrete usage examples.
```

### 3. Required Frontmatter

| Field | Description |
| ----- | ----------- |
| `name` | Must match directory name exactly (kebab-case) |
| `description` | One-line summary for discovery |

### 4. Optional Frontmatter

| Field | Description |
| ----- | ----------- |
| `version` | Semver (e.g., `1.0.0`) |
| `author` | GitHub username |
| `tags` | Array for categorization |
| `status` | `experimental`, `stable`, `deprecated` |

## Validation Rules

Skills must pass these checks:

| Rule | Requirement |
| ---- | ----------- |
| **SKILL.md exists** | Required file in skill directory |
| **Valid frontmatter** | YAML must parse, required fields present |
| **Name matches** | `name` field must equal directory name |
| **Kebab-case** | Directory name: lowercase, hyphens only |
| **Max 500 lines** | Keep skills focused and maintainable |

### Running Validation Locally

```bash
bun run validate
```

## Local-First Workflow

**Zero latency**: Skills work immediately after saving.

1. Create `skills/my-skill/SKILL.md`
2. Save the file
3. The skill is now discoverable and usable
4. Iterate: edit, save, test, repeat

No git push required for local use.

## Branch Naming Convention

Skill branches **must** follow this pattern:

| Pattern | Use case |
| ------- | -------- |
| `skill/add-<slug>` | Creating a new skill |
| `skill/update-<slug>` | Modifying an existing skill |
| `skill/remove-<slug>` | Deleting a skill |

The `merge-readiness` check enforces this. PRs with wrong branch names will fail.

## Pushing for Permanence

When the skill works locally:

```bash
# Create branch with correct naming
git checkout -b skill/add-my-skill

# Commit and push with Graphite
gt create -am "feat: add my-skill for [purpose]"
gt submit --no-interactive
```

## Merge Readiness

PRs touching `skills/**` run the `merge-readiness` check which validates:

| Check | Blocking |
| ----- | -------- |
| Branch naming (`skill/*`) | Yes |
| Required labels exist | No (warning) |
| Auto-merge enabled | No (warning) |
| Merge settings correct | No (warning) |

Once checks pass, enable auto-merge on the PR. It merges automatically when validation completes.

## Optional Supporting Files

### references/

External documentation, API specs, research notes.

```text
skills/my-skill/references/
└── api-docs.md
```

### scripts/

Executable helpers for the skill.

```text
skills/my-skill/scripts/
└── setup.sh
```

### assets/

Templates, images, configuration files.

```text
skills/my-skill/assets/
└── config-template.json
```

### .research/

Temporary research notes. Removed before merge.

## Issue-Driven Workflow

For tracked work, use beads:

```bash
# Create issue
bd create --title="Create [skill-name] skill" --type=feature

# Claim work
bd update <id> --status=in_progress

# Implement skill (local-first)

# Close when done
bd close <id>
bd sync
```

## Best Practices

1. **Start simple** - Minimal viable skill, iterate to add features
2. **Keep focused** - One skill solves one problem well
3. **Document clearly** - Future you (or agents) will thank you
4. **Test locally** - Verify before pushing
5. **Under 500 lines** - If longer, consider splitting

## Common Issues

### Skill Not Discovered

- Verify `SKILL.md` exists with frontmatter
- Check `name` field matches directory name
- Ensure directory is under `skills/`

### Validation Fails

- Run `bun run validate` locally
- Check frontmatter YAML syntax
- Verify name is kebab-case
- Check line count (max 500)

### Name Mismatch

```yaml
# Directory: skills/my-skill/
# Frontmatter must match:
---
name: my-skill  # Correct
name: mySkill   # Wrong - will fail validation
---
```
