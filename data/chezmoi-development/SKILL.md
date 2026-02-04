---
name: chezmoi-development
description: This skill should be used when developing or modifying dotfiles using chezmoi. Covers using .chezmoidata for configuration data and modify_ scripts (or run_onchange_after_ scripts for symlinked directories) for non-destructive file merging. Particularly useful when needing to configure application settings without overwriting user preferences.
---

# Chezmoi Development

## Overview

Develop dotfiles using chezmoi's advanced features for non-destructive configuration management. This skill focuses on two key patterns:
1. Using `.chezmoidata/` to store structured configuration data
2. Using `modify_` scripts (or `run_onchange_after_` scripts for symlinked directories) to merge configuration into existing files without overwriting user settings

## When to Use This Skill

Use this skill when:
- Developing dotfiles with chezmoi that need to configure applications
- Need to enforce required settings while preserving user preferences
- Managing JSON/YAML/TOML configuration files in dotfiles
- Application config files already exist and shouldn't be overwritten
- Working with dotfiles in a team where users may have custom settings

## Core Concepts

### .chezmoidata Directory

Store structured configuration as data files (YAML, JSON, or TOML) in `.chezmoidata/` at the root of the chezmoi source directory.

**Purpose:** Separate configuration data from templates, making it reusable across multiple files and easier to maintain.

**Location:** `~/.local/share/chezmoi/.chezmoidata/`

**Access in templates:** Reference data via dot notation (e.g., `{{ .app.config.setting }}`)

### modify_ Scripts vs run_onchange_ Scripts

There are two approaches for non-destructive configuration management in chezmoi:

#### modify_ Scripts (Preferred for regular directories)

Create executable scripts that transform existing files by reading them via stdin and outputting the modified version to stdout.

**Purpose:** Update existing files non-destructively by merging new config with existing content.

**Naming:** `modify_` + target file path + `.tmpl`
- Example: `modify_dot_config/app/settings.json.tmpl` → modifies `~/.config/app/settings.json`

**Execution:** chezmoi runs the script, captures stdout, and writes it to the target file.

**How it works:** Chezmoi provides file contents via **stdin** (use `cat -` to read), script outputs merged result to **stdout**.

**Limitation:** Cannot be used when the target directory is a symlink (chezmoi requires managing the directory).

#### run_onchange_after_ Scripts (For symlinked directories)

Create executable scripts in `.chezmoiscripts/` that read from disk and write back to disk.

**Purpose:** Update files in directories that may be symlinks (common in Coder workspaces).

**Naming:** `run_onchange_after_<name>.sh.tmpl` in `.chezmoiscripts/`
- Example: `.chezmoiscripts/run_onchange_after_update-claude-settings.sh.tmpl`

**Execution:** Script runs after other chezmoi operations, whenever the rendered script content changes.

**How it works:** Script reads from disk (`cat "$FILE"`), merges config, writes back to disk (`echo "$result" > "$FILE"`).

**Use when:** Target directory is or may be a symlink, preventing chezmoi from managing individual files within it.

## Workflow: Implementing Non-Destructive Config Management

Follow this workflow when implementing configuration management for an application:

### Step 1: Define Configuration Data

Create a data file in `.chezmoidata/` with the configuration to enforce.

**Choose file format based on data complexity:**
- YAML for nested structures with comments
- JSON for simple data or when templates need JSON output
- TOML for flat key-value pairs

**Example - `.chezmoidata/myapp.yaml`:**
```yaml
---
# Application configuration to enforce
required_settings:
  feature_flag: true
  api_endpoint: "https://api.example.com"

optional_defaults:
  theme: "dark"
  timeout: 30
```

**Access in templates:**
```bash
{{ .myapp.required_settings.feature_flag }}
{{ .myapp.optional_defaults.theme }}
```

### Step 2: Create modify_ Script

Create a script that merges configuration data into the target file.

**Script requirements:**
1. Read existing file from stdin (NOT from disk!)
2. Load configuration from `.chezmoidata` via template
3. Merge configuration (required settings take precedence)
4. Output merged result to stdout

