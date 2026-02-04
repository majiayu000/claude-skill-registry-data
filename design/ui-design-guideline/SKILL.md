---
name: ui-design-guideline
description: Create project-specific UI design guideline as a Claude Code Skill. Use when the user says "UI design guideline", "design system", "style guide", or wants to create design guidelines for their project.
---

# UI Design Guideline Skill Generator

This skill creates a project-specific UI design guideline as a **Claude Code Skill** and registers it to `.claude/skills/design-guideline/`.

## Output Location (Important)

Generated skill will be placed in the following structure:

```
.claude/
└── skills/
    └── design-guideline/
        ├── SKILL.md              # Main (max 500 lines)
        └── references/
            ├── colors.md         # Color system
            ├── typography.md     # Typography
            ├── spacing.md        # Spacing
            ├── components.md     # Components
            └── tokens.json       # Design tokens
```

## Execution Flow

### Phase 1: Check Existing Skill

First, check if `.claude/skills/design-guideline/` already exists:

```bash
ls -la .claude/skills/design-guideline/
```

**If exists**: Ask user using AskUserQuestion:
- "A design guideline skill already exists. Do you want to overwrite it?"
- Options: "Overwrite" / "Cancel"

If user selects "Cancel", stop execution.

### Phase 2: Information Gathering

Ask the following using AskUserQuestion tool:

1. **Project name** (required)
2. **Target platform**: Web / iOS / Android / React Native / Flutter
3. **Primary brand color** (e.g., #3B82F6)
4. **Accessibility level**: WCAG 2.1 AA / AAA
5. **Reference URL** (optional) - Analyze with WebFetch if provided

### Phase 3: Create Directory

```bash
mkdir -p .claude/skills/design-guideline/references
```

### Phase 4: Generate Files

Generate the following files in order:

#### 4.1 SKILL.md (main file)

Refer to `templates/skill-template.md` for generation.

**Important**: Keep under 500 lines. Link to references/ for details.

```yaml
---
name: design-guideline
description: UI design guideline for {PROJECT_NAME}. Use when developing UI components, styling, or making design decisions.
---
```

#### 4.2 references/colors.md

Refer to `references/color-systems.md` for generation.

- Primary color palette (50-900 scale)
- Secondary color palette
- Grayscale
- Semantic colors

#### 4.3 references/typography.md

Refer to `references/typography-scales.md` for generation.

- Font family
- Size scale (xs-6xl)
- Heading styles

#### 4.4 references/spacing.md

Refer to `references/spacing-systems.md` for generation.

- 8px base spacing
- Grid and breakpoints

#### 4.5 references/components.md

Refer to `references/component-patterns.md` for generation.

20+ component specifications (Button, Input, Card, Modal, etc.)

#### 4.6 references/tokens.json

Refer to `templates/design-tokens.json` for generation.

### Phase 5: Completion Report

After generation, report to the user:

1. List of generated files
2. How to use the skill (Claude will automatically reference it)
3. How to customize

## Reference Files

Always refer to these during generation:

- [references/color-systems.md](references/color-systems.md) - Color system best practices
- [references/typography-scales.md](references/typography-scales.md) - Typography
- [references/spacing-systems.md](references/spacing-systems.md) - Spacing
- [references/component-patterns.md](references/component-patterns.md) - Components
- [references/accessibility.md](references/accessibility.md) - Accessibility

## Template Files

- [templates/skill-template.md](templates/skill-template.md) - SKILL.md template
- [templates/design-tokens.json](templates/design-tokens.json) - Tokens template
