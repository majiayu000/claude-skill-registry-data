---
name: plugin-creator
description: Create comprehensive Claude Code plugins with proper structure, commands, agents, hooks, and marketplace configuration. Use when the user wants to build a new Claude Code plugin or asks how to create/structure a plugin.
---

# Claude Code Plugin Creator

This skill helps you create well-structured Claude Code plugins following best practices from the official documentation and successful plugins like gemini-search.

## When to Use This Skill

Invoke this skill when the user:
- Asks to create a new Claude Code plugin
- Wants to understand plugin structure and architecture
- Needs help with plugin.json, marketplace.json, or other config files
- Wants to add commands, agents, or hooks to their plugin
- Asks about plugin best practices or conventions

## Plugin Architecture Overview

A Claude Code plugin consists of:

1. **Core Configuration** (`.claude-plugin/`)
   - `plugin.json` - Plugin metadata and entry points
   - `marketplace.json` - Marketplace listing information

2. **Commands** (`commands/`)
   - Markdown files defining slash commands (e.g., `/search`, `/stats`)
   - YAML frontmatter with name, description, usage, examples
   - Command execution instructions

3. **Agents** (`agents/`)
   - Markdown files defining subagents with isolated context
   - YAML frontmatter with description and capabilities
   - Agent-specific instructions and patterns

4. **Hooks** (`hooks/`)
   - `hooks.json` - Hook configuration with matchers
   - Bash scripts for PreToolUse, PostToolUse, UserPromptSubmit events
   - Event-driven automation

5. **Scripts** (`scripts/`)
   - Bash scripts for plugin functionality
   - Use `${CLAUDE_PLUGIN_ROOT}` for portability

6. **Documentation**
   - `README.md` - User-facing docs
   - `CLAUDE.md` - Instructions for Claude Code
   - `CHANGES.md` - Changelog
   - `CONTRIBUTING.md`, `TESTING.md`, etc.

## Step-by-Step Plugin Creation

### Step 1: Initialize Plugin Structure

```bash
# Create directory structure
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/commands
mkdir -p my-plugin/agents
mkdir -p my-plugin/hooks
mkdir -p my-plugin/scripts
mkdir -p my-plugin/tests

# Initialize git repository
cd my-plugin
git init
git checkout -b main
```

### Step 2: Create plugin.json

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Brief description of what your plugin does",
  "author": "Your Name",
  "license": "MIT",
  "commands": "commands",
  "agents": "agents",
  "hooks": "hooks/hooks.json"
}
```

**Important fields:**
- `name`: kebab-case plugin identifier
- `version`: Semantic versioning (MAJOR.MINOR.PATCH)
- `commands`, `agents`, `hooks`: Relative paths to entry points

### Step 3: Create marketplace.json

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": {
        "type": "github",
        "repo": "username/repo-name"
      },
      "description": "Detailed description for the marketplace",
      "version": "0.1.0",
      "author": {
        "name": "Your Name"
      },
      "license": "MIT",
      "homepage": "https://github.com/username/repo-name",
      "repository": {
        "type": "git",
        "url": "https://github.com/username/repo-name.git"
      },
      "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
      ],
      "category": "productivity",
      "commands": "./commands",
      "agents": "./agents",
      "hooks": "./hooks/hooks.json",
      "strict": true,
      "features": [
        "Feature 1 description",
        "Feature 2 description",
        "Feature 3 description"
      ],
      "requirements": {
        "dependencies": [
          {
            "name": "dependency-name",
            "description": "What this dependency does",
            "install": "npm install -g dependency-name",
            "required": true
          }
        ]
      }
    }
  ]
}
```

**Key sections:**
- `source.type`: "github" or "directory" for local testing
- `category`: "productivity", "development", "utilities", etc.
- `strict`: Set to true for production plugins
- `features`: User-facing feature list
- `requirements.dependencies`: External tools needed

### Step 4: Create Commands

Create a command file in `commands/my-command.md`:

