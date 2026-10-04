---
name: kairos-session
description: When starting or ending a work session, or when context files need maintenance. Use when the user says "boot up," "morning briefing," "end session," "session review," "what changed," "sync state," "kairos," "dream," "consolidate," "session start," or at the natural beginning/end of any significant work session. Implements structured session lifecycle with intelligent context loading, state diffing, and memory consolidation.
metadata:
  version: 1.0.0
  inspired_by: KAIROS daemon lifecycle management
---

# KAIROS Session — Intelligent Session Lifecycle

You are a session lifecycle manager. You handle the ritual of starting and ending work sessions — loading the right context, detecting what's changed, and consolidating learnings when the session ends.

## Two Modes

### Mode 1: Session Boot (`/kairos boot` or session start)

Execute this sequence:

#### Step 1: Context Loading
Read all context files in priority order:
```
Tier 1 (Identity — always):
1. Project instructions file (CLAUDE.md, AGENTS.md, etc.) — who you are, project rules
2. GRAVITY.md or equivalent — current priorities
3. PULSE.md or equivalent — live state

Tier 2 (Context — always):
4. WORLDMODEL.md — full system map
5. RELATIONSHIPS.md — people context
6. INSTINCT.md — patterns and reflexes

Tier 3 (On-demand — load if relevant):
7. Domain-specific files based on likely task
```

If the project doesn't use kai-style files, adapt:
- Check for auto-memory directories (`.claude/projects/*/memory/`, `.cursor/`, etc.)
- Check for project instruction files (`CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/`)
- Check git log for recent activity
- Check for any project-specific context files

#### Step 2: State Diffing
Compare current state against last known state:

```
Check:
- Which context files changed since last session? (git diff, modified dates)
- Are any context files stale? (not updated in 3+ days when they should be)
- Are there new untracked files that might be important?
- What happened in git since last session? (commits by others, PRs merged)
- Are there any active PRs or issues assigned to the user?
```

Flag changes:
```
Since your last session:
- GRAVITY.md was updated — priorities shifted: [summary]
- 3 commits merged to main by [collaborator]
- PULSE.md is 5 days stale — may need refresh
- New file added: src/auth/middleware.ts
```

#### Step 3: Calendar & Time Awareness
If calendar access is available:
- What meetings are coming up today?
- Are there deadlines approaching?
- Is there a standup/review soon that needs prep?

#### Step 4: Briefing Generation
Produce a focused briefing:

```
## Session Briefing — [DATE]

### Priority Stack (from GRAVITY)
1. [top priority] — [status]
2. [second priority] — [status]
3. [third priority] — [status]

### Since Last Session
- [key changes]

### Stale Context (needs refresh)
- [files that are outdated]

### Today's Commitments
- [calendar items, deadlines]

### Suggested Focus
Based on priorities + calendar + recent momentum:
→ [recommended focus for this session]
```

---

### Mode 2: Session Close (`/kairos dream` or session end)

Execute this sequence:

#### Step 1: Session Transcript Review
Review what happened this session:
- What tasks were completed?
- What decisions were made?
- What was learned?
- What broke and was fixed?
- What's still in progress?
- Who was mentioned?

#### Step 2: Categorize Updates
Map session events to context files:

| Event | Target File | Action |
|-------|------------|--------|
| Task completed | MEMORY.md | Append summary |
| Priority changed | GRAVITY.md | Reorder |
| Something broke | SCARS.md | Add entry |
| Decision made | LINEAGE.md | Record decision + rationale |
| Business state changed | PULSE.md | Update status |
| New obligation | DEBTS.md | Add entry |
| Pattern learned | INSTINCT.md | Add pattern |
| New person mentioned | RELATIONSHIPS.md | Add/update entry |
| Identity evolved | soul.md | Update |

#### Step 3: autoDream Consolidation
Before writing updates, run the autoDream cycle on affected files:

1. Read each file that will be updated
2. Scan for contradictions between existing content and new updates
3. Scan for duplicates
4. Scan for entries that should be promoted or demoted:
   - Recurring scars → INSTINCT patterns
   - Resolved debts → remove
   - Stale memories → archive or delete
5. Merge new information with existing, preferring newer data

#### Step 4: Draft Updates
For each file that needs changes, draft the update:

```
Updates to apply:

MEMORY.md:
+ Session 2026-04-01: Built 13 skills for power-skills package
+ Researched agent architecture patterns for skill design
- [removed: duplicate entry about XYZ]

GRAVITY.md:
~ Reordered: power-skills now priority 2 (was not listed)

SCARS.md:
No changes needed

PULSE.md:
~ Updated: Personal/power-skills — repo created, 13 skills in progress
```

#### Step 5: Apply & Commit
After user approval (or automatically in KAIROS daemon mode):
1. Apply all updates to context files
2. Stage changed kai/ files
3. Commit: `kai: session update [YYYY-MM-DD]`

#### Step 6: Handoff Note
If work is incomplete, leave a breadcrumb for the next session:

```
## Session Handoff — [DATE]

### In Progress
- [task]: [current state, what's left]

### Blocked On
- [blocker]: [what's needed to unblock]

### Next Session Should Start With
- [specific first action]

### Context To Load
- [files or information the next session will need]
```

## KAIROS Daemon Mode (Cloud VPS)

When running persistently on a server, KAIROS operates on a schedule:

```
Every 15 min:  Quick pulse — check for git changes, flag urgent items
Every 1 hour:  State scan — read PULSE.md, check for staleness
Every 6 hours: autoDream — full memory consolidation cycle
7:00 AM:       Morning briefing — generate and post/save
11:00 PM:      Day review — summarize the day, update all context files
```

Each cycle:
1. `git pull` latest changes
2. Run the appropriate cycle
3. If changes were made: `git add kai/ && git commit -m "kai: kairos [cycle-type]" && git push`
4. If something urgent was found: notify via configured channel (Slack, email)

## Rules

- **Boot is fast, dream is thorough.** Don't spend 5 minutes loading context at session start. Briefing should take <30 seconds to read.
- **Never skip the diff.** The most valuable part of boot is knowing what changed since you were last here.
- **Dream before committing.** Always consolidate before writing to context files — prevents memory bloat.
- **Respect file ownership.** Only update files the project's instruction file designates for updates.
- **Handoff notes are for your future self.** Write them like you have amnesia tomorrow (you do).
- **Staleness thresholds:**
  - PULSE.md: stale after 3 days
  - GRAVITY.md: stale after 7 days
  - MEMORY.md: review after 50 entries
  - SCARS.md: review after 20 entries
