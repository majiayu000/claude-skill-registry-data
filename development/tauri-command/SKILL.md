---
name: tauri-command
description: Tauri コマンドの実装を支援します。フロントエンドとバックエンド間の通信、invoke 関数の実装、camelCase から snake_case への自動変換、戻り値の統一パターンなど、Tauri 固有の実装パターンに使用します。
model: sonnet
---

# Tauri Command Implementation Skill

Flequit プロジェクトの Tauri コマンド実装を支援するスキルです。

## 重要: 命名規則の自動変換

Tauri は JavaScript の `camelCase` を自動的に Rust の `snake_case` に変換します。

### パラメータ命名ルール

**JavaScript 側（camelCase）** ⇔ **Rust 側（snake_case）**

```typescript
// JavaScript/TypeScript - camelCase を使用
await invoke('update_task', {
  projectId: 'project-123',        // Rust側: project_id
  taskId: 'task-456',             // Rust側: task_id
  partialSettings: {...}          // Rust側: partial_settings
});

await invoke('create_task_assignment', {
  taskAssignment: {               // Rust側: task_assignment
    task_id: 'task-123',
    user_id: 'user-456'
  }
});
```

```rust
// Rust側 - snake_case を使用
#[tauri::command]
pub async fn update_task(
    project_id: String,           // JavaScript側: projectId
    task_id: String,              // JavaScript側: taskId
    partial_settings: PartialSettings // JavaScript側: partialSettings
) -> Result<bool, String> {
    // 実装
}

#[tauri::command]
pub async fn create_task_assignment(
    task_assignment: TaskAssignment  // JavaScript側: taskAssignment
) -> Result<bool, String> {
    // 実装
}
```

## 戻り値の統一

### void コマンドの戻り値

```rust
// Rust側 - 成功時に () (Unit型) を返す
#[tauri::command]
pub async fn save_settings(settings: Settings) -> Result<(), String> {
    // 保存処理
    Ok(()) // Unit型を返す
}
```

```typescript
// JavaScript側 - 成功を true として扱う
async saveSettings(settings: Settings): Promise<boolean> {
  try {
    await invoke('save_settings', { settings });
    return true; // void成功 = true
  } catch (error) {
    console.error('Failed to save settings:', error);
    return false; // エラー = false
  }
}
```

## 統一エラーハンドリング

### TypeScript側のパターン

```typescript
// 汎用エラーハンドリングパターン
async function tauriServiceMethod<T>(
  command: string,
  params?: object
): Promise<T | null> {
  try {
    const result = await invoke(command, params) as T;
    return result;
  } catch (error) {
    console.error(`Failed to execute ${command}:`, error);
    return null;
  }
}

// boolean戻り値用
async function tauriBooleanMethod(
  command: string,
  params?: object
): Promise<boolean> {
  try {
    await invoke(command, params);
    return true;
  } catch (error) {
    console.error(`Failed to execute ${command}:`, error);
    return false;
  }
}
```

### Rust側のパターン

```rust
#[tauri::command]
pub async fn get_task(
    project_id: String,
    task_id: String
) -> Result<Task, String> {
    task_facade::get_task(&repositories, &project_id, &task_id)
        .await
        .map_err(|e| format!("Failed to get task: {:?}", e))
}

#[tauri::command]
pub async fn delete_task(
    project_id: String,
    task_id: String
) -> Result<bool, String> {
    task_facade::delete_task(&repositories, &project_id, &task_id)
        .await
        .map_err(|e| format!("Failed to delete task: {:?}", e))
}
```

## 実装チェックリスト

### JavaScript/TypeScript 実装

- [ ] パラメータ名を `camelCase` で記述
- [ ] Rust側の `snake_case` 関数パラメータに対応
- [ ] void戻り値コマンドは `true`/`false` で返す
- [ ] 適切なエラーハンドリングを実装
- [ ] コンソールログにエラー内容を出力

### Rust 実装

- [ ] 関数パラメータを `snake_case` で記述
- [ ] JavaScript側の `camelCase` パラメータに対応
- [ ] `Result<T, String>` でエラーを処理
- [ ] 適切なエラーメッセージを提供
- [ ] `#[tauri::command]` アトリビュートを追加

## 完全な実装例

### TypeScript側（Service）

