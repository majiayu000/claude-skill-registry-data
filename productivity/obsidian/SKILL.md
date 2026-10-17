---
name: obsidian
version: 1.0.0
description: Local-first knowledge management with markdown vaults, bidirectional linking, plugin ecosystem, and flexible sync strategies
author: workspace-hub
category: productivity
type: skill
capabilities:
  - markdown_knowledge_base
  - bidirectional_linking
  - graph_visualization
  - plugin_ecosystem
  - templating_automation
  - dataview_queries
  - sync_strategies
  - backup_workflows
tools:
  - obsidian
  - obsidian-cli
  - dataview
  - templater
  - git
tags: [obsidian, knowledge-management, markdown, zettelkasten, pkm, second-brain, notes, linking, productivity]
platforms: [desktop, mobile, linux, macos, windows, ios, android]
related_skills:
  - yaml-configuration
  - git-sync-manager
  - markdown-documentation
---

# Obsidian Knowledge Management Skill

Master Obsidian for building a personal knowledge management system with markdown-based notes, bidirectional linking, powerful plugins, and flexible sync strategies. This skill covers vault organization, linking strategies, plugin ecosystem, and backup workflows.

## When to Use This Skill

### USE Obsidian when:
- Building a personal knowledge base or second brain
- Implementing Zettelkasten or evergreen note systems
- Need local-first, privacy-focused note-taking
- Want full control over your data (plain markdown files)
- Creating interlinked notes with graph visualization
- Writing with markdown and want powerful editing
- Need offline access to all your notes
- Building project documentation alongside code
- Journaling with daily notes and templates

### DON'T USE Obsidian when:
- Need real-time collaboration (use Notion, Google Docs)
- Require database-style structured data (use Notion)
- Need web-based access without sync setup
- Team-wide knowledge base with permissions (use Confluence)
- Simple note-taking without linking (use Apple Notes, Bear)
- Need built-in task management with reminders (use Todoist)

## Prerequisites

### Installation

```bash
# Download from official site
# https://obsidian.md/download

# macOS via Homebrew
brew install --cask obsidian

# Linux (AppImage)
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v1.5.3/Obsidian-1.5.3.AppImage
chmod +x Obsidian-1.5.3.AppImage
./Obsidian-1.5.3.AppImage

# Linux (Flatpak)
flatpak install flathub md.obsidian.Obsidian

# Linux (Snap)
sudo snap install obsidian --classic
```

### Create Your First Vault

```bash
# Create vault directory
mkdir -p ~/Documents/ObsidianVault

# Initialize vault structure
cd ~/Documents/ObsidianVault
mkdir -p "Daily Notes" "Templates" "Inbox" "Projects" "Areas" "Resources" "Archive"

# Create initial configuration
mkdir -p .obsidian
cat > .obsidian/app.json << 'EOF'
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "Inbox",
  "attachmentFolderPath": "Attachments",
  "showUnsupportedFiles": false,
  "defaultViewMode": "source"
}
EOF

# Create .gitignore for vault
cat > .gitignore << 'EOF'
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/data.json
.trash/
*.sync-conflict-*
EOF
```

### Verify Setup

```bash
# Check vault structure
tree -L 2 ~/Documents/ObsidianVault

# Expected output:
# ObsidianVault/
# ├── .obsidian/
# │   └── app.json
# ├── Archive/
# ├── Areas/
# ├── Daily Notes/
# ├── Inbox/
# ├── Projects/
# ├── Resources/
# └── Templates/
```

## Core Capabilities

### 1. Vault Structure and Organization

**PARA Method Structure:**
```markdown
# Vault Organization with PARA Method
#
# Projects/ - Active projects with deadlines
# Areas/    - Ongoing responsibilities
# Resources/- Reference materials
# Archive/  - Completed or inactive items

# Example folder structure:
ObsidianVault/
├── Daily Notes/           # Daily journal entries
├── Inbox/                 # Quick capture, process later
├── Projects/
│   ├── Project-Alpha/
│   │   ├── Overview.md
│   │   ├── Tasks.md
│   │   └── Meeting Notes/
│   └── Project-Beta/
├── Areas/
│   ├── Health/
│   ├── Finance/
│   ├── Career/
│   └── Learning/
├── Resources/
│   ├── Books/
│   ├── Courses/
│   ├── Articles/
│   └── Recipes/
├── Archive/
│   └── 2025-Q1/
├── Templates/
│   ├── Daily Note.md
│   ├── Meeting Note.md
│   ├── Project.md
│   └── Book Note.md
└── Attachments/
    └── images/
```

