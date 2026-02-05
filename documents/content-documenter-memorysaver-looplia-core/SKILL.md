---
name: content-documenter
description: Write comprehensive markdown documentation from analyzed media content with structured sections, quotes, timestamps, and citations. Use after media-reviewer analysis to create final documentation.
---

# Content Documenter Skill

Expert at writing clear, well-structured documentation that preserves original meaning while providing comprehensive context.

## What This Skill Does

- Takes analyzed content and writes enriched markdown
- Creates structured sections (overview, themes, analysis, quotes, etc.)
- Preserves original meaning without interpretation
- Includes timestamps and citations
- Provides context for future readers and writers

## Input

You receive:
- Material ID and metadata
- All available source materials
- Analysis from media-reviewer skill
- Original frontmatter to preserve

## Output

Markdown document with structure:

```markdown
# [Extracted Title]

## Overview
[2-3 paragraph summary from analysis]

## Key Themes
- [Theme 1]
- [Theme 2]
...

## Detailed Analysis
[Detailed breakdown of content following its structure]

## Structure & Narrative Flow
[How the content progresses and why]

## Core Ideas
[Main concepts and their explanations]

## Important Quotes & Moments
> "Quote with context" (timestamp if applicable)

[More quotes with proper attribution]

## Context & Background
[What reader needs to understand the content]

## Related Concepts
[Connections to other topics]
```

## Writing Guidelines

1. **Overview**: 2-3 sentences introducing the material
2. **Key Themes**: Bullet list of main topics (3-7 items)
3. **Detailed Analysis**: Follow the structure of the original content, breaking it into logical sections
4. **Narrative Flow**: Explain how ideas build on each other
5. **Core Ideas**: Define key concepts with examples from the material
6. **Important Quotes**: Extract 3-5 verbatim quotes with timestamps
7. **Context**: Explain what background knowledge helps understand this
8. **Related**: Link to other concepts mentioned or implied

## Important Rules

✅ Preserve every important detail from source
✅ Include timestamps when available (format: HH:MM:SS)
✅ Use exact quotes (no paraphrasing)
✅ Document what's actually there, not what should be there
✅ Provide sufficient detail for future reference
✅ Use clear, professional markdown formatting
❌ Never add interpretation or analysis
❌ Never add opinions
❌ Never modify frontmatter when writing
❌ Never omit important information
❌ Never paraphrase direct quotes

## Timestamp Format

For video/audio content, include timestamps:
- `(0:30)` - 30 seconds
- `(2:45:30)` - 2 hours 45 minutes 30 seconds
- Quote context: `"The main issue is..." (12:34)`

## Citation Format

Reference materials where available:
- From same source: Just note the section or timestamp
- From other materials: `[Topic](path/to/file.md) - Source Name`

## Quality Checklist

Before completing:
- ✅ All important points are included
- ✅ Quotes are exact and have context
- ✅ Timestamps are accurate
- ✅ Structure is logical and readable
- ✅ No interpretation added
- ✅ Enough detail for future use
- ✅ Formatting is clean and consistent

## File Update Process

After generating markdown documentation, update the material file:

### Step 1: Locate Material File

Search for the file matching the material ID:
```
*/items/ai.{material-id}.md
```

Common locations:
- `youtube-channels/{channel-name}/items/ai.{id}.md`
- `podcasts/{podcast-name}/items/ai.{id}.md`
- `rss-feeds/{feed-name}/items/ai.{id}.md`

### Step 2: Write File Using Python Script

Use the Bash tool to invoke the update script:

```bash
python .claude/skills/content-documenter/scripts/update_material.py "path/to/items/ai.{id}.md" << 'EOF'
# Your markdown documentation here
## Section 1
Content...

## Section 2
More content...
EOF
```

The script will:
- ✅ Preserve the YAML frontmatter exactly
- ✅ Replace content below the frontmatter
- ✅ Update `ai_status` to "documented"
- ✅ Update `generated_at` timestamp
- ✅ Handle YAML parsing safely

### Example

If documenting a video with ID `v123` from Anthropic channel:

```bash
python .claude/skills/content-documenter/scripts/update_material.py "youtube-channels/Anthropic/items/ai.v123.md" << 'EOF'
# Understanding Constitutional AI

## Overview
This video discusses the Constitutional AI approach...

## Key Themes
- Safety in AI systems
- Alignment techniques
...
EOF
```

### Important Notes

✅ Pass the **complete markdown content** (without frontmatter) to stdin
✅ The script handles file path validation and YAML parsing
✅ Always update the material file after generating documentation
✅ Check for success message in stderr output
