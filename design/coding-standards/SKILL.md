---
name: coding-standards
description: Flequit プロジェクトのコーディング標準への準拠をチェックします。命名規則、ファイル構造、型定義、エラーハンドリング、コメント、インポート順序などのコーディング標準チェックに使用します。
allowed-tools: Read, Edit, Bash(bun check:*), Bash(bun run lint:*)
model: sonnet
---

# Coding Standards Skill

Flequit プロジェクトのコーディング標準への準拠をチェックするスキルです。

## 命名規則

### TypeScript/JavaScript

```typescript
// ✅ OK: camelCase
const userName = 'john';
const taskList = [];
function getUserById(id: string) {}

// ✅ OK: PascalCase (クラス、型、コンポーネント)
class TaskManager {}
interface Task {}
type TaskStatus = 'todo' | 'in_progress' | 'completed';

// ✅ OK: SCREAM_SNAKE_CASE (定数)
const USER_ROLE_ADMIN = 'admin';
const MAX_RETRY_COUNT = 3;

// ❌ NG: snake_case（Rust以外では使用しない）
const user_name = 'john'; // camelCase にすべき
function get_user_by_id(id: string) {} // camelCase にすべき
```

### Rust

```rust
// ✅ OK: snake_case
let user_name = "john";
fn get_user_by_id(id: &str) {}

// ✅ OK: PascalCase (構造体、Enum)
struct TaskManager {}
enum TaskStatus {
    Todo,
    InProgress,
    Completed,
}

// ✅ OK: SCREAM_SNAKE_CASE (定数)
const USER_ROLE_ADMIN: &str = "admin";
const MAX_RETRY_COUNT: usize = 3;

// ❌ NG: camelCase（Rustでは使用しない）
let userName = "john"; // snake_case にすべき
fn getUserById(id: &str) {} // snake_case にすべき
```

### ファイル・ディレクトリ名

```
✅ OK: kebab-case
components/task-item.svelte
services/task-service.ts
repositories/task-repository.rs

❌ NG: camelCase や snake_case
components/TaskItem.svelte
services/task_service.ts
```

## ファイル構造

### ファイルサイズ制限

- **200行以上**: 必須分割対象（テストコード除外）
- **100行以上**: 分割を検討
- **例外**: 設定ファイル、データ定義

```typescript
// ❌ NG: 250行の巨大ファイル
// task-service.ts (250行)

// ✅ OK: 機能ごとに分割
// task-service.ts (120行)
// task-filter-service.ts (70行)
// task-sort-service.ts (60行)
```

### 単一責任原則

```typescript
// ✅ OK: 1ファイル1責任
// task-service.ts - タスク操作のみ
export class TaskService {
  async getTasks(projectId: string) { /* ... */ }
  async createTask(request: CreateTaskRequest) { /* ... */ }
}

// ❌ NG: 複数の責任
// app-service.ts - タスク、プロジェクト、ユーザー全部
export class AppService {
  async getTasks() { /* ... */ }
  async getProjects() { /* ... */ }
  async getUsers() { /* ... */ }
}
```

## 型定義

### 厳密な型指定

```typescript
// ✅ OK: 具体的な型
interface Task {
  id: string;
  title: string;
  status: 'todo' | 'in_progress' | 'completed';
  assignee?: User;
}

// ❌ NG: any を使用
interface Task {
  id: any; // string にすべき
  title: string;
  status: string; // Union type にすべき
  assignee: any; // User | undefined にすべき
}
```

### Optional vs Required

```typescript
// ✅ OK: 明確な区別
interface CreateTaskRequest {
  title: string;           // 必須
  description?: string;    // オプション
  dueDate?: Date;         // オプション
}

interface Task {
  id: string;             // 作成後は必須
  title: string;          // 必須
  description: string;    // 作成後は必須（空文字列でも）
  dueDate?: Date;        // 常にオプション
}
```

### Rust の型定義

```rust
// ✅ OK: 適切な derive
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: TaskId,
    pub title: String,
    pub status: TaskStatus,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TaskStatus {
    Todo,
    InProgress,
    Completed,
}
```

## エラーハンドリング

### TypeScript

```typescript
// ✅ OK: 明示的なエラーハンドリング
async function fetchTasks(): Promise<Task[] | null> {
  try {
    const response = await api.getTasks();
    return response.data;
  } catch (error) {
    console.error('Failed to fetch tasks:', error);
    return null;
  }
}

// ✅ OK: Result型パターン
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchTasksWithResult(): Promise<Result<Task[]>> {
  try {
    const data = await api.getTasks();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

// ❌ NG: エラーを無視
async function fetchTasks(): Promise<Task[]> {
  const response = await api.getTasks(); // エラーが throw される可能性
  return response.data;
}
```

### Rust

```rust
// ✅ OK: カスタムエラー型
#[derive(Debug, thiserror::Error)]
pub enum ServiceError {
    #[error("Resource not found: {0}")]
    NotFound(String),

    #[error("Validation failed: {0}")]
    Validation(String),

    #[error("Repository error: {0}")]
    Repository(#[from] RepositoryError),
}

pub type ServiceResult<T> = Result<T, ServiceError>;

// ✅ OK: エラーの伝播
pub async fn get_task(id: &TaskId) -> ServiceResult<Task> {
    let task = repository.find_by_id(id).await?
        .ok_or_else(|| ServiceError::NotFound("Task not found".to_string()))?;
    Ok(task)
}

// ❌ NG: unwrap でパニック
pub async fn get_task(id: &TaskId) -> Task {
    repository.find_by_id(id).await.unwrap().unwrap() // パニックの可能性
}
```

## インポート順序

### TypeScript