**Zettelkasten Structure:**
```markdown
# Zettelkasten-style vault
ObsidianVault/
├── 0-Inbox/               # Fleeting notes
├── 1-Literature Notes/    # Notes from sources
├── 2-Permanent Notes/     # Your own ideas
├── 3-Structure Notes/     # MOCs (Maps of Content)
├── 4-Projects/            # Project-specific notes
└── Templates/
```

**Naming Conventions:**
```markdown
# Date-based naming for daily notes
Daily Notes/2025-01-17.md

# Timestamp-based for Zettelkasten
202501171430 - Concept Name.md

# Descriptive naming for permanent notes
How to Structure a Knowledge Base.md

# Project-prefixed naming
Project-Alpha - Meeting 2025-01-17.md

# Use lowercase with hyphens for consistency
my-note-about-something.md
```

### 2. Linking and Backlinking

**Basic Linking:**
```markdown
# Internal links
[[Note Name]]
[[Note Name|Display Text]]
[[Folder/Subfolder/Note Name]]

# Link to heading
[[Note Name#Heading Name]]
[[Note Name#Heading Name|Custom Text]]

# Link to block
[[Note Name#^block-id]]

# Embed notes
![[Note Name]]
![[Note Name#Heading]]
![[image.png]]
![[document.pdf]]

# External links
[External Link](https://example.com)
```

**Block References:**
```markdown
# In source note (Source Note.md)
This is an important concept. ^important-concept

This paragraph explains something crucial about the topic.
It spans multiple lines. ^key-explanation

# In referencing note
As mentioned in [[Source Note#^important-concept]], this concept is key.

# Embed the block
![[Source Note#^important-concept]]
```

**Linking Best Practices:**
```markdown
# Note: The Power of Compound Interest.md

## Summary
Compound interest is the concept where interest earns interest over time.

## Related Concepts
- [[Time Value of Money]] - foundational concept
- [[Investment Strategies]] - practical applications
- [[Rule of 72]] - quick estimation method

## Sources
- [[Book - The Psychology of Money]]
- [[Article - Warren Buffett on Compounding]]

## Applications
See [[Personal Finance MOC#Investment Strategies]] for implementation.

## Tags
#finance #investing #concepts
```

**Alias Usage:**
```yaml
---
aliases: [PKM, Knowledge Management, KM]
---

# Personal Knowledge Management

This note can now be linked via:
- [[Personal Knowledge Management]]
- [[PKM]]
- [[Knowledge Management]]
```

### 3. Tags and Properties (Frontmatter)

**YAML Frontmatter:**
```yaml
---
title: Complete Guide to Obsidian
date: 2025-01-17
updated: 2025-01-17
type: reference
status: active
tags:
  - obsidian
  - knowledge-management
  - productivity
author: Your Name
rating: 5
source: https://obsidian.md
related:
  - "[[Markdown Basics]]"
  - "[[Note-Taking Methods]]"
cssclass: wide-page
---

# Complete Guide to Obsidian

Content starts here...
```

**Common Property Patterns:**
```yaml
# For book notes
---
title: "Book Title"
author: "Author Name"
type: book
status: reading  # reading, completed, abandoned
started: 2025-01-01
finished:
rating:
genre: [non-fiction, productivity]
---

# For meeting notes
---
title: Weekly Team Sync
type: meeting
date: 2025-01-17
attendees:
  - Alice
  - Bob
  - Charlie
project: "[[Project Alpha]]"
action-items: true
---

# For project notes
---
title: Project Alpha Overview
type: project
status: active  # planning, active, on-hold, completed
start-date: 2025-01-01
due-date: 2025-03-31
priority: high
stakeholders:
  - Team Lead
  - Product Manager
---
```

**Tag Hierarchies:**
```markdown
# Use nested tags for organization
#status/active
#status/completed
#status/on-hold

#type/note
#type/literature
#type/project

#area/health
#area/finance
#area/career

#source/book
#source/article
#source/podcast
#source/video

# In a note:
#project/alpha #status/active #priority/high
```

