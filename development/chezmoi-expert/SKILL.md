---
name: chezmoi-expert
description: Use chezmoi like an expert for managing dotfiles with advanced features including templates, secrets management, scripts, external dependencies, and multi-machine configurations. This skill should be used when working with chezmoi dotfiles, optimizing performance, debugging issues, or implementing advanced patterns.
---

# Chezmoi Expert

## Overview

This skill provides expert-level knowledge for using chezmoi, a dotfile manager that maintains consistent configurations across multiple machines. It covers advanced template systems, secure secrets management, script automation, external file management, multi-machine strategies, performance optimization, and comprehensive troubleshooting techniques.

## When to Use This Skill

Use this skill when:
- Working with chezmoi dotfile configurations
- Setting up new machines with dotfiles
- Implementing machine-specific configurations
- Managing secrets securely in dotfiles
- Creating template-based configurations
- Automating setup with scripts
- Managing external dependencies
- Optimizing chezmoi performance
- Debugging chezmoi issues
- Migrating to or between chezmoi setups

## Core Principles

### Declarative State Management

Chezmoi operates on a declarative model with three key states:
- **Source State**: Desired configuration stored in `~/.local/share/chezmoi`
- **Target State**: Computed desired state based on source + config + templates
- **Destination State**: Current state of files in home directory

### Template-Driven Configuration

Use Go templates with Sprig functions to create machine-specific configurations from a single source. Templates evaluate based on:
- Built-in variables (`.chezmoi.os`, `.chezmoi.hostname`, etc.)
- Config file data (`~/.config/chezmoi/chezmoi.toml`)
- Static data files (`.chezmoidata/`)
- External sources (password managers, commands)

### Idempotent Operations

All operations should be safe to run multiple times. Scripts should check state before making changes. Templates should produce consistent output for the same inputs.

## Quick Reference

### Common Operations

**Edit and apply**:
```bash
chezmoi edit --apply ~/.zshrc
```

**Preview changes**:
```bash
chezmoi diff
```

**Apply changes**:
```bash
chezmoi apply --verbose
```

**Add new file**:
```bash
chezmoi add --template ~/.gitconfig
```

**Update from remote**:
```bash
chezmoi update
```

**Check system health**:
```bash
chezmoi doctor
```

**Test template**:
```bash
chezmoi execute-template "{{ .chezmoi.hostname }}"
```

### File Naming Conventions

Understanding chezmoi file naming is essential:

- `dot_filename` → `.filename`
- `private_dot_filename` → `.filename` (mode 600)
- `executable_filename` → `filename` (mode +x)
- `exact_dirname` → `dirname/` (removes unmanaged files)
- `encrypted_filename.age` → `filename` (decrypted with age)
- `filename.tmpl` → `filename` (template evaluated)
- `symlink_name` → symlink to target

Prefixes can be combined: `private_encrypted_dot_ssh/private_encrypted_id_rsa.age.tmpl`

## Working with Templates

### Data Sources Priority

Chezmoi loads data in this order (later sources override earlier):
1. Built-in variables (`.chezmoi.*`)
2. Static data files (`.chezmoidata.$FORMAT`)
3. Data directories (`.chezmoidata/*.yaml`)
4. Config file data (`chezmoi.toml` `[data]` section)

### Creating Templates

Convert existing file to template:
```bash
chezmoi add --template ~/.gitconfig
```

Test template rendering:
```bash
chezmoi cat ~/.gitconfig
chezmoi execute-template "{{ .user.email }}"
```

### Common Template Patterns

**OS-specific logic**:
```go
{{ if eq .chezmoi.os "darwin" -}}
macOS configuration
{{ else if eq .chezmoi.os "linux" -}}
Linux configuration
{{ end -}}
```

**Machine-class logic**:
```go
{{ if eq .machine_class "work" -}}
work-specific configuration
{{ else -}}
personal configuration
{{ end -}}
```

**Include files with change detection**:
```bash
# Hash triggers script rerun when file changes
# config.ini hash: {{ include "config.ini" | sha256sum }}
```

**For detailed template system documentation**, reference `references/templates.md`.

## Managing Secrets

Never commit plaintext secrets to the repository. Use these approaches:

### Password Manager Integration

Chezmoi provides built-in functions for major password managers:

**1Password**:
```go
{{ onepasswordRead "op://vault/item/field" }}
```

**Bitwarden**:
```go
{{ (bitwarden "item" "name").login.password }}
```

**Pass**:
```go
{{ pass "path/to/secret" }}
```

### Encryption

For secrets that must be stored in repository:

**Age encryption** (recommended):
```bash
# Generate key
chezmoi age decrypt --generate > ~/.config/chezmoi/key.txt

# Add encrypted file
chezmoi add --encrypt ~/.ssh/id_rsa
```

