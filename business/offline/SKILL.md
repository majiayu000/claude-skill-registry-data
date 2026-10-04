---
name: offline
description: Offline-first architecture with local storage, sync, and conflict resolution. Use when adding offline support, data synchronization, local caching, or queue-based sync. Supports fully offline apps and online-first apps with offline fallback.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Offline - Offline-First Architecture

Implement offline-first architecture with local storage, automatic sync, and conflict resolution. Supports multiple patterns from fully offline apps to online-first with offline fallback.

## When to Use This Skill

- Adding offline support to existing features
- Building fully offline-first apps
- Implementing data synchronization
- Adding local caching with sync
- User asks "offline mode", "sync data", "work offline", "cache locally"

## When NOT to Use This Skill

- **Simple in-memory caching** - Use `/data` caching patterns instead
- **Network connectivity detection** - Use `/network-connectivity` instead
- **Error handling for failed requests** - Use `/data` NetworkFailure types

## Questions to Ask

1. **Offline mode:** Fully offline-first or online-first with offline fallback?
2. **Data complexity:** Simple key-value or structured relational data?
3. **Sync strategy:** Periodic sync, on-demand, or push-based?
4. **Conflict resolution:** Last-write-wins, server-wins, or custom merge?
5. **Data sensitivity:** Does local data need encryption?

## Quick Reference

### Offline Patterns

| Pattern | Use When | Local DB | Sync |
|---------|----------|----------|------|
| **Fully Offline** | Notes, journals, todo apps | Primary | Optional upload |
| **Offline-First** | Field apps, travel apps | Primary | Background sync |
| **Online-First + Fallback** | E-commerce, social apps | Cache | On reconnect |
| **Cache-Only** | Read-heavy feeds | TTL cache | Refresh on pull |

### Storage Options

| Storage | Best For | Encryption | Performance |
|---------|----------|------------|-------------|
| **Drift (SQLite)** | Relational data, complex queries | AES-256 via SQLCipher | Fast |
| **Hive** | Key-value, settings, small objects | Built-in AES-256 | Very fast |
| **Isar** | Large datasets, full-text search | Limited | Fastest |
| **SharedPreferences** | Flags, simple settings | None | Fast |
| **SecureStorage** | Tokens, PII | Platform keychain | Slower |

### Sync Strategies

| Strategy | Trigger | Best For |
|----------|---------|----------|
| **Periodic** | Timer (5-15 min) | Background updates |
| **On-Demand** | User pull-to-refresh | User-controlled sync |
| **On-Reconnect** | Connectivity change | Offline queue flush |
| **Push-Based** | FCM/WebSocket | Real-time apps |
| **Delta Sync** | Timestamp-based | Large datasets |

### Conflict Resolution

| Strategy | How It Works | Best For |
|----------|--------------|----------|
| **Last-Write-Wins (LWW)** | Latest timestamp wins | Simple apps, non-critical data |
| **Server-Wins** | Server always authoritative | Multi-user shared data |
| **Client-Wins** | Local changes preserved | Single-user apps |
| **Custom Merge** | Field-level merge logic | Complex business rules |
| **User Prompt** | Ask user to resolve | Important conflicts |

## Workflow

### Phase 1: Analyze Requirements

1. Determine offline pattern (see Quick Reference)
2. Identify data that needs offline access
3. Choose storage solution based on data complexity
4. Define sync strategy and conflict resolution

### Phase 2: Setup Local Storage

1. Add dependencies to `pubspec.yaml`
2. Create local database models/tables
3. Implement local data source

**See:** [storage-guide.md](storage-guide.md) for detailed setup

### Phase 3: Implement Sync Layer

1. Add sync status tracking to models
2. Create sync queue for pending operations
3. Implement sync service with conflict resolution
4. Add background sync via WorkManager (optional)

**See:** [sync-guide.md](sync-guide.md) for sync patterns

### Phase 4: Update Repository

1. Modify repository to read local-first
2. Add write-through or write-behind patterns
3. Handle sync status in domain entities
4. Integrate with connectivity monitoring

### Phase 5: Verify

```bash
dart run .claude/skills/offline/scripts/check.dart --feature {feature}
```

## Core API

```dart
final items = await repository.getAll(); // Local-first read
await repository.create(item);           // Saves locally, queues sync
final isSynced = ref.watch(syncStatusProvider);
```

**See:** [storage-guide.md](storage-guide.md) for dependencies and file structure.

## Guides

| File | Content |
|------|---------|
| [architecture-guide.md](architecture-guide.md) | Offline architecture patterns and decisions |
| [storage-guide.md](storage-guide.md) | Local storage setup (Drift, Hive) |
| [sync-guide.md](sync-guide.md) | Sync strategies and conflict resolution |

## Reference Files

**See:** `reference/` for complete implementations:

- `reference/models/` - SyncStatus enum, SyncOperation, OfflineEntity mixin
- `reference/local_storage/` - Drift database, Hive local source
- `reference/sync/` - SyncQueue, SyncService, ConflictResolver
- `reference/repositories/` - Offline-first and cache-first patterns
- `reference/providers/` - Sync status providers

## Checklist

**Setup:**
- [ ] Offline pattern determined (fully offline vs. online-first + fallback)
- [ ] Storage solution chosen (Drift/Hive) and added to pubspec.yaml
- [ ] Local database/tables created

**Models:**
- [ ] Domain entity has `syncStatus` field
- [ ] DTO model has sync tracking fields (`localId`, `updatedAt`, `isSynced`)
- [ ] Client-generated UUIDs for new entities

**Repository:**
- [ ] Reads from local storage first
- [ ] Writes to local storage immediately
- [ ] Queues remote sync operations
- [ ] Handles sync failures gracefully

**Sync:**
- [ ] Sync queue persists pending operations
- [ ] Sync triggers on connectivity restore
- [ ] Conflict resolution strategy implemented
- [ ] Sync status exposed to UI

**Verification:**
- [ ] Works in airplane mode
- [ ] Data persists across app restarts
- [ ] Sync completes when online
- [ ] Conflicts resolved correctly

## Related Skills

- `/network-connectivity` - Connectivity monitoring and offline banner
- `/data` - Base repository patterns, caching, error handling
- `/push-notifications` - Push-based sync triggers
- `/analytics` - Track sync events and failures

## Common Issues

| Issue | Solution |
|-------|----------|
| Data not persisting | Ensure database initialized before use (`await AppDatabase.init()`) |
| Sync queue grows indefinitely | Implement retry limits and age-based pruning |
| Conflicts overwriting local | Use timestamps for LWW, or user prompts for critical data |
| Slow startup on large datasets | Use pagination, lazy-load details on demand |

**See:** [sync-guide.md](sync-guide.md) for detailed troubleshooting.

## Next Steps

After running this skill:
1. Run `/network-connectivity` for offline banner
2. Run `/testing` for offline scenario tests
3. Run `/i18n` for sync status messages
4. Consider `/push-notifications` for push-based sync
