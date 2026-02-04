---
name: wordpress-docs-review
description: Review and validate WordPress documentation against official style guide standards. Use when reviewing documentation for WordPress core, themes, plugins, or related projects. Checks compliance with voice/tone, accessibility, inclusivity, code formatting, and technical writing standards.
license: MIT
---

# WordPress Documentation Review

This skill provides systematic review of WordPress documentation against the official WordPress Documentation Style Guide.

## When to Use This Skill

Use this skill when:
- Reviewing WordPress documentation before publication
- Auditing existing documentation for style guide compliance
- Providing feedback on documentation pull requests
- Ensuring documentation meets WordPress standards

## Review Process

### Step 1: Understand the Documentation Type

Identify the documentation type to apply appropriate standards:
- **End-user documentation**: Focus on clarity, accessibility, and conversational tone
- **Developer documentation**: Allow technical precision while maintaining clarity
- **Code reference**: Emphasize accuracy and code standards compliance
- **Tutorial/guide**: Check procedural clarity and step-by-step flow

### Step 2: Systematic Review

Review documentation in this order for comprehensive coverage:

#### A. General Guidelines

**Document Structure**
- [ ] Follows defined structure with clear hierarchy
- [ ] Uses proper heading levels (H1 → H6, no skipping)
- [ ] Breaks text into digestible paragraphs (not walls of text)
- [ ] Includes introductory context before diving into details

**Voice and Tone**
- [ ] Conversational yet professional tone
- [ ] Avoids "we" statements (e.g., "we recommend" → "you can")
- [ ] Uses second person ("you") to address readers directly
- [ ] Avoids colloquialisms, slang, and cultural references
- [ ] No excessive claims about WordPress products/features
- [ ] No predictions about future features

**Accessibility**
- [ ] Alt text provided for all images (50 char limit)
- [ ] No color-only information conveyance
- [ ] Clear link text (not "click here")
- [ ] Proper table structure (no complex rowspan/colspan)
- [ ] No flickering/flashing content

**Inclusivity**
- [ ] Gender-neutral language throughout
- [ ] Uses "they/their/them" for singular pronouns
- [ ] Avoids ableist language
- [ ] No cultural/religious bias
- [ ] Diverse examples (names, locations, professions)
- [ ] Preferred terminology:
  - "allowlist" (not "whitelist")
  - "blocklist" (not "blacklist")
  - "main" (not "master" branch)
  - "primary/subordinate" (not "master/slave")

**Global Audience**
- [ ] American English spelling (color, optimize)
- [ ] Date format: Month DD, YYYY (e.g., October 28, 2025)
- [ ] Spells out numbers one through nine
- [ ] Times in UTC when relevant
- [ ] No idioms or culturally-specific references
- [ ] Simple sentence structure for translation

#### B. Language and Grammar

**Voice and Tense**
- [ ] Active voice (not passive)
- [ ] Present tense (not future)
- [ ] Second person perspective

**Capitalization**
- [ ] Sentence case for headings
- [ ] UI elements match exact capitalization from interface
- [ ] Proper nouns capitalized appropriately

**Articles and Clarity**
- [ ] Articles (a, an, the) included where appropriate
- [ ] Contractions used appropriately
- [ ] Conditional clauses before instructions
- [ ] Clear pronoun antecedents

#### C. Developer Content

**Code in Text**
- [ ] Monospace font for: filenames, paths, commands, functions, variables, UI elements with user input
- [ ] Proper formatting for method names with empty parentheses: `delete()`
- [ ] Keywords not used as verbs or pluralized

**Code Examples**
- [ ] Proper indentation (spaces, not tabs)
- [ ] Lines wrapped at 80 characters
- [ ] Introductory sentence before code blocks
- [ ] Follows WordPress Coding Standards
- [ ] Syntax highlighting where applicable

**Placeholders**
- [ ] Enclosed in `<var>` tags in HTML or backticks+asterisks in Markdown
- [ ] Uppercase with underscores: `*`POST_ID`*` or `<var>POST_ID</var>`
- [ ] No possessive pronouns (MY_, YOUR_)
- [ ] Description list provided for multiple placeholders

**Command-line Syntax**
- [ ] Dollar sign ($) prompt for commands
- [ ] Optional arguments in square brackets: `[--force]`
- [ ] Mutually exclusive arguments in angle brackets: `<plugin|zip|url>`
- [ ] Multiple values indicated with ellipsis: `...`
- [ ] Proper line continuation characters (\ for Linux, ^ for Windows)

**UI Elements**
- [ ] Names in bold: **Settings**
- [ ] Task-focused instructions (not click-focused)
- [ ] Proper element terminology (button, menu, field)

#### D. Punctuation

- [ ] Serial (Oxford) commas in lists
- [ ] One space after periods
- [ ] Em dashes (—) for breaks, en dashes (–) for ranges
- [ ] Straight quotes (not curly quotes)
- [ ] Minimal exclamation points
- [ ] Minimal parentheses

#### E. Formatting

**Links**
- [ ] Descriptive link text (not "click here" or bare URLs)
- [ ] Cross-references to related content
- [ ] External links to authoritative sources only

**Lists**
- [ ] Numbered lists for sequential steps
- [ ] Bulleted lists for non-sequential items
- [ ] Parallel structure in list items
- [ ] Sentence case for list items

**Media**
- [ ] Images in SVG or PNG format
- [ ] Alt text provided (< 50 characters)
- [ ] Screenshots at appropriate resolution
- [ ] Focused on relevant content

**Tables**
- [ ] Simple structure (avoid rowspan/colspan)
- [ ] Headers properly marked
- [ ] Mobile-friendly layout

### Step 3: Provide Structured Feedback

Organize feedback by priority:

**Critical Issues** (Must fix before publication)
- Accessibility violations
- Incorrect technical information
- Code that doesn't follow WordPress standards
- Offensive or non-inclusive language

**Important Issues** (Should fix)
- Voice/tone inconsistencies
- Unclear instructions
- Missing alt text or descriptions
- Formatting inconsistencies

**Suggestions** (Nice to have)
- Style improvements
- Additional examples
- Enhanced clarity

### Step 4: Generate Review Output

Format the review as:

```markdown
## WordPress Documentation Review

### Summary
[Brief overview of documentation quality and main findings]

### Critical Issues
1. [Issue with specific location and fix]
2. [Issue with specific location and fix]

### Important Issues
1. [Issue with specific location and fix]
2. [Issue with specific location and fix]

### Suggestions
1. [Improvement with rationale]
2. [Improvement with rationale]

### Positive Highlights
- [What the documentation does well]
- [Effective techniques used]

### Overall Assessment
[Overall rating and readiness for publication]
```

## Reference Materials

For detailed guidance on specific topics, consult:
- `references/developer-content.md` - Code examples, placeholders, command-line syntax, UI elements
- `references/style-guidelines.md` - Complete style, voice, and tone guidelines with examples

## Key Terminology Reference

| Recommended | Not Recommended |
|-------------|----------------|
| allowlist | whitelist |
| blocklist | blacklist |
| main branch | master branch |
| primary/subordinate | master/slave |
| person with disability | disabled person, handicapped |
| uses synthetic speech | mute, dumb |
| placeholder variable | placeholder |

## Best Practices

1. **Be specific**: Point to exact locations with line numbers or section headings
2. **Provide examples**: Show correct and incorrect versions side-by-side
3. **Explain why**: Connect feedback to style guide principles
4. **Balance criticism**: Acknowledge what works well
5. **Prioritize**: Focus on issues that impact understanding or accessibility first
