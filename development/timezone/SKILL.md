---
name: timezone
description: REQUIRED for ANY date/time code - prevents timezone bugs by enforcing Mountain Time utilities instead of native Date objects. Use when working with dates, times, timestamps, scheduling, cutoffs, date inputs, or API date serialization.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Mountain Time & Date Handling Skill

## Purpose

Ensure all date/time operations in Sweet Angel Bakery use Mountain Time (America/Boise) consistently to prevent timezone bugs, off-by-one errors, and scheduling issues. The business operates in Mountain Time, and all features must respect this regardless of user location or server environment (Cloudflare Workers run in UTC).

## When to Activate This Skill

**REQUIRED** whenever working with:
- Date/time comparisons or calculations
- Delivery/pickup scheduling
- Active/scheduled content (banners, notifications, product drops)
- Cutoff time validation
- API serialization of dates
- HTML date inputs
- Countdown timers
- Calendar or scheduling features
- Database queries filtering by timestamps
- Any code calling `new Date()` or parsing date strings

## Core Principles

1. **Never use `new Date()` for business logic** - always use `getCurrentMountainTime()`
2. **Never parse ISO dates without timezone context** - use `parseMountainISODate()`
3. **Never serialize dates with `.toISOString().split('T')[0]`** - use `getMountainISODate()`
4. **Always store timestamps in UTC** - use `integer({ mode: "timestamp" })` in schema
5. **Always validate date inputs** - use Zod schemas from `@/schemas/date.schema.ts`
6. **Always label timezone in admin UI** - add "(Mountain Time)" or "(MT)" to labels

## Database Storage Pattern

### ✅ CORRECT: Store UTC, Compare in MT

```typescript
// Schema - store as UTC timestamp
export const contentTable = sqliteTable("content", {
  startDate: integer({ mode: "timestamp" }), // UTC timestamp
  endDate: integer({ mode: "timestamp" }),   // UTC timestamp
});

// Server action - compare in Mountain Time
import { getCurrentMountainTime } from "@/utils/timezone";

const now = getCurrentMountainTime(); // Current MT time as Date object
const active = await db.select()
  .from(contentTable)
  .where(
    and(
      lte(contentTable.startDate, now), // Compares UTC timestamps correctly
      gte(contentTable.endDate, now)
    )
  );
```

**Why this works:**
- Database stores absolute UTC timestamps (portable, no DST issues)
- `getCurrentMountainTime()` returns Date object representing "now" in MT
- JavaScript Date objects internally use UTC timestamps
- Drizzle ORM compares the underlying UTC values correctly

## Critical Patterns

### ✅ Server-Side Date Operations

```typescript
"use server";

import { getCurrentMountainTime, getMountainISODate } from "@/utils/timezone";

/**
 * TIMEZONE: Uses Mountain Time for all date comparisons.
 * Scheduled content activates based on MT time, regardless of user location.
 */
export const myAction = createServerAction()
  .handler(async () => {
    const now = getCurrentMountainTime();

    // For API responses, serialize as ISO string in MT
    return {
      date: getMountainISODate(now), // "YYYY-MM-DD" in MT
      items: activeItems.map(item => ({
        ...item,
        deliveryDate: getMountainISODate(item.deliveryDate),
      })),
    };
  });
```

### ✅ HTML Date Inputs

```typescript
"use client";

import { getMountainISODate } from "@/utils/timezone";

<div className="space-y-2">
  <Label htmlFor="date">Delivery Date (Mountain Time)</Label>
  <Input
    id="date"
    type="date"
    min={getMountainISODate(new Date())}
    value={selectedDate}
    onChange={(e) => setSelectedDate(e.target.value)}
  />
  <p className="text-xs text-muted-foreground">
    Available dates are in Mountain Time
  </p>
</div>
```

### ✅ Client-Side Date Display

```typescript
"use client";

/**
 * Parse ISO date string for display only.
 * Creates Date in browser timezone - acceptable for display purposes.
 *
 * IMPORTANT: Server sends dates via getMountainISODate(), so the calendar
 * date is already correct. This just creates a Date object for formatting.
 *
 * For server-side calculations, use parseMountainISODate() instead.
 */
function parseLocalDate(isoDateString: string): Date {
  const [year, month, day] = isoDateString.split("-").map(Number);
  return new Date(year, month - 1, day);
}

const date = parseLocalDate("2025-11-26"); // From server
const formatted = format(date, "EEEE, MMMM d"); // "Tuesday, November 26"
```

### ✅ Zod Validation

