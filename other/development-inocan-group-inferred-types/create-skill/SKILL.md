---
name: create-skill

description: Create a new Claude Code skill with proper directory structure and SKILL.md format.
---

# Create Skill

Create a new Claude Code skill with proper directory structure and format.

## Usage

Invoke with: `/create-skill <skill-name> <description>`

Example: `/create-skill code-review Review code for best practices and potential issues`

## Instructions

When this skill is invoked:

1. **Parse the skill name and description**

   - Extract skill name (should be kebab-case, e.g., `my-skill`)
   - Extract or ask for a brief description of what the skill does

2. **Create directory structure**

   - Create directory at `~/.claude/skills/<skill-name>/`
   - Create `SKILL.md` file inside the directory

3. **Generate SKILL.md content**

   The file must follow this exact format:

   ```markdown
   ---
   name: <skill-name>

   description: <brief description of the skill>
   ---

   # <Skill Title>

   <Longer description of what this skill does>

   ## Usage

   Invoke with: `/<skill-name>` or `/<skill-name> <arguments>`

   ## Instructions

   When this skill is invoked:

   1. **First step**
      - Sub-step details
      - More details

   2. **Second step**
      - Sub-step details

   3. **Third step**
      ...

   ## Example Interaction (optional)

   Show example input/output

   ## Notes (optional)

   Additional notes or constraints
   ```

4. **Ask user for skill details**

   - What should the skill do?
   - What steps should it follow?
   - Any specific constraints or notes?

5. **Write the file and confirm**

   - Write the SKILL.md file
   - Show the created content to user
   - Confirm the skill is ready to use

## Skill File Requirements

- **Location**: `~/.claude/skills/<skill-name>/SKILL.md` (user-level, global)
- **Location**: `.claude/skills/<skill-name>/SKILL.md` (project-level)
- **YAML Front Matter**: Must include `name` and `description` fields
- **Markdown Content**: Clear instructions for Claude to follow

## Example

```
User: /create-skill pr-review Review pull requests for code quality

Assistant: I'll create a new skill called "pr-review".

Creating directory: ~/.claude/skills/pr-review/
Creating file: ~/.claude/skills/pr-review/SKILL.md

Generated content:
---
name: pr-review

description: Review pull requests for code quality and best practices.
---

# PR Review Skill
...

Skill "pr-review" created successfully\!
You can now use it with: /pr-review
```
