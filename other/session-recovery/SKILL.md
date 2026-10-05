---
name: session-recovery
description: >
  Seamless continuation across sessions and IDEs — on session start, read
  .toh/memory/ and greet the user with where the last session left off so
  nothing needs re-explaining. Handles first run (no memory yet), mid-task
  resume, and returns after days or weeks. Use at the start of every new
  session or when the user says continue / "ทำต่อ".
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🔄 Session Recovery Skill

> **Purpose:** Seamless continuation across sessions and IDEs
> **Version:** 1.0.0
> **Author:** Toh Framework Team

## Overview

This skill enables AI to remember context across sessions and IDEs, so users can continue where they left off without re-explaining everything.

## Core Principle

```
User opens new session (even after days/weeks)
    ↓
AI reads memory files
    ↓
AI greets with context: "สวัสดีครับ! ครั้งก่อนเราทำ X ค้างไว้..."
    ↓
User can continue immediately
```

**ZERO RE-EXPLANATION NEEDED**

---

## Session Start Behavior

### First Time (No Memory)

When `.toh/memory/` is empty or doesn't exist:

```markdown
สวัสดีครับ! 👋 ผมเป็น Toh Framework Agent

พร้อมช่วยสร้างระบบให้ครับ บอกได้เลยว่าอยากสร้างอะไร

💡 ตัวอย่าง:
- "สร้างระบบร้านกาแฟ"
- "สร้างเว็บขายของออนไลน์"
- "สร้างระบบจองคิว"

หรือพิมพ์ `/toh-help` เพื่อดูคำสั่งทั้งหมดครับ
```

### Returning User (Has Memory)

When `.toh/memory/` has data:

```markdown
สวัสดีครับพี่โต! 👋 ยินดีต้อนรับกลับมา

📋 **สรุปโปรเจค:** [project name]
[Brief summary from summary.md]

🔥 **ครั้งก่อนทำค้างไว้:**
- [Last active task from active.md]

📊 **สถานะปัจจุบัน:**
- ✅ [Completed items]
- ⏳ [In progress]
- ⬚ [Not started]

💡 **แนะนำ:** [Next logical step]

ทำต่อเลยไหมครับ? หรือต้องการทำอะไรอื่น?
```

---

## Memory Reading Protocol

### On Session Start

AI MUST read these files in order:

```
1. .toh/memory/active.md     → Current task, blockers
2. .toh/memory/summary.md    → Project overview, features
3. .toh/memory/decisions.md  → Key decisions made
4. (Optional) .toh/memory/archive/ → If user asks about history
```

### Smart Summary Generation

AI should summarize, not dump raw content:

```
❌ Bad: "active.md says: Current Focus: Dashboard UI..."

✅ Good: "ครั้งก่อนกำลังทำ Dashboard UI ครับ เหลือแค่เชื่อม API"
```

---

## Cross-IDE Continuity

### Scenario: Claude Code → Cursor

```
[Claude Code session ends]

[User opens Cursor]

Cursor AI: "สวัสดีครับ! ผมเห็นว่าเมื่อกี้ทำกับ Claude Code อยู่
          กำลังทำ Dashboard ค้างไว้ที่ส่วน API connection ครับ
          
          ทำต่อเลยไหมครับ?"
```

### Scenario: Days Gap

```
[User returns after 3 days]

AI: "สวัสดีครับพี่โต! 👋 ไม่เจอกัน 3 วัน
    
    📋 โปรเจคร้านกาแฟ - สถานะล่าสุด:
    - ✅ UI ทุกหน้าเสร็จแล้ว
    - ✅ Mock data พร้อม
    - ⏳ ยังไม่ได้เชื่อม Supabase
    
    ครั้งก่อนค้างไว้ที่: จะเชื่อม database
    
    ทำต่อเลยไหมครับ?"
```

---

## Context Awareness

### AI Should Know