```typescript
import { futureMountainDateSchema } from "@/schemas/date.schema";

const schema = z.object({
  deliveryDate: futureMountainDateSchema, // Validates YYYY-MM-DD, ensures future
  endDateTime: z.coerce.date(), // For datetime-local inputs
});
```

### ✅ Admin UI Best Practices

```typescript
<DialogDescription>
  All dates and times are in Mountain Time (America/Boise).
  Content will activate based on Mountain Time, regardless of user location.
</DialogDescription>

<div className="grid gap-4">
  <div className="space-y-2">
    <Label htmlFor="startDate">Start Date (MT)</Label>
    <Input id="startDate" type="datetime-local" />
  </div>
  <div className="space-y-2">
    <Label htmlFor="endDate">End Date (MT)</Label>
    <Input id="endDate" type="datetime-local" />
  </div>
</div>

<p className="text-sm text-muted-foreground">
  This content will appear to all users when Mountain Time is between the start and end dates.
</p>
```

## Anti-Patterns to Avoid

### ❌ WRONG: Direct Date Construction

```typescript
const now = new Date(); // Uses server timezone (UTC on Cloudflare) or browser timezone
const date = new Date("2025-11-26"); // Parses as UTC midnight = wrong day in MT
```

### ❌ WRONG: UTC Serialization

```typescript
// This converts MT date to UTC, then strips time - causes off-by-one bugs!
deliveryDate: option.deliveryDate.toISOString().split('T')[0]
```

### ❌ WRONG: Browser Timezone Hacks

```typescript
function getIsoDate(date: Date) {
  // DON'T do manual timezone offset calculations
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000)
    .toISOString()
    .split("T")[0];
}
```

### ❌ WRONG: Timezone-Specific Strings in Database

```typescript
// Schema - WRONG
endDate: text(), // "2025-03-15T14:00:00-07:00" - loses DST context

// Schema - CORRECT
endDate: integer({ mode: "timestamp" }), // UTC timestamp
```

## Available Utilities

### Core Functions (`src/utils/timezone.ts`)

| Function | Purpose | Example |
|----------|---------|---------|
| `getCurrentMountainTime()` | Get current time in MT | `const now = getCurrentMountainTime()` |
| `toMountainTime(date)` | Convert any Date to MT | `const mt = toMountainTime(utcDate)` |
| `getMountainISODate(date)` | Get YYYY-MM-DD in MT | `const str = getMountainISODate(new Date())` |
| `parseMountainISODate(str)` | Parse YYYY-MM-DD as MT midnight | `const date = parseMountainISODate("2025-11-26")` |
| `getMountainDayOfWeek(date)` | Get day 0-6 in MT | `const day = getMountainDayOfWeek(date)` |
| `isBeforeMountainCutoff(opts)` | Check cutoff in MT | `const ok = isBeforeMountainCutoff({cutoffDay: 2, cutoffTime: "23:59"})` |
| `formatMountainTime(date, fmt)` | Format display in MT | `formatMountainTime(date, "datetime")` |
| `addDaysMountainTime(date, n)` | Add days handling DST | `const next = addDaysMountainTime(date, 7)` |
| `getNextDayOfWeek(day, from?)` | Next occurrence of weekday | `const thu = getNextDayOfWeek(4)` |

### Validation Schemas (`src/schemas/date.schema.ts`)

| Schema | Purpose |
|--------|---------|
| `mountainISODateSchema` | Validates YYYY-MM-DD format |
| `futureMountainDateSchema` | Validates future dates only |
| `optionalMountainISODateSchema` | Optional date field |
| `MountainISODate` | TypeScript branded type |

## Recent Timezone Overhaul (Nov 2025)

### Critical Bugs Fixed

1. **API Serialization** - Changed `.toISOString().split('T')[0]` → `getMountainISODate()`
   - File: `src/app/(storefront)/_actions/get-fulfillment-options.action.ts`

2. **HTML Date Inputs** - Changed `new Date().toISOString().split('T')[0]` → `getMountainISODate(new Date())`
   - File: `src/app/(admin)/admin/delivery-settings/_components/one-off-date-dialog.tsx`

3. **Import Errors** - Updated date-fns-tz v2 → v3 API
   - Changed `zonedTimeToUtc` → `fromZonedTime`
   - Changed `utcToZonedTime` → `toZonedTime`

4. **Timezone Offset Hacks Removed** - Replaced manual calculations with proper utilities
   - File: `src/app/(admin)/admin/orders/_components/fulfillment-filters.tsx`