**File naming for modify_ scripts:**
- For `~/.config/myapp/settings.json` → `dot_config/myapp/modify_settings.json.tmpl`
- The directory structure mirrors the target path
- The `modify_` prefix goes on the **filename** (not the directory)
- The file must be executable (`chmod +x`)

**Example - `dot_config/myapp/modify_settings.json.tmpl`:**
```bash
{{- if .include_defaults -}}
#!/bin/bash
set -e

# Read existing settings from stdin (chezmoi provides current file contents)
# If stdin is empty (file doesn't exist), use empty object
existing=$(cat - || echo '{}')
if [ -z "$existing" ]; then
    existing='{}'
fi

# Load configuration from .chezmoidata
required='{{ .myapp.required_settings | toJson }}'
defaults='{{ .myapp.optional_defaults | toJson }}'

# Merge: existing + defaults + required (right side wins)
echo "$existing" | jq --argjson defaults "$defaults" \
                       --argjson required "$required" \
                       '. * $defaults * $required'
{{- end }}
```

**CRITICAL for modify_ scripts:** Chezmoi provides file contents via **stdin**, not by file path. Always use `cat -` to read from stdin. (Note: `run_onchange_` scripts read from disk instead - see the distinction in Core Concepts above.)

**For YAML files, use `yq` instead of `jq`:**
```bash
# Merge YAML files
existing=$(cat "$HOME/.config/app/config.yaml" || echo '{}')
required='{{ .app.config | toYaml }}'
echo "$existing" | yq eval-all '. as $item ireduce ({}; . * $item)' - <(echo "$required")
```

### Step 3: Make Script Executable (Optional - if needed)

Ensure the modify script is executable in the source directory:

```bash
chmod +x ~/.local/share/chezmoi/dot_config/myapp/modify_settings.json.tmpl
```

**Note:** Chezmoi automatically creates parent directories when writing files, so you typically don't need `run_before_` scripts just to create directories.

**Only use `run_before_` scripts when you need to:**
- Remove old symlinks that would conflict with new files
- Set special directory permissions
- Install dependencies (like `jq` for JSON processing)

### Step 4: Test the Implementation

Preview changes before applying:

```bash
# View what would be written to the file
chezmoi cat ~/.config/myapp/settings.json

# Show diff between current and new state
chezmoi diff

# Apply with dry run
chezmoi apply --dry-run --verbose
```

Test merge logic manually:

```bash
# Extract and test the modify script
chezmoi execute-template < modify_dot_config/myapp/settings.json.tmpl > /tmp/test_modify.sh
chmod +x /tmp/test_modify.sh

# Test with sample input
echo '{"userSetting":"value"}' | /tmp/test_modify.sh
```

## Common Patterns

### Pattern: Merge with jq

Merge JSON objects where required settings override existing ones:

```bash
echo "$existing" | jq --argjson required "$required_settings" \
                       '. * $required'
```

The `*` operator performs recursive merge with right-side precedence.

### Pattern: Conditional Configuration

Apply different config based on environment or profile:

```yaml
# .chezmoidata/app.yaml
{{ if eq .profile "work" -}}
config:
  api_url: "https://work.api.com"
{{ else if eq .profile "personal" -}}
config:
  api_url: "https://personal.api.com"
{{ end -}}
```

### Pattern: Environment Variable References

Include environment variables in configuration:

```yaml
# .chezmoidata/app.yaml
config:
  api_key: "{{ env "APP_API_KEY" }}"
  debug: {{ env "DEBUG" | default "false" }}
```

### Pattern: Multi-File Configuration

Use same data across multiple files:

```
.chezmoidata/
  brand.yaml                          # Logo paths, colors, fonts

modify_dot_config/app1/settings.json.tmpl   # References {{ .brand.logo }}
modify_dot_config/app2/config.toml.tmpl     # References {{ .brand.colors }}
dot_bashrc.tmpl                             # References {{ .brand.theme }}
```

## Symlinks and Execution Order

### Using symlink_ Prefix

Chezmoi creates symlinks declaratively using the `symlink_` prefix in the source state.

