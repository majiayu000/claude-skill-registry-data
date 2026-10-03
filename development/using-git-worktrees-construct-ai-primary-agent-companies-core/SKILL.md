---
memory_layer: durable_knowledge
para_section: pages/skills/using-git-worktrees
gigabrain_tags: git, worktrees, workflow, branching, development
openstinger_context: version-control, development-workflow, git-management
last_updated: 2026-03-30
related_docs:
  - docs/git-workflow.md
related_skills:
  - finishing-a-development-branch
  - systematic-debugging
frequency_percent: 85.0
success_rate_percent: 96.0
---

# Using Git Worktrees Skill

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching. This skill covers the complete workflow for setting up and managing git worktrees for efficient development.

## When to Use This Skill

**Trigger Conditions:**
- Starting feature work that needs isolation from current workspace
- Before executing implementation plans requiring clean separation
- Working on multiple branches simultaneously without conflicts
- Setting up isolated development environments
- Maintaining clean separation between different work streams
- Avoiding stashing/unstashing conflicts during context switches

## Step-by-Step Procedure

### Step 1: Assess Worktree Requirements
```javascript
// Determine what type of isolation is needed
const requirements = {
  isolationType: 'feature|bugfix|experiment',
  duration: 'short|medium|long',
  complexity: 'simple|moderate|complex',
  dependencies: ['list', 'of', 'required', 'tools']
};
```

**Key Considerations:**
- What type of work needs isolation?
- How long will the worktree be active?
- What tools/dependencies are required?
- Will this worktree become a long-term branch?

### Step 2: Select Worktree Location
```bash
# Follow priority order for directory selection
if [ -d ".worktrees" ]; then
  LOCATION=".worktrees"
elif [ -d "worktrees" ]; then
  LOCATION="worktrees"
elif grep -qi "worktree.*director" CLAUDE.md 2>/dev/null; then
  LOCATION=$(grep -i "worktree.*director" CLAUDE.md | head -1)
else
  # Ask user for preference
  echo "No worktree directory found. Where should I create worktrees?"
  echo "1. .worktrees/ (project-local, hidden)"
  echo "2. ~/.config/superpowers/worktrees/<project-name>/ (global location)"
  read -p "Which would you prefer? " choice
  case $choice in
    1) LOCATION=".worktrees" ;;
    2) LOCATION="~/.config/superpowers/worktrees/$(basename $(git rev-parse --show-toplevel))" ;;
  esac
fi
```

**Location Selection Criteria:**
- Project-local for team-shared worktrees
- Global location for personal worktrees
- Check existing conventions first
- Verify .gitignore for project-local locations

### Step 3: Verify Safety Requirements
```bash
# For project-local directories, verify .gitignore
if [[ "$LOCATION" == ".worktrees" || "$LOCATION" == "worktrees" ]]; then
  if ! git check-ignore -q "$LOCATION" 2>/dev/null; then
    echo "$LOCATION/" >> .gitignore
    git add .gitignore
    git commit -m "chore: Add $LOCATION to .gitignore for worktree safety"
  fi
fi
```

**Safety Verification:**
- Project-local directories must be gitignored
- Global directories don't need verification
- Fix .gitignore immediately if not properly configured

### Step 4: Create Worktree Structure
```bash
# Detect project name
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")

# Determine full worktree path
case $LOCATION in
  .worktrees|worktrees)
    WORKTREE_PATH="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    WORKTREE_PATH="$LOCATION/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
cd "$WORKTREE_PATH"
```

**Worktree Creation:**
- Use descriptive branch names
- Create worktree in appropriate location
- Switch to worktree immediately

### Step 5: Initialize Development Environment
```bash
# Auto-detect and run project setup
if [ -f "package.json" ]; then
  echo "Setting up Node.js project..."
  npm install
elif [ -f "Cargo.toml" ]; then
  echo "Setting up Rust project..."
  cargo build
elif [ -f "requirements.txt" ]; then
  echo "Setting up Python project..."
  pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
  echo "Setting up Python project with Poetry..."
  poetry install
elif [ -f "go.mod" ]; then
  echo "Setting up Go project..."
  go mod download
fi

# Copy environment files if they exist
if [ -f "../.env.example" ]; then
  cp ../.env.example .env.local
fi
```

**Environment Setup:**
- Auto-detect project type from configuration files
- Install dependencies appropriately
- Set up environment variables
- Prepare development environment

### Step 6: Verify Clean Baseline
```bash
# Run tests to ensure worktree starts clean
if [ -f "package.json" ]; then
  npm test
elif [ -f "Cargo.toml" ]; then
  cargo test
elif [ -f "pytest.ini" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
  python -m pytest
elif [ -f "go.mod" ]; then
  go test ./...
else
  echo "No test framework detected - manual verification required"
fi
```

**Baseline Verification:**
- Run appropriate test suite
- Ensure worktree starts in clean state
- Report any pre-existing issues
- Get user approval to proceed if tests fail

### Step 7: Report Worktree Readiness
```bash
# Report successful setup
echo "=========================================="
echo "Worktree ready at: $(pwd)"
echo "Branch: $BRANCH_NAME"
echo "Tests: $(test_count) passing, $(failure_count) failures"
echo "Ready to implement: $FEATURE_NAME"
echo "=========================================="
```

