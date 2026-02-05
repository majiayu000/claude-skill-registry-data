---
name: chezmoi
description: Chezmoi dotfile management expertise
---

# Chezmoi Expertise

Comprehensive guidance on managing dotfiles with chezmoi, including templating,
cross-platform configuration, and secret management.

## File Naming Conventions

### Prefix System

- `dot_` → `.` (hidden files)
- `private_` → Sets 0600 permissions
- `readonly_` → Sets 0444 permissions
- `executable_` → Sets executable bit
- `run_` → Scripts that run (once, onchange, always)
- `modify_` → Modifies existing files
- `create_` → Creates files if they don't exist
- `symlink_` → Creates symbolic links

### Suffix System

- `.tmpl` → Go template files
- `.literal` → Treat as literal (no templating)

### Examples

```
dot_zshrc.tmpl → ~/.zshrc (templated)
private_dot_ssh/config.tmpl → ~/.ssh/config (0600, templated)
run_onchange_install-packages.sh.tmpl → Runs when content changes
```

## Templating System

### Template Variables

```go
{{ .chezmoi.hostname }}     // Machine hostname
{{ .chezmoi.os }}          // Operating system (darwin, linux, windows)
{{ .chezmoi.arch }}        // Architecture (amd64, arm64)
{{ .chezmoi.username }}    // Current username
{{ .chezmoi.homeDir }}     // Home directory path
{{ .chezmoi.sourceDir }}   // Chezmoi source directory
```

### Conditional Logic

```go
{{ if eq .chezmoi.os "darwin" }}
  # macOS-specific configuration
{{ else if eq .chezmoi.os "linux" }}
  # Linux-specific configuration
{{ end }}

{{ if .is_work_machine }}
  # Work-specific settings
{{ end }}
```

### Advanced Templates

```go
{{- $email := promptStringOnce . "email" "Email address" -}}
export EMAIL="{{ $email }}"

{{- if hasKey . "gpg_key" }}
export GPG_KEY="{{ .gpg_key }}"
{{- end }}
```

## Data Management

### Configuration File (.chezmoi.toml.tmpl)

```toml
[data]
    email = "user@example.com"
    is_work_machine = false

[data.github]
    username = "myusername"

[diff]
    exclude = ["scripts"]

[merge]
    command = "nvim"
    args = ["-d", "{{ .Destination }}", "{{ .Source }}"]
```

### External Data Sources

```toml
[data]
    weather = """{{ output "curl" "-s" "wttr.in/?format=%c+%t" }}"""
    hostname = """{{ output "hostname" "-s" }}"""
```

## Secret Management

### Password Manager Integration

```go
# Bitwarden
export GITHUB_TOKEN="{{ (bitwarden "item" "github-token").login.password }}"

# 1Password
export API_KEY="{{ onepasswordRead "op://Personal/API Key/password" }}"

# Encrypted files
{{ includeTemplate "private_dot_ssh/id_rsa.tmpl" . | decrypt }}
```

### Encryption

```bash
# Encrypt a file
chezmoi add --encrypt ~/.ssh/id_rsa

# Decrypt for editing
chezmoi edit ~/.ssh/id_rsa

# Set encryption method in .chezmoi.toml
encryption = "age"  # or "gpg"
```

## Scripts and Hooks

### Script Types

- `run_once_` → Runs once only
- `run_onchange_` → Runs when script content changes
- `run_always_` → Runs every time

### Script Ordering

- `run_before_` → Before applying dotfiles
- `run_after_` → After applying dotfiles
- Numeric prefixes for order: `run_onchange_before_10-install.sh`

### Example Script

```bash
# run_onchange_before_install-packages.sh.tmpl
#!/bin/bash
{{ if eq .chezmoi.os "darwin" -}}
brew bundle --file=- <<EOF
{{ range .packages.darwin -}}
{{ . }}
{{ end -}}
EOF
{{ else if eq .chezmoi.os "linux" -}}
sudo apt-get update
sudo apt-get install -y {{ range .packages.linux }}{{ . }} {{ end }}
{{ end -}}
```

## Directory Management

### Directory Attributes

```
.chezmoiremove     # Files to remove
.chezmoiignore     # Files to ignore
.chezmoitemplates  # Shared templates
.chezmoiexternal   # External files to download
```

### External Files (.chezmoiexternal.toml)

```toml
[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    exact = true
    stripComponents = 1

[".config/nvim/autoload/plug.vim"]
    type = "file"
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
```

## Best Practices

### Repository Organization

```
~/dotfiles/
├── dot_config/
│   ├── nvim/
│   └── git/
├── private_dot_ssh/
├── dot_zshrc.tmpl
├── .chezmoi.toml.tmpl
├── .chezmoiignore
└── run_onchange_install-packages.sh.tmpl
```

### Idempotency

- Use `run_onchange_` for package installation
- Check for command existence before installing
- Use `modify_` for partial file changes

### Cross-Platform Configuration

```go
{{ $configDir := .chezmoi.homeDir }}
{{ if eq .chezmoi.os "darwin" }}
    {{ $configDir = printf "%s/Library/Application Support" .chezmoi.homeDir }}
{{ else }}
    {{ $configDir = printf "%s/.config" .chezmoi.homeDir }}
{{ end }}
```

## Common Patterns

### Machine-Specific Configuration

```toml
# .chezmoi.toml.tmpl
{{ $hostname := .chezmoi.hostname }}
{{ if eq $hostname "work-laptop" }}
[data]
    is_work_machine = true
    proxy = "http://proxy.company.com:8080"
{{ else }}
[data]
    is_work_machine = false
{{ end }}
```

### Git Configuration

```ini
# dot_gitconfig.tmpl
[user]
    name = {{ .name | quote }}
    email = {{ .email | quote }}
{{ if .is_work_machine }}
    signingkey = {{ .work_gpg_key | quote }}
{{ end }}

[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
```

## Essential Commands

```bash
chezmoi init                    # Initialize chezmoi
chezmoi add ~/.zshrc           # Add a file
chezmoi edit ~/.zshrc          # Edit the source file
chezmoi diff                   # Show what would change
chezmoi apply                  # Apply changes
chezmoi update                 # Pull and apply latest

# Working with templates
chezmoi execute-template < file.tmpl  # Test templates
chezmoi data                         # Show template data

# Managing secrets
chezmoi add --encrypt file          # Add encrypted
chezmoi decrypt file               # Decrypt file
```

## Error Prevention

### Common Pitfalls

1. **Template Syntax**: Always use `{{-` and `-}}` to control whitespace
2. **File Permissions**: Remember `private_` prefix for sensitive files
3. **Script Dependencies**: Check for tools before using in scripts
4. **Circular Templates**: Avoid templates including themselves

### Debugging

```bash
chezmoi doctor                 # Check configuration
chezmoi verify                 # Verify dotfiles
chezmoi apply --dry-run -v    # Verbose dry run
```

## Template Functions

```go
# String functions
{{ .variable | quote }}        # Quote a string
{{ .variable | upper }}        # Uppercase
{{ .variable | lower }}        # Lowercase
{{ printf "%s/%s" .dir .file }}  # Format string

# Conditionals
{{ if eq .var "value" }}...{{ end }}
{{ if ne .var "value" }}...{{ end }}
{{ if and .a .b }}...{{ end }}
{{ if or .a .b }}...{{ end }}

# Includes
{{ include "template-name" . }}
{{ includeTemplate "file.tmpl" . }}
```
