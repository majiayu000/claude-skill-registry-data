---
name: extension-create
descriptive-title: Creating Claude Code Extensions
description: Creates slash commands, subagents/workflows, or agent skills using the Claude request type framework. Analyzes requirements, determines the optimal extension type (command/subagent/skill), decides project vs personal scope, and generates properly structured files following templates and best practices. Use when creating new commands, workflows, or skills, or when the user mentions "create a command", "new workflow", "build a skill", or requests custom Claude Code extensions.
platforms: ["claude-code"]
status: stable
allowed-tools: ["Read","Write","Bash","Grep","Glob","AskUserQuestion"]
category: development
tags: ["claude-code","extensions","skills","commands","workflows","scaffolding"]
---

# Creating extensions

Creates slash commands, subagents/workflows, or agent skills for Claude Code following the decision framework and best practices.

## What you should do

When invoked, guide the user through creating the right type of extension:

1. **Understand the requirement** - Gather information about what the user wants to create:
   - What task or capability do they want to add?
   - How complex is the workflow?
   - Should it be manually triggered or automatically discovered?
   - Does it generate extensive output or "chatter"?
   - Does it need supporting files, scripts, or templates?
   - Is this for personal use or team-wide adoption?

2. **Evaluate using the framework** - Apply the Claude request type framework criteria:
   - **Initiation**: User-only (manual) or Discoverable (automatic)?
   - **Context needs**: Full conversation history or summary context?
   - **Verbosity**: Manageable output or extensive (pollutes main thread)?
   - **Specialization**: General purpose or needs specialist persona?
   - **Resource use**: Standard (instructions only) or heavy (requires references/scripts)?

3. **Determine the extension type** based on evaluation profile:

   **Slash Command** when:
   - User-only initiation (manual trigger required)
   - Full context needed
   - Manageable output
   - Generalist (no special persona)
   - Standard resources (single file sufficient)

   **Subagent/Workflow** when:
   - Discoverable (automatic invocation)
   - Summary context (context isolation needed)
   - **Extensive verbosity** (PRIMARY INDICATOR - pollutes main thread)
   - **Specialist persona** (PRIMARY INDICATOR - needs distinct system prompt)
   - Standard resources

   **Agent Skill** when:
   - Discoverable (automatic invocation)
   - Any context needs
   - Any verbosity level
   - Any specialization level
   - **Heavy resource use** (PRIMARY INDICATOR - requires multiple files, scripts, templates, or references)

4. **Determine the scope and format** - Critical: Different formats for different scopes:

   **Project-specific** (Claude Code format):
   - **Project-level**: `.claude/commands/`, `.claude/subagents/`, `.claude/skills/` (shared with team)
   - **Personal-level**: `~/.claude/commands/`, `~/.claude/subagents/`, `~/.claude/skills/` (personal only)
   - Uses Claude Code format (minimal frontmatter, platform-specific)

   **Agent-playbook global** (Multi-platform format):
   - **Repository**: `core/workflows/`, `core/skills/` in agent-playbook repo
   - Uses extended frontmatter with `platforms`, `status`, `category`, `tags`
   - Gets distributed to multiple platforms via build process
   - **Ask user to check if this is agent-playbook repo** before using this format

   Ask the user which scope, then use the appropriate format.

5. **Generate the extension** - Use format based on scope (see reference files for complete examples):

   **Project-specific (Claude Code format)**:
   - Minimal frontmatter
   - Platform-specific conventions
   - See [COMMANDS.md](COMMANDS.md), [WORKFLOWS.md](WORKFLOWS.md), [SKILLS.md](SKILLS.md) for Claude Code format

   **Agent-playbook global (Multi-platform format)**:
   - Extended frontmatter with `platforms: ["claude-code"]`, `status`, `category`, `tags`
   - Platform-agnostic content
   - Build process transforms for each platform
   - Only use if user confirms this is agent-playbook repository

6. **Validate and test** - Ensure the extension follows best practices:
   - Correct file location
   - Proper frontmatter format
   - Clear, actionable instructions
   - Follows naming conventions
   - Includes appropriate metadata

## Decision framework reference

Use this quick reference to determine extension type:

### Primary indicators (strongest signals)

- **Extensive verbosity** → Subagent (context isolation required)
- **Specialist persona** → Subagent (distinct system prompt needed)
- **Heavy resources** → Skill (multiple files, scripts, templates)

### Supporting indicators

- **User-only initiation** → Slash command (manual trigger)
- **Discoverable initiation** → Subagent or Skill (automatic)
- **Single file sufficient** → Slash command (simplest)
- **Context pollution** → Subagent (isolate the chatter)

## File naming conventions

**Slash commands**: `<area>[-<subarea>]-<verb>[-<object>].md`

- Examples: `git-review.md`, `docs-format.md`, `test-run.md`

**Subagents/workflows**: `<area>[-<subarea>]-<verb>[-<object>].md`

- Examples: `repo-code-quality-review.md`, `git-commit.md`, `docs-organize.md`

**Agent skills**: `<area>[-<subarea>]-<verb>[-<object>]/SKILL.md`

