---
name: lms-database
description: Supabase database query patterns, RLS policies, migration records, and nested join patterns. Use this skill when writing database queries, understanding RLS behavior, debugging query errors, or implementing new migrations.
---

# LMS Database Skill

> Supabase 資料庫查詢模式、RLS 政策、Migration 記錄
> Last Updated: 2026-01-02
>
> **相關 Skill**: [kcis-school-config](../kcis-school-config/SKILL.md) - 學校專屬設定

## Database Connection Strings

```bash
# Staging Database (kqvpcoolgyhjqleekmee)
# Used by: lms-staging.zeabur.app
psql "postgresql://postgres.kqvpcoolgyhjqleekmee:geonook8588@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres"

# Production Database (piwbooidofbaqklhijup)
# Used by: lms.kcislk.ntpc.edu.tw (future)
psql "postgresql://postgres.piwbooidofbaqklhijup:geonook8588@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
```

---

## Supabase Nested Join 查詢模式（重要！）

### 核心規則

Supabase 的 `table!inner` 語法是透過 **外鍵（FK）** 連接，不是透過查詢中選取的欄位。

### 資料庫關聯鏈

```
scores → exam_id (FK) → exams → course_id (FK) → courses → class_id (FK) → classes
```

**注意**：`exams` 表**沒有** `class_id` 欄位（Migration 035 已移除），只有 `course_id`。

### 正確模式

```typescript
const { data } = await supabase
  .from('scores')
  .select(`
    student_id,
    assessment_code,
    score,
    exam:exams!inner(
      course_id,                    // ← 取得 FK 欄位
      course:courses!inner(
        id,
        class_id,                   // ← 從 course 取得 class_id
        course_type
      )
    )
  `)
  .in('student_id', studentIds)   // ← 限制查詢範圍
  .not('score', 'is', null);

// 過濾時使用 exam.course.class_id
const filtered = data.filter(s => {
  const examData = s.exam as { course_id: string; course: { class_id: string; ... } };
  return classIdSet.has(examData.course.class_id);  // 正確
});
```

### 錯誤模式

```typescript
exam:exams!inner(
  class_id,                       // ← 這個欄位已不存在！會返回 400 Error
  course:courses!inner(...)
)
```

### 為什麼這很重要

- `exams` 表只有 `course_id` 欄位（NOT NULL）
- **`class_id` 已在 Migration 035 移除**
- 如果需要 class_id，必須從 `exam.course.class_id` 取得
- 直接查詢 `exams.class_id` 會返回 400 Bad Request

### 效能最佳實踐

```typescript
// 永遠加上限制條件避免全表掃描
.in('student_id', studentIds)
.in('exam_id', examIds)
.eq('class_id', classId)
```

---

## RLS (Row Level Security) 核心規則

### 四層安全架構（v1.66.0）

```
1. Authentication (Supabase Auth) - 必須登入
2. RLS (Database Layer) - 粗粒度：authenticated_read, admin_full_access
3. Application Layer (lib/api/permissions.ts) - 細粒度：角色過濾
4. Frontend (AuthGuard) - 頁面存取控制
```

**設計原則**：
- RLS 只負責「是否登入」和「是否 Admin」
- 細粒度權限（Head 年級過濾、Teacher 課程過濾）在 Application Layer 處理
- 避免 RLS 跨表查詢造成遞迴

### 簡化後的 RLS Policies

每張表最多 4 個 policies：
1. `service_role_bypass` - Service Role 繞過
2. `admin_full_access` - Admin 完整存取
3. `authenticated_read` - 已登入者可讀
4. `teacher_manage_own` - 教師管理自己課程（僅 courses, exams, scores）

### 角色權限矩陣

| 角色 | RLS 層 | Application 層 |
|------|--------|----------------|
| admin | 全部存取 | 不過濾 |
| office_member | 可讀全部 | 不過濾（唯讀）|
| head | 可讀全部 | 過濾 grade_band + track |
| teacher | 可讀全部 + 寫自己課程 | 過濾 teacher_id |

### Service Role Bypass

所有表都有 `service_role_bypass` 政策：
- Service Role Key 可繞過所有 RLS
- 用於 CSV 匯入、Migration 等管理操作

---

## 關鍵 Migration 記錄

### Migration 014: Track 欄位型別修正
- `users.track`: `track_type` → `course_type`
- `students.track`: `track_type` → `course_type` (nullable)
- 重建 3 個 Analytics 視圖

### Migration 015: RLS 效能優化
- 優化 49 個 policies
- `auth.uid()` → `(SELECT auth.uid())`
- Database Linter 警告從 44+ 降至 0

### Migration 028: Users 表 RLS 遞迴修復
- 刪除 24 個有遞迴問題的 policies
- 建立簡單的 `authenticated_read_users` 政策

### Migration 029: Course Tasks Kanban
- 建立 `course_tasks` 表
- 支援任務看板功能

### Migration 030: Four-Term 學期系統
- 新增 `exams.term` (1-4) 和 `exams.semester` (1-2) 欄位
- 自動計算 trigger

