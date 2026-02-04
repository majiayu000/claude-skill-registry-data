---
name: skill-browser
description: Discover, browse, and compare agent skills from repositories. Shows new skills, updates, and helps users find relevant skills. Use when exploring available skills or checking for updates.
license: MIT
---

# Skill Browser

Discover and browse agent skills from GitHub repositories, compare with locally installed skills, and identify updates or new additions.

## When to Use This Skill

Use skill-browser when you need to:

- Discover new skills available in a repository
- Check for updates to installed skills
- Browse skills by category
- Find skills relevant to specific needs
- Compare local installation with repository
- Get an overview of available skills before installing

## Browsing Process

### Step 1: Identify Repository

Extract repository information from user request:

**Repository Formats**:

- Short form: "tnez/dot-agents"
- Full URL: "<https://github.com/tnez/dot-agents>"
- Default: If not specified, use "tnez/dot-agents"

**Branch**:

- Default to "main"
- Can specify: "browse skills in tnez/dot-agents branch develop"

### Step 2: Fetch Skills Catalog

Retrieve the repository's CATALOG.md file:

**URL Construction**:

````text
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/CATALOG.md
```text

**Example**:

```text
https://raw.githubusercontent.com/tnez/dot-agents/main/CATALOG.md
```text

**Use WebFetch** to download CATALOG.md content.

**Fallback if CATALOG.md Missing**:

If CATALOG.md doesn't exist (404 error):

1. Inform user catalog is not available
2. Suggest browsing GitHub repository directly
3. Or manually provide skill path for installation

### Step 3: Parse Catalog

Extract skill information from CATALOG.md:

**Expected Format**:

```markdown
## Category Name

### skill-name

- **Path:** category/skill-name
- **Added:** YYYY-MM-DD
- **Updated:** YYYY-MM-DD
- **Description:** Brief description
- **Files:** SKILL.md, CONTEXT.md, scripts/
- **Dependencies:** tool1, tool2
```text

**Extract for Each Skill**:

- Name
- Category (Examples, Documents, Meta)
- Path in repository
- Date added
- Date last updated
- Description
- Available files
- Dependencies (if any)

### Step 4: Check Local Installation

Compare catalog with locally installed skills:

**Discovery**:

Use Glob to find installed skills:

```text
.agents/skills/*/SKILL.md
.claude/skills/*/SKILL.md
~/.agents/skills/*/SKILL.md
~/.claude/skills/*/SKILL.md
```text

**For Each Installed Skill**:

1. Read SKILL.md
2. Extract skill name from YAML frontmatter
3. Add to list of installed skills

**Categorize Skills**:

- **New**: In catalog but not installed
- **Updates Available**: Installed but catalog shows newer date
- **Up to Date**: Installed and matches catalog
- **Local Only**: Installed but not in catalog (custom skills)

### Step 5: Filter and Sort

Organize skills based on user's request:

**By Status**:

- Show only new skills
- Show only updates available
- Show all skills

**By Category**:

- Examples
- Documents
- Meta
- All categories

**By Relevance** (if user specifies interest):

- Match description to user's stated needs
- Prioritize relevant categories

### Step 6: Present Results

Format and display skill information:

**Presentation Format**:

```text
# Available Skills from tnez/dot-agents

## 🆕 New Skills (not installed)

### find-local-events (examples/)
Search for local events with location/datetime disambiguation
- Added: 2025-11-16
- Files: SKILL.md, CONTEXT.md

### markdown-to-pdf (documents/)
Convert markdown to PDF with Pandoc
- Added: 2025-11-15
- Files: SKILL.md, scripts/convert.sh
- Dependencies: pandoc, texlive

## 🔄 Updates Available

### get-weather (examples/)
Fetch weather information using wttr.in
- Installed: 2025-11-10
- Updated: 2025-11-15 (5 days newer)
- Changes: Enhanced error handling

## ✅ Up to Date

### skill-creator (meta/)
Create new agent skills with templates
- Installed: 2025-11-15
- Latest: 2025-11-15 (current)