```typescript
// src/lib/services/task-service.ts
import { invoke } from '@tauri-apps/api/tauri';
import type { Task, CreateTaskRequest } from '$lib/types';

export class TaskService {
  async getTasks(projectId: string): Promise<Task[] | null> {
    try {
      const tasks = await invoke<Task[]>('get_tasks', { projectId });
      return tasks;
    } catch (error) {
      console.error('Failed to get tasks:', error);
      return null;
    }
  }

  async createTask(request: CreateTaskRequest): Promise<Task | null> {
    try {
      const task = await invoke<Task>('create_task', {
        projectId: request.projectId,
        title: request.title,
        description: request.description
      });
      return task;
    } catch (error) {
      console.error('Failed to create task:', error);
      return null;
    }
  }

  async updateTask(
    projectId: string,
    taskId: string,
    updates: Partial<Task>
  ): Promise<boolean> {
    try {
      await invoke('update_task', {
        projectId,
        taskId,
        partialTask: updates
      });
      return true;
    } catch (error) {
      console.error('Failed to update task:', error);
      return false;
    }
  }

  async deleteTask(projectId: string, taskId: string): Promise<boolean> {
    try {
      const result = await invoke<boolean>('delete_task', {
        projectId,
        taskId
      });
      return result;
    } catch (error) {
      console.error('Failed to delete task:', error);
      return false;
    }
  }
}

export const taskService = new TaskService();
```

### Rust側（Command）

```rust
// src-tauri/src/commands/task.rs
use flequit_core::facades::task as task_facade;
use flequit_storage::models::command::task::{Task, PartialTask};

#[tauri::command]
pub async fn get_tasks(
    project_id: String,  // JavaScript: projectId
    state: tauri::State<'_, AppState>
) -> Result<Vec<Task>, String> {
    let repositories = &state.repositories;

    task_facade::get_tasks(repositories, &project_id)
        .await
        .map_err(|e| format!("Failed to get tasks: {:?}", e))
}

#[tauri::command]
pub async fn create_task(
    project_id: String,  // JavaScript: projectId
    title: String,
    description: Option<String>,
    state: tauri::State<'_, AppState>
) -> Result<Task, String> {
    let repositories = &state.repositories;

    task_facade::create_task(
        repositories,
        &project_id,
        &title,
        description.as_deref()
    )
    .await
    .map_err(|e| format!("Failed to create task: {:?}", e))
}

#[tauri::command]
pub async fn update_task(
    project_id: String,   // JavaScript: projectId
    task_id: String,      // JavaScript: taskId
    partial_task: PartialTask,  // JavaScript: partialTask
    state: tauri::State<'_, AppState>
) -> Result<(), String> {
    let repositories = &state.repositories;

    task_facade::update_task(
        repositories,
        &project_id,
        &task_id,
        partial_task
    )
    .await
    .map_err(|e| format!("Failed to update task: {:?}", e))
}

#[tauri::command]
pub async fn delete_task(
    project_id: String,  // JavaScript: projectId
    task_id: String,     // JavaScript: taskId
    state: tauri::State<'_, AppState>
) -> Result<bool, String> {
    let repositories = &state.repositories;

    task_facade::delete_task(repositories, &project_id, &task_id)
        .await
        .map_err(|e| format!("Failed to delete task: {:?}", e))
}
```

### コマンド登録

```rust
// src-tauri/src/lib.rs
use crate::commands::task;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            task::get_tasks,
            task::create_task,
            task::update_task,
            task::delete_task,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## 注意事項

### 1. 自動変換の対象範囲

Tauri の自動変換は**パラメータ名のみ**に適用されます。以下は含まれません：

- Struct のフィールド名
- Enum のバリアント名

これらは手動で対応する必要があります。

### 2. 一貫性の維持

プロジェクト全体で同じパターンを使用してください：

- JavaScript: 常に `camelCase`
- Rust: 常に `snake_case`
- 型定義を TypeScript と Rust で一致させる

### 3. 型安全性

TypeScript の型定義と Rust の構造体定義を一致させます：

```typescript
// TypeScript
interface Task {
  id: string;
  title: string;
  status: 'todo' | 'in_progress' | 'completed';
}
```

```rust
// Rust
#[derive(Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    pub status: TaskStatus,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TaskStatus {
    Todo,
    InProgress,
    Completed,
}
```

### 4. テスト

実際の Tauri 環境でテストすることを推奨：

```bash
# Tauri dev モードで起動
bun run tauri dev

# ブラウザの開発者ツールでコマンドをテスト
await window.__TAURI__.invoke('get_tasks', { projectId: 'test' });
```

## 関連ドキュメント

詳細は以下のドキュメントを参照：
- `docs/en/develop/rules/coding-standards.md` - Tauri⇔Frontend通信ルール
- `docs/en/develop/design/backend-tauri/rust-guidelines.md` - Rust設計ガイドライン
- `docs/en/develop/design/error-handling.md` - エラーハンドリング
