---
name: gap-tracker
description: Track and update progress on system design gap implementation. Use when implementing patterns, marking items complete, checking progress, viewing remaining items, or updating the implementation plan. Triggers on "mark complete", "check progress", "show gaps", "update tracker", "what's next", "implementation status".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Gap Implementation Tracker

A skill to track progress on implementing system design patterns from the ByteByteGo gap analysis.

## File Locations

- **Implementation Plan**: `docs/gap-analysis/implementation-plan.md`
- **Gap Analyses**: `docs/gap-analysis/part_*_gap_analysis.md`
- **System Design Page**: `app/system-design/page.tsx`

## Commands

### 1. Check Progress
When the user asks to "check progress", "show status", or "implementation status":

1. Read the implementation plan file
2. Count completed items (lines with `- [x]`)
3. Count remaining items (lines with `- [ ]`)
4. Report summary by phase

**Response format:**
```
## Implementation Progress

### Phase 1 (HIGH Priority)
- Completed: X/55
- In Progress: X
- Remaining: X

### Phase 2 (MEDIUM Priority)
- Completed: X/45
- Remaining: X

### Phase 3 (LOW Priority)
- Completed: X/30
- Remaining: X

### Overall: X/130 items completed (X%)
```

### 2. Mark Item Complete
When the user says "mark complete [ITEM-ID]" or "completed [ITEM-ID]":

1. Read the implementation plan
2. Find the line containing the item ID (e.g., `CACHE-001`, `K8S-002`)
3. Change `- [ ]` to `- [x]` for that line
4. Update the Summary Dashboard counts at the top of the file
5. Add an entry to the Progress Log with today's date
6. Write the updated file

**Example:**
User: "Mark complete CACHE-001"
→ Find `- [ ] **CACHE-001**:` and change to `- [x] **CACHE-001**:`
→ Update dashboard: Phase 1 Completed: 0 → 1, Remaining: 55 → 54

### 3. Show Next Items
When the user asks "what's next", "show next items", or "what should I work on":

1. Read the implementation plan
2. Find the first uncompleted items in Phase 1 (HIGH priority)
3. Show the next 5 items to work on
4. Include the item ID, title, and brief description

**Response format:**
```
## Next Items to Implement

1. **CACHE-001**: Thunder Herd Problem
   - Diagram showing problem and solutions (locking, early expiration)

2. **CACHE-002**: Cache Penetration
   - Queries for non-existent data, Bloom filter solution

[etc.]
```

### 4. Show Items by Category
When the user asks "show [category] items" or "list [category] gaps":

1. Read the implementation plan
2. Filter items by category prefix (e.g., CACHE, K8S, NET, SEC, DB)
3. Show all items in that category with completion status

**Category prefixes:**
- `CACHE` - Caching
- `K8S` - Kubernetes
- `NET` - Networking
- `SEC` - Security
- `DB` - Database
- `MICRO` - Microservices
- `CLOUD` - Cloud
- `CASE` - Case Studies
- `APP` - Application Patterns
- `DATA` - Data Engineering
- `SEARCH` - Search
- `AI` - AI/ML
- `LINUX` - Linux/OS
- `API` - API Design
- `RT` - Real-Time
- `DEVOPS` - DevOps
- `PERF` - Performance
- `ARCH` - Architecture
- `MSG` - Messaging
- `PAY` - Payment
- `DEV` - Developer Resources
- `ROAD` - Roadmaps
- `PROG` - Programming
- `WEB` - Web/Frontend
- `MISC` - Miscellaneous

### 5. Update Dashboard
When the user says "update dashboard" or after marking items complete:

1. Count all `- [x]` items in Phase 1, Phase 2, Phase 3
2. Update the Summary Dashboard table at the top of the file
3. Update the "Last Updated" date

**Dashboard format to update:**
```markdown
| Phase | Total Items | Completed | In Progress | Remaining |
|-------|-------------|-----------|-------------|-----------|
| Phase 1 (HIGH) | 55 | [COUNT] | 0 | [55-COUNT] |
| Phase 2 (MEDIUM) | 45 | [COUNT] | 0 | [45-COUNT] |
| Phase 3 (LOW) | 30 | [COUNT] | 0 | [30-COUNT] |
| **TOTAL** | **130** | **[TOTAL]** | **0** | **[130-TOTAL]** |
```

### 6. Add Progress Log Entry
When the user says "log progress" or after completing items:

1. Find the Progress Log section
2. Add a new row with today's date, items completed, and notes
3. Write the updated file

**Format:**
```markdown
| 2026-01-02 | CACHE-001, CACHE-002 | Implemented caching problems diagrams |
```

### 7. Verify Implementation
When the user says "verify [ITEM-ID]" or "check if [ITEM-ID] is implemented":

1. Read the item details from implementation plan
2. Search the system-design page.tsx for related patterns
3. Report whether the pattern exists and completeness

## Example Interactions

**User:** "Check progress"
**Claude:** Reads implementation plan, counts items, reports summary

**User:** "Mark complete K8S-001"
**Claude:** Updates the item to [x], updates dashboard, logs progress

**User:** "What's next?"
**Claude:** Shows next 5 uncompleted HIGH priority items

**User:** "Show all caching items"
**Claude:** Lists all CACHE-* items with their status

**User:** "I just implemented the Thunder Herd pattern"
**Claude:** Identifies CACHE-001, marks it complete, updates dashboard

## Notes

- Always update the dashboard after marking items complete
- Keep the Progress Log updated for tracking velocity
- Phase 1 items should be prioritized over Phase 2 and 3
- When implementing, refer to the original gap analysis files for more details
