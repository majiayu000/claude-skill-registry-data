---
name: gpa-cgpa-calculator
description: GPA and CGPA calculation formulas and logic for JKKN COE grading system. This skill should be used when implementing GPA calculation, CGPA calculation, grade point lookup, pass status determination, or semester results processing. Automatically triggers when user mentions 'GPA', 'CGPA', 'grade point', 'semester results', 'cumulative grade', or 'grade calculation'.
---

# GPA & CGPA Calculator

This skill provides the complete formulas, logic, and data sources for calculating Grade Point Average (GPA) and Cumulative Grade Point Average (CGPA) in the JKKN COE grading system.

## Overview

| Component | Formula | Data Source |
|-----------|---------|-------------|
| Grade Points | Lookup from grade table based on percentage | `grade_system` table |
| Pass Status | Course-specific pass marks comparison | `courses` table |
| GPA | Σ(Credits × GradePoints) / ΣCredits | Per semester |
| CGPA | Σ(SemesterGPA × SemesterCredits) / ΣCredits | Across all semesters |

## Calculation Workflow

```
MARKS ENTRY (final_marks)
         │
         ▼
PASS STATUS (courses table)
Compare obtained vs course-specific pass marks
         │
         ▼
PERCENTAGE CALCULATION
percentage = (total_obtained / total_maximum) × 100
         │
         ▼
GRADE POINT LOOKUP (grade_system table)
Match percentage to grade range → get grade_point
         │
         ▼
GPA CALCULATION
GPA = Σ(Credits × GradePoints) / ΣCredits
         │
         ▼
CGPA CALCULATION
CGPA = Σ(SemesterGPA × SemesterCredits) / ΣSemesterCredits
```

## 1. Grade Point Determination

To determine grade points, fetch the grade table from `grade_system` table filtered by program type (UG or PG).

### API Fetch Pattern

```typescript
const res = await fetch('/api/grading/grade-system?is_active=true')
const data = await res.json()

// Filter by program type
const gradeTable = data
  .filter(r => r.grade_system_code === programType) // 'UG' or 'PG'
  .sort((a, b) => b.min_mark - a.min_mark)
```

### Grade Lookup Function

```typescript
interface GradeTableEntry {
  min: number
  max: number
  gradePoint: number
  letterGrade: string
  description: string
}

function getGradeFromPercentage(
  percentage: number,
  gradeTable: GradeTableEntry[],
  isAbsent: boolean = false
): { gradePoint: number; letterGrade: string; description: string } {
  if (isAbsent) {
    const absentEntry = gradeTable.find(g => g.min === -1 && g.max === -1)
    if (absentEntry) {
      return {
        gradePoint: absentEntry.gradePoint,
        letterGrade: absentEntry.letterGrade,
        description: absentEntry.description
      }
    }
    return { gradePoint: 0, letterGrade: 'AAA', description: 'ABSENT' }
  }

  // Sort table by min descending to check higher ranges first
  const sortedTable = [...gradeTable]
    .filter(g => g.min >= 0)
    .sort((a, b) => b.min - a.min)

  for (const grade of sortedTable) {
    if (percentage >= grade.min && percentage <= grade.max) {
      return {
        gradePoint: grade.gradePoint,
        letterGrade: grade.letterGrade,
        description: grade.description
      }
    }
  }

  // Default to fail
  return { gradePoint: 0, letterGrade: 'U', description: 'Re-Appear' }
}
```

## 2. Pass Status Determination

Pass marks are **course-specific** and fetched from the `courses` table. Do NOT use hardcoded UG/PG defaults.

### Database Fields (courses table)

| Field | Description |
|-------|-------------|
| `internal_pass_mark` | Minimum internal marks to pass |
| `external_pass_mark` | Minimum external marks to pass |
| `total_pass_mark` | Minimum total marks to pass |

### Pass Status Logic

```typescript
function checkPassStatus(
  internalObtained: number,
  externalObtained: number,
  totalObtained: number,
  coursePassMarks: {
    internal_pass_mark: number
    external_pass_mark: number
    total_pass_mark: number
  }
): boolean {
  const { internal_pass_mark, external_pass_mark, total_pass_mark } = coursePassMarks

  // A component passes if: pass_mark = 0 (no minimum) OR obtained >= pass_mark
  const passesInternal = internal_pass_mark === 0 || internalObtained >= internal_pass_mark
  const passesExternal = external_pass_mark === 0 || externalObtained >= external_pass_mark
  const passesTotal = total_pass_mark === 0 || totalObtained >= total_pass_mark

  return passesInternal && passesExternal && passesTotal
}
```

### Database Trigger (SQL)

Reference: `supabase/migrations/20251204000001_fix_pass_status_trigger_join.sql`

