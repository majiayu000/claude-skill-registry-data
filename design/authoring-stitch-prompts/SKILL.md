---
name: authoring-stitch-prompts
description: >
  Converts natural-language descriptions or UI spec files into optimized Google Stitch prompts.
  Use when creating, refining, or validating design directives for Google Stitch.
  The Skill follows Stitch best practices—short, directive prompts focused on screens, structure, and visual hierarchy with clear UI vocabulary, concise style cues, and one primary intent per prompt.
  Trigger when the user wants to prepare or improve prompts for Stitch.
allowed-tools: Read, Grep, Write
---

# Authoring Stitch Prompts

## Quick Start
1. **Collect context** – accept natural language, specs, or referenced files describing the screen/app.
2. **Parse essentials** – identify app type, screen focus, layout elements, and visual cues.
3. **Detect split points** – analyze if input contains multiple screens or distinct intents (>2). Apply smart defaults: split if >2 screens/intents, else combine. Users can request regeneration with different approach.
4. **Filter aggressively** – strip ALL non-UI concerns (backend, auth, APIs, caching, error handling, performance metrics, code-level specs). Focus EXCLUSIVELY on visual layout, components, colors, typography, spacing, and interaction patterns.
5. **Condense** – rewrite into one atomic Stitch directive using "Design/Create/Add…" phrasing.
6. **Structure output** – follow the Stitch prompt template (directive sentence → bullet list → 3–6 style cues → constraints). Do NOT use multi-section headings.
7. **Validate** – ensure UI nouns are present, word count <250, NO technical implementation terms, and format matches EXAMPLES.md structure before returning the prompt.

Use this Skill whenever users need Stitch-ready wording, prompt refinements, or style-consistent rewrites.

---

## File Output (.google-stitch/{feature}/)

Generate optimized prompts in **feature-based directories** with organized artifact storage:

1. **Feature Name (Directory)**:
   - Derive from main screen/page purpose
   - Lowercase, replace whitespace with hyphens
   - Strip non `a-z0-9-` characters, collapse duplicate hyphens, trim ends
   - Examples: "analytics dashboard" → `dashboard`, "landing page" → `landing`, "admin panel" → `admin-panel`
   - Keep semantic and concise (prefer "dashboard" over "analytics-dashboard" when unambiguous)

2. **Directory Structure**:
   - Create feature directory: `.google-stitch/{feature}/`
   - Pre-create subdirectories:
     * `exports/` - For Stitch-generated outputs (PNG, SVG, HTML)
     * `wireframes/` - For pre-work mockups and reference images
   - Prompt files live at feature root

3. **File Composition**:
   - Start with `<!-- Layout: {Title Case Name} -->` HTML comment label
   - Add layout prompt content
   - Add `---` separator line
   - For each component:
     * Add `<!-- Component: {Title Case Name} -->` HTML comment label
     * Add component prompt content
     * Add `---` separator (between components, not after last)

4. **6-Prompt Stitch Limit**:
   - Count total prompts (layout + all components)
   - If ≤6 prompts: Save as `prompt-v{version}.md`
   - If >6 prompts: Split into multiple part files
     * Part 1: Layout + first 5 components (6 prompts)
     * Part 2: Next 6 components
     * Part N: Remaining components (max 6 per part)
     * Save as: `prompt-v{version}-part{N}.md`
     * Warn user about Stitch's 6-screen generation limit

5. **Version Auto-Increment**:
   - Scan `.google-stitch/{feature}/prompt-v*.md`
   - Find highest version number, increment automatically
   - Start at v1 if no matches
   - Each feature maintains independent version history
   - Note: Entire file versioned together (not per-component)

6. **File Path Resolution**:
   - Resolve repo root via `git rev-parse --show-toplevel`
   - Create `{root}/.google-stitch/{feature}/` directory
   - Create `{feature}/exports/` and `{feature}/wireframes/` subdirectories
   - Write composed Markdown file to `{feature}/prompt-v{version}.md`

7. **Report**:
   - After presenting prompts inline, show file info:
     ```
     📂 Feature: {feature}/
     📄 File: prompt-v{version}.md

     Contains {N} prompts (within 6-prompt limit ✓):
       • Layout: {Title}
       • Component: {Title}
       • Component: {Title}

     Directory structure:
       .google-stitch/{feature}/
       ├── prompt-v{version}.md     ← Generated prompt
       ├── exports/                 ← Place Stitch outputs here
       └── wireframes/              ← Place mockups/references here

     Usage:
       1. Copy prompt file → Paste into Stitch → Generate designs
       2. Save Stitch exports to exports/ directory
       3. Store wireframes/mockups in wireframes/ directory
     ```

**Examples:**

Multi-component page (4 prompts):
```
Input: "Analytics dashboard with KPI cards, revenue chart, and subscriptions table"

Output: .google-stitch/dashboard/prompt-v1.md

Directory created:
  .google-stitch/dashboard/
  ├── prompt-v1.md
  ├── exports/
  └── wireframes/

File content:
  <!-- Layout: Analytics Dashboard -->
  Design a web dashboard page for SaaS analytics overview.
  [...layout prompt content...]

  ---

  <!-- Component: KPI Metrics -->
  Design metric cards displaying key SaaS performance indicators.
  [...component prompt content...]

  ---

  <!-- Component: Revenue Chart -->
  Design an interactive line chart for monthly revenue tracking.
  [...component prompt content...]

  ---

  <!-- Component: Subscriptions Table -->
  Design a subscription activity table showing recent changes.
  [...component prompt content...]
```

