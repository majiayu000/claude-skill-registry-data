---
name: sindri-extension-guide
description: Guide users through creating Sindri extensions. Use when creating new extensions, understanding extension.yaml structure, validating extensions against schemas, or learning about extension installation methods (mise, apt, binary, npm, script, hybrid). Helps with extension development, registry updates, and category assignment.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Sindri Extension Development Guide

## Slash Commands (Recommended)

For reliable extension creation with all documentation updates, use these commands:

| Command                          | Purpose                                                   |
| -------------------------------- | --------------------------------------------------------- |
| `/extension/new <name> [source]` | Create new extension with complete documentation workflow |
| `/extension/update-docs <name>`  | Update documentation for existing extension               |

**Example:**

```
/extension/new mdflow https://github.com/johnlindquist/mdflow
/extension/update-docs nodejs
```

These commands enforce the complete workflow including all required documentation updates.

---

## Overview

This skill guides you through creating declarative YAML extensions for Sindri. Extensions are **YAML files, not bash scripts** - all configuration is driven by declarative YAML definitions.

## Documentation Locations

**IMPORTANT:** After creating any extension, you must update the relevant documentation.

### Key Documentation Files

| Type                | Path                                       | Purpose                            |
| ------------------- | ------------------------------------------ | ---------------------------------- |
| **Schema**          | `docker/lib/schemas/extension.schema.json` | Extension validation schema        |
| **Registry**        | `docker/lib/registry.yaml`                 | Master extension registry          |
| **Profiles**        | `docker/lib/profiles.yaml`                 | Extension profile definitions      |
| **Categories**      | `docker/lib/categories.yaml`               | Category definitions               |
| **Extension Docs**  | `docs/extensions/{NAME}.md`                | Individual extension documentation |
| **Catalog**         | `docs/EXTENSIONS.md`                       | Overview of all extensions         |
| **Authoring Guide** | `docs/EXTENSION_AUTHORING.md`              | Detailed authoring reference       |
| **Slides**          | `docs/slides/extensions.html`              | Visual presentation                |

## Quick Start Checklist

1. [ ] Create directory: `docker/lib/extensions/{name}/`
2. [ ] Create `extension.yaml` with required sections
3. [ ] Add to `docker/lib/registry.yaml`
4. [ ] Validate: `./cli/extension-manager validate {name}`
5. [ ] Test: `./cli/extension-manager install {name}`
6. [ ] **Update documentation** (see Post-Extension Checklist below)

## Extension Directory Structure

```text
docker/lib/extensions/{extension-name}/
├── extension.yaml       # Required: Main definition
├── scripts/             # Optional: Custom scripts
│   ├── install.sh       # Custom installation
│   ├── uninstall.sh     # Custom removal
│   └── validate.sh      # Custom validation
├── templates/           # Optional: Config templates
│   └── config.template
└── mise.toml            # Optional: mise configuration
```

## Minimal Extension Template

```yaml
metadata:
  name: my-extension
  version: 1.0.0
  description: Brief description (10-200 chars)
  category: dev-tools
  dependencies: []

install:
  method: mise
  mise:
    configFile: mise.toml

validate:
  commands:
    - name: mytool
      versionFlag: --version
      expectedPattern: "v\\d+\\.\\d+\\.\\d+"
```

## Extension YAML Sections

### 1. Metadata (Required)

```yaml
metadata:
  name: extension-name # lowercase with hyphens
  version: 1.0.0 # semantic versioning
  description: What it does # 10-200 characters
  category: dev-tools # see categories below
  author: Your Name # optional
  homepage: https://... # optional
  dependencies: # other extensions needed
    - nodejs
    - python
```

**Valid Categories:**

- `base` - Core system components
- `language` - Programming runtimes (Node.js, Python, etc.)
- `dev-tools` - Development tools (linters, formatters)
- `infrastructure` - Cloud/container tools (Docker, K8s, Terraform)
- `ai` - AI/ML tools and frameworks
- `agile` - Project management tools (Jira, Linear)
- `database` - Database servers
- `monitoring` - Observability tools
- `mobile` - Mobile SDKs
- `desktop` - GUI environments
- `utilities` - General tools

### 2. Requirements (Optional)