```typescript
// 1. Node modules
import { invoke } from '@tauri-apps/api/tauri';
import { writable } from 'svelte/store';

// 2. Internal libraries ($lib で始まる)
import type { Task } from '$lib/types';
import { taskService } from '$lib/services/task-service';
import TaskItem from '$lib/components/task-item.svelte';

// 3. Relative paths（エイリアスがない場合のみ）
import './component.css';
```

### Svelte コンポーネントのインポート

```typescript
// ✅ OK: エイリアスを使用
import TaskItem from '$lib/components/task-item.svelte';
import Textbox from '$lib/components/ui/textbox.svelte';

// ❌ NG: 相対パス（エイリアスがある場合）
import TaskItem from '../../components/task-item.svelte';

// ✅ OK: エイリアスがない場合のみ相対パス許可
// src/routes/tasks/+page.svelte
import LocalHelper from './local-helper.svelte';
```

### Rust

```rust
// 1. 標準ライブラリ
use std::collections::HashMap;
use std::sync::Arc;

// 2. 外部 crate
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;

// 3. 自 crate
use crate::models::task::Task;
use crate::services::task_service;

// 4. 親モジュール
use super::repository::TaskRepository;
```

## コメント

### TypeScript

```typescript
/**
 * ユーザーのタスク一覧を取得
 *
 * @param userId - 対象ユーザーのID
 * @param options - 取得オプション
 * @returns Promise<Task[]> - タスク一覧
 *
 * @example
 * ```typescript
 * const tasks = await getUserTasks('user-123', { includeCompleted: false });
 * ```
 */
export async function getUserTasks(
  userId: string,
  options: GetTasksOptions = {}
): Promise<Task[]> {
  // 実装
}
```

### Rust

```rust
/// タスクの進捗を計算
///
/// # Arguments
///
/// * `completed_tasks` - 完了タスク数
/// * `total_tasks` - 総タスク数
///
/// # Returns
///
/// 進捗パーセンテージ (0-100)
///
/// # Examples
///
/// ```
/// let progress = calculate_progress(3, 10);
/// assert_eq!(progress, 30);
/// ```
pub fn calculate_progress(completed_tasks: usize, total_tasks: usize) -> u8 {
    if total_tasks == 0 {
        return 0;
    }
    ((completed_tasks * 100) / total_tasks) as u8
}
```

## 関数・メソッド

### 純粋関数の推奨

```typescript
// ✅ OK: 純粋関数
function calculateProgress(completedTasks: number, totalTasks: number): number {
  if (totalTasks === 0) return 0;
  return Math.round((completedTasks / totalTasks) * 100);
}

// ✅ OK: 副作用が必要な場合は明確に分離
function updateTaskInStore(task: Task): void {
  taskStore.updateTask(task);
}

// ❌ NG: 副作用を持つ関数（名前から推測できない）
function calculateProgressAndUpdate(completedTasks: number, totalTasks: number): number {
  const progress = Math.round((completedTasks / totalTasks) * 100);
  updateProgressUI(progress); // 副作用 - 名前から推測できない
  return progress;
}
```

## Svelte 5 パターン

### Props 定義

```typescript
// ✅ OK: 明確な Props interface
<script lang="ts">
  interface Props {
    task: Task;
    readonly?: boolean;
    onUpdate?: (task: Task) => void;
    onDelete?: (taskId: string) => void;
  }

  let {
    task,
    readonly = false,
    onUpdate = () => {},
    onDelete = () => {}
  }: Props = $props();
</script>
```

### State 管理

```typescript
// ✅ OK: $state と $derived の適切な使用
let isEditing = $state<boolean>(false);
let formData = $state<CreateTaskRequest>({
  title: '',
  description: ''
});

const isFormValid = $derived(
  formData.title.trim().length > 0
);

// ❌ NG: 手動で状態を同期
let isFormValid = $state<boolean>(false);
$effect(() => {
  isFormValid = formData.title.trim().length > 0; // $derived を使うべき
});
```

## チェックリスト

### TypeScript/Svelte

- [ ] 変数・関数名は camelCase
- [ ] クラス・型名は PascalCase
- [ ] 定数は SCREAM_SNAKE_CASE
- [ ] ファイル名は kebab-case
- [ ] ファイルサイズが200行以下
- [ ] any 型を使用していない
- [ ] エラーハンドリングが適切
- [ ] インポート順序が正しい
- [ ] Svelte コンポーネントのインポートにエイリアス使用
- [ ] $state, $derived を適切に使用

### Rust

- [ ] 変数・関数名は snake_case
- [ ] 構造体・Enum は PascalCase
- [ ] 定数は SCREAM_SNAKE_CASE
- [ ] ファイル名は snake_case
- [ ] 適切な derive を使用
- [ ] unwrap を避けて ? 演算子使用
- [ ] カスタムエラー型を定義
- [ ] インポート順序が正しい

### 共通

- [ ] 単一責任原則に従っている
- [ ] 適切なコメントが記述されている
- [ ] テストが書かれている
- [ ] ドキュメントが更新されている

## Lint/Format コマンド

### フロントエンド

```bash
# 型チェック
bun check

# Lint チェック
bun run lint

# Lint 自動修正
bun run lint:fix

# Format
bun run format
```

### バックエンド

```bash
# 型チェック
cargo check

# Lint (clippy)
cargo clippy

# Format
cargo fmt

# Format チェック
cargo fmt --check
```

## 関連ドキュメント

詳細は以下のドキュメントを参照：
- `docs/en/develop/rules/coding-standards.md` - コーディング標準全体
- `docs/en/develop/rules/frontend.md` - フロントエンドルール
- `docs/en/develop/rules/backend.md` - バックエンドルール
- `docs/en/develop/design/frontend/svelte5-patterns.md` - Svelte 5 パターン
