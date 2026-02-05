---
name: init-rules
description: Initialize Rails coding conventions for a project by detecting dependencies and copying matching rules with examples to .claude/rules/hustler-rails/. Use when setting up Rails conventions for a new project or updating existing rules. Trigger with phrases like "initialize rails rules", "setup rails conventions", "init hustler-rails".
---

## Step 1: Check for Existing Rules

Check if `.claude/rules/hustler-rails/` has files:

```bash
ls .claude/rules/hustler-rails/ 2>/dev/null | wc -l
```

If count > 0, use AskUserQuestion tool:

```json
{
  "questions": [
    {
      "question": "hustler-rails rules already exist. How should I proceed?",
      "header": "Existing rules",
      "multiSelect": false,
      "options": [
        {
          "label": "Backup and recreate",
          "description": "Renames existing to .backup-[timestamp]"
        },
        {
          "label": "Merge new files",
          "description": "Keep existing, add new only"
        },
        { "label": "Cancel", "description": "Exit without changes" }
      ]
    }
  ]
}
```

Handle response:

- **Backup and recreate**: `mv .claude/rules/hustler-rails .claude/rules/hustler-rails.backup-$(date +%Y%m%d-%H%M%S)`
- **Merge new files**: Proceed to Step 2 (script won't overwrite)
- **Cancel**: Exit

## Step 2: Run Init Script

Execute:

```bash
ruby {baseDir}/scripts/init-rules.rb {baseDir}
```

## Step 3: Show Results

Present the script's output to the user. If errors occurred, explain them.
