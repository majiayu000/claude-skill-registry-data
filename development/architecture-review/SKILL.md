---
name: architecture-review
description: Flequit のクリーンアーキテクチャ、レイヤードアーキテクチャへの準拠をチェックします。レイヤー間の依存関係、crate 間のアクセス制御、Store と Service の分離、アンチパターンの検出などのアーキテクチャレビューに使用します。
model: sonnet
---

# Architecture Review Skill

Flequit プロジェクトのアーキテクチャ準拠をチェックするスキルです。

## アーキテクチャ概要

### バックエンド: クリーンアーキテクチャ（Crate分離版）

```
Main Crate (flequit)
├── Application Layer (commands, controllers, events)
    ↓
flequit-core Crate
├── Domain Layer (facade → services)
    ↓
flequit-storage Crate
├── Data Access Layer (repositories)
```

### フロントエンド: レイヤードアーキテクチャ

```
UI Layer (Components)
    ↓
UI Service Layer (Orchestration, Side Effects)
    ↓
Store Layer (Reactive State)
    ↓
Backend Communication (Tauri Commands)
```

## バックエンド: Crate 間アクセス制御

### ルール

1. **Main Crate (flequit)**: `flequit-core` のみ参照可能
2. **flequit-core**: `flequit-storage` のみ参照可能
3. **flequit-storage**: 外部 crate 参照不可（完全独立）

### Crate 内アクセス制御

#### Main Crate (flequit)

```rust
// ✅ OK: Facade を参照
use flequit_core::facades::task;

#[tauri::command]
pub async fn get_tasks(project_id: String) -> Result<Vec<Task>, String> {
    task::get_tasks(&repositories, &project_id).await
}

// ❌ NG: Service を直接参照
use flequit_core::services::task_service; // Facade 経由で呼ぶべき

// ❌ NG: Repository を直接参照
use flequit_storage::repositories::task_repository; // Facade 経由で呼ぶべき
```

#### flequit-core Crate

```rust
// ✅ OK: Facade から Service を参照
// facades/task.rs
use crate::services::task_service;

pub async fn create_task(...) -> Result<Task, String> {
    task_service::create(&repositories, ...).await
}

// ✅ OK: Service から Repository を参照
// services/task_service.rs
use flequit_storage::repositories::task_repository;

pub async fn get_tasks(repositories: &R, project_id: &str) -> Result<Vec<Task>> {
    repositories.task().get_all(project_id).await
}

// ❌ NG: Service から Facade を参照
use crate::facades::task; // 循環参照

// ❌ NG: Facade から他の Facade を参照
use crate::facades::project; // Facade は他の Facade を参照しない
```

#### flequit-storage Crate

```rust
// ✅ OK: Repository 内での参照
use crate::models::task::Task;
use crate::errors::RepositoryError;

// ❌ NG: 外部 crate の参照
use flequit_core::services::...; // Storage は独立している
```

## フロントエンド: レイヤー分離チェック

### Store と UI Service の分離

#### Store: 純粋な状態管理のみ

```typescript
// ✅ OK: Reactive state のみ
export class TaskStore {
  private tasks = $state<Task[]>([]);

  get allTasks() {
    return this.tasks;
  }

  get completedTasks() {
    return $derived(this.tasks.filter(t => t.status === 'completed'));
  }

  // ✅ OK: 状態の更新メソッド
  setTasks(tasks: Task[]) {
    this.tasks = tasks;
  }

  addTask(task: Task) {
    this.tasks.push(task);
  }
}

// ❌ NG: Store が直接 invoke を呼ぶ
export class TaskStore {
  async loadTasks() {
    const tasks = await invoke('get_tasks'); // Service でやるべき
    this.tasks = tasks;
  }
}

// ❌ NG: Store が Service を import
import { taskService } from '$lib/services/task-service'; // UI Service でやるべき
```

#### UI Service: オーケストレーションと副作用

```typescript
// ✅ OK: Backend 通信と Store 更新の連携
export class TaskUIService {
  constructor(private store: TaskStore) {}

  async loadTasks(projectId: string): Promise<boolean> {
    try {
      const tasks = await invoke<Task[]>('get_tasks', { projectId });
      this.store.setTasks(tasks);
      return true;
    } catch (error) {
      console.error('Failed to load tasks:', error);
      return false;
    }
  }

  async createTask(request: CreateTaskRequest): Promise<boolean> {
    try {
      const task = await invoke<Task>('create_task', request);
      this.store.addTask(task);
      return true;
    } catch (error) {
      console.error('Failed to create task:', error);
      return false;
    }
  }
}

// ❌ NG: UI Service が状態を直接持つ
export class TaskUIService {
  private tasks = $state<Task[]>([]); // Store でやるべき
}
```

### コンポーネント: UI のみ

