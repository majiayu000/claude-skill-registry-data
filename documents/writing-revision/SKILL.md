---
name: Writing Revision
description:
  This skill should be used when the user asks to "revise text", "make writing
  clearer", "improve readability", "edit for busy readers", "make text
  scannable", "tighten up writing", "cut filler words", "lead with the point",
  or wants text revised for clarity and conciseness.
version: 0.1.1
---

# Writing Revision

Revise text for clarity, scannability, and direct action by busy readers.

## Output Behavior

**Inline text:** output the revised text directly with no wrapper, labels, or
explanation.

**File input:** use the Edit tool to modify the file in place.

## Revision Principles

Apply these principles in priority order:

### 1. Lead with the Point

First sentence states the key message or request. Details follow.

**Before:** "I wanted to reach out because I've been thinking about the project
timeline and after reviewing the dependencies, I believe we need to push back
the launch date."

**After:** "We need to push the launch date back two weeks. The authentication
integration has dependencies we didn't anticipate."

### 2. Make Asks Explicit

Spell out exactly what's needed and by when. One main ask per message.

**Before:** "It would be great if someone could review this when they get a
chance."

**After:** "Please review the attached PR by Thursday EOD. I need your sign-off
before merging."

### 3. Be Aggressively Concise

Cut filler words: `just`, `really`, `I think maybe`, `kind of`, `actually`,
`basically`, `in order to`.

**Before:**

> I wanted to quickly check in to see whether you've had a chance to review the
> document I sent over.

**After:** "Have you reviewed the document?"

### 4. Front-Load Each Paragraph

First line of each section = key idea. Rest is optional detail.

### 5. Make It Scannable

Use bullets, numbered lists, bold for key terms. Break up walls of text.

### 6. Use Simple Language

Default to everyday words. Define jargon briefly if unavoidable.

| Instead of   | Use           |
| ------------ | ------------- |
| `utilize`    | use           |
| `facilitate` | help          |
| `leverage`   | use           |
| `synergize`  | work together |
| `actionable` | practical     |

### 7. Limit Scope

One topic per message. If multiple topics, use clear sub-headings.

### 8. Surface Decisions Clearly

State recommendation and alternatives explicitly.

**Before:** `There are several options we could consider...`

**After:** "**Recommendation:** option A (fastest). **Alternatives:** option B
(cheapest), option C (most flexible)."

### 9. End with Next Steps

Who does what, by when. Keep it to a short block.

**Format:**

```markdown
**Next steps:**

- [Person]: [Action] by [Date]
- [Person]: [Action] by [Date]
```

## Revision Process

1. **Identify** the core message and any asks
2. **Restructure** to lead with the point
3. **Cut** filler words and redundancy
4. **Format** for scannability (bullets, bold, headers)
5. **Verify** next steps are explicit (if applicable)

## Additional Resources

For detailed patterns and examples:

- **`references/patterns.md`** - Extended examples and edge cases