```yaml
requirements:
  domains: # Network access needed
    - api.github.com
    - registry.npmjs.org
  diskSpace: 500 # MB required
  secrets: # Credentials needed
    - GITHUB_TOKEN
```

### 3. Install (Required)

Choose ONE installation method:

**mise** (recommended for language tools):

```yaml
install:
  method: mise
  mise:
    configFile: mise.toml # Reference to mise config
    reshim: true # Rebuild shims after install
```

**apt** (system packages):

```yaml
install:
  method: apt
  apt:
    repositories:
      - name: docker
        key: https://download.docker.com/linux/ubuntu/gpg
        url: https://download.docker.com/linux/ubuntu
        suite: jammy
        component: stable
    packages:
      - docker-ce
      - docker-ce-cli
```

**binary** (direct download):

```yaml
install:
  method: binary
  binary:
    url: https://github.com/org/repo/releases/download/v1.0.0/tool-linux-amd64.tar.gz
    extract: tar.gz # tar.gz, zip, or none
    destination: ~/.local/bin/tool
```

**npm** (Node.js packages):

```yaml
install:
  method: npm
  npm:
    packages:
      - typescript
      - eslint
    global: true
```

**script** (custom installation):

```yaml
install:
  method: script
  script:
    path: scripts/install.sh
    timeout: 300 # seconds (default: 300)
```

**hybrid** (multiple methods):

```yaml
install:
  method: hybrid
  hybrid:
    steps:
      - method: apt
        apt:
          packages: [build-essential]
      - method: script
        script:
          path: scripts/install.sh
```

### 4. Configure (Optional)

```yaml
configure:
  templates:
    - source: templates/config.template
      destination: ~/.config/tool/config.yaml
      mode: overwrite # overwrite|append|merge|skip-if-exists
  environment:
    - key: TOOL_HOME
      value: $HOME/.tool
      scope: bashrc # bashrc|profile|session
```

### 5. Validate (Required)

```yaml
validate:
  commands:
    - name: tool-name
      versionFlag: --version
      expectedPattern: "\\d+\\.\\d+\\.\\d+"
  mise:
    tools:
      - node
      - python
    minToolCount: 2
  script:
    path: scripts/validate.sh
    timeout: 60
```

### 6. Remove (Optional)

```yaml
remove:
  confirmation: true
  mise:
    removeConfig: true
    tools: [node, python]
  apt:
    packages: [package-name]
    purge: false
  script:
    path: scripts/uninstall.sh
  paths:
    - ~/.config/tool
    - ~/.local/share/tool
```

### 7. Upgrade (Optional)

```yaml
upgrade:
  strategy: automatic # automatic|manual|none
  mise:
    upgradeAll: true
  apt:
    packages: [package-name]
    updateFirst: true
  script:
    path: scripts/upgrade.sh
```

### 8. Bill of Materials (Optional but Recommended)

```yaml
bom:
  tools:
    - name: node
      version: dynamic # or specific version
      source: mise
      type: runtime
      license: MIT
      homepage: https://nodejs.org
```

## Adding to Registry

After creating your extension, add it to `docker/lib/registry.yaml`:

```yaml
extensions:
  my-extension:
    category: dev-tools
    description: Short description
    dependencies: [nodejs]
    protected: false
```

## Validation Commands

```bash
# Validate single extension
./cli/extension-manager validate my-extension

# Validate all extensions
./cli/extension-manager validate-all

# Check extension info
./cli/extension-manager info my-extension

# Test installation
./cli/extension-manager install my-extension

# Check status
./cli/extension-manager status my-extension
```

## Common Patterns

### Language Runtime (mise-based)

Best for: Node.js, Python, Go, Rust, Ruby

- Use `method: mise` with a `mise.toml` config file
- Set appropriate environment variables in configure section
- Validate with version command

### Development Tool (npm-based)

Best for: TypeScript, ESLint, Prettier

- Depend on `nodejs` extension
- Use `method: npm` with global packages
- Add configuration templates

### CLI Tool (binary download)

Best for: GitHub releases, standalone binaries

- Use `method: binary` with GitHub release URL
- Handle extraction (tar.gz, zip)
- Validate binary exists and runs

### Complex Setup (hybrid)

Best for: Desktop environments, multi-step installs

- Use `method: hybrid` with ordered steps
- Combine apt + script for flexibility
- Include cleanup in remove section