```markdown
---
name: my-command
description: Brief description of what this command does
usage: /my-command [arguments]
examples:
  - /my-command example argument
  - /my-command "quoted argument"
---

You are the command handler for the my-command in the my-plugin plugin.

## Execution Instructions

When this command is invoked:

1. Parse the user's arguments
2. Execute the required logic (call scripts, process data, etc.)
3. Present results to the user

## Example: Calling a Script

Run the following command:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh" arg1 "{{USER_ARG}}"
```

Where `{{USER_ARG}}` is the argument provided by the user.

## Response Format

Present results with:
- Clear summary of what was done
- Formatted output (tables, lists, etc.)
- Any warnings or errors
- Next steps or suggestions

## Error Handling

If the command fails:
- Display clear error messages
- Suggest troubleshooting steps
- Recommend related commands
```

**Command best practices:**
- Use YAML frontmatter with required fields
- Provide clear usage examples
- Use `${CLAUDE_PLUGIN_ROOT}` for script paths
- Define clear error handling

### Step 5: Create Agents (Optional)

Create an agent file in `agents/my-agent.md`:

```markdown
---
description: Agent description and purpose
capabilities:
  [
    "capability-1",
    "capability-2",
    "capability-3",
  ]
---

# My Agent Name

This agent provides [specific functionality] with [key features].

## Features

- Feature 1 with context isolation
- Feature 2 with specific behavior
- Feature 3 with error handling

## Usage Patterns

Describe when and how this agent should be used:
- Pattern 1: [scenario]
- Pattern 2: [scenario]
- Pattern 3: [scenario]

## Important Notes

- Key architectural decision
- Performance considerations
- Limitations or constraints
```

**Agent best practices:**
- Use for context isolation and token savings
- Define clear capabilities
- Specify usage patterns
- Document architecture decisions

### Step 6: Create Hooks (Optional)

Create `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "pattern|Pattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/pre-hook.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "pattern|Pattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/post-hook.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "/command1|/command2",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user-prompt-hook.sh"
          }
        ]
      }
    ]
  }
}
```

**Hook types:**
- `PreToolUse`: Before tool execution (suggestions, validation)
- `PostToolUse`: After tool execution (error detection, cleanup)
- `UserPromptSubmit`: On user command submission

Create hook script in `hooks/pre-hook.sh`:

```bash
#!/bin/bash

# Example hook script
# Receives JSON input via stdin with context about the event

# Read input
input=$(cat)

# Process input and provide feedback
echo "Hook executed successfully"
```

**Hook best practices:**
- Use matchers for targeted triggering
- Keep hooks fast and lightweight
- Use `${CLAUDE_PLUGIN_ROOT}` for portability
- Handle errors gracefully

### Step 7: Create Scripts

Create executable scripts in `scripts/`:

```bash
#!/bin/bash

# Script template
set -euo pipefail

# Use environment variables for configuration
SCRIPT_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
LOG_FILE="${LOG_FILE:-/tmp/my-plugin.log}"

# Function definitions
function main() {
    local arg1="$1"
    local arg2="${2:-default}"

    # Your logic here
    echo "Processing: $arg1"

    # Return JSON for structured output
    echo '{"status":"success","result":"data"}'
}

