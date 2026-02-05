---
name: using-lt-cli
description: Expert for lenne.tech CLI (lt command). ALWAYS activate when user mentions "lt", "lt CLI", "lenne.tech CLI", fullstack workspace, local templates, or any lt command. Provides comprehensive reference for all lt CLI features including fullstack init, git workflows, server creation, and advanced options. Works alongside generating-nest-servers for NestJS development tasks.
---

# LT CLI Expert

You are an expert in the lenne.tech CLI tool (`lt` command). This skill provides comprehensive reference for all lt CLI features.

**CRITICAL:** For NestJS server development (modules, objects, properties), ALWAYS use the `generating-nest-servers` skill instead.

## Skill Activation

This skill activates whenever:
- User mentions "lt", "lt CLI", or "lenne.tech CLI"
- User wants to create a fullstack workspace
- User mentions local templates, symlinks, or branch options
- Any lt command is being used

## Complementary Skills

For NestJS server development, this skill works **alongside** `generating-nest-servers`:

| Task | Skills Used |
|------|-------------|
| `lt fullstack init` | **using-lt-cli** |
| `lt git get`, `lt git reset` | **using-lt-cli** |
| `lt server create` | **using-lt-cli** + generating-nest-servers |
| `lt server module`, `lt server object` | **using-lt-cli** + generating-nest-servers |
| NestJS code modifications | generating-nest-servers |

Both skills can be active simultaneously - this skill provides CLI syntax reference, while `generating-nest-servers` provides NestJS development expertise

## Related Skills

**Works closely with:**
- `generating-nest-servers` skill - For ALL NestJS server development
- `building-stories-with-tdd` skill - For Test-Driven Development with NestJS

**When to use which:**
- Git operations (`lt git`)? Use this skill (using-lt-cli)
- Fullstack init? Use this skill (using-lt-cli)
- NestJS development? Use `generating-nest-servers` skill
- TDD approach? Use `building-stories-with-tdd` skill

---

## Available Commands

### 1. Git Operations

#### Get Branch
**Command**: `lt git get <branch-name>` (alias: `lt git g`)

Checks out a branch, creating it if it doesn't exist.

**Non-interactive syntax**:
```bash
lt git get <branch-name>
```

**Examples**:
```bash
# Checkout existing or create new branch
lt git get DEV-123

# Using alias
lt git g feature/new-feature
```

**What it does**:
1. Checks if branch exists locally
2. If not, checks if it exists on remote
3. If remote exists, checks out and tracks remote branch
4. If neither exists, creates new branch from current branch
5. Switches to the branch

#### Reset to Remote
**Command**: `lt git reset`

Resets current branch to match remote (discards local changes).

**Interactive**: Prompts for confirmation before resetting.

**What it does**:
1. Fetches latest from remote
2. Resets current branch to origin/<branch>
3. Discards all local changes and commits

**WARNING**: This is destructive! All local changes will be lost.

### 2. Fullstack Initialization

#### Initialize Fullstack Workspace
**Command**: `lt fullstack init` (alias: `lt full init`)

Creates complete fullstack workspace with frontend and backend.

**Interactive mode**:
- Prompts for workspace name
- Prompts for frontend framework (Angular or Nuxt)
- Prompts for git initialization
- Prompts for git repository URL (if git enabled)

**Non-interactive syntax**:
```bash
lt fullstack init --name <WorkspaceName> --frontend <angular|nuxt> --git <true|false> [--git-link <GitURL>] [--api-branch <branch>] [--frontend-branch <branch>] [--api-copy <path>] [--api-link <path>] [--frontend-copy <path>] [--frontend-link <path>]
```

**Parameters**:
- `--name` - Workspace/project name (PascalCase recommended)
- `--frontend` - Frontend framework: `angular` or `nuxt`
- `--git` - Initialize git repository: `true` or `false`
- `--git-link` - Git repository URL (optional, only if `--git true`)
- `--api-branch` - Branch of nest-server-starter to use for API (optional, for testing specific branches)
- `--frontend-branch` - Branch of frontend starter to use (optional, for testing specific branches)
- `--api-copy` - Path to local API template directory (copies the template)
- `--api-link` - Path to local API template directory (creates symlink for fastest testing)
- `--frontend-copy` - Path to local frontend template directory (copies the template)
- `--frontend-link` - Path to local frontend template directory (creates symlink for fastest testing)

