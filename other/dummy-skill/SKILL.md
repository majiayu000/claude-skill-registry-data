---
name: note-formatter
description: Format raw notes into a structured markdown document with a title, one-sentence summary, and key points. Use when the user provides unstructured notes that need organizing.
license: MIT
---

# Note Formatter

Given raw notes, produce a structured `formatted_notes.md` file.

## Output Format

Save to `formatted_notes.md` with this exact structure:

```markdown
# [Extracted Title]

## Summary

[One sentence capturing the core topic]

## Key Points

- [Point 1]
- [Point 2]
- [Point 3]
```

## Rules

- Extract the title from the subject matter — do not copy a heading verbatim if one exists
- Write the summary in exactly one sentence
- Extract 3–5 key points — distill the meaning, do not copy sentences verbatim
- Save the file to the output directory specified in the task prompt
