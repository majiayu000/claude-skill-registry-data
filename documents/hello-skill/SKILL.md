---
name: documentation-review
version: 1.0.0
description: Reviews documentation against internal standards.
tags:
  - documentation
  - review
  - quality
compatibility:
  codex: ">=0.1.0"
  claude: ">=1.0.0"
entrypoint: SKILL.md
license: internal
owners:
  - platform-team
---

# Documentation Review Skill

This skill helps review documentation files against internal quality standards.

## Usage

When invoked, this skill will analyze documentation files and check for:

- Proper formatting and structure
- Compliance with style guides
- Completeness of content
- Code example validity
- Link integrity

## Requirements

- Documentation files in Markdown format
- Access to style guide rules

## Configuration

The skill can be configured with custom rules by creating a `rules.yaml` file:

```yaml
rules:
  max_heading_depth: 3
  require_code_lang: true
  check_links: true
```

## Examples

### Basic Usage

```
Review the README.md file
```

### With Custom Rules

```
Review all documentation in /docs using strict rules
```

## Output

The skill produces a structured report with:
- List of issues found
- Severity levels (error, warning, info)
- Suggested fixes
- Quality score

## Maintenance

This skill is maintained by the Platform Team. For issues or feature requests, please contact platform-team@company.com.
