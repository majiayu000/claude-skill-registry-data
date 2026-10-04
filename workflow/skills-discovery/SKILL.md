---
name: skills-discovery
description: Find/install skills better than base knowledge for a task.
---

# Skills Discovery

You can extend your capabilities by discovering and installing Agent Skills from the claude-plugins.dev registry. Skills provide specialized knowledge, tools, and techniques for specific technologies, frameworks, and domains.

## When to search for skills

First, check if an installed skill matches the task. If not, search the registry—specialized skills may exist that you haven't installed yet.

Before starting any non-trivial task, ask yourself:

1. Do I have a skill for this? → Use it
2. Might one exist that I don't have? → Search the registry

Search proactively when:

- The task involves specific technologies, frameworks, or file formats
- You're about to do something where best practices matter (testing, deployment, APIs, documentation)
- The domain is specialized (PDF processing, data pipelines, ML workflows)
- You notice yourself about to give generic advice where expert patterns would help

Also search when users explicitly ask to find, install, or manage skills.

## Discovery workflow

Use the registry API for search (the CLI's search command is interactive and not suitable for programmatic use):

```bash
curl "https://claude-plugins.dev/api/skills?q=QUERY&limit=20&offset=0"
```

**Parameters:**

- `q`: Search query (e.g., "frontend", "python", "pdf")
- `limit`: Results per page (max 100)
- `offset`: Pagination offset

**Response structure:**

```json
{
  "skills": [
    {
      "id": "...",
      "name": "skill-name",
      "namespace": "@owner/repo/skill-name",
      "sourceUrl": "https://github.com/...",
      "description": "...",
      "author": "...",
      "installs": 123,
      "stars": 45
    }
  ],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

## Search strategies

The registry indexes skill names, descriptions, and tags. Construct queries that match how skill authors describe their work.

**Query construction:**

- Use 1-3 specific terms (too broad = noise, too narrow = misses)
- Prefer widely-used terminology over project-specific jargon
- Technology + task often outperforms either alone
- If results are poor, broaden or try synonyms

## Installation

If user wants to install: `npx skills-installer install @owner/repo/skill-name`.

## After install

Promote to shared, vendor-strip the SKILL.md, and run install-one-question-one → `~/.claude/references/skills-management.md` § Post-Install: Promote + Vendor-Strip.

## Management

```bash
# List installed skills
npx skills-installer list

# Uninstall a skill
npx skills-installer uninstall @owner/repo/skill-name
```