- Directory name uses kebab-case
- Examples: `creating-agent-skills/`, `tests-run/`, `gh-project-setup/`

All names use:

- Kebab-case (lowercase with hyphens)
- American English spelling
- Imperative verbs for workflows
- Gerund form for skill names

## Best practices by type

### Slash commands

- Keep it simple (one file only)
- Use clear argument hints
- Specify allowed-tools if restrictive
- Write clear, direct instructions

For detailed slash command best practices, see [COMMANDS.md](COMMANDS.md).

### Subagents/workflows

- Define clear persona and specialization
- Include step-by-step invocation workflow
- Specify model if non-default needed
- Restrict tools to minimum required
- USE PROACTIVELY statement in description

For detailed workflow best practices, see [WORKFLOWS.md](WORKFLOWS.md).

### Agent skills

- Use gerund form naming ("Managing X")
- Write third-person descriptions
- Include specific trigger keywords
- Keep `SKILL.md` under 500 lines
- Use progressive disclosure for details
- Test discovery with real scenarios

For detailed skill best practices, see [SKILLS.md](SKILLS.md).

## Example interactions

**User request**: "Create a command to run my tests"

- **Analysis**: User-only, manageable output, single purpose → **Slash command**
- **Scope**: Ask if project or personal
- **Location**: `.claude/commands/test-run.md` (project) or `~/.claude/commands/test-run.md` (personal)
- **Format**: Claude Code format (minimal frontmatter)

**User request**: "I need something that does a deep code quality audit"

- **Analysis**: Extensive verbosity (would pollute main thread), specialist persona needed → **Subagent**
- **Scope**: Ask if project-specific or global (agent-playbook)
- **Location**: `.claude/subagents/code-quality-audit.md` (project) or `core/workflows/code-quality-audit.md` (agent-playbook)
- **Format**: Claude Code format for project, multi-platform for agent-playbook

**User request**: "Create a workflow for managing GitHub Projects with our team conventions"

- **Analysis**: Heavy resources (needs field IDs, templates, examples), team-wide → **Skill**
- **Scope**: Ask if project-specific or global (agent-playbook)
- **Location**: `.claude/skills/gh-project-manage/SKILL.md` (project) or `core/skills/gh-project-manage/SKILL.md` (agent-playbook)
- **Format**: Claude Code format for project, multi-platform for agent-playbook

## Output format

When creating an extension, provide:

1. **Analysis summary**:
   - Extension type chosen and why
   - Scope (project vs personal)
   - File location

2. **Complete file content** with proper formatting

3. **Next steps**:
   - How to `test` or `use` it
   - Any additional setup needed
   - `Build` or `distribution` steps if applicable

## Format selection guide

**CRITICAL**: Use the correct format for the scope.

### For project-specific extensions

**Location**: `.claude/` directories in any project
**Format**: Claude Code format (minimal frontmatter)
**When**: Extension is specific to this project or personal workflow

Example workflow frontmatter:

```yaml
---
name: workflow-name
description: Brief description. USE PROACTIVELY when <trigger>.
persona: You are a <role> specializing in <specialization>.
tools: Bash, Read, Grep, Glob
model: haiku
---
```

### For agent-playbook global extensions

**Location**: `core/workflows/`, `core/skills/` in agent-playbook repo ONLY
**Format**: Multi-platform format (extended frontmatter)
**When**: Extension should be available globally across all projects and platforms

Example workflow frontmatter:

```yaml
---
name: workflow-name
descriptive-title: Human-readable title
description: Brief description. USE PROACTIVELY when <trigger>.
persona: You are a <role> specializing in <specialization>.
tools: Bash, Read, Grep, Glob
model: haiku
---
```

**Check first**: Ask "Is this the agent-playbook repository?" before using multi-platform format.

### After creation (agent-playbook only)

If created in `core/`:

1. Run `npm run build:claude` to generate distribution files
2. Run `npm run dist:local` to deploy to `~/.claude/`

## Remember

- **Primary indicators** (verbosity, specialization, resources) are strongest signals
- **Context pollution** is the key heuristic for subagents
- **Automatic discovery** is the key benefit of skills over commands
- **Simplicity** favors commands over more complex types
- When uncertain, ask the user clarifying questions
- Default to project-level unless clearly personal
- Always follow repository conventions and templates

## Reference documentation

For detailed best practices by type:

- [COMMANDS.md](COMMANDS.md) - Complete slash command reference with patterns and examples
- [WORKFLOWS.md](WORKFLOWS.md) - Comprehensive subagent/workflow guide with system prompt patterns
- [SKILLS.md](SKILLS.md) - Detailed skill creation guide with progressive disclosure strategies

## Official documentation

For complete details:

- **Request type framework**: `docs/type-decision-framework.md`
- **Extension architecture**: `docs/claude-code-extension-architecture.md`
- **Slash commands**: <https://code.claude.com/docs/en/slash-commands>
- **Agent skills**: <https://code.claude.com/docs/en/skills>
- **Subagents**: <https://code.claude.com/docs/en/sub-agents>