---
name: media-reviewer
description: Analyze media content structure, narrative flow, key themes, and important moments from videos, podcasts, and articles. Use when you need to understand content organization before documenting.
---

# Media Reviewer Skill

Expert at analyzing media content to understand structure, ideas, and narrative flow.

## What This Skill Does

- Reads media materials (captions, transcripts, blog posts)
- Understands the ideas and concepts being presented
- Identifies narrative structure and how content progresses
- Discovers key moments, turning points, and themes
- Recognizes how content is organized and why

## Input

You receive:
- Material ID (e.g., 'v123')
- All available source files (captions, transcripts, HTML)
- Material metadata from frontmatter

## Output (Implicit)

Internal analysis (structured as assistant's thinking) that will be used by content-documenter skill to generate documentation.

Focus on:
- **Content structure**: How is this organized?
- **Core ideas**: What are the main concepts?
- **Narrative flow**: How does it progress?
- **Key moments**: What are important moments?
- **Themes**: What topics emerge?
- **Documentary angle**: How would you structure this for a documentary?

## Analysis Approach

1. **Read all available materials** for the given material ID
2. **Understand the context** from metadata (title, source, date)
3. **Identify main topics** and how they connect
4. **Track narrative progression** from beginning to end
5. **Extract key insights** and memorable moments
6. **Note important quotes** and timestamps
7. **Understand the author's intent** (if applicable)
8. **Recognize patterns** and recurring themes

## Example Analysis

Given a video about Constitutional AI:
- **Structure**: Introduction → Problem statement → Solution → Examples → Conclusion
- **Core ideas**: Alignment, interpretability, harmlessness
- **Key moments**: When method is first introduced (timestamp), key examples
- **Themes**: Safety in AI, human values, transparency
- **Documentary angle**: How safety concerns drive the approach, specific breakthrough moments

## Important Rules

✅ Be thorough and comprehensive
✅ Understand the material deeply
✅ Preserve nuance and detail
✅ Note what makes this content unique
❌ Don't add your own analysis or interpretation
❌ Don't skip important details
❌ Don't oversimplify complex concepts
