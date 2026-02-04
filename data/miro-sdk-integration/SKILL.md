---
name: miro-sdk-integration
description: Use when working with Miro SDK v2 operations, board manipulation, creating shapes, text, frames, or syncing data between Miro and database. Helps implement features for master board, project rows, and client reports.
allowed-tools: Read, Grep, Glob, Edit, Bash, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__query-docs
---

# Miro SDK v2 Integration Skill

## Overview

This skill guides implementation of Miro SDK v2 features for the project management system. It ensures proper use of existing services, adherence to board architecture patterns, and safe database synchronization.

---

## Critical Services (Always Read First)

**Location**: `/src/features/boards/services/`

### Core Services

1. **miroSdkService.ts** (106KB - Primary Workhorse)
   - 50+ methods for board operations
   - Shape creation, text manipulation, frame organization
   - Safe operations that return null on error instead of throwing
   - Methods: `createFrame()`, `createStickyNote()`, `createText()`, `createShape()`, etc.

2. **masterBoardService.ts**
   - Manages "Master Board" - consolidated view of all clients with projects
   - Creates vertical frames with mini-kanbans
   - Updates when projects change status
   - Coordinates with `projectRowService`

3. **projectRowService.ts**
   - Manages individual project timeline rows
   - Status columns for deliverables (pending, wip, review, approved)
   - Real-time updates from database changes
   - Tracks Miro item IDs in `miroItemRegistry`

4. **projectSyncOrchestrator.ts**
   - Orchestrates bidirectional sync: Database ↔ Miro
   - Source of truth is always Supabase
   - Handles create, update, delete operations
   - Prevents infinite sync loops

5. **brandWorkspaceService.ts**
   - Creates project workspace frames
   - Sections: Brief, Process, Deliverables
   - Project-specific collaboration area

6. **miroReportService.ts** & **miroClientReportService.ts**
   - Generate visual reports on Miro boards
   - Charts, metrics, status summaries
   - Client-facing report generation

7. **miroItemRegistry.ts**
   - Tracks Miro item IDs ↔ Database entity relationships
   - Critical for identifying what items represent
   - Prevents duplicate creation

---

## Safe SDK Access Pattern

**ALWAYS use `miroAdapter`** from `@shared/lib/miroAdapter`:

```typescript
import { miroAdapter } from '@shared/lib/miroAdapter';

// ✅ Check availability before operations
if (miroAdapter.isAvailable()) {
  await miroAdapter.showInfo('Message to user');
}

// ✅ Safe operations return null instead of throwing
const boardInfo = await miroAdapter.getBoardInfo();
if (!boardInfo) {
  logger.warn('Not in Miro context');
  return;
}

// ✅ Get board ID safely
const boardId = await miroAdapter.getBoardId();

// ❌ NEVER access window.miro directly
// window.miro.board.get() // DON'T DO THIS
```

---

## Board Architecture

### Master Board Layout

```
┌─────────────────────────────────────────┐
│          MASTER BOARD                    │
├─────────────────────────────────────────┤
│  Client A         Client B               │
│  ┌─────────┐     ┌─────────┐            │
│  │ Project │     │ Project │            │
│  │  Mini   │     │  Mini   │            │
│  │ Kanban  │     │ Kanban  │            │
│  └─────────┘     └─────────┘            │
└─────────────────────────────────────────┘
```

Managed by: `masterBoardService.ts`

### Project Row Layout

```
┌───────────────────────────────────────────────┐
│  PROJECT: "Brand Identity for Client X"       │
├──────────┬──────────┬──────────┬─────────────┤
│ Pending  │   WIP    │  Review  │  Approved   │
├──────────┼──────────┼──────────┼─────────────┤
│ [Logo]   │ [Colors] │ [Fonts]  │ [Guidelines]│
└──────────┴──────────┴──────────┴─────────────┘
```

Managed by: `projectRowService.ts`

---

## Constants & Configuration

**Location**: `/src/features/boards/services/constants/`

```typescript
// Layout constants
import { LAYOUT } from '@shared/config/boardConfig';

LAYOUT.frameStartX      // Starting X position for frames
LAYOUT.frameStartY      // Starting Y position for frames
LAYOUT.frameWidth       // Standard frame width
LAYOUT.frameHeight      // Standard frame height
LAYOUT.stickyNoteSize   // Standard sticky note dimensions

// Colors (Use explicit hex - CSS vars don't work in Miro iframe!)
import { COLORS } from '@shared/config/boardConfig';

COLORS.primary          // #050038
COLORS.accent           // #2563EB
COLORS.success          // #10B981
COLORS.warning          // #F59E0B
COLORS.error            // #EF4444

// Briefing templates
import { BRIEFING_TEMPLATE } from '@shared/config/boardConfig';
```