### 4. Templates

**Daily Note Template:**
```markdown
---
date: {{date}}
type: daily
tags:
  - daily-note
---

# {{date:dddd, MMMM D, YYYY}}

## Morning Review
- [ ] Review calendar
- [ ] Check priorities
- [ ] Set daily intention

## Today's Focus
> What is the ONE thing I can do today that will make everything else easier?

1.

## Tasks
### Must Do
- [ ]

### Should Do
- [ ]

### Could Do
- [ ]

## Notes & Ideas


## Meetings
```dataview
TABLE WITHOUT ID
  file.link as "Meeting",
  attendees as "Attendees"
FROM #meeting
WHERE date = date("{{date:YYYY-MM-DD}}")
```

## Journal


## Evening Review
- What went well today?
- What could be improved?
- What did I learn?

---
**Links:** [[{{date:YYYY-MM-DD|yesterday(-1)}}]] | [[{{date:YYYY-MM-DD|tomorrow(+1)}}]]
```

**Meeting Note Template:**
```markdown
---
title: {{title}}
type: meeting
date: {{date:YYYY-MM-DD}}
time: {{time:HH:mm}}
attendees:
  -
project:
tags:
  - meeting
---

# {{title}}

## Attendees
-

## Agenda
1.

## Discussion Notes


## Decisions Made


## Action Items
- [ ] @Person: Task - Due:

## Follow-up
- Next meeting:
- Related:

---
**Created:** {{date:YYYY-MM-DD HH:mm}}
```

**Project Template:**
```markdown
---
title: {{title}}
type: project
status: planning
start-date: {{date:YYYY-MM-DD}}
due-date:
priority: medium
tags:
  - project
---

# {{title}}

## Overview
**Goal:**
**Success Criteria:**

## Status
```dataview
TABLE WITHOUT ID
  status as "Status",
  due-date as "Due Date",
  priority as "Priority"
WHERE file.name = this.file.name
```

## Key Resources
-

## Milestones
- [ ] Milestone 1 -
- [ ] Milestone 2 -
- [ ] Milestone 3 -

## Tasks
### In Progress
```dataview
TASK
FROM "Projects/{{title}}"
WHERE !completed AND contains(text, "WIP")
```

### Pending
```dataview
TASK
FROM "Projects/{{title}}"
WHERE !completed AND !contains(text, "WIP")
```

## Notes


## Related
- [[Project MOC]]

---
**Created:** {{date:YYYY-MM-DD}}
```

**Book Note Template:**
```markdown
---
title: "{{title}}"
author:
type: book
status: reading
started: {{date:YYYY-MM-DD}}
finished:
rating:
genre: []
isbn:
tags:
  - book
  - literature-note
---

# {{title}}

## Book Info
- **Author:**
- **Published:**
- **Pages:**
- **Genre:**

## Why I Read This


## Summary (3 sentences)


## Key Ideas
1.

## Favorite Quotes
> Quote here (p. X)

## Chapter Notes

### Chapter 1:


## How This Applies to My Life


## Related Books
- [[]]

## Action Items
- [ ]

---
**Rating:** /5
**Would Recommend To:**
```

### 5. Dataview Plugin

**Installation:**
```markdown
1. Settings > Community plugins > Turn off Safe mode
2. Browse community plugins > Search "Dataview"
3. Install and Enable
4. Settings > Dataview > Enable JavaScript Queries (optional)
```

**Basic Queries:**
```markdown
## List all notes tagged with #project
```dataview
LIST
FROM #project
```

## Table of books with ratings
```dataview
TABLE author, rating, status
FROM #book
SORT rating DESC
```

## Tasks due this week
```dataview
TASK
FROM "Projects"
WHERE due >= date(today) AND due <= date(today) + dur(7 days)
SORT due ASC
```

## Recent notes (last 7 days)
```dataview
TABLE file.ctime as "Created", file.mtime as "Modified"
FROM ""
WHERE file.ctime >= date(today) - dur(7 days)
SORT file.ctime DESC
LIMIT 10
```
```

**Advanced Dataview Queries:**
```markdown
## Project Status Dashboard
```dataview
TABLE WITHOUT ID
  file.link as "Project",
  status as "Status",
  priority as "Priority",
  due-date as "Due Date",
  (date(due-date) - date(today)).days as "Days Left"
