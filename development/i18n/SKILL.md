---
name: i18n
description: Inlang Paraglide を使用した国際化（i18n）対応を支援します。翻訳メッセージの追加、reactiveMessage の使用、言語切り替え実装、翻訳のテスト、パラメータ付きメッセージなどの国際化関連タスクに使用します。
model: sonnet
---

# Internationalization (i18n) Skill

Flequit プロジェクトの国際化（Inlang Paraglide）を支援するスキルです。

## システム概要

### 基本設定

- **フレームワーク**: Inlang Paraglide
- **サポート言語**: English (base), Japanese
- **設定ファイル**: `project.inlang/settings.json`
- **自動生成**: `bun run build` で翻訳ファイルを自動生成
- **リアクティブ対応**: リロード不要で即座に言語切り替え

### ディレクトリ構造

```
project.inlang/
├── settings.json           # Inlang 設定
└── messages/
    ├── en.json             # 英語メッセージ
    └── ja.json             # 日本語メッセージ

src/paraglide/              # 自動生成（Git除外）
├── messages/
│   ├── index.ts
│   ├── en.ts
│   └── ja.ts
└── runtime.ts

src/lib/stores/
└── locale.svelte.ts        # 言語状態管理
```

## 翻訳メッセージの追加

### 1. メッセージファイルに追加

```json
// project.inlang/messages/en.json
{
  "button_save": "Save",
  "button_cancel": "Cancel",
  "label_task_title": "Task Title",
  "error_network_failed": "Network request failed",
  "welcome_user": "Welcome, {username}!",
  "task_count": "You have {count} {count, plural, one {task} other {tasks}} remaining"
}

// project.inlang/messages/ja.json
{
  "button_save": "保存",
  "button_cancel": "キャンセル",
  "label_task_title": "タスクタイトル",
  "error_network_failed": "ネットワークリクエストに失敗しました",
  "welcome_user": "ようこそ、{username}さん！",
  "task_count": "{count}個のタスクが残っています"
}
```

### 2. ビルドして型を生成

```bash
bun run build
```

これにより `src/paraglide/messages/` に型付きメッセージ関数が自動生成されます。

## 基本的な使用方法

### 1. シンプルなメッセージ

```svelte
<script lang="ts">
  import * as m from '$paraglide/messages';
  import { reactiveMessage } from '$lib/stores/locale.svelte';

  // Reactive message を作成
  const msg_save = reactiveMessage(m.button_save());
  const msg_cancel = reactiveMessage(m.button_cancel());
</script>

<button>{$msg_save}</button>
<button>{$msg_cancel}</button>
```

### 2. パラメータ付きメッセージ

```svelte
<script lang="ts">
  import * as m from '$paraglide/messages';
  import { reactiveMessage } from '$lib/stores/locale.svelte';

  let username = 'John';

  // パラメータを動的に渡す
  const msg_welcome = reactiveMessage(() =>
    m.welcome_user({ username })
  );
</script>

<h1>{$msg_welcome}</h1>
```

### 3. 複数形対応メッセージ

```svelte
<script lang="ts">
  import * as m from '$paraglide/messages';
  import { reactiveMessage } from '$lib/stores/locale.svelte';

  let tasks = $state<Task[]>([]);

  // 数値に応じて複数形を切り替え
  const msg_count = reactiveMessage(() =>
    m.task_count({ count: tasks.length })
  );
</script>

<p>{$msg_count}</p>
```

## 高度な使用方法

### 1. 条件付き翻訳

```typescript
// ステータスに応じたメッセージ
const getStatusMessage = (status: TaskStatus) =>
  reactiveMessage(() => {
    switch (status) {
      case 'todo': return m.status_todo();
      case 'in_progress': return m.status_in_progress();
      case 'completed': return m.status_completed();
      default: return m.status_unknown();
    }
  });

// 使用例
const msg_status = getStatusMessage(task.status);
```

### 2. コンポーネントレベルのメッセージ管理

