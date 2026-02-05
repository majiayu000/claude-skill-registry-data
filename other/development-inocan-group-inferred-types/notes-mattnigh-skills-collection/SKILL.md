---
name: notes
description: DO NOT USE THE APPLICATION NOTE SERVICE. Maintain and organize daily notes for the current project. Create, update, and manage these notes in a structured manner upon user request. Use this skill when the user requests "please make|create|write|add a note...".
allowed-tools: Bash, Glob, Read
---

# Notes Skill

Centralizes project development notes so Claude captures important insights, decisions, and learnings in a structured, timestamped format.

## Critical Workflow

**REQUIRED**: Before creating notes, determine the note type and load the appropriate template reference:

- **Code Review Notes** → Read `references/review-note-template.md` FIRST, then use `scripts/create-note.sh --template review`
- **Development Notes** → Use `scripts/create-note.sh` (default template)

### Code Review Notes

**MANDATORY: Load the template reference before creating review notes:**

```bash
# 1. Read the template reference (REQUIRED)
Read: .claude/skills/notes/references/review-note-template.md

# 2. Use the unified script with --template flag
./.claude/skills/notes/scripts/create-note.sh --template review "Component/File Name" "path/to/file.tsx" "Review findings markdown"
```

### Development Notes

```bash
# Default template (no flag needed)
./.claude/skills/notes/scripts/create-note.sh "Title" "file:line" "Body"

# Or explicitly
./.claude/skills/notes/scripts/create-note.sh --template default "Title" "file:line" "Body"
```

**Guidelines**:
1. **Always load template references** before creating notes of that type
2. **Use the --template flag** for non-default note types (e.g., `--template review`)
3. **Body format**: Use markdown with code blocks, evaluation points, next steps
4. **Keep it concise**: Focus on actionable insights
5. **IMPORTANT**: When user mentions "push to github" or creating issues, use `Skill("github")` tool (NOT bash `gh` commands)

## Note Structure

Use this format for all notes unless prompted otherwise:

```markdown
## [YYYY-MM-DD]

### [HH:MM:SS] - Brief note title

- **File**: path/to/file.tsx:line-number
- **Current approach/pattern**: description of current implementation
- **Suggested update**: description of improvement or change
- **Context**: explanation of why this matters
- **Code reference**:
  \`\`\`typescript
  // relevant code snippet
  \`\`\`
- **References**: (only if researched)
  - link 1
  - link 2
- **Next steps**:
  - step 1
  - step 2
```

## Key Guidelines

- Always include file paths with line numbers when referencing code
- Use code blocks to highlight relevant source code
- Timestamp each entry for tracking when insights were captured
- Include "Next steps" to actionable items from the note
- Keep references lean—only include if you performed research
- Don't over-explain; be concise and direct

## Helper Script

The unified `create-note.sh` script supports multiple templates via `--template` flag:

```bash
# Development notes (default)
./.claude/skills/notes/scripts/create-note.sh \
  "Add error boundary to Pokemon detail" \
  "app/routes/pokemon.\$id.tsx:45" \
  "- **Current approach**: No error handling for failed Pokemon API calls
- **Suggested update**: Wrap component in ErrorBoundary component
- **Context**: Route can crash if API returns 404
- **Next steps**:
  - Create error boundary component
  - Add fallback UI for failed loads"

# Code review notes
./.claude/skills/notes/scripts/create-note.sh \
  --template review \
  "home-outlet" \
  "app/routes/home-outlet.tsx" \
  "#### Critical Issues
1. **Loading spinners lack announcements** (lines 135-136)
   - Problem: No screen reader feedback
   - Fix: Add role=\"status\" and aria-label

**Reviewers**: Accessibility, React Router"
```

The script automatically:
- Generates timestamp in correct format
- Creates or appends to today's note file
- Maintains consistent note structure
- Routes to appropriate directory based on template (`docs/notes/` or `docs/notes/reviews/`)
- Supports extensible template system (add new templates in script's case statement)

## Template References (load on demand)

**CRITICAL**: Always load the appropriate template reference BEFORE creating notes of that type. These references define the structure, format, and guidelines for each note category.

- **Code Review Notes** - Multi-perspective review findings organized by severity with actionable fixes. [Open template](references/review-note-template.md)
- **Development Notes** - Standard development insights, decisions, and learnings. (Default format in SKILL.md)

Each template stays out of context until explicitly opened, keeping Claude's context lean while providing fast access to detailed formatting guidance.