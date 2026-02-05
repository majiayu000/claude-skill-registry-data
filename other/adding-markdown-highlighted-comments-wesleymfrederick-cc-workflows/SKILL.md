---
name: adding-markdown-highlighted-comments
description: Use when adding responses to markdown documents with user-highlighted comments, encountering markup errors, or unsure about mark tag placement - ensures proper model-highlight formatting with required attributes and correct placement within markdown elements
---

# Adding markdown Highlighted Comments

## Overview

Add AI responses to markdown documents using standardized highlighted markup that tracks authorship, timestamps, and relationships between comments.

**Core principle:** Marks go INSIDE markdown formatting. Each line/paragraph gets separate marks. Code blocks get one mark wrapping the entire block including fences.

## When to Use

Use this skill when:
- User asks you to add comments/responses to an markdown document
- Document contains `<mark class="user-highlight">` tags
- You need to respond to highlighted user comments
- Working with documents that have highlighted sections

Don't use for:
- Plain markdown without highlight markup
- Chat-only responses
- Documents without existing highlight infrastructure

## Required Markup Structure

### Class and Attributes

**ALWAYS use exactly:**

```html
<mark class="model-highlight"
      data-model="claude-sonnet-4-20250514"
      data-created="2025-01-06T10:30:00"
      data-modified="2025-01-06T10:30:00"
      data-id="mark-1736163000-a1b2c3"
      data-group-id="response-202501061030">
```

**Required attributes - no exceptions:**
- `class="model-highlight"` (exactly this, not claude-highlight or claude-response)
- `data-model` - your exact model ID
- `data-created` - ISO 8601 timestamp
- `data-modified` - ISO 8601 timestamp (same as created for new)
- `data-id` - unique: `mark-TIMESTAMP-RANDOM`
- `data-group-id` - group identifier: `response-YYYYMMDDHHMM`

**Do NOT invent attributes:**
- ❌ `data-in-reply-to`
- ❌ `data-user-id`
- ❌ Any other custom attributes

### Group Delimiters

**ALWAYS wrap your entire response:**

```html
<!-- group-id:response-202501061030 -->

[Your marked-up response here]

<!-- /group-id:response-202501061030 -->
```

Missing delimiters = violation.

## Mark Placement Rules

### Rule 1: Marks INSIDE Formatting

```markdown
✅ CORRECT: **<mark ...>Bold text</mark>**
❌ WRONG: <mark ...>**Bold text**</mark>

✅ CORRECT: *<mark ...>Italic text</mark>*
❌ WRONG: <mark ...>*Italic text*</mark>

✅ CORRECT: • **<mark ...>Item</mark>**<mark ...> - description</mark>
❌ WRONG: • <mark ...>**Item** - description</mark>
```

### Rule 2: Separate Marks Per Line/Paragraph

**One sentence = one mark. Multiple sentences = multiple marks.**

```markdown
✅ CORRECT:
**<mark ...>First sentence here.</mark>**

**<mark ...>Second sentence here.</mark>**

❌ WRONG - Multi-sentence paragraph:
**<mark ...>First sentence here. Second sentence here.</mark>**

❌ WRONG - Multi-paragraph:
**<mark ...>First paragraph here.

Second paragraph here.</mark>**
```

**For bullet lists, use `•` character, not markdown `-` syntax:**

```markdown
✅ CORRECT:
• **<mark ...>Item title</mark>**<mark ...> - description text</mark>
• **<mark ...>Second item</mark>**<mark ...> - more description</mark>

❌ WRONG - Using markdown dash:
<mark ...>- Item title - description text</mark>

❌ WRONG - Mark outside bullet:
<mark ...>• Item title - description</mark>
```

### Rule 3: Code Blocks - Single Mark for Entire Block

```markdown
✅ CORRECT:
<mark ...>```typescript
function example() {
  return true;
}
```</mark>

❌ WRONG:
```text
(marks inside code block content)
```typescript
<mark ...>function example() {
  return true;
}</mark>
```

