---
name: create-worktree
description: Creates a new git/jj worktree for development work with proper setup, dependencies, and optional thoughts initialization. Use when user needs to create a new worktree for feature development or bug fixes.
allowed-tools: Bash, AskUserQuestion
---

# Create Worktree

This skill creates a new worktree for development work with proper setup and verification.

## When to Activate

Activate this skill when:
- User needs to create a new worktree for a feature or bug fix
- Starting work on a Linear ticket (ENG-XXXX format)
- Need to work on multiple branches simultaneously
- Want an isolated workspace with its own dependencies

## Process

### 1. Gather Information

Ask the user for:
- Worktree name (or generate a unique one)
- Base branch (or use current branch)
- Whether to initialize thoughts directory (default: yes)

### 2. Create Worktree

**For git users:**
```bash
# Set up variables
WORKTREE_NAME="[name or generated]"
BASE_BRANCH="[base or current branch]"
WORKTREES_BASE="$HOME/wt/[repo-name]"
WORKTREE_PATH="${WORKTREES_BASE}/${WORKTREE_NAME}"

# Verify worktrees base directory exists
if [ ! -d "$WORKTREES_BASE" ]; then
    echo "Creating worktrees directory: $WORKTREES_BASE"
    mkdir -p "$WORKTREES_BASE"
fi

# Check if worktree already exists
if [ -d "$WORKTREE_PATH" ]; then
    echo "Error: Worktree directory already exists: $WORKTREE_PATH"
    exit 1
fi

# Create worktree (creates branch if it doesn't exist)
if git show-ref --verify --quiet "refs/heads/${WORKTREE_NAME}"; then
    echo "Using existing branch: ${WORKTREE_NAME}"
    git worktree add "$WORKTREE_PATH" "$WORKTREE_NAME"
else
    echo "Creating new branch: ${WORKTREE_NAME}"
    git worktree add -b "$WORKTREE_NAME" "$WORKTREE_PATH" "$BASE_BRANCH"
fi

# Copy .claude directory if it exists
if [ -d ".claude" ]; then
    cp -r .claude "$WORKTREE_PATH/"
fi

# Change to worktree and run setup
cd "$WORKTREE_PATH"
make setup || {
    echo "Setup failed. Cleaning up..."
    cd - > /dev/null
    git worktree remove --force "$WORKTREE_PATH"
    git branch -D "$WORKTREE_NAME" 2>/dev/null || true
    exit 1
}
```

**For jj users:**
```bash
# Set up variables
WORKTREE_NAME="[name or generated]"
BASE_BOOKMARK="[base bookmark]"
WORKTREES_BASE="$HOME/wt/[repo-name]"
WORKTREE_PATH="${WORKTREES_BASE}/${WORKTREE_NAME}"

# Verify worktrees base directory exists
if [ ! -d "$WORKTREES_BASE" ]; then
    echo "Creating worktrees directory: $WORKTREES_BASE"
    mkdir -p "$WORKTREES_BASE"
fi

# Check if worktree already exists
if [ -d "$WORKTREE_PATH" ]; then
    echo "Error: Worktree directory already exists: $WORKTREE_PATH"
    exit 1
fi

# Create new workspace
jj workspace add --name "$WORKTREE_NAME" "$WORKTREE_PATH"

# Set bookmark in new workspace
cd "$WORKTREE_PATH"
jj bookmark create "$WORKTREE_NAME"

# Copy .claude directory if it exists from original workspace
if [ -d "../.claude" ]; then
    cp -r ../.claude .
fi

# Run setup
make setup || {
    echo "Setup failed. Cleaning up..."
    cd - > /dev/null
    jj workspace forget "$WORKTREE_NAME"
    rm -rf "$WORKTREE_PATH"
    exit 1
}
```

### 3. Generate Unique Name (if needed)

If no name provided, generate one:

```bash
# Random adjectives and nouns for naming
adjectives=("swift" "bright" "clever" "smooth" "quick" "clean" "sharp" "neat" "cool" "fast")
nouns=("fix" "task" "work" "dev" "patch" "branch" "code" "build" "test" "run")

# Pick random values
adj=${adjectives[$RANDOM % ${#adjectives[@]}]}
noun=${nouns[$RANDOM % ${#nouns[@]}]}
timestamp=$(date +%H%M)

# Generate name
WORKTREE_NAME="${adj}_${noun}_${timestamp}"
```

### 4. Success Message

After successful creation:

```
✅ Worktree created successfully!
📁 Path: [WORKTREE_PATH]
🔀 Branch/Bookmark: [WORKTREE_NAME]

To work in this worktree:
  cd [WORKTREE_PATH]

To remove this worktree later (git):
  git worktree remove [WORKTREE_PATH]
  git branch -D [WORKTREE_NAME]

To remove this worktree later (jj):
  jj workspace forget [WORKTREE_NAME]
  rm -rf [WORKTREE_PATH]
```

## Important Notes

- The script runs `make setup` to install dependencies in the new worktree
- If setup fails, the worktree is automatically cleaned up
- The .claude directory is copied to the new worktree if it exists
- Worktrees are created in `$HOME/wt/[repo-name]/` by default
- For Linear tickets, use the ticket number as the worktree name (e.g., `ENG-2166`)
- Thoughts initialization is optional and can be skipped with `--no-thoughts` flag
