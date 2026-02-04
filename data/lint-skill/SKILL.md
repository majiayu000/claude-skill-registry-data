---
name: lint-skill
description: |
  Validate skill documents against PMC skill design principles.
  Checks format ownership, composite skill structure, and internal consistency.

  CHECKS:
  1. FORMAT OWNERSHIP - kb skill owns all format templates (kb/references/)
  2. COMPOSITE STRUCTURE - Steps must have associated skills, stage announcements
  3. INTERNAL CONSISTENCY - No gaps, broken references, or missing sections

  Use when:
  - Creating new skills
  - Reviewing existing skills
  - Periodic skill maintenance
  - User says "lint skills", "check skills", "validate skills"
---

# Lint Skill Documents

Validate skill documents against PMC skill design principles.

## Prerequisites

**ALWAYS run /pmc:kb first** to understand KB structure and skill organization.

## Default Scope

By default, lint-skill checks all skills in the **same directory** as itself:

```
.pmc/marketplace/plugins/pmc/skills/
├── lint-skill/    <- this skill
├── dev/           <- checked
├── kb/            <- checked
├── plan/          <- checked
└── ...            <- all siblings checked
```

**Override scope:**
- `/pmc:lint-skill skill-name` - Check single skill
- `/pmc:lint-skill path/to/skills/` - Check different directory

---

## Skill Design Principles

### Principle 1: Format Ownership

**KB skill owns all format templates.**

- All format templates live in `kb/references/*.md`
- Other skills reference formats, never define them
- Directory structure defined in `kb/references/directory-structure.md`

**Check:**
- Skill defines document formats? → ERROR (move to kb/references/)
- Skill duplicates format info from kb? → WARNING (reference instead)

### Principle 2: Composite Skill Structure

**Composite skills (orchestrators) follow strict patterns.**

A composite skill:
- Coordinates multiple other skills in sequence
- Each step has explicit skill association
- Declares stage transitions during execution

**Required Elements:**

1. **Frontmatter WORKFLOW** - Lists all steps with associated skills:
   ```yaml
   WORKFLOW:
   1. STEP_NAME - /pmc:skill-name (brief description)
   2. STEP_NAME - /pmc:skill-a + /pmc:skill-b
   ```

2. **Stage Announcements** - Documents how to announce transitions:
   ```
   === ENTERING STEP_NAME ===
   [... work ...]
   ```

3. **Step-Skill Mapping** - Every step must have at least one skill:
   ```markdown
   ## Step N: STEP_NAME

   **Skill:** `/pmc:skill-name`
   ```
   Or for multiple skills:
   ```markdown
   **Skills:**
   - `/pmc:skill-a` → purpose
   - `/pmc:skill-b` → purpose
   ```

4. **Skill Reference Table** - Summary of all step-skill mappings:
   ```markdown
   | Step | Skill | Purpose |
   |------|-------|---------|
   | 1. STEP | `/pmc:skill` | What it does |
   ```

**Check:**
- Step without associated skill? → ERROR (create or assign skill)
- Missing stage announcement pattern? → ERROR
- Missing skill reference table? → WARNING

### Principle 3: Internal Consistency

**Skills must be internally consistent and complete.**

**Checks:**

| Check | Type | Description |
|-------|------|-------------|
| Broken skill references | ERROR | `/pmc:nonexistent` referenced |
| Broken file references | ERROR | Links to non-existent files |
| Missing Prerequisites section | WARNING | Should reference /pmc:kb |
| Undefined placeholders | ERROR | `{placeholder}` or `TBD` in content |
| Inconsistent naming | WARNING | Skill name in frontmatter vs filename |
| Missing "Use when" section | WARNING | Frontmatter should have triggers |
| Empty sections | WARNING | Headers with no content |

---

## Validation Procedure

### Step 1: Identify Skills to Check

**Default:** All sibling skills in same directory as lint-skill.

```bash
# Default scope (sibling skills)
ls .pmc/marketplace/plugins/pmc/skills/*/SKILL.md

# Single skill
ls .pmc/marketplace/plugins/pmc/skills/{skill-name}/SKILL.md

# Recently modified only
git diff --name-only HEAD~5 -- .pmc/marketplace/plugins/pmc/skills/
```

### Step 2: Classify Each Skill

| Type | Characteristics | Example |
|------|-----------------|---------|
| **Atomic** | Single responsibility, no skill delegation | kb, reflect, complete |
| **Composite** | Orchestrates other skills, has steps | dev, workflow |
| **Validation** | Checks/verifies artifacts | lint-kb, plan-validation, ticket-status |
| **Reference** | Manages templates/formats | kb (format ownership) |

### Step 3: Run Checks Per Type

#### For All Skills

```markdown
## Basic Checks

- [ ] Frontmatter has `name` and `description`
- [ ] Description has `Use when:` triggers
- [ ] Has Prerequisites section referencing /pmc:kb
- [ ] No TBD/TODO/placeholder markers
- [ ] All `/pmc:skill` references exist
- [ ] All file path references exist
- [ ] Skill name matches directory name
```

#### For Composite Skills (Additional)

```markdown
## Composite Skill Checks

- [ ] WORKFLOW in frontmatter lists all steps
- [ ] Each step has associated skill(s)
- [ ] Stage announcement pattern documented
- [ ] Skill Reference Table exists
- [ ] All referenced skills exist
- [ ] No orphan steps (step without skill)
- [ ] No orphan skills (skill without step)
```

