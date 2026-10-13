---
name: time-bomb-radar
description: 'Finds deferred operations that crash on aged data -- code that passes every test but breaks weeks or months after release. Covers cascade deletes, cache expiry, trial paths, background accumulation, date-threshold transitions, and scheduled side effects. Triggers: "time bomb", "time-bomb", "/time-bomb-radar", "aged data", "deferred deletion".'
version: 2.2.0  # +Pattern 7 cascade delete with live child references (was 2.1.0)
author: Terry Nyberg
license: Apache-2.0
allowed-tools: [Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion]
inherits: radar-suite-core.md
metadata:
  tier: execution
  category: analysis
---

# Time Bomb Radar

> Finds code that works today but crashes after the data gets old enough.

Time bombs are deferred operations that pass every test, every code review, every pattern matcher, then crash your app weeks or months after release. The trigger is **data age + environment state**, not code paths. They produce 1-star reviews from your most loyal users -- the ones who kept the app long enough for the timer to fire.

**Origin:** A production-class crash where `SafeDeletionManager` archived items for 30 days, then cascade-deleted them, triggering a SwiftData `_FullFutureBackingData` fatal error on unresolved iCloud `.externalStorage` faults. The bug was invisible during development because no test data was 30 days old. If shipped, every user would have crashed on day 31.

## Quick commands

| Command | What it does |
|---------|-------------|
| `/time-bomb-radar` | Full audit across all 7 patterns |
| `/time-bomb-radar deferred-deletes` | Pattern 1 only -- cascade deletes on aged data |
| `/time-bomb-radar cache-expiry` | Pattern 2 only -- cache purge with model relationships |
| `/time-bomb-radar trial-expiry` | Pattern 3 only -- subscription/trial expiry paths |
| `/time-bomb-radar background-tasks` | Pattern 4 only -- accumulated background work |
| `/time-bomb-radar date-transitions` | Pattern 5 only -- date-threshold state changes |
| `/time-bomb-radar scheduled-side-effects` | Pattern 6 only -- notifications/reminders scheduled from aged data |
| `/time-bomb-radar cascade-live-refs` | Pattern 7 only -- cascade delete with live child references |
| `--show-suppressed` | Show findings suppressed by known-intentional entries (see § Intentional Suppression Flags) |
| `--accept-intentional` | Mark current finding as known-intentional (see § Intentional Suppression Flags) |

### Intentional Suppression Flags

Both flags wrap the protocol in `radar-suite-core.md § Known-Intentional Suppression`, which owns the canonical spec for `.radar-suite/known-intentional.yaml` (file format, fields, matching rules).

| Flag | Behavior |
|------|----------|
| `--show-suppressed` | After the scan completes, list every finding that was suppressed by a matching entry in `.radar-suite/known-intentional.yaml` this session. Output includes the finding (file:line + pattern), the suppression entry that matched, and the date the entry was added. Read-only — does not modify the suppression file. |
| `--accept-intentional` | Interactive flow that appends a new entry to `.radar-suite/known-intentional.yaml` for the most recently presented finding in the current conversation. Asks via `AskUserQuestion` to confirm the file:line + pattern_fingerprint + reason text before writing. Requires the conversation to contain at least one finding emitted by this skill (refuses with "No recent finding to accept" otherwise). |

Future scans (this session or later) will silently skip findings matching accepted entries and increment the `intentional_suppressed` counter per § Pre-Scan Startup.

## Shared Patterns

See `radar-suite-core.md` for: Tier System, Pipeline UX Enhancements, Table Format, Progress Banner, Issue Rating Tables, Handoff YAML schema, Known-Intentional Suppression, Pattern Reintroduction Detection, Experience-Level Output Rules, Session Persistence, short_title requirement.

## Key concepts

These concepts appear throughout the 7 patterns. Understanding them makes the patterns easier to apply regardless of framework.

### Lazy loading and faults

Most ORMs don't load related objects until you access them. A `User` object with 50 photos doesn't load those photos into memory just because you fetched the user. Instead, the photos are represented as **faults** -- lightweight placeholders that get filled in when you access them.

This is efficient for normal use. It becomes dangerous when:
- The real data is stored remotely (cloud sync, external storage) and hasn't been downloaded
- The object is being deleted and the ORM tries to resolve all its faults to track the cascade
- The app has been idle for weeks and the local cache has been evicted

**In SwiftData:** Faults are `_FullFutureBackingData<T>` objects. Accessing them triggers resolution. If resolution fails (data not available), it's a `fatalError` -- not a throwing error. You cannot catch it.

**In Core Data:** Faults are `NSManagedObject` subclasses with `isFault == true`. Accessing a property triggers resolution. If the store is unavailable, you get `NSObjectInaccessibleException`.

**In Django/SQLAlchemy/ActiveRecord:** Lazy-loaded relationships raise database errors if the connection is lost or the row was deleted. The ORM equivalent of "this object doesn't exist anymore."

**In any ORM with cloud sync:** The object exists in the schema but the data hasn't been synced to this device. The fault resolution goes to the network, which may be unavailable.

### Cascade deletes

When you delete a parent object, the ORM can automatically delete its children. This is configured via delete rules (`.cascade` in SwiftData/Core Data, `on_delete=CASCADE` in Django, `dependent: :destroy` in Rails).

The problem: cascade deletion forces the ORM to **find and visit every child** before deleting them. If any child is a fault whose data isn't locally available, the visit fails.

Object-level cascade delete: ORM loads each child into memory, snapshots it for change tracking, then deletes it. Triggers fault resolution. **Dangerous on aged data.**