```typescript
// components/task-form.svelte
<script lang="ts">
  import * as m from '$paraglide/messages';
  import { reactiveMessage } from '$lib/stores/locale.svelte';

  // このコンポーネントで使用するメッセージをまとめる
  const messages = {
    title: reactiveMessage(m.label_task_title()),
    description: reactiveMessage(m.label_task_description()),
    save: reactiveMessage(m.button_save()),
    cancel: reactiveMessage(m.button_cancel()),
    placeholder_title: reactiveMessage(m.placeholder_task_title()),
    error_required: reactiveMessage(m.error_field_required())
  };
</script>

<form>
  <label>{$messages.title}</label>
  <input placeholder={$messages.placeholder_title} required />

  <label>{$messages.description}</label>
  <textarea></textarea>

  <div class="actions">
    <button type="button">{$messages.cancel}</button>
    <button type="submit">{$messages.save}</button>
  </div>
</form>
```

### 3. 動的メッセージ生成

```typescript
// タスクの状態に応じたメッセージを動的に生成
const getTaskStatusMessage = (task: Task) =>
  reactiveMessage(() => {
    const params = {
      taskName: task.title,
      assignee: task.assignee?.name || 'Unassigned'
    };

    switch (task.status) {
      case 'completed':
        return m.task_completed_message(params);
      case 'in_progress':
        return m.task_in_progress_message(params);
      default:
        return m.task_todo_message(params);
    }
  });
```

## 言語切り替えの実装

### 1. 言語選択コンポーネント

```svelte
<!-- components/language-selector.svelte -->
<script lang="ts">
  import { localeStore } from '$lib/stores/locale.svelte';
  import * as m from '$paraglide/messages';
  import { reactiveMessage } from '$lib/stores/locale.svelte';

  const msg_language = reactiveMessage(m.language_label());

  const languageOptions = [
    { code: 'en', name: 'English' },
    { code: 'ja', name: '日本語' }
  ];

  function handleLanguageChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    localeStore.setLocale(target.value);
  }
</script>

<div class="language-selector">
  <label for="language-select">{$msg_language}</label>
  <select
    id="language-select"
    value={localeStore.currentLocale}
    onchange={handleLanguageChange}
  >
    {#each languageOptions as option (option.code)}
      <option value={option.code}>
        {option.name}
      </option>
    {/each}
  </select>
</div>
```

### 2. アプリケーション起動時の言語復元

```svelte
<!-- app.svelte -->
<script lang="ts">
  import { localeStore } from '$lib/stores/locale.svelte';

  // 保存された言語設定を復元
  $effect(() => {
    localeStore.loadSavedLocale();
  });
</script>
```

## メッセージキーの命名規則

### パターン

```json
{
  "button_{action}": "Button labels",
  "label_{field}": "Form labels",
  "placeholder_{field}": "Input placeholders",
  "error_{type}": "Error messages",
  "status_{state}": "Status labels",
  "tooltip_{action}": "Tooltip text",
  "message_{context}": "User messages",
  "heading_{section}": "Section headings"
}
```

### 具体例

```json
{
  "button_save": "Save",
  "button_cancel": "Cancel",
  "button_delete": "Delete",
  "button_add_task": "Add Task",

  "label_task_title": "Task Title",
  "label_task_description": "Description",
  "label_due_date": "Due Date",

  "placeholder_search_tasks": "Search tasks...",
  "placeholder_task_title": "Enter task title",

  "error_network_failed": "Network request failed",
  "error_field_required": "This field is required",
  "error_invalid_email": "Invalid email address",

  "status_todo": "To Do",
  "status_in_progress": "In Progress",
  "status_completed": "Completed",

  "tooltip_add_task": "Add new task",
  "tooltip_delete_task": "Delete this task",

  "message_task_created": "Task created successfully",
  "message_task_deleted": "Task deleted successfully",

  "heading_task_list": "Task List",
  "heading_project_settings": "Project Settings"
}
```

## テストでの翻訳モック

### 正しいアプローチ

