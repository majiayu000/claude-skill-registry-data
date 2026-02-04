---
name: doc-automation
description: Documentation automation with file versioning and metadata. Use for maintaining documentation, tracking file versions, adding metadata headers.
allowed-tools: Read, Write, Bash, Glob, Grep
model: haiku
---

# Documentation Automation Skill

Automate documentation maintenance with consistent versioning and metadata.

## Core Functions

### 1. File Metadata Standard

Every tracked file should have metadata. Format depends on file type:

#### Markdown Files (.md)

```markdown
---
version: "1.0.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
author: "agent-name or user"
status: "draft|active|deprecated"
---
```

#### JSON Files (.json)

```json
{
  "_meta": {
    "version": "1.0.0",
    "created": "YYYY-MM-DD",
    "updated": "YYYY-MM-DD",
    "schema": "schema-name"
  }
}
```

#### TypeScript/JavaScript (in comments)

```typescript
/**
 * @version 1.0.0
 * @created YYYY-MM-DD
 * @updated YYYY-MM-DD
 * @author agent-name
 */
```

### 2. Versioning Rules

Follow semantic versioning:

- **Major (X.0.0)**: Breaking changes, complete rewrites
- **Minor (0.X.0)**: New features, significant additions
- **Patch (0.0.X)**: Bug fixes, small updates, metadata changes

### 3. Automatic Metadata Updates

When editing files:

1. Check if metadata exists
2. If missing, add with version 1.0.0
3. If exists, increment version appropriately
4. Update `updated` date to today
5. Keep `created` date unchanged

### 4. Version Tracking File

Maintain `.ai/versions.json` for project-wide version tracking:

```json
{
  "_meta": {
    "version": "1.0.0",
    "updated": "YYYY-MM-DD"
  },
  "files": {
    "path/to/file.md": {
      "version": "1.2.0",
      "created": "YYYY-MM-DD",
      "updated": "YYYY-MM-DD",
      "changelog": [
        {
          "version": "1.2.0",
          "date": "YYYY-MM-DD",
          "change": "Added section X"
        },
        {
          "version": "1.1.0",
          "date": "YYYY-MM-DD",
          "change": "Expanded examples"
        },
        {
          "version": "1.0.0",
          "date": "YYYY-MM-DD",
          "change": "Initial creation"
        }
      ]
    }
  }
}
```

## Tracked File Types

| Type      | Track Versions | Metadata Location |
| --------- | -------------- | ----------------- |
| `.md`     | Yes            | YAML frontmatter  |
| `.json`   | Yes            | `_meta` property  |
| `.ts/.js` | Optional       | JSDoc header      |
| `.py`     | Optional       | Module docstring  |
| Skills    | Yes            | YAML frontmatter  |
| Agents    | Yes            | YAML frontmatter  |

## Commands

### Add Metadata to File

When creating or significantly updating a file:

1. Add appropriate metadata header
2. Set version to 1.0.0 if new, increment if existing
3. Update versions.json

### Validate Documentation

Check all tracked files:

- Have proper metadata
- Versions match versions.json
- No stale files (updated > 90 days ago)

### Generate Changelog

Extract changes from versions.json for release notes

## Hook Integration

This skill works with the `progress-save` hook to automatically:

1. Track files modified in session
2. Update versions.json on session end
3. Ensure metadata consistency

## Token Efficiency

- Metadata adds ~50 tokens per MD file
- versions.json is centralized, not loaded per-file
- Only load file versions when needed for comparison
