---
name: book-companion-skill
description: Create companion Codex workflows from book chapters, reader exercises, prompts, field notes, and teaching material. Use when Codex needs to turn a chapter excerpt, 書籍練習, AI 提示詞, worksheet, or author note into a reusable Skill-style workflow, GitHub-shareable companion artifact, or book link resource for readers.
---

# Book Companion Skill

## Overview

Convert book material into a reader-friendly, executable Codex workflow. Preserve the author's voice, make the task usable by someone who only has the book in front of them, and produce artifacts that can be shared through GitHub or linked from a printed/e-book chapter.

## Workflow

1. Identify the source material:
   - Book title or working title
   - Chapter or section
   - Reader goal
   - Raw exercise, prompt, note, or example
   - Expected output format, if provided

2. Decide the artifact type:
   - **Reader prompt**: A short prompt readers can paste into Codex or ChatGPT.
   - **Skill draft**: A `SKILL.md` workflow for repeatable use.
   - **Chapter companion card**: A compact Markdown card for a GitHub README, QR landing page, or book appendix.
   - **Exercise upgrade**: A clearer, more testable version of a chapter exercise.

3. Translate the book material into action:
   - Keep the reader's first step obvious.
   - State what input the reader should provide.
   - State what Codex should produce.
   - Include constraints only when they materially improve the result.
   - Avoid assuming readers know internal author notes or private context.

4. Package the result for sharing:
   - Use stable filenames and short slugs.
   - Prefer Markdown for GitHub readability.
   - Include a clear "Use this with Codex" prompt.
   - Include install or copy instructions only when the artifact is a full Skill.
   - Keep book-facing links durable: point readers to a GitHub repo, release, or landing page rather than a local file path.

## Output Patterns

### Reader Prompt

Use this shape when the reader should copy one prompt from GitHub or a QR page:

```markdown
## Chapter X: <exercise name>

Paste this into Codex:

> Use this chapter exercise to help me <reader goal>. My raw material is below. Ask at most two clarifying questions if needed, then produce <expected output>.
```

### Skill Draft

Use this shape when the book material should become a reusable Codex Skill:

```markdown
---
name: <short-hyphen-name>
description: <what the skill does and exact trigger scenarios>
---

# <Human Title>

## Overview

<one or two sentences>

## Workflow

<steps another Codex instance can follow>
```

### Chapter Companion Card

Use this shape for GitHub pages, README sections, and book links:

```markdown
## <Chapter / Tool / Exercise Name>

**Use when:** <reader situation>

**Input:** <what the reader brings>

**Codex prompt:** `<single concise prompt>`

**Output:** <what Codex returns>
```

## Quality Bar

- Make the artifact useful without private context.
- Keep names short, lowercase, and hyphenated for Skill folders.
- Put trigger scenarios in the `description` frontmatter, not only in the body.
- Keep `SKILL.md` lean; move long examples or chapter-specific details to `references/`.
- Do not include hidden author-only assumptions in reader-facing prompts.
- When the output is for GitHub, include relative links and durable headings.

## References

Read `references/chapter-workflow-patterns.md` when converting multiple chapter exercises, building a companion README, or standardizing many book links.
