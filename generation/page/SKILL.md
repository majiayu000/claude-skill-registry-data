---
name: page
description: Scaffold a new page from the site's template system (e.g., new course landing page)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - TodoWrite
model: sonnet
argument-hint: <page-type> <slug> [key=value ...]
---

# Page — scaffold a new page

You are running the `page` skill. Your job: create a new page for an existing website, using its template system if available, or by cloning the most similar existing page.

## Step-by-step

### Step 0 — Parse arguments

Parse `$ARGUMENTS`:
- First word: page type (e.g., `course`, `landing`, `generic`)
- Second word: slug (e.g., `ai-automation`)
- Remaining: key=value pairs for page data

Site root: `--root <path>` argument, or default to current working directory. Convention: site repos live at `~/Sites/<name>/`.

### Step 1 — Detect site structure

Check if the site uses the template system:
- Does `templates/` directory exist?
- Does `site.json` exist?

**If templated (templates/ + site.json exist):**
1. Read `site.json` to understand page types and required fields
2. Read the relevant template (e.g., `templates/pages/course.html`)
3. Prompt user for any missing required fields
4. Add new entry to `site.json`
5. Run `python3 tools/html_template_engine.py --templates templates/ --out . --data site.json`

**If raw HTML (no template system):**
1. Find the most recent page of the same type (Glob for `course-*.html`)
2. Read it to understand the structure
3. Create a copy with the new slug
4. Replace page-specific content (title, description, course name, etc.)
5. Flag: "Consider running `/refactor extract-template` to avoid future copy-paste"

### Step 2 — Fill in content

For each required field not provided in arguments:
- Ask the user for the value
- OR use sensible defaults with `[REVIEW]` markers

### Step 3 — Post-generation validation

Run: `python3 tools/site_audit.py --root "<site_root>" --mechanical-only --checks missing_meta,link_integrity`

Report any issues found on the new page.

### Step 4 — Summary

Report:
- File created: `<path>`
- Method used: template or clone
- Validation: pass/fail
- Next steps (e.g., "update the course description and hero image")

## See also

- [tools/page_scaffold.py](../../../tools/page_scaffold.py) — template-based generator
- [tools/html_template_engine.py](../../../tools/html_template_engine.py) — Jinja2 builder
- [workflows/page_generation.md](../../../workflows/page_generation.md) — the SOP
