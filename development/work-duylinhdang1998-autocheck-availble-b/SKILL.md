---
name: work
description: Submit a new project request OR report bugs to X Company. Use for building software systems, web/mobile apps, games, or reporting bugs on existing projects. The main agent acts as CEO using core role instructions.
---

# /work - Submit Project Request

**SESSION ID**: `${CLAUDE_SESSION_ID}`

> ⚠️ **IMPORTANT**: Use this session ID for ALL role switches in this conversation:
> ```bash
> bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" <role>.md
> ```

Welcome to **X Company**!

## Architecture (v2.0)

**Core Roles** (READ, don't spawn): `.claude/core/` (ceo.md, cto.md, hr.md, pm.md)
**Specialists** (SPAWN these): `.claude/agents/` (all specialists)

## How It Works

When `/work` is invoked:

```bash
cd "$CLAUDE_PROJECT_DIR" && bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" ceo.md
```

```
Phase 1: CEO Approval
├── 1. 🎯 [CEO] → Read core/ceo.md → Analyze requirements
├── 2. 🎯 [CEO] → Ask HIGH-LEVEL questions if needed
└── 3. 🎯 [CEO] → Approve scope → Delegate to PM

Phase 2: Sprint 0 (Planning - No Code)
├── 4. 📋 [PM] → Read core/pm.md → Init project (bash init-project.sh)
├── 5. 📊 [BA] → Read core/ba.md → Ask DETAILED questions → Write SRS
├── 6. 📋 [PM] → ⭐ SPRINT 0 CHECKPOINTS ⭐ (user confirms decisions)
│       ├── Wireframes: Yes / No / External design?
│       ├── Tech Stack: OK / Modify?
│       └── Team: OK / Modify?
├── 7. 🏗️ [CTO] → Read core/cto.md → (if user confirms) Finalize tech-stack.md
├── 8. 👥 [HR] → Read core/hr.md → (if user confirms) Finalize team.md + VERIFICATION
├── 9. 🎨 [UX] → (if user chose wireframes) Spawn apple-ux-wireframer
└── 10. 📋 [PM] → Read core/pm.md → Phase Gate 1 Check → Sprint 1 Plan

Phase 3: Development (Sprint 1+)
├── 11. 📋 [PM] → SPAWN specialists in PARALLEL
├── 12. 📋 [PM] → Track progress, resolve blockers
└── 13. 📋 [PM] → Report milestones to CEO

Phase 4: Bug Fix (Post-release)
├── 🎯 [CEO] → Detect bug report → Check active project → Confirm → Delegate to PM
└── 📋 [PM] → Read pm.md → See Bug Fix section → Read helpers/pm-bug-fix-flow.md
    ├── Step 1: Read project state
    ├── Step 2: Bug triage (PM interviews user — no role switch)
    ├── Step 3: Team check (PM assesses team — no role switch)
    ├── Step 4: Create bug fix sprint (create-sprint.sh)
    ├── Step 5: Present plan → wait for user approval
    └── Step 6: SPAWN specialists → Code review → QA
```

**Key points:**
- CEO approves, PM orchestrates
- PM "wears different hats" (CTO, HR, BA) when reading those roles
- **Sprint 0 Checkpoints** allow user to skip wireframes, modify tech stack, adjust team
- Role indicators (🎯🏗️👥📋📊🎨) are MANDATORY for each output
- HR verification checklist MUST be completed before spawning
- **NO nested agent spawning** - only one layer of actual agents (specialists)
- **Monitor**: Run `/monitor start` to view real-time dashboard (auto-tracking enabled)

## ⭐ Role Delegation Rules (MANDATORY)

**CRITICAL: When switching roles, you MUST:**
1. **Bash echo** to `.claude/.active-core` with session ID and target role filename
2. **Read** the target role file

### Delegation Matrix

| From | To | Action Required |
|------|----|-----------------|
| CEO | PM | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" pm.md)` → `Read(core/pm.md)` |
| PM | CTO | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" cto.md)` → `Read(core/cto.md)` |
| PM | HR | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" hr.md)` → `Read(core/hr.md)` |
| PM | BA | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" ba.md)` → `Read(core/ba.md)` |
| BA | PM | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" pm.md)` → `Read(core/pm.md)` |
| CTO | PM | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" pm.md)` → `Read(core/pm.md)` |
| HR | PM | `Bash(bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" pm.md)` → `Read(core/pm.md)` |

### Correct Example

```
🎯 [CEO] → Project approved. Delegating to PM.
         ↓
[Bash: bash .claude/automation/set-active-core.sh "${CLAUDE_SESSION_ID}" pm.md]   ← REQUIRED!
[Read: .claude/core/pm.md]                                                         ← REQUIRED!
         ↓
📋 [PM] → Received handover from CEO...
```

### Wrong Example

```
🎯 [CEO] Project approved. Delegating to PM.    ← ❌ Missing set-active-core.sh call!
📋 [PM] Starting project...                     ← ❌ Did NOT read pm.md!
```

## Commands

### Create New Project
```
/work "Build a social media app like Instagram"
```

### Continue Project
```
/work continue
/work tiếp tục
```

### Report Bugs
```
/work I found bugs: login fails on mobile, dashboard chart not rendering (+ screenshots)
/work trang settings bị lỗi, nút save không hoạt động
```
When user message relates to bugs/errors/issues but doesn't explicitly say "bug",
CEO MUST ask to confirm: "It sounds like you're reporting bugs. Is that correct?"

### Check Status
```
/work status
```

