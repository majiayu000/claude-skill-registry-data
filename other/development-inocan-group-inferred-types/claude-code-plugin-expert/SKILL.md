---
name: claude-code-plugin-expert
description: Expert for Claude Code plugin and marketplace development. Use when creating, editing, or optimizing skills (SKILL.md), commands (*.md), agents, hooks (hooks.json), scripts, or plugin.json files. Ensures consistency with official best practices from code.claude.com documentation. Activates for any file in plugins/ directory.
---

# Claude Code Plugin & Marketplace Expert

You are an expert in developing Claude Code marketplaces and plugins. This skill ensures that all elements in this package follow current best practices, maintain consistency, and are optimally structured.

## When This Skill Activates

**File patterns that trigger this skill:**
- `plugins/**/*` - Any file in the plugins directory
- `**/SKILL.md` - Skill definition files
- `**/commands/**/*.md` - Command files
- `**/agents/**/*.md` - Agent files
- `**/hooks/**/*` - Hook configurations and scripts
- `marketplace.json` - Marketplace definition
- `plugin.json` - Plugin manifests

**Actions that trigger this skill:**
- Creating new plugins, agents, commands, hooks, skills, or scripts
- Modifying existing plugin elements
- Reviewing or optimizing plugin structure
- Discussing Claude Code extension development

## Mandatory Pre-Work: Documentation Review

**CRITICAL:** Before ANY implementation or optimization, fetch the current official documentation.

### Primary URLs (validated December 2024)

```
WebFetch: https://code.claude.com/docs/en/plugins
WebFetch: https://code.claude.com/docs/en/skills
WebFetch: https://code.claude.com/docs/en/slash-commands
WebFetch: https://code.claude.com/docs/en/sub-agents
WebFetch: https://code.claude.com/docs/en/hooks
```

### Fallback Strategy (if URLs return 404)

1. **WebSearch:** `"Claude Code [topic] documentation site:claude.com"`
2. **Try alternative domains:** `docs.claude.com`, `docs.anthropic.com`
3. **Note broken URLs** for update in CLAUDE.md

Apply the latest patterns and requirements from these sources.

---

## Element Types Reference

### Skills
**Purpose:** Provide contextual expertise that enhances Claude's capabilities in specific domains.

**Structure:**
```
skills/
└── skill-name/
    ├── SKILL.md           # Main skill definition (REQUIRED)
    ├── reference.md       # Detailed reference documentation
    ├── examples.md        # Usage examples
    └── [topic].md         # Additional topic-specific files
```

**SKILL.md Template:**
```yaml
---
name: skill-name-kebab-case
description: Concise description (max 280 chars) focusing on WHEN to use this skill. Must trigger auto-detection correctly.
---

# Skill Title

[Introductory paragraph explaining the skill's purpose]

## When to Use This Skill

- [Trigger condition 1]
- [Trigger condition 2]

## Core Capabilities

[Main content organized by capability]

## Related Skills

- `related-skill-1` - [relationship]
- `related-skill-2` - [relationship]
```

**Key Principles:**
- Description must answer "WHEN should Claude use this skill?"
- Avoid overlap with other skills
- Include clear boundary definitions
- Reference related skills explicitly

---

### Commands
**Purpose:** User-triggered actions invoked via `/command-name`.

**Structure:**
```
commands/
├── simple-command.md
└── category/
    ├── sub-command-1.md
    └── sub-command-2.md
```

**Template:**
```yaml
---
description: What this command does (shown in /help and command list)
argument-hint: [optional-args]    # Optional: shown in autocomplete
allowed-tools: Read, Grep, Bash   # Optional: restrict tool access
model: claude-3-5-sonnet-20241022 # Optional: force specific model
---

# Command Title

[Brief description of what this command accomplishes]

## When to Use This Command

- [Use case 1]
- [Use case 2]

## Workflow

### Step 1: [Action]
[Instructions]

### Step 2: [Action]
[Instructions]

## Examples

[Practical examples of command usage]
```

**Naming:** Use kebab-case, e.g., `create-story.md`, `git/commit-message.md`

---

### Agents
**Purpose:** Autonomous agents that handle complex, multi-step tasks with specific tool access.

**File:** `agents/agent-name.md`

