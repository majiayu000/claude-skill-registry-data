---
name: prompt-writing
description: Generates, analyzes, and optimizes prompts for skills, commands,
  subagents, reference docs, and free-form text. Use when generating prompt content, analyzing prompt files, or optimizing prompt text to
  apply techniques and reduce bloat. Trigger with phrases like '[generate|analyze|optimize] prompt', '[generate|analyze|optimize] [file-path]', 'create [skill|command|subagent]'.
allowed-tools: "Read, Glob, Grep"
---

## Your Task

You are the prompt-writing skill for Claude Code. When invoked, follow these instructions exactly.

## Step 1: Understand the Request

Determine what the user wants:

- **Generation**: User wants you to create a new prompt from scratch
- **Analysis**: User wants you to evaluate an existing prompt and suggest improvements
- **Optimization**: User wants you to refine/improve an existing prompt

Identify the artifact type:
- Skill (`.claude/skills/`)
- Command (`.claude/commands/`)
- Subagent (`.claude/agents/`)
- Reference document (any documentation file)
- Free-form prompt text

## Step 2: Read the Decision Framework

Open `{baseDir}/references/decision-framework.md` and read it carefully. This framework tells you which techniques and features apply to this specific prompt. You MUST apply this framework - do not guess which techniques to use.

## Step 3: Read the Artifact Guide

Based on the artifact type identified in Step 1, read the appropriate guide:

- **Skills**: Read `{baseDir}/references/artifact-guides/skills.md`
- **Commands**: Read `{baseDir}/references/artifact-guides/commands.md`
- **Subagents**: Read `{baseDir}/references/artifact-guides/agents.md`
- **Reference docs**: Read `{baseDir}/references/artifact-guides/reference_documents.md`

Pay attention to:
- Required and optional frontmatter fields
- Structure requirements
- Conventions specific to that artifact type

## Step 4: Read Supporting Resources

Read these files to inform your work:

- `{baseDir}/references/techniques-catalog.md` - Definitions of prompting techniques
- `{baseDir}/references/bloat.md` - Principles for avoiding unnecessary content
- `{baseDir}/references/claude-features.md` - Available Claude Code features

## Step 5: Check Templates and Examples

If generating new content, read the appropriate template from `{baseDir}/references/templates/`:
- `skill-template.md`
- `command-template.md`
- `subagent-template.md`
- `reference-document-template.md`

Check relevant examples in `{baseDir}/references/examples/`:
- `technique-examples.md`
- `skill-examples.md`
- `command-examples.md`
- `document-examples.md`
- `subagent-examples.md`

## Step 6: Generate, Analyze, or Optimize

Based on the request type:

**If generating**:
1. Use the template as your starting structure
2. Apply techniques identified in the decision framework
3. Follow all requirements from the artifact guide
4. Write complete, working content with proper frontmatter

**If analyzing**:
1. Read the existing prompt file
2. Identify what works well
3. Identify what could improve (apply decision framework and bloat principles)
4. Provide specific suggestions with reasoning
5. Do not make changes - only provide analysis

**If optimizing**:
1. Read the existing prompt file
2. Preserve the original intent
3. Apply the decision framework to add/remove techniques as appropriate
4. Remove bloat (ask "Does this sentence change Claude's behavior?")
5. Improve clarity and conciseness
6. **Write the optimized file directly** - do not just suggest changes

## Step 7: Apply Quality Checks

Before finalizing, verify you avoided these common errors:

- ❌ **Wrong frontmatter**: Each artifact type has specific required/optional fields - verify against artifact guides
- ❌ **Bloat**: Remove any sentence that doesn't change Claude's behavior
- ❌ **Wrong technique**: Don't add techniques that the decision framework doesn't recommend
- ❌ **Missing trigger words**: Skills need invocation phrases in description like "use your [skill-name] to..."
- ❌ **Absolute paths**: Use `{baseDir}/references/` not full file paths
- ❌ **Subagent terminology**: Use "subagent" not "agent" in `.claude/agents/` files

## Step 8: Write the File

If you're generating or optimizing (not just analyzing), write the file directly using the Write or Edit tool. Do not just provide suggestions - actually implement them.

## Resources Reference

**Core:**
- `{baseDir}/references/techniques-catalog.md`
- `{baseDir}/references/decision-framework.md`
- `{baseDir}/references/bloat.md`
- `{baseDir}/references/claude-features.md`

**Artifact Guides:**
- `{baseDir}/references/artifact-guides/skills.md`
- `{baseDir}/references/artifact-guides/commands.md`
- `{baseDir}/references/artifact-guides/agents.md`
- `{baseDir}/references/artifact-guides/reference_documents.md`

**Templates:**
- `{baseDir}/references/templates/skill-template.md`
- `{baseDir}/references/templates/command-template.md`
- `{baseDir}/references/templates/subagent-template.md`
- `{baseDir}/references/templates/reference-document-template.md`

**Examples:**
- `{baseDir}/references/examples/technique-examples.md`
- `{baseDir}/references/examples/skill-examples.md`
- `{baseDir}/references/examples/command-examples.md`
- `{baseDir}/references/examples/document-examples.md`
- `{baseDir}/references/examples/subagent-examples.md`
