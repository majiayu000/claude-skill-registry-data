---
name: rrule-scheduling
description: RFC 5545 RRULE recurrence patterns for scheduling. Use when implementing recurring schedules, calendar events, or time-based automation. Triggers on mentions of RRULE, recurrence, recurring events, weekly schedule, or calendar patterns.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# RRULE Scheduling Patterns

## What is RRULE?

RRULE (Recurrence Rule) is the RFC 5545 standard for defining recurring events. Used by Google Calendar, Outlook, and iCal.

## Library: rrule.js

```bash
npm install rrule
```

## Basic Patterns

### Daily

```typescript
import { RRule } from 'rrule';

const daily = new RRule({
  freq: RRule.DAILY,
  dtstart: new Date(2024, 0, 1, 8, 0), // Jan 1, 2024 at 8am
});

// RRULE string: "FREQ=DAILY"
```

### Weekdays Only

```typescript
const weekdays = new RRule({
  freq: RRule.WEEKLY,
  byweekday: [RRule.MO, RRule.TU, RRule.WE, RRule.TH, RRule.FR],
  dtstart: new Date(2024, 0, 1, 8, 0),
});

// RRULE string: "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"
```

### Specific Days

```typescript
// Monday, Wednesday, Friday
const mwf = new RRule({
  freq: RRule.WEEKLY,
  byweekday: [RRule.MO, RRule.WE, RRule.FR],
  dtstart: new Date(2024, 0, 1),
});

// Weekends only
const weekends = new RRule({
  freq: RRule.WEEKLY,
  byweekday: [RRule.SA, RRule.SU],
  dtstart: new Date(2024, 0, 1),
});
```

### Every N Weeks

```typescript
// Every 2 weeks on Friday
const biweekly = new RRule({
  freq: RRule.WEEKLY,
  interval: 2,
  byweekday: [RRule.FR],
  dtstart: new Date(2024, 0, 5), // First Friday
});

// RRULE string: "FREQ=WEEKLY;INTERVAL=2;BYDAY=FR"
```

### Monthly Patterns

```typescript
// First Monday of each month
const firstMonday = new RRule({
  freq: RRule.MONTHLY,
  byweekday: [RRule.MO.nth(1)],
  dtstart: new Date(2024, 0, 1),
});

// Last Friday of each month
const lastFriday = new RRule({
  freq: RRule.MONTHLY,
  byweekday: [RRule.FR.nth(-1)],
  dtstart: new Date(2024, 0, 1),
});

// 15th of each month
const monthly15th = new RRule({
  freq: RRule.MONTHLY,
  bymonthday: 15,
  dtstart: new Date(2024, 0, 15),
});
```

## Expanding Occurrences

### Get Occurrences in Range

```typescript
function getOccurrences(
  rruleString: string,
  dtstart: Date,
  rangeStart: Date,
  rangeEnd: Date
): Date[] {
  const rule = RRule.fromString(rruleString);
  rule.options.dtstart = dtstart;

  return rule.between(rangeStart, rangeEnd, true);
}

// Example: Get all occurrences for next week
const occurrences = getOccurrences(
  'FREQ=WEEKLY;BYDAY=MO,WE,FR',
  new Date(2024, 0, 1),
  new Date(), // now
  new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // +7 days
);
```

### Get Next Occurrence

```typescript
function getNextOccurrence(
  rruleString: string,
  dtstart: Date,
  after: Date = new Date()
): Date | null {
  const rule = RRule.fromString(rruleString);
  rule.options.dtstart = dtstart;

  return rule.after(after);
}
```

## Human-Readable Text

```typescript
const rule = new RRule({
  freq: RRule.WEEKLY,
  byweekday: [RRule.MO, RRule.TU, RRule.WE, RRule.TH, RRule.FR],
  dtstart: new Date(2024, 0, 1, 8, 0),
});

console.log(rule.toText());
// "every week on Monday, Tuesday, Wednesday, Thursday, Friday"
```

## Handling End Dates

### Count-Based

```typescript
// Repeat 10 times
const limited = new RRule({
  freq: RRule.WEEKLY,
  count: 10,
  dtstart: new Date(2024, 0, 1),
});
```

### Until Date

```typescript
// Until end of year
const untilEndOfYear = new RRule({
  freq: RRule.WEEKLY,
  byweekday: [RRule.MO, RRule.FR],
  until: new Date(2024, 11, 31),
  dtstart: new Date(2024, 0, 1),
});
```

## Exceptions (EXDATE)

Use RRuleSet to add exceptions:

```typescript
import { RRule, RRuleSet } from 'rrule';

const rruleSet = new RRuleSet();

// Add the main rule
rruleSet.rrule(new RRule({
  freq: RRule.WEEKLY,
  byweekday: [RRule.MO, RRule.WE, RRule.FR],
  dtstart: new Date(2024, 0, 1),
}));

// Exclude specific dates (holidays)
rruleSet.exdate(new Date(2024, 0, 15)); // MLK Day
rruleSet.exdate(new Date(2024, 11, 25)); // Christmas

// Get occurrences (holidays excluded)
const dates = rruleSet.between(
  new Date(2024, 0, 1),
  new Date(2024, 11, 31)
);
```

## Database Storage

Store RRULE as a string:

```typescript
interface ScheduleBlock {
  id: string;
  zoneId: string;
  playlistId: string;

  // Time within each occurrence
  startTime: string;  // "08:00"
  endTime: string;    // "10:00"

  // Recurrence
  rrule: string;      // "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"
  dtstart: Date;      // Anchor date for recurrence
  until: Date | null; // End date (null = forever)

  priority: number;
  isActive: boolean;
}
```

## Conflict Resolution

When multiple schedules overlap, use priority:

```typescript
function resolveScheduleForTime(
  schedules: ScheduleBlock[],
  targetDate: Date
): ScheduleBlock | null {
  const activeSchedules = schedules
    .filter(s => {
      // Check if schedule applies to this date
      const rule = RRule.fromString(s.rrule);
      const occurrences = rule.between(
        startOfDay(targetDate),
        endOfDay(targetDate)
      );
      return occurrences.length > 0;
    })
    .filter(s => {
      // Check time range
      const time = targetDate.toTimeString().slice(0, 5);
      return time >= s.startTime && time < s.endTime;
    })
    .sort((a, b) => b.priority - a.priority);

  return activeSchedules[0] ?? null;
}
```

## Common Patterns for B2B Music

```typescript
// Morning shift: Mon-Fri 6am-12pm
const morning = 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR';

// Afternoon shift: Mon-Fri 12pm-6pm
const afternoon = 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR';

// Evening shift: Mon-Fri 6pm-10pm
const evening = 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR';

// Weekend daytime: Sat-Sun 10am-10pm
const weekend = 'FREQ=WEEKLY;BYDAY=SA,SU';

// Happy hour: Mon-Fri 4pm-7pm
const happyHour = 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR';

// Sunday brunch: Every Sunday
const sundayBrunch = 'FREQ=WEEKLY;BYDAY=SU';
```