**Naming:** `symlink_` + target path + `.tmpl` (template optional)
- Example: `symlink_dot_config/app.tmpl` → creates symlink at `~/.config/app`

**Content:** The file content (with trailing newline stripped) becomes the symlink target.

**Example - `symlink_dot_config/myapp.tmpl`:**
```bash
{{ if eq .profile "work" -}}
/shared/work/.config/myapp
{{ else -}}
/shared/default/.config/myapp
{{ end -}}
```

**Conditional symlinks:**
```bash
{{- if .is_coder -}}
/shared/.config/app
{{- end -}}
```

If the content is empty or whitespace-only after template processing, the symlink is removed.

### Execution Order

Understanding execution order is critical to avoid race conditions:

1. **Read source state** - Parse all files in chezmoi source directory
2. **Read destination state** - Check current state of target files
3. **Compute target state** - Determine what changes are needed
4. **Run `run_before_` scripts** - Execute in alphabetical order
5. **Update entries** - Process all entries in alphabetical order by target name:
   - Regular files (`dot_`, `private_`, etc.)
   - Symlinks (`symlink_`)
   - Modified files (`modify_`)
   - Directories
   - Scripts (`run_`)
6. **Run `run_after_` scripts** - Execute in alphabetical order

**Key insight:** All entry types (files, symlinks, modify scripts) are processed together in step 5, sorted alphabetically by their final target path.

### Avoiding Race Conditions

**❌ WRONG - Creating directory in run_before prevents symlinking:**
```bash
# .chezmoiscripts/run_before_00_setup.sh.tmpl
mkdir -p "$HOME/.config/app"

# Later, this fails because ~/.config/app already exists as a directory
# symlink_dot_config/app.tmpl
/shared/.config/app
```

**✅ CORRECT - Use symlink_ declaratively:**
```bash
# symlink_dot_config/app.tmpl
{{ if .is_coder -}}
/shared/.config/app
{{ end -}}

# modify_dot_config/app/settings.json.tmpl
# This works because symlink is created first (alphabetically)
```

**✅ ALSO CORRECT - Let chezmoi create directories automatically:**
```bash
# No run_before script needed!
# modify_dot_config/app/settings.json.tmpl
# Chezmoi automatically creates ~/.config/app/ when writing the file
```

### When to Use Each Approach

| Approach | Use When | Example |
|----------|----------|---------|
| `symlink_` | Entire directory should point elsewhere | Link `~/.config/app` → `/shared/.config/app` |
| `modify_` | Merge config into existing file | Merge marketplace config into `settings.json` |
| `dot_` regular file | Fully manage file content | Template `~/.bashrc` from scratch |
| `run_before_` | Install dependencies, clean up old state | Install `jq`, remove old symlinks |
| `run_after_` | Post-install tasks, restart services | Run `systemctl --user daemon-reload` |

**IMPORTANT:** Chezmoi automatically creates parent directories when writing files. You do NOT need `run_before_` scripts to create directories for `modify_` scripts or regular files.

### Pattern: Conditional Symlinking in Coder

For Coder workspaces with persistent `/shared/` storage:

```bash
# symlink_dot_config/gh.tmpl - Link to shared GitHub CLI config
{{- if .is_coder -}}
/shared/.config/gh
{{- end -}}
```

If `.is_coder` is false, the symlink won't be created. If it's true, the symlink points to persistent storage.

### Pattern: Symlink vs Modify Decision

**Use symlink when:**
- Entire directory managed externally (e.g., `/shared/`)
- Content is already in a persistent location
- No need to merge with existing content

**Use modify when:**
- Need to merge with existing user settings
- Want to preserve user customizations
- Enforcing required settings while allowing optional ones

**Example scenario - Claude Code config:**
```bash
# ❌ BAD - Symlink loses user settings
symlink_dot_claude.tmpl → /shared/.claude

# ✅ GOOD - Modify merges marketplace config with user settings
modify_dot_claude/settings.json.tmpl → merges settings
```

## Best Practices

### Parent Directories Are Created Automatically

