---
name: YADM Utilities
description: This skill should be used when the user asks to "track files with yadm", "check yadm status", "commit to yadm", "sync dotfiles", "add to yadm", "manage Claude Code configuration with yadm", "what should I track in yadm", "use yadm alternates", "create OS-specific dotfiles", "configure yadm for multiple machines", "bootstrap yadm", "run yadm bootstrap", "setup new machine with yadm", or mentions yadm operations for dotfiles management.
version: 0.1.0
---

# YADM Utilities

This skill provides guidance for managing dotfiles using YADM (Yet Another Dotfiles Manager), with specialized knowledge for tracking Claude Code configuration files, using YADM's alternates feature for multi-system configurations, and bootstrapping new machines.

## Overview

YADM is a dotfiles manager that uses git under the hood but operates on your home directory. It provides a clean way to version control configuration files without turning your entire home directory into a git repository.

### Key Concepts

**YADM operates like git but manages `$HOME`:**
- `yadm status` shows tracked files in home directory
- `yadm add ~/.file` tracks specific files
- `yadm commit` creates commits
- `yadm push/pull` syncs with remote repository

**Core principle:** Track configuration that represents work and preferences, not generated files or machine-specific state.

## Common YADM Operations

### Check Repository Status

```bash
yadm status
```

Shows tracked files with uncommitted changes and untracked files that match yadm patterns.

### Track New Files

```bash
# Track a specific file
yadm add ~/.claude/agents/new-agent.md

# Track multiple files at once
yadm add ~/.claude/settings.json ~/.claude/CLAUDE.md

# Check what will be committed
yadm status
```

### Commit Changes

```bash
# Commit with descriptive message
yadm commit -m "Add new agent for X functionality"

# Commit multiple changes
yadm commit -m "Update Claude Code plugin configuration"
```

### Sync with Remote

```bash
# Push changes to remote
yadm push

# Pull updates from remote
yadm pull

# Check sync status
yadm status
```

### List Tracked Files

```bash
# Show all files tracked by yadm
yadm ls-files

# Show only Claude Code files
yadm ls-files | grep "^\.claude"
```

## YADM Bootstrap Feature

The bootstrap feature automates additional setup steps after cloning a dotfiles repository to a new machine. This is essential for installing dependencies, configuring applications, and setting up the environment.

### How Bootstrap Works

**Bootstrap program location:** `$HOME/.config/yadm/bootstrap`

**Execution:** Run `yadm bootstrap` to execute the bootstrap program

**Automatic prompting:** After `yadm clone`, YADM offers to run bootstrap if it exists

**Language agnostic:** Bootstrap can be any executable (bash, python, etc.)

### Creating a Bootstrap Script

Create an executable program at `~/.config/yadm/bootstrap`:

```bash
#!/bin/bash
# Example bootstrap script

set -e

echo "Running yadm bootstrap..."

# Install Homebrew if not present
if ! command -v brew >/dev/null 2>&1; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Process Brewfile if it exists
if [ -f "$HOME/.Brewfile" ]; then
    echo "Installing Homebrew packages..."
    brew bundle --global
fi

# Initialize git submodules
if [ -f "$HOME/.gitmodules" ]; then
    echo "Initializing git submodules..."
    yadm submodule update --init --recursive
fi

# Set up Claude Code plugins
if [ -d "$HOME/.claude" ]; then
    echo "Setting up Claude Code plugins..."
    claude plugin marketplace update
    # Install plugins as needed
fi

echo "Bootstrap complete!"
```

**Make executable:**
```bash
chmod +x ~/.config/yadm/bootstrap
```

### Bootstrap Best Practices

**Idempotent design:** Bootstrap should be safe to run multiple times

**Check before install:** Verify if tools/configs already exist before creating them

**Error handling:** Use `set -e` and handle failures gracefully

**Progress output:** Echo what's happening for user visibility

**Platform detection:** Use conditionals for OS-specific setup

### Common Bootstrap Tasks

**Install package managers:**
```bash
# Homebrew on macOS
if [[ "$OSTYPE" == "darwin"* ]] && ! command -v brew >/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
```

**Process Brewfile:**
```bash
if [ -f "$HOME/.Brewfile" ]; then
    brew bundle --global
fi

# Or with alternates
if [ -f "$HOME/.Brewfile" ]; then
    # yadm alternates will have created the right symlink
    brew bundle --file="$HOME/.Brewfile"
fi
```