**GPG encryption**:
```bash
# Configure recipient in chezmoi.toml
chezmoi add --encrypt ~/.netrc
```

### Best Practice: Centralize Secret Retrieval

Call password managers once in config template (`.chezmoi.toml.tmpl`), not in every file template:

```toml
# .chezmoi.toml.tmpl
[data.secrets]
  github_token = {{ onepasswordRead "op://vault/github/token" | quote }}
  
# Then reference in templates:
# {{ .secrets.github_token }}
```

**For comprehensive secrets documentation**, reference `references/secrets.md`.

## Script Automation

Scripts execute during `chezmoi apply` to automate setup tasks.

### Script Types

- `run_before_*`: Runs before applying files (prerequisites)
- `run_after_*`: Runs after applying files (post-configuration)
- `run_onchange_*`: Runs when script content changes (recommended)
- `run_once_*`: Runs once per machine (tracked in state)
- `run_always_*`: Runs every time (use sparingly)

### Script Execution Order

Scripts execute alphabetically. Use numeric prefixes for control:
```bash
run_once_before_01-install-brew.sh
run_once_before_02-install-packages.sh
run_onchange_after_99-cleanup.sh
```

### Template Scripts

Add `.tmpl` suffix for platform-specific scripts:
```bash
# run_onchange_install-packages.sh.tmpl
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew install package
{{ else if eq .chezmoi.os "linux" -}}
#!/bin/bash
sudo apt install -y package
{{ end -}}
```

### Trigger on File Changes

Embed file hashes to rerun scripts when dependencies change:
```bash
# Brewfile hash: {{ include "Brewfile" | sha256sum }}
brew bundle --file={{ joinPath .chezmoi.sourceDir "Brewfile" | quote }}
```

### Best Practices

- Use `set -euo pipefail` in bash scripts
- Make scripts idempotent (safe to run multiple times)
- Check prerequisites before using commands
- Prefer `run_onchange_` over `run_always_`
- Use `run_once_` for expensive one-time operations

**For detailed script documentation**, reference `references/scripts.md`.

## External File Management

Manage files from external sources without storing them in repository.

### External Types

**.chezmoiexternal.toml.tmpl**:

**Single file**:
```toml
[".vim/autoload/plug.vim"]
  type = "file"
  url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
  refreshPeriod = "168h"
```

**Archive**:
```toml
[".oh-my-zsh"]
  type = "archive"
  url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
  exact = true
  stripComponents = 1
  refreshPeriod = "168h"
```

**Git repository**:
```toml
[".config/nvim"]
  type = "git-repo"
  url = "https://github.com/NvChad/NvChad.git"
  refreshPeriod = "168h"
```

**Platform-specific binary**:
```toml
[".local/bin/age"]
  type = "archive-file"
  url = "https://github.com/FiloSottile/age/releases/download/v1.1.1/age-v1.1.1-{{ .chezmoi.os }}-{{ .chezmoi.arch }}.tar.gz"
  executable = true
  path = "age/age"
  refreshPeriod = "168h"
```

### Refresh Management

Set `refreshPeriod` to avoid checking on every apply:
- Weekly: `168h`
- Daily: `24h`
- Manual only: `0`

Force refresh when needed:
```bash
chezmoi apply --refresh-externals
```

**For comprehensive externals documentation**, reference `references/externals.md`.

## Multi-Machine Configuration

### Recommended Strategy: Config File Data + OS Detection

**Each machine** (`~/.config/chezmoi/chezmoi.toml`):
```toml
[data]
  machine_class = "work"  # or "personal", "server"
  email = "john@company.com"

[data.features]
  work_tools = true
  gaming = false
```

**Templates** use both machine config and OS detection:
```bash
# dot_gitconfig.tmpl
[user]
  email = {{ .email | quote }}

{{ if eq .chezmoi.os "darwin" -}}
[credential]
  helper = osxkeychain
{{ end -}}

{{ if eq .machine_class "work" -}}
[http]
  proxy = http://proxy.company.com
{{ end -}}
```

**Control file installation** with `.chezmoiignore`:
```bash
{{ if ne .machine_class "work" }}
.work-config/**
{{ end }}

{{ if ne .chezmoi.os "darwin" }}
.config/aerospace/**
{{ end }}
```

### Machine-Specific Externals

Template `.chezmoiexternal.toml.tmpl` to download different tools per machine:
```toml
{{ if .features.work_tools -}}
[".local/bin/work-cli"]
  type = "file"
  url = "https://internal.company.com/cli"
{{ end -}}
```

**For multi-machine strategies and patterns**, reference `references/multi-machine.md`.

## Common Workflows

### Daily Workflow

```bash
# Edit file
chezmoi edit --watch ~/.zshrc

# Preview changes
chezmoi diff

# Apply changes
chezmoi apply

# Commit and push
chezmoi cd
git add .
git commit -m "Update config"
git push
```

