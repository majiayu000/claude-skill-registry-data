---
name: create-api-endpoint
description: Django REST APIへのプロキシエンドポイントとそれを使用するComposableを作成する手順
---

# API エンドポイント作成スキル

このスキルは、「いぬいのうた」プロジェクトでDjango REST APIへのプロキシエンドポイントと、それを使用するComposableを作成する標準パターンを提供します。

## アーキテクチャ概要

```
クライアント → Composable → Nuxt Server API (プロキシ) → Django REST API
```

**なぜプロキシ層が必要か:**
- セキュリティ: Django APIのURLを隠蔽
- 型安全性: TypeScriptでレスポンス型を定義
- エラーハンドリング: 一貫したエラー処理
- 認証: 将来的な認証トークン管理の準備

## ステップ1: APIプロキシエンドポイントの作成

### 基本テンプレート（GET）

```typescript
// server/api/resource/index.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const query = getQuery(event);
  
  try {
    const response = await fetch(
      `${config.djangoApiUrl}/resource/?${new URLSearchParams(query as any)}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch data'
    });
  }
});
```

### ID指定取得（GET）

```typescript
// server/api/resource/[id].get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const id = getRouterParam(event, 'id');
  
  if (!id) {
    throw createError({
      statusCode: 400,
      message: 'ID is required'
    });
  }
  
  try {
    const response = await fetch(
      `${config.djangoApiUrl}/resource/${id}/`
    );
    
    if (!response.ok) {
      throw createError({
        statusCode: response.status,
        message: `Resource not found: ${id}`
      });
    }
    
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch resource'
    });
  }
});
```

### 作成（POST）

```typescript
// server/api/resource/index.post.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const body = await readBody(event);
  
  try {
    const response = await fetch(
      `${config.djangoApiUrl}/resource/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    );
    
    if (!response.ok) {
      throw createError({
        statusCode: response.status,
        message: 'Failed to create resource'
      });
    }
    
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
});
```

### 更新（PUT）

```typescript
// server/api/resource/[id].put.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const id = getRouterParam(event, 'id');
  const body = await readBody(event);
  
  try {
    const response = await fetch(
      `${config.djangoApiUrl}/resource/${id}/`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    );
    
    if (!response.ok) {
      throw createError({
        statusCode: response.status,
        message: 'Failed to update resource'
      });
    }
    
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
});
```

### 削除（DELETE）

```typescript
// server/api/resource/[id].delete.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const id = getRouterParam(event, 'id');
  
  try {
    const response = await fetch(
      `${config.djangoApiUrl}/resource/${id}/`,
      {
        method: 'DELETE',
      }
    );
    
    if (!response.ok) {
      throw createError({
        statusCode: response.status,
        message: 'Failed to delete resource'
      });
    }
    
    return { success: true };
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
});
```

## ステップ2: 型定義の作成

```typescript
// app/types/api.ts

// 検索パラメータ
export interface ResourceSearchParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}

// レスポンス型
export interface Resource {
  id: string;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

// ページネーション付きレスポンス
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// 作成・更新用の型
export interface CreateResourceInput {
  name: string;
  description: string;
}

export interface UpdateResourceInput extends Partial<CreateResourceInput> {
  id: string;
}
```

## ステップ3: Composableの作成

```typescript
// composables/useResources.ts
import type { 
  Resource, 
  ResourceSearchParams, 
  PaginatedResponse,
  CreateResourceInput,
  UpdateResourceInput 
} from '~/types/api';

export const useResources = () => {
  const resources = ref<Resource[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const totalCount = ref(0);

  // 一覧取得
  const fetchResources = async (params?: ResourceSearchParams) => {
    loading.value = true;
    error.value = null;
    
    try {
      const data = await $fetch<PaginatedResponse<Resource>>('/api/resource', {
        query: params,
      });
      resources.value = data.results;
      totalCount.value = data.count;
    } catch (e) {
      error.value = 'データの取得に失敗しました';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  // ID指定取得
  const fetchResource = async (id: string): Promise<Resource | null> => {
    loading.value = true;
    error.value = null;
    
    try {
      const data = await $fetch<Resource>(`/api/resource/${id}`);
      return data;
    } catch (e) {
      error.value = 'データの取得に失敗しました';
      console.error(e);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // 作成
  const createResource = async (input: CreateResourceInput): Promise<Resource | null> => {
    loading.value = true;
    error.value = null;
    
    try {
      const data = await $fetch<Resource>('/api/resource', {
        method: 'POST',
        body: input,
      });
      return data;
    } catch (e) {
      error.value = '作成に失敗しました';
      console.error(e);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // 更新
  const updateResource = async (input: UpdateResourceInput): Promise<Resource | null> => {
    loading.value = true;
    error.value = null;
    
    try {
      const data = await $fetch<Resource>(`/api/resource/${input.id}`, {
        method: 'PUT',
        body: input,
      });
      return data;
    } catch (e) {
      error.value = '更新に失敗しました';
      console.error(e);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // 削除
  const deleteResource = async (id: string): Promise<boolean> => {
    loading.value = true;
    error.value = null;
    
    try {
      await $fetch(`/api/resource/${id}`, {
        method: 'DELETE',
      });
      return true;
    } catch (e) {
      error.value = '削除に失敗しました';
      console.error(e);
      return false;
    } finally {
      loading.value = false;
    }
  };

  return {
    resources,
    loading,
    error,
    totalCount,
    fetchResources,
    fetchResource,
    createResource,
    updateResource,
    deleteResource,
  };
};
```

## ステップ4: コンポーネントでの使用

```vue
<script setup lang="ts">
const { resources, loading, error, fetchResources } = useResources();

// ページマウント時にデータ取得
onMounted(() => {
  fetchResources({ page: 1, page_size: 20 });
});
</script>

<template>
  <div>
    <div v-if="loading">読み込み中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="resource in resources" :key="resource.id">
        {{ resource.name }}
      </div>
    </div>
  </div>
</template>
```

## 重要な注意点

### 環境変数の使用

プロキシエンドポイントでは必ず `useRuntimeConfig()` を使用：

```typescript
const config = useRuntimeConfig();
const djangoApiUrl = config.djangoApiUrl; // server側のみアクセス可能
```

### エラーハンドリング

- **サーバー側**: `createError()` でHTTPエラーを返す
- **クライアント側**: try-catchでエラーメッセージを表示

### クエリパラメータの型安全性

```typescript
const query = getQuery(event);
// query は Record<string, string | string[]> 型

// 型安全に変換
const params = {
  search: typeof query.search === 'string' ? query.search : undefined,
  page: query.page ? Number(query.page) : 1,
};
```

## チェックリスト

API エンドポイント作成完了時に確認：

- [ ] `server/api/` にプロキシエンドポイント作成
- [ ] 環境変数 `runtimeConfig.djangoApiUrl` を使用
- [ ] エラーハンドリング実装
- [ ] 型定義を `app/types/` に作成
- [ ] Composable を `app/composables/` に作成
- [ ] Composable で loading/error 状態を管理
- [ ] すべての非同期処理に try-catch
- [ ] TypeScript strict モード準拠