`beforeEach` で `setTranslationService()` を使用：

```typescript
import { test, expect, beforeEach } from 'vitest';
import { setTranslationService } from '$lib/stores/locale.svelte';
import { createUnitTestTranslationService, unitTestTranslations } from '../unit-translation-mock';

beforeEach(() => {
  setTranslationService(createUnitTestTranslationService());
});

test('翻訳が必要な関数のテスト', () => {
  expect(getStatusLabel('not_started')).toBe(unitTestTranslations.status_not_started);
});
```

### 重要なポイント

1. **`createUnitTestTranslationService()` を使用**: 専用サービスを使用
2. **プロパティ参照で比較**: `unitTestTranslations.some_key` を使用
3. **`afterEach` での復元不要**: 各ファイルが独立
4. **グローバルモック禁止**: `vitest.setup.ts` でモックしない

### 避けるべきアプローチ

```typescript
// ❌ NG: 直接モック（脆弱）
vi.mock('$paraglide/runtime', () => ({
  languageTag: () => 'en'
}));

// ❌ NG: グローバルモック（テスト間の干渉）
// vitest.setup.ts
vi.mock('$lib/stores/locale.svelte', () => ({ /* ... */ }));

// ✅ OK: 各テストファイルで setTranslationService を使用
beforeEach(() => {
  setTranslationService(createUnitTestTranslationService());
});
```

## パフォーマンス最適化

### 1. 頻繁に使用されるメッセージのみリアクティブ化

```typescript
// 共通メッセージは事前に作成
const commonMessages = {
  save: reactiveMessage(m.button_save()),
  cancel: reactiveMessage(m.button_cancel()),
  loading: reactiveMessage(m.status_loading())
};

// 特定のメッセージは必要な時のみ作成
const getSpecificMessage = (key: string) =>
  reactiveMessage(() => m[key]());
```

### 2. メッセージのプリロード

```typescript
// アプリ起動時に言語設定を復元
<script lang="ts">
  import { localeStore } from '$lib/stores/locale.svelte';

  $effect(() => {
    localeStore.loadSavedLocale();
  });
</script>
```

## チェックリスト

### メッセージ追加時

- [ ] 英語と日本語の両方を追加
- [ ] 命名規則に従っている（`prefix_description` 形式）
- [ ] パラメータが必要な場合は `{param}` 形式で定義
- [ ] 複数形が必要な場合は `plural` を使用
- [ ] `bun run build` で型を生成

### コンポーネント実装時

- [ ] `reactiveMessage()` でラップ
- [ ] `$` プレフィックスでアクセス
- [ ] パラメータが動的な場合は関数形式 `() => m.message({ param })`
- [ ] コンポーネントレベルでメッセージをまとめる

### テスト実装時

- [ ] `beforeEach` で `setTranslationService()` を呼び出し
- [ ] `unitTestTranslations` を使用して比較
- [ ] 文字列リテラルではなくプロパティ参照で比較
- [ ] グローバルモックを使用していない

## トラブルシューティング

### 1. メッセージが更新されない

```bash
# ビルドして型を再生成
bun run build
```

### 2. 型エラー: メッセージ関数が見つからない

```typescript
// ❌ NG: import が間違っている
import { button_save } from '$paraglide/messages/en';

// ✅ OK: 正しい import
import * as m from '$paraglide/messages';
const msg = reactiveMessage(m.button_save());
```

### 3. 言語切り替えが反映されない

```typescript
// reactiveMessage でラップされているか確認
// ❌ NG: 直接使用
const message = m.button_save(); // 言語切り替えで更新されない

// ✅ OK: reactiveMessage でラップ
const message = reactiveMessage(m.button_save()); // 更新される
```

## 関連ドキュメント

詳細は以下のドキュメントを参照：
- `docs/en/develop/design/frontend/i18n-system.md` - 国際化システム全体
- `docs/en/develop/design/testing.md` - テストでの翻訳モック
- `project.inlang/settings.json` - Inlang 設定