### Multi-Machine Sync

**Machine A** (make changes):
```bash
chezmoi edit ~/.gitconfig
chezmoi apply
chezmoi cd && git add . && git commit -m "Update" && git push
```

**Machine B** (get changes):
```bash
chezmoi update  # Pull and apply
```

### New Machine Setup

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply username
```

**For detailed workflows and patterns**, reference `references/workflows.md`.

## Performance Optimization

### Key Optimizations

1. **Set refreshPeriod on externals**: Prevent checking on every apply
2. **Minimize password manager calls**: Call once in config template
3. **Use run_onchange over run_always**: Reduce script execution
4. **Simplify templates**: Extract complex logic to config
5. **Use .chezmoiignore**: Skip irrelevant files

### Measure Performance

```bash
time chezmoi apply
chezmoi apply --verbose 2>&1 | grep -E "took|duration"
```

**For comprehensive performance optimization**, reference `references/performance.md`.

## Troubleshooting

### Diagnostic Commands

```bash
# Quick health check
chezmoi doctor

# Show available data
chezmoi data

# Test template
chezmoi execute-template "{{ .variable }}"

# Preview file rendering
chezmoi cat ~/.gitconfig

# Debug mode
chezmoi apply --debug --dry-run
```

### Common Issues

**Template variable not found**:
```bash
chezmoi data | grep variable  # Check if defined
chezmoi edit-config           # Add to config
```

**Script not running**:
```bash
# Check naming (run_onchange_ prefix)
ls ~/.local/share/chezmoi/ | grep run_

# Clear state to force rerun
chezmoi state delete-bucket --bucket=scriptState
```

**Permission denied**:
```bash
# Make file executable or private
chezmoi chattr +executable ~/.local/bin/script
chezmoi chattr +private ~/.ssh/config
```

**Encryption fails**:
```bash
# Verify encryption key
ls ~/.config/chezmoi/key.txt
chezmoi cat-config | grep age
```

**For comprehensive troubleshooting**, reference `references/troubleshooting.md`.

## Advanced Patterns

### Template Fragments

Reuse common template logic:

```bash
# .chezmoitemplates/git-config
[user]
  name = "{{ .user.name }}"
  email = "{{ .user.email }}"

# In dot_gitconfig.tmpl:
{{ template "git-config" . }}
```

### Derived Data

Compute values once in config template:

```toml
# .chezmoi.toml.tmpl
[data]
{{- if and (eq .chezmoi.os "darwin") (eq .chezmoi.arch "arm64") }}
  platform = "macos-arm"
{{- else if eq .chezmoi.os "linux" }}
  platform = "linux"
{{- end }}

# Use in templates:
# {{ if eq .platform "macos-arm" }}...{{ end }}
```

### Feature Flags

Control optional functionality:

```toml
# chezmoi.toml
[data.features]
  experimental = true
  beta_ui = false
  work_tools = true
```

```bash
# In templates:
{{ if .features.experimental -}}
# experimental configuration
{{ end -}}
```

## Reference Documentation

This skill includes comprehensive reference documentation:

- **templates.md**: Complete template system guide with data sources, syntax, functions, and patterns
- **secrets.md**: Password manager integration, encryption (age/GPG), and best practices
- **scripts.md**: Script execution types, environment, error handling, and common patterns
- **externals.md**: External file management, types, refresh strategies, and troubleshooting
- **workflows.md**: Daily operations, multi-machine sync, file management patterns
- **troubleshooting.md**: Diagnostic commands, common issues, debugging techniques
- **performance.md**: Optimization strategies for externals, templates, scripts, and git
- **multi-machine.md**: Configuration strategies for managing multiple machines

Reference these documents for detailed information on specific topics.

## Best Practices Summary

1. **Version control everything**: Commit source directory to git
2. **Never commit secrets**: Use password managers or encryption
3. **Use templates wisely**: Only template files that need variation
4. **Make scripts idempotent**: Safe to run multiple times
5. **Set refreshPeriod**: On all external files
6. **Test before applying**: Use `--dry-run --verbose`
7. **Document machine setup**: README with initialization instructions
8. **Keep it simple**: Start basic, add complexity as needed
9. **Use feature flags**: Better than machine-specific conditionals
10. **Monitor performance**: Profile and optimize slow operations

## Getting Started

For new users or new machines:

1. Install chezmoi and initialize from repository
2. Configure machine-specific data in `~/.config/chezmoi/chezmoi.toml`
3. Preview changes with `chezmoi diff`
4. Apply dotfiles with `chezmoi apply`
5. Verify with `chezmoi doctor`

For advanced users:
- Reference detailed documentation in `references/` for specific topics
- Use `chezmoi execute-template` to test template logic
- Profile performance with `time chezmoi apply --verbose`
- Leverage all script types for comprehensive automation
- Implement multi-machine strategies for different environments