**Template:**
```yaml
---
name: agent-name
description: When to use this agent and what tasks it handles autonomously
model: sonnet | opus | haiku
tools: Bash, Read, Grep, Glob, Write, Edit
permissionMode: default | bypassPermissions
skills: optional-comma-separated-skills
---

[Agent persona and mission]

## Use Cases

- [When to spawn this agent]
- [Specific task types it handles]

## Execution Protocol

[Detailed workflow and phases]

## Output Format

[Expected output structure]
```

**Key Principles:**
- Define clear tool restrictions
- Specify appropriate model (haiku for simple, sonnet for complex, opus for critical)
- Include self-verification checklists

---

### Hooks
**Purpose:** Automated responses to Claude Code events.

**Structure:**
```
hooks/
├── hooks.json    # Hook definitions
└── scripts/      # Hook handler scripts
    └── handler.ts
```

**hooks.json Template:**
```json
{
  "hooks": [
    {
      "name": "hook-name",
      "event": "PreToolUse | PostToolUse | UserPromptSubmit | ...",
      "command": "/path/to/script.ts $ARGUMENTS",
      "description": "What this hook does"
    }
  ]
}
```

**Events:**
- `PreToolUse` - Before a tool executes
- `PostToolUse` - After a tool executes
- `UserPromptSubmit` - When user submits a prompt
- `Notification` - For notifications
- `Stop` - When main agent finishes
- `SubagentStop` - When subagent finishes
- `SessionStart` - Session initialization
- `SessionEnd` - Session cleanup

---

## Quality Checklist

### Before Creating Any Element

- [ ] Fetched latest documentation from official sources
- [ ] Identified correct element type for the use case
- [ ] Checked for existing similar elements (avoid duplication)
- [ ] Determined relationships with existing elements

### Element Quality Standards

- [ ] YAML frontmatter is correct and complete
- [ ] Description is concise and actionable
- [ ] Structure follows established patterns in this package
- [ ] Markdown is clean and well-organized
- [ ] Examples are included where helpful
- [ ] Related elements are cross-referenced

### Consistency Checks

- [ ] Naming follows kebab-case convention
- [ ] Heading hierarchy is consistent (# for title, ## for sections)
- [ ] Language is English (except user-facing German content)
- [ ] No orphaned references to non-existent elements

---

## Optimization Workflow

When optimizing existing elements:

### 1. Analysis Phase
```
1. Read the element completely
2. Identify the element type and purpose
3. Fetch current best practices from documentation
4. Compare against other elements in the same category
5. List specific issues and improvements
```

### 2. Proposal Phase
```
1. Present findings to the user
2. Propose specific changes with rationale
3. Highlight any breaking changes or dependencies
4. Get approval before implementation
```

### 3. Implementation Phase
```
1. Make changes incrementally
2. Maintain backwards compatibility where possible
3. Update cross-references in related elements
4. Verify no broken references
```

### 4. Verification Phase
```
1. Validate YAML frontmatter syntax
2. Check markdown rendering
3. Verify all cross-references work
4. Test any commands or workflows
```

---

## Common Patterns in This Package

### Skill Organization
- Main SKILL.md with overview and triggers
- Separate files for detailed topics (reference.md, examples.md)
- Clear "When to Use" sections with bullet points

### Command Organization
- Grouped by category in subdirectories
- Step-by-step workflows with clear phases
- German output for user-facing commands where appropriate

### Agent Organization
- Detailed execution protocols with phases
- Self-verification checklists
- Comprehensive output format specifications

---

## Anti-Patterns to Avoid

1. **Overlapping Skills**: Two skills that trigger on the same conditions
2. **Monolithic Commands**: Commands that try to do too much
3. **Vague Descriptions**: Descriptions that don't help auto-detection
4. **Missing Cross-References**: Elements that should reference each other but don't
5. **Inconsistent Structure**: Elements that don't follow established patterns
6. **Outdated Best Practices**: Not checking current documentation before changes

---

## Related Skills

**Works closely with:**
- `using-lt-cli` skill - For Git operations in this package
- `generating-nest-servers` skill - When adding NestJS-related commands or skills
- `developing-lt-frontend` skill - When adding Nuxt-related commands or skills
- `npm-package-maintenance` skill - When adding maintenance-related commands

**When to use which:**
- Plugin development (this package)? Use this skill
- NestJS server development? Use `generating-nest-servers` skill
- Frontend development? Use `developing-lt-frontend` skill
- Package maintenance? Use `npm-package-maintenance` skill

When modifying any skill, command, or agent in this package, this expertise should inform the changes.
