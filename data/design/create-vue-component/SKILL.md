---
name: create-vue-component
description: Nuxt 4プロジェクトで新しいVue 3コンポーネントを作成する際のテンプレートとガイドライン
---

# Vue 3 コンポーネント作成スキル

このスキルは、「いぬいのうた」プロジェクトでVue 3コンポーネントを作成する際の標準テンプレートと手順を提供します。

## 基本テンプレート

```vue
<script setup lang="ts">
interface Props {
  title: string;
  count: number;
}

interface Emits {
  (e: 'update', value: number): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const handleClick = () => {
  emit('update', props.count + 1);
};
</script>

<template>
  <div>
    <h2>{{ title }}</h2>
    <button @click="handleClick">Count: {{ count }}</button>
  </div>
</template>
```

## 作成手順

### 1. 配置場所を決定

- **汎用コンポーネント**: `app/components/`
- **レイアウト用**: `app/components/layout/` （自動的にグローバル登録される）
- **機能別**: `app/components/[feature]/` （例: `app/components/player/`）

### 2. ファイル名の決定

- **命名規則**: PascalCase
- **例**: `SongRow.vue`, `VideoPlayer.vue`, `PlaylistItem.vue`

### 3. コンポーネント構造

```vue
<script setup lang="ts">
// 1. Props定義（必須の場合）
interface Props {
  // Props型定義
}

// 2. Emits定義（イベント送信する場合）
interface Emits {
  (e: 'eventName', payload: PayloadType): void;
}

// 3. Props/Emitsの登録
const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 4. リアクティブな状態
const localState = ref<Type>(initialValue);
const computed = computed(() => {
  // 算出プロパティ
});

// 5. メソッド定義
const handleAction = () => {
  // ロジック
  emit('eventName', payload);
};

// 6. ライフサイクル（必要な場合）
onMounted(() => {
  // マウント時の処理
});
</script>

<template>
  <div class="container">
    <!-- UI実装 -->
  </div>
</template>
```

## 重要なルール

### 必須事項

✅ **TypeScript strict モード準拠**
- すべての Props と Emits に型定義
- `any` 型の使用禁止

✅ **Composition API**
- `<script setup>` を必ず使用
- Options API は使用禁止

✅ **単一責任の原則**
- 1コンポーネント = 1つの責務
- 複雑になったら分割を検討

✅ **Props/Emitsの明示**
- Props は読み取り専用として扱う
- 親への通知は Emits を使用

### 避けるべきパターン

❌ Options API (`data()`, `methods`, `computed`)
❌ Props の直接変更
❌ 直接的な DOM 操作
❌ グローバル状態への直接アクセス

## レイアウトコンポーネントの特別ルール

`app/components/layout/` 内のコンポーネントは自動的にグローバル登録されます：

```
app/components/layout/Header.vue  → <LayoutHeader />
app/components/layout/Footer.vue  → <LayoutFooter />
app/components/layout/Sidebar.vue → <LayoutSidebar />
```

## Composables の活用

複雑なロジックは Composables に抽出：

```typescript
// composables/useSomething.ts
export const useSomething = () => {
  const state = ref(initialValue);
  
  const action = () => {
    // ロジック
  };
  
  return { state, action };
};
```

コンポーネント内で使用：

```vue
<script setup lang="ts">
const { state, action } = useSomething();
</script>
```

## スタイリング

Tailwind CSS のユーティリティクラスを使用：

```vue
<template>
  <div class="flex items-center gap-4 p-4 bg-gray-100 rounded-lg">
    <h2 class="text-xl font-bold">{{ title }}</h2>
    <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      ボタン
    </button>
  </div>
</template>
```

レスポンシブデザイン：

```vue
<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- モバイル: 1列、タブレット: 2列、デスクトップ: 3列 -->
  </div>
</template>
```

## チェックリスト

コンポーネント作成完了時に確認：

- [ ] ファイル名は PascalCase
- [ ] `<script setup lang="ts">` を使用
- [ ] Props/Emits に型定義
- [ ] 単一責任を守っている
- [ ] Tailwind CSS でスタイリング
- [ ] レスポンシブ対応
- [ ] エラーハンドリング実装（非同期処理がある場合）
- [ ] ローディング状態の表示（データ取得がある場合）
