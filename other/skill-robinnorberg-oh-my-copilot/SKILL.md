---
name: skill
description: Manage local skills - list, add, remove, search, edit, setup wizard
argument-hint: "<command> [args]"
level: 2
---

# Skill Management CLI

Meta-skill for managing oh-my-copilot skills via CLI-like commands.

## Subcommands

### /skill list

Show all available skills organized by scope.

**Behavior:**
1. Scan bundled built-in skills in the plugin `skills/` directory (read-only)
2. Scan user skills at `${COPILOT_HOME:-~/.copilot}/skills/omc-learned/`
3. Scan project skills at `.omg/skills/`
4. Parse YAML frontmatter for metadata
5. Display in organized table format:

```
BUILT-IN SKILLS (bundled with oh-my-copilot):
| Name              | Description                    | Scope    |
|-------------------|--------------------------------|----------|
| visual-verdict    | Structured visual QA verdicts  | built-in |
| ralph             | Persistence loop               | built-in |

USER SKILLS (~/.claude/skills/omc-learned/):
| Name              | Triggers           | Quality | Usage | Scope |
|-------------------|--------------------|---------|-------|-------|
| error-handler     | fix, error         | 95%     | 42    | user  |
| api-builder       | api, endpoint      | 88%     | 23    | user  |

PROJECT SKILLS (.omg/skills/):
| Name              | Triggers           | Quality | Usage | Scope   |
|-------------------|--------------------|---------|-------|---------|
| test-runner       | test, run          | 92%     | 15    | project |
```

**Fallback:** If quality/usage stats not available, show "N/A"

**Built-in skill note:** Built-in skills are bundled with oh-my-copilot and are discoverable/readable, but not removed or edited through `/skill remove` or `/skill edit`.

---

### /skill add [name]

Interactive wizard for creating a new skill.

**Behavior:**
1. **Ask for skill name** (if not provided in command)
   - Validate: lowercase, hyphens only, no spaces
2. **Ask for description**
   - Clear, concise one-liner
3. **Ask for triggers** (comma-separated keywords)
   - Example: "error, fix, debug"
4. **Ask for argument hint** (optional)
   - Example: "<file> [options]"
5. **Ask for scope:**
   - `user` → `${COPILOT_HOME:-~/.copilot}/skills/omc-learned/<name>/SKILL.md`
   - `project` → `.omg/skills/<name>/SKILL.md`
6. **Create skill file** with template:

```yaml
---
name: <name>
description: <description>
triggers:
  - <trigger1>
  - <trigger2>
argument-hint: "<args>"
---

# <Name> Skill

## Purpose

[Describe what this skill does]

## When to Activate

[Describe triggers and conditions]

## Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

```
/oh-my-copilot:<name> example-arg
```

## Notes

[Additional context, edge cases, gotchas]
```

7. **Report success** with file path
8. **Suggest:** "Edit `/skill edit <name>` to customize content"

**Example:**
```
User: /skill add custom-logger
Assistant: Creating new skill 'custom-logger'...

Description: Enhanced logging with structured output
Triggers (comma-separated): log, logger, logging
Argument hint (optional): <level> [message]
Scope (user/project): user

✓ Created skill at ~/.claude/skills/omc-learned/custom-logger/SKILL.md
→ Edit with: /skill edit custom-logger
```

---

### /skill remove <name>

Remove a skill by name.

**Behavior:**
1. **Search for skill** in both scopes:
   - `${COPILOT_HOME:-~/.copilot}/skills/omc-learned/<name>/SKILL.md`
   - `.omg/skills/<name>/SKILL.md`
2. **If found:**
   - Display skill info (name, description, scope)
   - **Ask for confirmation:** "Delete '<name>' skill from <scope>? (yes/no)"
3. **If confirmed:**
   - Delete entire skill directory (e.g., `${COPILOT_HOME:-~/.copilot}/skills/omc-learned/<name>/`)
   - Report: "✓ Removed skill '<name>' from <scope>"
4. **If not found:**
   - Report: "✗ Skill '<name>' not found in user or project scope"

**Safety:** Never delete without explicit user confirmation.

**Example:**
```
User: /skill remove old-logger
Assistant: Found skill 'old-logger' in user scope:
  Description: Legacy logging utility
  Scope: user (~/.claude/skills/omc-learned/)

Delete 'old-logger' skill? (yes/no)

User: yes
Assistant: ✓ Removed skill 'old-logger' from user scope
```

