---
name: Plugin Publishing
description: Use when the user wants to publish, share, or submit a Claude Code plugin to the marketplace
version: 1.0.0
---

# Plugin Publishing

Guide users through publishing their Claude Code plugins to the marketplace.

## When to Use This Skill

Activate this skill when the user:
- Wants to publish a plugin they've created
- Asks how to share a plugin
- Needs to update a published plugin
- Wants to submit to the official marketplace
- Has questions about plugin requirements

## Pre-Publishing Checklist

Before publishing, ensure the plugin has:

### Required Structure
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # ✅ Required manifest
├── README.md                 # ✅ Required documentation
├── LICENSE                   # ✅ Required license file
├── commands/                 # Optional
│   └── *.md
├── skills/                   # Optional
│   └── */SKILL.md
├── agents/                   # Optional
├── hooks/                    # Optional
│   └── hooks.json
└── scripts/                  # Optional
```

### Valid Manifest

```json
{
  "name": "plugin-name",
  "description": "Clear, concise description of the plugin",
  "version": "1.0.0",
  "author": "Your Name or Organization"
}
```

### Quality Requirements

- [ ] Unique plugin name (check registry first)
- [ ] Semantic versioning (MAJOR.MINOR.PATCH)
- [ ] Clear description (under 200 characters)
- [ ] Comprehensive README
- [ ] Valid LICENSE file
- [ ] No hardcoded secrets or credentials
- [ ] Works with current Claude Code version

## Publishing Process

### Step 1: Validate Plugin

Run the validation command:
```
/plugin-marketplace:publish --validate
```

This checks:
- Manifest structure and required fields
- File structure correctness
- README presence and format
- License compatibility
- No security issues detected

### Step 2: Create Account (First Time)

If publishing for the first time:
```
/plugin-marketplace:publish --register
```

This will:
- Create publisher account
- Verify email/identity
- Set up authentication

### Step 3: Publish

Submit the plugin:
```
/plugin-marketplace:publish
```

Or with explicit path:
```
/plugin-marketplace:publish ./path/to/plugin
```

### Step 4: Verification (Optional)

For verified badge, additional review is required:
- Code review by maintainers
- Security audit
- Quality assessment
- May take 1-2 weeks

## Plugin Naming Conventions

### Format
```
@scope/plugin-name
```

### Scope Types

| Scope | Description | Example |
|-------|-------------|---------|
| `@username` | Personal plugins | `@john/my-helper` |
| `@org` | Organization plugins | `@acme/internal-tools` |
| `@claude` | Official Anthropic | `@claude/git-assistant` |
| `@community` | Verified community | `@community/formatter` |

### Name Requirements

- Lowercase letters, numbers, hyphens only
- 3-50 characters
- Must be unique in scope
- Descriptive and meaningful

## Version Management

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1  (Patch: bug fixes)
1.0.1 → 1.1.0  (Minor: new features, backwards compatible)
1.1.0 → 2.0.0  (Major: breaking changes)
```

### Updating Published Plugins

```
/plugin-marketplace:publish --update
```

Requires:
- Bumped version number
- Changelog entry (recommended)
- Passing validation

## README Requirements

A good README includes:

```markdown
# Plugin Name

Brief description of what the plugin does.

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`
/plugin-marketplace:install @scope/plugin-name
\`\`\`

## Usage

### Commands
- `/plugin-name:command1` - Description
- `/plugin-name:command2` - Description

### Configuration
How to configure the plugin.

## Examples

Real usage examples.

## License

MIT (or your license)
```

## Security Guidelines

### Do NOT Include

- API keys or secrets
- Hardcoded credentials
- Personal data
- Malicious code
- Obfuscated code

### Security Best Practices

1. **Use environment variables** for sensitive config
2. **Validate inputs** in commands and hooks
3. **Minimal permissions** - only request what's needed
4. **Secure dependencies** - keep them updated
5. **Document security** - explain what permissions are for

## Marketplace Categories

Choose the most appropriate category:

| Category | For Plugins That... |
|----------|---------------------|
| `code-generation` | Generate code or boilerplate |
| `code-analysis` | Analyze, lint, or review code |
| `testing` | Help with testing workflows |
| `formatting` | Format or style code |
| `documentation` | Generate or manage docs |
| `git` | Enhance git workflows |
| `ai-enhancement` | Extend Claude capabilities |
| `productivity` | Improve developer workflow |
| `integration` | Connect to external services |
| `utilities` | General utilities |

## Example Publishing Flow

### User: "I want to publish my formatter plugin"

**Response:**
Great! Let's publish your formatter plugin. First, let me validate it:

```
/plugin-marketplace:publish --validate
```

**Validation Results:**
✅ Manifest valid
✅ README present
✅ LICENSE (MIT) detected
✅ Commands: 2 found
✅ Skills: 1 found
⚠️ Suggestion: Add keywords to manifest for better discoverability

Would you like to proceed with publishing? I can help you:
1. Fix the suggestions first
2. Publish as-is
3. Review what will be published

### User: "Publish it"

**Response:**
Publishing @username/code-formatter v1.0.0...

```
/plugin-marketplace:publish
```

✅ Plugin published successfully!

**Your plugin is now available at:**
`/plugin-marketplace:install @username/code-formatter`

**Next steps:**
- Share the install command with users
- Apply for verification (optional)
- Monitor feedback and issues

Would you like me to help you apply for verified status?
