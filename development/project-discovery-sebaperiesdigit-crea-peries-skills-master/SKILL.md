---
name: project-discovery
description: Use when someone asks to explore this project, understand what's in this project, show me around, how do I start here, what can I do in this project, give me a tour, analyze this project, or map the codebase. Read-only project inspection for beginners.
argument-hint: [path or folder]
context: fork
agent: Explore
allowed-tools: Read, Glob, Grep, Bash(git status), Bash(git branch --show-current), Bash(git log --oneline -5)
---

## What This Skill Does

Inspects an unfamiliar VS Code project in read-only mode and produces a beginner-friendly overview of its purpose, structure, documentation, available Claude Skills, MCP connectors, rules, restrictions, Git status, and safe next steps. Designed for employees who are new to a project and need to understand what they can safely do.

## Process

Follow this order strictly. Do not skip steps. After each section, briefly share what you found before moving to the next.

### Step 1: Read Root Files

If $ARGUMENTS is provided, use it as the path within the current project root. Otherwise use the project root.

Read the following files if they exist (in order):
- `README.md` — Project description, setup instructions, purpose
- `CLAUDE.md` — Project-wide rules and restrictions that apply to all work
- `package.json`, `Cargo.toml`, `pyproject.toml`, or other language-specific config — Purpose and dependencies
- `.gitignore` — What's intentionally excluded
- Any other root-level documentation files (*.md)

Do not read deeply into subdirectories yet. Report what you find conversationally.

### Step 2: List Project Structure

List the top-level directories and their apparent purpose:
- `src/` or equivalent — Source code
- `docs/` — Documentation
- `tests/` or `__tests__` — Test files
- `output/` — Generated output files
- `.claude/` — Claude configuration (inspected in Step 3)

Use Glob or the directory listing. Report the structure conversationally. Do not explore unrelated external folders.

### Step 3: Inspect .claude/

Examine `.claude/` directory:
- List all skill directories under `.claude/skills/`
- For each skill, read only the frontmatter block — the text strictly between the first two `---` lines — to extract: name, description, whether it accepts arguments. Do not grep or scan the rest of the file for these fields: some skills (e.g. `skill-builder`) contain example SKILL.md templates with their own `name:`/`description:` lines inside a code fence in the body, which a whole-file search would misattribute.
- Do not read full skill content unless it is short (< 20 lines)
- Check for any configuration files or custom rules

Report available skills and what each one does. If no skills exist, state: "No skills configured yet — that's normal."

### Step 4: Check MCP Configuration

Inspect configuration files that may define MCP connectors:
- Look for `.mcp.json`, `mcp.json`, or MCP-related settings in project config files
- Read only enough to identify connector names, types, and filenames

For each connector found, report ONLY:
- Connector name
- Configuration filename it was found in
- Whether configuration appears present (yes/no)

**NEVER display:** passwords, API keys, tokens, connection strings, or raw config values.

If no MCP configuration is found, state: "No MCP connectors detected — this project has no external tool connections configured."

### Step 5: Git Status (Optional)

Try these commands in order. If any fails (not a git repo, git unavailable, etc.), report it clearly and continue.

1. `git status` — Current branch and changed files
2. `git branch --show-current` — Active branch name
3. `git log --oneline -5` — Recent commit history

Report findings conversationally. If not a git repo or git unavailable, say: "This folder is not a Git repository (or Git is unavailable) — that's fine."

### Step 6: Summarize Everything

Compile findings into a clear, beginner-friendly summary with these sections:

```
## Project Discovery: [project name]

### Project Purpose
[from README or inferred from structure]

### Important Folders
- [folder] → [purpose]

### Available Skills
- /[name] — [description]

### Configured Connectors Detected
- [name] — [type] (found in [filename])

### Standing Rules
[from CLAUDE.md or "None documented"]

### Known Restrictions
[from CLAUDE.md or observed structure]

### Missing Information
- [anything not found that would be useful]

### Recommended First Safe Action
[one concrete next step based on findings]
```

### Step 7: Recommended First Safe Action

Based on everything discovered, suggest one concrete, safe action the employee could take next. For example:
- "Try running `/skill-name` to see how it works"
- "Read `README.md` for setup instructions"
- "Ask your manager if there's a CLAUDE.md to add"

## Notes

- NEVER modify any files — this skill is read-only
- NEVER display passwords, API keys, tokens, connection strings, or any credential-like values
- NEVER install packages, run migrations, start services, or execute project scripts
- NEVER test live MCP connectivity
- NEVER explore outside the current project root
- Never guess — flag missing resources clearly (e.g., "CLAUDE.md not found")
- Handle empty, incomplete, or undocumented projects gracefully — don't invent structure
- Bash is permitted only for: `git status`, `git branch --show-current`, `git log --oneline -5`
- If Git commands fail, report it and continue — do not attempt destructive git commands
- Keep the output fully conversational — do not create any report files
- Clickable-question convention: not applicable. This skill runs with `context: fork` (an isolated subagent with no back-and-forth with the user) and is entirely read-only/report-only — it never asks the user anything, so there are no question points to convert.
