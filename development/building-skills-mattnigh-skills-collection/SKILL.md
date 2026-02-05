---
name: building-skills
description: Creating new Claude Code skills for StickerNest. Use when the user asks to create a skill, build a skill, add a new skill, make a Claude skill, or extend Claude's capabilities for this project. Covers skill structure, YAML frontmatter, trigger-focused descriptions, and StickerNest-specific skill patterns.
---

# Building Claude Code Skills for StickerNest

This meta-skill guides you through creating new Claude Code skills that are specific to StickerNest development patterns.

## What Makes a Good Skill

Skills are **model-invoked** - Claude automatically uses them when relevant. This means:

1. **Discovery is critical** - The description determines when Claude uses the skill
2. **Content must be actionable** - Claude needs clear instructions to follow
3. **Context is king** - Reference actual files, patterns, and conventions from StickerNest

---

## Interactive Skill Creation Process

### Step 1: Gather Requirements

Ask the user:

```
1. What task or workflow should this skill handle?
   Example: "Managing canvas history and undo/redo"

2. When should Claude use this skill? (Be specific about trigger phrases)
   Example: "When user asks to add undo, implement history, track changes"

3. What existing code/patterns should this skill reference?
   Example: "src/canvas/history/CommandStack.ts"

4. Should this be project-specific (.claude/skills/) or personal (~/.claude/skills/)?
```

### Step 2: Design the Skill

**Naming Convention**: Use gerund form (verb + -ing)
- `managing-canvas-history` (not `canvas-history-manager`)
- `generating-ai-widgets` (not `ai-widget-generator`)
- `debugging-pipelines` (not `pipeline-debugger`)

**Description Formula**:
```
[What it does]. Use when [trigger phrases]. Covers [key topics].
```

Example:
```
Managing canvas history and undo/redo operations. Use when the user asks
to add undo functionality, implement history tracking, revert changes,
or manage canvas state over time. Covers CommandStack, HistoryEntry types,
and integration with useCanvasStore.
```

### Step 3: Structure the Content

```markdown
---
name: {gerund-name}
description: {trigger-focused description under 1024 chars}
---

# {Title}

Brief overview of what this skill enables.

## Core Concepts
Key terminology and mental models.

## Step-by-Step Guide
Actionable instructions with code examples.

## Common Patterns
Reusable patterns from StickerNest codebase.

## Reference Files
Links to relevant source files.

## Troubleshooting
Common issues and solutions.
```

### Step 4: Validate

Checklist:
- [ ] Name is gerund form, lowercase, hyphens only (max 64 chars)
- [ ] Description includes trigger phrases AND topics covered
- [ ] Description is under 1024 characters
- [ ] YAML frontmatter is properly formatted
- [ ] Instructions reference actual StickerNest files/patterns
- [ ] Code examples are complete and runnable
- [ ] File is under 500 lines (split if larger)

---

## StickerNest Skill Categories

When creating skills, consider these domains:

| Domain | Example Skills |
|--------|---------------|
| **Widgets** | creating-widgets, connecting-widget-pipelines, testing-widgets |
| **UI/UX** | creating-components, styling-with-tokens, building-panels |
| **State** | creating-zustand-stores, managing-canvas-state |
| **Runtime** | debugging-pipelines, managing-widget-lifecycle |
| **Testing** | testing-widgets, writing-e2e-tests |
| **AI** | generating-ai-widgets, configuring-ai-providers |
| **Canvas** | managing-canvas-history, handling-canvas-gestures |

---

## Skill Template Generator

To create a new skill, use this template:

```bash
# Create skill directory
mkdir -p .claude/skills/{skill-name}

# Create SKILL.md
cat > .claude/skills/{skill-name}/SKILL.md << 'TEMPLATE'
---
name: {skill-name}
description: {Brief what + when triggers + topics covered}
---

# {Skill Title}

{One paragraph overview}

## When to Use This Skill

This skill helps when you need to:
- {Use case 1}
- {Use case 2}
- {Use case 3}

## Core Concepts

### {Concept 1}
{Explanation}

### {Concept 2}
{Explanation}

## Step-by-Step Guide

### Step 1: {First Step}
{Instructions with code}

### Step 2: {Second Step}
{Instructions with code}

## Code Examples

### Example: {Example Name}
```typescript
// Complete, runnable example
```

## Common Patterns

### Pattern: {Pattern Name}
{Description and code}

## Reference Files

- **{Category}**: `{file-path}`
- **{Category}**: `{file-path}`

## Troubleshooting

### Issue: {Problem}
**Cause**: {Why it happens}
**Fix**: {How to resolve}
TEMPLATE
```

---

## Advanced: Supporting Files

For complex skills, add supporting files:

```
.claude/skills/my-skill/
├── SKILL.md              # Main instructions (required)
├── examples.md           # Extended examples
├── reference.md          # Detailed reference docs
├── templates/
│   └── template.ts       # Code templates
└── scripts/
    └── helper.js         # Utility scripts
```

Reference them in SKILL.md:
```markdown
See [examples.md](./examples.md) for more examples.
```

---

## Analyzing Existing Code for Skills

When creating a skill about existing functionality:

1. **Find the relevant files**:
   ```bash
   # Search for related code
   grep -r "keyword" src/ --include="*.ts"
   ```

2. **Identify patterns**:
   - What interfaces/types are used?
   - What's the file structure convention?
   - How do similar features work?

3. **Extract examples**:
   - Find 2-3 representative examples from codebase
   - Simplify for the skill (remove noise)
   - Annotate with explanations

4. **Document the "why"**:
   - Why does this pattern exist?
   - What problems does it solve?
   - What are the alternatives?

---

## Testing Your Skill

After creating a skill:

1. **Test discovery**: Ask Claude something that should trigger it
   ```
   "How do I {task the skill covers}?"
   ```

2. **Test instructions**: Follow the skill's guidance yourself
   - Are the steps clear?
   - Do code examples work?
   - Are file paths correct?

3. **Test edge cases**: Try variations
   ```
   "I want to {slightly different phrasing}"
   ```

---

## Example: Creating a New Skill

Let's say we want to create a skill for managing canvas history:

### 1. Requirements
- **Task**: Managing undo/redo and canvas history
- **Triggers**: "add undo", "implement history", "revert changes", "track state"
- **References**: `src/canvas/history/`, `useCanvasStore`

### 2. Name & Description
```yaml
name: managing-canvas-history
description: Managing canvas history and undo/redo operations. Use when the user asks to add undo functionality, implement history tracking, revert changes, or manage canvas state over time. Covers CommandStack, HistoryEntry, and useCanvasStore integration.
```

### 3. Content Outline
- Core concepts: Command pattern, history stack
- Guide: Adding undoable actions
- Patterns: Command implementation, state snapshots
- Reference: Actual file paths

### 4. Validate
- [x] Gerund name: `managing-canvas-history`
- [x] Trigger phrases in description
- [x] Under 1024 chars
- [x] References actual codebase

---

## Existing StickerNest Skills

Reference these for patterns:

| Skill | Location |
|-------|----------|
| `creating-widgets` | `.claude/skills/creating-widgets/` |
| `connecting-widget-pipelines` | `.claude/skills/connecting-widget-pipelines/` |
| `testing-widgets` | `.claude/skills/testing-widgets/` |
| `creating-components` | `.claude/skills/creating-components/` |
| `creating-zustand-stores` | `.claude/skills/creating-zustand-stores/` |
