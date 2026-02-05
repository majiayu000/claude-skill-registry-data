---
name: setup-worktree
description: Install worktree management script in the current project
---

# Setup Worktree

Installs the worktree management script and configures the current project for worktree-based development.

## When to Use

- First time using worktrees in a project
- Setting up a new project with SQLite database
- User explicitly requests worktree setup

## Installation Steps

### Step 1: Detect Package Manager

Detect which package manager the project uses:

```bash
# Detect package manager
if [ -f "pnpm-lock.yaml" ]; then
  PKG_MANAGER="pnpm"
elif [ -f "yarn.lock" ]; then
  PKG_MANAGER="yarn"
elif [ -f "package-lock.json" ]; then
  PKG_MANAGER="npm"
else
  PKG_MANAGER="npm"  # Default fallback
fi

echo "Detected package manager: $PKG_MANAGER"
```

### Step 2: Check Prerequisites

Verify the project has:
```bash
# Check for package.json
test -f package.json || echo "No package.json found"

# Check for git repository
git rev-parse --git-dir > /dev/null 2>&1 || echo "Not a git repository"

# Check for tsx (package manager specific)
case $PKG_MANAGER in
  pnpm)
    pnpm ls tsx > /dev/null 2>&1 || TSX_MISSING=1
    ;;
  yarn)
    yarn list --pattern tsx > /dev/null 2>&1 || TSX_MISSING=1
    ;;
  npm)
    npm ls tsx > /dev/null 2>&1 || TSX_MISSING=1
    ;;
esac
```

If `tsx` is not installed, add it using the detected package manager:
```bash
if [ -n "$TSX_MISSING" ]; then
  echo "Installing tsx..."
  case $PKG_MANAGER in
    pnpm) pnpm add -D tsx ;;
    yarn) yarn add -D tsx ;;
    npm) npm install -D tsx ;;
  esac
  echo "✓ tsx installed"
fi
```

### Step 3: Copy Worktree Script

Copy the generic worktree management script to the project:

```bash
# Create scripts directory if it doesn't exist
mkdir -p scripts

# Copy the script from the skills plugin
SKILL_PATH="$HOME/.claude/plugins/worktree"
if [ -d "$SKILL_PATH/scripts" ]; then
  cp "$SKILL_PATH/scripts/manage-worktree.ts" scripts/
  echo "✓ Copied manage-worktree.ts to scripts/"
else
  echo "❌ Worktree plugin not found. Install it first with: claude plugin add worktree"
  exit 1
fi
```

### Step 4: Add Package Script

Add the `worktree` script to `package.json`:

**Using Edit tool** (preferred):
- Read `package.json`
- Add `"worktree": "tsx scripts/manage-worktree.ts"` to the `scripts` section
- Use Edit tool to add it

**Alternative - Using jq**:
```bash
# Backup first
cp package.json package.json.backup

# Add worktree script
jq '.scripts.worktree = "tsx scripts/manage-worktree.ts"' package.json > package.json.tmp
mv package.json.tmp package.json
```

### Step 5: Update .gitignore

Add worktree-related files to `.gitignore`:

```bash
# Check if .gitignore exists
if [ ! -f .gitignore ]; then
  touch .gitignore
fi

# Add worktree entries if not already present
grep -q "^\.worktrees" .gitignore || echo ".worktrees/" >> .gitignore
grep -q "^\.worktree-metadata\.json" .gitignore || echo ".worktree-metadata.json" >> .gitignore

echo "✓ Updated .gitignore"
```

### Step 6: Detect SQLite Databases

Scan the project for SQLite databases to confirm setup will work:

