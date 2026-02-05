---
name: updating-readme
description: Updates existing README.md files after code changes. Use for requests to update, check, fix, or add to an existing README. Trigger phrases include "update readme", "check readme", "is the readme current", "add to readme", "fix readme", "readme out of date". Also use after adding dependencies, environment variables, or configuration. For creating new READMEs from scratch, use writing-documentation instead.
version: 1.0.0
---

# Updating README

## Overview

Maintains existing README.md files with minimal, targeted updates that preserve the original style and structure.

## When to Use This Skill

Use updating-readme when:
- README exists and needs a section update
- New dependency was added
- New environment variable was introduced
- Configuration options changed
- User asks "is the README up to date?" or "check the README"
- Minor corrections or additions needed

## Handoff Rules

### To writing-documentation skill
Escalate to writing-documentation when:
- No README.md exists (cannot update what doesn't exist)
- README needs complete rewrite (changes exceed 50% of document)
- User requests documentation beyond just README
- README lacks standard structure and needs restructuring

### From writing-documentation skill
After writing-documentation creates a README:
- This skill takes over for ongoing maintenance
- Preserve the style and structure writing-documentation established
- Apply minimal, targeted updates only

### Decision Matrix

| Scenario | Use This Skill | Use writing-documentation |
|----------|----------------|---------------------------|
| Update existing section | ✓ | |
| Add new dependency to README | ✓ | |
| Add environment variable docs | ✓ | |
| Fix outdated instructions | ✓ | |
| Check if README current | ✓ | |
| No README exists | | ✓ |
| Complete README rewrite | | ✓ |
| README + other docs needed | | ✓ |

## README Section Taxonomy

| Section | Update Triggers |
|---------|-----------------|
| **Title/Badges** | Version bumps, CI status changes, new integrations |
| **Description** | Major feature additions, project scope changes |
| **Features** | New capabilities added, features deprecated |
| **Prerequisites** | Runtime version changes, new system requirements |
| **Installation** | New dependencies, setup steps change |
| **Configuration** | New env vars, config file changes |
| **Usage** | API changes, new examples needed |
| **Development** | Dev tooling changes, new scripts |
| **Testing** | Test framework changes, new test commands |
| **Deployment** | Infrastructure changes, new deploy steps |
| **Contributing** | Process changes, new guidelines |

## Change Detection

When checking if README needs updates, first read `references/patterns.md` for language-specific regex patterns, then use these detection rules:

### Dependency Files → Installation Section
- package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod, Gemfile

### Environment Files → Configuration Section
- .env.example changes
- New `process.env.*` or `os.environ[*]` in code

### Source Structure → Multiple Sections
- New directories in src/ → may need Architecture section
- New entry points → Usage section
- New CLI commands → Usage section

### CI/CD Files → Development/Deployment
- .github/workflows/* changes
- Dockerfile, docker-compose.yml changes

## Update Methodology

### Step 1: Detect What Changed
Run the check script:
```bash
python .claude/skills/updating-readme/scripts/check-readme.py
```

Review output to identify:
- Which files changed since last README update
- Which README sections are affected
- Priority of updates needed

### Step 2: Preserve Existing Style
Before making changes, note:
- Emoji usage (or lack thereof)
- Heading hierarchy and formatting
- Voice and tone
- Any custom sections

### Step 3: Apply Minimal Updates
- Add new information without rewriting existing content
- Update version numbers and requirements inline
- Add new list items to existing lists
- Only restructure if absolutely necessary

### Step 4: Validate

After applying updates, run verification:

1. **Run audit**:
   ```bash
   python .claude/skills/updating-readme/scripts/check-readme.py
   ```

2. **Verify**:
   - All HIGH PRIORITY issues are resolved
   - No new issues introduced by your changes
   - Style consistency maintained

3. **If issues remain**, fix and re-run until clean.

## Templates for Missing Sections

When adding a section that doesn't exist, read `references/templates.md` and select the appropriate template:
- Prerequisites section
- Environment Variables section
- Testing section
- Development section
- Deployment section
- Troubleshooting section

## Suggesting vs. Applying

- **Small, obvious updates** → Apply directly
- **Structural changes** → Suggest and explain before applying
- **Ambiguous changes** → Ask user for clarification

## Examples

### Example 1: New Dependency Added

**User:** "I just added redis to my project, update the README"

**Process:**
1. Check package.json or requirements.txt for redis dependency
2. Locate Installation and Prerequisites sections
3. Add redis to prerequisites if system installation required
4. Update installation instructions if setup steps needed
5. Add Configuration section entry if REDIS_URL env var used
6. Run check-readme.py to verify no issues remain

### Example 2: New Feature Implemented

**User:** "Update README after adding the export feature"

**Process:**
1. Identify what the export feature does from code
2. Add entry to Features section
3. Add usage example if API changed
4. Update any relevant configuration docs
5. Run check-readme.py to verify

### Example 3: README Audit

**User:** "Check if my README is up to date"

**Process:**
1. Run `python .claude/skills/updating-readme/scripts/check-readme.py`
2. Report findings organized by priority
3. Offer to apply HIGH PRIORITY fixes
4. Suggest MEDIUM PRIORITY improvements