5. **Client Parsing Documentation** - Added clear warnings about browser timezone
   - Files: `src/components/fulfillment-method-selector.tsx`, `src/app/(admin)/admin/delivery-settings/_components/one-off-dates-table.tsx`

6. **Validation Schemas Added** - Created Zod schemas for date validation
   - File: `src/schemas/date.schema.ts`

7. **Missing Type Exports** - Added `DeliveryOneOffDate` type
   - File: `src/db/schema.ts`

## Reference Implementation

### Core Files
- `src/utils/timezone.ts` - All timezone utilities (BUSINESS_TIMEZONE = 'America/Boise')
- `src/utils/delivery.ts` - Complex delivery date calculations
- `src/utils/format-date.ts` - Display formatting in MT
- `src/schemas/date.schema.ts` - Zod validation schemas

### Server Actions (Examples)
- `src/app/(storefront)/_actions/get-fulfillment-options.action.ts` - Proper API serialization
- `src/app/(storefront)/_actions/site-content.action.ts` - Active content filtering
- `src/app/(admin)/admin/delivery-settings/_actions/one-off-dates.action.ts` - Date validation

### Client Components (Examples)
- `src/app/(admin)/admin/delivery-settings/_components/one-off-date-dialog.tsx` - HTML date inputs
- `src/components/fulfillment-method-selector.tsx` - Client-side date parsing with docs
- `src/app/(admin)/admin/site-content/_components/notification-form-dialog.tsx` - Admin UI patterns

### Database Schema
- `src/db/schema.ts:643-653` - Home notifications (timestamp pattern)
- `src/db/schema.ts:655-664` - Sales banner (timestamp pattern)
- `src/db/schema.ts:274-295` - Delivery closures & one-off dates (date string pattern)

## Testing Checklist

When implementing or modifying date/time features:

- [ ] Import `getCurrentMountainTime` from `@/utils/timezone`
- [ ] Use MT utilities for all server-side date comparisons
- [ ] Store timestamps as UTC (`integer({ mode: "timestamp" })`)
- [ ] Serialize API responses with `getMountainISODate()`
- [ ] Use MT utilities for HTML date input min/max values
- [ ] Validate inputs with Zod schemas from `@/schemas/date.schema.ts`
- [ ] Add timezone labels to admin UI ("Mountain Time" or "MT")
- [ ] Add timezone comments to time-sensitive code
- [ ] Document client-side parsing with timezone warnings
- [ ] Test at 11:59 PM MT (next day in UTC) for off-by-one bugs
- [ ] Test during DST transitions (March/November)
- [ ] Test with delivery cutoff times
- [ ] Test with users in different timezones (verify consistency)

## Decision Framework

Ask yourself: **"Would this work correctly if a user in Tokyo at 3 AM was viewing content scheduled for 'today' in Mountain Time?"**

If the answer is **no**, you need to use Mountain Time utilities.

## Code Comments Template

```typescript
/**
 * TIMEZONE: Uses Mountain Time (America/Boise) for all date operations.
 * Admin sets dates in MT, backend stores as UTC timestamps,
 * comparisons/calculations use getCurrentMountainTime().
 */
```

## Common Bug Scenarios

1. **Off-by-one bug at night** - User sees wrong delivery date at 11 PM MT
   - Cause: `.toISOString().split('T')[0]` converts to UTC first
   - Fix: Use `getMountainISODate()`

2. **Cutoff time calculation wrong** - Orders placed before cutoff are rejected
   - Cause: Using `new Date()` instead of `getCurrentMountainTime()`
   - Fix: Import and use `getCurrentMountainTime()`

3. **Content shows/hides at wrong time** - Banner appears 7 hours early/late
   - Cause: Database comparison using `new Date()` (UTC on Cloudflare)
   - Fix: Use `getCurrentMountainTime()` in query

4. **Date picker shows yesterday** - HTML input min date is off by one
   - Cause: `new Date().toISOString().split('T')[0]` in `min` attribute
   - Fix: Use `getMountainISODate(new Date())`

## Summary

The bakery operates in Mountain Time. **Every date/time operation must use Mountain Time utilities** to ensure consistent, predictable behavior for all users regardless of their location.

- Database: Store UTC timestamps
- Business Logic: Operate in Mountain Time
- Display: Show Mountain Time
- Validation: Use MT-aware Zod schemas
- Documentation: Label timezone in UI and code comments

When in doubt, import from `@/utils/timezone.ts` and avoid native `Date` operations.
