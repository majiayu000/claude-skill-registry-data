---
name: skill-architect
description: >
  Expert guide for creating OpenCode skills. Use when: (1) Creating new 
  skills with scripts and resources, (2) Learning skill design patterns,
  (3) Validating existing skills, (4) Choosing the right skill archetype.
---

# Skill Architect

Create high-quality OpenCode skills.

## Quick Start

| Goal | Action |
|------|--------|
| Create a new skill | `npx tsx scripts/init.ts <name>` |
| Validate existing skill | `npx tsx scripts/validate.ts <path>` |
| Deep analysis | Use `@skill-analyzer` subagent |

## What is a Skill?

Skills are domain knowledge packages with optional scripts and resources:

```
my-skill/
├── SKILL.md          # Instructions (always loaded)
├── scripts/          # Executable code
├── references/       # Documentation (loaded on demand)
└── assets/           # Templates, images, files
```

**Location:** `.opencode/skills/<name>/`

**Use a skill when you need:**
- Executable scripts for external APIs or complex operations
- Reference documentation for domain knowledge
- Templates or assets for output generation
- Multi-step workflows with decision trees

---

## Context Efficiency

Skills load into the main context window. To keep context lean:

1. **Keep SKILL.md under 500 lines** - Move details to `references/`
2. **Use subagents for heavy analysis** - They run in isolated context
3. **Progressive disclosure** - Load references only when needed
4. **Scripts execute, not read** - Zero token cost

### When to Use Subagents

| Operation | Main Context | Subagent |
|-----------|--------------|----------|
| Quick validation | ✓ | |
| Deep file analysis | | ✓ |
| Multi-file comparison | | ✓ |
| Pattern matching | | ✓ |
| Simple scaffolding | ✓ | |

For comprehensive skill analysis, delegate to the `@skill-analyzer` subagent.

---

## Creating a Skill

### Phase 1: Discovery

Understand what the skill needs to do:

1. List 3-5 concrete use cases
2. Identify what Claude doesn't already know (proprietary formats, APIs, sequences)
3. Determine if scripts are needed (repetitive operations, external APIs)

### Phase 2: Choose Archetype

Select the pattern that fits your use case (see `references/archetypes.md`):

| Type | When to Use | Example |
|------|-------------|---------|
| **Workflow** | Multi-step processes with clear sequence | deploy-buddy |
| **Tool Collection** | Related operations, no fixed order | atlassian |
| **Guidelines** | Standards, policies, brand rules | brand-voice |
| **Integration** | External API/service integration | stripe-sync |

### Phase 3: Scaffold

```bash
npx tsx scripts/init.ts <name>
```

Creates the directory structure with a template SKILL.md.

### Phase 4: Implement

Write your SKILL.md following these guidelines:

1. **Keep it under 500 lines** - Move details to references
2. **Start with a decision tree** - Help Claude pick the right workflow
3. **Show, don't tell** - Concrete examples beat abstract descriptions
4. **Include error recovery** - What to do when things fail

### Phase 5: Validate

```bash
npx tsx scripts/validate.ts .opencode/skills/<name>
```

Fix any errors and address warnings.

### Phase 6: Iterate

Test with real queries. Refine based on what you observe.

---

## Writing Effective Instructions

Four core principles (details in `references/patterns.md`):

### 1. Claude is Already Smart

Don't explain obvious things. Focus on what Claude doesn't know:
- Proprietary formats and schemas
- Business-specific logic
- Required sequences and dependencies

### 2. Match Specificity to Fragility

| Operation Type | Instruction Style |
|----------------|-------------------|
| Flexible | Prose guidelines |
| Preferred pattern | Pseudocode, parameters |
| Fragile (must be exact) | Exact scripts, strict templates |

### 3. Show, Don't Tell

- Concrete examples > abstract descriptions
- Input/output pairs for format expectations
- Real error messages with solutions

### 4. Progressive Disclosure

- SKILL.md = entry point (always loaded)
- `references/` = details (on demand)
- `scripts/` = execute without reading

---

## Skill Structure

### SKILL.md

The main entry point. Must have YAML frontmatter:

```yaml
---
name: my-skill
description: >
  [What it does]. Use when: (1) [Trigger 1], (2) [Trigger 2], (3) [Trigger 3].
---
```

**Required fields:**

| Field | Requirements |
|-------|--------------|
| `name` | Kebab-case, matches directory name, max 64 chars, no consecutive hyphens |
| `description` | 20-1024 chars, no angle brackets (`<` or `>`), include numbered triggers |

**Optional fields:**

```yaml
---
name: my-skill
description: >
  [What it does]. Use when: (1) [Trigger 1], (2) [Trigger 2].
license: MIT                      # License identifier
allowed-tools:                    # Restrict which tools the skill can use
  - read
  - write
  - bash
metadata:                         # Custom metadata
  version: "1.0"
  author: "Team Name"
---
```

| Field | Purpose |
|-------|---------|
| `license` | License identifier (e.g., "MIT", "Apache-2.0") |
| `allowed-tools` | List of tools the skill is permitted to use |
| `metadata` | Custom key-value pairs (version, author, etc.) |

### scripts/

Executable code. Prefer TypeScript (`npx tsx`).

### references/

Documentation loaded on demand. Use for content over 100 lines.

### assets/

Files used in output (templates, images). Not loaded into context.

---

## Scripts Reference

### init.ts

```bash
npx tsx scripts/init.ts my-tool
```

Creates `.opencode/skills/my-tool/` with template files.

### validate.ts

```bash
npx tsx scripts/validate.ts .opencode/skills/my-tool
```

**Errors** (must fix): Missing SKILL.md, invalid frontmatter, bad name/description

**Warnings** (should fix): Over 500 lines, missing references, weak description

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Explaining the obvious | Delete it - Claude knows |
| Vague instructions | Be specific: "If X, do Y" |
| Missing decision tree | Add workflow routing at top |
| Weak description | Add numbered trigger scenarios |
| Wall of text | Move to references |

---

## Subagent: skill-analyzer

For deep analysis without bloating main context, use:

```
@skill-analyzer Analyze the skill at .opencode/skills/my-tool
```

The subagent runs in its own context and returns a concise summary.

---

## Examples

See `references/examples/` for annotated skills:
- **deploy-buddy.md** - Workflow skill
- **stripe-sync.md** - Integration skill
