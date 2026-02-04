---
name: leap-year-analyzer
description: "Analyze leap year calculations, calendar systems, and date validation logic. Use this when the user asks about leap year rules, calendar types (Gregorian, Julian, Hebrew, Chinese), year range validation (1582-9999), mathematical formulas, or needs to understand the core leap year detection algorithms."
allowed-tools: Read, Grep, Glob
---

# Leap Year Analyzer Skill

This Skill helps analyze and understand the leap year calculation logic used in the IsLeapYear application.

## When to Use

- Understanding leap year calculation rules
- Comparing calendar systems
- Validating year ranges
- Explaining mathematical formulas
- Debugging leap year logic
- Adding support for new calendar types

## Core Leap Year Logic

Located in `src/utils/leap-year.ts`

### Gregorian Calendar

The standard leap year rule used globally since 1582:

```typescript
(year % 4 === 0 && year % 100 !== 0) || year % 400 === 0
```

**Rules:**
1. Divisible by 4 → Leap year
2. BUT divisible by 100 → Not a leap year
3. BUT divisible by 400 → Leap year

**Valid Range:** 1582-9999 (Gregorian calendar introduction to far future)

**Examples:**
- 2024 → Leap (divisible by 4, not by 100)
- 2000 → Leap (divisible by 400)
- 1900 → Not leap (divisible by 100, not by 400)
- 2100 → Not leap (divisible by 100, not by 400)

### Julian Calendar

Simpler rule used before Gregorian calendar:

```typescript
year % 4 === 0
```

**Rule:** Any year divisible by 4 is a leap year (no century exception)

### Hebrew Calendar

Uses Metonic cycle approximation (19-year cycle with 7 leap years):

```typescript
[3, 6, 8, 11, 14, 17, 19].includes((year % 19) + 1)
```

**Leap years occur in years:** 3, 6, 8, 11, 14, 17, 19 of each 19-year cycle

### Chinese Calendar

Also uses Metonic cycle approximation:

```typescript
[3, 5, 8, 11, 13, 16, 19].includes((year % 19) + 1)
```

**Leap years occur in years:** 3, 5, 8, 11, 13, 16, 19 of each 19-year cycle

## Calendar Type Enum

```typescript
type CalendarType = "gregorian" | "julian" | "hebrew" | "chinese";
```

## Why 1582 for Gregorian?

Pope Gregory XIII introduced the Gregorian calendar in October 1582 to correct drift in the Julian calendar. The app validates Gregorian dates starting from this year to maintain historical accuracy.

## Common Tasks

### 1. Validating a Year

```typescript
if (Number.isNaN(year)) {
  return errorResponse("Invalid year parameter");
}

if (year < 1582 || year > 9999) {
  return errorResponse("Year must be between 1582 and 9999");
}
```

### 2. Checking Leap Year

Use the functions from `src/utils/leap-year.ts`:
- `isLeapYear(year: number, calendar?: CalendarType): boolean`
- Import: `import { isLeapYear } from "@/utils/leap-year"`

### 3. Calculating Leap Years in Range

Iterate through range and count:
```typescript
const leapYears = [];
for (let y = start; y <= end; y++) {
  if (isLeapYear(y, calendar)) {
    leapYears.push(y);
  }
}
```

## Mathematical Insights

### Frequency of Leap Years

- **Gregorian:** 97 leap years every 400 years (24.25%)
- **Julian:** 1 leap year every 4 years (25%)
- **Hebrew/Chinese:** 7 leap years every 19 years (~36.8%)

### Century Years

Only 1 in 4 century years is a leap year in Gregorian:
- 1600 ✓ Leap
- 1700 ✗ Not leap
- 1800 ✗ Not leap
- 1900 ✗ Not leap
- 2000 ✓ Leap
- 2100 ✗ Not leap

## Testing Leap Year Logic

```bash
# Current year (2025 - not a leap year)
curl http://localhost:3000/api/check

# Standard leap year
curl http://localhost:3000/api/check/2024

# Century leap year
curl http://localhost:3000/api/check/2000

# Century non-leap year
curl http://localhost:3000/api/check/1900

# Julian vs Gregorian comparison
curl http://localhost:3000/api/calendar/julian/check/1900
curl http://localhost:3000/api/calendar/gregorian/check/1900

# Batch test edge cases
curl -X POST http://localhost:3000/api/check/batch \
  -H "Content-Type: application/json" \
  -d '{"years": [1900, 2000, 2024, 2100, 2400]}'
```

## Important Notes

- Always validate year range for Gregorian calendar (1582-9999)
- Julian calendar doesn't have the 100/400 exceptions
- Hebrew and Chinese calendars use approximations (actual calendars are more complex)
- The core logic maintains the satirical tone but uses mathematically correct algorithms
- Functions are exported from `src/utils/leap-year.ts` and used across API routes