The database trigger `auto_determine_pass_status` automatically calculates pass status on INSERT/UPDATE to `final_marks` table by:
1. Fetching pass criteria from `courses` table via `course_offerings`
2. Calculating percentage for each component
3. Comparing obtained percentage against pass percentage
4. Setting `is_pass`, `pass_status`, `is_distinction`, `is_first_class`

## 3. GPA Calculation (Semester)

### Formula (Vector Dot Product)

```
GPA = (C⃗ · G⃗) / ΣCi = Σ(Ci × Gi) / ΣCi
```

Where:
- `Ci` = Credits for course i
- `Gi` = Grade Points for course i

### Implementation

```typescript
function calculateGPA(credits: number[], gradePoints: number[]): number {
  if (credits.length === 0 || credits.length !== gradePoints.length) {
    return 0
  }

  // Dot product: Σ(Ci × Gi)
  let dotProduct = 0
  let totalCredits = 0

  for (let i = 0; i < credits.length; i++) {
    dotProduct += credits[i] * gradePoints[i]
    totalCredits += credits[i]
  }

  if (totalCredits === 0) return 0

  // GPA = Dot product / Total credits (rounded to 2 decimal places)
  return Math.round((dotProduct / totalCredits) * 100) / 100
}
```

### Example

| Course | Credits (Ci) | Grade Points (Gi) | Ci × Gi |
|--------|--------------|-------------------|---------|
| CS101 | 4 | 10.0 | 40.0 |
| CS102 | 4 | 9.0 | 36.0 |
| MA101 | 3 | 8.0 | 24.0 |
| **Total** | **11** | | **100.0** |

**GPA = 100.0 / 11 = 9.09**

## 4. CGPA Calculation (Cumulative)

### Formula (Weighted Average)

```
CGPA = Σn(GPAn × TCn) / Σn(TCn)
```

Where:
- `GPAn` = GPA for semester n
- `TCn` = Total credits for semester n

### Implementation

```typescript
function calculateCGPA(semesterGPAs: number[], semesterCredits: number[]): number {
  if (semesterGPAs.length === 0 || semesterGPAs.length !== semesterCredits.length) {
    return 0
  }

  // Weighted sum: Σ(GPAn × TCn)
  let weightedSum = 0
  let totalCredits = 0

  for (let i = 0; i < semesterGPAs.length; i++) {
    weightedSum += semesterGPAs[i] * semesterCredits[i]
    totalCredits += semesterCredits[i]
  }

  if (totalCredits === 0) return 0

  // CGPA = Weighted sum / Total credits (rounded to 2 decimal places)
  return Math.round((weightedSum / totalCredits) * 100) / 100
}
```

### Alternative: Direct CGPA Calculation

Calculate CGPA directly from all courses across all semesters (yields same result):

```typescript
function calculateCGPADirect(allCredits: number[], allGradePoints: number[]): number {
  return calculateGPA(allCredits, allGradePoints)
}
```

### Example

| Semester | GPA (GPAn) | Credits (TCn) | GPAn × TCn |
|----------|------------|---------------|------------|
| Sem 1 | 9.09 | 11 | 99.99 |
| Sem 2 | 8.55 | 11 | 94.05 |
| Sem 3 | 8.80 | 12 | 105.60 |
| **Total** | | **34** | **299.64** |

**CGPA = 299.64 / 34 = 8.81**

## 5. Data Sources Summary

| Data | Table | Fields |
|------|-------|--------|
| Pass Marks | `courses` | `internal_pass_mark`, `external_pass_mark`, `total_pass_mark` |
| Max Marks | `courses` | `internal_max_mark`, `external_max_mark`, `total_max_mark` |
| Grade Points | `grade_system` | `min_mark`, `max_mark`, `grade_point`, `grade`, `description` |
| Credits | `courses` | `credits` |
| Obtained Marks | `final_marks` | `internal_marks_obtained`, `external_marks_obtained`, `total_marks_obtained` |

## 6. Classification Thresholds

After calculating total percentage, determine additional classifications:

```typescript
// Distinction: ≥75% total
const isDistinction = totalPercentage >= 75

// First Class: ≥60% total
const isFirstClass = totalPercentage >= 60
```

## 7. Reference Implementation

For complete working implementation, see:
- Test page: `app/(coe)/grading/test-gpa-cgpa/page.tsx`
- Database trigger: `supabase/migrations/20251204000001_fix_pass_status_trigger_join.sql`
- Grade system API: `app/api/grading/grade-system/route.ts`

## Key Reminders

1. **Pass marks are course-specific** - Always fetch from `courses` table
2. **Grade tables are program-type specific** - Filter by UG or PG
3. **Both CGPA methods yield same result** - Weighted semester GPA or direct all-courses
4. **Always round to 2 decimal places** - Use `Math.round(value * 100) / 100`
5. **Handle edge cases** - Zero credits, absent students, missing data
