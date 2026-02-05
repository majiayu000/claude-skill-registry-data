---
name: how-to-publish-paks
description: |
  A practical guide for creating and publishing Agent Skills (paks) to the Paks registry. Covers SKILL.md format, frontmatter structure, validation, versioning, and publishing workflow.
license: MIT
tags:
  - paks
  - agent-skills
  - publishing
  - skill-creation
  - registry
  - paks-cli
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.4"
---

# How to Publish Paks (Agent Skills)

## Overview

Paks are reusable instruction sets that enhance AI coding agents. This guide covers the complete workflow from creation to publishing on the Paks registry.

## Prerequisites

- `paks` CLI installed (`brew tap stakpak/stakpak && brew install paks`)
- Stakpak API key for publishing
- Git repository for your skill

## Workflow

### Step 1: Create Skill Structure

```bash
# Create a new skill with the paks CLI
paks create my-skill

# Or with optional directories
paks create my-skill --with-scripts --with-references
```

This generates:
```
my-skill/
├── SKILL.md          # Required: Manifest + instructions
├── scripts/          # Optional: Helper scripts
├── references/       # Optional: Reference documentation
└── assets/           # Optional: Static files
```

### Step 2: Write SKILL.md with Frontmatter

The `SKILL.md` file uses YAML frontmatter for metadata:

```yaml
---
name: my-skill                    # Required: 1-64 chars, lowercase + hyphens
description: |                    # Required: 1-1024 chars
  What this skill does and when to use it.
license: MIT                      # Optional: License type
tags:                             # Recommended: For discoverability
  - keyword1
  - keyword2
metadata:
  author: Your Name <email@example.com>
  version: "1.0.0"                # Semantic version (must match git tag)
---

# Skill Title

## Instructions

Your skill instructions go here...
```

**Frontmatter Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (lowercase, hyphens only) |
| `description` | Yes | What the skill does, when to use it |
| `license` | No | License type (MIT, Apache-2.0, etc.) |
| `tags` | No | Keywords for search/discovery |
| `metadata.version` | Yes | Semantic version matching git tag |
| `metadata.author` | No | Author name and email |

### Step 3: Write Skill Content

After the frontmatter, write clear instructions:

```markdown
# Skill Title

## Overview
Brief description of what this skill accomplishes.

## Prerequisites
Required tools, files, or context.

## Instructions

### Step 1: First Action
Imperative instructions with examples.

### Step 2: Next Action
Continue with clear, atomic steps.

## Troubleshooting
Common issues and solutions.

## References
- [Official Documentation](https://example.com)
```

**Best Practices:**
- Keep under 5,000 words (~800 lines)
- Use imperative language ("Analyze code for...") not second person
- Reference external files for detailed content
- Include code examples and configuration snippets

### Step 4: Validate the Skill

```bash
# Validate skill structure and frontmatter
paks validate my-skill

# Strict mode (warnings become errors)
paks validate my-skill --strict
```

### Step 5: Authenticate with Registry

```bash
# Login with API token
paks login --token <your-api-token>

# Verify login
paks login
```

### Step 6: Publish to Registry

**Important:** The git tag version must match `metadata.version` in SKILL.md.

```bash
# Dry run first (see what would be published)
paks publish my-skill --dry-run

# Publish with automatic version bump
paks publish my-skill --bump patch   # 1.0.0 → 1.0.1
paks publish my-skill --bump minor   # 1.0.0 → 1.1.0
paks publish my-skill --bump major   # 1.0.0 → 2.0.0

# Publish using existing git tag (non-interactive)
paks publish my-skill --tag v1.0.0 --yes
```

## Version Management

The paks registry uses git tags for versioning. The workflow:

1. Update `metadata.version` in SKILL.md
2. Commit changes
3. Create matching git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Publish: `paks publish my-skill --tag v1.0.0 --yes`

**Common Version Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| "Tag does not match version" | Tag and SKILL.md version mismatch | Update SKILL.md version to match tag |
| "Tag already exists" | Trying to reuse existing tag | Create new tag with bumped version |
| "No SKILL.md found at path" | Tag points to commit without SKILL.md | Create new tag after adding SKILL.md |

## Multi-Skill Repository

For repositories with multiple skills:

```
my-repo/
├── skill-one/
│   └── SKILL.md
├── skill-two/
│   └── SKILL.md
└── skill-three/
    └── SKILL.md
```

Publish each skill separately:
```bash
paks publish skill-one --tag v1.0.0 --yes
paks publish skill-two --tag v1.0.0 --yes
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `paks create <name>` | Create new skill from template |
| `paks validate <path>` | Validate skill structure |
| `paks publish <path>` | Publish to registry |
| `paks login` | Authenticate with registry |
| `paks search <query>` | Search published skills |
| `paks info <skill>` | Show skill details |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "not a terminal" error | Use `--yes` flag for non-interactive mode |
| Version mismatch | Ensure SKILL.md version matches git tag |
| Validation fails | Check frontmatter YAML syntax |
| Login fails | Verify API token is correct |
| Publish fails | Ensure you're logged in and tag exists |

## References

- [Paks CLI Documentation](https://github.com/stakpak/paks)
- [Agent Skills Specification](https://agentskills.io)
- [Paks Registry](https://paks.stakpak.dev)
