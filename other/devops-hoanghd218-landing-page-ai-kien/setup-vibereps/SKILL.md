---
name: setup-vibereps
description: First-time setup for vibereps exercise tracker. Use when user wants to install, configure, or set up vibereps for the first time. Guides through exercise selection, hook configuration, and preferences.
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash
---

# Setup Vibereps

Guide users through first-time vibereps configuration.

## Setup Flow

### Step 1: Ask Exercise Preferences

Use AskUserQuestion to ask:

```
Question: "Which exercises do you want to do?"
Header: "Exercises"
MultiSelect: true
Options:
- squats: "Lower body strength, good for desk workers"
- jumping_jacks: "Cardio, gets blood flowing quickly"
- calf_raises: "Subtle, can do while standing at desk"
- standing_crunches: "Core workout, elbow to opposite knee"
- side_stretches: "Flexibility, relieves back tension"
- pushups: "Upper body, requires floor space"
```

### Step 2: Ask Trigger Preference

```
Question: "When should exercises trigger?"
Header: "Trigger"
Options:
- "After edits (Recommended)": "Exercise after Claude writes/edits code"
- "After tasks": "Exercise when Claude completes a task"
- "Manual only": "Only when you run the tracker yourself"
```

### Step 3: Configure Hook

Based on answers, add to `~/.claude/settings.json`:

**After edits:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "VIBEREPS_EXERCISES={exercises} {vibereps_dir}/exercise_tracker.py post_tool_use '{}'"
      }]
    }],
    "Notification": [{
      "hooks": [{
        "type": "command",
        "command": "{vibereps_dir}/notify_complete.py '{}'"
      }]
    }]
  }
}
```

**After tasks:**
```json
{
  "hooks": {
    "TaskComplete": [{
      "hooks": [{
        "type": "command",
        "command": "VIBEREPS_EXERCISES={exercises} {vibereps_dir}/exercise_tracker.py task_complete '{}'"
      }]
    }],
    "Notification": [{
      "hooks": [{
        "type": "command",
        "command": "{vibereps_dir}/notify_complete.py '{}'"
      }]
    }]
  }
}
```

Replace `{vibereps_dir}` with the actual path (e.g., `~/.vibereps` or the repo path).
Replace `{exercises}` with comma-separated exercise list (e.g., `squats,jumping_jacks,calf_raises`).

### Step 4: Test

Run a quick test:
```bash
./exercise_tracker.py user_prompt_submit '{}'
```

## Important Paths

- Hook script: Use `$PWD/exercise_tracker.py` if in repo, or `~/.vibereps/exercise_tracker.py` if installed via curl
- UI file: `exercise_ui.html` (same directory as hook script)
- Settings: `~/.claude/settings.json`

## Detecting Install Location

Check which exists:
```bash
if [[ -f "$HOME/.vibereps/exercise_tracker.py" ]]; then
    VIBEREPS_DIR="$HOME/.vibereps"
elif [[ -f "./exercise_tracker.py" ]]; then
    VIBEREPS_DIR="$(pwd)"
fi
```

## Disable Later

To temporarily disable, add `VIBEREPS_DISABLED=1` to the hook command.