Batch/SQL-level delete: ORM issues `DELETE FROM children WHERE parent_id = ?` directly. Never loads objects. Never triggers faults. **Safe on aged data.**

### External storage

Some ORMs store large binary data (photos, PDFs, audio) outside the main database file. SwiftData uses `.externalStorage` to put `Data` properties on disk instead of inline in SQLite. Core Data has "Allows External Storage" in the model editor. Other frameworks use file references.

External storage is the highest-risk target for time bombs because:
- The file may not be downloaded from the cloud yet
- The file may have been evicted from the local cache
- The ORM may not distinguish between "file not downloaded yet" and "file doesn't exist"

## Why testing misses these

- No test data is 30 days old
- Simulators/emulators have perfect local data (no cloud sync delays)
- Unit tests use in-memory stores (no external storage faults)
- CI runs on fresh environments every time
- The developer's device has good Wi-Fi and fully synced data

To catch a time bomb manually, you'd need to: create data, archive it, set your device clock forward 30-90 days, disconnect from the network, and relaunch. Nobody does this.

## Skill Introduction (MANDATORY — run before scanning)

**This section replaces `radar-suite-core.md § Session Setup` for the time-bomb-radar entry point.** Do NOT also run core's 4-question Session Setup — its questions are consolidated below. On first invocation, ask all setup questions in a single `AskUserQuestion` call:

**Question 1: "What's your experience level with Swift/SwiftUI?"**
- **Beginner** — New to Swift. Plain language, analogies, define terms on first use.
- **Intermediate** — Comfortable with SwiftUI basics. Standard terms, explain non-obvious patterns.
- **Experienced (Recommended)** — Fluent with SwiftUI. Concise findings, no definitions.
- **Senior/Expert** — Deep expertise. Terse, file:line only, skip explanations.

**Question 2: "Table format?"**
- **Full tables (Recommended)** — full Issue Rating Tables
- **Compact tables** — 3-column with details below

**Question 3: "Would you like a brief explanation of what this skill does?"**
- **No, let's go (Recommended)** — Skip explanation, proceed to scan.
- **Yes, explain it** — Show one of the explanations below adapted to experience level, then proceed.

Store as: `USER_EXPERIENCE`, `TABLE_FORMAT`. Apply to ALL output for the session, per `radar-suite-core.md § Experience-Level Output Rules`. Also persist to `.radar-suite/session-prefs.yaml` per `radar-suite-core.md § Session Persistence`.

**Note on fix mode:** Time-bomb-radar is a read-only audit skill — it identifies bombs and writes them to the handoff/ledger, but does NOT apply fixes directly. The capstone-radar and roundtrip-radar skills consume time-bomb findings and drive the fix work. So no FIX_MODE question is asked here; the `allowed-tools` list includes Edit/Write only for handoff/ledger persistence, not for source modification.

**Experience-adapted explanations for Time Bomb Radar:**

- **Beginner**: "I'll search your codebase for operations that fire after a time delay — deletions, cache purges, trial expirations, background tasks, and date-based state changes. For each one, I check whether it can crash on data that's been sitting idle for weeks or months with incomplete cloud sync. Think of it like asking: 'If this code runs 90 days after the data was created, on a phone with bad Wi-Fi, what breaks?' Bugs found this way don't show up in tests — they only appear in production, weeks after release, on your most loyal users' devices."
- **Intermediate**: "Time-bomb-radar audits deferred operations that pass tests but fail on aged data with incomplete sync. Covers 7 patterns: cascade deletes (1), cache expiry (2), trial expiry (3), background task accumulation (4), date-threshold transitions (5), scheduled side effects (6), and cascade delete with live child references (7). Outputs BOMB/Risky/Safe ratings with grep evidence and file:line citations."
- **Experienced**: "Time bomb audit across 7 patterns: deferred cascade deletes, cache expiry with model relationships, trial/subscription expiry paths, background task accumulation, date-threshold state transitions, scheduled side effects from aged data, and cascade delete with live child references. Outputs rated findings with grep evidence."
- **Senior/Expert**: "7-pattern aged-data audit. BOMB/Risky/Safe + grep evidence + file:line."