**Examples**:
```bash
# With git and repository
lt fullstack init --name MyApp --frontend angular --git true --git-link https://github.com/user/myapp.git

# Without git
lt fullstack init --name MyApp --frontend nuxt --git false

# Using alias
lt full init --name MyProject --frontend angular --git true

# With local templates (symlink for fastest testing)
lt fullstack init --name MyApp --frontend nuxt --git false \
  --api-link ~/code/nest-server-starter \
  --frontend-link ~/code/nuxt-base-starter

# With local templates (copy for independent development)
lt fullstack init --name MyApp --frontend angular --git true \
  --api-copy ~/code/nest-server-starter \
  --frontend-copy ~/code/ng-base-starter
```

**What gets created**:
```
<workspace-name>/
  frontend/          # Angular or Nuxt application
  projects/
    api/            # NestJS backend (@lenne.tech/nest-server)
  package.json      # Root workspace configuration
  .gitignore        # (if git enabled)
  .git/             # (if git enabled)
```

**Post-creation steps**:
1. `cd <workspace-name>`
2. Install dependencies: `npm install`
3. Start backend: `cd projects/api && npm start`
4. Start frontend: `cd frontend && npm start`

---

## How to Redirect to generating-nest-servers

When you detect ANY NestJS server task, immediately inform the user:

**Template response**:
```
For NestJS server development tasks, please use the **generating-nest-servers skill** instead.

This skill is specifically designed for all NestJS/nest-server work, including:
- Creating modules, objects, or properties
- Modifying existing server code
- Generating complete server structures

I can help you with your NestJS server task using the generating-nest-servers skill.
```

---

## Best Practices

### Git Operations
1. **Always commit changes before `lt git reset`** - It's destructive!
2. **Use meaningful branch names** - Follow your team's conventions (e.g., `DEV-123`, `feature/xyz`)
3. **Check status first** - Run `git status` before reset operations

### Fullstack Init
1. **Plan your architecture** - Know which frontend framework you need
2. **Set up git early** - Use `--git true` from the start
3. **Follow naming conventions** - Use PascalCase for workspace names
4. **Read the generated README** - Each project has specific setup instructions

---

## Troubleshooting

### Git Reset Not Working
**Symptom**: Reset command fails or doesn't reset properly
**Cause**: Remote branch doesn't exist or network issues
**Solution**:
- Check if remote branch exists: `git branch -r`
- Ensure you're connected to remote: `git remote -v`
- Fetch first: `git fetch origin`

### Fullstack Init Fails
**Symptom**: Installation errors during `lt fullstack init`
**Cause**: Network issues, missing dependencies, or permissions
**Solution**:
- Check internet connection
- Ensure Node.js is installed: `node --version`
- Check npm permissions
- Try with sudo if permission errors persist

### Branch Already Exists
**Symptom**: `lt git get` says branch exists but can't switch
**Cause**: Uncommitted changes in working directory
**Solution**: Commit, stash, or discard changes first:
```bash
git stash        # Save changes temporarily
lt git get <branch>
git stash pop    # Restore changes
```

---

## Working with This Skill

When helping users:

1. **Clarify intent**: Is this a git operation or fullstack setup?
2. **Redirect server tasks**: Immediately suggest nest-server-generator for any NestJS work
3. **Provide complete commands**: Include all necessary flags
4. **Warn about destructive operations**: Always warn before `lt git reset`
5. **Explain side effects**: Describe what will happen

### Example Response Pattern

**User**: "Switch to branch DEV-456"

**Your response**:
```bash
# Switch to branch DEV-456 (creates if it doesn't exist)
lt git get DEV-456

# This will:
# ✓ Check if DEV-456 exists locally
# ✓ If not, check remote
# ✓ If remote exists, checkout and track
# ✓ If neither exists, create new branch
# ✓ Switch to the branch
```

**User**: "Create a User module"

**Your response**:
```
For creating NestJS modules, please use the **generating-nest-servers skill** instead.

That skill is specifically designed for all NestJS/nest-server development tasks.

Then I can help you create the User module with all necessary files and configurations.
```

---

## Important Notes

- **CLI works from anywhere** in your project directory
- **Automatically finds** the nearest git repository for git commands
- **Creates missing directories** for fullstack init
- **Validates inputs** before executing destructive operations
- **Always use generating-nest-servers skill** for NestJS server development

---

## Command Reference

For detailed command syntax and all available options, see [reference.md](reference.md).

For NestJS server commands (`lt server module`, `lt server object`, etc.), use the **generating-nest-servers skill**.
