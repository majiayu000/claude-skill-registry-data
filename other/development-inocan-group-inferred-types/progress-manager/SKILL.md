---
name: progress-manager
description: |
  Manages course progress tracking in ~/.claude-course/progress.json.
  Use when: loading, saving, or displaying course progress.
  Internal skill - used by /ccc:course commands.
---

# Progress Manager

Tracks user progress through the Claude Code Course.

## Storage Location

```
./progress.json
```

Progress is stored in the current working directory. This keeps progress tied to the project.

## Progress Schema

```json
{
  "version": "1.0.0",
  "started_at": "2025-01-15T10:00:00Z",
  "current_lesson": 1,
  "lessons": {
    "1": {
      "started_at": "2025-01-15T10:00:00Z",
      "completed_at": null,
      "theory_read": true,
      "practice_completed": false,
      "practice_attempts": 2
    }
  },
  "completed": false
}
```

## Operations

### Load Progress

Read `./progress.json`. If doesn't exist, use default:
```json
{"version":"1.0.0","current_lesson":1,"lessons":{},"completed":false}
```

### Save Progress

Write updated JSON to `./progress.json`.

### Reset Progress

Delete `./progress.json`.

## Display Progress

### Progress Bar
```
Lesson 1: ████████░░ 80%
Lesson 2: ██████████ Done!
Lesson 3: ░░░░░░░░░░ Not started
```

### Summary
```
## Your Progress

Current: Lesson 2 — Твой первый скилл
Completed: 1/5 lessons
Time spent: ~45 minutes

Next: Complete practice task for Lesson 2
```

## Lesson States

| State | Display | Meaning |
|-------|---------|---------|
| not_started | ░░░░░░░░░░ | Haven't opened yet |
| in_progress | ████░░░░░░ | Theory read, practice pending |
| completed | ██████████ ✓ | All tasks done |

## Update Progress

### Mark Theory Read
```json
{
  "lessons": {
    "1": {
      "theory_read": true
    }
  }
}
```

### Mark Practice Completed
```json
{
  "lessons": {
    "1": {
      "practice_completed": true,
      "completed_at": "2025-01-15T10:30:00Z"
    }
  },
  "current_lesson": 2
}
```

### Mark Course Completed
When lesson 5 practice is completed:
```json
{
  "completed": true,
  "completed_at": "2025-01-15T12:00:00Z"
}
```

## Integration

Used by:
- `/ccc:course` — Show current progress, continue
- `/ccc:progress` — Detailed progress view
- `/ccc:lesson N` — Update current lesson
- `/ccc:practice` — Track practice attempts
- `/ccc:reset` — Clear all progress