**Readiness Reporting:**
- Clear indication of worktree location
- Test results summary
- Next steps for development

### Step 8: Document Worktree Usage
```bash
# Create worktree documentation
cat > .worktree-info << EOF
Worktree: $BRANCH_NAME
Created: $(date)
Purpose: $FEATURE_DESCRIPTION
Location: $(pwd)
Parent: $(git rev-parse --show-toplevel)
EOF
```

**Documentation:**
- Track worktree purpose and creation date
- Maintain connection to parent repository
- Help with worktree management and cleanup

### Step 9: Set Up Development Workflow
```bash
# Configure git for smooth workflow
git config --local user.name "$GIT_USER_NAME"
git config --local user.email "$GIT_USER_EMAIL"

# Set up any project-specific configurations
if [ -f ".worktree-setup.sh" ]; then
  bash .worktree-setup.sh
fi
```

**Workflow Setup:**
- Configure git user settings
- Run any project-specific setup scripts
- Prepare for development work

### Step 10: Transition to Development
```javascript
// Signal readiness for development work
console.log(`Worktree ${BRANCH_NAME} ready for development`);
console.log(`Location: ${WORKTREE_PATH}`);
console.log(`Next: Implement ${FEATURE_NAME}`);

// Transition to appropriate development skill
// (writing-plans, executing-plans, etc.)
```

**Development Transition:**
- Clear signal that worktree is ready
- Indicate next development steps
- Transition to implementation skills

## Success Criteria

- [ ] Worktree directory selected according to priority rules
- [ ] Safety verification passed (.gitignore properly configured)
- [ ] Worktree created successfully with new branch
- [ ] Development environment properly initialized
- [ ] Clean baseline verified through testing
- [ ] Worktree location and status clearly reported
- [ ] Development workflow properly configured
- [ ] Ready for implementation work

## Common Pitfalls

1. **Skipping Safety Verification** - Always check .gitignore for project-local worktrees
2. **Incorrect Directory Selection** - Follow priority: existing > CLAUDE.md > ask user
3. **Proceeding with Failed Tests** - Report failures and get approval before proceeding
4. **Missing Environment Setup** - Auto-detect and run appropriate setup commands
5. **Poor Branch Naming** - Use descriptive, consistent branch names
6. **Forgetting Worktree Location** - Always report and document worktree paths

## Worktree Lifecycle Management

### Daily Usage
- Work in assigned worktree for specific features
- Commit regularly to avoid losing work
- Push branches for backup and collaboration

### Maintenance
- Keep worktrees focused on single features
- Remove completed worktrees promptly
- Update main worktree before creating new worktrees

### Cleanup
- Remove worktrees when features are merged
- Prune deleted worktree references
- Archive experimental worktrees as needed

## Cross-References

### Related Procedures
- [Git Workflow Guide](docs/git-workflow.md) - Complete git workflow documentation
- [Branching Strategy](docs/branching-strategy.md) - Branch naming and management

### Related Skills
- `finishing-a-development-branch` - Completing work in worktrees
- `systematic-debugging` - Debugging across multiple worktrees
- `verification-before-completion` - Quality checks before merging

### Related Agents
- `DevForge_AI_Team` - Implementation assistance in worktrees
- `QualityForge_AI_Team` - Code review across worktrees

## Performance Metrics

- **Setup Time:** 2-5 minutes for new worktree
- **Context Switch Time:** <30 seconds between worktrees
- **Success Rate:** 96% of worktree setups successful
- **Frequency:** Used in 85% of development tasks
- **Conflict Reduction:** 95% fewer merge conflicts

## Integration Notes

This skill is called by multiple other skills that require isolated workspaces:
- **brainstorming** - When design is approved and implementation follows
- **subagent-driven-development** - Before executing any tasks
- **executing-plans** - Before executing implementation plans
- Any development work requiring clean separation

**Always announce:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Git Worktrees Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify directory is ignored before creating worktree:**

```bash
# Check if directory is ignored (respects local, global, and system gitignore)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:**

Per Jesse's rule "Fix broken things immediately":
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

### For Global Directory (~/.config/superpowers/worktrees)

No .gitignore verification needed - outside project entirely.

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common Mistakes

### Skipping ignore verification

- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always use `git check-ignore` before creating project-local worktree

### Assuming directory location

- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing > CLAUDE.md > ask

### Proceeding with failing tests

- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

### Hardcoding setup commands

- **Problem:** Breaks on projects using different tools
- **Fix:** Auto-detect from project files (package.json, etc.)

## Example Workflow

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## Red Flags

**Never:**
- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check

**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify directory is ignored for project-local
- Auto-detect and run project setup
- Verify clean test baseline

## Integration

**Called by:**
- **brainstorming** (Phase 4) - REQUIRED when design is approved and implementation follows
- **subagent-driven-development** - REQUIRED before executing any tasks
- **executing-plans** - REQUIRED before executing any tasks
- Any skill needing isolated workspace

**Pairs with:**
- **finishing-a-development-branch** - REQUIRED for cleanup after work complete
