---
name: lms-features
description: LMS feature implementations including Browse Gradebook, Course Kanban, Communications, Statistics Module, MAP Analytics, Teacher Schedule, and Attendance System. Use this skill when implementing or modifying these features, understanding their data structures, or debugging feature-specific issues.
---

# LMS Features Skill

> Browse Gradebook、Course Kanban、Communications、Statistics Module、MAP Analytics、Teacher Schedule
> Last Updated: 2025-12-29

## Browse Gradebook 架構

### 功能概述

監控全校班級的成績輸入進度：
- **Class-Based 視圖**：每班一行（84 班），取代舊版 exam-based（1000 筆）
- **LT/IT/KCFS 進度欄**：顯示三種課程的成績輸入完成率
- **狀態篩選**：On Track / Behind / Not Started
- **年級篩選**：G1-G6

### 資料結構

```typescript
interface ClassProgress {
  class_id: string;
  class_name: string;
  grade: number;
  student_count: number;
  lt_progress: number;      // 0-100%
  it_progress: number;      // 0-100%
  kcfs_progress: number;    // 0-100%
  lt_teacher: string | null;
  it_teacher: string | null;
  kcfs_teacher: string | null;
  overall_status: 'on_track' | 'behind' | 'not_started';
}
```

### 進度計算

```typescript
// 每個課程的進度 = 已輸入成績數 / (學生數 × expected_total)
// LT/IT: 從 gradebook_expectations 表取得，預設 13
// KCFS: 依年級 (G1-2: 4, G3-4: 5, G5-6: 6)
const progress = (scores_entered / (student_count * expected_total)) * 100;

// 狀態判定
if (lt >= 80 && it >= 80 && kcfs >= 80) return 'on_track';
if (lt > 0 || it > 0 || kcfs > 0) return 'behind';
return 'not_started';
```

### 批次查詢（重要）

因應 Supabase `max_rows` 限制（10,000），使用兩階段並行查詢：

```typescript
// Stage 1: 取得 exam IDs（依 term 過濾）
const { data: exams } = await supabase
  .from('exams')
  .select('id, course_id')
  .in('course_id', courseIds)
  .eq('term', filters.term);

// Stage 2: 分批並行查詢 scores
const EXAM_BATCH_SIZE = 500;
const batches = chunk(examIds, EXAM_BATCH_SIZE);
const batchResults = await Promise.all(
  batches.map(batch =>
    supabase.from('scores')
      .select('exam_id')
      .in('exam_id', batch)
      .not('score', 'is', null)
  )
);

// Aggregate by course_id
```

**效能**: ~100-150ms，可處理 26,000+ scores

### 相關檔案

| 檔案 | 說明 |
|------|------|
| `types/browse-gradebook.ts` | TypeScript 型別定義 |
| `lib/api/browse-gradebook.ts` | API：`getClassesProgress()` |
| `app/(lms)/browse/gradebook/page.tsx` | UI 元件 |

---

## Course Kanban 架構

### 功能概述

課程層級的任務看板：
- **Kanban 三欄**：To Do / In Progress / Done
- **拖曳排序**：使用 @dnd-kit/core
- **課程隔離**：綁定 `course_id`，教師只看自己的任務

### 資料表

