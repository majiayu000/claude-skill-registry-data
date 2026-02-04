---
name: modules-readme-updater
description: Update the README.md file to list all available journal modules under the Features section. Use when adding, removing, or reorganizing modules and keeping documentation in sync.
---

# Modules README Updater

This Skill updates the project README.md to accurately document all existing journal modules in a clear, consistent, and properly indented structure under the Features section.

## When to use this Skill

Use this Skill when:
- A new module is added or removed
- Module names change
- The README documentation is outdated
- You want to ensure modules are documented consistently and alphabetically

## Instructions

### Step 1: Locate the insertion point

1. Open README.md.
2. Start updating from line 12.
3. Preserve existing indentation and formatting.

### Step 2: Update the Features section

1. Ensure the section header exists:

### Features

2. Under Features, add or update the parent bullet:

- Daily logging of your life

### Step 3: List all modules as sub-items

1. Add all modules as child list items under “Daily logging of your life”.
2. Each module must:
   - Be indented as a sub-list
   - Represent exactly one module
   - Use consistent naming

Example structure:

### Features

- Daily logging of your life
  - Energy
  - Health
  - Mood
  - Sexual activity
  - Sleep

### Step 4: Alphabetical ordering

1. Sort all module names alphabetically.
2. Do not group, filter, or reorder manually beyond alphabetical order.
3. Do not omit any existing module.

### Step 5: Formatting rules

- Use spaces, not tabs
- Keep indentation consistent
- Do not add descriptions or extra text
- Do not modify other sections of README.md

## Validation checklist

- README.md updated starting at line 12
- Features section exists
- “Daily logging of your life” is the parent item
- All modules are listed
- Modules are alphabetically ordered
- Markdown indentation is correct
- No unrelated content was changed

## Output expectation

The Features section clearly documents all journal modules as sub-features of daily life logging, using clean and valid Markdown.