**Initialize submodules:**
```bash
yadm submodule update --init --recursive
```

**Configure applications:**
```bash
# iTerm2 preferences
defaults write com.googlecode.iterm2 PrefsCustomFolder -string "$HOME/.config/iterm2"

# Terminal theme
tic -x "$HOME/.config/terminfo/xterm-256color-italic.terminfo"
```

**Update remote URL to SSH:**
```bash
yadm remote set-url origin "git@github.com:username/dotfiles.git"
```

**Install plugin managers:**
```bash
# vim-plug
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

**Claude Code setup:**
```bash
# Update marketplaces
claude plugin marketplace update

# Install plugins
claude plugin install superpowers@superpowers-marketplace
claude plugin install elements-of-style@superpowers-marketplace

# Clone custom plugin repos
if [ ! -d "$HOME/.claude/plugins/repos/devops-toolkit" ]; then
    git clone git@github.com:username/devops-toolkit.git \
        "$HOME/.claude/plugins/repos/devops-toolkit"
fi
```

### Advanced: Bootstrap.d Directory Structure

For complex bootstraps, split into separate scripts in `$HOME/.config/yadm/bootstrap.d/`:

```
~/.config/yadm/
├── bootstrap                    # Main script
└── bootstrap.d/
    ├── 00-system.sh            # System setup
    ├── 10-packages.sh          # Package installation
    ├── 20-applications.sh      # App configuration
    ├── 30-claude-code.sh       # Claude Code setup
    └── 99-cleanup.sh           # Final steps
```

**Main bootstrap script:**
```bash
#!/bin/bash
set -e

BOOTSTRAP_D="$HOME/.config/yadm/bootstrap.d"