#### For Format/Reference Skills

```markdown
## Format Ownership Checks

- [ ] Format templates in kb/references/ only
- [ ] Other skills reference, not duplicate
- [ ] Directory structure in directory-structure.md
- [ ] No format definitions outside kb/references/
```

### Step 4: Report Issues

```markdown
# Skill Lint Report

## Summary

| Skill | Type | Errors | Warnings |
|-------|------|--------|----------|
| dev | composite | 0 | 1 |
| plan | atomic | 1 | 0 |

## Issues

### plan (ERRORS: 1)

| Severity | Check | Issue |
|----------|-------|-------|
| ERROR | broken-reference | `/pmc:nonexistent` not found (line 45) |

### dev (WARNINGS: 1)

| Severity | Check | Issue |
|----------|-------|-------|
| WARNING | empty-section | "## Advanced Usage" has no content |
```

---

## Fixing Common Issues

### Missing Skill for Step

If a composite skill step has no associated skill:

1. **Option A**: Create new skill
   ```bash
   mkdir .pmc/marketplace/plugins/pmc/skills/{new-skill}
   # Create SKILL.md with atomic skill template
   ```

2. **Option B**: Assign existing skill
   - Find skill that covers this functionality
   - Update step to reference it

3. **Option C**: Merge into adjacent step
   - If step is trivial, combine with related step

### Format Definition Outside kb

If skill defines formats that should be in kb/references/:

1. Extract format to `kb/references/{format}-format.md`
2. Replace inline definition with reference:
   ```markdown
   **Format:** See [kb/references/{format}-format.md](../kb/references/{format}-format.md)
   ```

### Broken Skill Reference

If `/pmc:skill` doesn't exist:

1. Check for typo in skill name
2. Check if skill was renamed/removed
3. Create missing skill if needed
4. Update reference to correct skill

---

## Skill Templates

### Atomic Skill Template

```markdown
---
name: {skill-name}
description: |
  {One-line summary of what this skill does.}

  {2-3 lines of detail about the skill's purpose.}

  Use when:
  - {trigger condition 1}
  - {trigger condition 2}
---

# {Skill Title}

{Brief description.}

## Prerequisites

**ALWAYS run /pmc:kb first** to understand KB structure.

## When to Use

**Use when:**
- {condition}

**Skip when:**
- {condition}

---

## Procedure

### Step 1: {Name}

{Instructions}

### Step 2: {Name}

{Instructions}

---

## Checklist

- [ ] {Item 1}
- [ ] {Item 2}
```

### Composite Skill Template

```markdown
---
name: {skill-name}
description: |
  {One-line summary - orchestrates X workflow.}
  Coordinates skills in sequence: a → b → c.

  WORKFLOW:
  1. STEP_A - /pmc:skill-a (description)
  2. STEP_B - /pmc:skill-b + /pmc:skill-c
  3. STEP_C - /pmc:skill-d (description)

  Use when:
  - {trigger condition 1}
  - {trigger condition 2}
---

# {Workflow Title}

{Brief description of the workflow.}

## Prerequisites

**ALWAYS run /pmc:kb first** to understand KB structure.

## State Announcements

**ALWAYS announce stage transitions:**

```
=== ENTERING STEP_A ===
[... work ...]

=== ENTERING STEP_B ===
[... work ...]
```

## Workflow Overview

```
{ASCII diagram showing flow}
```

---

## Step 1: STEP_A

**Skill:** `/pmc:skill-a`

{What this step does and when to proceed.}

---

## Step 2: STEP_B

**Skills:**
- `/pmc:skill-b` → {purpose}
- `/pmc:skill-c` → {purpose}

{Instructions for this step.}

---

## Skill Reference

| Step | Skill | Purpose |
|------|-------|---------|
| 1. STEP_A | `/pmc:skill-a` | {purpose} |
| 2. STEP_B | `/pmc:skill-b` | {purpose} |
| 2. STEP_B | `/pmc:skill-c` | {purpose} |
| 3. STEP_C | `/pmc:skill-d` | {purpose} |
```

---

## Checklist

### Basic Validation
- [ ] All skills have frontmatter with name/description
- [ ] All skills have "Use when" triggers
- [ ] All skills reference /pmc:kb in prerequisites
- [ ] No TBD/TODO markers
- [ ] All skill references valid
- [ ] All file references valid

### Composite Skills
- [ ] WORKFLOW in frontmatter
- [ ] Every step has skill(s)
- [ ] Stage announcements documented
- [ ] Skill Reference Table exists
- [ ] No orphan steps or skills

### Format Ownership
- [ ] All formats in kb/references/
- [ ] No format duplication across skills
- [ ] Other skills reference kb formats

---

## Example Report

```
=== LINT SKILL REPORT ===

Checked: 15 skills
Errors: 2
Warnings: 4

## ERRORS

### plan/SKILL.md
- LINE 156: Broken reference `/pmc:nonexistent` - skill does not exist

### workflow/SKILL.md
- LINE 45: Step "3. EXECUTE" has no associated skill

## WARNINGS

### dev/SKILL.md
- Missing Skill Reference Table (composite skill should have one)

### test/SKILL.md
- Empty section "## Advanced Usage"

### reflect/SKILL.md
- No "Use when" in frontmatter description

### validate/SKILL.md
- Placeholder found: "{TBD}" at line 89

=== END REPORT ===
```