```text

**For code blocks:** Wrap entire block including fence markers. Do NOT put marks inside the code content.

### Rule 4: No Spaces Between Adjacent Marks

```markdown
✅ CORRECT: </mark><mark ...>
❌ WRONG: </mark> <mark ...>
```

## Placement in Document

### Find Comment Group

1. Scan for user comments (`user-highlight` marks)
2. Group related comments:
   - Comments in same list
   - Comments separated by 1-2 lines
   - Comments under same heading
3. Find LAST comment in group

### Insert Response

Place your response:
- ✅ AFTER the last user comment in the group
- ✅ BEFORE next unhighlighted section/heading
- ❌ NOT in the middle of user comment group
- ❌ NOT overwriting existing content

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `class="claude-highlight"` | Use `class="model-highlight"` exactly |
| `class="claude-response"` | Use `class="model-highlight"` exactly |
| `**<mark>text</mark>**` | Put mark inside: `**<mark>text</mark>**` |
| Multi-paragraph single mark | Create separate mark per paragraph |
| Code mark inside fences | Wrap entire block including ``` markers |
| Missing group delimiters | Always add `<!-- group-id:... -->` wrapping |
| Inventing attributes | Only use the 6 required attributes |

## Quick Reference

**Every response needs:**
1. ☐ Group delimiters with matching group-id
2. ☐ Each line/paragraph has separate mark tags
3. ☐ Marks INSIDE markdown formatting (bold, italic, bullets)
4. ☐ Code blocks: single mark wrapping entire block + fences
5. ☐ All 6 required attributes on every mark
6. ☐ `class="model-highlight"` (not any other variation)
7. ☐ No spaces between adjacent mark tags
8. ☐ Placed after last user comment, before next approved section

## Workflow

```markdown
1. Read document to locate user comments
2. Identify comment group (all related comments)
3. Find last comment in group
4. Add group delimiter: <!-- group-id:response-YYYYMMDDHHMM -->
5. Write response with proper mark tags
6. Add closing delimiter: <!-- /group-id:response-YYYYMMDDHHMM -->
7. Verify placement (after comments, before approved content)
```

## Complete Example

**User comments:**

```markdown
**<mark class="user-highlight" data-created="..." data-modified="..." data-id="mark-1">Question 1?</mark>**

**<mark class="user-highlight" data-created="..." data-modified="..." data-id="mark-2">Question 2?</mark>**
```

**Your response:**

```markdown
<!-- group-id:response-202501061030 -->

**<mark class="model-highlight" data-model="claude-sonnet-4-20250514" data-created="2025-01-06T10:30:00" data-modified="2025-01-06T10:30:00" data-id="mark-1736163000-abc" data-group-id="response-202501061030">Answer to question 1 here.</mark>**

**<mark class="model-highlight" data-model="claude-sonnet-4-20250514" data-created="2025-01-06T10:30:05" data-modified="2025-01-06T10:30:05" data-id="mark-1736163005-def" data-group-id="response-202501061030">Answer to question 2 here.</mark>**

<mark class="model-highlight" data-model="claude-sonnet-4-20250514" data-created="2025-01-06T10:30:10" data-modified="2025-01-06T10:30:10" data-id="mark-1736163010-ghi" data-group-id="response-202501061030">```typescript
function handleTokenExpiration() {
  // implementation
}
```</mark>

<!-- /group-id:response-202501061030 -->
```

## Red Flags - STOP and Fix

If you catch yourself:
- Using `claude-highlight` or `claude-response` class
- Putting marks outside `**bold**` or `*italic*`
- Creating one mark for multiple sentences (even in same paragraph)
- Creating one mark for multiple paragraphs
- Using markdown `-` instead of `•` bullet character
- Putting marks around entire bullet including `•`
- Putting marks inside code block content
- Skipping group delimiters "to save time"
- Inventing new attributes like `data-in-reply-to`
- Adding spaces between adjacent mark tags
- Omitting bold formatting to "save time"

**All of these mean: Wrong markup. Fix before proceeding.**

## Common Rationalizations That Mean You're Failing

| Excuse | Reality |
|--------|---------|
| "Multi-sentence is more readable" | Wrong. One sentence = one mark. No exceptions. |
| "Markdown bullets are standard" | Wrong. Use `•` character, not `-` syntax. |
| "Skipping bold saves time" | Wrong. Match user formatting exactly. |
| "I'll fix formatting later" | Wrong. Fix now or you'll forget. |
| "Close enough under pressure" | Wrong. Pressure doesn't excuse violations. |
| "The skill doesn't apply here" | Wrong. If document has highlights, skill applies. |

**All of these mean: You're rationalizing. Follow the rules.**
