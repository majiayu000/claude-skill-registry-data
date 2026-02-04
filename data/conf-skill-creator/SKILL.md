---
name: conf-skill-creator
description: Creates skills for installing software and configuring computers. Use when asked to create a new skill for machine setup, software installation, update or removal, or system configuration.
---

# Creating Computer Configuration Skills

When creating a new skill for installing software or configuring a computer:

## Structure
Create the skill in `.claude/skills/<skill-name>/SKILL.md`

## Required Frontmatter
```yaml
---
name: skill-name
description: Brief description of what this installs/configures
---
```

## Instructions to Include

1. **Prerequisites** - What must be installed first (e.g., Homebrew, apt)
2. **Installation commands** - The exact commands to run
3. **Configuration steps** - Any post-install configuration needed
4. **Verification** - How to confirm success
5. **Update** - How to update to newer versions
6. **Uninstallation** - How to remove the software and clean up configuration files

## Example Skill

```yaml
---
name: install-node
description: Installs Node.js via nvm. Use when setting up Node.js or JavaScript development.
---

## Prerequisites
- macOS or Linux
- curl installed

## Installation
1. Install nvm: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash`
2. Restart terminal or run: `source ~/.bashrc`
3. Install Node: `nvm install --lts`

## Verify
Run `node --version` to confirm installation.

## Update
- Update nvm itself: `cd ~/.nvm && git fetch --tags && git checkout $(git describe --tags --abbrev=0)`
- Install newer Node version: `nvm install --lts` (keeps previous versions)
- Switch to new version: `nvm use --lts`
- Set new default: `nvm alias default <version>`

## Uninstall
1. Remove installed Node versions: `nvm uninstall <version>` or `nvm uninstall --lts`
2. Remove nvm itself:
   - Delete nvm directory: `rm -rf ~/.nvm`
   - Remove nvm lines from shell config (`~/.bashrc`, `~/.zshrc`, or `~/.profile`)
3. Restart terminal to apply changes
```

## Guidelines
- Keep skills focused on one tool or configuration
- Use Homebrew on macOS, apt on Debian/Ubuntu
- Include rollback steps for complex changes
- Prefer idempotent commands that can safely re-run
- Always include update instructions for upgrading to newer versions
- Always include uninstall instructions covering both software removal and config cleanup
