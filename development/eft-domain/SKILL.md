---
name: eft-domain
description: >
  Escape from Tarkov game domain knowledge for EFT-Tracker.
  Understands quest structures, traders, Kappa container progression,
  and tarkov.dev API integration.
  Activates when user mentions: quest, trader, Kappa, task, hideout,
  PMC, SCAV, Tarkov, wipe, progression, locked, available, completed.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# EFT Domain Knowledge Skill

## Game Context

**Escape from Tarkov (EFT)** is a hardcore tactical FPS with RPG elements. Players complete quests from traders to unlock gear, gain reputation, and progress toward the **Kappa container** (ultimate goal).

**EFT-Tracker** helps players track quest progress and visualize quest dependencies.

## Quest System

### Quest Status

```typescript
type QuestStatus = "locked" | "available" | "completed";
```

- **locked** - Prerequisites not met (level or quest requirements)
- **available** - Can be started (all prerequisites met)
- **completed** - Already finished

### Quest Types

```typescript
type QuestType =
  | "standard" // Regular trader quests
  | "pvp_zone" // PVP Zone quests (Arena)
  | "reputation" // Fence reputation repair
  | "lightkeeper" // Lightkeeper questline
  | "faction_bear" // BEAR-only quests
  | "faction_usec" // USEC-only quests
  | "story" // Main story quests (1.0)
  | "prestige"; // Prestige quests (require The Collector)
```

### Quest Dependencies

Quests can have prerequisites with different status requirements:

```typescript
type RequirementStatusType = "complete" | "active" | "failed";

// Quest A requires Quest B to be completed
{ requiredQuest: questB, requirementStatus: ["complete"] }

// Quest A requires Quest B to be active OR completed
{ requiredQuest: questB, requirementStatus: ["active", "complete"] }
```

## Traders

| Trader | Specialty | Color |
| ------ | --------- | ----- |
| Prapor | Weapons, ammo | Red |
| Therapist | Medical, food | Purple |
| Fence | Scav items, reputation | Gray |
| Skier | Western weapons | Blue |
| Peacekeeper | NATO weapons, USD | Light Blue |
| Mechanic | Weapon mods | Yellow |
| Ragman | Armor, clothing | Orange |
| Jaeger | Survival, hunting | Green |
| Lightkeeper | Special endgame | Cyan |
| BTR Driver | Convoy quests | Olive |
| Ref | Arena quests | Pink |

## Kappa Container

The **Kappa Secure Container** is the ultimate progression goal:

- Requires completing all "Kappa required" quests
- Quest: "The Collector" unlocks Kappa
- `kappaRequired: boolean` flag on quests indicates if needed for Kappa

### Kappa Progress Tracking

```typescript
// Filter for Kappa-required quests only
const kappaQuests = quests.filter((q) => q.kappaRequired);

// Calculate Kappa progress
const completed = kappaQuests.filter((q) => q.computedStatus === "completed");
const progress = (completed.length / kappaQuests.length) * 100;
```

## Data Structures

### Quest Interface

```typescript
interface Quest {
  id: string;
  title: string;
  wikiLink: string | null;
  levelRequired: number;
  kappaRequired: boolean;
  questType: QuestType;
  factionName: string | null; // "BEAR" | "USEC" | null
  traderId: string;
  trader: Trader;
  objectives: Objective[];
  dependsOn: QuestDependency[];
  dependedOnBy: QuestDependent[];
}
```

### Quest with Progress

```typescript
interface QuestWithProgress extends Quest {
  progress: QuestProgress | null;
  computedStatus: QuestStatus; // Calculated based on dependencies
}
```

## tarkov.dev API

The app syncs quest data from **tarkov.dev** GraphQL API.

### Key Endpoints

```graphql
query {
  tasks {
    id
    name
    wikiLink
    minPlayerLevel
    kappaRequired
    taskRequirements {
      task {
        id
      }
      status
    }
    trader {
      id
      name
    }
  }
}
```

### Data Sync

Quest data is periodically synced and stored in the database. The sync process:

1. Fetches all tasks from tarkov.dev
2. Maps API structure to internal Quest model
3. Updates database with new/changed quests
4. Preserves user progress associations

## Quest Tree Visualization

The quest tree uses **ReactFlow** to visualize dependencies:

- Nodes = Quests (colored by status)
- Edges = Dependencies (arrows show requirement direction)
- Layout = Hierarchical (dagre algorithm)

### Node Colors

```typescript
const statusColors = {
  locked: "gray",
  available: "cyan",
  completed: "green",
};
```

### Focus Mode

Double-click a quest to enter **Focus Mode**:

- Shows only the selected quest and its dependency chain
- Filters out unrelated quests
- ESC exits focus mode

## Common Operations

### Mark Quest Complete

```typescript
await updateQuestProgress({
  questId: quest.id,
  status: "completed",
  completedAt: new Date(),
});
```

### Get Next Available Quests

```typescript
const nextQuests = quests.filter(
  (q) => q.computedStatus === "available" && q.levelRequired <= playerLevel
);
```

### Calculate Dependency Chain

```typescript
function getDependencyChain(quest: Quest): Quest[] {
  const chain: Quest[] = [quest];
  for (const dep of quest.dependsOn) {
    chain.push(...getDependencyChain(dep.requiredQuest));
  }
  return chain;
}
```

## Wipe Cycles

EFT has periodic **wipes** that reset all player progress. The tracker supports:

- Resetting all quest progress for new wipe
- Preserving historical progress (optional)
- Quick-start options for returning players

## Terminology Reference

| Term | Meaning |
| ---- | ------- |
| PMC | Private Military Contractor (main character) |
| SCAV | Scavenger (alternate play mode) |
| Wipe | Server reset of all progress |
| Kappa | Best secure container (5x3 slots) |
| Hideout | Player base for crafting |
| Labs | High-tier locked map |
| FIR | Found In Raid (item status) |
| Fence rep | Scav karma system |

## Files Reference

| File | Purpose |
| ---- | ------- |
| `packages/types/src/quest.ts` | Quest type definitions |
| `packages/types/src/api.ts` | API response types |
| `apps/web/src/app/api/quests/` | Quest API routes |
| `apps/web/src/components/quest-tree/` | ReactFlow visualization |
