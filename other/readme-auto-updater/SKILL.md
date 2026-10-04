---
name: readme-auto-updater
description: >
  Automatically generates and updates README.md files for Next.js projects by scanning
  project structure, APIs, dependencies, and git history. This skill should be used when:
  (1) A new module or feature is completed, (2) Significant changes are made to the codebase,
  (3) The user requests README generation or update, (4) During CI/CD pipeline for documentation
  sync, (5) When project structure changes. Integrates with jkkn-terminologies skill to enforce
  JKKN-compliant language in all generated documentation. Automatically triggers when user
  mentions 'readme', 'documentation update', 'module complete', or requests project documentation.
---

# README Auto-Updater Skill

This skill automatically generates and maintains README.md files for Next.js projects by
analyzing the codebase and intelligently merging updates with existing documentation.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  README Auto-Updater                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Triggers           Scanners              Output             │
│  ─────────          ────────              ──────             │
│  • Manual           • Structure    ───►   Metadata    ───►  │
│  • Git Hook         • APIs                JSON               │
│  • File Watch       • Dependencies                           │
│  • CI/CD            • Changes                     ▼          │
│                                              ┌────────────┐  │
│                                              │  Claude    │  │
│                     JKKN Terms    ◄────────  │  Smart     │  │
│                     Enforcement              │  Merge     │  │
│                          │                   └────────────┘  │
│                          ▼                         │         │
│                    README.md  ◄─────────────────────         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Dependencies

This skill depends on:
- **jkkn-terminologies**: For enforcing JKKN-compliant terminology in generated content

## Workflows

### Workflow 1: Full README Generation

Generate a complete README from scratch or major update.

**Steps:**

1. **Run all scanners** to collect project metadata:
   ```bash
   python scripts/run_scanners.py [project_path] --output readme-metadata.json
   ```

2. **Read the generated metadata:**
   ```bash
   # Output: readme-metadata.json
   ```

3. **Read the template reference:**
   ```
   references/readme-template.md
   ```

4. **Generate README content** using the template structure:
   - Populate all sections from metadata
   - Generate AI descriptions for modules and APIs
   - Apply JKKN terminology throughout
   - Format tables and code blocks properly

5. **Validate terminology** using jkkn-terminologies skill:
   - Scan generated content for prohibited terms
   - Replace any traditional terms with JKKN equivalents

6. **Write the README.md** to project root

### Workflow 2: Incremental Update

Update specific sections based on changes.

**Steps:**

1. **Run targeted scanner** based on change type:
   - Structure changes → `python scripts/scan_structure.py`
   - API changes → `python scripts/scan_apis.py`
   - Dependency changes → `python scripts/scan_dependencies.py`
   - Git activity → `python scripts/scan_changes.py`

2. **Read existing README.md**

3. **Identify sections to update** based on scanner output

4. **Smart merge:**
   - Preserve custom content (manually written sections)
   - Update auto-generated sections
   - Maintain document structure

5. **Apply JKKN terminology validation**

6. **Write updated README.md**

### Workflow 3: Module Completion Update

When a module is marked complete.

**Steps:**

1. **Scan structure** to detect module status:
   ```bash
   python scripts/scan_structure.py [project_path]
   ```

2. **Update Modules table** in README:
   - Change status icon from 🔄 to ✅
   - Update description if needed
   - Update progress counts

3. **Add to Recent Changes section:**
   - Add entry for module completion
   - Include date and brief description

4. **Validate and write**

### Workflow 4: Quick Scan (File Watcher Mode)

Lightweight scan for real-time updates.

**Steps:**

1. **Detect changed files** from watcher event

2. **Run minimal scan** (structure only)

3. **Check if README sections need update:**
   - New files in app/ → Update Modules
   - New components → Update Components count
   - New API routes → Update API Reference

4. **Queue update** (debounce multiple changes)

5. **Apply update when stable**

## Scanner Scripts

### run_scanners.py (Main Entry)
Orchestrates all scanners and generates combined metadata.

```bash
# Full scan
python scripts/run_scanners.py ./my-project --output readme-metadata.json

# Output: readme-metadata.json with all project data
```

### scan_structure.py
Analyzes project folder structure, modules, and components.

**Extracts:**
- Directory tree
- App Router modules with completion status
- Component inventory
- File organization

