---
name: sync-claude-md
description: Synchronize project CLAUDE.md with recent codebase changes by analyzing git history, reviewing against official Anthropic best practices using parallel agents, and proposing comprehensive updates. Use when CLAUDE.md is outdated or doesn't exist.
license: Complete terms in LICENSE.txt
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebFetch
  - Task
  - AskUserQuestion
  - Glob
  - Grep
---

# Sync CLAUDE.md

## Overview

This skill keeps project-level CLAUDE.md files synchronized with codebase evolution. It analyzes git history since the last CLAUDE.md update, spawns 3 parallel review agents to validate against official Anthropic documentation, and proposes comprehensive changes with user approval before applying.

**When to use:**
- CLAUDE.md hasn't been updated in many commits
- Major architectural changes occurred (new libraries, patterns, tools)
- CLAUDE.md doesn't exist and needs to be created
- User explicitly requests: `/sync-claude-md`

## Workflow Decision Tree

```
START: /sync-claude-md invoked
│
├─ CLAUDE.md exists? (check ./CLAUDE.md or ./.claude/CLAUDE.md)
│  │
│  ├─ YES → Go to "Update Existing CLAUDE.md" workflow
│  │
│  └─ NO → Go to "Create New CLAUDE.md" workflow
│
END
```

## Update Existing CLAUDE.md Workflow

### Phase 1: Discovery & Context Analysis

**Step 1.1: Locate CLAUDE.md**
- Check for `./CLAUDE.md` (preferred)
- Check for `./.claude/CLAUDE.md` (alternative)
- If both exist: warn user, prefer `./CLAUDE.md`

**Step 1.2: Find Last Update**
```bash
# Find when CLAUDE.md was last modified
git log --follow --format="%H" -1 -- CLAUDE.md

# Count commits since that update
git rev-list --count <last_commit>..HEAD
```

**Step 1.3: Determine Context Gathering Strategy**
- If commit count > 10: Use heavy analysis (subagents for context)
- If commit count ≤ 10: Direct analysis (read commits directly)

### Phase 2: Context Gathering

**When >10 commits since update:**
1. Read all commit messages between last update and HEAD:
   ```bash
   git log --oneline <last_commit>..HEAD
   ```
2. Identify major changes (library migrations, new tools, architecture shifts)
3. If changes are complex, spawn subagent(s) to analyze specific areas:
   ```
   Task: "Analyze the Effect.ts migration in commits X-Y and summarize
   what documentation changes are needed for CLAUDE.md"
   ```
4. Summarize findings concisely to preserve context window

**When ≤10 commits since update:**
1. Read commit messages directly
2. Optionally read `git show --stat <commit>` for key commits
3. Identify what changed (new commands, libraries, patterns, files)

### Phase 3: Parallel Agent Review

Spawn 3 parallel agents (sonnet model) with identical instructions:

**Agent Prompt:**
```
Review the project CLAUDE.md file and tell me if it follows best practices.
You must read official docs about CLAUDE.md on the official Anthropic website
before reviewing our CLAUDE.md. Then report to me.

Focus on:
- Does it contain technical guidance (commands, code style, testing)?
- Are architectural patterns documented?
- Is it concise and actionable?
- Does it follow the official structure recommendations?

Report:
1. What aligns with best practices
2. What's missing or incorrect
3. Specific recommendations
```

**Execute in parallel:**
```typescript
Task(agent1, prompt)
Task(agent2, prompt)
Task(agent3, prompt)
```

Wait for all 3 agents to complete, then collect reports.

### Phase 4: Master Analysis

**Step 4.1: Read Official Documentation**
Fetch Anthropic's official CLAUDE.md documentation:
```
WebFetch("https://code.claude.com/docs/en/memory.md",
  "Extract all information about CLAUDE.md files: structure, content, best practices")
```

**Step 4.2: Cross-Reference Findings**
- Compare 3 agent reports (look for consensus)
- Validate against official docs
- Identify gaps based on commit context from Phase 2

**Step 4.3: Analyze Current vs Required**
Compare current CLAUDE.md sections against:
- Recent changes (from Phase 2 context)
- Agent findings (from Phase 3)
- Official best practices (from Step 4.1)

**Step 4.4: Generate Comprehensive Proposal**
Create detailed change proposal with:
- **Summary**: What needs updating and why
- **Sections to Add**: New sections with exact content
- **Sections to Modify**: Specific changes to existing sections
- **Sections to Remove**: Outdated content to delete
- **Rationale**: Why each change aligns with best practices

Format proposal as markdown with clear sections.

### Phase 5: User Approval Gate

**Present proposal to user:**
```markdown
## Proposed Changes to CLAUDE.md

### Summary
[Brief overview of what will change]

### Changes

#### 1. Add Section: "Effect.ts Integration"
**Rationale:** Recent migration to Effect.ts (commits abc-xyz) not documented
**Content:**
```
[Show exact content to be added]
```

#### 2. Update Section: "Development Commands"
**Rationale:** Biome linter added but not documented
**Changes:**
- Add: `bun run lint`
- Add: `bun run check`
[etc...]

[Continue for all changes...]
```

**Ask user:**
```
Apply these changes to CLAUDE.md? (yes/no)
```

**Wait for user response.**

### Phase 6: Application

**If user approves:**
1. Apply all proposed changes to CLAUDE.md file
2. Use Edit tool for modifications, Write tool if complete rewrite needed
3. Confirm changes applied successfully
4. **DO NOT** commit to git (let user commit manually)
5. Display summary:
   ```
   ✅ CLAUDE.md updated successfully

   Changes applied:
   - Added 3 new sections
   - Updated 2 existing sections
   - Removed 1 outdated section

   Next step: Review changes and commit when ready
   ```