---

Install skills: "Install find-local-events from tnez/dot-agents"
Update skills: "Update get-weather"
Browse category: "Show me all document skills"
```text

## Examples

### Example 1: Discover New Skills

**User Request**:
"What's new in tnez/dot-agents?"

**Process**:

1. Fetch CATALOG.md from tnez/dot-agents
2. Parse all skills
3. Check local installation
4. Filter to only NEW skills (not installed)
5. Present list with descriptions

**Expected Output**:

```text
# New Skills Available

I found 2 new skills you haven't installed:

1. **find-local-events** (examples/)
   Search for local events with location/datetime disambiguation
   Added: 2025-11-16

2. **image-review-pdf** (documents/)
   Review and analyze images in PDF documents
   Added: 2025-11-16

Would you like to install any of these?
```text

### Example 2: Check for Updates

**User Request**:
"Check for updates to my installed skills"

**Process**:

1. Fetch CATALOG.md
2. Get list of installed skills
3. Compare dates/versions
4. Identify skills with updates
5. Show what's changed (if info available)

**Expected Output**:

```text
# Skill Updates Available

2 of your installed skills have updates:

1. **markdown-to-pdf**
   Installed: 2025-11-10
   Latest: 2025-11-15
   - Added error handling for missing dependencies
   - Improved PDF formatting options

2. **skill-creator**
   Installed: 2025-11-13
   Latest: 2025-11-15
   - New templates added
   - Enhanced validation

Update all? Or select individual skills?
```text

### Example 3: Browse by Category

**User Request**:
"Show me all document-related skills"

**Process**:

1. Fetch CATALOG.md
2. Filter to "Documents" category
3. Present all skills in that category
4. Mark installed vs available

**Expected Output**:

```text
# Documents Skills

## ✅ Installed

- **markdown-to-pdf**: Convert markdown to PDF with Pandoc

## 🆕 Available

- **image-review-pdf**: Review and analyze images in PDF documents
- **docx-to-markdown**: Convert Word documents to markdown

Install a skill: "Install image-review-pdf"
```text

### Example 4: Find Relevant Skills

**User Request**:
"I need skills for working with events and calendars"

**Process**:

1. Fetch CATALOG.md
2. Search descriptions for keywords: "event", "calendar"
3. Rank by relevance
4. Present matching skills

**Expected Output**:

```text
# Skills for Events and Calendars

Found 1 matching skill:

### find-local-events (examples/)
Search for local events, activities, and happenings in a specified location
and timeframe. Handles location disambiguation and datetime clarification.

- Status: Not installed
- Added: 2025-11-16
- Files: SKILL.md, CONTEXT.md

Install: "Install find-local-events"
```text

## Advanced Features

### Skill Comparison

When user wants to compare similar skills:

**Process**:

1. Identify skills with related functionality
2. Fetch SKILL.md for each
3. Compare features, dependencies, complexity
4. Present side-by-side comparison

**Example**:

```text
Comparing event-related skills:

| Feature           | find-local-events | calendar-sync |
| ----------------- | ----------------- | ------------- |
| Search events     | ✓                 | ✗             |
| Location handling | ✓ (with disambig) | ✗             |
| Sync with cal     | ✗                 | ✓             |
| Dependencies      | None              | icalendar     |
| Complexity        | Medium            | High          |

Recommendation: For discovering events, use find-local-events
```text

### Dependency Checking

Before presenting skills, check if dependencies are available:

**Process**:

1. Extract dependencies from catalog
2. Check if tools are installed locally
3. Mark skills as "ready" or "requires setup"
4. Warn about missing dependencies

**Example**:

```text
### markdown-to-pdf
⚠️ Requires: pandoc, texlive (not installed)

Install dependencies first:
  brew install pandoc basictex  # macOS
  apt-get install pandoc texlive  # Linux