FROM #project
WHERE status != "completed"
SORT priority ASC, due-date ASC
```

## Reading Progress
```dataview
TABLE WITHOUT ID
  file.link as "Book",
  author as "Author",
  status as "Status",
  rating as "Rating"
FROM #book
WHERE status = "reading" OR status = "completed"
SORT status ASC, rating DESC
```

## Notes by Area (grouped)
```dataview
TABLE WITHOUT ID
  file.link as "Note",
  file.mtime as "Last Modified"
FROM "Areas"
GROUP BY file.folder
SORT file.mtime DESC
```

## Meeting Action Items
```dataview
TASK
FROM #meeting
WHERE !completed AND contains(text, "@")
GROUP BY file.link
SORT file.ctime DESC
```

## Weekly Review - Notes Created
```dataview
TABLE WITHOUT ID
  file.link as "Note",
  file.ctime as "Created"
FROM ""
WHERE file.ctime >= date(today) - dur(7 days)
  AND !contains(file.path, "Templates")
SORT file.ctime DESC
```

## Orphan Notes (no backlinks)
```dataview
LIST
FROM ""
WHERE length(file.inlinks) = 0
  AND length(file.outlinks) = 0
  AND !contains(file.path, "Templates")
  AND !contains(file.path, "Archive")
LIMIT 20
```
```

**DataviewJS Examples:**
```javascript
// Custom table with calculated fields
```dataviewjs
const pages = dv.pages('#project')
  .where(p => p.status !== 'completed')
  .sort(p => p['due-date'], 'asc');

dv.table(
  ["Project", "Status", "Days Until Due", "Progress"],
  pages.map(p => [
    p.file.link,
    p.status,
    p['due-date'] ?
      Math.round((new Date(p['due-date']) - new Date()) / (1000 * 60 * 60 * 24)) :
      'No due date',
    `${p.progress || 0}%`
  ])
);
```

// Task summary by project
```dataviewjs
const projects = dv.pages('#project');

for (let project of projects) {
  const tasks = project.file.tasks;
  const completed = tasks.filter(t => t.completed).length;
  const total = tasks.length;

  if (total > 0) {
    dv.paragraph(`**${project.file.name}**: ${completed}/${total} tasks (${Math.round(completed/total*100)}%)`);
  }
}
```
```

### 6. Templater Plugin

**Installation:**
```markdown
1. Community plugins > Search "Templater"
2. Install and Enable
3. Settings > Templater > Template folder location: "Templates"
4. Enable "Trigger Templater on new file creation"
```

**Templater Syntax:**
```markdown
# Basic Templater commands

## Date/Time
<% tp.date.now("YYYY-MM-DD") %>
<% tp.date.now("dddd, MMMM D, YYYY") %>
<% tp.date.now("HH:mm") %>
<% tp.date.yesterday("YYYY-MM-DD") %>
<% tp.date.tomorrow("YYYY-MM-DD") %>

## File Information
<% tp.file.title %>
<% tp.file.path() %>
<% tp.file.folder() %>
<% tp.file.creation_date("YYYY-MM-DD") %>

## User Input
<% tp.system.prompt("Enter project name") %>
<% tp.system.suggester(["Option 1", "Option 2"], ["value1", "value2"]) %>

## Cursor Placement
<% tp.file.cursor() %>
<% tp.file.cursor(1) %>  <!-- Named cursor -->

## File Operations
<% tp.file.rename("New Name") %>
<% tp.file.move("Folder/Subfolder") %>
```

**Advanced Templater Template:**
```markdown
<%*
// Prompt for project details
const projectName = await tp.system.prompt("Project Name");
const priority = await tp.system.suggester(
  ["High", "Medium", "Low"],
  ["high", "medium", "low"],
  false,
  "Select Priority"
);
const dueDate = await tp.system.prompt("Due Date (YYYY-MM-DD)",
  tp.date.now("YYYY-MM-DD", 30));

// Rename file
await tp.file.rename(projectName);

// Move to Projects folder
await tp.file.move(`Projects/${projectName}`);
-%>
---
title: <% projectName %>
type: project
status: planning
priority: <% priority %>
start-date: <% tp.date.now("YYYY-MM-DD") %>
due-date: <% dueDate %>
tags:
  - project
---

# <% projectName %>

## Overview
<% tp.file.cursor() %>

## Goals
-

## Milestones
- [ ]

## Resources
-

---
**Created:** <% tp.date.now("YYYY-MM-DD HH:mm") %>
```

