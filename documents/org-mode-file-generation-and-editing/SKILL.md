---
name: Org-Mode File Generation and Editing
description: |
  Comprehensive org-mode file generation and editing with proper syntax, formatting, and structure.
  Use when Claude needs to work with org-mode files (.org) for: (1) Creating new org-mode documents,
  (2) Editing existing org files while preserving formatting, (3) Converting content to org-mode format,
  (4) Ensuring correct org-mode syntax for headlines, properties, links, timestamps, and other elements.
  IMPORTANT: This skill is for general org-mode files. For org-roam notes (files in roam/ directory),
  use the org-roam-skill instead.
---

# Org-Mode File Generation and Editing

This skill provides comprehensive knowledge of org-mode file format, syntax, and best practices for generating and editing org-mode documents.

## Skill vs Org-Roam Skill

**Use this skill for**:
- General org-mode files (.org) anywhere in the filesystem
- Documents, notes, TODO lists, project plans
- Any org file NOT in an org-roam directory

**Use org-roam-skill for**:
- Files in `/roam/` or `/org-roam/` directories
- Notes requiring org-roam database sync
- Creating notes via emacsclient and org-roam functions

## Quick Reference

### Most Common Operations

**Create new org file**:
1. Choose or modify a template from `assets/templates/`
2. Apply proper headline structure with `*` markers
3. Add properties drawer if needed (for IDs and metadata)
4. Use correct timestamp format for scheduling

