---
name: Managing Cross-Repository Configuration
description: Use when user asks where to put configuration, skills, or learnings, or discusses sharing config across projects. Provides decision criteria for the three-tier architecture (global ~/.claude, plugin, project-local .claude) to prevent duplication and ensure reusability. Invoke before creating new skills or configuration to determine the correct tier and location.
---

# Managing Cross-Repository Configuration

When working across multiple repositories (e.g., your marketplace repo, vLLM, llama stack, etc.), you need a clear strategy for where to store configurations, learnings, and skills to ensure consistency without duplication.

## Three-Tier Architecture

Claude Code supports three tiers of configuration, each with specific use cases:

### 1. Global Configuration (`~/.claude/CLAUDE.md`)

**Use for:**
- Personal coding style preferences
- General development patterns you prefer across all projects
- Your personal workflow preferences
- Cross-language, cross-project knowledge
- Tool usage preferences
- Communication style preferences

**Benefits:**
- Automatically available in ALL repositories
- No installation or setup needed
- Single source of truth for personal preferences
- Simplest approach for most user preferences

**Example content:**
```markdown
# Python code style
- Always put imports at the top of the file, not within methods
- Use descriptive variable names over comments

# General preferences
- Prefer Edit tool over Write for existing files
- Keep commit messages concise and action-oriented
```

### 2. Plugin Skills (in marketplace/plugin repos)

**Use for:**
- Domain-specific expertise (e.g., PR review patterns, testing strategies)
- Shareable, reusable capabilities
- Structured knowledge for specific problem domains
- Workflow patterns others might benefit from

**Benefits:**
- Versioned and organized by domain
- Shareable across teams
- Available wherever marketplace is installed
- Can be distributed and maintained separately

**When to use:**
- Creating reusable capabilities for specific domains
- Knowledge that should be version-controlled
- Patterns that could benefit others
- Structured workflows with multiple steps

### 3. Project-Local Configuration (`.claude/CLAUDE.md` in project)

**Use for:**
- This specific codebase's architecture patterns
- Project-specific conventions and decisions
- Team agreements for this repository
- Codebase-specific context

**Benefits:**
- Only applies to this repository
- Can be committed to version control
- Shared across team members
- Won't interfere with other projects

**Example content:**
```markdown
# This Project's Patterns

- Authentication uses JWT tokens stored in httpOnly cookies
- All API routes go through middleware/auth.ts
- Database migrations use Prisma in prisma/migrations/
```

## Decision Framework

When deciding where to store configuration or learnings, ask:

**Is this personal preference?** → Global (`~/.claude/CLAUDE.md`)
- Coding style you prefer
- Your workflow patterns
- How you like tools to be used

**Is this shareable domain knowledge?** → Plugin Skill
- PR review techniques
- Testing strategies
- Deployment patterns
- General best practices

**Is this specific to one codebase?** → Project-Local (`.claude/CLAUDE.md`)
- Where files are located in this repo
- This project's architecture decisions
- Team conventions for this codebase

## Cross-Repository Consistency

To ensure consistency across all repositories:

### For Personal Preferences
Use `~/.claude/CLAUDE.md` exclusively. This automatically applies everywhere you use Claude Code.

### For Domain Knowledge
Create plugin skills in a marketplace repository:
1. Develop skills in your marketplace source repo
2. Version and commit skills
3. Install marketplace globally or per-project
4. Skills available wherever marketplace is installed
5. Update skills in source repo, push changes
6. Other repos get updates when they reload

### For Project-Specific Patterns
Use project-local `.claude/CLAUDE.md` committed to that repository's version control.

## Implementation Pattern: The `/learn` Command

A well-designed `/learn` command should:

1. **Identify the learning type** from the conversation
2. **Ask the user** which tier is appropriate:
   - Global: Personal preferences
   - Plugin Skill: Domain expertise
   - Project-Local: This codebase's patterns
3. **Save accordingly**:
   - Global: Append to `~/.claude/CLAUDE.md`
   - Plugin: Use skill-builder to create/update skill
   - Project: Append to `.claude/CLAUDE.md` in current repo
4. **Confirm** where the learning was saved

This ensures learnings are:
- Scoped appropriately
- Discoverable where needed
- Not duplicated across tiers

## Common Anti-Patterns

