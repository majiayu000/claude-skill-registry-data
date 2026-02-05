---
name: world-lifecycle
description: Provides context about how worlds (games) are created, loaded, saved, shared, and fetched in Codako. Use when working on API routes for worlds, the explore page, editor save/load logic, forking, or localStorage handling for anonymous users.
---

# World Lifecycle & Persistence

## When to Use This Skill

Activate this skill when working on:
- API routes for worlds (`api/src/routes/worlds.ts`)
- The World database entity (`api/src/db/entity/world.ts`)
- The Explore page (`frontend/src/components/explore-page.jsx`)
- Editor page load/save logic (`frontend/src/components/editor-page.tsx`)
- World creation, forking, or cloning (`frontend/src/actions/main-actions.tsx`)
- Data migrations for older world formats (`frontend/src/editor/data-migrations.ts`)
- Anonymous user localStorage handling
- API helper functions (`frontend/src/helpers/api.ts`)

## Key Files

| File | Purpose |
|------|---------|
| `api/src/db/entity/world.ts` | World database entity (TypeORM) |
| `api/src/routes/worlds.ts` | All world API endpoints |
| `frontend/src/actions/main-actions.tsx` | World CRUD actions |
| `frontend/src/components/editor-page.tsx` | Editor load/save with adapters |
| `frontend/src/components/explore-page.jsx` | Public worlds listing |
| `frontend/src/editor/data-migrations.ts` | Legacy data format migrations |
| `frontend/src/helpers/api.ts` | HTTP request helper |

## Database Model

```typescript
@Entity({ name: "worlds" })
class World {
  id: number;              // Primary key
  name: string;            // World name (default: "Untitled")
  data: string | null;     // JSON-serialized game state
  thumbnail: string;       // Preview image (base64 or URL)
  playCount: number;       // Incremented on each load
  forkCount: number;       // Incremented when forked
  userId: number;          // Owner's user ID
  forkParentId: number;    // Reference to original (if forked)
  createdAt: Date;
  updatedAt: Date;
}
```

## API Endpoints

### Public Endpoints (No Auth)

| Endpoint | Purpose |
|----------|---------|
| `GET /worlds/explore` | Top 50 worlds by playCount |
| `GET /worlds/:id` | Fetch world + increment playCount |

### Authenticated Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /worlds?user=me` | List current user's worlds |
| `POST /worlds` | Create new world |
| `POST /worlds?from=id` | Clone from existing world |
| `POST /worlds?from=id&fork=true` | Fork (clone + track parent) |
| `PUT /worlds/:id` | Update name, thumbnail, or data |
| `DELETE /worlds/:id` | Delete world |

### Explore Page Query

```typescript
// Returns top 50 worlds sorted by popularity
const worlds = await World.find({
  relations: ["user", "forkParent"],
  order: { playCount: "DESC" },
  take: 50,
});
```

### Create World Logic

```typescript
// POST /worlds?from=<id>&fork=<true>
if (sourceWorld) {
  if (fork) sourceWorld.forkCount += 1;
  newWorld = {
    userId: req.user.id,
    name: sourceWorld.name,
    data: sourceWorld.data,
    thumbnail: sourceWorld.thumbnail,
    forkParentId: fork ? sourceWorld.id : null,
  };
} else {
  newWorld = { userId: req.user.id, name: "Untitled", data: null, thumbnail: "#" };
}
```

## Frontend Architecture

### Two Storage Adapters

The editor uses different adapters based on authentication:

```typescript
const APIAdapter = {
  load: (me, worldId) => GET /worlds/:id,
  save: (me, worldId, json) => PUT /worlds/:id
};

const LocalStorageAdapter = {
  load: (me, worldId) => localStorage.getItem(worldId),
  save: (me, worldId, json) => localStorage.setItem(worldId, JSON.stringify(...))
};

// Selection based on URL
const Adapter = window.location.href.includes("localstorage")
  ? LocalStorageAdapter
  : APIAdapter;
```

### Auto-Save Mechanism

```typescript
const saveWorldSoon = () => {
  if (_saveTimeout.current) clearTimeout(_saveTimeout.current);
  _saveTimeout.current = setTimeout(() => saveWorld(), 5000);
};

// Called on every world change via StoreProvider.onWorldChanged
```

### Before-Unload Protection

```typescript
window.addEventListener("beforeunload", () => {
  if (_saveTimeout.current) {
    saveWorld();
    return "Your changes are still saving...";
  }
});
```

## Anonymous User Flow

### Creating a World (Not Logged In)

```typescript
// 1. Fetch source world (if cloning)
const template = from ? await makeRequest(`/worlds/${from}`) : {};

// 2. Generate localStorage key
const storageKey = `ls-${Date.now()}`;

// 3. Store in localStorage
localStorage.setItem(storageKey, JSON.stringify({...template, id: storageKey}));

// 4. Redirect with localstorage flag
window.location.href = `/editor/${storageKey}?localstorage=true`;
```

### Uploading After Sign-In

```typescript
// 1. Create empty world on server
const created = await POST /worlds

// 2. Upload localStorage data
await PUT /worlds/${created.id} with { name, data, thumbnail }

// 3. Mark localStorage as uploaded (prevents duplicates)
localStorage.setItem(storageKey, JSON.stringify({ uploadedAsId: created.id }));

// 4. Redirect to real world
window.location.href = `/editor/${created.id}`;
```

## Data Migrations

When loading worlds, `applyDataMigrations()` handles legacy formats:

```typescript
// Key transformations:
action.to → action.value                    // Renamed field
action.value: string → { constant: string } // Wrapped in RuleValue
conditions: object → conditions: array[]    // Object to array format
transform: "90deg" → "90"                   // Remove "deg" suffix
transform: "flip-xy" → "180"                // Normalize flip
```

Migrations run automatically on load, allowing old saved worlds to work with current engine.

## Lifecycle Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      EXPLORE PAGE                           │
│  GET /worlds/explore → Top 50 by playCount                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      PLAY/VIEW                              │
│  GET /worlds/:id → playCount++, return full data            │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   CREATE (Logged In)     │    │   CREATE (Anonymous)     │
│   POST /worlds?from&fork │    │   Store in localStorage  │
│   → New DB record        │    │   → ls-{timestamp} key   │
└──────────────────────────┘    └──────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       EDITOR                                │
│  Load: APIAdapter or LocalStorageAdapter                    │
│  Auto-save: PUT /worlds/:id (debounced 5s)                  │
│  Data migrations applied on load                            │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                   UPLOAD (Anonymous → Logged In)            │
│  POST /worlds (create) → PUT /worlds/:id (upload data)      │
│  localStorage marked with uploadedAsId                      │
└─────────────────────────────────────────────────────────────┘
```

## Important Patterns

1. **Play Count Tracking**: Every `GET /worlds/:id` increments `playCount`
2. **Fork Tracking**: Forking increments source's `forkCount` and sets `forkParentId`
3. **Tutorial World**: Special ID "tutorial" maps to `process.env.TUTORIAL_WORLD_ID`
4. **Basic Auth**: All authenticated requests use `Authorization: Basic {base64(user:pass)}`
5. **Debounced Saves**: Editor saves 5 seconds after last change
6. **Upload Deduplication**: localStorage stores `uploadedAsId` to prevent re-uploads