**If user rejects:**
1. Explain what was not applied
2. Offer to save proposal to file for later reference
3. End workflow

---

## Create New CLAUDE.md Workflow

### Phase 1: Project Analysis

**Step 1.1: Detect Project Type**
Read project files to understand technology stack:
- `package.json` → Node/Bun project, identify runtime & dependencies
- `tsconfig.json` → TypeScript configuration
- `Cargo.toml` → Rust project
- `pyproject.toml` / `requirements.txt` → Python project
- `.github/workflows/` → CI/CD presence
- `docker-compose.yml` → Docker usage

**Step 1.2: Identify Key Patterns**
Look for:
- Testing framework (Jest, Bun test, pytest, etc.)
- Linting/formatting (Biome, ESLint, Prettier, Black, etc.)
- Build tools (Vite, webpack, cargo, etc.)
- Effect management (Effect.ts, neverthrow, Result types, etc.)
- Architecture patterns (docs/, src/ structure)

### Phase 2: Fetch Official Guidance

**Fetch Anthropic Documentation:**
```
WebFetch("https://code.claude.com/docs/en/memory.md",
  "Extract best practices for creating new CLAUDE.md files:
   structure, required sections, examples")
```

### Phase 3: Generate Initial CLAUDE.md

**Ask user for approach:**
```
CLAUDE.md doesn't exist. Generate:
1. Minimal starter template (basic structure, fill in later)
2. Comprehensive CLAUDE.md (full analysis of your project)

Choose option (1 or 2):
```

**Option 1: Minimal Template**
Generate basic structure:
```markdown
# CLAUDE.md

## Project Overview
[Project name] - [Brief description]

**Runtime**: [Detected runtime]
**Language**: [Detected language]

## Development Commands

```bash
# Install dependencies
[detected package manager] install

# Run tests
[detected test command]

# Run linter
[detected lint command]
```

## Architecture
[To be documented]

## Important Notes
- [Add project-specific notes]
```

**Option 2: Comprehensive Analysis**
1. Analyze entire project structure
2. Read key configuration files
3. Identify all development commands
4. Document architectural patterns found
5. List important notes (env vars, special setup, etc.)
6. Generate complete CLAUDE.md following official structure

### Phase 4: Present to User

Show generated CLAUDE.md in full:
```markdown
## Proposed CLAUDE.md

[Show complete content]

---
Create this file? (yes/no)
```

### Phase 5: Create File

**If user approves:**
1. Create `./CLAUDE.md` (preferred location)
2. Confirm creation
3. Suggest next steps:
   ```
   ✅ CLAUDE.md created successfully

   Next steps:
   1. Review and customize content
   2. Add project-specific patterns
   3. Commit to repository for team sharing
   ```

**If user rejects:**
1. Offer to save draft to different location
2. End workflow

---

## Context Window Management

**Conservative Approach:**
- Monitor context usage throughout workflow
- If >150k tokens used: summarize findings before continuing
- Prioritize essential information over exhaustive detail
- Use subagents to offload heavy analysis when needed

**Summarization Triggers:**
- After gathering >10 commits context
- After collecting 3 agent reports
- Before final proposal generation

**Bailout Conditions:**
- If approaching 180k tokens: warn user and offer abbreviated workflow
- Always prefer completing workflow with summaries over incomplete execution

---

## Error Handling

**CLAUDE.md not found and not in git repo:**
- Detect via `git rev-parse --is-inside-work-tree`
- Inform user: "Not a git repository. CLAUDE.md is most useful in version-controlled projects."
- Offer to create anyway or exit

**Both ./CLAUDE.md and ./.claude/CLAUDE.md exist:**
- Warn user about duplicate
- Recommend consolidating to `./CLAUDE.md`
- Ask which to update or if both should be synced

**Official docs unreachable:**
- Retry WebFetch once with 10s timeout
- If still fails: use embedded best practices knowledge
- Warn user that official docs weren't consulted

**Agent failures:**
- If 1 agent fails: continue with 2 agent reports
- If 2+ agents fail: abort parallel review, do direct review instead
- Always inform user of failures

---

## Best Practices

**DO:**
- Always fetch latest official Anthropic documentation
- Give users full visibility into proposed changes before applying
- Preserve existing good content in CLAUDE.md
- Focus on actionable, technical guidance over vague descriptions
- Keep proposals concise with clear rationale

**DON'T:**
- Never auto-commit changes (user commits manually)
- Don't break context window with excessive detail
- Don't skip user approval gate
- Don't remove content without understanding its purpose
- Don't generate vague or generic documentation

---

## Example Usage

**Scenario 1: CLAUDE.md outdated after major refactor**
```
User: /sync-claude-md

[Skill detects 15 commits since last update]
[Analyzes commits, spawns 3 agents, fetches official docs]
[Proposes adding Effect.ts section, updating commands, adding security section]

Skill: "Apply these changes to CLAUDE.md? (yes/no)"
User: yes

[Changes applied, user commits manually]
```

**Scenario 2: No CLAUDE.md exists**
```
User: /sync-claude-md

Skill: "CLAUDE.md doesn't exist. Generate:
1. Minimal starter template
2. Comprehensive CLAUDE.md
Choose option (1 or 2):"

User: 2

[Analyzes project, generates comprehensive CLAUDE.md]
[Shows preview]

Skill: "Create this file? (yes/no)"
User: yes

[File created, user reviews and commits]
```

**Scenario 3: Recent update, minor changes needed**
```
User: /sync-claude-md

[Skill detects 3 commits since last update]
[Reads commits directly, spawns agents, reviews]

Skill: "CLAUDE.md is mostly up to date. Proposed changes:
- Add 1 new command: 'bun run format'
- Update Important Notes with new library

Apply? (yes/no)"
User: yes

[Changes applied]
```