**DON'T:**
- Store personal preferences in project-local files (won't follow you)
- Store project-specific patterns globally (pollutes other projects)
- Create plugin skills for one-off project patterns
- Duplicate the same guidance across multiple tiers

**DO:**
- Use the simplest tier that meets your needs
- Default to global for personal preferences
- Use plugins for reusable, shareable knowledge
- Keep project-local truly project-specific

## Validation

To verify your configuration architecture:

1. **Test global application**: Check that `~/.claude/CLAUDE.md` preferences apply in a new, unrelated repository
2. **Test plugin availability**: Verify plugin skills work in projects where the marketplace is installed
3. **Test isolation**: Confirm project-local settings don't leak to other repositories
4. **Check for duplication**: Ensure the same guidance doesn't exist in multiple tiers

## Example Scenario

**Situation:** You learn a better way to write commit messages while working on vLLM.

**Decision process:**
- Is this how YOU prefer all commit messages? → Global
- Is this a general best practice for commit messages? → Plugin Skill
- Is this how vLLM specifically wants commits? → Project-Local

Most likely: **Global** (`~/.claude/CLAUDE.md`) because commit message style is typically a personal preference that should apply everywhere you work.

## Working with Git Worktrees

When frequently context-switching between multiple PRs or bugs, git worktrees provide a better workflow than stashing or multiple clones.

### Why Worktrees?

**Use worktrees when:**
- You need to switch between multiple branches/PRs frequently throughout the day
- You want separate working directories for each branch
- You don't want to stash/commit WIP when context-switching

**Benefits over alternatives:**
- Each worktree is a separate directory with its own branch
- Share the same `.git` repository (saves space vs multiple clones)
- No need to stash/commit when switching contexts
- Claude Code can work independently in each worktree

### Basic Worktree Usage

```bash
# Create worktree for existing branch
git worktree add ../myrepo-feature-x feature-x

# Create worktree with new branch
git worktree add ../myrepo-bugfix -b bugfix/issue-123

# List all worktrees
git worktree list

# Remove worktree when done
git worktree remove ../myrepo-feature-x
```

### Sharing .claude Configuration Across Worktrees

**Scenario 1: Team project where `.claude/` is committed**

No special setup needed! The `.claude/CLAUDE.md` file is in version control, so all worktrees automatically share the same configuration through git.

**Scenario 2: Large OSS project where `.claude/` cannot be committed**

Use symlinks to share your project-local configuration across worktrees:

```bash
# In your main worktree (keep the real .claude directory here)
ls .claude/CLAUDE.md  # Verify it exists

# In each additional worktree
cd ../myrepo-feature-x
rm -rf .claude  # Remove if it exists
ln -s /full/path/to/main-worktree/.claude .claude

# Prevent accidental commits
echo ".claude" >> .git/info/exclude
```

### Automation Script for OSS Projects

Create a script to automate worktree creation with shared `.claude/`:

```bash
#!/bin/bash
# create-worktree.sh
PROJECT_NAME=$(basename $(git rev-parse --show-toplevel))
MAIN_WORKTREE=$(git rev-parse --show-toplevel)
BRANCH=$1
WORKTREE_DIR="../${PROJECT_NAME}-${BRANCH}"

# Create the worktree
git worktree add "$WORKTREE_DIR" -b "$BRANCH"

# Symlink .claude directory
cd "$WORKTREE_DIR"
rm -rf .claude
ln -s "${MAIN_WORKTREE}/.claude" .claude

# Exclude from git
echo ".claude" >> .git/info/exclude

echo "Worktree created at $WORKTREE_DIR with shared .claude config"
```

Usage:
```bash
./create-worktree.sh feature/new-optimization
```

### Worktree Configuration Strategy

With worktrees, your three-tier configuration works seamlessly:

1. **Global** (`~/.claude/CLAUDE.md`)
   - Automatically available in all worktrees
   - No setup needed

2. **Plugin Skills** (from marketplace)
   - Available wherever marketplace is installed
   - Works the same in all worktrees

3. **Project-Local** (`.claude/CLAUDE.md`)
   - **Committed projects**: Shared automatically via git
   - **Uncommitted (OSS)**: Shared via symlinks

### Common Worktree Mistakes

**DON'T:**
- Use multiple full clones (wastes space and creates sync issues)
- Create separate `.claude/` directories in each worktree (causes divergence)
- Forget to symlink `.claude/` in OSS projects

**DO:**
- Use worktrees for frequent context-switching
- Symlink `.claude/` for OSS projects where you can't commit configuration
- Keep one "main" worktree with the real `.claude/` directory
- Add `.claude` to `.git/info/exclude` in OSS projects

## Ensuring Critical Skills Are Always Available

Plugin skills are model-invoked based on description matching. For critical workflow information you want **guaranteed** in every session, use a hybrid approach.

### Hybrid Pattern: Global + Plugin

**When to use:**
- A plugin skill contains critical day-to-day workflow information
- You want core concepts available in every session, every project
- You need detailed guidance available on-demand

**Implementation:**

1. **Brief essentials in global config** (`~/.claude/CLAUDE.md`):
   - Key reminders and principles
   - Quick reference to core concepts
   - Pointer to the detailed skill

2. **Comprehensive details in plugin skill**:
   - Full workflows and examples
   - Decision frameworks
   - Automation scripts
   - Edge cases and anti-patterns

**Example:**

```markdown
# In ~/.claude/CLAUDE.md (always loaded)

# Claude Code Configuration
- Three tiers: Global (~/.claude/CLAUDE.md), Plugin Skills, Project-Local (.claude/CLAUDE.md)
- For detailed guidance, use the cross-repo-config skill

# Git Worktrees for Context-Switching
- Use git worktrees (not multiple clones) for frequent PR/bug switching
- In OSS projects: symlink .claude/ from main worktree
- For automation scripts, use the cross-repo-config skill
```

**Benefits:**
- Global config ensures core concepts are always present ✅
- Skill provides detailed guidance when needed ✅
- Reduces skill file size (progressive disclosure) ✅
- Improves discoverability (explicit skill reference) ✅
- User can quickly reference essentials ✅

**Don't:**
- Duplicate all skill content in global config
- Put project-specific patterns in global config
- Rely solely on skill discoverability for critical workflows

**Do:**
- Keep global config entries brief (1-3 bullets per topic)
- Point to the skill name explicitly for details
- Ensure the skill is globally installed if critical

## Tips for Success

1. **Start with global**: Most personal preferences belong in `~/.claude/CLAUDE.md`
2. **Plugin skills for patterns**: Use when you'd answer "others could benefit from this"
3. **Project-local is rare**: Only truly project-specific architecture belongs here
4. **Review periodically**: Check if project-local settings should be elevated to global
5. **Keep it simple**: Don't over-engineer the tier structure
6. **Use worktrees for context-switching**: Better than stashing or multiple clones
7. **Symlink .claude in OSS projects**: Share configuration across worktrees when you can't commit
8. **Hybrid for critical skills**: Brief in global, detailed in skill, both globally available