```bash
echo "Scanning for SQLite databases..."

# Check for Cloudflare D1
if [ -d ".wrangler/state/v3/d1" ]; then
  echo "  ✓ Found Cloudflare D1 databases in .wrangler/state/v3/d1/"
fi

# Check for .db, .sqlite, .sqlite3 files
DB_FILES=$(find . -maxdepth 2 -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" 2>/dev/null)
if [ -n "$DB_FILES" ]; then
  echo "  ✓ Found SQLite files:"
  echo "$DB_FILES" | sed 's/^/    - /'
fi
```

If no databases found, warn the user:
```
⚠ No SQLite databases detected yet.
  - Worktrees will still work but won't snapshot any databases
  - You can configure custom database path in CLAUDE.md with:
    WORKTREE_DB_PATH=path/to/your/database
```

### Step 7: Configure Project (Optional)

Prompt user if they want to add configuration to `CLAUDE.md`:

```markdown
## Worktree Configuration

Use git worktrees for parallel development with isolated databases and ports.

### Configuration

- `PROJECT_PREFIX=your-project-name` - Branch naming prefix (default: directory name)
- `WORKTREE_BASE_PORT=4322` - Starting port for dev servers (default: 4322)
- `WORKTREE_MAIN_PORT=4321` - Main worktree dev server port (default: 4321)
- `WORKTREE_DEV_COMMAND=dev` - npm script to start dev server (default: "dev")

### When to Use Worktrees

**Use worktrees** (via `pnpm worktree create`):
- Database/schema changes requiring isolated state
- Backend API changes that need separate dev server
- Parallel development on multiple features
- Testing migrations before merging

**Use regular branches** (simpler):
- UI-only changes (styling, components, copy)
- Documentation updates
- Simple fixes with no database interaction

### Commands

```bash
# Create worktree for issue #15
pnpm worktree create 15 dark-mode --start-server

# List active worktrees
pnpm worktree list

# Delete worktree
pnpm worktree delete 15
```

See worktree plugin README for full documentation.
```

### Step 8: Verify Installation

Test that the script works using the detected package manager:

```bash
# Run the worktree command to see help
case $PKG_MANAGER in
  pnpm) pnpm worktree ;;
  yarn) yarn worktree ;;
  npm) npm run worktree ;;
esac

# Expected output should show:
# Worktree Management CLI
# Commands:
#   create ...
#   delete ...
#   list
#   info ...
```

### Step 9: Announce Completion

Output:
```
✅ Worktree management installed successfully!

Setup complete:
  ✓ scripts/manage-worktree.ts installed
  ✓ package.json updated with "pnpm worktree" command
  ✓ .gitignore updated
  ✓ {N} SQLite database(s) detected

Get started:
  $PKG_MANAGER worktree create <issue-number> <slug> [--start-server]

Example:
  $PKG_MANAGER worktree create 15 dark-mode --start-server

For help:
  $PKG_MANAGER worktree
```

## Error Handling

If script installation fails:
- Check that `~/.claude/plugins/worktree` exists
- Verify the plugin is installed: `claude plugin list`
- Install manually: `claude plugin add worktree`

If package.json update fails:
- Ensure `jq` is installed or use Edit tool
- Manually add: `"worktree": "tsx scripts/manage-worktree.ts"` to scripts section

## Configuration in CLAUDE.md

The skill should suggest adding this to the project's `CLAUDE.md`:

```markdown
## Git Worktree Workflow

This project uses git worktrees for parallel development with isolated SQLite databases.

When creating a new issue/feature:
1. Claude creates a GitHub issue with the plan
2. Claude creates a worktree: `pnpm worktree create {N} {slug} --start-server`
3. Each worktree gets:
   - Isolated git directory in `.worktrees/issue-{N}-{slug}/`
   - Snapshot of current SQLite database(s)
   - Dedicated dev server port (4322+)
   - Symlinked node_modules (saves disk space)

Commands:
- `pnpm worktree list` - Show all active worktrees
- `pnpm worktree info {N}` - Show details for issue #{N}
- `pnpm worktree delete {N}` - Clean up worktree

See `/ship` and `/done` skills for automatic worktree management.
```
