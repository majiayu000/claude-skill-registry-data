---
name: "intermediate-example"
description: "An intermediate example with metadata and examples"
version: "1.2.0"
author: "Example Author"
created: "2025-01-15"
updated: "2025-10-23"
category: "examples"
tags: ["example", "tutorial", "intermediate"]
complexity: "intermediate"
has_examples: true
example_files: ["examples/demo.py"]
when_to_use:
  - "When learning how to structure skills with metadata"
  - "When you need examples to reference"
---

# Intermediate Example Skill

This skill demonstrates more comprehensive metadata usage and includes
example files in an `examples/` subdirectory.

## Features

- **Version tracking**: Semantic versioning
- **Authorship**: Author and date information
- **Categorization**: Tags and category for organization
- **Complexity**: Indicates skill difficulty level
- **Examples**: Reference example files in the skill folder

## Folder Structure

```
intermediate-example/
├── SKILL.md              ← This file
└── examples/             ← Optional examples folder
    └── demo.py           ← Example Python script
```

## Metadata Fields

### Required
- `name`: Unique identifier
- `description`: Brief description

### Optional (shown in this skill)
- `version`: Semantic version
- `author`: Skill creator
- `created`, `updated`: ISO dates
- `category`: Main category
- `tags`: List of tags for searching
- `complexity`: beginner, intermediate, or advanced
- `has_examples`: Boolean flag
- `example_files`: Paths relative to skill folder

## Using Examples

The `examples/demo.py` file shows a simple Python script that demonstrates
the concept. You can reference these files in your skill documentation.

## Best Practices

1. **Use semantic versioning** for the version field
2. **Keep tags relevant** and lowercase
3. **Set appropriate complexity** to help users find suitable skills
4. **List all example files** in the frontmatter
5. **Organize examples** in subdirectories

## Next Steps

Check out the `advanced-example` skill for even more metadata fields
and a more complex folder structure with templates!
