---
name: skill-creator
description: Create new skills for the POS following Anthropic's established patterns. Use when users want to create a new skill, update an existing skill, or ask "how do I create a skill". Triggers on phrases like "create skill", "new skill", "build skill", or "skill for X".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Skill Creator

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Create effective skills that extend Claude's capabilities for the POS workflow.

## Core Principles

### Context is Precious
The context window is shared with system prompts, conversation history, and user requests. Only include information Claude doesn't already have. Challenge each piece: "Does this justify its token cost?"

### Graduated Information Loading
1. **Metadata** (~100 words) - Always in context (name + description)
2. **SKILL.md body** (<500 lines) - Loaded when skill triggers
3. **Bundled resources** (unlimited) - Loaded as needed

### Appropriate Constraints
- **High freedom**: Multiple valid approaches, use text guidance
- **Medium freedom**: Preferred patterns exist, use pseudocode
- **Low freedom**: Fragile operations, use specific scripts

## Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, allowed-tools)
│   └── Markdown instructions (<500 lines)
└── Bundled Resources (optional)
    ├── scripts/      - Executable code for deterministic tasks
    ├── references/   - Documentation loaded contextually
    └── assets/       - Output resources (templates, images)
```

## Creation Process

### Step 1: Understand the Skill
Ask clarifying questions:
- "What functionality should this skill support?"
- "Give examples of how this skill would be used"
- "What should trigger this skill?"

### Step 2: Plan Resources
For each use case, identify:
- Scripts for repetitive code
- References for documentation
- Assets for templates/output

### Step 3: Initialize Structure
Create the skill directory:
```bash
mkdir -p .claude/skills/{skill-name}/{scripts,references,assets}
```

### Step 4: Write SKILL.md

#### Frontmatter (CRITICAL)
```yaml
---
name: skill-name
description: What it does AND when to use it. Include trigger phrases.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---
```

The description is the PRIMARY triggering mechanism. Include:
- What the skill does
- Specific triggers/contexts
- Example phrases that should activate it

#### Body Guidelines
- Use imperative form ("Create...", "Run...", not "This skill creates...")
- Keep under 500 lines
- Split large content into references/
- Include examples over verbose explanations
- Reference bundled resources with clear "when to read" guidance

### Step 5: Add Resources

**Scripts** - For deterministic, repeated code:
```
scripts/validate.py     # Data validation
scripts/generate.sh     # Code generation
```

**References** - For contextual documentation:
```
references/patterns.md  # Design patterns
references/schemas.md   # Data schemas
```

**Assets** - For output generation:
```
assets/template.md      # Document template
assets/boilerplate/     # Starter code
```

### Step 6: Validate

Check:
- [ ] SKILL.md has valid YAML frontmatter
- [ ] Description includes triggers AND purpose
- [ ] Body is under 500 lines
- [ ] References are linked from SKILL.md
- [ ] No unnecessary files (no README, CHANGELOG, etc.)

## Anti-Patterns

❌ **Don't include:**
- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- Information Claude already knows
- "When to Use This Skill" in body (put in description!)
- Deeply nested reference files

✅ **Do include:**
- Clear trigger phrases in description
- Concise examples over explanations
- References for variant-specific details
- Scripts for repeated operations

## Progressive Disclosure Patterns

### Pattern 1: High-level with references
```markdown
## Quick start
[basic example]

## Advanced
- **Feature A**: See [FEATURE-A.md](references/feature-a.md)
- **Feature B**: See [FEATURE-B.md](references/feature-b.md)
```

### Pattern 2: Domain organization
```
skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```

### Pattern 3: Framework variants
```
skill/
├── SKILL.md (workflow + selection)
└── references/
    ├── laravel.md
    ├── nuxt.md
    └── flutter.md
```

## CTO Workflow Integration

Skills in this system should:
1. Follow tiered context loading principles
2. Use orchestrator pattern for file operations
3. Reference existing SOPs when applicable
4. Integrate with team/project structure

## Output

After creating a skill, report:
- Skill path: `.claude/skills/{skill-name}/`
- Files created
- How to trigger the skill
- Suggested test scenarios

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