**Daily Note with Templater:**
```markdown
<%*
const yesterday = tp.date.now("YYYY-MM-DD", -1);
const tomorrow = tp.date.now("YYYY-MM-DD", 1);
const dayName = tp.date.now("dddd");
const weekNumber = tp.date.now("W");
-%>
---
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% weekNumber %>
type: daily
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

## Morning Routine
- [ ] Review yesterday's notes
- [ ] Check calendar
- [ ] Set top 3 priorities

## Top 3 Priorities
1. <% tp.file.cursor(1) %>
2.
3.

## Schedule
| Time | Activity |
|------|----------|
| 09:00 | |
| 10:00 | |
| 11:00 | |
| 12:00 | Lunch |
| 13:00 | |
| 14:00 | |
| 15:00 | |
| 16:00 | |
| 17:00 | |

## Notes


## Tasks Completed
-

## Tomorrow's Preview
-

---
[[<% yesterday %>]] | [[<% tomorrow %>]]
```

### 7. Sync Strategies

**Git-Based Sync:**
```bash
#!/bin/bash
# sync-vault.sh - Git-based vault sync

VAULT_PATH="$HOME/Documents/ObsidianVault"
cd "$VAULT_PATH" || exit 1

# Initialize if not a git repo
if [ ! -d .git ]; then
    git init
    git remote add origin git@github.com:username/obsidian-vault.git
fi

# Pull latest changes
echo "Pulling latest changes..."
git pull --rebase origin main 2>/dev/null || true

# Add all changes
git add -A

# Commit if there are changes
if ! git diff --cached --quiet; then
    COMMIT_MSG="Vault sync: $(date '+%Y-%m-%d %H:%M')"
    git commit -m "$COMMIT_MSG"

    # Push changes
    echo "Pushing changes..."
    git push origin main
    echo "Sync complete!"
else
    echo "No changes to sync."
fi
```

**Automated Git Sync with Cron:**
```bash
# Add to crontab (crontab -e)
# Sync every 30 minutes
*/30 * * * * /path/to/sync-vault.sh >> /var/log/obsidian-sync.log 2>&1

# Or use launchd on macOS
# ~/Library/LaunchAgents/com.obsidian.sync.plist
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.obsidian.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/username/scripts/sync-vault.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>/tmp/obsidian-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/obsidian-sync-error.log</string>
</dict>
</plist>
```

**Obsidian Sync (Official):**
```markdown
# Obsidian Sync - Official Solution
# Pros: Seamless, end-to-end encrypted, version history
# Cons: Paid subscription ($8/month or $96/year)

Setup:
1. Settings > Sync > Set up Obsidian Sync
2. Log in with Obsidian account
3. Create or connect to remote vault
4. Select folders/files to sync

Best Practices:
- Exclude large binary files
- Use selective sync for large vaults
- Enable "Sync all other types" for attachments
```

**iCloud Sync (macOS/iOS):**
```bash
# Move vault to iCloud Drive
VAULT_NAME="ObsidianVault"
mv ~/Documents/$VAULT_NAME ~/Library/Mobile\ Documents/com~apple~CloudDocs/$VAULT_NAME

# Create symlink for easy access
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/$VAULT_NAME ~/Documents/$VAULT_NAME

# On iOS: Open Obsidian > Create new vault > Store in iCloud
```

**Syncthing Setup:**
```bash
# Install Syncthing
brew install syncthing  # macOS
sudo apt install syncthing  # Ubuntu

# Start Syncthing
syncthing

# Access web GUI at http://localhost:8384
# Add folder: ~/Documents/ObsidianVault
# Share with other devices

# Syncthing ignore patterns (.stignore)
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash
*.sync-conflict-*
```

### 8. Backup Strategies