```typescript
// ✅ OK: UI Service 経由で操作
<script lang="ts">
  import { taskUIService } from '$lib/services/ui/task-ui-service';
  import { taskStore } from '$lib/stores/task.svelte';

  async function handleCreate() {
    const success = await taskUIService.createTask(formData);
    if (success) {
      // UI 更新
    }
  }
</script>

{#each taskStore.allTasks as task}
  <TaskItem {task} />
{/each}

// ❌ NG: コンポーネントが直接 invoke を呼ぶ
<script lang="ts">
  import { invoke } from '@tauri-apps/api/tauri';

  async function handleCreate() {
    await invoke('create_task', formData); // UI Service でやるべき
  }
</script>
```

## アンチパターン検出

### 1. 循環参照

```rust
// ❌ NG: Service が Facade を参照
// services/task_service.rs
use crate::facades::task; // 循環参照!

// ✅ OK: Facade が Service を参照
// facades/task.rs
use crate::services::task_service;
```

### 2. レイヤー飛び越し

```rust
// ❌ NG: Command が直接 Repository を参照
use flequit_storage::repositories::task_repository;

#[tauri::command]
pub async fn get_tasks() -> Result<Vec<Task>, String> {
    task_repository::get_all().await // Facade 経由で呼ぶべき
}

// ✅ OK: Command が Facade を参照
use flequit_core::facades::task;

#[tauri::command]
pub async fn get_tasks() -> Result<Vec<Task>, String> {
    task::get_all(&repositories).await
}
```

### 3. Store に副作用

```typescript
// ❌ NG: Store が副作用を持つ
export class TaskStore {
  async saveToBackend() {
    await invoke('save_tasks', { tasks: this.tasks }); // UI Service でやるべき
  }

  async syncWithServer() {
    const serverTasks = await fetch('/api/tasks'); // UI Service でやるべき
    this.tasks = await serverTasks.json();
  }
}

// ✅ OK: Store は純粋な状態管理のみ
export class TaskStore {
  private tasks = $state<Task[]>([]);

  setTasks(tasks: Task[]) {
    this.tasks = tasks;
  }
}
```

### 4. プロキシだけの Service

```typescript
// ❌ NG: 単なるプロキシ（価値なし）
export class TaskService {
  async getTasks(projectId: string) {
    return await invoke('get_tasks', { projectId }); // これだけなら不要
  }
}

// ✅ OK: オーケストレーション + 状態管理
export class TaskUIService {
  constructor(
    private taskStore: TaskStore,
    private projectStore: ProjectStore
  ) {}

  async loadTasksForCurrentProject(): Promise<boolean> {
    const project = this.projectStore.current;
    if (!project) return false;

    try {
      const tasks = await invoke<Task[]>('get_tasks', {
        projectId: project.id
      });
      this.taskStore.setTasks(tasks);
      return true;
    } catch (error) {
      console.error('Failed to load tasks:', error);
      return false;
    }
  }
}
```

## ファイルサイズチェック

### ルール

- **200行以上**: 必須分割対象（テストコード除外）
- **100行以上**: 分割を検討
- **例外**: 設定ファイル、データ定義

### 分割方法

```typescript
// ❌ NG: 200行を超える巨大ファイル
// task-service.ts (300行)

// ✅ OK: 機能ごとに分割
// task-ui-service.ts (150行)
// task-filter-service.ts (80行)
// task-sort-service.ts (70行)
```

## チェックリスト

### バックエンド

- [ ] Command は Facade のみ参照している
- [ ] Facade は Service のみ参照している
- [ ] Service は Repository を参照している
- [ ] Repository は外部 crate を参照していない
- [ ] 循環参照が存在しない
- [ ] トランザクションは Facade レイヤーで管理している

### フロントエンド

- [ ] Store は純粋な状態管理のみを行っている
- [ ] UI Service がオーケストレーションを担当している
- [ ] コンポーネントは UI Service 経由で操作している
- [ ] Store が直接 invoke を呼んでいない
- [ ] Store が Service を import していない
- [ ] 単なるプロキシ Service が存在しない

### 共通

- [ ] ファイルサイズが200行以下（テスト除く）
- [ ] 単一責任原則に従っている
- [ ] 命名規則に従っている（camelCase/snake_case）

## 関連ドキュメント

詳細は以下のドキュメントを参照：
- `docs/en/develop/design/architecture.md` - アーキテクチャ全体
- `docs/en/develop/design/backend-tauri/rust-guidelines.md` - Rust 設計ガイドライン
- `docs/en/develop/design/frontend/layers.md` - フロントエンドレイヤー
- `docs/en/develop/design/frontend/store-and-service-architecture.md` - Store と Service 分離
- `docs/en/develop/design/frontend/anti-patterns.md` - アンチパターン
- `docs/en/develop/rules/file-structure.md` - ファイル構造ルール
