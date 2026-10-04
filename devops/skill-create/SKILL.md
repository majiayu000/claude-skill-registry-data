---
name: skill-create
description: Create and validate Claude Code skills with proper structure, checklists, and validation scripts. Use when creating a new skill, auditing existing skills, or ensuring skills meet quality standards. Generates complete skill scaffolds with SKILL.md, check scripts, guides, and templates.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Skill Creation & Validation

Create complete, well-structured Claude Code skills. Generates scaffolds, validates skill completeness, and ensures quality standards.

## When to Use This Skill

- Creating a new skill from scratch
- Auditing existing skills for completeness
- Validating a skill before deployment
- Understanding skill best practices
- User asks "create skill", "new skill", or "validate skill"

## Questions to Ask

1. **Skill category:** Code-heavy, Auth, Config, Knowledge, or Orchestration?
2. **Core purpose:** What problem does this skill solve? (1-2 sentences)
3. **Trigger words:** What keywords should invoke this skill?
4. **Reference code:** Will it include Dart templates, or just guides?
5. **Validation needs:** What should the check script verify?

## Quick Reference

### Skill Categories

| Category | Examples | Focus |
|----------|----------|-------|
| **Code-Heavy** | domain, data, presentation | Generate detailed code from specs |
| **Auth** | auth, phone-auth, social-login | Authentication with platform setup |
| **Config** | release, ci-cd, analytics | Platform configs and workflows |
| **Knowledge** | design, i18n, testing, a11y | Guidelines and patterns |
| **Orchestration** | plan, init, feature-init | Coordinate other skills |

### Directory Structure

```
.claude/skills/{skill-name}/
├── SKILL.md              # Main entry (<300 lines)
├── {topic}-guide.md      # Detailed guides (reference/ for code)
├── templates/            # Platform configs (XML, YAML)
└── scripts/check.dart    # Validation script
```

### SKILL.md Requirements

| Section | Required | Purpose |
|---------|----------|---------|
| YAML frontmatter | YES | name, description, allowed-tools |
| When to Use | YES | Clear trigger scenarios |
| Workflow | YES | Numbered implementation steps |
| Guides table | YES | Links to detailed content |
| Checklist | YES | Verification items |
| Related Skills | YES | Cross-references |
| Quick Reference | Recommended | Decision tables, key patterns |

## Workflow

### Phase 1: Define Skill

1. Determine skill category and core purpose
2. Identify trigger words for description
3. List what the skill should NOT handle (delegate to other skills)
4. Define expected outputs (files, code, configs)

### Phase 2: Create Structure

```bash
# Create skill directory
mkdir -p .claude/skills/{skill-name}/{scripts,templates,reference}

# Validate structure
dart run .claude/skills/skill-create/scripts/validate.dart --skill {skill-name}
```

### Phase 3: Write SKILL.md

Use template from `templates/SKILL.md.template`:

1. Write frontmatter (name, description, allowed-tools)
2. Add "When to Use" section with clear scenarios
3. Define workflow with numbered steps
4. Add guides table linking to detailed content
5. Include checklist for verification
6. Add "Related Skills" section

### Phase 4: Create Supporting Files

Based on category:

**Code-Heavy Skills:**
- `reference/` - Full Dart implementations
- `scripts/check.dart` - Validates generated code

**Config Skills:**
- `templates/` - Platform config files (XML, YAML, properties)
- `{topic}-guide.md` - Setup instructions
- `scripts/check.dart` - Validates config presence

**Knowledge Skills:**
- `{topic}-guide.md` - Best practices and patterns
- `examples.md` - Code examples
- `scripts/check.dart` - Audits code for issues

### Phase 5: Validate

```bash
# Run full validation
dart run .claude/skills/skill-create/scripts/validate.dart --skill {skill-name}

# Check specific aspects
dart run .claude/skills/skill-create/scripts/validate.dart --skill {skill-name} --check frontmatter
dart run .claude/skills/skill-create/scripts/validate.dart --skill {skill-name} --check structure
dart run .claude/skills/skill-create/scripts/validate.dart --skill {skill-name} --check references
```

### Phase 6: Register

Update `SKILL_STRUCTURE.md`:
1. Add to "Complete Skill Reference" table
2. Add to skill flow diagrams
3. Add to delegation rules if needed

## Commands

```bash
dart run .claude/skills/skill-create/scripts/validate.dart --skill {name}  # Validate
dart run .claude/skills/skill-create/scripts/validate.dart --all           # Validate all
dart run .claude/skills/skill-create/scripts/validate.dart --list-checks   # List checks
dart run .claude/skills/skill-create/scripts/validate.dart --skill {name} --report  # Detailed
```

## Quality Gates

A skill must pass these gates before deployment:

### Gate 1: Structure (Required)

- [ ] SKILL.md exists
- [ ] SKILL.md < 300 lines
- [ ] Valid YAML frontmatter
- [ ] Required sections present

### Gate 2: Content (Required)

- [ ] Description < 1024 chars
- [ ] Description in third person
- [ ] Workflow has numbered steps
- [ ] Checklist has > 3 items
- [ ] All internal links resolve

### Gate 3: Quality (Recommended)

- [ ] No code blocks > 10 lines in SKILL.md
- [ ] Reference files have header comments
- [ ] Check script exists and runs
- [ ] Related Skills section accurate

### Gate 4: Integration (Recommended)

- [ ] Registered in SKILL_STRUCTURE.md
- [ ] Cross-references to/from other skills accurate
- [ ] No duplicate functionality with existing skills

**See:** [quality-gates.md](quality-gates.md) for detailed criteria.

## Guides

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Comprehensive skill creation checklist |
| [quality-gates.md](quality-gates.md) | Detailed quality criteria |
| [examples.md](examples.md) | Well-structured skill examples |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/SKILL.md.template` | Starting point for SKILL.md |
| `templates/check.dart.template` | Validation script scaffold |
| `templates/guide.md.template` | Guide file structure |

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Long SKILL.md | 500+ lines with code | < 200 lines, move code to `reference/` |
| Vague description | "Helps with data stuff" | Specific: "Generate DTOs, repositories..." |
| Missing delegation | Inline i18n, testing, a11y | Use "Run /i18n" in Next Steps |
| No validation | No way to verify | Add `scripts/check.dart` |

**See:** [examples.md](examples.md) for well-structured skill examples.

## Checklist

**Structure:**
- [ ] Directory follows standard structure
- [ ] SKILL.md exists with valid frontmatter
- [ ] SKILL.md < 300 lines (ideally < 200)
- [ ] All internal links resolve

**Content:**
- [ ] "When to Use" section with clear scenarios
- [ ] Workflow with numbered steps
- [ ] Guides table with linked files
- [ ] Checklist with verification items
- [ ] Related Skills section

**Quality:**
- [ ] Description in third person
- [ ] Description includes trigger words
- [ ] No code blocks > 10 lines in SKILL.md
- [ ] Reference files have header comments
- [ ] Check script validates key requirements

**Integration:**
- [ ] Added to SKILL_STRUCTURE.md skill table
- [ ] Added to skill flow diagrams
- [ ] Cross-references accurate
- [ ] Delegation rules documented

## Related Skills

- All skills - This skill helps create and validate them
- SKILL_STRUCTURE.md - Central documentation this skill supports

## Next Steps

After creating a skill:
1. Run `validate.dart --skill {name}` to check quality gates
2. Update SKILL_STRUCTURE.md to register the skill
3. Test the skill with representative tasks
4. Verify Claude finds reference files correctly