**Edit existing org file**:
1. Read the file first to understand structure
2. Preserve existing formatting and indentation
3. Maintain headline hierarchy (don't skip levels)
4. Keep properties drawers intact

**Get syntax help**:
- Headlines and structure → Read `references/org-syntax.md`
- Properties and metadata → Read `references/properties.md`
- Links → Read `references/links.md`
- Timestamps and scheduling → Read `references/timestamps.md`
- Real examples → Read `references/examples.md`

## Core Principles

1. **Org-mode is plain text with structure**: No special encoding, just text with formatting conventions
2. **Headlines create hierarchy**: Use `*` for levels (*, **, ***, etc.)
3. **Indentation varies**: Matters for lists, doesn't matter for headline content
4. **Properties must be first**: `:PROPERTIES:` drawer immediately after headline
5. **Timestamps have specific formats**: Active `<>` vs inactive `[]`

## Essential Syntax at a Glance

### Headlines

```org
* Top level headline
** Second level headline
*** Third level headline
**** Fourth level headline
```

With metadata:

```org
* TODO [#A] Task title :tag1:tag2:
** DONE [#B] Completed task :work:
```

Format: `*+ [TODO-keyword] [priority] Title :tags:`

### Properties Drawer

Must be immediately after headline (no blank lines):

```org
* Headline
:PROPERTIES:
:ID: unique-id-here
:CUSTOM_ID: readable-id
:CREATED: [2025-12-13 Fri]
:END:

Content goes here after properties.
```

### Common Properties

```org
:PROPERTIES:
:ID: 8f7a3c2e-9b1d-4e5f-a6c7-3d8e9f0a1b2c
:CUSTOM_ID: my-section
:CATEGORY: work
:EFFORT: 3:30
:CREATED: [2025-12-13 Fri 10:00]
:END:
```

Generate IDs with: `/Users/tahirbutt/.claude/skills/orgmode/scripts/generate_id.py`

### Links

```org
[[https://example.com][Link Description]]
[[file:path/to/file.org][File Link]]
[[#custom-id][Internal Link]]
[[id:UUID][ID Link]]
```

### Timestamps

```org
<2025-12-13 Fri>                    # Active (appears in agenda)
[2025-12-13 Fri]                    # Inactive (metadata only)
<2025-12-13 Fri 14:30>              # With time
<2025-12-13 Fri 14:30-16:00>        # Time range
SCHEDULED: <2025-12-15 Mon>         # When to start
DEADLINE: <2025-12-20 Fri>          # When must finish
<2025-12-13 Fri +1w>                # Repeat weekly
```

### Lists

```org
- Unordered item
- Another item
  - Nested item

1. Ordered item
2. Second item

- [ ] Checkbox unchecked
- [X] Checkbox checked
```

### Text Emphasis

```org
*bold*
/italic/
_underlined_
=verbatim=
~code~
+strikethrough+
```

### Blocks

```org
#+BEGIN_SRC python
def hello():
    print("Hello, world!")
#+END_SRC

#+BEGIN_EXAMPLE
Literal text here
#+END_EXAMPLE

#+BEGIN_QUOTE
Quotation here
#+END_QUOTE
```

## Workflows

### Workflow A: Creating New Org Files

**Step 1: Determine purpose**

What type of file are you creating?
- General document → Use `assets/templates/basic.org`
- Project plan → Use `assets/templates/project.org`
- Meeting notes → Use `assets/templates/meeting-notes.org`
- Custom → Start from scratch or adapt template

**Step 2: Set up file metadata**

Add document-level keywords at the top:

```org
#+TITLE: Document Title
#+AUTHOR: Author Name
#+DATE: <2025-12-13 Fri>
#+FILETAGS: :tag1:tag2:
```

**Step 3: Create headline structure**

Start with main headlines:

```org
* Introduction
* Main Content
** Subtopic 1
** Subtopic 2
* Conclusion
```

**Step 4: Add properties if needed**

For entries needing unique IDs or metadata:

```org
* Important Section
:PROPERTIES:
:ID: 8f7a3c2e-9b1d-4e5f-a6c7-3d8e9f0a1b2c
:CUSTOM_ID: important
:CREATED: [2025-12-13 Fri]
:END:
```

Generate UUID with: `python3 /Users/tahirbutt/.claude/skills/orgmode/scripts/generate_id.py`

**Step 5: Add content**

Write content under headlines. Add:
- Links with `[[URL][description]]`
- Timestamps with `<YYYY-MM-DD Day>` or `[YYYY-MM-DD Day]`
- Lists with `-` or `1.`
- Emphasis with `*bold*`, `/italic/`, etc.

**Step 6: Add TODO items and scheduling if applicable**

```org
* TODO [#A] Important task
SCHEDULED: <2025-12-15 Mon>
DEADLINE: <2025-12-20 Fri>
:PROPERTIES:
:EFFORT: 3:00
:END:
```

**Step 7: Validate syntax**

- Check headline hierarchy (no skipped levels like * then ***)
- Verify properties drawers immediately follow headlines
- Ensure timestamps use correct format
- Confirm links use `[[URL][desc]]` format

### Workflow B: Editing Existing Org Files

**Step 1: Read and understand**

Use the Read tool to examine the existing file:
- Note the headline structure
- Identify existing properties
- Observe formatting style
- Check for any custom patterns

**Step 2: Preserve structure**

When editing:
- Don't change headline levels unnecessarily
- Keep existing properties drawers intact
- Maintain indentation style
- Preserve blank line patterns

**Step 3: Make changes carefully**

**Adding headlines**:
- Use appropriate level (* for top, ** for sub, etc.)
- Maintain hierarchy (don't skip levels)

**Modifying properties**:
- Keep `:PROPERTIES:` and `:END:` markers
- Use `:KEY: value` format
- Don't remove important properties like `:ID:`

**Adding content**:
- Use existing emphasis style
- Match link format used in file
- Use same timestamp format (active vs inactive)

**Step 4: Validate changes**

After editing, verify:
- Headline structure is valid
- Properties drawers are well-formed
- Timestamps use correct format
- Links are properly formatted

## Common Patterns

### Meeting Notes

```org
#+TITLE: Team Meeting
#+DATE: <2025-12-13 Fri>

* Meeting: Sprint Planning <2025-12-13 Fri 10:00-11:00>
:PROPERTIES:
:ATTENDEES: Alice, Bob, Charlie
:LOCATION: Conference Room A
:END:

** Agenda
1. Review last sprint
2. Plan current sprint
3. Action items

** Discussion
Notes here.

** TODO Action item 1
DEADLINE: <2025-12-20 Fri>
:PROPERTIES:
:ASSIGNED_TO: Alice
:END:
```

### Project Planning

```org
* PROJECT Website Redesign
:PROPERTIES:
:CUSTOM_ID: website-project
:START_DATE: <2025-01-15 Wed>
:END:
SCHEDULED: <2025-01-15 Wed>
DEADLINE: <2025-03-31 Mon>

** TODO Phase 1: Design
DEADLINE: <2025-02-15 Sat>

** TODO Phase 2: Development
DEADLINE: <2025-03-20 Thu>
```

### TODO List with Repeating Tasks

```org
* TODO Weekly review
SCHEDULED: <2025-12-16 Mon 09:00 +1w>
:PROPERTIES:
:EFFORT: 1:00
:END:

* TODO Pay rent
DEADLINE: <2025-12-31 Wed +1m>

* TODO Exercise
SCHEDULED: <2025-12-13 Fri .+2d>
```

### Documentation with Links

```org
* Project Documentation

** Setup Guide
See [[file:docs/setup.org][setup instructions]] for installation.

** API Reference
[[file:docs/api.org::*Authentication][Authentication section]]

** Resources
- [[https://example.com][Official Site]]
- [[file:README.org][Project README]]
```

## When to Consult References

The `references/` directory contains detailed syntax guides. Read them when you need:

**org-syntax.md** - Core structure and elements
- Headlines and hierarchy
- Lists (unordered, ordered, description, checkboxes)
- Text emphasis and markup
- Blocks (SRC, EXAMPLE, QUOTE, etc.)
- Tables
- Comments
- Document keywords

**properties.md** - Properties and metadata
- Properties drawer syntax and rules
- Standard properties (ID, CUSTOM_ID, CATEGORY, EFFORT, etc.)
- Custom properties
- Property inheritance
- When to use properties vs other metadata

**links.md** - All link types
- External links (web, email, file)
- Internal links (headlines, custom IDs, targets)
- ID links for stability
- Link abbreviations
- Image links
- Best practices for link formatting

**timestamps.md** - Dates, times, and scheduling
- Active vs inactive timestamps
- Date and time ranges
- SCHEDULED and DEADLINE
- Repeating timestamps (+1d, +1w, +1m, etc.)
- Delay and warning periods
- Time duration and effort
- Clocking

**examples.md** - Real-world examples
- Complete example files
- Meeting notes
- Project plans
- TODO lists
- Research notes
- Course notes
- Recipe collection
- Best practices demonstrated

## Reference Navigation Guide

**Need to...**
- Understand headline syntax → `references/org-syntax.md`
- Format lists correctly → `references/org-syntax.md`
- Create properties drawer → `references/properties.md`
- Add unique ID → `references/properties.md` + `scripts/generate_id.py`
- Insert links → `references/links.md`
- Schedule tasks → `references/timestamps.md`
- Create repeating events → `references/timestamps.md`
- See complete examples → `references/examples.md`

**Complex scenarios**:
- Property inheritance → `references/properties.md`
- Link abbreviations → `references/links.md`
- Repeater types (+, ++, .+) → `references/timestamps.md`
- Multi-level projects → `references/examples.md`

## Templates

Pre-built templates in `assets/templates/`:

**basic.org** - Simple document structure
- Document metadata (title, author, date)
- Basic headline hierarchy
- Minimal structure for general documents

**project.org** - Project planning template
- Project properties (ID, dates, category)
- Timeline with phases
- TODO items with scheduling
- Team and resources sections
- Meeting schedule

**meeting-notes.org** - Meeting notes template
- Meeting metadata (attendees, location, time)
- Agenda structure
- Discussion notes sections
- Action items with assignments
- Next meeting scheduling

**Using templates**:
1. Copy template content
2. Replace placeholder text
3. Update dates and metadata
4. Modify structure as needed
5. Generate new IDs if required

## Generating Unique IDs

For properties that need unique identifiers:

```bash
python3 /Users/tahirbutt/.claude/skills/orgmode/scripts/generate_id.py
```

Returns a UUID like: `8f7a3c2e-9b1d-4e5f-a6c7-3d8e9f0a1b2c`

Use in properties:

```org
* Headline
:PROPERTIES:
:ID: 8f7a3c2e-9b1d-4e5f-a6c7-3d8e9f0a1b2c
:END:
```

## Common Mistakes to Avoid

1. **Blank line before properties**
   ```org
   * Headline

   :PROPERTIES:  # ✗ Wrong - blank line before drawer
   ```

   ```org
   * Headline
   :PROPERTIES:  # ✓ Correct - no blank line
   ```

2. **Skipping headline levels**
   ```org
   * Level 1
   *** Level 3  # ✗ Wrong - skipped level 2
   ```

   ```org
   * Level 1
   ** Level 2   # ✓ Correct - sequential levels
   ```

3. **Wrong timestamp format**
   ```org
   <12-13-2025>     # ✗ Wrong format
   <2025-12-13 Fri> # ✓ Correct format
   ```

4. **Missing link brackets**
   ```org
   [file:doc.org][Link]    # ✗ Wrong - single brackets
   [[file:doc.org][Link]]  # ✓ Correct - double brackets
   ```

5. **Space in emphasis markers**
   ```org
   * bold *         # ✗ Wrong - space inside
   *bold*           # ✓ Correct - no spaces
   ```

## Best Practices

1. **Use templates for consistency**: Start with templates for common document types
2. **Add IDs to important entries**: Use unique IDs for stable references
3. **Prefer CUSTOM_ID for human-readable links**: Use `#custom-id` over UUIDs when appropriate
4. **Use inactive timestamps for metadata**: `[2025-12-13 Fri]` for creation dates
5. **Add EFFORT to tasks**: Helps with planning and time tracking
6. **Tag headlines for organization**: Use `:tags:` for categorization
7. **Link with descriptions**: Use `[[URL][description]]` format
8. **Document SCHEDULED vs DEADLINE**: SCHEDULED = start, DEADLINE = must finish
9. **Use repeaters for recurring tasks**: `+1w` for weekly, `+1m` for monthly, etc.
10. **Keep structure simple**: Don't nest too deeply (3-4 levels max usually)

## Troubleshooting

**Properties not recognized**:
- Ensure no blank line between headline and `:PROPERTIES:`
- Check `:END:` is present
- Verify `:KEY: value` format with colon-key-colon space

**Links not working**:
- Confirm double bracket `[[...]]` format
- Check file paths are correct (relative or absolute)
- Verify Custom IDs exist if using `#id` links

**Timestamps not appearing**:
- Use active `<>` for agenda items
- Use inactive `[]` for metadata
- Include day of week: `<2025-12-13 Fri>`

**Emphasis not rendering**:
- Remove spaces: `*bold*` not `* bold *`
- Ensure matching markers: `*bold*` not `*bold`

## Advanced Topics

For advanced org-mode features, consult the references:

- **Property inheritance** → `references/properties.md`
- **Column view properties** → `references/properties.md`
- **Link abbreviations** → `references/links.md`
- **Radio and dedicated targets** → `references/links.md`
- **Repeater types** → `references/timestamps.md`
- **Time clocking** → `references/timestamps.md`
- **Complex project structures** → `references/examples.md`

## Summary

This skill provides everything needed to create and edit org-mode files correctly:

- **Quick reference** for common syntax
- **Two workflows** (creating new, editing existing)
- **Common patterns** for typical use cases
- **Templates** for quick starts
- **Detailed references** for deep dives
- **Examples** for real-world guidance

Use the quick reference and workflows for most tasks. Consult references when you need detailed syntax or are working with complex scenarios. Check examples to see best practices in action.
