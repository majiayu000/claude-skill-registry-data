---
name: attendance-reports
description: Exam Attendance Reports implementation reference for Student Sheets, Summary Reports, and Bundle Covers. Uses MyJKKN API for programs and exam_registrations for student details.
---

# Attendance Reports Skill

Reference for Exam Attendance Reports page following MyJKKN COE dev rules.

## Report Types

| Report | API Endpoint | DB Function |
|--------|--------------|-------------|
| Student Sheet | `/api/exam-management/exam-attendance/student-sheet` | `get_student_attendance_sheet()` |
| Summary Report | `/api/exam-management/exam-attendance/report` | Direct query |
| Bundle Cover | `/api/exam-management/exam-attendance/bundle-cover` | Direct query |

## Key Files

```
app/(coe)/exam-management/reports/attendance/page.tsx
app/api/exam-management/exam-attendance/student-sheet/route.ts
app/api/exam-management/exam-attendance/bundle-cover/route.ts
app/api/exam-management/exam-attendance/report/route.ts
supabase/migrations/20260110_update_student_attendance_sheet_use_program_code.sql
```

## MyJKKN Rules Applied

### 1. Programs from MyJKKN API

```typescript
const { fetchPrograms } = useMyJKKNInstitutionFilter()
const myjkknIds = institution?.myjkkn_institution_ids || []
const programs = await fetchPrograms(myjkknIds)
```

### 2. Student Details from exam_registrations

```sql
-- NOT from students table
COALESCE(er.stu_register_no, '-')::TEXT AS register_number,
COALESCE(er.student_name, '-')::TEXT AS student_name
```

### 3. program_code Direct Usage

```sql
-- COALESCE pattern for program_code
COALESCE(co.program_code, ea.program_code, '-')::TEXT AS program_code

-- LEFT JOIN for optional name lookup
LEFT JOIN public.programs p ON (
  p.program_code = COALESCE(co.program_code, ea.program_code)
  AND p.institutions_id = er.institutions_id
)
```

## Filter Cascade

```
Institution → Sessions → Programs (MyJKKN API)
                      ↓
               Exam Dates → Session Type (FN/AN) → Courses
```

## API Parameters

### Student Sheet
```
GET /api/exam-management/exam-attendance/student-sheet
  ?session_code={required}
  &exam_date={optional}
  &session={optional: FN/AN}
  &program_code={optional}
  &course_code={optional}
```

### Bundle Cover
```
GET /api/exam-management/exam-attendance/bundle-cover
  ?institution_id={required}
  &session_id={required}
  &exam_date={required}
  &session={required: FN/AN}
  &program_code={optional}
  &course_code={optional}
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 0 records returned | INNER JOIN to programs fails | Use LEFT JOIN with program_code |
| Student names missing | Using students table | Use exam_registrations |
| Bundle cover fails | Programs FK dependency | Use program_code directly |

## Testing Checklist

- [ ] Institution dropdown filters by user role
- [ ] Programs load from MyJKKN API
- [ ] Student names show from exam_registrations
- [ ] All three report types generate correctly
