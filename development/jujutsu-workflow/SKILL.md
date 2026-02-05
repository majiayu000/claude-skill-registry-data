---
name: jujutsu-workflow
description: Comprehensive guide to jujutsu (jj) workflow, distinguishing it from
  git, with step-by-step instructions for initializing repositories, describing
  commits with conventional format, rebasing, managing history, and using
  jujutsu safely. Use jj describe, jj new, jj status, and other jujutsu commands
  when working in jujutsu-enabled repositories.
license: Apache-2.0
compatibility: Requires jujutsu (jj) command-line tool and git
  compatibility layer
metadata:
  author: vdesjardins
  version: "1.0"
---

# Jujutsu Commits

Guide for creating well-formatted conventional commit messages and best
practices when working with jujutsu repositories.

## ⚠️ Critical: Jujutsu Repositories Only

**This skill is exclusively for repositories using jujutsu as the source
control management system.**

### Do Not Mix Git and Jujutsu

Never run git commands in a jujutsu-enabled repository. This can corrupt
repository state and cause data loss. If a repository has jujutsu enabled,
all source control operations must use jujutsu commands exclusively.

**Forbidden commands in jujutsu repos:**

- ❌ `git commit` (use `jj describe -m` instead)
- ❌ `git add` (jujutsu tracks all changes automatically)
- ❌ `git push` (use `jj git push` instead)
- ❌ `git pull` (use `jj git fetch` + `jj rebase` instead)
- ❌ `git branch` (use `jj bookmark` instead)
- ❌ `git merge` (use `jj rebase` instead)
- ❌ Any other `git` command

### Detecting Jujutsu-Enabled Repositories

Before using this skill, verify the repository is jujutsu-enabled:

**Check if jujutsu is enabled:**

```bash
# Jujutsu-enabled repos have a .jj directory
ls -la .jj

# Or try running jujutsu commands
jj status
```

If either succeeds, the repository is jujutsu-enabled. If you get an error
like "not a jujutsu repository", follow the initialization steps below.

### Initializing Jujutsu for Existing Git Repositories

If a repository currently uses git and you want to enable jujutsu:

```bash
# Initialize jujutsu in the current directory
jj git init

# This creates a .jj directory and sets up jujutsu
# Jujutsu can wrap the existing git repository, preserving all history
```

After initialization:

- Verify with `jj status` to confirm jujutsu is working
- You can now use all `jj` commands
- The `.jj` directory should be visible: `ls -la .jj`
- You should NOT use git commands anymore for this repository

**Note:** Jujutsu's git integration allows it to work alongside git while
managing the repository. Once jujutsu is initialized, treat it as your
primary SCM for this repository.

## Conventional Commit Format

All commit messages in this repository follow the conventional commits
specification with emoji prefixes for visual clarity.

### Commit Types

Each commit type has a corresponding emoji that must appear at the start of
the message:

| Type | Emoji | Description |
|------|-------|-------------|
| feat | ✨ | New features |
| fix | 🐛 | Bug fixes |
| docs | 📝 | Documentation changes |
| refactor | ♻️ | Code restructuring without changing |

  functionality |
| style | 🎨 | Code formatting, missing semicolons, etc. |
| perf | ⚡️ | Performance improvements |
| test | ✅ | Adding or correcting tests |
| chore | 🧑‍💻 | Tooling, configuration, maintenance |
| wip | 🚧 | Work in progress |
| remove | 🔥 | Removing code or files |
| hotfix | 🚑 | Critical fixes |
| security | 🔒 | Security improvements |

### Message Format

```text
<emoji> <type>(<scope>): <description>

[optional body explaining why, not what]

[optional footer with references]
```

**Examples:**

- `✨ feat(auth): add two-factor authentication support`
- `🐛 fix(api): resolve race condition in request handler`
- `♻️ refactor(parser): simplify token parsing logic`
- `📝 docs(readme): update installation instructions`

## Jujutsu Workflow

### Understanding Jujutsu Basics

Unlike git, jujutsu has some fundamental differences:

1. **No Staging Area** - All changes in your working directory are
   automatically tracked
2. **Working Copy is a Commit** - Your current state is always part of a
   commit
3. **Safe History Rewriting** - You can rewrite history without fear using
   `jj undo`
4. **Bookmarks, Not Branches** - Use bookmarks to track important commits
5. **Immutable Commits** - Commits cannot be modified; rewrites create new
   commits

#### Change-ID vs Commit-ID

Unlike git, jujutsu uses `change-id` to track logical changes across
rewrites. When you rewrite history, a new commit-id is generated, but the
`change-id` remains the same. This is what makes `jj undo` safe and history
rewriting worry-free. In command examples, use the `change-id` (e.g.,
`abc123def`) or shorthand references like `@` (current), `@-` (parent),
or `@-` followed by other revset syntax.

### Pre-Flight Checks

Before using any jujutsu workflow, always verify:

1. **Repository is jujutsu-enabled:**

   ```bash
   jj status
   ```

   If this fails with "not a jujutsu repository", the repo needs
   initialization (see "Initializing Jujutsu for Existing Git Repositories"
   above).

2. **You're in the correct directory:**

   ```bash
   pwd
   ```

   Verify you're at the repository root where `.jj` directory exists.

3. **Your environment has jujutsu installed:**

   ```bash
   jj --version
   ```

   Should display the jujutsu version.

If any of these checks fail, address the issue before proceeding with commit
operations.

### Creating and Describing Commits

#### Step 1: Check Current Status

