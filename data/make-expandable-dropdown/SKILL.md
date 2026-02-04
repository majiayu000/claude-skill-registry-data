---
name: make-expandable-dropdown
description: Converts highlighted text (typically bullet lists or paragraphs) into an expandable HTML <details> dropdown with a custom summary. Use this skill when the user wants to make content collapsible/expandable in their MDX files.
---

# Make Expandable Dropdown

## Overview

This skill wraps selected text in HTML `<details>` and `<summary>` tags to create collapsible/expandable sections in MDX files.

## When to Use This Skill

Use this skill when:
- User highlights text and asks to make it expandable/collapsible
- User wants to create a dropdown section
- User mentions making content hidden behind a toggle
- User wants to add a `<details>` block

## How It Works

1. **Detect the highlighted text** from system reminders
2. **Automatically extract the summary** from the first bullet point if the content starts with a list item (e.g., `- Summary text`). If no bullet point is found at the start, ask the user for a summary.
3. **Remove the first bullet** from the content (since it's now the summary)
4. **Wrap the remaining content** in `<details>` and `<summary>` tags
5. **Replace the original text** with the wrapped version

### Summary Extraction Rules

- If the selected text starts with a bullet (e.g., `- Technical explanation`), use that as the summary
- Remove the leading bullet marker and any extra whitespace
- If there's nested content after the first bullet, that becomes the expandable content
- Only ask the user for summary text if the selection doesn't start with a bullet point

## Example

**Before:**
```markdown
- Point one
- Point two
- Point three
```

**After:**
```html
<details>
<summary>Click to expand</summary>

- Point one
- Point two
- Point three
</details>
```

## Implementation Notes

- Preserve all formatting and indentation of the wrapped content
- Add blank lines around the content for proper markdown rendering
- The summary text should be concise and descriptive
- Multiple highlighted sections can be converted in sequence
- Where there are multiple levels of nested bullets, only change the top level bullet in the way described above