---

## Database Synchronization Pattern

### Critical Rule: Database is Source of Truth

```typescript
// ✅ CORRECT: Update database first, then sync to Miro
async function updateProjectStatus(projectId: string, status: ProjectStatus) {
  // 1. Update Supabase
  const { data, error } = await supabase
    .from('projects')
    .update({ status })
    .eq('id', projectId)
    .select()
    .single();

  if (error) throw error;

  // 2. Sync to Miro board
  await projectSyncOrchestrator.syncProjectToBoard(data);
}

// ❌ WRONG: Don't update Miro first
async function updateProjectStatusWrong(projectId: string, status: ProjectStatus) {
  // DON'T DO THIS
  await miroSdkService.updateFrameTitle(frameId, newTitle);
  await supabase.from('projects').update({ status }); // Out of sync!
}
```

### Sync Orchestrator Usage

```typescript
import { projectSyncOrchestrator } from '@features/boards/services/projectSyncOrchestrator';

// Sync single project
await projectSyncOrchestrator.syncProjectToBoard(project);

// Sync all projects on board
await projectSyncOrchestrator.syncAllProjectsToBoard(boardId);

// Handle deletions
await projectSyncOrchestrator.removeProjectFromBoard(projectId);
```

---

## Common Implementation Patterns

### Pattern 1: Creating Board Objects

```typescript
import { miroSdkService } from '@features/boards/services/miroSdkService';
import { LAYOUT, COLORS } from '@shared/config/boardConfig';

// Create frame
const frameId = await miroSdkService.createFrame({
  title: 'Project Workspace',
  x: LAYOUT.frameStartX,
  y: LAYOUT.frameStartY,
  width: LAYOUT.frameWidth,
  height: LAYOUT.frameHeight,
  style: {
    fillColor: COLORS.primary, // Use hex, not CSS variable!
  }
});

// Create sticky note
const stickyId = await miroSdkService.createStickyNote({
  content: 'Logo design',
  x: 100,
  y: 200,
  style: {
    fillColor: COLORS.warning,
  }
});

// Create text
const textId = await miroSdkService.createText({
  content: 'Project Brief',
  x: 300,
  y: 100,
  style: {
    fontSize: 24,
    color: COLORS.primary,
  }
});
```

### Pattern 2: Updating Board Objects

```typescript
// Update frame title
await miroSdkService.updateFrame(frameId, {
  title: 'Updated Title',
});

// Move sticky note
await miroSdkService.updateStickyNote(stickyId, {
  x: 150,
  y: 250,
});

// Update text content
await miroSdkService.updateText(textId, {
  content: 'Updated Brief',
});
```

### Pattern 3: Querying Board Objects

```typescript
// Get all frames on board
const frames = await miroSdkService.getAllFrames();

// Get specific item by ID
const item = await miroSdkService.getItemById(itemId);

// Get items by type
const stickies = await miroSdkService.getItemsByType('sticky_note');
```

### Pattern 4: Using Miro Item Registry

```typescript
import { miroItemRegistry } from '@features/boards/services/miroItemRegistry';

// Track new Miro item
miroItemRegistry.register({
  miroItemId: frameId,
  entityType: 'project',
  entityId: projectId,
});

// Lookup database entity from Miro item
const entity = miroItemRegistry.getEntity(miroItemId);
if (entity?.entityType === 'project') {
  const projectId = entity.entityId;
}

// Remove tracking
miroItemRegistry.unregister(miroItemId);
```

---

## Handling Board Events

### Webhook Processing

Miro board changes trigger webhooks processed by Edge Function:

**File**: `supabase/functions/miro-webhook/index.ts`

```typescript
// Webhook receives events: item:created, item:updated, item:deleted
// Process events and sync back to database if needed

// Example event types:
{
  type: 'item:created',
  data: {
    id: 'miro-item-id',
    type: 'sticky_note',
    // ... other properties
  }
}
```

**Important**: Prevent infinite loops by checking if change originated from sync operation.

---

## CSS Styling for Miro Context

### Critical: CSS Variables Don't Work in Miro Iframe!

```typescript
// ❌ WRONG: CSS variables won't resolve
style: {
  fillColor: 'var(--color-primary)', // Won't work!
}

// ✅ CORRECT: Use explicit hex colors
style: {
  fillColor: '#050038', // Works!
}

// ✅ BETTER: Use constants
import { COLORS } from '@shared/config/boardConfig';
style: {
  fillColor: COLORS.primary, // Resolves to '#050038'
}
```

