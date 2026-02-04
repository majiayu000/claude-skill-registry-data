---
name: weekly-structure
description: Automatically create weekly folder structures for Gastrohem WhatsApp conversations. This skill should be used when the user asks to create weekly folders, set up a new week, or prepare folder structure for WhatsApp documentation (e.g., "Create weekly structure", "Set up folders for next week", "Create structure for 27.10 - 02.11"). Creates Monday-Sunday folders with chat.md files in each department.
---

# Weekly Structure

## Overview

Automatically create weekly folder structures for Gastrohem WhatsApp documentation. The skill generates a complete week of daily folders (Monday through Sunday) with `chat.md` files in each, organized under department-specific weekly folders.

**Week definition:** Monday = start, Sunday = end

**Structure created:**
```
gastrohem whatsapp/{department}/{week}/
  ├── {monday}/
  │   └── chat.md
  ├── {tuesday}/
  │   └── chat.md
  ...
  └── {sunday}/
      └── chat.md
```

## When to Use This Skill

Use this skill when:
- Setting up a new week's documentation structure
- User requests "Create weekly structure" or "Set up folders for next week"
- User provides specific week range (e.g., "Create structure for 27.10 - 02.11")
- Preparing folders at the start of each week

**Default behavior:** If no week is specified, creates structure for current week (Monday-Sunday).

## Quick Start

### Creating Current Week Structure

To create folder structure for the current week (Monday-Sunday):

```bash
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh
```

Script automatically:
1. Calculates current week (Monday-Sunday)
2. Creates weekly folder in each department
3. Creates 7 daily folders (Monday through Sunday)
4. Creates `chat.md` file in each daily folder

### Creating Specific Week Structure

To create folder structure for a specific week:

```bash
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh "27.10 - 02.11"
```

**Week format:** `DD.MM - DD.MM` (e.g., "27.10 - 02.11" where 27.10 is Monday, 02.11 is Sunday)

**Important:** Week range must span Monday to Sunday (7 days).

## How It Works

### Step 1: Week Calculation

**If week provided:** Use the provided week range (e.g., "27.10 - 02.11")

**If no week provided:** Calculate current week:
- Find current day of week (1=Monday, 2=Tuesday, ..., 7=Sunday)
- Calculate Monday of current week (start)
- Calculate Sunday of current week (end)
- Format as "DD.MM - DD.MM"

### Step 2: Date Generation

Generate all 7 dates in the week:
- Parse start date from week range
- Generate dates for Monday through Sunday
- Format each as "DD.MM"

Example for week "27.10 - 02.11":
- Monday: 27.10
- Tuesday: 28.10
- Wednesday: 29.10
- Thursday: 30.10
- Friday: 31.10
- Saturday: 01.11
- Sunday: 02.11

### Step 3: Structure Creation

For each department in `gastrohem whatsapp/`:
1. Create weekly folder: `{department}/{week}/`
2. For each day (Monday-Sunday):
   - Create daily folder: `{department}/{week}/{DD.MM}/`
   - Create `chat.md` file with basic template

**Departments processed:**
- **ALL** directories in `gastrohem whatsapp/` are automatically detected and processed
- No need to manually list departments
- Script dynamically finds all department folders

### Step 4: chat.md Template

Each `chat.md` file is created with this template:

```markdown
# Chat - {DD.MM}

## Razgovori

<!-- Razgovori za ovaj dan -->

```

## Script Behavior

### Existing Folders

**Weekly folder exists:** Script continues and creates missing daily folders

**Daily folder exists:** Script skips creation, preserves existing content

**chat.md exists:** Script skips creation, preserves existing file

### Output Messages

Script provides clear feedback:
- ✅ Created items (folders, files)
- ℹ️ Already exists (skipped items)
- ⚠️ Warnings (missing departments)

### Example Output

```
=========================================
Kreiranje sedmične strukture: 21.10 - 27.10
Ponedjeljak - Nedjelja (7 dana)
=========================================

📅 Generiši datume...
Datumi za kreiranje:
   - 21.10
   - 22.10
   - 23.10
   - 24.10
   - 25.10
   - 26.10
   - 27.10

✅ Kreiran sedmični folder: administracija/21.10 - 27.10
   ✅ Dan: 21.10
      📝 Kreiran: chat.md
   ✅ Dan: 22.10
      📝 Kreiran: chat.md
   ...
   ✅ Kreirano 7 novih dana

=========================================
✅ Završeno!
=========================================
```

## Common Usage Patterns

### Setting Up Next Week

At the end of each week, prepare structure for next week:

1. Calculate next Monday's date
2. Calculate following Sunday's date
3. Run script with week range

Example (if today is Friday 25.10):
```bash
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh "28.10 - 03.11"
```

### Batch Creating Multiple Weeks

To create multiple weeks at once, run script multiple times:

```bash
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh "28.10 - 03.11"
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh "04.11 - 10.11"
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh "11.11 - 17.11"
```

### Filling Gaps

If daily folders are missing from an existing week, running the script again will create only the missing folders without affecting existing ones.

## Important Notes

- **Week definition:** Monday to Sunday (7 days)
- **Date format:** European format (DD.MM)
- **Preservation:** Existing folders and files are never overwritten
- **Auto-detection:** Script automatically detects ALL department folders in `gastrohem whatsapp/`
- **No hardcoded lists:** New departments are automatically included without script changes
- **chat.md:** Basic template created for each day

## Best Practices

1. **Weekly preparation:** Run at the start of each week to prepare structure
2. **Advance planning:** Create upcoming weeks in advance if needed
3. **Verify week range:** Ensure provided week spans Monday-Sunday
4. **Check output:** Review script output to confirm all folders created
5. **Use current week:** Omit week parameter to use current week automatically

## Resources

### scripts/create_weekly_structure.sh

Bash script that performs the weekly structure creation.

**Usage:**
```bash
# Current week
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh

# Specific week
bash .claude/skills/weekly-structure/scripts/create_weekly_structure.sh "DD.MM - DD.MM"
```

**Requirements:**
- macOS/Linux environment with bash
- Access to `gastrohem whatsapp/` directory
- Write permissions in the directory

**Exit codes:**
- 0: Success
- Non-zero: Error occurred

## Troubleshooting

### Script Not Executable

Make script executable:
```bash
chmod +x .claude/skills/weekly-structure/scripts/create_weekly_structure.sh
```

### Department Not Found

Verify department exists in `gastrohem whatsapp/` directory. Script skips non-existent departments with warning.

### Date Calculation Issues

Ensure system date command works correctly:
```bash
date +%d.%m  # Should output current date in DD.MM format
```

### Permissions

Ensure write permissions in `gastrohem whatsapp/` directory:
```bash
ls -la "gastrohem whatsapp/"
```