**Automated Backup Script:**
```bash
#!/bin/bash
# backup-vault.sh - Comprehensive vault backup

VAULT_PATH="$HOME/Documents/ObsidianVault"
BACKUP_DIR="$HOME/Backups/Obsidian"
DATE=$(date +%Y-%m-%d_%H%M%S)
BACKUP_NAME="obsidian-backup-$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create compressed backup
echo "Creating backup: $BACKUP_NAME.tar.gz"
tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
    -C "$(dirname "$VAULT_PATH")" \
    "$(basename "$VAULT_PATH")"

# Keep only last 30 backups
cd "$BACKUP_DIR"
ls -t obsidian-backup-*.tar.gz | tail -n +31 | xargs -r rm

# Calculate backup size
SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -f1)
echo "Backup complete: $SIZE"

# Optional: Upload to cloud storage
# rclone copy "$BACKUP_DIR/$BACKUP_NAME.tar.gz" remote:backups/obsidian/

# Optional: Verify backup integrity
tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" > /dev/null 2>&1 && \
    echo "Backup verified successfully" || \
    echo "WARNING: Backup verification failed!"
```

**Cloud Backup with rclone:**
```bash
#!/bin/bash
# cloud-backup.sh - Backup to multiple cloud providers

VAULT_PATH="$HOME/Documents/ObsidianVault"
DATE=$(date +%Y-%m-%d)

# Sync to Google Drive
rclone sync "$VAULT_PATH" gdrive:Backups/Obsidian \
    --exclude ".obsidian/workspace*.json" \
    --exclude ".trash/**"

# Sync to Dropbox
rclone sync "$VAULT_PATH" dropbox:Backups/Obsidian \
    --exclude ".obsidian/workspace*.json" \
    --exclude ".trash/**"

# Create versioned snapshot on S3
rclone copy "$VAULT_PATH" s3:bucket-name/obsidian/$DATE \
    --exclude ".obsidian/workspace*.json" \
    --exclude ".trash/**"

echo "Cloud backup complete: $DATE"
```

**Backup Verification:**
```bash
#!/bin/bash
# verify-backup.sh - Test backup restoration

BACKUP_FILE="$1"
TEST_DIR="/tmp/obsidian-backup-test"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: verify-backup.sh <backup-file.tar.gz>"
    exit 1
fi

# Clean test directory
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Extract backup
echo "Extracting backup..."
tar -xzf "$BACKUP_FILE" -C "$TEST_DIR"

# Verify contents
echo "Verifying contents..."
ORIGINAL_COUNT=$(find "$HOME/Documents/ObsidianVault" -type f -name "*.md" | wc -l)
BACKUP_COUNT=$(find "$TEST_DIR" -type f -name "*.md" | wc -l)

echo "Original notes: $ORIGINAL_COUNT"
echo "Backup notes: $BACKUP_COUNT"

if [ "$ORIGINAL_COUNT" -eq "$BACKUP_COUNT" ]; then
    echo "Verification PASSED"
else
    echo "WARNING: Note count mismatch!"
fi

# Cleanup
rm -rf "$TEST_DIR"
```

## Integration Examples

### Integration with Git Repositories

```bash
#!/bin/bash
# Link project documentation to code repository

PROJECT_NAME="my-project"
CODE_REPO="$HOME/code/$PROJECT_NAME"
VAULT_PATH="$HOME/Documents/ObsidianVault"

# Create project folder in vault
mkdir -p "$VAULT_PATH/Projects/$PROJECT_NAME"

# Symlink docs folder from code repo
ln -s "$CODE_REPO/docs" "$VAULT_PATH/Projects/$PROJECT_NAME/Docs"

# Create project overview note
cat > "$VAULT_PATH/Projects/$PROJECT_NAME/Overview.md" << EOF
---
title: $PROJECT_NAME
type: project
repo: $CODE_REPO
status: active
---

# $PROJECT_NAME

## Repository
\`$CODE_REPO\`

## Documentation
- [[Docs/README|README]]
- [[Docs/API|API Reference]]

## Notes
-

## Tasks
- [ ]
EOF
```

### Integration with Todoist

