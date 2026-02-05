---
name: obsidian-daily
description: Quick capture of notes, links, and ideas to the Obsidian vault
---

# Obsidian Quick Capture

Quickly add content to the Obsidian vault without creating full pages.

## Quick Note Types

### 1. Capture a Thought or Idea

Add to `~/dev/personal/obsidian/trobrock/Notes.md` under the "Jot down some text" section:

```markdown
{timestamp or topic}
{Your thought or notes here}
```

### 2. Add a To-Do Item

Add to `~/dev/personal/obsidian/trobrock/Notes.md` under the "Make a to-do list" section:

```markdown
- [ ] {Task description}
```

### 3. Save a Link/Bookmark

**Option A - Quick embed (for reference links):**
Add to `Notes.md` under "Embed links":
```markdown
- [[{Descriptive Title}]]
```

Then create the linked page with:
```markdown
# {Descriptive Title}

{URL}

{Brief notes about why this is useful}
```

**Option B - Inline link (for one-off references):**
Just add directly to Notes.md:
```markdown
[{Description}]({URL})
```

### 4. Add a Quote

Add to `~/dev/personal/obsidian/trobrock/Quotes.md`:
```markdown
> {The quote text}
> 
> - {Attribution}
```

### 5. Add to Wishlist

Add to `~/dev/personal/obsidian/trobrock/Stuff I want.md`:
```markdown
- {Item name} - {optional notes, price, or link}
```

## When to Create a Full Page vs Quick Capture

**Quick Capture (Notes.md):**
- Single thoughts or reminders
- Links to read later
- Quick to-dos
- Things that don't need their own structure

**Create Full Page:**
- Projects with multiple aspects
- Travel plans
- Topics that will grow over time
- Things that need their own checklist or sections

## Section Reference for Notes.md

| Section | Use For |
|---------|---------|
| Jot down some text | Freeform thoughts, meeting notes, ideas |
| Make a to-do list | Quick tasks not tied to a project |
| Create sub-pages | Links to detailed notes you're creating |
| Embed links | Bookmarks to external resources |

## Verification

- [ ] Content added to correct section
- [ ] Wiki links use `[[double brackets]]`
- [ ] External links use `[text](url)` format
- [ ] Checkboxes use `- [ ]` syntax