---

### /skill edit <name>

Edit an existing skill interactively.

**Behavior:**
1. **Find skill** by name (search both scopes)
2. **Read current content** via Read tool
3. **Display current values:**
   ```
   Current skill 'custom-logger':
   - Description: Enhanced logging with structured output
   - Triggers: log, logger, logging
   - Argument hint: <level> [message]
   - Scope: user
   ```
4. **Ask what to change:**
   - `description` - Update description
   - `triggers` - Update trigger keywords
   - `argument-hint` - Update argument hint
   - `content` - Edit full markdown content
   - `rename` - Rename skill (move file)
   - `cancel` - Exit without changes
5. **For selected field:**
   - Show current value
   - Ask for new value
   - Update YAML frontmatter or content
   - Write back to file
6. **Report success** with summary of changes

**Example:**
```
User: /skill edit custom-logger
Assistant: Current skill 'custom-logger':
  - Description: Enhanced logging with structured output
  - Triggers: log, logger, logging
  - Argument hint: <level> [message]

What would you like to edit? (description/triggers/argument-hint/content/rename/cancel)

User: triggers
Assistant: Current triggers: log, logger, logging
New triggers (comma-separated): log, logger, logging, trace

✓ Updated triggers for 'custom-logger'
```

---

### /skill search <query>

Search skills by content, triggers, name, or description.

**Behavior:**
1. **Scan all skills** in both scopes
2. **Match query** (case-insensitive) against:
   - Skill name
   - Description
   - Triggers
   - Full markdown content
3. **Display matches** with context:

```
Found 3 skills matching "typescript error":

1. typescript-fixer (user)
   Description: Fix common TypeScript errors
   Match: "typescript error handling patterns"

2. error-handler (user)
   Description: Generic error handling utilities
   Match: "Supports TypeScript and JavaScript errors"

3. lint-fix (project)
   Description: Auto-fix linting errors
   Match: "TypeScript ESLint error resolution"
```

**Ranking:** Prioritize matches in name/triggers over content matches

**Example:**
```
User: /skill search api endpoint
Assistant: Found 2 skills matching "api endpoint":

1. api-builder (user)
   Description: Generate REST API endpoints
   Triggers: api, endpoint, rest

2. backend-scaffold (project)
   Description: Scaffold backend services
   Match: "Creates API endpoint boilerplate"
```

---

### /skill info <name>

Show detailed information about a skill.

**Behavior:**
1. **Find skill** by name (search both scopes)
2. **Parse YAML frontmatter** and content
3. **Display complete details:**

```
Skill: custom-logger
Scope: user (~/.claude/skills/omc-learned/custom-logger/)
Description: Enhanced logging with structured output
Triggers: log, logger, logging
Argument Hint: <level> [message]
Quality: 95% (if available)
Usage Count: 42 times (if available)
File Path: /home/user/.claude/skills/omc-learned/custom-logger/SKILL.md

--- FULL CONTENT ---
[entire markdown content]
```

**If not found:** Report error with suggestion to use `/skill search`

**Example:**
```
User: /skill info custom-logger
Assistant: Skill: custom-logger
Scope: user
Description: Enhanced logging with structured output
Triggers: log, logger, logging
File: ~/.claude/skills/omc-learned/custom-logger/SKILL.md

--- CONTENT ---
# Custom Logger Skill

## Purpose
Enhanced logging with structured JSON output...
[rest of content]
```

---

### /skill sync

Sync skills between user and project scopes.

**Behavior:**
1. **Scan both scopes:**
   - User skills: `${COPILOT_HOME:-~/.copilot}/skills/omc-learned/`
   - Project skills: `.omg/skills/`
2. **Compare and categorize:**
   - User-only skills (not in project)
   - Project-only skills (not in user)
   - Common skills (in both)
3. **Display sync opportunities:**

```
SYNC REPORT:

User-only skills (5):
  - error-handler
  - api-builder
  - custom-logger
  - test-generator
  - deploy-helper

Project-only skills (2):
  - test-runner
  - backend-scaffold

Common skills (3):
  - frontend-ui-ux
  - git-master
  - planner

Options:
  [1] Copy user skill to project
  [2] Copy project skill to user
  [3] View differences
  [4] Cancel
```