```sql
CREATE TABLE course_tasks (
  id UUID PRIMARY KEY,
  course_id UUID REFERENCES courses(id),
  teacher_id UUID REFERENCES users(id),
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'todo',  -- 'todo' | 'in_progress' | 'done'
  due_date DATE,
  position INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 相關檔案

| 檔案 | 說明 |
|------|------|
| `types/course-tasks.ts` | TypeScript 型別定義 |
| `lib/api/course-tasks.ts` | CRUD API |
| `components/class/CourseKanban.tsx` | Kanban 元件 |

---

## Communications 架構

### 功能概述

課程層級的家長通訊追蹤：
- **LT 課程**：電話通訊追蹤（semester_start / midterm / final）
- **IT/KCFS 課程**：學生備忘功能

### 權限控制

| 角色 | 可見課程 | 可編輯 |
|------|----------|--------|
| Teacher | 自己任課的課程 | 是 |
| Head Teacher | 自己 track 類型的課程 | 否（唯讀） |
| Admin | 所有課程 | 是 |
| Office Member | 所有課程 | 否（唯讀） |

### 相關檔案

| 檔案 | 說明 |
|------|------|
| `db/migrations/024_create_communications.sql` | 資料表 + RLS |
| `app/(lms)/class/[classId]/communications/page.tsx` | UI 元件 |
| `components/os/ClassContextTabs.tsx` | Tab 導航 |

---

## Statistics Module

### 頁面結構

```
/browse/stats/
├── page.tsx           # 總覽 Dashboard
├── classes/page.tsx   # 班級統計
├── students/page.tsx  # 學生統計
├── grades/page.tsx    # 年級統計
├── teachers/page.tsx  # 教師統計
├── courses/page.tsx   # 課程統計
├── exams/page.tsx     # 考試統計
└── trends/page.tsx    # 趨勢分析
```

### GlobalFilterBar

全域篩選系統，支援：
- **學年選擇**：2025-2026 / 2026-2027
- **Term 選擇**：Term 1-4

```typescript
interface GlobalFilters {
  academicYear: string;   // '2025-2026'
  term: number | null;    // 1-4 或 null（全部）
}
```

### Four-Term 學期系統

| Term | 名稱 | Semester |
|------|------|----------|
| 1 | Fall Midterm（秋季期中） | 1 (Fall) |
| 2 | Fall Final（秋季期末） | 1 (Fall) |
| 3 | Spring Midterm（春季期中） | 2 (Spring) |
| 4 | Spring Final（春季期末） | 2 (Spring) |

### XLSX 匯出

所有統計頁面支援 XLSX 匯出：
```typescript
import * as XLSX from 'xlsx';

function exportToXLSX(data: any[], filename: string) {
  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Data');
  XLSX.writeFile(wb, `${filename}.xlsx`);
}
```

### 圖表類型

使用 Recharts：
- **BarChart**：班級/年級比較
- **LineChart**：趨勢分析
- **PieChart**：分佈統計
- **AreaChart**：累積進度
- **RadarChart**：多維度比較
- **ScatterChart**：相關性分析

---

## Class Context Tabs

### 導航結構

```
/class/[classId]/
├── overview     # 班級總覽（含 Kanban）
├── gradebook    # 成績簿
├── students     # 學生名冊
└── communications  # 通訊記錄
```

### Tab 元件

```typescript
// components/os/ClassContextTabs.tsx
const tabs = [
  { id: 'overview', label: 'Overview', path: `/class/${classId}` },
  { id: 'gradebook', label: 'Gradebook', path: `/class/${classId}/gradebook` },
  { id: 'students', label: 'Students', path: `/class/${classId}/students` },
  { id: 'communications', label: 'Communications', path: `/class/${classId}/communications` },
];
```

---

## 共用元件

### PageHeader

```typescript
interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: { label: string; href?: string }[];
  actions?: React.ReactNode;
}
```

### DataTable

```typescript
interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  searchable?: boolean;
  filterable?: boolean;
  exportable?: boolean;
}
```

### StatusBadge

```typescript
type Status = 'on_track' | 'behind' | 'not_started' | 'completed';

