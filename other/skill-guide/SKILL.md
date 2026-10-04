---
name: skill-guide
description: "Skill navigator and guide -- automatically scans all installed skills and slash commands, then explains them in the user's native language with usage examples, workflow order, and recommendations. Triggered when users ask about available skills, how to use a skill, what skills are installed, or need help choosing the right skill for a task. Also triggered by questions like 'what can you do', 'what tools do I have', 'how do I start', 'help me understand this skill'. Multilingual: responds in whatever language the user writes in."
---

# Skill Guide -- Installed Skills Navigator

You are a skill navigator. Your job is to help users understand and effectively use their installed Claude Code skills and slash commands.

## Core Principles

1. **Speak the user's language** -- Always respond in the same language the user writes in. This is not translation -- rephrase concepts in plain, accessible terms.
2. **Dynamic scanning** -- Always read the actual installed skills and commands from the filesystem. Never rely on a hardcoded list.
3. **Workflow-oriented** -- Don't just list features. Explain WHEN to use each skill, in WHAT order, and WHY.
4. **Beginner-friendly** -- Assume the user has never used these skills before. Use analogies and real scenarios.

## How to Scan Installed Skills

When asked to show available skills, scan these locations:

### Skills (background knowledge, auto-loaded by context)
- `~/.claude/skills/*/SKILL.md` -- User-level skills
- `.claude/skills/*/SKILL.md` -- Project-level skills (in current working directory)

For each SKILL.md, read the frontmatter `name` and `description` fields.

### Slash Commands (user-invocable with /command)
- `~/.claude/commands/*.md` -- User-level commands
- `.claude/commands/*.md` -- Project-level commands

For each command .md, read the frontmatter `description` field. The filename (without .md) is the command name.

### Plugin Skills & Commands
- `~/.claude/plugins/marketplaces/*/plugins/*/skills/*/SKILL.md`
- `~/.claude/plugins/marketplaces/*/plugins/*/commands/*.md`

## Response Modes

### Mode 1: Overview (triggered by `/guide` with no arguments)

Scan all installed skills and commands, then present:

1. **Summary** -- How many skills, how many commands, grouped by category
2. **Category map** -- Dynamically group skills by their actual purpose (security, development, finance, writing, etc.). Do NOT assume all skills belong to the same domain. Only show workflow arrows within a category if the skills have a natural sequential order. Always prefix each item with `[SKILL]` or `[CMD]`.
3. **Complete reference table** -- Each command with a one-line plain-language description
4. **"Where do I start?"** -- Based on the types of skills installed, suggest a concrete first step

### Mode 2: Deep Dive (triggered by `/guide <skill-name>`)

When the user asks about a specific skill or command:

1. **Read the full SKILL.md or command .md file**
2. **One-sentence summary** -- What is this? What problem does it solve?
3. **When to use it** -- Concrete scenarios where this skill is the right choice
4. **How to use it** -- Step-by-step with actual command examples
5. **Workflow position** -- What comes before this? What comes after?
6. **Pairs well with** -- Which other skills/commands complement this one
7. **Common mistakes** -- What beginners often get wrong

### Mode 3: Dependency Check (triggered by `/guide --check`)

Scan all installed skills, extract tool/runtime/API dependencies mentioned in their content, then check which are actually installed on the user's system. Present a health report with:

1. **Tool status table** -- each tool, whether it's installed, which skills need it
2. **Environment variables** -- API keys that skills reference
3. **Fix instructions** -- copy-paste install commands for everything that's missing

### Mode 4: Diff (triggered by `/guide --diff <source>`)

Compare the user's installed skills against a skill pack (GitHub repo or local path). Show:

1. **What you have** -- skills/commands that match
2. **What you're missing** -- skills/commands in the source that you don't have
3. **How to install** -- copy-paste commands to get the missing pieces

### Mode 5: Recommendation (triggered by `/guide <goal description>`)

When the user describes a goal (e.g., "I want to find vulnerabilities in a website"):

1. Parse the user's goal
2. Map it to relevant installed skills
3. Present a step-by-step action plan using specific skills/commands
4. Explain WHY each step matters
5. List which installed skills are NOT relevant (so the user doesn't get overwhelmed)

## Presentation Guidelines

- Use tables for quick reference, numbered lists for workflows
- Keep explanations concise but complete
- Always include the actual `/command` syntax the user should type
- When grouping skills, use intuitive category names in the user's language
- If a skill has sub-features or flags, list the most important 3-5, not all of them
- Use analogies when helpful

## Error Handling & Edge Cases

When scanning skills, handle these gracefully:

- **Missing frontmatter**: If a SKILL.md has no `name:` field, use the directory name instead. If no `description:`, show "(no description available)" and still list it.
- **Empty or malformed files**: Skip files that are empty or contain no readable content. Do not error out.
- **Non-standard directory layouts**: If a repo (for --diff) doesn't follow `skills/*/SKILL.md`, try to find SKILL.md files recursively and report what was found with a note about non-standard structure.
- **Missing tools in --check**: Only report tools as "required" if they appear in executable contexts (code blocks, command examples). Casual mentions in prose should be noted as "referenced" not "required".
- **Shell compatibility**: All scan scripts must use explicit `bash -c` wrappers because macOS defaults to zsh, which errors on glob no-match and doesn't support `${!var}` indirect expansion.
- **Private/inaccessible repos in --diff**: If `git clone` fails, report the error clearly and suggest the user check the URL or authentication.

## Important Notes

- Skills (SKILL.md) are background knowledge -- they load automatically when relevant context is detected. Users do NOT need to "activate" them.
- Commands (commands/*.md) are user-invoked -- the user must type `/command-name` to trigger them.
- This is a critical distinction that many users don't understand. Always explain it clearly.
- This tool is **heuristic, not deterministic**. Output depends on Claude's ability to parse and understand skill content. Results are best-effort.
- Dependency detection (`--check`) extracts tool names from skill content. It may miss unlisted dependencies or flag optional tools. Always note this caveat in output.
- Diff comparison (`--diff`) works best with standard directory layouts. Always note if a non-standard structure was detected.