| Information | Source |
|-------------|--------|
| Project name & type | summary.md |
| Business context | summary.md + business-context skill |
| Completed features | summary.md |
| Current task | active.md |
| Blockers/Issues | active.md |
| Key decisions | decisions.md |
| Tech choices | decisions.md |

### AI Should Track

| Metric | Purpose |
|--------|---------|
| Last session date | Time gap awareness |
| Last command used | Context for continuation |
| Incomplete tasks | Remind user |
| Errors encountered | Avoid repeating |

---

## Memory Update Protocol

### After Every Task

```
1. Update active.md
   - Move completed items
   - Add new next steps
   - Update current focus

2. Update summary.md (if feature completed)
   - Add to completed features
   - Update project structure

3. Update decisions.md (if decision made)
   - Log architectural decisions
   - Log design decisions
```

### Session End (If Detectable)

```markdown
## In active.md

### Session Log
- Session ended: [timestamp]
- Last action: [action]
- Pending: [what was in progress]
```

---

## Quick Continuation Commands

User can say:

| Command | AI Does |
|---------|---------|
| "ทำต่อ" / "continue" | Continue last task |
| "ทำต่อจากที่ค้างไว้" | Same as above |
| "ทำอะไรค้างไว้" | Show pending tasks |
| "สรุปให้หน่อย" | Summarize project state |
| "เริ่มใหม่" | Start fresh (confirm first) |

---

## Response Templates

### Session Start (With Context)

```markdown
สวัสดีครับพี่โต! 👋

📋 **[Project Name]** - [Business Type]

**สถานะ:**
[Progress bar or checklist]

**ครั้งก่อน:** [Last action]

**ถัดไป:** [Suggested next step]

ทำต่อเลยไหมครับ?
```

### Quick Status Check

```markdown
📊 **สถานะโปรเจค**

| Phase | Status |
|-------|--------|
| UI | ✅ เสร็จ |
| Logic | ⏳ 70% |
| Database | ⬚ ยังไม่เริ่ม |
| Testing | ⬚ ยังไม่เริ่ม |
| Deploy | ⬚ ยังไม่เริ่ม |

**กำลังทำ:** [Current task]
**ถัดไป:** [Next step]
```

---

## Edge Cases

### Empty Project (Has .toh but no code)

```markdown
สวัสดีครับ! 👋

เห็นว่าโปรเจคนี้ติดตั้ง Toh Framework แล้ว
แต่ยังไม่ได้เริ่มสร้างอะไรครับ

พร้อมเริ่มเมื่อไหร่ก็บอกได้เลยครับ!

💡 ลองเริ่มด้วย: "สร้างระบบ [อธิบายสั้นๆ]"
```

### Corrupted/Incomplete Memory

```markdown
สวัสดีครับ! 👋

ผมอ่าน memory ได้บางส่วน แต่ไม่ครบถ้วนครับ

จากที่เห็น:
- โปรเจค: [what can be detected]
- ไฟล์ที่มี: [detected files]

ช่วยบอกหน่อยได้ไหมครับว่าทำถึงไหนแล้ว?
ผมจะอัพเดท memory ให้ครับ
```

### Multiple Projects (Future)

```markdown
สวัสดีครับ! 👋

พบหลายโปรเจคในเครื่อง:
1. ☕ ร้านกาแฟ (active.md อัพเดทเมื่อวาน)
2. 🛒 E-commerce (active.md อัพเดท 3 วันก่อน)

ต้องการทำโปรเจคไหนครับ?
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| Smart Suggestions | Use memory to suggest relevant next steps |
| Business Context | Remember business type for context |
| Progress Tracking | Read/write progress to memory |
| Error Handling | Remember past errors to avoid |

---

## Best Practices

### DO:
- ✅ Greet with context immediately
- ✅ Summarize, don't dump raw data
- ✅ Offer to continue where left off
- ✅ Keep memory updated after every task

### DON'T:
- ❌ Ask "what are we working on?" when memory exists
- ❌ Ignore memory files
- ❌ Show raw memory content
- ❌ Forget to update memory after tasks

---

*Last Updated: 2024-12-03*
