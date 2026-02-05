---
name: lms-teacher-timetable
description: KCIS Linkou Campus elementary teacher timetable system. Use this skill when implementing teacher schedule features, querying schedules by teacher, displaying weekly timetables, or handling multi-type courses (English/EV/KCFS). Covers 73 teachers, 42 classes (G1-G6), and 8 daily periods.
---

# KCIS Teacher Timetable System

## Quick Reference

| Item | Value |
|------|-------|
| **Teachers** | 73 |
| **Classes** | 42 (G1-G6, 7 per grade) |
| **Daily Periods** | 8 (08:25-16:05) |
| **School Days** | Monday - Friday |

## Teacher Identification

**Primary Key**: `email` (unique, for matching)

```
Teacher lookup flow:
1. Get user by auth → retrieve email
2. Query timetable_entries by teacher_email → get schedule
```

## Course Types

| Type | Color | Click Action | Description |
|------|-------|--------------|-------------|
| english | Blue (`bg-blue-500`) | → `/class/{id}/attendance` | English (LT/IT) |
| kcfs | Emerald (`bg-emerald-500`) | → `/class/{id}` | Kang Chiao Future Skill |
| ev | Purple (`bg-purple-500`) | → `/class/{id}` | Extended Vocabulary |

## Period Schedule

| Period | Time |
|--------|------|
| 1 | 08:25-09:05 |
| 2 | 09:10-09:50 |
| 3 | 10:20-11:00 |
| 4 | 11:05-11:45 |
| 5 | 12:55-13:35 |
| 6 | 13:40-14:20 |
| 7 | 14:40-15:20 |
| 8 | 15:25-16:05 |

## Key Files

| File | Purpose |
|------|---------|
| `lib/api/timetable.ts` | API functions |
| `components/schedule/WeeklyTimetable.tsx` | Week view |
| `components/schedule/TimetableCell.tsx` | Cell styling |
| `components/schedule/TodaySchedule.tsx` | Mobile view |
| `app/(lms)/schedule/page.tsx` | Schedule page |
| `scripts/import-timetable.ts` | CSV import |

## API Functions

```typescript
// lib/api/timetable.ts

// Get schedule by email (primary method)
getTeacherScheduleByEmail(email: string, academicYear?: string): Promise<WeeklyTimetable>

// Get current user's schedule
getCurrentUserSchedule(userId: string, academicYear?: string): Promise<{
  weekly: WeeklyTimetable;
  stats: TeacherScheduleStats;
  periods: TimetablePeriod[];
}>

// Utilities
getCurrentDayOfWeek(): DayOfWeek | null  // null on weekends
formatPeriodTime(period: TimetablePeriod): string
```

## Click Navigation

```typescript
const handleCellClick = (entry: TimetableEntryWithPeriod) => {
  if (!entry.course_id) return;

  if (entry.course_type === "ev" || entry.course_type === "kcfs") {
    // EV/KCFS: Navigate to course page
    window.location.href = `/class/${entry.course_id}`;
  } else {
    // English: Navigate to attendance page
    window.location.href = `/class/${entry.course_id}/attendance`;
  }
};
```

## Data Statistics (2025-2026)

| Course Type | Entries | With course_id |
|-------------|---------|----------------|
| English | 1,064 | 1,064 (100%) |
| KCFS | 167 | 167 (100%) |
| EV | 56 | 0 (N/A) |

## Troubleshooting

### Schedule not showing
1. Check `users.email` matches `timetable_entries.teacher_email`
2. Verify `academic_year` is correct (2025-2026)
3. Check RLS policies allow access

### Click not navigating
1. Verify `course_id` is populated
2. Check course exists in `courses` table
3. Confirm `course_type` is correct

## References

- Database Schema: [references/schema.sql](references/schema.sql)
- Query Examples: [references/query-examples.md](references/query-examples.md)
- CSV Format: [references/csv-format.md](references/csv-format.md)