### Migration 031: 2026-2027 學年
- 複製 84 班級 + 252 課程

### Migration 032: Gradebook Expectations
- 建立 `gradebook_expectations` 表
- Head Teacher 成績進度預期設定

### Migration 033: KCFS Scoring System
- 新增 KCFS 評量類別代碼（COMM, COLLAB, SD, CT, BW, PORT, PRES）
- 新增 `scores.is_absent` 欄位
- 支援 0-5 分制的 KCFS 評分

### Migration 034: MAP Tables
- 建立 `map_assessments` 表（MAP 測驗成績）
- 建立 `map_goal_scores` 表（目標領域分數）
- 支援 NWEA MAP Growth 數據分析

### Migration 035: Sync Exams Schema
- **移除** `exams.class_id` 欄位
- 設定 `exams.course_id` 為 NOT NULL
- 重命名 `is_published` 為 `is_active`
- 同步 Staging 與 Production 資料庫結構

### Migration 036: RLS Simplification
- 簡化 RLS policies 從 100+ 降至 ~30
- 建立 `is_admin()` helper function
- 設計原則：不跨表查詢，防止無限遞迴
- 細粒度權限移至 Application Layer

### Migration 037: Complete RLS Policies
- 補齊 12 個遺漏表的 RLS policies
- 受影響表：map_assessments, map_goal_scores, attendance, behavior_tags, student_behaviors, communications, gradebook_expectations, academic_periods, kcfs_categories, timetable_entries, timetable_periods, course_tasks, admin_audit_logs

### Migration 038: Rename MAP Term
- 重命名 MAP 相關欄位

### Migration 039: Fall-to-Fall Growth Columns
- 新增 Fall-to-Fall 成長計算欄位

### Migration 040: Academic Periods
- 建立 `academic_periods` 表
- 學期與學年設定

### Migration 041: Student Class History
- 建立 `student_class_history` 表
- 儲存學生歷史班級資訊（academic_year, grade, english_class, homeroom）
- 用於 MAP 成長分析中的正確班級對應（避免學生升級後顯示新班級）

---

## 常用查詢模式

### 取得班級課程與教師

```typescript
const { data } = await supabase
  .from('courses')
  .select(`
    id,
    course_type,
    teacher:users!teacher_id(
      id,
      full_name
    ),
    class:classes!inner(
      id,
      class_name,
      grade
    )
  `)
  .eq('class_id', classId);
```

### 取得學生成績（含課程篩選）

```typescript
const { data } = await supabase
  .from('scores')
  .select(`
    student_id,
    assessment_code,
    score,
    exam:exams!inner(
      course:courses!inner(
        course_type
      )
    )
  `)
  .eq('exam.course.course_type', courseType)
  .in('student_id', studentIds);
```

### 取得 Head Teacher 管轄班級

```typescript
// HT 的 grade 和 track（course_type）定義管轄範圍
const { data } = await supabase
  .from('classes')
  .select('*')
  .eq('grade', headTeacherGrade)
  .eq('academic_year', academicYear);

// 課程需額外過濾 course_type
const courses = allCourses.filter(c => c.course_type === headTeacherTrack);
```

---

## 資料表索引

### 效能關鍵索引

```sql
-- scores 表
CREATE INDEX idx_scores_student_id ON scores(student_id);
CREATE INDEX idx_scores_exam_id ON scores(exam_id);

-- exams 表
CREATE INDEX idx_exams_course_id ON exams(course_id);
CREATE INDEX idx_exams_term ON exams(term);
CREATE INDEX idx_exams_course_term ON exams(course_id, term);

-- courses 表
CREATE INDEX idx_courses_class_id ON courses(class_id);
CREATE INDEX idx_courses_teacher_id ON courses(teacher_id);
```

---

## 常見錯誤與解決

### 錯誤：406 Not Acceptable

**原因**：RLS 政策阻擋查詢
**解決**：檢查用戶角色權限，或使用 service role

### 錯誤：25P02 transaction aborted

**原因**：RLS 無限遞迴
**解決**：檢查政策是否查詢同一張表，使用 SECURITY DEFINER 函數

### 錯誤：Nested join 結果為空

**原因**：FK 欄位與過濾邏輯不匹配
**解決**：從正確的巢狀物件取得 class_id（見上方正確模式）

### 錯誤：查詢結果被截斷到 1000 筆

**原因**：Supabase PostgREST 的 `max_rows` 預設是 1000
**解決**：
1. Supabase Dashboard → API Settings → Max rows 設為 10000
2. 程式碼使用 `.range()` 分頁查詢：
```typescript
// 分頁查詢繞過 max_rows 限制
const PAGE_SIZE = 1000;
let page = 0;
let allData: any[] = [];
let hasMore = true;

while (hasMore) {
  const { data } = await supabase
    .from('scores')
    .select('exam_id')
    .in('exam_id', examIds)
    .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1);

  if (data && data.length > 0) {
    allData = allData.concat(data);
    page++;
    hasMore = data.length === PAGE_SIZE;
  } else {
    hasMore = false;
  }
}
```
