---
name: content-author
description: Write quality content for HTML documents. Use when writing text content, prose, descriptions, or any human-readable content in HTML files. Ensures spelling and style quality.
allowed-tools: Read, Write, Edit
---

# Content Author Skill

This skill ensures all written content meets quality standards for spelling, grammar, and style.

## Spelling Awareness

This project uses **cspell** for spell checking with a custom dictionary.

### Known Project Terms

These terms are in `project-words.txt` and won't trigger spell errors:

**Technical:**
- XHTML, WCAG, htmlhint, pa11y, cspell, textlint, linkinator

**Custom Elements:**
- product-card, icon-element, user-avatar, status-badge, data-table, nav-menu

**HTML Terms:**
- doctype, tbody, thead, fieldset, hgroup, blockquote

Check `project-words.txt` for the full list.

### Adding New Terms

When using a new product name or technical term:

1. **Use slash command:** `/add-word TermName`
2. **Or edit directly:** Add to `project-words.txt` (one word per line)

## Style Guidelines

### Avoid Passive Voice

```
<!-- Passive (avoid) -->
The form was submitted by the user.
Errors were found in the document.

<!-- Active (prefer) -->
The user submitted the form.
The validator found errors in the document.
```

### Avoid Weasel Words

Remove vague qualifiers:

| Avoid | Use Instead |
|-------|-------------|
| various | (be specific) |
| many | (give number) |
| very | (remove or be specific) |
| somewhat | (remove) |
| fairly | (remove) |
| quite | (remove) |

### Link Text

Use descriptive link text:

```html
<!-- Bad -->
<a href="/docs">Click here</a>
<a href="/pricing">Learn more</a>
<a href="/features">Read more</a>

<!-- Good -->
<a href="/docs">Read the documentation</a>
<a href="/pricing">View pricing plans</a>
<a href="/features">Explore all features</a>
```

### Headings

Follow logical hierarchy:

```html
<h1>Page Title</h1>           <!-- One per page -->
  <h2>Major Section</h2>
    <h3>Subsection</h3>
      <h4>Detail</h4>
  <h2>Another Section</h2>
```

## Reading Level Guidelines

This project enforces reading level thresholds using Flesch-Kincaid scoring.

### Grade Level Thresholds

| Content Type | Max Grade Level | Audience |
|--------------|-----------------|----------|
| General | 8 | General public |
| Technical | 12 | Technical audience |

### Marking Content Style

For technical documentation, add one of these:

```html
<!-- In <head> -->
<meta name="content-style" content="technical"/>

<!-- Or on html/body -->
<html lang="en" data-content-style="technical">
<body data-content-style="technical">
```

Available content styles:
- `technical` - Technical documentation, API references (threshold: grade 12)
- Default (no attribute) - General content (threshold: grade 8)

### Writing for Readability

**Use shorter sentences:**
```
<!-- Hard to read (grade 12+) -->
The implementation of the aforementioned functionality requires
consideration of various architectural constraints that may
impact the overall system performance.

<!-- Easier to read (grade 8) -->
This feature needs careful planning. We must consider how it
affects system speed.
```

**Use simpler words:**

| Complex Word | Simpler Alternative |
|--------------|---------------------|
| utilize | use |
| implement | build, create |
| functionality | feature |
| subsequently | then, later |
| facilitate | help, enable |
| approximately | about |
| demonstrate | show |
| modification | change |

**Break up long paragraphs:** Aim for 3-4 sentences per paragraph.

**Use lists:** Convert complex sentences into bullet points when possible.

### Checking Reading Level

```bash
# Check readability
npm run lint:readability

# Check all content quality
npm run lint:content
```

## Content Checklist

Before finalizing content:

- [ ] Spelling checked (run `npm run lint:spelling`)
- [ ] No weasel words or vague language
- [ ] Links have descriptive text
- [ ] Headings follow hierarchy
- [ ] Alt text provided for images
- [ ] Proper capitalization for product names
- [ ] Reading level within threshold (run `npm run lint:readability`)

## Running Quality Checks

```bash
# Check spelling
npm run lint:spelling

# Check grammar/style (advisory)
npm run lint:grammar

# Check reading level
npm run lint:readability

# Run all content checks
npm run lint:content
```

## Special Content

### Code Examples

Wrap code in appropriate elements:

```html
<code>const x = 1</code>           <!-- Inline code -->
<pre><code>                        <!-- Code block -->
function example() {
  return true;
}
</code></pre>
<kbd>Ctrl+S</kbd>                  <!-- Keyboard input -->
<samp>Output text</samp>           <!-- Sample output -->
```

### Abbreviations

Define abbreviations on first use:

```html
<abbr title="HyperText Markup Language">HTML</abbr>
<abbr title="Web Content Accessibility Guidelines">WCAG</abbr>
```

### Dates and Times

Use semantic time element:

```html
<time datetime="2024-01-15">January 15, 2024</time>
<time datetime="14:30">2:30 PM</time>
```

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **fake-content** - Generate realistic fake content for HTML prototypes
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
- **markdown-author** - Write quality markdown content
