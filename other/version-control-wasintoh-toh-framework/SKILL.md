---
name: version-control
description: >
  Natural-language undo, rollback, and checkpoints that hide git entirely —
  "ย้อนกลับ", "undo", "ไม่เอาแล้ว", "เอาอันเดิมคืน" map to safe git
  stash/revert/checkpoint operations with cleanup and dev-server restart,
  reported in plain language. Use when the user wants to undo changes, restore
  a previous state, or save a safe checkpoint.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# ⏪ Version Control Skill

> **Purpose:** Easy undo/rollback without knowing git
> **Version:** 1.0.0
> **Author:** Toh Framework Team

## Overview

This skill enables users to undo changes easily using natural language, without needing to understand git commands or version control concepts.

## Core Principle

```
User says: "ย้อนกลับ" or "undo"
AI does: git stash/revert + cleanup + restart dev
User sees: "เรียบร้อยครับ กลับไปก่อนแก้ไขล่าสุดแล้ว"
```

**HIDE GIT COMPLEXITY** - User just says what they want.

---

## Trigger Words

### Undo/Rollback

| User Says | AI Understands |
|-----------|----------------|
| ย้อนกลับ | Undo last change |
| undo | Undo last change |
| เอาอันเดิมคืน | Revert to previous |
| ไม่เอาแล้ว | Discard current changes |
| กลับไปก่อนหน้า | Go back to previous state |
| ยกเลิกที่ทำไป | Cancel what was done |
| rollback | Revert changes |

### Checkpoint/Save

| User Says | AI Understands |
|-----------|----------------|
| save ไว้ก่อน | Create checkpoint |
| checkpoint | Create savepoint |
| เซฟไว้ | Save current state |
| บันทึกจุดนี้ | Mark this point |

---

## Auto-Checkpoint System

AI automatically creates checkpoints at key moments:

### Auto-Checkpoint Triggers

| Event | Checkpoint Name |
|-------|-----------------|
| After `/toh-vibe` | `vibe-[project-name]-initial` |
| After `/toh-ui` completion | `ui-[component-name]-done` |
| After `/toh-dev` completion | `dev-[feature-name]-done` |
| After `/toh-connect` | `connect-supabase-done` |
| Before major changes | `pre-[action]-backup` |

### Checkpoint Storage

```
.toh/checkpoints/
├── checkpoint-log.json     # List of all checkpoints
└── (git handles actual data)
```

**checkpoint-log.json:**
```json
{
  "checkpoints": [
    {
      "id": "cp-001",
      "name": "vibe-coffee-shop-initial",
      "timestamp": "2024-12-03T10:30:00Z",
      "description": "หลังสร้างโปรเจคร้านกาแฟ",
      "gitRef": "abc123"
    },
    {
      "id": "cp-002", 
      "name": "ui-dashboard-done",
      "timestamp": "2024-12-03T11:00:00Z",
      "description": "หลังสร้าง Dashboard UI",
      "gitRef": "def456"
    }
  ]
}
```

---

## Undo Operations

### Quick Undo (Last Change)

```
User: "ย้อนกลับ"

AI Process:
1. git stash or git checkout -- .
2. Restart dev server if needed
3. Confirm to user

AI Response:
"⏪ ย้อนกลับแล้วครับ!
กลับไปก่อนที่จะ [last action] แล้ว

💡 ถ้าต้องการ:
- ดูประวัติการแก้ไข พิมพ์ 'ดูประวัติ'
- ย้อนกลับไปจุดที่ save ไว้ พิมพ์ 'กลับไป [ชื่อ checkpoint]'"
```

### Rollback to Checkpoint

```
User: "กลับไปก่อนแก้ไข dashboard"

AI Process:
1. Find checkpoint matching "dashboard"
2. git checkout [checkpoint-ref]
3. Restart dev server
4. Confirm to user

AI Response:
"⏪ กลับไป checkpoint 'ui-dashboard-done' แล้วครับ!
(บันทึกเมื่อ 2 ชั่วโมงก่อน)

สถานะปัจจุบัน:
- ✅ Dashboard UI เสร็จแล้ว
- ❌ การแก้ไขหลังจากนั้นถูกยกเลิก

ทำต่อได้เลยครับ!"
```

### View History

```
User: "ดูประวัติ"

AI Response:
"📜 ประวัติการทำงาน:

1. 🕐 10:30 - สร้างโปรเจคร้านกาแฟ ✅
2. 🕐 11:00 - สร้าง Dashboard UI ✅
3. 🕐 11:30 - เพิ่ม POS logic ✅
4. 🕐 12:00 - ปรับ design → (ปัจจุบัน)

พิมพ์ 'กลับไป [เลข]' เพื่อย้อนกลับ
เช่น 'กลับไป 2' จะกลับไปหลังสร้าง Dashboard"
```

---

## Safety Features

### Before Destructive Operations

```
User: "ลบหน้า dashboard ทิ้ง"

AI: "⚠️ จะลบหน้า Dashboard นะครับ

ไฟล์ที่จะลบ:
- app/dashboard/page.tsx
- components/dashboard/

ยืนยันไหมครับ? (yes/no)
หรือพิมพ์ 'save ก่อน' เพื่อ backup ก่อนลบ"
```

### Auto-Backup Before Risky Changes

AI automatically creates backup before:
- Deleting files
- Major refactoring
- Changing database schema
- `/toh-connect` (in case of data loss)

---

## Git Operations Mapping

### User Language → Git Commands

| User Says | Git Operation |
|-----------|---------------|
| ย้อนกลับ | `git checkout -- .` or `git stash` |
| กลับไป checkpoint | `git checkout [ref]` |
| save ไว้ | `git add . && git commit -m "[auto]"` |
| ดูประวัติ | `git log --oneline` |
| ดู diff | `git diff` |
| ลบทิ้งหมด | `git reset --hard HEAD` |

### AI Never Shows

- Raw git commands
- Commit hashes (use checkpoint names instead)
- Merge conflicts (resolve automatically)
- Git error messages (translate or fix)

---

## Response Templates

### Successful Undo

```markdown
⏪ **ย้อนกลับแล้วครับ!**

กลับไปสถานะ: [checkpoint name]
เมื่อ: [time ago]

📁 ไฟล์ที่กลับคืน:
- [file list]

ทำต่อได้เลยครับ!
```

### Checkpoint Created

```markdown
💾 **บันทึก checkpoint แล้วครับ!**

ชื่อ: [checkpoint name]
เวลา: [now]

ถ้าต้องการกลับมาจุดนี้ พิมพ์:
"กลับไป [checkpoint name]"
```

### Cannot Undo

```markdown
⚠️ **ย้อนกลับไม่ได้ครับ**

เหตุผล: [reason in friendly language]

💡 แนะนำ:
- [alternative action]
```

---

## Integration with Memory

Update `.toh/memory/active.md` after undo:

```markdown
## Last Action
Undo to checkpoint: ui-dashboard-done

## Current State  
- Dashboard UI complete
- POS logic removed (was undone)

## Available Checkpoints
- vibe-coffee-shop-initial (10:30)
- ui-dashboard-done (11:00) ← current
```

---

## Best Practices

### DO:
- ✅ Auto-checkpoint at key moments
- ✅ Use friendly checkpoint names
- ✅ Confirm before destructive operations
- ✅ Show what will be undone

### DON'T:
- ❌ Show raw git commands
- ❌ Show commit hashes to user
- ❌ Allow undo without confirmation for major changes
- ❌ Lose user's work without backup

---

*Last Updated: 2024-12-03*