4. **Handle user choice:**
   - Option 1: Select skill(s) to copy to project
   - Option 2: Select skill(s) to copy to user
   - Option 3: Show side-by-side diff for common skills
   - Option 4: Exit

**Safety:** Never overwrite without confirmation

**Example:**
```
User: /skill sync
Assistant: Found 5 user-only skills and 2 project-only skills.

Copy 'error-handler' from user to project? (yes/no/skip)
User: yes
Assistant: ✓ Copied 'error-handler' to .omg/skills/

Copy 'api-builder' from user to project? (yes/no/skip)
User: skip
...
```

---

### /skill setup

Interactive wizard for setting up and managing local skills (formerly local-skills-setup).

**Behavior:**

#### Step 1: Directory Check and Setup

First, check if skill directories exist and create them if needed:

```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot');for(const[label,dir]of [['User',p.join(d,'skills','omc-learned')],['Project',p.join('.omg','skills')]]){if(f.existsSync(dir)){console.log(label+' skills directory exists: '+dir)}else{f.mkdirSync(dir,{recursive:true});console.log('Created '+label.toLowerCase()+' skills directory: '+dir)}}"
```

#### Step 2: Skill Scan and Inventory

Scan both directories and show a comprehensive inventory:

```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot');const walk=dir=>{let out=[];let entries=[];try{entries=f.readdirSync(dir,{withFileTypes:true})}catch{return out};for(const e of entries){const t=p.join(dir,e.name);if(e.isDirectory()){out=out.concat(walk(t))}else if(e.name.endsWith('.md')){out.push(t)}}return out};const first=(text,key)=>{const m=text.split(/\r?\n/).find(l=>l.startsWith(key+':'));return m?m.slice(key.length+1).trim():''};for(const[label,dir]of [['USER-LEVEL SKILLS',p.join(d,'skills','omc-learned')],['PROJECT-LEVEL SKILLS',p.join('.omg','skills')]]){console.log('=== '+label+' ('+dir+') ===');if(f.existsSync(dir)===false){console.log('Directory not found');console.log('');continue}const files=walk(dir);console.log('Total skills: '+files.length);for(const file of files){let text='';try{text=f.readFileSync(file,'utf8')}catch{};const name=first(text,'name')||p.basename(file);const desc=first(text,'description');console.log('  - '+name);if(desc)console.log('    Description: '+desc);console.log('    Modified: '+f.statSync(file).mtime.toISOString())}console.log('')}"

# Summary
TOTAL=$((USER_COUNT + PROJECT_COUNT))
echo "=== SUMMARY ==="
echo "Total skills across all directories: $TOTAL"
```

#### Step 3: Quick Actions Menu

After scanning, use the AskUserQuestion tool to offer these options:

**Question:** "What would you like to do with your local skills?"

**Options:**
1. **Add new skill** - Start the skill creation wizard (invoke `/skill add`)
2. **List all skills with details** - Show comprehensive skill inventory (invoke `/skill list`)
3. **Scan conversation for patterns** - Analyze current conversation for skill-worthy patterns
4. **Import skill** - Import a skill from URL or paste content
5. **Done** - Exit the wizard

**Option 3: Scan Conversation for Patterns**

Analyze the current conversation context to identify potential skill-worthy patterns. Look for:
- Recent debugging sessions with non-obvious solutions
- Tricky bugs that required investigation
- Codebase-specific workarounds discovered
- Error patterns that took time to resolve

Report findings and ask if user wants to extract any as skills (invoke `/skillify`; `/learner` is deprecated compatibility).

**Option 4: Import Skill**

Ask user to provide either:
- **URL**: Download skill from a URL (e.g., GitHub gist)
- **Paste content**: Paste skill markdown content directly

Then ask for scope:
- **User-level** (~/.claude/skills/omc-learned/) - Available across all projects
- **Project-level** (.omg/skills/) - Only for this project

Validate the skill format and save to the chosen location.

---

### /skill scan

Quick command to scan both skill directories (subset of `/skill setup`).

**Behavior:**
Run the scan from Step 2 of `/skill setup` without the interactive wizard.

---

## Skill Templates