if [ -d "$BOOTSTRAP_D" ]; then
    for script in "$BOOTSTRAP_D"/*; do
        if [ -x "$script" ]; then
            echo "Running $(basename "$script")..."
            "$script"
        fi
    done
fi
```

**With alternates support:**
```bash
# Create OS-specific scripts
bootstrap.d/10-packages.sh##os.Darwin
bootstrap.d/10-packages.sh##os.Linux

# yadm alternates creates the right symlink
```

### Brewfile Integration

**Track Brewfile in yadm:**
```bash
yadm add ~/.Brewfile
yadm commit -m "Add Brewfile for package management"
```

**Bootstrap installs from Brewfile:**
```bash
#!/bin/bash
# In ~/.config/yadm/bootstrap

if [ -f "$HOME/.Brewfile" ]; then
    echo "Installing packages from Brewfile..."
    brew bundle --global
fi
```

**OS-specific Brewfiles using alternates:**
```bash
.Brewfile##os.Darwin           # macOS packages
.Brewfile##os.Linux            # Linux packages
.Brewfile##default             # Common packages
```

### Bootstrap Workflow

**Initial setup on first machine:**
```bash
# Create bootstrap script
vi ~/.config/yadm/bootstrap

# Make executable
chmod +x ~/.config/yadm/bootstrap

# Track with yadm
yadm add ~/.config/yadm/bootstrap

# Track Brewfile
yadm add ~/.Brewfile

# Commit
yadm commit -m "Add bootstrap configuration"
yadm push
```

**Clone to new machine:**
```bash
# Clone dotfiles
yadm clone https://github.com/username/dotfiles.git

# YADM will prompt:
# "Found .config/yadm/bootstrap
#  It appears that a bootstrap program exists.
#  Would you like to execute it now? (y/n)"

# Or run manually
yadm bootstrap
```

**Re-run bootstrap after updates:**
```bash
# Pull latest changes
yadm pull

# Re-run bootstrap (should be idempotent)
yadm bootstrap
```

### Clone with Bootstrap Flags

**Auto-bootstrap:**
```bash
yadm clone --bootstrap https://github.com/username/dotfiles.git
```

**Skip bootstrap prompt:**
```bash
yadm clone --no-bootstrap https://github.com/username/dotfiles.git
```

## YADM Alternates Feature

YADM's alternates feature enables automatic selection of different file versions based on system attributes like OS, hostname, user, or custom classes. This is essential for maintaining a single dotfiles repository across multiple machines with different configurations.

### How Alternates Work

**Basic concept:** Add a suffix to filename: `filename##<condition>[,<condition>,...]`

YADM creates a symlink from the base filename to the most appropriate alternate version based on system attributes.

**Example:**
```
.gitconfig##default
.gitconfig##os.Darwin
.gitconfig##os.Linux
.gitconfig##os.Darwin,hostname.macbook-pro
```

On a macOS machine named "macbook-pro", YADM creates:
`.gitconfig` → `.gitconfig##os.Darwin,hostname.macbook-pro`

### Alternate Syntax

**Condition format:** `attribute.value`

**Multiple conditions:** Separate with commas (all must match)

**Negation:** Prefix with `~` to invert condition

**Attributes (with short codes):**

| Attribute | Code | Detection | Example |
|-----------|------|-----------|---------|
| `arch` | `a` | `uname -m` | `##arch.x86_64` |
| `class` | `c` | Manual config | `##class.Work` |
| `distro` | `d` | `lsb_release -si` | `##distro.Ubuntu` |
| `distro_family` | `f` | `/etc/os-release` | `##distro_family.debian` |
| `hostname` | `h` | `uname -n` | `##hostname.macbook` |
| `os` | `o` | `uname -s` | `##os.Darwin` |
| `user` | `u` | `id -u -n` | `##user.ada` |
| `extension` | `e` | Syntax highlighting | `##e.sh` |
| `template` | `t` | Template processor | `##template` |
| `default` | - | Fallback | `##default` |

### Practical Examples

**OS-specific shell config:**
```bash
.zshrc##os.Darwin        # macOS version
.zshrc##os.Linux         # Linux version
.zshrc##default          # Fallback for others
```

**Hostname-specific SSH config:**
```bash
.ssh/config##hostname.work-laptop
.ssh/config##hostname.personal-desktop
.ssh/config##default
```

**Class-based configurations:**
```bash
# Set class: yadm config local.class Work
.gitconfig##class.Work
.gitconfig##class.Personal

# Multiple classes
.aws/config##class.Work,class.AWS
```

**Combining conditions:**
```bash
# macOS work laptop
.claude/settings.json##os.Darwin,class.Work

# Linux personal desktop
.claude/settings.json##os.Linux,class.Personal
```

**Negation:**
```bash
# All systems except Darwin
.bashrc##~os.Darwin

# Work machines except specific host
.gitconfig##class.Work,~hostname.test-machine
```

### Class Configuration

**Set a class:**
```bash
yadm config local.class Work
```

**Add multiple classes:**
```bash
yadm config local.class Personal
yadm config --add local.class AWS
yadm config --add local.class Developer
```

**View all classes:**
```bash
yadm config --get-all local.class
```

### Bootstrap with Alternates

Alternates work seamlessly with bootstrap:

```bash
# Create OS-specific bootstrap scripts
.config/yadm/bootstrap##os.Darwin
.config/yadm/bootstrap##os.Linux

# Or use bootstrap.d with alternates
.config/yadm/bootstrap.d/10-packages.sh##os.Darwin
.config/yadm/bootstrap.d/10-packages.sh##os.Linux
```

YADM automatically creates the correct symlink before running bootstrap.

## Claude Code Configuration Management

### Quick Decision Framework

**Always track:**
- Custom agents (`~/.claude/agents/*.md`)
- Custom skills (`~/.claude/skills/*/SKILL.md` and supporting files)
- Hookify rules (`~/.claude/hookify.*.local.md`)
- Custom hooks (`~/.claude/hooks/*.py`, `~/.claude/hooks/*.sh`)
- Settings (`~/.claude/settings.json`, `~/.claude/CLAUDE.md`)
- Plugin configuration (`~/.claude/plugins/config.json`, `~/.claude/plugins/installed_plugins.json`, `~/.claude/plugins/known_marketplaces.json`)
- Custom scripts (`~/.claude/*.sh`)
- Bootstrap script (`~/.config/yadm/bootstrap`)

**Never track:**
- Cache directories (`~/.claude/plugins/cache/`, `~/.claude/plugins/marketplaces/`)
- Session state (`~/.claude/file-history/`, `~/.claude/todos/`, `~/.claude/projects/`)
- Debug logs (`~/.claude/debug/`)
- Lock files (`~/.claude/ide/*.lock`)
- History (`~/.claude/history.jsonl`)

**Plugin repositories are special:**
- Separate git repos in `~/.claude/plugins/repos/`
- Manage independently, not with yadm
- Bootstrap can clone them automatically

## Workflow: New Machine Setup with Bootstrap

The complete workflow for setting up a new machine:

1. **Clone dotfiles:**
   ```bash
   yadm clone https://github.com/username/dotfiles.git
   ```

2. **YADM prompts to run bootstrap:**
   ```
   Found .config/yadm/bootstrap
   It appears that a bootstrap program exists.
   Would you like to execute it now? (y/n)
   ```
   Answer `y` or run manually: `yadm bootstrap`

3. **Bootstrap automatically:**
   - Installs Homebrew
   - Processes Brewfile
   - Updates plugin marketplaces
   - Installs plugins
   - Clones custom plugin repos
   - Configures applications
   - Sets up environment

4. **Configure machine class:**
   ```bash
   yadm config local.class Work
   ```

5. **Verify setup:**
   ```bash
   ls -la ~/.claude/settings.json  # Check alternates
   claude plugin list              # Check plugins
   which brew                      # Verify Homebrew
   ```

## Workflow: Adding Bootstrap Tasks

When adding new bootstrap steps:

1. **Edit bootstrap script:**
   ```bash
   vi ~/.config/yadm/bootstrap
   ```

2. **Test locally (should be idempotent):**
   ```bash
   yadm bootstrap
   ```

3. **Verify no errors:**
   ```bash
   echo $?  # Should be 0
   ```

4. **Commit changes:**
   ```bash
   yadm add ~/.config/yadm/bootstrap
   yadm commit -m "Add bootstrap task for X"
   yadm push
   ```

5. **Test on another machine:**
   ```bash
   yadm pull
   yadm bootstrap
   ```

## Workflow: Updating Brewfile

When adding new packages:

1. **Edit Brewfile:**
   ```bash
   vi ~/.Brewfile
   ```

2. **Test installation:**
   ```bash
   brew bundle --global
   ```

3. **Track changes:**
   ```bash
   yadm add ~/.Brewfile
   yadm commit -m "Add package X to Brewfile"
   yadm push
   ```

4. **On other machines:**
   ```bash
   yadm pull
   yadm bootstrap  # Or: brew bundle --global
   ```

## Best Practices

### Bootstrap Best Practices

**Idempotent design:**
```bash
# Check before installing
if ! command -v brew >/dev/null; then
    install_homebrew
fi

# Check before creating
if [ ! -f "$HOME/.config/app/config" ]; then
    setup_config
fi
```

**Error handling:**
```bash
set -e  # Exit on error

# Or handle specific errors
if ! brew bundle --global; then
    echo "Warning: Some Brewfile packages failed"
    # Continue anyway
fi
```

**Progress output:**
```bash
echo "Step 1/5: Installing Homebrew..."
echo "Step 2/5: Processing Brewfile..."
```

**Platform detection:**
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS-specific
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux-specific
fi
```

### Commit Message Guidelines

Write descriptive commit messages:

**Good:**
```
Add yadm-manager agent for dotfiles management
Update bootstrap to install Claude Code plugins
Add Brewfile with development tools
Configure hookify rule to prevent Claude mentions
```

**Avoid:**
```
Update files
Changed stuff
WIP
```

### Documentation Maintenance

Keep `~/.claude/README.md` synchronized:
- Document bootstrap process
- List what gets installed
- Note any manual steps required
- Document alternates used

## Troubleshooting

### Bootstrap Not Running

**Check if bootstrap exists:**
```bash
ls -la ~/.config/yadm/bootstrap
```

**Check if executable:**
```bash
chmod +x ~/.config/yadm/bootstrap
```

**Run manually with debug:**
```bash
bash -x ~/.config/yadm/bootstrap
```

### Brewfile Errors

**Verify Brewfile syntax:**
```bash
brew bundle check --global
```

**Install specific packages:**
```bash
brew bundle --global --verbose
```

**Skip failing packages:**
```bash
brew bundle --global || true
```

### Alternates Not Working

**Check filename syntax:**
```bash
# Must be: filename##condition
# Verify with: yadm ls-files
```

**Verify attribute values:**
```bash
uname -s    # OS
uname -n    # Hostname
yadm config local.class  # Class
```

**Force alternate update:**
```bash
yadm alt
```

This skill enables efficient dotfiles management with YADM, including bootstrap automation for new machine setup, alternates for multi-system configurations, and specialized Claude Code configuration tracking.