Chezmoi creates parent directories automatically. Do NOT create directories in `run_before_` scripts unless you have a specific reason (like setting permissions).

**❌ Unnecessary:**
```bash
# .chezmoiscripts/run_before_setup.sh.tmpl
mkdir -p "$HOME/.config/app"  # Chezmoi will do this!
```

**✅ Only when needed:**
```bash
# .chezmoiscripts/run_before_setup.sh.tmpl
# Only if you need special permissions
mkdir -p "$HOME/.config/app"
chmod 700 "$HOME/.config/app"
```

### Always Handle Missing Files

Check if target file exists before reading:

```bash
if [ -f "$HOME/.config/app/settings.json" ]; then
    existing=$(cat "$HOME/.config/app/settings.json")
else
    existing='{}'  # Sensible default
fi
```

### Validate JSON/YAML Before Writing

Ensure output is valid before chezmoi writes it:

```bash
# Validate JSON
result=$(echo "$existing" | jq --argjson required "$required" '. * $required')
echo "$result" | jq empty  # Will fail if invalid
echo "$result"
```

### Use Template Guards

Control when scripts execute based on configuration:

```bash
{{ if .include_defaults -}}
# Only execute when include_defaults is true
{{ end -}}

{{ if eq .profile "work" -}}
# Only execute for work profile
{{ end -}}
```

### Separate Data from Logic

**❌ Bad - Hardcode config in template:**
```bash
echo '{"api":"https://api.com","timeout":30}' > ~/.app/config.json
```

**✅ Good - Reference .chezmoidata:**
```yaml
# .chezmoidata/app.yaml
config:
  api: "https://api.com"
  timeout: 30
```

```bash
# modify_dot_app/config.json.tmpl
echo '{{ .app.config | toJson }}'
```

### Document Configuration Structure

Add comments to data files explaining what each setting does:

```yaml
---
# Database configuration for application
database:
  # Maximum number of connections in the pool
  max_connections: 100

  # Connection timeout in seconds
  timeout: 30

  # Enable query logging (set to false in production)
  log_queries: true
```

### Script Ordering Matters

Use clear numeric prefixes to control execution order:

```
.chezmoiscripts/
  run_before_00_install-dependencies.sh.tmpl
  run_before_10_setup-directories.sh.tmpl
  run_before_20_remove-old-symlinks.sh.tmpl
  run_onchange_after_50_configure-apps.sh.tmpl
```

## Troubleshooting

### Race Condition: Directory Created Before Symlink

**Problem:** Want to symlink a directory, but it already exists as a real directory.

**Cause:** A `run_before_` script or another entry creates the directory before the symlink is processed.

**Solution 1 - Remove directory creation:**
```bash
# Delete the run_before script that creates the directory
# Let chezmoi handle it via symlink_ or modify_
```

**Solution 2 - Use symlink_ declaratively:**
```bash
# symlink_dot_config/app.tmpl
/shared/.config/app

# Don't create ~/.config/app anywhere else!
```

**Solution 3 - Remove existing directory:**
```bash
# .chezmoiscripts/run_before_00_cleanup.sh.tmpl
if [ -d "$HOME/.config/app" ] && [ ! -L "$HOME/.config/app" ]; then
    # Backup if needed
    [ -n "$(ls -A "$HOME/.config/app")" ] && \
        mv "$HOME/.config/app" "$HOME/.config/app.backup.$(date +%s)"
    rm -rf "$HOME/.config/app"
fi
```

### modify_ Script Not Running

**Check template guard:**
```bash
# View rendered script to see if template guard blocked it
chezmoi execute-template < modify_dot_app/settings.json.tmpl
```

**Verify script is executable:**
```bash
chmod +x ~/.local/share/chezmoi/modify_dot_app/settings.json.tmpl
```

### Data Not Available in Template

**List all available template data:**
```bash
chezmoi data | jq
```

**Check .chezmoidata file is valid:**
```bash
# For YAML
yq eval .chezmoidata/app.yaml

# For JSON
jq . .chezmoidata/app.json
```

### Merge Produces Incorrect Result

