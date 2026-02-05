---
name: using-anime-service
description: Guides using AnimeService for anime tracking operations. Use when implementing anime status checks, episode tracking, plan-to-watch, or hidden anime features.
---

# Using AnimeService

The AnimeService is the primary business logic layer for all anime management operations.

## Architecture

```
AnimeService (Business Logic)
    ├── EpisodeProgressRepository (Currently watching)
    ├── PlanToWatchRepository (Planned anime)
    ├── HiddenAnimeRepository (Hidden anime)
    └── AnimeStateValidator (Business rules)
```

## Data Models

### AnimeData (Base)

```typescript
interface AnimeData {
    animeId: string;      // Unique identifier
    animeTitle: string;   // Display title
    animeSlug: string;    // URL-friendly identifier
}
```

### EpisodeProgress

```typescript
interface EpisodeProgress extends AnimeData {
    currentEpisode: string;    // Episode identifier
    dateWatched: string;       // ISO timestamp
    totalEpisodes?: number;    // Optional total count
    seasonYear?: number;       // Optional season info
    imageUrl?: string;         // Optional thumbnail
}
```

### PlanToWatch

```typescript
interface PlanToWatch extends AnimeData {
    dateAdded: string;     // ISO timestamp
    plannedFor?: string;   // Optional target date
    priority?: number;     // Optional priority level
    reason?: string;       // Optional reason
}
```

### AnimeStatus

```typescript
interface AnimeStatus {
    isTracked: boolean;           // Currently watching
    isPlanned: boolean;           // Planned to watch
    isHidden: boolean;            // Hidden from view
    progress?: EpisodeProgress;   // Current progress if tracked
    plan?: PlanToWatch;           // Plan details if planned
}
```

### ActionResult

```typescript
interface ActionResult {
    success: boolean;
    error?: string;
}
```

## Usage

```typescript
import { AnimeService } from "@/commons/services";

const animeService = new AnimeService();
```

## Core Methods

### Get Status

```typescript
const status = await animeService.getAnimeStatus("anime-123");

if (status.isTracked) {
    console.log(`Episode: ${status.progress?.currentEpisode}`);
}
if (status.isPlanned) {
    console.log(`Planned on: ${status.plan?.dateAdded}`);
}
if (status.isHidden) {
    console.log("Hidden");
}
```

### Start Tracking

```typescript
const animeData = {
    animeId: "anime-123",
    animeTitle: "My Hero Academia",
    animeSlug: "my-hero-academia",
};

const result = await animeService.startTracking(animeData, "episode-1");

if (result.success) {
    console.log("Started tracking!");
} else {
    console.error(result.error);
}
```

### Update Episode Progress

```typescript
const result = await animeService.updateEpisodeProgress("anime-123", "episode-5");
```

### Stop Tracking

```typescript
const result = await animeService.stopTracking("anime-123");
```

### Plan to Watch

```typescript
// Add to plan
const result = await animeService.addToPlan(animeData);

// Remove from plan
const result = await animeService.removeFromPlan("anime-123");
```

### Hidden Anime

```typescript
// Hide anime (removes from other lists)
const result = await animeService.hideAnime("anime-123");

// Unhide
const result = await animeService.unhideAnime("anime-123");
```

### Get All Data

```typescript
const watching = await animeService.getAllWatchingAnime();  // EpisodeProgress[]
const planned = await animeService.getAllPlannedAnime();    // PlanToWatch[]
const hidden = await animeService.getAllHiddenAnime();      // string[]
```

## Business Rules

1. **Mutual Exclusivity**: Anime cannot be both tracked and planned
2. **Hidden Overrides**: Hidden removes from tracking and planning
3. **Auto Transitions**: Starting tracking removes from plan
4. **Data Validation**: All data validated before operations

## Error Handling Pattern

```typescript
const result = await animeService.startTracking(animeData);

if (!result.success) {
    showErrorToast(result.error);
    return;
}

// Success - update UI
updateWatchingList();
```

## Content Script Integration

```typescript
import { AnimeService } from "@/commons/services";

const animeService = new AnimeService();

async function handleStartWatching(animeData: AnimeData) {
    const result = await animeService.startTracking(animeData);

    if (result.success) {
        showSuccessToast("Started watching!");
    } else {
        showErrorToast(result.error);
    }
}
```

## Vue Component Integration

```typescript
import { AnimeService } from "@/commons/services";
import { ref, onMounted } from "vue";

const animeService = new AnimeService();
const watchingAnime = ref<EpisodeProgress[]>([]);

onMounted(async () => {
    watchingAnime.value = await animeService.getAllWatchingAnime();
});
```

## Testing

```typescript
import { describe, it, expect, beforeEach, vi } from "vitest";
import { AnimeService } from "@/commons/services";

describe("AnimeService", () => {
    let animeService: AnimeService;

    beforeEach(() => {
        vi.clearAllMocks();
        animeService = new AnimeService();
    });

    it("should start tracking anime", async () => {
        const animeData = {
            animeId: "test-123",
            animeTitle: "Test Anime",
            animeSlug: "test-anime",
        };

        const result = await animeService.startTracking(animeData);

        expect(result.success).toBe(true);
    });

    it("should handle errors", async () => {
        (chrome.storage.local.get as any).mockRejectedValue(new Error("Storage error"));

        const result = await animeService.startTracking(animeData);

        expect(result.success).toBe(false);
        expect(result.error).toBeDefined();
    });
});
```

## Quick Reference

| Operation | Method |
|-----------|--------|
| Check status | `getAnimeStatus(id)` |
| Start watching | `startTracking(data, episode?)` |
| Update episode | `updateEpisodeProgress(id, episode)` |
| Stop watching | `stopTracking(id)` |
| Add to plan | `addToPlan(data)` |
| Remove from plan | `removeFromPlan(id)` |
| Hide anime | `hideAnime(id)` |
| Unhide anime | `unhideAnime(id)` |
| Get watching list | `getAllWatchingAnime()` |
| Get planned list | `getAllPlannedAnime()` |
| Get hidden list | `getAllHiddenAnime()` |
