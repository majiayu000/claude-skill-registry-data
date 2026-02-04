---
name: Obsidian Formatting
description: This skill should be used when "creating Obsidian notes", "formatting frontmatter", "using Dataview syntax", "embedding images in Obsidian", or when working with Obsidian-specific markdown features. Provides expertise in YAML frontmatter, Dataview queries, wikilinks, and Obsidian markdown conventions.
version: 0.1.0
---

# Obsidian Formatting

## Overview

Obsidian uses an enhanced markdown format with YAML frontmatter, wikilinks, and plugin-specific syntax like Dataview and Mapview. This skill provides knowledge for creating properly formatted Obsidian notes, particularly for location-based notes with geographic data.

## When to Use This Skill

Load this skill when creating or formatting Obsidian notes, especially:
- Writing YAML frontmatter with proper syntax
- Using Dataview inline queries and code blocks
- Creating wikilinks for internal references
- Embedding images with Obsidian syntax
- Configuring Mapview plugin blocks for geographic visualization

## Core Concepts

### YAML Frontmatter

YAML frontmatter appears at the top of Obsidian notes between `---` delimiters. It stores structured metadata.

**Basic structure:**
```yaml
---
field: value
array_field:
  - item1
  - item2
nested:
  key: value
---
```

**Critical rules:**
- Must start file (no content before first `---`)
- Use 2-space indentation for nested structures
- Arrays use `- ` prefix (dash + space)
- Strings with special characters need quotes
- Wikilinks in frontmatter: `'[[Page Name]]'` (quoted)
- Coordinates: store as array `[latitude, longitude]`

### Wikilinks

Wikilinks create internal references between notes.

**Syntax:**
- Basic: `[[Note Name]]`
- With alias: `[[Note Name|Display Text]]`
- To heading: `[[Note Name#Heading]]`
- To block: `[[Note Name^block-id]]`

**In frontmatter:** Quote wikilinks to preserve syntax:
```yaml
Country: '[[UK]]'
Region: '[[Somerset]]'
```

### Dataview Inline Queries

Dataview queries display dynamic content based on note metadata.

**Inline queries** use backticks with `=` prefix:
```markdown
`= this.Country`
`= this.location[0]`
```

**Complex inline query for images:**
```markdown
`= choice(startswith(string(default(this.image, "")), "[["), "!" + this.image, choice(this.image, "![Image](" + this.image + ")", "No Image"))`
```

This query:
1. Checks if `image` field starts with `[[` (wikilink)
2. If yes: Prepends `!` to embed wikilinked image
3. If no: Uses markdown image syntax with URL
4. If empty: Shows "No Image"

### Mapview Plugin

Mapview creates interactive maps from note coordinates.

**Standard code block:**
```markdown
```mapview
{"name":"Current Note","query":"path:\"$filename$\"","chosenMapSource":0,"autoFit":true,"lock":true,"showLinks":true,"linkColor":"red","markerLabels":"off"}
```
```

**Key fields:**
- `query`: Dataview query to select notes (use `path:\"$filename$\"` for current note)
- `autoFit`: Center map on markers
- `lock`: Prevent map dragging
- `markerLabels`: Show/hide marker labels

### Obsidian Markdown Extensions

**Image embedding:**
- Wikilink: `![[image.png]]`
- URL: `![Alt text](https://example.com/image.jpg)`
- With size: `![[image.png|200]]` (200px width)

**Tags:**
- Inline: `#tag-name`
- In frontmatter: Use `tags:` array
```yaml
tags:
  - map/food
  - location
```

**Callouts (admonitions):**
```markdown
> [!note] Title
> Content here
```

## Location Note Formatting

### Required Frontmatter Fields

For location notes with Mapview integration:

```yaml
---
tags:
  - map/TYPE  # map/food, map/photo-location, map/accommodation/campsite, map/other
Country: '[[Country Name]]'
Region: '[[Region Name]]'
location:
  - LATITUDE
  - LONGITUDE
Source:
  - https://source1.com
  - https://source2.com
image: https://example.com/image.jpg  # Or '[[local-image.jpg]]'
publish: true
Done: false  # or visited: false
color: blue
icon: ICON_NAME  # map-pin, utensils, camera, tent-tree
---
```

### Location Coordinates

Store as array of two numbers (latitude first, longitude second):

```yaml
location:
  - 51.4776031
  - -2.6256316
```

**Do not use:**
- String format: `"51.4776031, -2.6256316"` ❌
- Object format: `{lat: 51.4776031, lon: -2.6256316}` ❌

### Note Structure

Standard structure for location notes:

```markdown
---
[frontmatter here]
---

```mapview
[mapview config]
```

## Description

[Detailed information about the location]

## [Type-Specific Section]
<!-- For photo locations: Photography Tips -->
<!-- For food: Can be omitted or custom -->

## Travel Information

[Directions, parking, accessibility, contact info]

[Image display query]
```

### Image Display Pattern

Use this Dataview query at the end of notes:

```markdown
`= choice(startswith(string(default(this.image, "")), "[["), "!" + this.image, choice(this.image, "![Image](" + this.image + ")", "No Image"))`
```

This handles both wikilinks (`[[image.jpg]]`) and URLs (`https://...`).

## Best Practices

### Frontmatter
- Always quote wikilinks: `'[[Page Name]]'`
- Use arrays for multiple values (tags, sources, location)
- Keep boolean values lowercase: `true`, `false`
- Validate YAML syntax (check indentation, colons, dashes)

### Content
- Use markdown headings (`##`) for sections
- Separate frontmatter from content with blank line
- Include Mapview block before content for geographic notes
- End with image display query if `image` field used

### Tags
- Use hierarchical tags: `map/food`, `map/photo-location`
- Consistent naming: kebab-case for multi-word tags
- Place in frontmatter for better organization

### Wikilinks
- Reference countries/regions as wikilinks for navigation
- Quote wikilinks in frontmatter values
- Use descriptive link text with aliases when needed

## Validation

Check notes for:
- ✅ Frontmatter opens and closes with `---`
- ✅ Required fields present (tags, Country, Region, Source)
- ✅ Location array has exactly 2 numbers (if present)
- ✅ Wikilinks quoted in frontmatter
- ✅ Tags use array syntax
- ✅ Mapview block includes valid JSON
- ✅ Image display query present if image field used

## Common Issues

**Issue:** Frontmatter parsing fails
**Cause:** Missing quotes around wikilinks or invalid YAML
**Fix:** Quote all wikilinks, check indentation and colons

**Issue:** Dataview query shows raw code
**Cause:** Dataview plugin not enabled or syntax error
**Fix:** Verify Dataview installed, check backtick and `=` placement

**Issue:** Map doesn't display location
**Cause:** Incorrect location format or Mapview plugin disabled
**Fix:** Use array format `[lat, lon]`, enable Mapview plugin

**Issue:** Image not displaying
**Cause:** Incorrect Dataview query or missing field
**Fix:** Use standard image display query, ensure `image` field exists

## Additional Resources

For detailed syntax and advanced features:
- **`references/dataview-syntax.md`** - Complete Dataview query reference
- **`references/frontmatter-schema.md`** - Field definitions and types
- **`examples/complete-note.md`** - Fully formatted example location note

Use these references when working with complex queries or unfamiliar field types.