Single component (1 prompt):
```
Input: "Login form with email and password"

Output: .google-stitch/login/prompt-v1.md

Directory created:
  .google-stitch/login/
  ├── prompt-v1.md
  ├── exports/
  └── wireframes/

File content:
  <!-- Component: Login Form -->
  Design a login form for web application.
  [...component prompt content...]
```

Large page split (8 prompts → 2 files):
```
Input: "Admin panel with navigation, dashboard, users, roles, settings, audit logs, notifications"

Output: .google-stitch/admin-panel/prompt-v1-part1.md (6 prompts)
- Layout: Admin Panel
- Component: Navigation
- Component: Dashboard
- Component: Users
- Component: Roles
- Component: Settings

Output: .google-stitch/admin-panel/prompt-v1-part2.md (2 prompts)
- Component: Audit Logs
- Component: Notifications

Directory created:
  .google-stitch/admin-panel/
  ├── prompt-v1-part1.md
  ├── prompt-v1-part2.md
  ├── exports/
  └── wireframes/

⚠️ Warning: Use part1 first, then part2 in separate Stitch session
```

Iteration (auto-increment):
```
Existing: .google-stitch/dashboard/prompt-v1.md

Input: "Update analytics dashboard with new metrics"

Auto-detected version → prompt-v2.md

Output: .google-stitch/dashboard/prompt-v2.md

Directory structure:
  .google-stitch/dashboard/
  ├── prompt-v1.md      ← Previous version
  ├── prompt-v2.md      ← New version
  ├── exports/
  └── wireframes/

(Entire file versioned together, versions coexist in same directory)
```

**Feature Directory Benefits:**
- **Organized artifacts**: All design files grouped by feature
- **Version history**: All versions accessible in one location
- **Design workflow**: Natural home for Stitch exports and wireframes
- **Stitch-native**: Uses Stitch's `---` separator convention
- **Auto-increment**: Detects existing versions, increments automatically
- **Batch generation**: Copy one file, generate entire page
- **Copy-paste ready**: File content works directly in Stitch interface

---

## Input Types

**Accepted**
- Natural-language descriptions (single screen or short flows)
- Markdown/YAML/JSON specs (`/specs/dashboard.md`)
- Revision directives ("move KPI cards above chart", "convert to French", "change button to green")
- References to uploaded wireframes or images
- Language conversion requests ("switch to Spanish", "German version")

**Input Detail Levels**

All detail levels are valid—Stitch infers patterns from minimal descriptions:

- **High-level** (minimal): "fitness tracker app", "professional project management dashboard"
- **Medium**: "fitness tracker with daily goals and progress charts"
- **Detailed**: Full component list with specific features and interactions

Use adjectives to convey vibe when details are sparse ("vibrant fitness app", "minimal meditation app").

---

## Workflow Overview

High-level loop: parse → condense → format → validate.  
Detailed branching logic, including cue extraction and revision handling, lives in [WORKFLOW.md](WORKFLOW.md).

---

## Output Structure

Prompts must follow the Stitch-friendly template:
- One-sentence description of the app/screen + primary intent.
- Bullet list (3–6 items) covering layout, components, or flows.
- Visual style cues (palette, typography, density, tone).
- Optional behavior/constraint reminders (responsiveness, export format).

Reference [templates/authoring-stitch-prompts-template.md](templates/authoring-stitch-prompts-template.md) for wording patterns.

---

## Examples

Representative before/after samples (SaaS dashboard, banking app, iterative edits, spec conversions) are in [EXAMPLES.md](EXAMPLES.md). Use them to mirror tone and formatting; keep this file lean by not re-embedding the full transcripts here.

---

## Implementation Notes

* Keep SKILL.md under 500 lines; detailed prompt transformation logic can go in `REFERENCE.md` or `templates/authoring-stitch-prompts-template.md`.
* Use concise, declarative language.
* Avoid narrative, meta, or conversational phrasing in outputs.
* Always output one atomic, Stitch-compatible prompt per request.

---

## Common Issues

- **Prompts too verbose** – Re-run formatting with the template and trim narration. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)#L1 for guidance.
- **Missing style cues** – Derive palette/typography keywords from user input or prior session context before finalizing. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)#L25.
- **Multi-goal briefs** – Split into multiple prompts; re-emphasize Stitch’s atomic focus. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)#L43.

---

## Reference Files

For advanced usage:

* [REFERENCE.md](REFERENCE.md) — Overview of Stitch best practices
* [EXAMPLES.md](EXAMPLES.md) — Sample transformations
* [WORKFLOW.md](WORKFLOW.md) — Detailed processing loop
* [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Error-handling guidance
* [templates/authoring-stitch-prompts-template.md](templates/authoring-stitch-prompts-template.md) — Output format template

---

## Version History

* v1.0.0 (2025-11-10): Initial release — authoring assistant for Stitch prompt optimization.