# Entry point
main "$@"
```

**Script best practices:**
- Use `set -euo pipefail` for safety
- Use `${CLAUDE_PLUGIN_ROOT}` for paths
- Provide structured output (JSON)
- Log to `/tmp/` for debugging
- Make scripts executable: `chmod +x scripts/*.sh`

### Step 8: Create CLAUDE.md

Create `CLAUDE.md` for project-specific instructions:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with this plugin.

## Project Overview

[Brief description of what this plugin does and its architecture]

## Common Commands

```bash
# Development & Testing
bash tests/run-tests.sh

# Using the plugin
/my-command [args]
```

## Architecture & Key Concepts

### Key Feature 1
[Explain important architectural decision]

### Key Feature 2
[Explain another important concept]

## Important Constraints

### Do NOT:
- Thing to avoid 1
- Thing to avoid 2

### Always:
- Best practice 1
- Best practice 2
```

### Step 9: Create Documentation

Essential docs:

1. **README.md** - User-facing documentation
   - Installation instructions
   - Usage examples
   - Features overview
   - Requirements

2. **CHANGES.md** - Changelog following Keep a Changelog format

3. **CONTRIBUTING.md** - Development workflow

4. **TESTING.md** - Testing guide

5. **LICENSE** - Open source license (MIT recommended)

### Step 10: Validate and Test

```bash
# Validate JSON files
jq empty .claude-plugin/plugin.json
jq empty .claude-plugin/marketplace.json
jq empty hooks/hooks.json

# Lint scripts
shellcheck scripts/*.sh hooks/*.sh

# Make scripts executable
chmod +x scripts/*.sh hooks/*.sh

# Test locally
# Add to .claude/settings.json:
{
  "extraKnownMarketplaces": {
    "local-test": {
      "source": {
        "source": "directory",
        "path": "/absolute/path/to/my-plugin"
      }
    }
  }
}

# Then in Claude Code:
/plugin add my-plugin@local-test
```

## Best Practices

### 1. Context Isolation with Agents

Use agents for expensive operations to save tokens:
- Search operations
- API calls
- Heavy processing

Benefits: 30-40% token savings through context isolation

### 2. Caching Strategy

Implement caching for expensive operations:
```bash
CACHE_DIR="${CACHE_DIR:-/tmp/my-plugin-cache}"
CACHE_TTL="${CACHE_TTL:-3600}"  # 1 hour

cache_key=$(echo -n "$query" | md5sum | cut -d' ' -f1)
cache_file="$CACHE_DIR/$cache_key.json"

if [[ -f "$cache_file" ]]; then
    # Check if cache is fresh
    cache_age=$(($(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file")))
    if [[ $cache_age -lt $CACHE_TTL ]]; then
        cat "$cache_file"
        exit 0
    fi
fi
```

### 3. Error Handling

Implement robust error handling:
```bash
set -euo pipefail

function error_handler() {
    local line_num=$1
    echo "Error on line $line_num" >&2
    exit 1
}

trap 'error_handler ${LINENO}' ERR
```

### 4. Logging

Log important events:
```bash
LOG_FILE="${LOG_FILE:-/tmp/my-plugin.log}"
ERROR_LOG="${ERROR_LOG:-/tmp/my-plugin-errors.log}"

function log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

function error_log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >> "$ERROR_LOG"
}
```

### 5. Semantic Versioning

Follow semantic versioning strictly:
- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### 6. Security Considerations

- Never commit API keys or secrets
- Validate all user inputs
- Use secure temp file creation
- Follow principle of least privilege
- Log security-relevant events

### 7. Performance Optimization

- Use caching for repeated operations
- Implement context isolation with agents
- Stream large outputs
- Use efficient data structures
- Benchmark critical paths

### 8. Testing Strategy

Create `tests/run-tests.sh`:
```bash
#!/bin/bash
set -euo pipefail

echo "Running integration tests..."

# Test 1: JSON validation
jq empty .claude-plugin/plugin.json || exit 1
jq empty .claude-plugin/marketplace.json || exit 1

# Test 2: Script syntax
shellcheck scripts/*.sh || exit 1

# Test 3: Functional tests
bash scripts/my-script.sh test-arg || exit 1

echo "All tests passed!"
```

## Common Patterns

### Pattern 1: Command with Script Execution

Command file calls bash script, script returns JSON, command formats output.

### Pattern 2: Agent-Based Processing

Main command spawns agent, agent processes in isolated context, results return to main.

### Pattern 3: Hook-Driven Automation

Hooks detect patterns, trigger scripts, provide suggestions or automation.

### Pattern 4: Caching Layer

Check cache first, execute on miss, store result, track analytics.

## Marketplace Publishing

### Prerequisites

1. GitHub repository with plugin code
2. Valid plugin.json and marketplace.json
3. Comprehensive README.md
4. LICENSE file (MIT recommended)
5. All tests passing

### Publishing Steps

1. **Prepare Release**
   ```bash
   # Update version in all files
   # Update CHANGES.md
   git add -A
   git commit -m "chore: prepare release v0.1.0"
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin main --tags
   ```

2. **Create GitHub Release**
   - Use GitHub UI or `gh release create`
   - Attach assets if needed
   - Copy changelog to release notes

3. **Test Installation**
   ```bash
   # Add marketplace to settings
   # Install plugin
   # Verify functionality
   ```

## Troubleshooting

### Plugin Not Loading

- Check JSON syntax with `jq empty`
- Verify paths in plugin.json
- Check file permissions
- Review Claude Code logs

### Commands Not Working

- Verify YAML frontmatter format
- Check script paths and permissions
- Test scripts independently
- Review command error logs

### Hooks Not Triggering

- Verify matchers are correct
- Check hooks.json syntax
- Test hook scripts independently
- Review hook execution logs

## Resources

- **Official Docs**: https://docs.claude.com/en/docs/claude-code
- **Skills Docs**: https://docs.claude.com/en/docs/claude-code/skills
- **Example Plugins**: https://github.com/anthropics/skills
- **Community**: https://github.com/hesreallyhim/awesome-claude-code

## Related Skills

This plugin-creator skill works together with other skills for a complete development workflow:

### web-research Skill
Use the **web-research** skill to efficiently research plugin development topics:
- Latest Claude Code plugin best practices
- Example plugins and their implementations
- Marketplace requirements and guidelines
- Tool comparisons for plugin dependencies

The web-research skill uses the gemini-search agent for token-efficient searches with caching.

### github-repo-management Skill
Use the **github-repo-management** skill for repository setup and CI/CD:
- Setting up GitHub Actions workflows for plugins
- Configuring issue templates and labels
- Release automation with semantic versioning
- Pull request workflows and branch protection
- GitHub Packages publishing

### shell-script-quality Skill
Use the **shell-script-quality** skill for script quality assurance:
- ShellCheck linting for plugin scripts
- BATS testing framework setup
- CI/CD integration for shell script testing
- Pre-commit hooks for quality checks

## Next Steps After Creating Plugin

1. **Initialize git repository**
   - Use the github-repo-management skill for repository setup
   - Configure branch protection and issue templates

2. **Create comprehensive tests**
   - Use the shell-script-quality skill for test setup
   - Add BATS tests for all scripts

3. **Add CI/CD with GitHub Actions**
   - Use the github-repo-management skill for workflow setup
   - Configure automated testing, linting, and releases

4. **Research best practices**
   - Use the web-research skill to find latest best practices
   - Research similar successful plugins

5. **Write user documentation**
   - README.md with installation and usage
   - CONTRIBUTING.md for contributors
   - CHANGES.md for changelog

6. **Test locally before publishing**
   - Local marketplace testing
   - Manual testing of all commands and hooks

7. **Publish to marketplace**
   - Create GitHub release
   - Verify installation from marketplace

8. **Gather user feedback**
   - Set up GitHub Discussions
   - Monitor issues and PRs

9. **Iterate and improve**
   - Address user feedback
   - Add new features based on usage patterns
   - Keep dependencies updated

## Example: Complete Minimal Plugin

Here's a complete minimal plugin structure:

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── commands/
│   └── hello.md
├── scripts/
│   └── hello.sh
├── CLAUDE.md
├── README.md
├── CHANGES.md
└── LICENSE
```

With `commands/hello.md`:
```markdown
---
name: hello
description: Say hello to the user
usage: /hello [name]
examples:
  - /hello World
---

Run: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/hello.sh" "{{NAME}}"`
Present the result to the user.
```

And `scripts/hello.sh`:
```bash
#!/bin/bash
name="${1:-World}"
echo "Hello, $name!"
```

This is the simplest possible plugin. From here, add complexity as needed!
