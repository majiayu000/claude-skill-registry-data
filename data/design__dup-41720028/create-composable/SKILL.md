---
name: create-composable
description: Nuxt 4プロジェクトで再利用可能なComposableを作成する際のテンプレートとガイドライン
---

# Composable 作成スキル

このスキルは、「いぬいのうた」プロジェクトで再利用可能なComposition API ロジックを作成する際の標準パターンを提供します。

## 基本テンプレート

```typescript
// composables/useSomething.ts
export const useSomething = () => {
  const state = ref<Type>(initialValue);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchData = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      // ロジック実装
      state.value = result;
    } catch (e) {
      error.value = 'エラーメッセージ';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  return {
    state,
    loading,
    error,
    fetchData,
  };
};
```

## Composable の種類と用途

### 1. API通信用 Composable

```typescript
// composables/useSongs.ts
export const useSongs = () => {
  const songs = ref<Song[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchSongs = async (params?: SongSearchParams) => {
    loading.value = true;
    error.value = null;
    
    try {
      const data = await $fetch('/api/songs', { query: params });
      songs.value = data.results;
    } catch (e) {
      error.value = 'データの取得に失敗しました';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  return { songs, loading, error, fetchSongs };
};
```

### 2. 状態管理用 Composable

```typescript
// composables/useToggle.ts
export const useToggle = (initialValue = false) => {
  const state = ref(initialValue);

  const toggle = () => {
    state.value = !state.value;
  };

  const setTrue = () => {
    state.value = true;
  };

  const setFalse = () => {
    state.value = false;
  };

  return {
    state,
    toggle,
    setTrue,
    setFalse,
  };
};
```

### 3. ビジネスロジック用 Composable

```typescript
// composables/usePlaybackControl.ts
export const usePlaybackControl = () => {
  const currentTime = ref(0);
  const duration = ref(0);
  const isPlaying = ref(false);

  const play = () => {
    isPlaying.value = true;
  };

  const pause = () => {
    isPlaying.value = false;
  };

  const seek = (time: number) => {
    currentTime.value = Math.max(0, Math.min(time, duration.value));
  };

  const progress = computed(() => {
    return duration.value > 0 ? currentTime.value / duration.value : 0;
  });

  return {
    currentTime,
    duration,
    isPlaying,
    progress,
    play,
    pause,
    seek,
  };
};
```

## 作成手順

### 1. ファイル配置

- **場所**: `app/composables/`
- **命名規則**: `use` プレフィックス + PascalCase
- **例**: `useSongs.ts`, `usePlayer.ts`, `usePlaylist.ts`

### 2. 型定義の作成

```typescript
// composables/useSongs.ts
import type { Song, SongSearchParams } from '~/types/api';

export const useSongs = () => {
  // 実装
};
```

### 3. 戻り値の型を明示

```typescript
interface UseSongsReturn {
  songs: Ref<Song[]>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  fetchSongs: (params?: SongSearchParams) => Promise<void>;
}

export const useSongs = (): UseSongsReturn => {
  // 実装
  return { songs, loading, error, fetchSongs };
};
```

### 4. 副作用の適切な管理

```typescript
export const useAutoFetch = (url: string) => {
  const data = ref(null);
  
  // ライフサイクルフックの使用
  onMounted(async () => {
    data.value = await $fetch(url);
  });
  
  // クリーンアップ
  onUnmounted(() => {
    // 必要に応じてクリーンアップ
  });
  
  return { data };
};
```

## 重要なルール

### 必須事項

✅ **`use` プレフィックス**
- すべてのComposableは `use` で始める

✅ **型安全性**
- 戻り値の型を明示
- ジェネリクスの活用

✅ **再利用性**
- 特定のコンポーネントに依存しない
- パラメータで挙動をカスタマイズ可能

✅ **エラーハンドリング**
- 非同期処理は必ずtry-catchで囲む
- エラー状態を返す

### Composables vs Stores の使い分け

**Composables を使うべき場合:**
- コンポーネントローカルな状態
- API通信ロジック
- 再利用可能なユーティリティ

**Stores を使うべき場合:**
- アプリケーション全体で共有する状態
- 複数コンポーネント間での同期が必要
- 永続化が必要な状態

## 実装パターン集

### パターン1: ページネーション付きAPI取得

```typescript
export const usePaginatedFetch = <T>(endpoint: string) => {
  const items = ref<T[]>([]);
  const page = ref(1);
  const totalPages = ref(1);
  const loading = ref(false);

  const fetchPage = async (pageNum: number) => {
    loading.value = true;
    try {
      const data = await $fetch(endpoint, {
        query: { page: pageNum }
      });
      items.value = data.results;
      totalPages.value = data.total_pages;
      page.value = pageNum;
    } finally {
      loading.value = false;
    }
  };

  return { items, page, totalPages, loading, fetchPage };
};
```

### パターン2: デバウンス検索

```typescript
export const useDebouncedSearch = (searchFn: (query: string) => Promise<void>) => {
  const query = ref('');
  const loading = ref(false);
  let timeoutId: NodeJS.Timeout;

  const search = (value: string) => {
    query.value = value;
    loading.value = true;
    
    clearTimeout(timeoutId);
    timeoutId = setTimeout(async () => {
      await searchFn(value);
      loading.value = false;
    }, 300);
  };

  onUnmounted(() => {
    clearTimeout(timeoutId);
  });

  return { query, loading, search };
};
```

### パターン3: ローカルストレージ連携

```typescript
export const useLocalStorage = <T>(key: string, initialValue: T) => {
  const state = ref<T>(initialValue);

  // 初期化時にローカルストレージから読み込み
  onMounted(() => {
    const stored = localStorage.getItem(key);
    if (stored) {
      state.value = JSON.parse(stored);
    }
  });

  // 状態が変わったら保存
  watch(state, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue));
  }, { deep: true });

  return state;
};
```

## チェックリスト

Composable作成完了時に確認：

- [ ] ファイル名は `use` プレフィックス
- [ ] `app/composables/` に配置
- [ ] 戻り値の型を明示
- [ ] エラーハンドリング実装
- [ ] 副作用を適切に管理（onMounted, onUnmounted等）
- [ ] 再利用性を考慮した設計
- [ ] TypeScript strictモード準拠
- [ ] 必要に応じてジェネリクス活用