const statusColors = {
  on_track: 'bg-green-500',
  behind: 'bg-yellow-500',
  not_started: 'bg-gray-500',
  completed: 'bg-blue-500',
};
```

---

## MAP Analytics Module (v1.54.0)

### 功能概述

NWEA MAP Growth 數據分析系統：
- **學生頁面 MAP Tab**：G3-G6 學生的 MAP 分析（G1-2 無 MAP 測驗）
- **Benchmark Classification**：E1/E2/E3 分級
- **Growth Index**：Fall → Spring 成長指數
- **Goal Areas**：閱讀/語言能力目標領域分析
- **Lexile Level**：閱讀等級追蹤

### 資料表

```sql
-- MAP 測驗成績
CREATE TABLE map_assessments (
  id UUID PRIMARY KEY,
  student_number TEXT NOT NULL,        -- 學號
  student_id UUID REFERENCES students(id),
  grade INTEGER NOT NULL,              -- 測驗時年級
  course TEXT NOT NULL,                -- 'Reading' | 'Language Usage'
  rit_score INTEGER NOT NULL,          -- RIT 分數（100-350）
  lexile_score TEXT,                   -- Lexile（Reading only，如 '1190L'）
  term_tested TEXT NOT NULL,           -- 'Fall 2024-2025' 格式
  academic_year TEXT NOT NULL,
  map_term TEXT NOT NULL,              -- 'fall' | 'winter' | 'spring' (distinct from ELA term 1-4)
  rapid_guessing_percent DECIMAL(5,2), -- 快速猜測百分比
  UNIQUE(student_number, course, term_tested)
);

-- 目標領域分數
CREATE TABLE map_goal_scores (
  id UUID PRIMARY KEY,
  assessment_id UUID REFERENCES map_assessments(id),
  goal_name TEXT NOT NULL,             -- 如 'Informational Text'
  goal_rit_range TEXT                  -- 如 '161-170'
);
```

### Benchmark Classification（E1/E2/E3 分級）

使用**兩科平均**判定學生程度：

```typescript
// 平均分 = (Language Usage RIT + Reading RIT) / 2
// 使用「測驗年級」的門檻判定（不是當前年級）

// G3 門檻
const G3_THRESHOLDS = { E1: 206, E2: 183 };
// G4 門檻
const G4_THRESHOLDS = { E1: 213, E2: 191 };
// G5 門檻
const G5_THRESHOLDS = { E1: 218, E2: 194 };
// G6：無分級（畢業年級）

// 判定邏輯
if (avg >= threshold.E1) return 'E1';
if (avg >= threshold.E2) return 'E2';
return 'E3';
```

### Growth Index（成長指數）

```typescript
// 成長指數 = 實際成長 / 期望成長
const growthIndex = actualGrowth / expectedGrowth;

// 判定
if (growthIndex >= 1.0) return 'Above Expected';
if (growthIndex >= 0.8) return 'Near Expected';
return 'Below Expected';
```

### 學生頁面 MAP Tab 元件

路徑：`app/(lms)/student/[id]/page.tsx`

```typescript
// 只有 G3-G6 學生顯示 MAP Tab
{studentGrade >= 3 && (
  <StudentMapAnalysisTab studentId={studentId} grade={studentGrade} />
)}
```

元件位置：`components/map/student/`
- `StudentBenchmarkStatus.tsx` - Benchmark 狀態卡
- `StudentGrowthIndex.tsx` - 成長指數卡
- `StudentGoalAreas.tsx` - 目標領域強弱項
- `StudentLexileLevel.tsx` - Lexile 閱讀等級
- `StudentBenchmarkHistory.tsx` - Benchmark 歷史圖表
- `StudentPeerComparison.tsx` - 同儕比較

### API 層

```
lib/api/map-student-analytics.ts  - 學生層級 MAP 分析
lib/api/map-analytics.ts          - 學校層級 MAP 統計
lib/map/benchmarks.ts             - Benchmark 分級邏輯
lib/map/norms.ts                  - NWEA 國家常模
lib/map/goals.ts                  - 目標領域定義
lib/map/lexile.ts                 - Lexile 解析與分類
```

### Lexile 閱讀等級

```typescript
// Lexile 格式
'1190L'   // 標準格式
'BR400L'  // Beginning Reader 格式

