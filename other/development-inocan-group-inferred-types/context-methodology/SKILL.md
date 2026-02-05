---
name: context-methodology
description: Knowledge about the context branch methodology for separating AI configuration from project code using git worktrees. Use when users ask about worktree structure, branch organization, or the separation of concerns pattern.
allowed-tools: Read, Glob, Grep, Bash
---

# Context Branch Methodology

This skill provides knowledge about the **context branch methodology** - a pattern for separating AI assistant configuration from project source code using git worktrees.

## The Problem

When using AI coding assistants like Claude Code, projects accumulate:
- `CLAUDE.md` files with instructions
- `.claude/` directories with settings, commands, agents
- Custom hooks and configurations

These files:
1. Clutter project history with AI-specific commits
2. Mix tooling concerns with business logic
3. Create noise in code reviews
4. May contain sensitive prompts or configurations

## The Solution

Use **two independent git histories** in the same repository:

### Branch Structure

| Branch | Purpose | Contains |
|--------|---------|----------|
| `context` | AI configuration | CLAUDE.md, .claude/, settings |
| `main`/`master` | Project code | Source code, tests, docs |
| `feature/*` | Development | Feature work (descends from main/master) |

### Directory Layout

```
bare-repo/
└── root/
    ├── context/           # context branch worktree
    │   ├── CLAUDE.md      # AI instructions
    │   ├── .claude/       # Commands, agents, skills
    │   ├── .gitignore     # Contains: worktree/**/
    │   └── worktree/      # All code worktrees here
    │       ├── feature/
    │       │   └── my-feature/  # Feature branch worktree
    │       └── fix/
    │           └── bug-123/     # Bugfix branch worktree
    └── main/              # main/master branch (direct access, read-only)
```

### Key Insight

The `context` branch's `.gitignore` contains `worktree/**/`, so:
- Nested worktrees are invisible to context commits
- AI config and code remain in separate histories
- Claude Code runs from `context/`, sees both contexts

## Detecting the Default Branch

Repositories may use either `main` or `master` as their default branch. Always detect it:

```bash
# Method 1: From remote HEAD (most reliable if remote exists)
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'

# Method 2: Check which branch exists locally
git branch -l main master 2>/dev/null | head -1 | tr -d '* '

# Method 3: Combined approach
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || git branch -l main master 2>/dev/null | head -1 | tr -d '* ')
```

## Workflow

### Creating a New Feature

```bash
# From the context worktree
cd root/context

# Detect default branch
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

# Create feature worktree from default branch
git worktree add -b feature/my-feature worktree/feature/my-feature $DEFAULT_BRANCH

# Work in the feature
cd worktree/feature/my-feature
# ... make changes ...

# Commit and push
git add . && git commit -m "feat: add feature"
git push -u origin feature/my-feature

# Create PR targeting default branch
gh pr create --base $DEFAULT_BRANCH
```

### Updating AI Configuration

```bash
# From context worktree (root/context)
# Edit CLAUDE.md or .claude/ files
git add .
git commit -m "context: update AI instructions"
git push origin context
```

## Rules

1. **Never edit `root/main/` or `root/master/` directly** - always use a worktree
2. **All code worktrees inside `worktree/`** - maintains the separation
3. **Feature branches from default branch** - not from `context`
4. **Context branch is orphan** - no shared history with main/master
5. **PRs target default branch** - context changes stay on context branch

## Benefits

- Clean project history (no AI config commits)
- Separate concerns (tooling vs code)
- Team flexibility (share context or keep personal)
- Easy experimentation (modify AI config without affecting code)

## Common Questions

**Q: How does Claude Code see both contexts?**
A: Claude runs from the `context/` directory, which contains both the AI config files AND the `worktree/` folder with code. The parent CLAUDE.md applies to nested directories.

**Q: Can I have multiple context branches?**
A: Yes! You could have `context-personal` and `context-team` for different configurations.

**Q: What if I need different AI config per feature?**
A: Each worktree can have its own `.claude/` that overrides or extends the parent context.

**Q: How do I migrate an existing repo?**
A: Use the `/context-init` command or the `worktree-manager` agent to set up the structure.

**Q: Does it work with both main and master?**
A: Yes! The commands auto-detect the default branch. You can also explicitly specify the base branch as an argument.
