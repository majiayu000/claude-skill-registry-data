---
name: setup-remote-repo-notes-dir
description: Create a structured notes directory for studying and documenting remote GitHub repositories. Use this skill when the user wants to set up a workspace for researching, analyzing, or taking notes on an external GitHub repository. Creates separate committed notes/ directory and gitignored code/ directory.
---

# Setup Remote Repository Notes Directory

## Overview

Facilitate studying and documenting remote GitHub repositories by creating a structured workspace with:
- A **notes/** directory for committed markdown documentation
- A **code/** directory for the gitignored cloned repository
- Automatic .gitignore configuration to keep code local while notes stay in version control

## When to Use This Skill

Use this skill when the user:
- Wants to study or analyze an external GitHub repository
- Needs to take notes about a remote codebase
- Wants to document findings from exploring another project
- Requests to "set up notes for a repo" or similar phrasing
- Provides a GitHub URL and mentions research, study, or documentation

**Example requests:**
- "Help me set up notes for studying https://github.com/anthropics/claude-code"
- "I want to research this repo: https://github.com/facebook/react"
- "Create a workspace for analyzing https://github.com/rust-lang/rust"

## Directory Structure

The skill creates the following structure:

```
reference/repo/<github-org-or-user>/<reponame>/
├── notes/          # Committed - contains markdown notes about the repo
│   └── README.md   # Initial note file with repo metadata
└── code/           # Gitignored - contains the cloned repository
    └── ...         # Contents of the cloned repo
```

**Design rationale:**
- **notes/** stays in version control → persistent documentation
- **code/** is gitignored → can be deleted/re-cloned without affecting notes
- **Hierarchical organization** → supports multiple repos from same org

## Git Worktree Compatibility

**New in v2:** The skill is now worktree-aware and optimizes for git worktree workflows.

### Behavior

**When invoked from a git worktree** (e.g., `/workspace/wip/username-123-feature`):
- ✅ **Code cloned to root**: `/workspace/reference/repo/<org>/<repo>/code/` (shared)
- ✅ **Notes in worktree**: `/workspace/wip/username-123-feature/reference/repo/<org>/<repo>/notes/` (local)

**When invoked from root** (`/workspace`):
- ✅ **Both in root**: `/workspace/reference/repo/<org>/<repo>/` (current behavior)

### Benefits

**Shared code directory:**
- Saves disk space (no duplicate clones per worktree)
- Reference repos persist after worktree deletion
- Single clone shared across all worktrees

**Worktree-local notes:**
- Notes can be committed with branch work
- Different branches can have different notes
- Follows git-worktrees best practice of keeping worktrees clean

### Example

```bash
# From worktree
cd /workspace/wip/codekiln-173-fix-skill
.claude/skills/setup-remote-repo-notes-dir/scripts/setup_repo_notes.sh https://github.com/anthropics/claude-code

# Result:
# Code:  /workspace/reference/repo/anthropics/claude-code/code/ (shared)
# Notes: /workspace/wip/codekiln-173-fix-skill/reference/repo/anthropics/claude-code/notes/ (local)

# From another worktree
cd /workspace/wip/codekiln-180-another-feature
.claude/skills/setup-remote-repo-notes-dir/scripts/setup_repo_notes.sh https://github.com/anthropics/claude-code

# Result:
# Code:  /workspace/reference/repo/anthropics/claude-code/code/ (reused!)
# Notes: /workspace/wip/codekiln-180-another-feature/reference/repo/anthropics/claude-code/notes/ (new)
```

## Usage

### Quick Start

Use the bundled bash script to set up the structure automatically:

```bash
.claude/skills/setup-remote-repo-notes-dir/scripts/setup_repo_notes.sh <github-url>
```

**Example:**
```bash
.claude/skills/setup-remote-repo-notes-dir/scripts/setup_repo_notes.sh https://github.com/anthropics/claude-code
```

### What the Script Does

1. **Parses the GitHub URL** to extract org/user and repository name
2. **Creates directory structure** under `reference/repo/<org>/<repo>/`
3. **Clones the repository** into the `code/` subdirectory
4. **Creates initial notes/README.md** with:
   - Repository name and URL
   - Date created
   - Purpose/description placeholder
   - Sections for findings, architecture, and notes
5. **Updates .gitignore** to exclude `reference/repo/**/code/` directories
6. **Provides next steps** for the user

### Supported GitHub URL Formats

The script accepts multiple GitHub URL formats:
- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `git@github.com:owner/repo.git`

### Manual Setup (Alternative)

For custom setups or when the script cannot be used, manually perform these steps:

1. **Parse the GitHub URL** to extract `<org>` and `<repo>`
2. **Create directories:**
   ```bash
   mkdir -p reference/repo/<org>/<repo>/notes
   mkdir -p reference/repo/<org>/<repo>/code
   ```
3. **Clone the repository:**
   ```bash
   git clone <github-url> reference/repo/<org>/<repo>/code
   ```
4. **Create initial notes/README.md** with repository metadata
5. **Update .gitignore** to add `reference/repo/**/code/`

## Workflow After Setup

After running the setup:

1. **Explore the cloned code:**
   ```bash
   cd reference/repo/<org>/<repo>/code
   # Read files, run the project, analyze structure
   ```

2. **Document findings in notes:**
   ```bash
   # Edit notes/README.md or create additional markdown files
   cd reference/repo/<org>/<repo>/notes
   ```

3. **Commit notes to version control:**
   ```bash
   git add reference/repo/<org>/<repo>/notes
   git commit -m "📚 docs: add notes for <org>/<repo>"
   ```

4. **Code directory remains gitignored** - can delete and re-clone anytime

## Benefits

- **Separation of concerns**: Notes (committed) vs code (local)
- **Consistent organization**: Standard location for all remote repo research
- **Version-controlled documentation**: Notes persist across machines
- **Flexibility**: Code can be deleted/updated without affecting notes
- **Multi-repo support**: Easy to manage multiple repositories

## Examples

### Example 1: Studying Claude Code

```bash
.claude/skills/setup-remote-repo-notes-dir/scripts/setup_repo_notes.sh https://github.com/anthropics/claude-code
```

**Result:**
```
reference/repo/anthropics/claude-code/
├── notes/
│   └── README.md    # "# claude-code" with metadata
└── code/            # Full clone of anthropics/claude-code
```

### Example 2: Researching React

```bash
.claude/skills/setup-remote-repo-notes-dir/scripts/setup_repo_notes.sh https://github.com/facebook/react
```

**Result:**
```
reference/repo/facebook/react/
├── notes/
│   └── README.md    # "# react" with metadata
└── code/            # Full clone of facebook/react
```

## Script Reference

### Location
`scripts/setup_repo_notes.sh`

### Usage
```bash
./setup_repo_notes.sh <github-url>
```

### Exit Codes
- `0` - Success
- `1` - Error (invalid URL, clone failure, etc.)

### Output
- Colored status messages (info, success, warnings, errors)
- Summary of created structure
- Next steps for the user

### Idempotency
- Safe to run multiple times on the same repository
- Existing files are preserved with warnings
- Git pull performed if repository already cloned

## Troubleshooting

**"Invalid GitHub URL format"**
- Ensure URL is in format: `https://github.com/owner/repo`
- Check for typos in the URL

**"Repository already cloned"**
- Script will pull latest changes instead of re-cloning
- Existing notes are preserved

**".gitignore already contains pattern"**
- Pattern already exists, no action needed
- Setup continues normally

**Clone fails with authentication error**
- Ensure you have access to the repository
- For private repos, use SSH URL: `git@github.com:owner/repo.git`
- Check GitHub credentials and SSH keys

## Integration with Other Skills

This skill complements:
- **example-skills:skill-creator** - For creating skills based on studied repos
- **example-skills:mcp-builder** - When studying MCP servers for reference

## Notes

- The `code/` directory is fully gitignored and can be safely deleted
- Notes directory can contain multiple markdown files, not just README.md
- Subdirectories can be created within `notes/` for organization
- Consider committing notes after each research session
- The script is idempotent - safe to run multiple times
