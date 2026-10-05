---
name: date-fns
description: Modern JavaScript date utility library with modular, tree-shakeable functions for formatting, parsing, comparison, and manipulation
layer: domain
category: utility
triggers:
  - "date-fns"
  - "date formatting"
  - "date parsing"
  - "date comparison"
  - "date manipulation"
  - "formatDistance"
  - "parseISO"
inputs:
  - "Date formatting or display requirements"
  - "Date arithmetic or comparison logic"
  - "Timezone handling needs"
outputs:
  - "Tree-shakeable date utility implementations"
  - "Locale-aware date formatting"
  - "Timezone-safe date operations"
linksTo:
  - typescript-frontend
  - react
  - nodejs
linkedFrom:
  - forms
  - i18n
riskLevel: low
memoryReadPolicy: none
memoryWritePolicy: none
sideEffects: []
---

# date-fns

## Overview

Modern JavaScript date utility library. Each function is a standalone module — import only what you use for minimal bundle size. Works with native `Date` objects (no wrapper types).

## When to Use

- Formatting dates for display (relative time, localized strings, durations)
- Parsing date strings from APIs or user input
- Comparing or sorting dates, checking ranges
- Date arithmetic (add/subtract days, find start/end of periods)
- Timezone conversions (via `date-fns-tz`)

## Key Patterns

### Formatting

```typescript
import { format, formatDistance, formatRelative, formatDuration, intervalToDuration } from 'date-fns';

format(new Date(), 'yyyy-MM-dd HH:mm');           // "2026-03-10 14:30"
formatDistance(subDays(new Date(), 3), new Date()); // "3 days ago" (with { addSuffix: true })
formatRelative(subDays(new Date(), 1), new Date()); // "yesterday at 2:30 PM"
formatDuration(intervalToDuration({ start: 0, end: 90000000 })); // "1 day 1 hour"
```

### Parsing

```typescript
import { parse, parseISO } from 'date-fns';

parseISO('2026-03-10T14:30:00Z');                   // Date from ISO string
parse('10/03/2026', 'dd/MM/yyyy', new Date());      // Date from custom format
```

### Comparison

```typescript
import { isBefore, isAfter, isWithinInterval, differenceInDays } from 'date-fns';

isBefore(dateA, dateB);
isWithinInterval(date, { start, end });
differenceInDays(new Date(2026, 2, 10), new Date(2026, 1, 1)); // 37
```

### Manipulation

```typescript
import { add, sub, set, startOfMonth, endOfWeek } from 'date-fns';

add(new Date(), { days: 7, hours: 3 });
startOfMonth(new Date());  // First day of current month, 00:00:00
endOfWeek(new Date(), { weekStartsOn: 1 }); // Sunday end (Monday-start week)
```

### Locale Support

```typescript
import { format } from 'date-fns';
import { ja } from 'date-fns/locale'; // Import locales individually for tree-shaking

format(new Date(), 'PPP', { locale: ja }); // "2026年3月10日"
```

### Intervals and Ranges

```typescript
import { eachDayOfInterval, isWithinInterval } from 'date-fns';

eachDayOfInterval({ start: new Date(2026, 2, 1), end: new Date(2026, 2, 7) }); // Date[]
```

### UTC / Timezone Helpers (date-fns-tz)

```typescript
import { zonedTimeToUtc, utcToZonedTime, format } from 'date-fns-tz';

const utc = zonedTimeToUtc('2026-03-10 09:00', 'Asia/Tokyo');
const zoned = utcToZonedTime(utc, 'America/New_York');
format(zoned, 'yyyy-MM-dd HH:mm zzz', { timeZone: 'America/New_York' });
```

### TypeScript Types

All functions accept `Date | number` for flexibility. Use `Interval` type for range objects.

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Importing entire library (`import * as dateFns`) | Import individual functions |
| Using `new Date(string)` for parsing | Use `parseISO` or `parse` with explicit format |
| Mutating dates directly | date-fns returns new Date instances (immutable) |
| Bundling all locales | Import only needed locales: `date-fns/locale/ja` |
| Ignoring timezone when comparing server/client dates | Use `date-fns-tz` for timezone-aware operations |

## Related Skills

- **typescript-frontend** — Type-safe date handling in UI components
- **react** — Date formatting in components, memo-friendly pure functions
- **nodejs** — Server-side date operations, API response formatting
