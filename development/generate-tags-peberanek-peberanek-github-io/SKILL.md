---
name: generate-tags
description: Generate tags for a blog post.
---

List existing tags using the following script:
```sh
uv run .claude/skills/generate-tags/scripts/list_tags.py
```

Use the existing tags to update `tags` in the blog post YAML frontmatter. Here is an example of an updated frontmatter:
```yaml
date: 2025-10-11
tags:
  - ai
  - ai-agents
  - ai-predictions
  - sam-altman
```

When the post is about AI topic, always include tag `ai`.