**User impact explanations:** Can be toggled at any time with `--explain` / `--no-explain`. When enabled, each finding gets a 3-line companion explanation (what's wrong, fix, user experience before/after). See `radar-suite-core.md` for format and rules. Store as `EXPLAIN_FINDINGS` (default: false).

**Experience-level auto-apply (time-bomb-radar local):** If `USER_EXPERIENCE` = Beginner, auto-set `EXPLAIN_FINDINGS = true` and default sort to `impact`. If Senior/Expert, default sort to `effort`. Apply all output rules from `radar-suite-core.md § Experience-Level Output Rules`.

## Pre-Scan Startup (MANDATORY — before any pattern scan)

1. **Known-intentional suppression:** Run the protocol in `radar-suite-core.md § Known-Intentional Suppression`. Core owns this — do not restate the steps here.

2. **Pattern reintroduction detection:** Run the protocol in `radar-suite-core.md § Pattern Reintroduction Detection`. Core owns this.

## Step 0: Codebase scan

Before checking individual patterns, collect baseline information:

### Swift/Apple projects

1. **Persistence framework**: SwiftData, Core Data, GRDB, Realm, or plain files?
2. **Cloud sync**: iCloud/CloudKit, Firebase, custom backend, or local-only?
3. **External storage**: Any `.externalStorage` attributes or large binary data stored outside the main database?
4. **Subscription/trial system**: StoreKit, RevenueCat, custom, or none?

```
Grep pattern="@Model|NSManagedObject|@Table" glob="**/*.swift" output_mode="files_with_matches"
Grep pattern="\.externalStorage|Allows External Storage" glob="**/*.swift" output_mode="content"
Grep pattern="cloudKit|CKContainer|iCloud|FirebaseFirestore" glob="**/*.swift" output_mode="files_with_matches"
Grep pattern="StoreKit|SubscriptionManager|TrialManager|RevenueCat" glob="**/*.swift" output_mode="files_with_matches"
```

### Other frameworks (Django, Rails, Node, etc.)

```
Grep pattern="on_delete.*CASCADE|dependent.*destroy|CASCADE" glob="**/*.{py,rb,ts,js}" output_mode="content"
Grep pattern="expires_at|ttl|max_age|cache_expiry" glob="**/*.{py,rb,ts,js}" output_mode="content"
Grep pattern="trial|subscription.*expir|free_tier" glob="**/*.{py,rb,ts,js}" output_mode="content"
Grep pattern="cron|scheduler|background_job|sidekiq|celery|delayed_job" glob="**/*.{py,rb,ts,js,yaml,yml}" output_mode="files_with_matches"
```

### Output

```
Persistence: [framework]
Cloud sync: [yes/no, which service]
External storage: [list of models/properties]
Subscription system: [yes/no, which framework]
```

### Pattern Relevance Matrix

Use the Step 0 output to decide which patterns to run. Pattern 1 always applies if there's any persistence framework; the rest scale with the codebase's characteristics.

| Codebase characteristic | Patterns to run |
|---|---|
| Any persistence framework (always) | 1, 4 |
| Has cache layer with TTL or expires_at | + 2 |
| Has freemium/trial/subscription system | + 3 |
| Has date-based state transitions (warranties, loans, password expiry, etc.) | + 5 |
| Schedules notifications, reminders, calendar events, or emails | + 6 |
| Swift + SwiftData/Core Data + SwiftUI with `.cascade` delete rules and views holding child refs | + 7 |

A full audit (`/time-bomb-radar` with no arguments) runs all patterns whose characteristic matches the Step 0 output and skips the rest. The skill announces which patterns were skipped and why in the opening banner so the user can override with a per-pattern command if needed.

---

## Pattern 1: Deferred deletion with cascade relationships

**The general problem:** Code that soft-deletes objects (archive, trash, recycle bin), then permanently deletes them after a time threshold. The permanent delete triggers cascade rules that try to visit related objects. If those objects have remote or externally stored data that isn't locally available, the visit fails.

This is the most dangerous pattern because the crash is usually uncatchable. The ORM hits a fatal error during internal bookkeeping (snapshot creation, change tracking), not during your code.

**Severity:** CRITICAL when cascade targets include external storage or cloud-synced data.

### How to find them (Swift)

```
Grep pattern="byAdding.*day.*value.*-|byAdding.*month.*value.*-" glob="**/*.swift" output_mode="content"
```

For each hit, check if the same file or calling chain includes:
```
Grep pattern="\.delete|context\.delete|modelContext\.delete|remove|purge|cleanup" path="[file from above]" output_mode="content"
```

### How to find them (other frameworks)

```
# Python/Django
Grep pattern="timedelta.*days|datetime.*now.*-" glob="**/*.py" output_mode="content"
# Then check same files for .delete(), bulk_delete, QuerySet.delete()

# Ruby/Rails
Grep pattern="ago|days\.ago|months\.ago" glob="**/*.rb" output_mode="content"
# Then check same files for destroy, destroy_all, delete, delete_all

# Node/TypeScript
Grep pattern="Date\.now.*-|subtract.*days|moment.*subtract" glob="**/*.{ts,js}" output_mode="content"
# Then check same files for .remove(), .delete(), .destroy()
```

### What to verify for each hit

**Enumerate-then-verify:** Don't stop at "does it have cascade targets with external storage?" Enumerate ALL cascade children, then check each one. The bug hides in the gap between what was handled and what exists.

1. **Enumerate:** List every cascade relationship from the parent model. Include grandchildren (e.g., Parent -> Child -> Grandchild where both relationships are cascade).
2. **Check external storage:** For each child/grandchild, check if it has `.externalStorage` (SwiftData), `Allows External Storage` (Core Data), or file references (other ORMs).
3. **Check coverage:** For each child/grandchild, check if it's covered by a batch delete in the deletion code. The finding is in the gap between what exists in the model and what's covered by batch deletes.
4. **Check sync:** Do the cascade targets sync with a cloud service?
5. **Check delete method:** Is the deletion done via batch/SQL-level delete or object-level delete?

**Common miss:** Existing code already handles the obvious case (e.g., photos) with comments explaining why. A human reading that assumes "they handled it." The skill must verify completeness -- enumerate all children, not just confirm the documented ones.

### Classification

| Delete method | Cascade target | Rating |
|---|---|---|
| Batch/SQL-level delete | Any | Safe |
| Object-level delete | No cascade | Safe |
| Object-level delete | Cascade to normal properties | Risky |
| Object-level delete | Cascade to external storage or cloud-synced data | BOMB |

### Swift-specific details

**Safe:** `context.delete(model: T.self, where:)` operates at the SQL level. Never materializes objects. Never triggers faults.

**Unsafe:** `context.delete(object)` with `.cascade` rule. Forces materialization of all related objects via `ModelSnapshot` creation. If any child has `_FullFutureBackingData` (unresolved iCloud `.externalStorage`), it's a fatal error.

**Fix:** Two-phase batch delete. Delete children first (by predicate), then delete parents. Requires stored properties used in predicates to be `internal` (not `private`).

```swift
// Phase 1: Batch-delete child objects (SQL-level, no materialization)
let childPredicate = #Predicate<ChildModel> {
    $0.parent?.statusRaw == "archived"
}
try? context.delete(model: ChildModel.self, where: childPredicate)

// Phase 2: Batch-delete parent objects (cascade is now a no-op)
let parentPredicate = #Predicate<ParentModel> {
    $0.statusRaw == "archived"
}
try? context.delete(model: ParentModel.self, where: parentPredicate)
```

### Django-specific details

**Safe:** `MyModel.objects.filter(archived_before=threshold).delete()` uses SQL-level CASCADE. No object loading if no signals/overrides.

**Unsafe:** Looping with `obj.delete()` when `pre_delete`/`post_delete` signals access related objects that may have been deleted by another process or have stale foreign keys.

**Additional risk:** Django's `on_delete=CASCADE` at the database level is safe, but Python-level cascade (`on_delete=models.CASCADE` with signal handlers) loads objects.

---

## Pattern 2: Cache expiry with model relationships

**The general problem:** Cache entries (API responses, OCR results, AI outputs, thumbnails) with a TTL that expire after N days. The cache works fine for fresh entries. When the purge runs on old entries, it may trigger relationship resolution or external data access on stale objects.

This is Pattern 1 in disguise, with a different trigger (TTL vs archive age) and often a different location in the codebase (cache managers vs deletion managers).

### How to find them (Swift)

```
Grep pattern="cacheExpiry|expiresAt|isExpired|ttl|maxAge|cacheExpiryDays" glob="**/*.swift" output_mode="content"
```

Exclude warranty/coverage/subscription business logic (those are Pattern 5).

### How to find them (other frameworks)

```
Grep pattern="expires_at|ttl|max_age|cache_timeout|CACHE_TTL" glob="**/*.{py,rb,ts,js,yaml}" output_mode="content"
Grep pattern="redis.*expire|memcache.*expir|cache\.delete" glob="**/*.{py,rb,ts,js}" output_mode="content"
```

### What to verify for each hit

1. Is the cache entry a persisted model or an external store (Redis, Memcached, files)?
2. Does it have relationships to other models?
3. How is the purge done -- batch delete or object-level loop?
4. Does the cache store binary data externally?

**Check ALL delete paths, not just expiry:** Once you find a cache model with `.externalStorage`, check every method that deletes instances of that model -- not just the TTL-triggered purge. User-triggered operations like "Clear Cache" and "Clear Cache for Item" have the same `.externalStorage` crash risk. The trigger is different (user action vs timer) but the fault resolution crash is identical.

### Classification

| Cache storage | Relationships | Purge method | Rating |
|---|---|---|---|
| UserDefaults, files, Redis, Memcached | N/A | Any | Safe |
| `@Model` / ORM model, no relationships | N/A | Any | Safe |
| `@Model` / ORM model, has relationships | N/A | Batch | Safe |
| `@Model` / ORM model, has relationships | N/A | Object-level | Risky |
| `@Model` / ORM model, `.externalStorage` | N/A | Object-level | BOMB |

---

## Pattern 3: Trial and subscription expiry paths

**The general problem:** Features gated behind a time-limited trial or subscription. The risk isn't the paywall UI. It's what happens to in-flight operations, initialized sessions, and cached permissions when the authorization state changes after weeks of being valid.

This pattern exists in every app with a freemium model, regardless of platform. The specific risk varies:
- **Mobile apps:** StoreKit/Google Play billing not initialized because the feature was always available during development
- **SaaS:** API keys or JWT tokens issued during trial that aren't invalidated on expiry
- **Desktop apps:** License files checked on startup but not re-validated during long-running sessions

### How to find them (Swift)

```
Grep pattern="daysRemaining|trialEnd|subscriptionExpir|canUse|isSubscribed|queriesRemaining" glob="**/*.swift" output_mode="content"
```

### How to find them (other frameworks)

```
Grep pattern="trial_end|subscription_expir|is_subscribed|can_use_feature|free_tier" glob="**/*.{py,rb,ts,js}" output_mode="content"
Grep pattern="billing.*check|license.*valid|entitlement" glob="**/*.{py,rb,ts,js}" output_mode="content"
```

### What to verify for each hit

1. **Session initialization:** Is the feature's session/manager initialized with trial-era permissions? Does it handle the transition to expired state mid-session?
2. **UI fallback:** When the trial expires, does the UI show a working paywall? Or does it show a broken state because the purchase system (StoreKit, Stripe, Google Play) wasn't initialized since the feature was always available?
3. **Data access:** Can the user still read data they created during the trial? Or does the expiry gate lock them out of their own content?
4. **Edge case:** What if the trial expires while the app is in the background/inactive, and the user returns to a view that assumes trial access?

### Classification

| Behavior on expiry | Rating |
|---|---|
| Gate checks at view/route level with graceful fallback | Safe |
| User can still read their own data (read-only) | Safe |
| Feature session assumes trial is active, no expiry handling | Risky |
| User loses access to data they created during trial | BOMB |
| Purchase/subscribe button broken because billing not initialized | BOMB |

### How to test

Set the device date (or server clock) forward past the trial end date. Launch the app. Verify:
- Paywall/upgrade prompt appears and the purchase flow works
- Previously created data is still accessible (read-only at minimum)
- No crashes from expired session objects or revoked permissions

---

## Pattern 4: Background task accumulation

**The general problem:** Background tasks (thumbnail generation, sync reconciliation, data cleanup, analytics upload, email queues) that process accumulated items. They work fine on 5 items. After weeks of the app (or service) being idle, they wake up to hundreds or thousands.

This affects every platform:
- **iOS:** `BGTaskScheduler` tasks with 30-second execution limits
- **Android:** `WorkManager` jobs with battery-aware scheduling
- **Server:** Cron jobs, Sidekiq/Celery workers, Lambda functions triggered by queue depth
- **Desktop:** LaunchAgent/scheduled tasks that process accumulated local data

### How to find them (Swift)

```
Grep pattern="BGTaskScheduler|scheduleCleanup|scheduleOnLaunch|performAfter|backgroundTask" glob="**/*.swift" output_mode="content"
```

### How to find them (other frameworks)

```
Grep pattern="cron|scheduler|background_job|sidekiq|celery|delayed_job|bull|agenda" glob="**/*.{py,rb,ts,js,yaml,yml}" output_mode="files_with_matches"
Grep pattern="WorkManager|JobScheduler|AlarmManager" glob="**/*.{kt,java}" output_mode="files_with_matches"
```

### What to verify for each hit

1. **Batch limit:** Is there an upper bound on items processed per run? (e.g., `.prefix(50)`, `LIMIT 100`)
2. **Memory management:** Does it process in chunks with saves/commits between them, or load everything at once?
3. **Timeout handling:** Background tasks have limited execution time on mobile. Server jobs have timeouts. What happens if the task is killed mid-batch?
4. **Stale data:** After weeks idle, do the items being processed still have valid relationships? Could related objects have been deleted on another device or by another process?
5. **Partial failure:** If item 23 of 100 fails, does it skip and continue, or abort the whole batch?
6. **External storage reads:** Does the task access `.externalStorage` properties (or equivalent) on the objects it processes? Reading `.externalStorage` triggers the same fault resolution as deleting -- if the data hasn't synced from iCloud, accessing it in a filter, map, or property check is a `fatalError`. Use predicates to filter at the SQL level instead of fetching objects and checking properties in Swift/Python/Ruby.

### Classification

| Behavior | Rating |
|---|---|
| Batch-limited, chunked processing, handles partial failure | Safe |
| No batch limit but lightweight per-item work (no I/O) | Risky (memory) |
| No batch limit, materializes relationships or does I/O per item | BOMB (memory + faults) |
| No timeout handling, can be killed mid-batch with unsaved state | Risky (data corruption) |

### Swift-specific fix

```swift
let items = fetchEligibleItems()
for chunk in items.prefix(100).chunks(ofCount: 20) {
    for item in chunk {
        process(item)
    }
    try context.save() // Save after each chunk
}
```

---

## Pattern 5: Date-threshold state transitions

**The general problem:** Objects that change state based on date arithmetic. Warranties expiring, loans becoming overdue, subscriptions lapsing, items aging into a different category, passwords expiring, tokens rotating. The transition code runs when the object is next accessed, which could be months later.

The risk: the code that computes the new state assumes the object is fully loaded and its relationships are intact. After months, optional fields may be nil from migration gaps, relationships may have been pruned by cloud sync, or the object may have been deleted on another device.

### How to find them (Swift)

```
Grep pattern="byAdding.*day|byAdding.*month" glob="**/*.swift" output_mode="content"
```

Filter to hits that also involve state changes:
```
Grep pattern="lifecyclePhase|\.status|isExpired|isOverdue|isDueSoon" glob="**/*.swift" output_mode="content"
```

### How to find them (other frameworks)

```
Grep pattern="timedelta|relativedelta|date_add|DATE_ADD|dateadd" glob="**/*.{py,rb,ts,js,sql}" output_mode="content"
Grep pattern="status.*expir|is_expired|is_overdue|is_stale" glob="**/*.{py,rb,ts,js}" output_mode="content"
```

### What to verify for each hit

1. **Nil/null safety:** After months, optional fields may be nil from migration gaps or incomplete sync. Does the date comparison handle missing dates gracefully?
2. **Deleted references:** The related object (warranty provider, loan recipient, subscription plan) may have been deleted. Does the transition handle a nil/null relationship?
3. **Stale computed properties:** If the state is computed from multiple fields, are all fields guaranteed to be populated after months of inactivity?
4. **Time zone drift:** Does the date comparison account for the user potentially being in a different time zone than when the data was created?

### Classification

| Behavior | Rating |
|---|---|
| Date comparison with nil guards and graceful fallback | Safe |
| Date comparison that force-unwraps or assumes non-nil | Risky |
| State transition that accesses relationships without nil checks | BOMB |

### Swift-specific fix

```swift
// Before (unsafe)
if item.warranty!.expirationDate < Date() { ... }

// After (safe)
guard let warranty = item.warranty,
      let expiration = warranty.expirationDate else { return }
if expiration < Date() { ... }
```

### Worked example: rolling-window counter with no per-incident timestamps

A subtler shape of this pattern: the date threshold *should* shift a counter, but the data model has no way to represent the underlying events, so the threshold can never fire. The counter is correct on day 1 and silently wrong after the window passes.

**Finding (RS-W11 — Monthly AppleCare 24-month rolling window has no per-incident timestamps)**

| # | Finding | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort |
|---|---|---|---|---|---|---|---|
| RS-W11 | Rolling 24-month ADH cap cannot decay because incident dates aren't stored | 🟡 HIGH | ⚪ Low | 🟡 High | 🟠 Excellent | 🟢 2 files | Small (option b) / Large (option a) |

**Why it's a time bomb:** `ItemEnums.swift:1035` declares `AppleCarePlanType.monthlyRolling` ADH cap as `.rolling(months: 24, max: 2)`, but the stored counter `screenRepairsUsed: Int` is a scalar — there's no array of incident dates. `ExtendedWarranty.swift:269-272` already names the gap in a doc comment: *"The rolling-window math is best-effort without per-incident timestamps: the stored \*Used count is treated as in-window. This is honest enough for users on a single Monthly plan; users with multi-year history should be advised that the count is approximate."*

A user on a 5-year-old Monthly plan with 4 historical screen repairs across that span sees *"4 used, 0 remaining"* forever, even though their first two incidents are outside the rolling 24-month window and should have decayed. The doc comment acknowledges this; no UI surfaces the warning to the user.

**Why it passes tests:** Test fixtures use a fresh plan with 0–2 historical incidents. The window never has anything to decay. The bug is invisible until production data accrues a third or fourth incident, which by definition takes months to years.

**Fix:**
- **(a) Large** — Add per-incident timestamps as a new `[IncidentRecord]` array on `ExtendedWarranty` (Bucket A migration: new relationship to a new `@Model`). Have `remainingADH` filter by `Date() - 24 months`.
- **(b) Small** — Surface a UI note for `monthlyRolling` rows: *"Counter does not auto-decay — manually reset when oldest incident is more than 24 months old."* Acknowledges the limitation the doc comment already names.

Option (b) is the smaller fix and ships the warning the code already knows it owes the user. Option (a) is the correct long-term fix; defer it behind a migration spike.

**Cite:** `Sources/Models/ExtendedWarranty.swift:269-291`, `Sources/Models/ItemEnums.swift:1035`.

---

## Pattern 6: Scheduled side effects from aged data

**The general problem:** Code that schedules future side effects (push notifications, calendar events, reminders, emails, webhook triggers) based on date fields in the data model. The scheduling happens when the object is created or updated, but the side effect fires later -- sometimes much later. If the date field is nil from a sync gap, the scheduling produces a wrong or missing result. If the related object has been deleted by the time the side effect fires, the handler crashes or shows garbage.

This is distinct from Pattern 5 (date-threshold state transitions) because the failure mode is different. Pattern 5 produces wrong computed state. Pattern 6 produces wrong or missing real-world actions -- a notification that never fires, a reminder for the wrong date, or a crash in the notification handler when it tries to look up the source object.

**Severity:** Usually Risky (silent failure) rather than BOMB (crash). But notification handlers that force-unwrap the source object are BOMB.

### How to find them (Swift)

```
Grep pattern="UNUserNotificationCenter|UNMutableNotificationContent|UNCalendarNotificationTrigger|UNTimeIntervalNotificationTrigger" glob="**/*.swift" output_mode="files_with_matches"
Grep pattern="EKEvent|EKReminder|EventKit" glob="**/*.swift" output_mode="files_with_matches"
```

For each hit, check what data feeds the scheduling:
```
Grep pattern="byAdding.*day|byAdding.*month|expirationDate|dueDate|returnDate" path="[file from above]" output_mode="content"
```

### How to find them (other frameworks)

```
# Python/Django
Grep pattern="send_mail|celery.*eta|schedule.*send|django_q" glob="**/*.py" output_mode="content"

# Ruby/Rails
Grep pattern="deliver_later|perform_later|notify|ActionMailer" glob="**/*.rb" output_mode="content"

# Node/TypeScript
Grep pattern="setTimeout|agenda\.schedule|bull\.add|cron\.schedule" glob="**/*.{ts,js}" output_mode="content"
```

### What to verify for each hit

1. **Nil date fields:** If the date used to schedule the side effect is nil (from a sync gap, migration, or incomplete data), does the code skip gracefully or schedule for epoch/now/crash?
2. **Deleted source object:** When the notification/reminder fires, can the handler still find the object it references? If the object was deleted (or archived) between scheduling and firing, what happens?
3. **Stale data:** If the date field was updated after the side effect was scheduled, is the old scheduled event cancelled and a new one created? Or does the stale event still fire?
4. **Timezone:** If the user changes timezones between scheduling and firing, does the side effect fire at the right local time?

### Classification

| Behavior | Rating |
|---|---|
| Nil-safe scheduling with guard-let, cancels stale events on update | Safe |
| Schedules from optional date without nil check | Risky (wrong time or missed event) |
| Handler force-unwraps source object on fire | BOMB (crash when object deleted) |
| No cancellation of stale events when source data changes | Risky (duplicate/wrong notifications) |

### Swift-specific fix

```swift
// Before (unsafe -- if expirationDate is nil, crashes or schedules for epoch)
let trigger = UNCalendarNotificationTrigger(
    dateMatching: Calendar.current.dateComponents([.year, .month, .day], from: item.expirationDate!),
    repeats: false
)

// After (safe)
guard let expirationDate = item.expirationDate else { return }
let reminderDate = Calendar.current.date(byAdding: .day, value: -daysBefore, to: expirationDate)
guard let reminderDate else { return }
let trigger = UNCalendarNotificationTrigger(
    dateMatching: Calendar.current.dateComponents([.year, .month, .day], from: reminderDate),
    repeats: false
)
```

---

## Pattern 7: Cascade delete with live child references

**The general problem:** A parent `@Model` object has a `.cascade` delete rule on a relationship. A view or closure elsewhere holds a direct reference to a child object independently of the parent. When the parent is deleted, SwiftData cascade-deletes the child, but the view/closure still holds and accesses the now-deleted child. Accessing properties of a deleted `@Model` crashes at runtime.

This is distinct from Pattern 1 (deferred deletion) because the delete is immediate, not time-delayed. The "bomb" is spatial, not temporal: it depends on which views are active when the delete happens, not on how much time has passed. But it belongs in time-bomb-radar because it shares the same diagnostic shape: an action (delete) whose consequences are invisible at the call site and only manifest when a distant piece of code touches the affected object later.

**Severity:** Usually BOMB (crash) if the child is accessed after deletion. Safe if the view observes the parent and dismisses when the parent is deleted.

### How to find them (Swift)

```
Grep pattern="\.cascade|deleteRule.*cascade" glob="**/*.swift" output_mode="files_with_matches"
```

For each cascade relationship, identify the child type. Then check if any view holds a direct reference to the child type independent of navigating through the parent:

```
Grep pattern="@Query.*ChildType|@Bindable.*ChildType|let.*: ChildType|var.*: ChildType" glob="**/*.swift" output_mode="files_with_matches"
```

### What to verify for each hit

1. **Independent child reference:** Does any view hold the child directly (via `@Query`, `@Bindable`, `let`/`var` parameter, or `@State`) rather than accessing it through `parent.children`?
2. **Active view during delete:** Can the user trigger a parent delete while a view holding the child is still presented? (e.g., detail sheet for child is open, user deletes parent from a list in the background)
3. **Observation of parent lifecycle:** Does the child-holding view observe the parent and dismiss or guard when the parent is deleted?
4. **Navigation stack cleanup:** If the child view is on a navigation stack, does deleting the parent pop the stack back?

### Classification

| Behavior | Rating |
|---|---|
| View holds child independently, no guard on parent deletion | BOMB (crash on access) |
| View holds child independently, but parent delete pops navigation/dismisses sheet | Safe |
| View accesses child only through parent reference (`parent.children`) | Safe (parent nil-check guards access) |
| Child has `.nullify` or `.deny` delete rule (not `.cascade`) | Not applicable to this pattern |

### Swift-specific detail

SwiftData cascade deletes happen synchronously when the parent is deleted in a context. If a SwiftUI view holds an `@Bindable` reference to the child, the view body may re-evaluate after the delete and access properties on a deleted object. The fix is either:
- Dismiss the child view before or upon parent deletion
- Use `@Query` filtered by parent ID (query returns empty when parent is deleted, view shows empty state)
- Access children only through the parent's relationship property

---

## Findings format

For every hit, produce a rated finding:

| # | Pattern | File:Line | Trigger | Risk | Evidence |
|---|---------|-----------|---------|------|----------|
| 1 | Pattern 1: Deferred delete | SafeDeletionManager.swift:89 | 30 days after archive | BOMB | Cascade to PhotoAttachment with .externalStorage |
| 2 | Pattern 2: Cache expiry | OCRCacheManager.swift:235 | 90 days after cache creation | Risky | Object-level purge, no .externalStorage but has relationships |
| 3 | Pattern 3: Trial expiry | AITrialManager.swift:44 | Trial end date | Safe | Gate check at view level with fallback |
| 4 | Pattern 4: Background accumulation | ThumbnailGenerator.swift:152 | First launch after >30 day idle | Risky | No batch limit; loads relationships per item |
| 5 | Pattern 5: Date-threshold transition | ExtendedWarranty.swift:78 | Warranty expiration date | Risky | Force-unwraps `.warranty!.expirationDate` |
| 6 | Pattern 6: Scheduled side effect | NotificationManager.swift:201 | Scheduled reminder fire date | BOMB | Handler force-unwraps deleted source `Item` |
| 7 | Pattern 7: Cascade live-ref | Item.swift:405 | Parent delete while child sheet open | BOMB | Child view holds @Bindable ref, no dismiss guard |

### Rating each finding

| Rating | Meaning |
|--------|---------|
| **BOMB** | Will crash or corrupt data on aged data. Fix before release. |
| **Risky** | May fail under specific conditions (bad network, large accumulation). Test manually. |
| **Safe** | Handles aged data correctly. Document why it's safe. |

### Evidence required for each rating

- **BOMB**: Show the cascade chain or fault path. Identify the external storage property or unguarded relationship access.
- **Risky**: Show the code path and explain the failure condition.
- **Safe**: Show the batch delete call, nil guard, or batch limit that prevents the issue.

A rating without evidence is a guess, not an audit.

### Finding Dependencies and Fingerprints

When creating findings, populate these optional fields where relationships are obvious:

- **`depends_on`/`enables`:** If one finding must be fixed before another (e.g., "fix cascade delete" must happen before "add batch purge for cache"), populate with finding IDs.
- **`pattern_fingerprint`/`grep_pattern`/`exclusion_pattern`:** Time bomb patterns are highly generalizable. Assign fingerprints like `cascade_delete_with_external_storage`, `object_level_purge_with_relationships`, `unbounded_batch_accumulation`.

---

## Post-fix verification

After fixing any BOMB or Risky finding, re-verify before closing it:

1. **Re-enumerate:** For Pattern 1 fixes, re-list all cascade children and confirm every one is covered. A partial fix (e.g., adding DocumentAttachment but missing other children) is still a bug.
2. **Check sibling methods:** For Pattern 2 fixes, confirm all delete methods on the same model were converted, not just the one that was flagged. If `pruneExpired()` was fixed but `clearAll()` still uses object-level delete, the model is still vulnerable.
3. **Build:** Verify the project compiles on all target platforms.
4. **Update handoff:** Mark the finding as `status: fixed` in the handoff YAML with evidence of what was changed.

A fix that covers 9 of 10 cascade children is not a fix. Enumerate again after every change.

---

## Progress banner

After completing each pattern scan, print:

```
---------------------------------------------
TIME BOMB RADAR: Pattern [N]/7 complete
  Scanned: [pattern name]
  Hits: [count]
  Bombs: [count] | Risky: [count] | Safe: [count]
  Next: Pattern [N+1] -- [name]
---------------------------------------------
```

Then `AskUserQuestion` before proceeding to the next pattern.

### Pipeline Mode Behavior (Tier 2/3)

When running inside a Tier 2 or Tier 3 pipeline (detected via `tier` field in `.radar-suite/session-prefs.yaml`):

1. **On skill start:** Emit the pipeline-level progress banner (see `radar-suite-core.md` Pipeline UX Enhancements #1). If this is the first skill in the pipeline OR `experience_level` is Beginner/Intermediate, also emit the audit-only statement.
2. **On skill completion:** Emit a per-skill mini rating table marked "PRELIMINARY" (see Pipeline UX Enhancements #2). Then emit the pipeline-level progress banner showing this skill as complete.
3. **Within-skill pattern banners** (above) are still emitted normally in addition to the pipeline-level banners.

### short_title Requirement (v2.1)

Every finding MUST include a `short_title` field (max 8 words). This is the human-scannable label used in pipeline banners, pre-capstone summaries, and ledger output.

Example: `short_title: "30-day cascade delete crash"`

All finding ID references in output (tables, banners, summaries) use the format: `RS-NNN (short_title)`.

---

## On Completion -- Write Handoff

Write findings to `.radar-suite/time-bomb-radar-handoff.yaml`:

```yaml
source: time-bomb-radar
version: "<SKILL_VERSION>"  # read from frontmatter at write time (currently 2.2.0); keep in sync with VERSION file
date: <ISO 8601>
project: <project name>
build: <build number>
patterns_audited: [1, 2, 3, 4, 5, 6, 7]  # omit any patterns skipped per § Pattern Relevance Matrix

for_roundtrip_radar:
  suspects:
    - workflow: "<affected workflow>"
      finding: "<time bomb description>"
      trigger_condition: "<e.g., 30 days after archive>"
      file: "<path:line>"

for_capstone_radar:
  blockers:
    - finding: "<BOMB description>"
      urgency: "CRITICAL"
      domain: "Time Bomb"
      pattern: "<pattern number and name>"

findings:
  - id: <unique hash>
    pattern: <1-6>
    description: "<plain language>"
    file: "<path>"
    line: <number>
    trigger: "<when it fires>"
    rating: "BOMB|Risky|Safe"
    confidence: "verified|probable|possible"
    status: "open|fixed|deferred|accepted"
    evidence: "<what was checked>"
```

### End-of-Run Directory Cleanup (MANDATORY)

Per the Artifact Lifecycle rules in `radar-suite-core.md`, before returning from this skill:
1. List files in `.radar-suite/` (and `.agents/ui-audit/` or equivalent if used).
2. Move any stale single-use handoffs (`RESUME_PHASE_*.md`, `RESUME_*.md` except `NEXT_STEPS.md`, `*-v[0-9]*.md`) to `.radar-suite/archive/superseded/`.
3. Confirm Class 1 persistent-state files (`ledger.yaml`, `session-prefs.yaml`) are in-place rewrites — not dated or versioned.
4. Confirm Class 2 handoff files are overwrites, not appends.

This prevents `.radar-suite/` from accumulating stale prose artifacts across runs.

### Write to Unified Ledger (MANDATORY)

After writing the handoff YAML, also write findings to `.radar-suite/ledger.yaml` following the Ledger Write Rules in `radar-suite-core.md`:

1. Read existing ledger (or initialize if missing)
2. Record this session (timestamp, skill name, build)
3. For each finding: check for duplicates, assign RS-NNN ID if new, set `impact_category`, compute `file_hash`
4. Write updated ledger

**Impact category mapping for time-bomb-radar findings:**
- BOMB rating → `crash`
- Risky rating with data implications → `data-loss`
- Risky rating with UX implications → `ux-degraded`
- Safe ratings → do not write to ledger (informational only)

## On Startup -- Read Ledger & Handoffs

Check for prior findings that inform this audit:

### Unified Ledger

```
Read .radar-suite/ledger.yaml (if exists) — check for existing findings to avoid duplicates
```

If the ledger contains time-bomb findings, note their RS-NNN IDs. When you find the same issue, update the existing finding instead of creating a new one.

**Regression check:** For any `fixed` findings in the ledger whose `file_hash` no longer matches the current file, flag for re-verification per the Regression Detection protocol in `radar-suite-core.md`.

### Own prior handoff (regression check)

```
Read .radar-suite/time-bomb-radar-handoff.yaml (if exists)
```

If a prior handoff exists, this is a re-run. For each previously-fixed finding:
- Verify the fix is still in place (read the file, confirm batch delete or predicate is present)
- If the fix has been reverted or modified, re-rate and re-report
- Report regression findings separately from new findings

This prevents the skill from rediscovering everything from scratch on every run while also catching regressions.

### Data model radar handoff

```
Read .radar-suite/data-model-radar-handoff.yaml (if exists)
```

Look for:
- Models with `.externalStorage` properties (high-priority targets for Pattern 1)
- Relationship graphs with cascade rules (Pattern 1 candidates)
- Serialization gaps (may indicate fields that aren't fully populated after sync)

---

## Cross-skill handoff

Time bomb findings feed directly into:
- **roundtrip-radar** as suspects for workflow-level testing
- **capstone-radar** as release blockers (any BOMB = no-ship)

Time bomb radar consumes:
- **data-model-radar** handoff for model relationships and external storage properties

---

## End reminder

After every pattern: print progress banner, then `AskUserQuestion`. Never leave a blank prompt.

Any finding rated BOMB is an automatic release blocker. Do not downgrade without evidence that the code path is unreachable.
