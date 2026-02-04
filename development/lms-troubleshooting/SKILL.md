---
name: lms-troubleshooting
description: Solved issues, common errors, and debugging techniques for LMS. Use this skill when debugging issues, understanding error codes, fixing RLS problems, or troubleshooting environment variable issues.
---

# LMS Troubleshooting Skill

> 已解決問題、常見錯誤、除錯技巧
> Last Updated: 2025-12-29

## Statistics 頁面成績不顯示

### 問題描述

- `/browse/stats/students`、`/browse/stats/classes`、`/browse/stats/grades` 頁面顯示 1514 學生但成績全為 "-"
- Gradebook 頁面正常顯示成績

### 根本原因

Supabase nested join 語法理解錯誤：
- 錯誤使用 `exam.class_id` 配合 `course:courses!inner`
- Supabase 的 `courses!inner` 透過 `course_id` FK 連接，不是 `class_id`

### 解決方案

```typescript
// 錯誤
exam:exams!inner(
  class_id,  // 這個欄位與 courses!inner 無關
  course:courses!inner(course_type)
)
// 然後過濾 exam.class_id → 永遠不匹配

// 正確
exam:exams!inner(
  course_id,
  course:courses!inner(
    class_id,  // 從 course 取得 class_id
    course_type
  )
)
// 過濾 exam.course.class_id
```

### 修改檔案

`lib/api/statistics.ts`

---

## Browse 頁面無限載入

### 問題描述

Browse 頁面從其他頁面導航進入時出現無限載入，必須重新整理才能顯示資料。

### 根本原因

1. Next.js client-side navigation 時，React 可能重用組件實例
2. `useRef` 值在導航之間保持不變
3. Debounce effect 造成雙重 fetch

### 解決方案：debouncedSearch 模式

```typescript
// 1. 只對搜尋輸入做 debounce
const [debouncedSearch, setDebouncedSearch] = useState("");

useEffect(() => {
  const timer = setTimeout(() => setDebouncedSearch(searchQuery), 300);
  return () => clearTimeout(timer);
}, [searchQuery]);

// 2. 單一 effect 處理所有資料抓取
useEffect(() => {
  if (authLoading || !user) return;

  let isCancelled = false;

  async function fetchData() {
    setLoading(true);
    try {
      const data = await apiCall({
        grade: selectedGrade === "All" ? undefined : selectedGrade,
        search: debouncedSearch || undefined,
      });
      if (!isCancelled) {
        setData(data);
        setLoading(false);
      }
    } catch (err) {
      if (!isCancelled) {
        setError(err.message);
        setLoading(false);
      }
    }
  }

  fetchData();
  return () => { isCancelled = true; };
}, [authLoading, user, selectedGrade, debouncedSearch]);
```

### 重點

- 搜尋框需要 debounce，下拉選單不需要
- 使用 `isCancelled` flag 取消過時請求
- 直接在依賴陣列列出狀態

---

## RLS 無限遞迴

### 問題描述

- Migration 015/017 的 policies 造成無限遞迴
- SSO 登入成功但查詢 users 表返回 500 錯誤
- 錯誤碼：25P02（transaction aborted）

### 根本原因

```sql
-- 政策的 USING clause 調用函式查詢 users 表
CREATE POLICY "heads_view_jurisdiction" ON users
USING (
  is_head() AND get_user_grade() = grade  -- 這兩個函式查詢 users 表！
);
-- → 觸發 policy → 無限循環
```

### 解決方案

**Migration 019e**：移除 heads_view_jurisdiction policy
**Migration 028**：刪除 24 個有遞迴問題的 policies，建立簡單的 `authenticated_read_users` 政策

```sql
-- 簡單政策，不查詢 users 表
CREATE POLICY "authenticated_read_users" ON users
FOR SELECT USING (auth.role() = 'authenticated');
```

---

## RLS 簡化（Migration 036/037）

### 問題描述

- RLS policies 過於複雜（100+ policies），難以維護
- 複雜的跨表查詢造成效能問題和遞迴風險
- MAP 資料不顯示（map_assessments 表缺少 policies）

### 解決方案

**Migration 036**：RLS 簡化
- 從 100+ policies 減少至 ~30 policies
- 建立 `is_admin()` helper function
- 每張表最多 4 個 policies

**Migration 037**：補齊遺漏表
- 為 12 個遺漏表新增 RLS policies
- 修復 MAP 資料不顯示問題

### 新架構：四層安全

```
1. Authentication (Supabase Auth)
2. RLS (粗粒度：authenticated_read, admin_full_access)
3. Application Layer (lib/api/permissions.ts)
4. Frontend (AuthGuard)
```

細粒度權限（Head 年級過濾、Teacher 課程過濾）移至 Application Layer，使用 `requireAuth()`, `requireRole()`, `filterByRole()` 函數。

---

## Claude Code 環境變數快取

### 問題描述

