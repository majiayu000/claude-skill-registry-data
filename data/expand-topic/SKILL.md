---
name: expand-topic
description: Generate a new article on a topic. Content is published directly.
---

# Expand Topic

Generate a new article on a philosophical topic.

## When to Use

- When a todo item is type `expand-topic`
- When `/expand-topic [topic]` is invoked
- After research has been completed on a topic

## Instructions

### 1. Check for Research

Look in `obsidian/research/` for existing research on this topic.

If no research exists:
- For simple topics, proceed with general knowledge
- For complex topics, run `/research-topic` first

### 2. Determine Target Location

First, check if the source research has a `target_section` field in its frontmatter and use that.

Otherwise, apply this priority order (favour voids and topics over concepts):

1. **Voids** (`obsidian/voids/[slug].md`) — if the article explores:
   - Cognitive limits or boundaries of thought
   - Unchartable territories or things that resist understanding
   - The unexplored, unexplorable, or occluded
   - Paradoxes or self-referential difficulties
   - Apophatic or negative approaches to knowledge

2. **Topics** (`obsidian/topics/[slug].md`) — if the article addresses:
   - Big philosophical questions (consciousness, free will, meaning, identity)
   - Substantive explorations that connect multiple concepts
   - Questions humans actually ask about life and mind
   - Anything that could be framed as "What does X mean for us?"

3. **Concepts** (`obsidian/concepts/[slug].md`) — only if the article is:
   - A definitional piece explaining a specific philosophical term
   - Background material that other articles will reference
   - A technical idea that serves as building block, not destination

**Default to topics** when uncertain. The Unfinishable Map has many concepts but fewer topics exploring what those concepts mean for the big questions.

Use kebab-case for filenames (e.g., `hard-problem-of-consciousness.md`).

**Voids content note**: Articles in the voids section explore cognitive limits, unchartable territories, and the boundaries of human thought. They should:
- Maintain intellectual honesty about what is speculation vs. established
- Acknowledge uncertainty about whether limits are real or merely difficult
- Connect to the voids framework (unexplored, unexplorable, occluded)
- Reference the voids index: `[[voids]]`

### 3. Review Style Guide

Before writing, review `obsidian/project/writing-style.md` for:
- Document structure requirements (opening summary, H2 sections, tenet connection)
- Named-anchor summary pattern for forward references
- Background vs. novelty guidance (what to include/omit)
- LLM optimization (front-load important information)

### 4. Check Tenet Alignment

Before writing, review `obsidian/tenets/tenets.md` and ensure the article will:
- Not contradict any tenet
- Not endorse positions that tenets "rule out"
- Acknowledge the Map's perspective where relevant

### 5. Generate Article

Use the existing generation tool:
```bash
uv run python scripts/generate.py article "[Topic Title]" --style exploratory
```

Or write directly with this structure:

```markdown
---
title: "[Topic Title]"
description: "[150-160 chars emphasizing human+AI collaboration, iterative refinement, and pursuit of truth]"
created: YYYY-MM-DD
modified: YYYY-MM-DD
human_modified:
ai_modified: YYYY-MM-DDTHH:MM:SS+00:00
draft: false
topics: []
concepts: []
related_articles: []
ai_contribution: 100
author:
ai_system: [current model]
ai_generated_date: YYYY-MM-DD
last_curated:
---

[Opening paragraph - accessible hook into the topic]

## [First Major Section]

[Content...]

## [Second Major Section]

[Content...]

## Relation to Site Perspective

[How this topic connects to the Map's tenets - be explicit]

## Further Reading

- [[related-article-1]]
- [[related-article-2]]

## References

[If based on research, cite sources]
```

### 5.5 Length Check (Self-Edit if Over Target)

Before finalizing, count words and check against section thresholds:

```bash
uv run python -c "
from pathlib import Path
from tools.curate.length import analyze_length
a = analyze_length(Path('[filepath]'))
print(f'{a.word_count} words ({a.excess_percent:.0f}% of {a.soft_threshold} target) - {a.status}')
"
```

**Target ranges by section:**
| Section | Target | Soft Max | Hard Max |
|---------|--------|----------|----------|
| concepts/ | 1500-2000 | 2500 | 3500 |
| topics/ | 2000-2500 | 3000 | 4000 |
| voids/ | 1500-2000 | 2000 | 3000 |

**If over soft max:** Self-edit before publishing:
- Tighten prose (remove "it is the case that", "one might argue")
- Cut redundant explanations
- Replace detailed tangents with links to other articles
- Ensure the core argument is preserved

**If over hard max:** Mandatory self-edit:
- The article is too long for its section
- Consider splitting into multiple articles
- Or significantly condense following `/condense` principles

Include final word count in the changelog entry.

### 6. Update Todo

If this was a todo item:
1. Mark the task as complete
2. Note the output file

### 7. Log to Changelog

Append to `obsidian/workflow/changelog.md`:
```markdown
### HH:MM - expand-topic
- **Status**: Success
- **Topic**: [topic name]
- **Output**: [filepath]
- **Word count**: [count]
- **Based on research**: [yes/no, link if yes]
```

### 8. Commit

Create a git commit with message:
```
feat(content): Add article on [topic]

Based on research: [yes/no]
```

### 9. Check Apex Sources

After creating the article, check if it's a source for any apex article:

1. Read `obsidian/apex/apex-articles.md`
2. For each apex article entry, check if the new article path appears in `Source articles`
3. If yes, add a task to `obsidian/workflow/todo.md`:
   ```markdown
   - [ ] P2 apex-evolve: [apex-slug] — source [new-article] created
   ```

This ensures apex articles are updated when their source content changes.

## Content Guidelines

Follow the comprehensive guidance in `obsidian/project/writing-style.md`.

**Quick reference:**
- Lead with the most important point (LLM truncation resilience)
- Use named-anchor pattern for forward references
- Include "Relation to Site Perspective" section
- Minimize standard background; focus on what's novel
- Short: 500-800 words | Medium: 1000-1500 | Long: 2000-3000

## Important

- **CRITICAL: ALWAYS set `draft: false`** — Content is published directly. Never use `draft: true`.
- **ALWAYS include a `description`** — 150-160 chars emphasizing human+AI collaboration, iterative refinement, pursuit of truth. Avoid generic descriptions.
- ALWAYS include `ai_contribution: 100`
- ALWAYS include current model in `ai_system`
- ALWAYS update `ai_modified` timestamp
- Content must align with site tenets
