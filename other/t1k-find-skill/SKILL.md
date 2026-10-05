---
name: t1k:find-skill
description: "Discover available skills by keyword search across all activation fragments and installed modules. Use when asking 'what skill handles X', 'how do I do Y', 'find skill for Z', or 'list all skills'."
keywords: [discover, find, search, list, available, skills, lookup]
version: 1.0.0
argument-hint: "<query> [--all] [--installed-only]"
effort: low
origin: theonekit-core
repository: The1Studio/theonekit-core
module: null
protected: true
---

# TheOneKit Find-Skill — Skill Discovery

Search available skills by keyword when you need to know what capability exists. Critical as module count grows across kits.

## Usage

```
/t1k:find-skill "ECS batch processing"   # Find skills matching a query
/t1k:find-skill "auth"                   # All skills related to auth
/t1k:find-skill --all                    # List every available skill
/t1k:find-skill --all --installed-only   # Only installed skills
```

## Algorithm

1. **Load activation sources:**
   - Read ALL `.claude/t1k-activation-*.json` fragments → collect keyword-to-skill mappings
   - Read ALL installed `module.json` files → collect `activation.keywords` per module
   - Read ALL `SKILL.md` frontmatter (`description` field) for richer matching

2. **Fuzzy-match query:**
   - Tokenize user query into words
   - Match against: activation keywords, skill names, SKILL.md descriptions
   - Rank results:
     1. Exact keyword match (highest)
     2. Prefix match (query is prefix of keyword)
     3. Substring match (query appears inside keyword)
     4. Description match (query word appears in SKILL.md description)

3. **Resolve install status:**
   - Read `.claude/metadata.json` → `installedModules`
   - Mark each result: `[installed]` or `[not installed — module: {name}]`

4. **Output results** with install status, module, and description.

## Output Format

```
## Skills matching "ECS batch"

### Installed

| Skill | Module | Description |
|-------|--------|-------------|
| dots-ecs-core | dots-core (theonekit-unity) | ECS system patterns, burst compilation, job scheduling |
| dots-ecs-batch | dots-core (theonekit-unity) | Batch entity processing with IJobChunk and EntityQuery |

### Available (not installed)

| Skill | Module | Kit | Install Command |
|-------|--------|-----|-----------------|
| dots-ecs-advanced | dots-advanced | theonekit-unity | /t1k:modules add dots-advanced |

### No match in uninstalled modules.
```

## --all Flag

Lists every available skill (no filtering). Output grouped by module:

```
## All Available Skills

### Core (always available)
- t1k:cook — End-to-end feature implementation
- t1k:fix — Bug fix workflow
- t1k:plan — Planning and architecture
- ...

### Module: dots-core (theonekit-unity) [installed v2.1.0]
- dots-ecs-core — ECS system patterns
- dots-physics — Physics simulation patterns
- ...

### Module: ui (theonekit-unity) [installed v1.3.0]
- unity-ui — UI toolkit patterns
- ...

### Module: rendering (theonekit-unity) [NOT INSTALLED]
  Install: /t1k:modules add rendering
- unity-rendering — SRP render pipeline patterns
- ...
```

## Uninstalled Module Suggestion

When results include uninstalled modules, offer installation:

```
2 results found in uninstalled module 'dots-advanced'.
Install it? Run: /t1k:modules add dots-advanced
```

Do NOT auto-install — always ask the user first.

## Category Browsing

When no query provided (or `--all`), group skills by category (from `module.json` → `category`):

```
/t1k:find-skill --all --category "Testing & QA"
```

Available categories: Core Workflows, Planning & Analysis, Backend, Frontend & Design, Game Engine, Testing & QA, DevOps & CI/CD, Security, Documentation, Git & VCS, Kit Management, Utilities

## Gotchas

- **Core skills are always available** — they live in `.claude/skills/` regardless of metadata
- **Fragment-only kits**: Some older kits may not have `module.json` — fall back to `t1k-activation-*.json` only
- **Description quality varies**: SKILL.md descriptions may be short; keyword matching is more reliable
- **Cross-kit skills**: A skill installed from `theonekit-designer` appears in results even in a Unity project

## Auto-Activation Keywords

Triggers on: `find skill`, `search skill`, `what skill`, `available skills`, `discover`, `how do I`, `which skill`, `skill for`, `list skills`, `skill search`
