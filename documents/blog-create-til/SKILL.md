---
description: Write a "today I learned" blog
model: haiku
---

# Goal

- Write a concise, engaging "Today I Learned" (TIL) blog post on the user's topic

# Workflow

## Structure

1. Title
2. What I Learned
3. Why It Matters
4. Example / Demonstration
5. Key Takeaways
6. References or Further Reading

- The post should:
  - Start with a short intro: what I learned and why it caught my attention
  - Explain the concept in simple language for engineers and curious readers
  - Include a practical example, code snippet, or real-world use case if relevant
  - Highlight surprising insights, common misconceptions, or lessons learned
  - End with key takeaways and actionable advice for further exploration

## Use Front Matter and TL;DR

- Add front matter as in `.claude/skills/blog.rules.md` `## Front Matter (YAML)`
- Add TL;DR as in `.claude/skills/blog.rules.md` `## TL;DR Section`

## Beautify

- Run a command to format the code for proper visualization
  ```bash
  > prettier --tab-width 4 --prose-wrap always --print-width 80 -w <FILE>
  ```

# Conventions

## Tone

- Conversational and reflective
- Technical but accessible
- Curious and educational

## Length

- Keep the post between 500 and 1000 words. Favor clarity and practical value
  over exhaustive coverage

## Formatting Rules

- Write using bullet points

- Follow the rules in:

  - `.claude/skills/blog.rules.md`
  - `.claude/skills/markdown.rules.md`
  - `.claude/skills/text.rules.md`

# Verification

- [ ] Confirm front matter and a TL;DR are present per
      `.claude/skills/blog.rules.md`
- [ ] Confirm the post is between 500 and 1000 words
- [ ] Confirm `prettier` ran without errors
