---
name: lms-architecture
description: LMS-ESID core architecture including one-class-three-teachers system, course structure, grade levels, role permissions, and database schema. Use this skill when understanding teacher types (LT/IT/KCFS/HT), course relationships, class naming conventions, academic year data, or table relationships.
---

# LMS Architecture Skill

> LMS-ESID 專案的核心架構知識，包含一班三師系統、課程架構、年段系統
> Last Updated: 2025-12-22

## 一班三師系統 (One Class, Three Teachers)

### 教師類型定義

| 類型 | 全名 | 說明 |
|------|------|------|
| **LT** | Local Teacher | 本地教師，教授 English Language Arts (ELA) |
| **IT** | International Teacher | 國際教師，教授 English Language Arts (ELA) |
| **KCFS** | Kang Chiao Future Skill | 康橋未來技能課程，獨立課程類型 |
| **HT** | Head Teacher | 年段主任，管理特定年級的特定課程類型 |

### 課程架構

每個班級都包含三種標準課程：
1. **LT English Language Arts (ELA)** - 本地教師授課
2. **IT English Language Arts (ELA)** - 國際教師授課
3. **KCFS** - 康橋未來技能課程

### 資料表關聯

```
classes (84 班)
    ↓ 1:3
courses (252 筆 = 84 × 3 課程類型)
    ↓
exams → scores
```

### Track 欄位語意（重要！）

| 欄位 | 型別 | 語意 | 說明 |
|------|------|------|------|
| `classes.track` | `track_type` ENUM | **永遠為 NULL** | 班級不屬於任何單一 track |
| `users.track` | `course_type` ENUM | HT 課程類型職責 | LT/IT/KCFS，定義 HT 管理範圍 |
| `students.track` | `course_type` ENUM | **已棄用** | 設為 NULL，改用 `students.level` |
| `courses.course_type` | `course_type` ENUM | 實際課程類型 | LT/IT/KCFS |

### courses 表設計

```sql
CREATE TABLE courses (
  id UUID PRIMARY KEY,
  class_id UUID REFERENCES classes(id),
  course_type course_type NOT NULL,  -- 'LT' | 'IT' | 'KCFS'
  teacher_id UUID REFERENCES users(id),  -- 可為 NULL（待指派）
  academic_year TEXT,
  is_active BOOLEAN DEFAULT true
);
```

**工作流程**：課程建立（teacher_id = NULL）→ 教師指派（更新 teacher_id）

---

## 小學年段系統

### 年級範圍
- **Grade 1 至 Grade 6** (G1-G6)
- 每個年級 14 個班級
- 總計 84 個班級（林口校區）

### Level 分級格式

**格式**：`G[1-6]E[1-3]`

| Level |
|-------|
| E1 |
| E2 |
| E3 |

**重要**：不同年級的 E1 能力標準不同，只在同年級內比較 Level

**資料庫欄位**：TEXT 型別，帶 CHECK 約束驗證格式

### 班級命名格式

`G[1-6] [StandardName]`

範例：
- G4 Seekers
- G6 Navigators
- G1 Explorers

---

## 學年資料架構

### 2025-2026 學年（當前）
- **班級數量**：84 個班級
- **課程數量**：252 筆（84 × 3）
- **教師指派**：✅ 已完成（80 位教師）

### 2026-2027 學年
- **班級數量**：84 個班級（從 2025-2026 複製）
- **課程數量**：252 筆（teacher_id = NULL）
- **教師指派**：⏳ 待新學年開始

### Level 分佈（2025-2026）

| 年級 | E1 | E2 | E3 |
|------|----|----|-----|
| G1 | 5 | 5 | 4 |
| G2 | 5 | 5 | 4 |
| G3 | 4 | 7 | 3 |
| G4 | 4 | 7 | 3 |
| G5 | 3 | 7 | 4 |
| G6 | 4 | 7 | 3 |

---

## 角色與權限架構

### 角色定義

| 角色 | 說明 | 權限範圍 |
|------|------|----------|
| **admin** | 系統管理員 | 全域存取 |
| **head** | 年段主任 | Grade + Course Type |
| **teacher** | 教師 | 自己任課班級 |
| **office_member** | 行政人員 | 唯讀全部 + 任課編輯 |

### Head Teacher 權限範例

G4 LT Head Teacher 可以：
- ✅ 查看所有 G4 年級班級
- ✅ 管理 G4 年級所有 LT 課程（14 個班級）
- ❌ 不能管理 G4 的 IT 或 KCFS 課程

### Office Member 雙重身份

行政人員可能同時是授課教師：
- **查看權限**：可查看所有班級、學生、成績（唯讀）
- **編輯權限**：若同時為授課教師，可編輯自己任課班級的成績

---

## 資料表 Schema 摘要

### 核心資料表

```
users          - 教師、管理員帳號
classes        - 班級資料
courses        - 課程（班級 × 課程類型）
students       - 學生資料
student_courses - 學生選課關聯
exams          - 考試/評量
scores         - 成績記錄
```

### 輔助資料表

```
assessment_codes   - 評量代碼定義 (FA1-8, SA1-4, FINAL, MID)
assessment_titles  - 評量顯示名稱覆寫
course_tasks       - 課程任務看板
communications     - 家長通訊記錄
gradebook_expectations - 成績預期設定
```

### MAP 資料表（NWEA MAP Growth，G3-G6 only）

```
map_assessments    - MAP 測驗成績
                     student_number, grade, course, rit_score, lexile_score
                     term_tested, academic_year, rapid_guessing_percent

map_goal_scores    - 目標領域分數
                     assessment_id, goal_name, goal_rit_range
```

### 點名系統資料表

```
attendance         - 點名記錄
                     student_id, course_id, date, period, status (P/L/A/S)

behavior_tags      - 行為標籤定義
                     name, type (positive/negative)

student_behaviors  - 學生行為記錄
                     student_id, course_id, tag_id, date
```

### 課表系統資料表

```
timetable_entries  - 課表項目
                     teacher_email, day, period, class_name, course_type, course_id

timetable_periods  - 節次時間定義
                     period_number, start_time, end_time
```

### 資料表關聯圖

```
                    ┌─────────────┐
                    │   classes   │
                    │   (84 班)   │
                    └──────┬──────┘
                           │ 1:3
                    ┌──────▼──────┐
                    │   courses   │
                    │  (252 課程) │
                    └──────┬──────┘
                           │ 1:N
                    ┌──────▼──────┐
                    │    exams    │
                    │ (course_id) │  ← 注意：沒有 class_id
                    └──────┬──────┘
                           │ 1:N
                    ┌──────▼──────┐
                    │   scores    │
                    └─────────────┘
```
