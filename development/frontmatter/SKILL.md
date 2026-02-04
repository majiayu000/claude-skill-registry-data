---
name: frontmatter
description: Generates YAML frontmatter metadata (date/time, git commit, branch, repository) for workflow documentation. Use when creating research docs, plans, or work summaries.
---

# Frontmatter Generator

Collect metadata for document frontmatter by running:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/frontmatter/workflow-tools-frontmatter.sh
```

## Output Format

```
Current Date/Time (TZ): 2025-01-15 10:30:45 EST
Current Git Commit Hash: abc123...
Current Branch Name: main
Repository Name: my-project
```

If not in a git repository, only the date/time line is returned.

## Mapping to YAML Frontmatter

Use the output to populate these fields:

| Script Output | YAML Field |
|---------------|------------|
| Current Date/Time (TZ) | `date:` |
| Current Git Commit Hash | `git_commit:` |
| Current Branch Name | `branch:` |
| Repository Name | `repository:` |