**Test jq merge manually:**
```bash
existing='{"user":"setting"}'
required='{"new":"value"}'

echo "$existing" | jq --argjson required "$required" '. * $required'
```

**Check operator precedence:**
- `*` recursive merge (right side wins)
- `+` concatenate (arrays append, objects merge)

### Script Fails with "command not found"

**Ensure dependencies are installed in run_before script:**
```bash
# .chezmoiscripts/run_before_00_install-jq.sh.tmpl
#!/bin/bash
if ! command -v jq &> /dev/null; then
    if [ "$(uname)" = "Darwin" ]; then
        brew install jq
    else
        sudo apt-get install -y jq
    fi
fi
```

## Declarative Package Installation

Chezmoi can install packages declaratively using a combination of `.chezmoidata/packages.yaml` and `run_onchange_` scripts. This pattern ensures packages are installed when the package list changes.

### Pattern: npm Package Installation

**1. Declare packages in `.chezmoidata/packages.yaml`:**
```yaml
---
# Package declarations for declarative installation
# Top-level keys become template variables (e.g., .npm, .apt, .brew)
npm:
  global:
    - "@anthropic-ai/claude-code"
    - "typescript"
```

**2. Create installation script `.chezmoiscripts/run_onchange_after_install-npm-packages.sh.tmpl`:**
```bash
#!/bin/bash
# Install npm packages declaratively based on .chezmoidata/packages.yaml
# This script runs when the package list changes

{{ if .include_defaults -}}
set -e

# Function to run npm commands via mise
run_npm() {
    if command -v mise >/dev/null 2>&1; then
        mise exec -- npm "$@"
    else
        npm "$@"
    fi
}

# Check if npm is available (via mise or directly)
if command -v mise >/dev/null 2>&1; then
    if ! mise exec -- npm --version >/dev/null 2>&1; then
        echo "⚠️  Node.js/npm not available via mise. Skipping npm package installation."
        exit 0
    fi
elif ! command -v npm >/dev/null 2>&1; then
    echo "⚠️  npm not found. Skipping npm package installation."
    exit 0
fi

# Install global npm packages
{{ if .npm.global -}}
{{ range .npm.global -}}
if ! run_npm list -g "{{ . }}" >/dev/null 2>&1; then
    echo "📦 Installing {{ . }}..."
    run_npm install -g "{{ . }}"
    echo "✓ Installed {{ . }}"
else
    echo "✓ {{ . }} already installed"
fi
{{ end -}}
{{ end -}}

{{ end -}}
```

**How it works:**
- The script template references `.npm.global` from `.chezmoidata/packages.yaml`
- `run_onchange_` prefix means the script executes when its rendered content changes
- When you add/remove packages in `packages.yaml`, the rendered script changes, triggering re-execution
- Each package is checked before installation to avoid redundant installs
- Uses `mise exec` to ensure npm is available from mise-managed Node.js

**Adaptable to other package managers:**
- apt: Create `.chezmoidata/packages.yaml` with `apt: [...]` and use `{{ range .apt }}`
- brew: Create with `brew: [...]` and use `{{ range .brew }}`
- pip: Create with `pip: [...]` and use `{{ range .pip }}`

## Reference Documentation

For a complete, working example of this pattern, see:
- `references/chezmoidata-modify-example.md` - Real-world Claude Code marketplace configuration

## Quick Reference

| Task | Command |
|------|---------|
| Preview file output | `chezmoi cat ~/.config/app/settings.json` |
| Show changes | `chezmoi diff` |
| Test template | `chezmoi execute-template < file.tmpl` |
| View template data | `chezmoi data` |
| Apply changes | `chezmoi apply` |
| Dry run | `chezmoi apply --dry-run --verbose` |

| Pattern | Purpose |
|---------|---------|
| `.chezmoidata/app.yaml` | Store structured configuration data |
| `modify_dot_app/config.json.tmpl` | Merge config into existing file |
| `run_before_00_setup.sh.tmpl` | Ensure prerequisites before applying |
| `{{ .app.setting \| toJson }}` | Convert data to JSON in template |
| `jq '. * $required'` | Merge JSON with right-side precedence |