```text

### Update All

Batch update multiple skills:

**User Request**: "Update all my installed skills"

**Process**:

1. Check all installed skills for updates
2. Present list of updates
3. Ask for confirmation
4. Use skill-installer to update each one
5. Report results

## Integration with skill-installer

Seamlessly hand off to skill-installer for installation:

**Workflow**:

```text
User: "Browse skills in tnez/dot-agents"
Agent: [Uses skill-browser to show catalog]

Agent: "Found 3 new skills. Would you like to install any?"
User: "Install find-local-events and skill-creator"

Agent: [Uses skill-installer for each]
        "Installing find-local-events..."
        "Installing skill-creator..."
        "Done! Both skills installed to .agents/skills/"
```text

## Best Practices

### Presentation

- **Be concise**: Don't overwhelm with too many skills at once
- **Categorize**: Group by status (new/updates/current)
- **Highlight**: Show most relevant or recently added first
- **Actionable**: Always suggest next steps (install, update, etc.)

### Filtering

- **Default to summary**: Show counts, not full lists initially
- **Allow drilling down**: User can request more details
- **Smart filtering**: Match user's stated interests
- **Status-aware**: Different views for new users vs established users

### Updates

- **Check dates**: Compare installation dates with catalog dates
- **Show changes**: If available, show what's new in updates
- **Batch operations**: Support "update all" efficiently
- **Preserve user data**: Warn about CONTEXT.md and customizations

## Common Pitfalls

- **CATALOG.md not found**: Have fallback strategy
- **Date parsing**: Handle various date formats
- **Missing local skills**: Glob might not find all installations
- **Ambiguous requests**: "Show me skills" - new? all? updates?
- **Large catalogs**: Don't dump 50 skills at once, paginate or summarize

## Error Handling

### Catalog Not Found

```text
✗ CATALOG.md not found in tnez/dot-agents

The repository may not have a skills catalog yet.

Try:
  1. Browse repository directly: https://github.com/tnez/dot-agents
  2. Install specific skill: "Install find-local-events from tnez/dot-agents"
  3. Check if repository has different catalog format
```text

### Network Error

```text
✗ Cannot fetch catalog from tnez/dot-agents
  Network error or repository unavailable

Try:
  1. Check internet connection
  2. Verify repository URL
  3. Try again later
```text

### No Skills Installed

```text
ℹ️ No skills currently installed

You can install skills from tnez/dot-agents:
  "Install skill-creator" - Create new skills
  "Install find-local-events" - Search for local events

Or browse all available skills:
  "Show me all available skills"
```text

## Dependencies

**None** - Pure agentic skill using:

- WebFetch (for downloading CATALOG.md)
- Glob (for finding installed skills)
- Read (for checking installed skill details)

No external tools required.

## Catalog Format Requirements

For repositories to work with skill-browser, CATALOG.md should follow this format:

```markdown
# Agent Skills Catalog

Last updated: YYYY-MM-DD

## Category Name

### skill-name

- **Path:** category/skill-name
- **Added:** YYYY-MM-DD
- **Updated:** YYYY-MM-DD
- **Description:** One-line description
- **Files:** SKILL.md, optional files
- **Dependencies:** comma-separated list or "None"
```text

This format enables automated parsing and presentation.

## Troubleshooting

### Q: Catalog shows skill but it's not found when installing

A: Path in catalog may be incorrect. Try:

- Check repository structure on GitHub
- Install using full path
- Report issue to repository maintainers

### Q: How do I know if a skill is compatible?

A: Check:

- Dependencies listed in catalog
- Agent requirements in SKILL.md
- Platform compatibility notes

### Q: Can I browse private repositories?

A: No - WebFetch only works with public repositories. For private repos, use GitHub authentication or clone locally.

### Q: Why don't I see my locally installed custom skills?

A: Skill-browser only shows repository catalogs. Your local-only skills won't appear in repository listings.

## Resources

- Agent Skills Repository: <https://github.com/tnez/dot-agents>
- CATALOG.md format specification (in this repository)
- skill-installer for installation
- Agent Skills Specification: <https://github.com/anthropics/skills/blob/main/agent_skills_spec.md>
````