- Claude Code 會將 `.env.local` 內容儲存在會話歷史檔案中
- 即使更新 `.env.local`，Next.js 編譯時仍使用舊值
- 導致客戶端 JavaScript bundle 硬編碼錯誤的 Supabase URL

### 症狀識別

```bash
# 檢查 Shell 環境變數
env | grep SUPABASE
# 如果顯示舊 URL，表示遇到快取問題

# 檢查編譯產物
grep -r "old-project-id.supabase.co" .next/static/chunks/
# 如果找到舊 URL，表示 webpack 使用了錯誤的環境變數
```

### 解決方案

**方案 A**：清除 Claude Code 會話快取（推薦）
```bash
rm -f ~/.claude/projects/-Users-chenzehong-Desktop-LMS/*.jsonl
# 重啟 Cursor/VSCode
```

**方案 B**：使用外部終端機（繞過 Claude Code）
```bash
# 在系統終端機（非 Claude Code）中執行
cd /Users/chenzehong/Desktop/LMS
npm run dev
```

---

## Gradebook 406 Error

### 問題描述

Gradebook 頁面載入時出現 406 Not Acceptable 錯誤。

### 根本原因

GradebookHeader 組件查詢 courses 表觸發 RLS 衝突。

### 解決方案

移除 GradebookHeader 中的 courses 查詢，改用從父組件傳入的資料。

---

## Signal 10 (git push 錯誤)

### 問題描述

`git push` 命令偶爾返回 Signal 10 錯誤。

### 根本原因

Claude Code 的 Bash 工具在長時間操作時可能被中斷。

### 解決方案

```bash
# 方案 1：使用外部終端機
# 在系統終端機執行 git push

# 方案 2：重試
git push origin develop
```

---

## 常見錯誤代碼

| 錯誤碼 | 說明 | 解決方案 |
|--------|------|----------|
| 406 | RLS 阻擋查詢 | 檢查用戶角色權限 |
| 500 | 伺服器錯誤 | 檢查 console log |
| 25P02 | RLS 無限遞迴 | 使用 SECURITY DEFINER 函數 |
| 42P01 | 表不存在 | 執行 migration |
| 42501 | 權限不足 | 檢查 service role key |

---

## 除錯技巧

### 檢查 Auth 狀態

```typescript
const { userId, role, isReady } = useAuthReady();
console.log('[Auth]', { userId, role, isReady });
```

### 檢查 RLS 行為

```sql
-- 以特定用戶身份查詢
SET request.jwt.claims = '{"sub": "user-uuid", "role": "authenticated"}';
SELECT * FROM some_table;
```

### 檢查 Supabase 查詢

```typescript
const { data, error } = await supabase.from('...').select('...');
if (error) {
  console.error('[Supabase Error]', error.code, error.message, error.hint);
}
```

### 檢查 Build 產物

```bash
# 搜尋硬編碼的環境變數
grep -r "supabase.co" .next/static/chunks/ | head -5
```

---

## Staging/Production Schema 不一致

### 問題描述

- Staging 的 `exams` 表有 `class_id` 和 `course_id` 兩個欄位
- Production 的 `exams` 表只有 `course_id` 欄位
- 查詢 `exams.class_id` 在 Production 返回 400 Bad Request

### 根本原因

Production 資料庫先上線，結構是正確的（exams → courses → classes）。
Staging 資料庫後來建立時，添加了冗餘的 `class_id` 欄位。

### 解決方案

**Migration 035**：同步 Staging 結構至 Production 標準

```sql
-- 刪除 class_id 欄位
ALTER TABLE exams DROP COLUMN IF EXISTS class_id CASCADE;

-- 設定 course_id 為 NOT NULL
ALTER TABLE exams ALTER COLUMN course_id SET NOT NULL;

-- 重命名 is_published 為 is_active
ALTER TABLE exams RENAME COLUMN is_published TO is_active;
```

### 程式碼修正

**所有使用 `exams.class_id` 的查詢需改為 nested join**：

```typescript
// 錯誤（Production 會返回 400）
.select(`
  exam:exams!inner(
    class_id,
    course:courses!inner(...)
  )
`)

// 正確
.select(`
  exam:exams!inner(
    course_id,
    course:courses!inner(
      class_id,
      course_type
    )
  )
`)
```

### 修改檔案清單

- `app/(lms)/student/[id]/page.tsx`
- `lib/analytics/core.ts`
- `lib/analytics/queries.ts`

---

## 400 Error 查詢不存在的欄位

### 問題描述

查詢 Supabase 返回 400 Bad Request，錯誤訊息類似：
```
column exams.class_id does not exist
```

### 根本原因

程式碼嘗試查詢不存在於資料庫中的欄位。

### 解決方案

1. 確認欄位是否存在於資料表中
2. 檢查 Migration 035 是否已執行
3. 如需 class_id，使用 nested join 從 courses 表取得

### 檢查資料表結構

```bash
# 連接 Production 資料庫
psql "postgresql://postgres.piwbooidofbaqklhijup:geonook8588@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

# 檢查 exams 表結構
\d exams
```
