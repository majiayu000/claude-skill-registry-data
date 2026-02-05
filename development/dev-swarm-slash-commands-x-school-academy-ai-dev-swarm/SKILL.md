---
name: dev-swarm-slash-commands
description: Create custom slash commands for popular AI agents (Claude Code, Codex, Gemini CLI). Use when user asks to create slash commands, custom commands, or reusable prompts for AI agent CLIs.
---

# AI Builder - Create Slash Commands for AI Agents

Create short, reusable slash command templates for a specific AI agent the user requests (Claude Code, Codex, or Gemini CLI).

## When to Use This Skill

- Create or update a slash command for a specific AI agent
- Standardize prompts across a team
- Automate repetitive agent workflows

## Your Roles in This Skill

- **DevOps Engineer**: Choose locations and file formats for each agent.
- **Backend Developer**: Define templates and argument handling.
- **Technical Writer**: Keep descriptions and usage notes clear and short.
- **Project Manager**: Enforce naming, scope, and completeness.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps:

### Step 1: Confirm Inputs

Ask:
1. Target agent(s): Claude Code, Codex, Gemini CLI
2. Command purpose (1 sentence)
3. Arguments/parameters
4. Scope: project or user

**Understanding scopes:**
- **Project-scoped**: only this repo (checked into git)
- **User-scoped**: all projects for this user

### Step 2: Choose the Target Agent

Only implement the command for the agent the user asked for. Do not create cross-agent commands unless explicitly requested.

### For Claude Code

**Location:**
- Project commands: `.claude/commands/`
- User commands: `~/.claude/commands/`

**File format:** Markdown (`.md`)

**Naming:**
- File: `command-name.md` becomes `/command-name`
- Namespaced: `category/command.md` becomes `/category:command`

**Parameter substitution:**
- `$ARGUMENTS` - All arguments passed to the command
- `$1`, `$2`, ..., `$9` - Individual space-separated arguments

### For Codex

**Location:**
- Custom prompts: `~/.codex/prompts/` (or `$CODEX_HOME/prompts`)
- Must use subfolder name `prompts`

**Codex does not support project level commands**

**File format:** Markdown (`.md`)

```markdown
---
description: Prep a branch, commit, and open a draft PR
argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
---

Create a branch named `dev/<feature_name>` for this work.
If files are specified, stage them first: $FILES.
Commit the staged changes with a clear message.
Open a draft PR on the same branch. Use $PR_TITLE when supplied; otherwise write a concise summary yourself.
```

#### Add metadata and arguments
Codex reads prompt metadata and resolves placeholders the next time the session starts.

- Description: Shown under the command name in the popup. Set it in YAML front matter as description:.
- Argument hint: Document expected parameters with argument-hint: KEY=<value>.
- Positional placeholders: $1 through $9 expand from space-separated arguments you provide after the command. $ARGUMENTS includes them all.
- Named placeholders: Use uppercase names like $FILE or $TICKET_ID and supply values as KEY=value. Quote values with spaces (for example, FOCUS="loading state").
- Literal dollar signs: Write $$ to emit a single $ in the expanded prompt.


**Naming:**
- Commands invoked as `/prompts:<name>`
- File `review-code.md` becomes `/prompts:review-code`

**Parameter types:**
1. **Positional arguments**: `$1` through `$9`
   - Usage: `/prompts:mycommand arg1 arg2 arg3`
2. **All arguments**: `$ARGUMENTS`
   - Gets all space-separated arguments
3. **Named placeholders**: `$FILE`, `$TICKET_ID` (uppercase)
   - Usage: `/prompts:mycommand FILE=app.js TICKET_ID=123`
   - Quote values with spaces: `FILE="my file.js"`

### For Gemini CLI

**Location:**
- User commands: `~/.gemini/commands/`
- Project commands: `.gemini/commands/`

**File format:** TOML (`.toml`)

```toml
# In: <project>/.gemini/commands/review.toml
# Invoked via: /review FileCommandLoader.ts

description = "Reviews the provided context using a best practice guide."
prompt = """
You are an expert code reviewer.

Your task is to review {{args}}.

Use the following best practices when providing your review:

@{docs/best-practices.md}
```

When you run /review FileCommandLoader.ts, the @{docs/best-practices.md} placeholder is replaced by the content of that file, and {{args}} is replaced by the text you provided, before the final prompt is sent to the model.