When creating skills via `/skill add` or `/skill setup`, offer quick templates for common skill types:

### Error Solution Template

```markdown
---
id: error-[unique-id]
name: [Error Name]
description: Solution for [specific error in specific context]
source: conversation
triggers: ["error message fragment", "file path", "symptom"]
quality: high
---

# [Error Name]

## The Insight
What is the underlying cause of this error? What principle did you discover?

## Why This Matters
What goes wrong if you don't know this? What symptom led here?

## Recognition Pattern
How do you know when this applies? What are the signs?
- Error message: "[exact error]"
- File: [specific file path]
- Context: [when does this occur]

## The Approach
Step-by-step solution:
1. [Specific action with file/line reference]
2. [Specific action with file/line reference]
3. [Verification step]

## Example
\`\`\`typescript
// Before (broken)
[problematic code]

// After (fixed)
[corrected code]
\`\`\`
```

### Workflow Skill Template

```markdown
---
id: workflow-[unique-id]
name: [Workflow Name]
description: Process for [specific task in this codebase]
source: conversation
triggers: ["task description", "file pattern", "goal keyword"]
quality: high
---

# [Workflow Name]

## The Insight
What makes this workflow different from the obvious approach?

## Why This Matters
What fails if you don't follow this process?

## Recognition Pattern
When should you use this workflow?
- Task type: [specific task]
- Files involved: [specific patterns]
- Indicators: [how to recognize]

## The Approach
1. [Step with specific commands/files]
2. [Step with specific commands/files]
3. [Verification]

## Gotchas
- [Common mistake and how to avoid it]
- [Edge case and how to handle it]
```

### Code Pattern Template

```markdown
---
id: pattern-[unique-id]
name: [Pattern Name]
description: Pattern for [specific use case in this codebase]
source: conversation
triggers: ["code pattern", "file type", "problem domain"]
quality: high
---

# [Pattern Name]

## The Insight
What's the key principle behind this pattern?

## Why This Matters
What problems does this pattern solve in THIS codebase?

## Recognition Pattern
When do you apply this pattern?
- File types: [specific files]
- Problem: [specific problem]
- Context: [codebase-specific context]

## The Approach
Decision-making heuristic, not just code:
1. [Principle-based step]
2. [Principle-based step]

## Example
\`\`\`typescript
[Illustrative example showing the principle]
\`\`\`

## Anti-Pattern
What NOT to do and why:
\`\`\`typescript
[Common mistake to avoid]
\`\`\`
```

### Integration Skill Template

```markdown
---
id: integration-[unique-id]
name: [Integration Name]
description: How [system A] integrates with [system B] in this codebase
source: conversation
triggers: ["system name", "integration point", "config file"]
quality: high
---

# [Integration Name]

## The Insight
What's non-obvious about how these systems connect?

## Why This Matters
What breaks if you don't understand this integration?

## Recognition Pattern
When are you working with this integration?
- Files: [specific integration files]
- Config: [specific config locations]
- Symptoms: [what indicates integration issues]

## The Approach
How to work with this integration correctly:
1. [Configuration step with file paths]
2. [Setup step with specific details]
3. [Verification step]

## Gotchas
- [Integration-specific pitfall #1]
- [Integration-specific pitfall #2]
```

---

## Error Handling

**All commands must handle:**
- File/directory doesn't exist
- Permission errors
- Invalid YAML frontmatter
- Duplicate skill names
- Invalid skill names (spaces, special chars)

**Error format:**
```
✗ Error: <clear message>
→ Suggestion: <helpful next step>
```

---

## Usage Examples

```bash
# List all skills
/skill list

# Create a new skill
/skill add my-custom-skill

# Remove a skill
/skill remove old-skill

# Edit existing skill
/skill edit error-handler

# Search for skills
/skill search typescript error

# Get detailed info
/skill info my-custom-skill

# Sync between scopes
/skill sync

# Run setup wizard
/skill setup

# Quick scan
/skill scan
```

## Usage Modes

### Direct Command Mode

When invoked with an argument, skip the interactive wizard:

- `/oh-my-copilot:skill list` - Show detailed skill inventory
- `/oh-my-copilot:skill add` - Start skill creation (invoke skillify)
- `/oh-my-copilot:skill scan` - Scan both skill directories

### Interactive Mode

