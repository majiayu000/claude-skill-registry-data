---
name: filament-performance-lord
description: Lord skill for Filament v5 performance optimization — deferred loading, query optimization, caching, Octane, and real-time patterns.
triggers:
  - filament performance lord
  - filament performance
  - filament slow
  - filament optimize
  - filament query
  - filament octane
  - filament cache
  - filament defer
  - أداء filament
  - تسريع filament
personas:
  - DEV
  - DB
  - SRE
tech_stack:
  - filament-5
  - laravel-13
  - php-8-5
  - mysql-9-7
  - postgresql-19
lord: true

---

# Filament Performance Lord

[OBJ] Optimize Filament v5 admin panels for speed — deferred loading, query optimization, caching, Octane compatibility, and real-time patterns.

[RULES]
1. [CMD] Query Context7 for Filament v5 performance docs. Use `/filament/filament` library ID.
2. [REQ] Deferred Loading: `->deferLoading()` on all relation managers and heavy schemas. Prevents waterfall renders. Measure with `Filament\Telemetry`.
3. [REQ] Query Optimization: Eager load relationships (`->with()`). NEVER N+1 queries. Use `->withCount()` for badge counts. `->deferLoading()` for relation manager tabs.
4. [REQ] Table Performance: `->persistGroupingInSession()` to avoid re-grouping. Cursor pagination for >10k rows (`->cursorPaginate()`). Index all sort columns. NEVER `->get()` without pagination on large tables.
5. [REQ] Caching: Cache computed table columns via `->getStateUsing()` with `Cache::remember()`. Cache navigation via `NavigationManager`. NEVER compute in render loops.
6. [REQ] Octane Compatibility: Register `FlushAuthenticationState`, `FlushSessionState`, `FlushUploadedFiles` listeners. Use `octane.warm` for pre-resolving. Granular flush — NEVER flush entire app state.
7. [REQ] Real-time: Reverb SSE for live updates (NEVER client-side polling). `->deferLoading()` + Reverb push for relation managers. Use `Laravel\Reverb` for WebSocket server.
8. [REQ] Asset Loading: `loadedOnRequest()` for lazy JS. `FilamentAsset::register()` with versioning. NEVER load all assets on every page. Use Vite for production builds.
9. [REQ] Database Indexing: Index all Filament table sort columns. Index foreign keys. Use `EXPLAIN (ANALYZE, BUFFERS)` on PG / `EXPLAIN` on MySQL for slow table queries. Add composite indexes for multi-column sorts.
10. [REQ] Memory: State < 50KB per Livewire component (Redis for larger). Pass scalar IDs (NEVER full models). Use `->deferLoading()` to keep initial render lean.
11. [REQ] CSP: `LIVEWIRE_CSP_SAFE=false` in dev (Filament Alpine `x-init` incompatible with CSP-safe build). `true` in production with strict nonce-based CSP only.
12. [REQ] Profiling: Use `Laravel\Telescope` in dev for query analysis. `Filament\Debugbar` for component render time. NEVER deploy with debug tools enabled.

[WORKFLOWS]
1. Diagnose Slow Panel: Enable Telescope → load panel → identify N+1 queries → add `->with()` → add `->deferLoading()` → re-measure → add indexes if needed.
2. Octane Migration: Install Octane → register flush listeners → test with `octane:reload` → benchmark with `wrk` → tune `octane.warm` → deploy with FrankenPHP or Swoole.
3. Real-time Setup: Install Reverb → configure WebSocket server → add `->deferLoading()` on relation managers → push updates via `Broadcast::event()` → listen in Filament component.