## Script Guidelines

All scripts must:

1. Start with `#!/usr/bin/env bash`
2. Include `set -euo pipefail`
3. Exit 0 on success, non-zero on failure
4. Use `$HOME`, `$WORKSPACE` environment variables
5. Log progress with echo statements

Example:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Installing my-tool..."
# Installation commands here
echo "my-tool installed successfully"
```

## Troubleshooting

| Issue                   | Solution                                  |
| ----------------------- | ----------------------------------------- |
| Schema validation fails | Check YAML syntax, verify required fields |
| Dependencies not found  | Add missing extensions to registry.yaml   |
| Install times out       | Increase timeout in script section        |
| Validation fails        | Check expectedPattern regex escaping      |
| Permission denied       | Scripts must be executable                |

---

## Post-Extension Documentation Checklist

**CRITICAL:** After creating or modifying an extension, you MUST complete these documentation updates:

### Required Updates (Always Do These)

- [ ] **Registry Entry** - Add to `docker/lib/registry.yaml`

  ```yaml
  extensions:
    my-extension:
      category: dev-tools
      description: Short description
      dependencies: []
  ```

- [ ] **Extension Documentation** - Create `docs/extensions/{NAME}.md`
  - Use UPPERCASE for filename (e.g., `NODEJS.md`, `AI-TOOLKIT.md`)
  - Include: overview, installation, configuration, usage examples
  - For VisionFlow: `docs/extensions/vision-flow/VF-{NAME}.md`

- [ ] **Extension Catalog** - Update `docs/EXTENSIONS.md`
  - Add to appropriate category table
  - Include link to extension doc

### Conditional Updates (When Applicable)

- [ ] **Profiles** - If adding extension to profiles:
  - Update `docker/lib/profiles.yaml`
  - Update relevant profile descriptions in `docs/EXTENSIONS.md`

- [ ] **Categories** - If adding new category:
  - Update `docker/lib/categories.yaml`
  - Update `docker/lib/schemas/extension.schema.json` (category enum)
  - Update category docs in `docs/EXTENSIONS.md`

- [ ] **Schema** - If adding new extension fields:
  - Update `docker/lib/schemas/extension.schema.json`
  - Update `docs/SCHEMA.md`
  - Update `REFERENCE.md` in this skill

- [ ] **Slides** - If extension is notable/featured:
  - Update `docs/slides/extensions.html`

### VisionFlow-Specific Updates

- [ ] Update `docs/extensions/vision-flow/README.md`
- [ ] Update `docs/extensions/vision-flow/CAPABILITY-CATALOG.md`
- [ ] Update VisionFlow profile if applicable

### Validation After Updates

```bash
# Validate YAML files
pnpm validate:yaml

# Lint markdown
pnpm lint:md

# Validate extension
./cli/extension-manager validate {name}
```

---

## Extension Documentation Template

When creating `docs/extensions/{NAME}.md`, use this template:

```markdown
# {Extension Name}

{Brief description of what the extension provides.}

## Overview

{More detailed explanation of the extension's purpose and capabilities.}

## Installation

\`\`\`bash
extension-manager install {name}
\`\`\`

## What Gets Installed

- {Tool 1} - {purpose}
- {Tool 2} - {purpose}

## Configuration

{Any configuration options or environment variables.}

## Usage

{Usage examples.}

## Dependencies

{List any extension dependencies.}

## Requirements

- **Disk Space:** {X} MB
- **Network:** {domains accessed}
- **Secrets:** {optional secrets}

## Related Extensions

- {Related extension 1}
- {Related extension 2}
```

---

## Reference Files

- **Schema**: `docker/lib/schemas/extension.schema.json`
- **Registry**: `docker/lib/registry.yaml`
- **Categories**: `docker/lib/categories.yaml`
- **Profiles**: `docker/lib/profiles.yaml`
- **Examples**: `docker/lib/extensions/*/extension.yaml`

For detailed field reference, see REFERENCE.md.
For complete examples, see EXAMPLES.md.

**Tip:** Use `Glob` and `Grep` tools to discover current documentation files dynamically:

```bash
# Find all extension docs
ls docs/extensions/*.md

# Find VisionFlow docs
ls docs/extensions/vision-flow/*.md
```