```python
#!/usr/bin/env python3
"""sync_todoist_obsidian.py - Sync Todoist tasks to Obsidian"""

import os
import json
from datetime import datetime
from todoist_api_python import TodoistAPI

TODOIST_API_KEY = os.environ.get("TODOIST_API_KEY")
VAULT_PATH = os.path.expanduser("~/Documents/ObsidianVault")

def sync_todoist_to_obsidian():
    api = TodoistAPI(TODOIST_API_KEY)

    # Get all tasks due today
    tasks = api.get_tasks(filter="today | overdue")

    # Generate markdown
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
date: {today}
source: todoist
type: task-sync
---

# Todoist Tasks - {today}

## Due Today
"""

    for task in tasks:
        checkbox = "[ ]" if not task.is_completed else "[x]"
        due_str = task.due.string if task.due else "No due date"
        content += f"- {checkbox} {task.content} (Due: {due_str})\n"

    # Write to vault
    output_path = f"{VAULT_PATH}/Inbox/Todoist-{today}.md"
    with open(output_path, "w") as f:
        f.write(content)

    print(f"Synced {len(tasks)} tasks to {output_path}")

if __name__ == "__main__":
    sync_todoist_to_obsidian()
```

### Integration with Notion Export

```python
#!/usr/bin/env python3
"""notion_to_obsidian.py - Export Notion pages to Obsidian"""

import os
import re
from notion_client import Client

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
VAULT_PATH = os.path.expanduser("~/Documents/ObsidianVault")

def notion_to_markdown(block):
    """Convert Notion block to markdown"""
    block_type = block["type"]

    if block_type == "paragraph":
        text = extract_text(block["paragraph"]["rich_text"])
        return f"{text}\n\n"
    elif block_type == "heading_1":
        text = extract_text(block["heading_1"]["rich_text"])
        return f"# {text}\n\n"
    elif block_type == "heading_2":
        text = extract_text(block["heading_2"]["rich_text"])
        return f"## {text}\n\n"
    elif block_type == "heading_3":
        text = extract_text(block["heading_3"]["rich_text"])
        return f"### {text}\n\n"
    elif block_type == "bulleted_list_item":
        text = extract_text(block["bulleted_list_item"]["rich_text"])
        return f"- {text}\n"
    elif block_type == "numbered_list_item":
        text = extract_text(block["numbered_list_item"]["rich_text"])
        return f"1. {text}\n"
    elif block_type == "to_do":
        text = extract_text(block["to_do"]["rich_text"])
        checked = "x" if block["to_do"]["checked"] else " "
        return f"- [{checked}] {text}\n"
    elif block_type == "code":
        text = extract_text(block["code"]["rich_text"])
        language = block["code"]["language"]
        return f"```{language}\n{text}\n```\n\n"

    return ""

def extract_text(rich_text):
    """Extract plain text from Notion rich text"""
    return "".join([t["plain_text"] for t in rich_text])

def export_page(notion, page_id, output_path):
    """Export a Notion page to markdown file"""
    # Get page properties
    page = notion.pages.retrieve(page_id)
    title = extract_text(page["properties"]["title"]["title"])

    # Get page content
    blocks = notion.blocks.children.list(page_id)

    content = f"""---
title: {title}
source: notion
imported: {datetime.now().strftime("%Y-%m-%d")}
---

# {title}

"""

    for block in blocks["results"]:
        content += notion_to_markdown(block)

    # Write to vault
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    filepath = f"{output_path}/{safe_title}.md"

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Exported: {title}")

# Usage
notion = Client(auth=NOTION_API_KEY)
export_page(notion, "page-id-here", f"{VAULT_PATH}/Imports/Notion")
```

## Best Practices

### 1. Note Naming and Organization

```markdown
# Use consistent naming conventions
- lowercase-with-hyphens.md (recommended)
- Title Case Note Name.md (acceptable)
- Avoid: spaces_underscores_MixedCase.md

# Date prefix for temporal notes
2025-01-17 Daily Note.md
2025-01-17 Meeting with Team.md

# Unique identifier prefix for Zettelkasten
202501171430 Concept Name.md

# Project prefix for project notes
Project-Alpha Meeting Notes.md
Project-Alpha Requirements.md
```

### 2. Linking Strategy

```markdown
# Link generously but meaningfully
- Link when concepts are related
- Don't link common words
- Use descriptive link text

# Create hub notes (MOCs - Maps of Content)
# These serve as entry points to topics

# Example MOC: Programming MOC.md
# [[Python Basics]]
# [[JavaScript Fundamentals]]
# [[Data Structures]]

# Use unlinked mentions to discover connections
# Settings > Core plugins > Backlinks > Show unlinked mentions
```

