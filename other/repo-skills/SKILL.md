---
name: repo-skills
description: After cloning a repository, scan for skill definitions and load them on demand. Always use this after cloning any repo.
---

# Repo Skill Discovery

After cloning any repository, scan for skill definitions. Replace `<repo-root>` below with the absolute path of the cloned repository:

```bash
find <repo-root>/.claude/skills -name "SKILL.md" 2>/dev/null
find <repo-root>/.codex/agents \( -name "*.md" -o -name "*.toml" \) 2>/dev/null
find <repo-root>/.skills -name "SKILL.md" 2>/dev/null
```

If no skill files are found, skip the index output and proceed with the task.

For each skill file found, read only the metadata (YAML frontmatter for .md files, top-level fields for .toml files) to extract the name and description. Output a compact index:

<repo-skills repo="org/repo-name" path="/absolute/path/to/repo">
- skill-name: one-line description
- skill-name: one-line description
</repo-skills>

When a discovered skill is relevant to your current task, read its full file and follow its instructions.

If the `<repo-skills>` index is missing from your conversation history (e.g. after context compaction), re-scan the repo using the path from `git rev-parse --show-toplevel` in the repo's working directory to rebuild it.