When invoked without arguments, run the full guided wizard.

---

## Benefits of Local Skills

**Automatic Application**: Claude detects triggers and applies skills automatically - no need to remember or search for solutions.

**Version Control**: Project-level skills (`.omg/skills/`) are intended to be committed with your code so the whole team benefits. In linked worktrees, uncommitted skills remain local to that worktree and disappear if it is removed.

**Evolving Knowledge**: Skills improve over time as you discover better approaches and refine triggers.

**Reduced Token Usage**: Instead of re-solving the same problems, Claude applies known patterns efficiently.

**Codebase Memory**: Preserves institutional knowledge that would otherwise be lost in conversation history.

---

## Skill Quality Guidelines

Good skills are:

1. **Non-Googleable** - Can't easily find via search
   - BAD: "How to read files in TypeScript"
   - GOOD: "This codebase uses custom path resolution requiring fileURLToPath"

2. **Context-Specific** - References actual files/errors from THIS codebase
   - BAD: "Use try/catch for error handling"
   - GOOD: "The aiohttp proxy in server.py:42 crashes on ClientDisconnectedError"

3. **Actionable with Precision** - Tells exactly WHAT to do and WHERE
   - BAD: "Handle edge cases"
   - GOOD: "When seeing 'Cannot find module' in dist/, check tsconfig.json moduleResolution"

4. **Hard-Won** - Required significant debugging effort
   - BAD: Generic programming patterns
   - GOOD: "Race condition in worker.ts - Promise.all at line 89 needs await"

---

## Related Skills

- `/oh-my-copilot:skillify` - Extract a skill from current conversation (`/oh-my-copilot:learner` is a deprecated alias)
- `/oh-my-copilot:note` - Save quick notes (less formal than skills)
- `/oh-my-copilot:deepinit` - Generate AGENTS.md codebase hierarchy

---

## Example Session

```
> /oh-my-copilot:skill list

Checking skill directories...
✓ User skills directory exists: ~/.claude/skills/omc-learned/
✓ Project skills directory exists: .omg/skills/

Scanning for skills...

=== USER-LEVEL SKILLS ===
Total skills: 3
  - async-network-error-handling
    Description: Pattern for handling independent I/O failures in async network code
    Modified: 2026-01-20 14:32:15

  - esm-path-resolution
    Description: Custom path resolution in ESM requiring fileURLToPath
    Modified: 2026-01-19 09:15:42

=== PROJECT-LEVEL SKILLS ===
Total skills: 5
  - session-timeout-fix
    Description: Fix for sessionId undefined after restart in session.ts
    Modified: 2026-01-22 16:45:23

  - build-cache-invalidation
    Description: When to clear TypeScript build cache to fix phantom errors
    Modified: 2026-01-21 11:28:37

=== SUMMARY ===
Total skills: 8

What would you like to do?
1. Add new skill
2. List all skills with details
3. Scan conversation for patterns
4. Import skill
5. Done
```

---

## Tips for Users

- Run `/oh-my-copilot:skill list` periodically to review your skill library
- After solving a tricky bug, immediately run skillify to capture it
- Use project-level skills for codebase-specific knowledge
- Use user-level skills for general patterns that apply everywhere
- Review and refine triggers over time to improve matching accuracy

---

## Implementation Notes

1. **YAML Parsing:** Use frontmatter extraction for metadata
2. **File Operations:** Use Read/Write tools, never Edit for new files
3. **User Confirmation:** Always confirm destructive operations
4. **Clear Feedback:** Use checkmarks (✓), crosses (✗), arrows (→) for clarity
5. **Scope Resolution:** Always check both user and project scopes
6. **Validation:** Enforce naming conventions (lowercase, hyphens only)

---

## Related Skills

- `/oh-my-copilot:skillify` - Extract a skill from current conversation (`/oh-my-copilot:learner` is a deprecated alias)
- `/oh-my-copilot:note` - Save quick notes (less formal than skills)
- `/oh-my-copilot:deepinit` - Generate AGENTS.md codebase hierarchy

---

## Future Enhancements

- `/skill export <name>` - Export skill as shareable file
- `/skill import <file>` - Import skill from file
- `/skill stats` - Show usage statistics across all skills
- `/skill validate` - Check all skills for format errors
- `/skill template <type>` - Create from predefined templates