Start by reviewing what changes exist in the working copy:

```bash
jj status
```

This shows the current commit, its message, and what files have changed.

#### Using INTENTS Files and jj diff Together

When you make changes using OpenCode or other tools, they may create
`INTENTS-*.md` files that document the original intent behind the changes.
Combine INTENTS files with `jj diff` to capture both the reasoning and all
actual changes:

1. Run `jj status` to check for `INTENTS-*.md` files
2. If INTENTS files exist:
   - Read the file to understand the original prompt/intent
   - Run `jj diff` to see all actual changes in the working copy
   - Cross-reference: The INTENTS file explains WHY, the diff shows WHAT
     changed
   - Account for any manual edits not mentioned in INTENTS (they appear in
     the diff)
   - Write a commit message that captures both the original intent and any
     additional changes
   - Example: INTENTS says "refactor parser" but diff shows you also fixed
     a bug, so message should be: `🐛 fix(parser): refactor for performance
     and fix edge case handling`
3. If no INTENTS files exist:
   - Run `jj diff` to see the actual changes
   - Determine the commit type and write a message based on what changed

This approach ensures your commit messages capture the complete picture: the
original intent plus any additional changes made along the way.

#### Step 2: Create a New Commit (if needed)

To create a new commit with your current changes:

```bash
jj new -m "<emoji> <type>(<scope>): <description>"
```

Or create without a message and describe it after:

```bash
jj new
```

#### Step 3: Set the Commit Message

Describe the current working copy commit with:

```bash
jj describe -m "<emoji> <type>(<scope>): <description>"
```

For interactive editing:

```bash
jj describe
```

#### Step 4: Verify the Change

Review what you've committed:

```bash
jj diff
jj log -r @-  # Show previous commit
```

### Workflow Example: Adding a Feature

```bash
# Ensure you're on the main branch
jj edit main
jj git fetch
jj rebase -d main  # Rebase onto latest main if needed

# Create a new feature commit
jj new -m "✨ feat(parser): add JSON schema validation"

# Make your changes...
# Your changes are automatically tracked in the working copy

# Split into multiple commits if needed
jj split  # Interactive split
# or use jj split -i for interactive mode

# Create a test commit
jj new -m "✅ test(parser): add schema validation tests"

# Add test code...

# Refine commits as needed
jj squash  # Combine with parent commit if needed
jj absorb  # Move changes to matching commits automatically

# Push to remote
jj git push
```

### Common Jujutsu Operations

#### Navigate Commits

```bash
jj next              # Move to next descendant commit
jj prev              # Move to parent commit
jj edit <change-id>  # Switch to a specific commit
```

#### Edit Commits

```bash
jj describe      # Open editor for current commit message and changes
jj absorb        # Automatically move changes to matching commits
jj squash        # Combine current commit with parent
jj split         # Split current commit (interactive)
jj split -i      # Interactive split mode
```

#### Abandon Changes

```bash
jj restore                # Discard all changes in working copy
jj abandon <change-id>    # Delete a commit entirely
```

#### Manage Bookmarks (Lightweight Branches)

```bash
jj bookmark create <name>              # Create a bookmark at current commit
jj bookmark list                       # List all bookmarks
jj bookmark set <name> -r <change-id>  # Move bookmark to a commit
jj bookmark delete <name>              # Remove a bookmark
```

#### Rebase and History

```bash
jj rebase -d main                # Rebase current branch onto main
jj rebase -d <target> -r <src>   # Rebase specific commit
```

#### Remote Operations

```bash
jj git fetch              # Fetch from remote
jj git push               # Push current commit to remote
jj git push -c @          # Push current commit (@ shorthand) -
                          # create a bookmark at the same time
```

### Undo and Safety

Jujutsu's most powerful feature: **you can safely undo anything**.

```bash
jj undo                   # Undo the last jujutsu command
```

This makes experimentation and history rewriting completely safe.

## Pre-Commit Checks

Before creating commits, ensure code quality by running:

```bash
pre-commit run -a
```

This runs linting, formatting, and other checks to catch issues early.

## Best Practices

1. **Write Clear Messages** - Explain the WHY, not just the WHAT
2. **Keep Commits Focused** - Each commit should represent a single logical
   change
3. **Use Imperative Mood** - "add feature" not "added feature"
4. **Reference Issues** - Link to GitHub issues when relevant: "fixes #123"
5. **Small Commits** - Jujutsu makes splitting and combining commits
   easy—use it!
6. **Leverage History Rewriting** - Don't fear rebasing; `jj undo` has your
   back
7. **Use Bookmarks Wisely** - Track important commits with bookmarks instead
   of creating branches
8. **Absorb Frequently** - Use `jj absorb` to automatically organize changes
   across commits

## Troubleshooting

### Accidentally Ran a Git Command?

If you accidentally ran a git command:

```bash
jj undo
```

This reverts the last jujutsu operation, including any git commands run
through jujutsu.

### Need to Undo Multiple Changes?

View the operation history:

```bash
jj op log
```

Then undo to a specific operation:

```bash
jj op revert <operation-id>
```

### Conflicts During Rebase?

Jujutsu handles conflicts gracefully:

```bash
jj status              # See conflicts
jj diff                # Review the conflicting changes
# Edit conflicted files...
jj resolve             # Mark conflicts as resolved
```

## References

- [Jujutsu Official Documentation](https://jujutsu-vcs.github.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Repository Commit Guidelines](../../shell/tools/jujutsu/default.nix)
