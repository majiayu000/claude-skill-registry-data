---
name: metool
description: Package management for modular code organization. This skill should be used when creating, installing, or modifying metool packages, working with package structure conventions, or adding Claude Code skills to packages.
---

# Metool Package Management

## Overview

Metool (mt) organizes code through packages - self-contained units with scripts, functions, configuration, and documentation. Packages are organized in modules and installed via GNU Stow symlinks. From shell utilities to complete applications, all code follows the same structure.

See [README.md](README.md) for installation and getting started.

## Quick Reference

### Package Structure

```
package-name/
├── README.md        # Required
├── SKILL.md         # Optional (AI assistance)
├── bin/             # Executables → ~/.metool/bin/
├── shell/           # Functions, aliases → sourced on startup
├── config/          # Dotfiles (dot- prefix) → ~/
├── lib/             # Library functions (not symlinked)
└── libexec/         # Helper scripts (not in PATH)
```

See [docs/packages/structure.md](docs/packages/structure.md) for conventions.

### Essential Commands

```bash
mt package add module/package    # Add to working set
mt package install package-name  # Install (create symlinks)
mt cd package-name               # Navigate to package
mt edit function-name            # Edit a function/script
mt reload                        # Reload shell configuration
```

See [docs/commands/README.md](docs/commands/README.md) for full reference.

## Workflows

### Creating a Package

Create directory structure, add README.md, implement components, install.

See [docs/packages/creation.md](docs/packages/creation.md) for step-by-step guide.

```bash
mt package new my-package /path/to/module  # Create from template
```

### Adding a Skill to a Package

Create SKILL.md in package root with required frontmatter.

See [docs/skills/README.md](docs/skills/README.md) for skill creation.

### Service Packages

For systemd/launchd services, use the service package template.

See [docs/services/README.md](docs/services/README.md) for service management.

### Package Promotion

Move packages between modules (dev → public).

See [docs/packages/promotion.md](docs/packages/promotion.md) for workflow.

```bash
mt package diff package-name dev pub  # Compare versions
```

## Discovering Packages

```bash
mt module list                    # List modules in working set
mt package list                   # List all packages
mt package list | grep -w git     # Find specific package
```

## Troubleshooting

### Installation Conflicts

When config files conflict, remove existing files when prompted.

### Prerequisites

```bash
mt deps              # Check dependencies
mt deps --install    # Auto-install on macOS
```

Requires: GNU coreutils, GNU Stow 2.4.0+

## Documentation

- [docs/getting-started.md](docs/getting-started.md) - Installation and setup
- [docs/packages/README.md](docs/packages/README.md) - Package management
- [docs/skills/README.md](docs/skills/README.md) - Claude Code skills
- [docs/services/README.md](docs/services/README.md) - Service packages
- [docs/commands/README.md](docs/commands/README.md) - Command reference