### scan_apis.py
Extracts API routes, server actions, and type definitions.

**Extracts:**
- Next.js API routes (app/api/*)
- Server actions with 'use server'
- Service layer functions
- TypeScript interfaces

### scan_dependencies.py
Analyzes package.json for tech stack and dependencies.

**Extracts:**
- Project metadata (name, version)
- Tech stack identification
- Categorized dependencies
- Available npm scripts

### scan_changes.py
Analyzes git history for changelog generation.

**Extracts:**
- Recent commits categorized by type
- Modified files
- Feature additions
- Bug fixes
- Contributors

## JKKN Terminology Integration

All generated README content MUST use JKKN terminology.

### Pre-Generation Rules

Before writing any content, apply these transformations:

| If module/file contains | Generate description using |
|------------------------|---------------------------|
| student, user (person) | learner |
| teacher, admin, staff | learning facilitator, team member |
| classroom, room | learning studio |
| course, syllabus | learning pathway |
| grade, score | learning assessment |
| pass/fail | achieved/did not meet outcomes |

### Post-Generation Validation

After generating content:

1. Run JKKN terminology validator on generated text
2. Replace any violations automatically
3. Log any edge cases for manual review

### Example Transformations

```
❌ "Student management module"
✅ "Learner management module"

❌ "Teacher dashboard for grading"
✅ "Learning facilitator dashboard for assessments"

❌ "Classroom scheduling system"
✅ "Learning studio scheduling system"
```

## Metadata JSON Schema

The `readme-metadata.json` file follows this structure:

```json
{
  "generated_at": "ISO timestamp",
  "project": {
    "name": "string",
    "version": "string",
    "description": "string",
    "root": "path"
  },
  "structure": {
    "has_src": "boolean",
    "has_app_router": "boolean",
    "tree_string": "ASCII tree"
  },
  "modules": [
    {
      "name": "string",
      "status": "complete|in_progress|planned",
      "status_icon": "emoji",
      "pages": "number",
      "components": "number",
      "description": "string"
    }
  ],
  "apis": {
    "routes": [...],
    "server_actions": [...],
    "services": [...],
    "types": [...]
  },
  "tech_stack": [...],
  "scripts": [...],
  "dependencies": {...},
  "changes": {
    "branch": {...},
    "recent_commits": [...],
    "changelog": [...]
  },
  "summary": {...}
}
```

## Trigger Integration

### Git Hook (post-commit)

```bash
#!/bin/bash
# .git/hooks/post-commit

# Run quick scan
python .claude/skills/readme-auto-updater/scripts/scan_structure.py . > /tmp/structure.json

# Check if significant changes
if grep -q '"status": "complete"' /tmp/structure.json; then
  echo "Module completed - README update recommended"
  # Trigger Claude Code for smart merge
fi
```

### GitHub Action

```yaml
name: Update README

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run scanners
        run: python .claude/skills/readme-auto-updater/scripts/run_scanners.py

      - name: Update README
        # Claude Code action or manual commit
        run: |
          if [ -f readme-metadata.json ]; then
            echo "Metadata generated, README update available"
          fi
```

### Claude Code Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "echo 'Consider running /readme-update if module changes detected'"
      }
    ]
  }
}
```

## Usage Examples

### Generate New README

```
User: Generate a README for this project

Claude:
1. Runs: python scripts/run_scanners.py .
2. Reads: readme-metadata.json
3. Reads: references/readme-template.md
4. Generates README content following template
5. Applies JKKN terminology
6. Writes: README.md
```

### Update After Module Completion

```
User: The auth module is now complete, update the README

Claude:
1. Runs: python scripts/scan_structure.py .
2. Reads current README.md
3. Updates Modules table: auth → ✅ Complete
4. Adds to Recent Changes
5. Validates JKKN terminology
6. Writes updated README.md
```

### Sync Documentation

```
User: Sync the README with current project state

Claude:
1. Runs all scanners
2. Compares metadata with existing README
3. Identifies outdated sections
4. Smart merges updates
5. Preserves custom content
6. Writes updated README.md
```

## Best Practices

1. **Run full scan** for initial README generation
2. **Run incremental scans** for routine updates
3. **Preserve manual sections** - don't overwrite custom content
4. **Validate terminology** before every write
5. **Review generated content** for accuracy
6. **Commit README changes** separately from code changes