// 七個等級
const LEXILE_BANDS = [
  { range: 'BR', label: 'Beginning Reader' },
  { range: '0-200', label: 'Early Reader' },
  { range: '200-400', label: 'Developing' },
  { range: '400-600', label: 'Intermediate' },
  { range: '600-800', label: 'Fluent' },
  { range: '800-1000', label: 'Advanced' },
  { range: '1000+', label: 'Proficient' },
];
```

### 權限控制

| 角色 | 查看範圍 |
|------|----------|
| Admin | 全校學生 |
| Office Member | 全校學生（唯讀）|
| Head Teacher | 管轄年級學生 |
| Teacher | 自己班級學生 |

---

## Teacher Schedule System (v1.56.0)

### 功能概述

教師課表系統，支援週視圖和今日視圖：
- **Weekly View**：5x8 格狀課表（週一到週五，8 節課）
- **Today View**：垂直列表，適合手機
- **Click-to-Navigate**：點擊課程直接進入點名或課程頁面
- **Current Period Highlight**：當前節次高亮顯示

### 頁面路徑

```
/schedule              # 教師課表頁面
```

### 課程類型與顏色

| 類型 | 顏色 | 點擊行為 |
|------|------|----------|
| English | 藍色 (`bg-blue-500`) | → 點名頁面 |
| KCFS | 翡翠綠 (`bg-emerald-500`) | → 課程頁面 |
| EV | 紫色 (`bg-purple-500`) | → 課程頁面 |

### 資料表

```sql
-- 課表項目
timetable_entries (
  teacher_email, teacher_name, day, period,
  class_name, course_type, course_id, academic_year
)

-- 節次時間
timetable_periods (
  period_number, start_time, end_time
)
```

### 相關檔案

| 檔案 | 說明 |
|------|------|
| `app/(lms)/schedule/page.tsx` | 主頁面 |
| `components/schedule/WeeklyTimetable.tsx` | 週視圖 |
| `components/schedule/TodaySchedule.tsx` | 今日視圖 |
| `components/schedule/TimetableCell.tsx` | 課表格子 |
| `lib/api/timetable.ts` | API 函數 |

### 權限控制

| 角色 | 可見範圍 |
|------|----------|
| Teacher | 自己的課表 |
| Head Teacher | 自己的課表 |
| Admin | 自己的課表 |

### 資料統計 (2025-2026)

- English: 1,064 筆 (100% 有 course_id)
- KCFS: 167 筆 (100% 有 course_id)
- EV: 56 筆 (不需 course_id)

---

## Attendance System (v1.56.0)

### 功能概述

課程點名系統，從課表點擊進入：
- **點名頁面**：顯示課程學生列表
- **狀態選擇**：P (出席) / L (遲到) / A (缺席) / S (病假)
- **行為標籤**：正向/負向行為記錄
- **批次儲存**：自動儲存點名狀態

### 頁面路徑

```
/class/[classId]/attendance    # 點名頁面（從課表進入）
```

### 點名狀態

| 代碼 | 英文 | 顏色 |
|------|------|------|
| P | Present | 綠色 |
| L | Late | 黃色 |
| A | Absent | 紅色 |
| S | Sick | 藍色 |

### 相關檔案

| 檔案 | 說明 |
|------|------|
| `app/(lms)/class/[classId]/attendance/page.tsx` | 點名頁面 |
| `components/attendance/AttendanceSheet.tsx` | 點名表元件 |
| `components/attendance/AttendanceStatusButton.tsx` | 狀態按鈕 |
| `components/attendance/BehaviorTagPicker.tsx` | 行為標籤選擇 |
| `lib/api/attendance.ts` | API 函數 |

### 權限控制

| 角色 | 可見範圍 |
|------|----------|
| Teacher | 自己的課程 |
| Head Teacher | 自己的課程 |
| Admin | 所有課程 |

### 資料表

```sql
-- 點名記錄
attendance (
  student_id, course_id, date, period,
  status, recorded_by, note
)

-- 行為標籤
behavior_tags (
  name, name_zh, type, icon, sort_order
)

-- 學生行為記錄
student_behaviors (
  student_id, course_id, tag_id, date, recorded_by
)
```
