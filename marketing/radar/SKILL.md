---
name: radar
description: Competitor/industry monitoring feature - track social accounts, detect viral content, analyze trends.
---

# Radar Feature Development

Radar is OpenPromo's competitor monitoring and content discovery tool. It tracks TikTok and Instagram accounts, syncs their content, detects anomalies (viral spikes, outperformers), and helps users discover trending content ideas.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Dashboard UI                            │
│  RadarPage → RadarSourcesPanel, RadarContentFeed, RadarDigest   │
└────────────────────────────┬────────────────────────────────────┘
                             │ orpc
┌────────────────────────────▼────────────────────────────────────┐
│                      Worker (orpc routes)                       │
│                   packages/dash/worker/src/orpc/routes/radar.ts │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     Core Domain Logic                           │
│  packages/core/src/domain/radar/                                │
│  ├── entity/                                                    │
│  │   ├── EntRadarSource.ts      (tracked accounts)              │
│  │   ├── EntRadarContentItem.ts (synced posts)                  │
│  │   ├── EntRadarSavedIdea.ts   (bookmarked content)            │
│  │   └── EntRadarDigest.ts      (AI summaries)                  │
│  ├── radar-sync-service.ts      (fetches & processes content)   │
│  └── radar-digest-service.ts    (generates AI summaries)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     External APIs (TikHub)                      │
│  packages/core/src/providers/tikhub/                            │
│  ├── client.ts         (HTTP client with KV caching)            │
│  ├── tikhub.ts         (unified exports)                        │
│  └── tikhub-tiktok-web.ts (TikTok Web API types)                │
└─────────────────────────────────────────────────────────────────┘
```

## Key Files

### Data Models (Drizzle)
- `packages/core/src/schemas/radar.sql.ts` - Table definitions
  - `radarSourcesTable` - Tracked accounts (TikTok, Instagram)
  - `radarContentItemsTable` - Synced posts/videos
  - `radarSavedIdeasTable` - User bookmarks
  - `radarDigestsTable` - AI-generated summaries

### Entities
- `EntRadarSource` - Add/remove/pause tracked sources, validation
- `EntRadarContentItem` - Store/query synced content, anomaly flags
- `EntRadarSavedIdea` - Save/unsave content as ideas
- `EntRadarDigest` - Generate/store weekly digests

### Services
- `radar-sync-service.ts` - Core sync logic
  - `syncSource(source)` - Fetch posts, detect anomalies, store
  - `syncWorkspace(workspaceId)` - Sync all sources for workspace
  - Anomaly detection: viral_spike (5x avg), outperformer (2x avg)

### API Routes
- `packages/dash/worker/src/orpc/routes/radar.ts`
  - Sources: `addSource`, `listSources`, `removeSource`, `pauseSource`, `resumeSource`
  - Content: `listContent`, `listAnomalies`
  - Ideas: `saveIdea`, `listIdeas`, `unsaveIdea`
  - Digests: `getLatestDigest`, `listDigests`, `generateDigest`
  - Sync: `triggerSync`

### UI Components
- `packages/dash/ui/src/components/radar/`
  - `RadarPage.tsx` - Main page with tabs (Anomalies, All, Saved)
  - `RadarSourcesPanel.tsx` - Grid of tracked source cards
  - `RadarAddSourceForm.tsx` - URL input to add sources
  - `RadarContentFeed.tsx` - Grid of content cards
  - `RadarEmptyState.tsx` - Empty state with onboarding
  - `RadarDigestCard.tsx` - AI digest display
  - `radar-url-parser.ts` - Parse TikTok/IG profile URLs

### Query Hooks
- `packages/dash/ui/src/queries/radar.ts`
  - `useRadarSources`, `useAddRadarSource`, `useRemoveRadarSource`
  - `useRadarContent`, `useRadarAnomalies`
  - `useRadarIdeas`, `useSaveRadarIdea`, `useUnsaveRadarIdea`
  - `useTriggerRadarSync`, `useGenerateRadarDigest`

## TikHub Integration

TikHub provides the social media APIs. API calls are cached in KV (24h TTL).

### TikTok
```typescript
// Get secUid from username (required for fetching posts)
TikHub.TikTokWeb.getSecUid(username)

// Get user profile
TikHub.TikTokWeb.fetchUserInfo({ user_id: secUid })

// Get user posts (returns up to 20)
TikHub.TikTokWeb.fetchUserPosts({ secUid, count: 20 })
```

### Instagram
```typescript
// Get user profile (data nested under data.data)
TikHub.InstagramV2.fetchUserInfo({ username })

// Get user posts (data nested under data.data.items)
TikHub.InstagramV2.fetchUserPosts({ username })
```

**Important**: Instagram API responses are nested under `data.data`, not `data` directly.

## Adding New Source Types

1. Add type to `radarSourceTypePgEnum` in `radar.sql.ts`
2. Add validation method to `TikHubPlatformValidator` in `EntRadarSource.ts`
3. Add fetch method to `TikHubPlatformFetcher` in `radar-sync-service.ts`
4. Update `fetchContent()` switch in sync service
5. Update URL parser in `radar-url-parser.ts`
6. Update UI icons in components

## Anomaly Detection

Content is flagged as anomaly based on views vs baseline:
- **viral_spike**: 5x+ average views (score 0.8-1.0)
- **outperformer**: 2x-5x average views (score 0.3-0.79)

Baseline is calculated from last 20 posts with min 5 posts required.

## Sync Flow

1. User adds source via URL → `EntRadarSource.add()`
   - Validates account exists via TikHub API
   - Extracts profile data (avatar, stats)
   - Stores source with `status: 'active'`
   - Auto-triggers sync for new source

2. Sync runs (manual or cron) → `radarSyncService.syncSource()`
   - Fetches latest posts from platform API
   - Calculates/updates baseline metrics
   - Detects anomalies based on views
   - Upserts content items with anomaly flags
   - Updates `lastSyncedAt` timestamp

## UI Patterns

### Source Cards
```tsx
<SourceCard source={source} />
// Shows: avatar, @username, platform icon, follower count, video count
// Actions: pause/resume, remove (with ConfirmDialog)
```

### Content Cards
```tsx
<RadarContentCard item={item} />
// Uses GridCard building blocks from @/components/common/grid-card
// Shows: thumbnail, metrics (views/likes/comments), anomaly badge
// Actions: Save Idea (hover), Open Original (dropdown)
```

### Add Source Flow
1. User pastes TikTok/IG profile URL
2. URL parsed → preview card shown
3. User clicks "Add Source"
4. Source validated, created, auto-synced

## Common Tasks

### Debug sync issues
```typescript
// Check logs for:
console.log("[radar] syncing source", { sourceId, sourceType, identifier });
console.log("[radar] fetched content", { count });
log.info("instagram posts fetched", { count });
```

### Test API responses
Use labs route or add temp logging in validator/fetcher functions.

### Clear KV cache
```typescript
// Cache keys are prefixed with "tikhub:"
const key = `tikhub:${url}`;
await kv.delete(key);
```

## Route Configuration

Route: `/workspaces/:workspaceSlug/radar`

Search params (zod validated):
```typescript
const radarSearchSchema = z.object({
  tab: z.enum(["anomalies", "all", "saved"]).catch("anomalies"),
});
```