### 3. Daily Notes Workflow

```markdown
# Morning routine
1. Create daily note from template
2. Review yesterday's note
3. Set top 3 priorities
4. Check calendar and add scheduled items

# Throughout the day
- Capture thoughts in daily note
- Link to relevant notes
- Create new notes for substantial ideas

# Evening routine
- Review completed tasks
- Process inbox items
- Reflect on the day
- Preview tomorrow
```

### 4. Progressive Summarization

```markdown
# Layer 0: Original content (source)
# Layer 1: Bold key passages
# Layer 2: Highlight within bold
# Layer 3: Executive summary at top

Example:
---
## Summary
Key insight in 2-3 sentences.

## Notes
The original passage contains **important information that stands out**.
Within that, ==the most crucial point== is highlighted.
```

### 5. Maintenance Routines

```markdown
# Weekly Review
- [ ] Process inbox notes
- [ ] Review orphan notes
- [ ] Update project statuses
- [ ] Clean up dead links

# Monthly Review
- [ ] Archive completed projects
- [ ] Review and update MOCs
- [ ] Backup vault
- [ ] Update plugins

# Use Dataview for maintenance
```dataview
LIST
FROM ""
WHERE file.mtime < date(today) - dur(90 days)
  AND !contains(file.path, "Archive")
  AND !contains(file.path, "Templates")
LIMIT 20
```
```

## Troubleshooting

### Common Issues

**Issue: Slow performance with large vault**
```markdown
Solutions:
1. Disable unused plugins
2. Reduce graph view nodes: Settings > Graph > Filters
3. Exclude folders from search: Settings > Files & Links > Excluded files
4. Use lazy loading for Dataview
5. Split into multiple vaults if > 10,000 notes
```

**Issue: Sync conflicts**
```markdown
Solutions:
1. Close Obsidian on all devices before syncing
2. Use .sync-conflict-* in .gitignore
3. For Git sync: pull before editing
4. For iCloud: wait for sync indicator
5. Use Obsidian Sync for best experience
```

**Issue: Broken links after moving notes**
```markdown
Solutions:
1. Use Obsidian's built-in move (F2 or right-click > Move)
2. Enable "Automatically update internal links"
3. Use Consistent Attachments and Links plugin
4. Run "Find and replace in all files" for bulk fixes
```

**Issue: Images not displaying**
```markdown
Solutions:
1. Check attachment folder setting
2. Use relative paths: ![[image.png]]
3. Verify file exists in vault
4. Check file extension (case-sensitive on Linux)
5. For external images: ensure URL is accessible
```

**Issue: Plugin conflicts**
```markdown
Solutions:
1. Disable all plugins, enable one by one
2. Check plugin compatibility in settings
3. Clear plugin cache: .obsidian/plugins/*/
4. Update all plugins to latest versions
5. Check plugin GitHub for known issues
```

### Plugin Recommendations

```markdown
## Essential Plugins
- Dataview - Query and display data
- Templater - Advanced templating
- Calendar - Visual date navigation
- Periodic Notes - Daily/weekly/monthly notes
- Quick Switcher++ - Enhanced note switching

## Productivity
- Tasks - Task management
- Kanban - Visual task boards
- Day Planner - Schedule visualization
- Reminder - Task reminders

## Writing
- Linter - Markdown formatting
- Natural Language Dates - "tomorrow", "next week"
- Paste URL into selection - Smart link pasting
- Auto Link Title - Fetch titles for URLs

## Organization
- Tag Wrangler - Manage tags
- Folder Note - Folder as note
- Recent Files - Quick access to recent notes
- Starred - Bookmark important notes
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-17 | Initial release with comprehensive Obsidian patterns |

## Resources

- [Obsidian Official](https://obsidian.md/)
- [Obsidian Help](https://help.obsidian.md/)
- [Obsidian Forum](https://forum.obsidian.md/)
- [Obsidian Hub](https://publish.obsidian.md/hub)
- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- [Templater Documentation](https://silentvoid13.github.io/Templater/)
- [Obsidian Plugin Stats](https://obsidian-plugin-stats.vercel.app/)

---

*This skill enables building a powerful, privacy-first knowledge management system with Obsidian's markdown-based approach, bidirectional linking, and extensible plugin ecosystem.*