---

## Entry Points & HTML Files

The app has **4 HTML entry points** (configured in `vite.config.ts`):

1. **index.html** - Main panel entry (sidebar panel)
2. **app.html** - Full app interface (modal or standalone)
3. **board-modal.html** - Modal dialogs opened from board UI
4. **admin-modal.html** - Admin-specific modal dialogs

**When adding Miro features**, ensure proper entry point is configured.

---

## Rate Limiting & Performance

### Miro API Limits

- **Max 25 API calls per second**
- Use batching for bulk operations
- Implement retry logic with exponential backoff

```typescript
// ✅ Batch operations
const items = await Promise.all(
  itemIds.map(id => miroSdkService.getItemById(id))
);

// ❌ Sequential operations in loop (slow + may hit rate limit)
for (const id of itemIds) {
  const item = await miroSdkService.getItemById(id); // DON'T
}
```

---

## Testing in Miro Context

### Availability Checks

```typescript
import { miroAdapter } from '@shared/lib/miroAdapter';

// Gate Miro-specific code
if (!miroAdapter.isAvailable()) {
  logger.warn('Not in Miro context, skipping board operation');
  return null;
}

// Proceed with Miro operations
const board = await miroAdapter.board.get();
```

### Testing Entry Points

Test all 4 HTML entry points:
- Panel view (index.html)
- Full app (app.html)
- Board modal (board-modal.html)
- Admin modal (admin-modal.html)

### Browser Console

Check for SDK errors in browser console:
- Miro SDK initialization errors
- API rate limit warnings
- Item not found errors

---

## Common Pitfalls

### ❌ Don't Trust Miro Item Timestamps

Miro doesn't guarantee accurate timestamps. Use database timestamps as source of truth.

### ❌ Don't Assume Items Exist

Always validate before manipulating:

```typescript
const item = await miroSdkService.getItemById(itemId);
if (!item) {
  logger.error('Item not found', { itemId });
  return;
}
// Now safe to update
await miroSdkService.updateItem(item.id, { ... });
```

### ❌ Don't Create Duplicate Items

Check `miroItemRegistry` before creating:

```typescript
const existing = miroItemRegistry.getByEntity('project', projectId);
if (existing) {
  // Update existing item
  await miroSdkService.updateFrame(existing.miroItemId, { ... });
} else {
  // Create new item
  const frameId = await miroSdkService.createFrame({ ... });
  miroItemRegistry.register({
    miroItemId: frameId,
    entityType: 'project',
    entityId: projectId,
  });
}
```

---

## Role-Based Access

RLS policies enforce access control:

- **Admin**: Full access to all boards
- **Designer**: Access to assigned projects only
- **Client**: Access to own projects only

**Always verify permissions** before Miro operations that expose sensitive data.

---

## Before Making Changes Checklist

- [ ] Read relevant service in `/src/features/boards/services/`
- [ ] Check if similar functionality already exists
- [ ] Understand board layout from constants
- [ ] Verify role-based access requirements
- [ ] Plan database-first sync strategy
- [ ] Use explicit hex colors, not CSS variables
- [ ] Check `miroItemRegistry` for item tracking
- [ ] Test with `miroAdapter.isAvailable()` guards
- [ ] Test all 4 HTML entry points
- [ ] Verify browser console for errors

---

## Useful Context7 Queries

When implementing Miro features, query Context7 for:

```
"Miro SDK v2 create frame with custom style"
"Miro SDK v2 sticky note positioning best practices"
"Miro SDK v2 webhook event handling"
"Miro SDK v2 batch operations rate limits"
"Miro SDK v2 board selection and viewport"
```

---

## Quick Reference

```typescript
// Services
import { miroSdkService } from '@features/boards/services/miroSdkService';
import { masterBoardService } from '@features/boards/services/masterBoardService';
import { projectRowService } from '@features/boards/services/projectRowService';
import { projectSyncOrchestrator } from '@features/boards/services/projectSyncOrchestrator';
import { miroItemRegistry } from '@features/boards/services/miroItemRegistry';

// Safe SDK access
import { miroAdapter } from '@shared/lib/miroAdapter';

// Constants
import { LAYOUT, COLORS, BRIEFING_TEMPLATE } from '@shared/config/boardConfig';

// Logger
import { createLogger } from '@shared/lib/logger';
const logger = createLogger('MiroFeature');
```

---

**Remember**: Database is source of truth. Miro is a visual representation. Always sync from database to Miro, never the reverse.
