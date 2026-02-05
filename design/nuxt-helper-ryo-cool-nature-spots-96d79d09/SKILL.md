---
name: nuxt-helper
description: Nuxt.js/Vue.js開発を支援するスキル。コンポーネント作成、Composition API、Pinia、Vuetify、i18nのベストプラクティスを提供します。
---

# Nuxt Helper Skill

Nature-Spotsプロジェクトにおける Nuxt.js/Vue.js 開発を効率化するスキルです。

## 機能

### 1. コンポーネント作成パターン

#### 基本的なコンポーネント（Composition API）

```vue
<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <slot />
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
interface Props {
  title: string
}

const props = defineProps<Props>()
</script>
```

#### フォームコンポーネント（v-model対応）

```vue
<template>
  <v-text-field
    :model-value="modelValue"
    :label="label"
    @update:model-value="emit('update:modelValue', $event)"
  />
</template>

<script setup lang="ts">
interface Props {
  modelValue: string
  label: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
</script>
```

#### リスト表示コンポーネント（v-for最適化）

```vue
<template>
  <div>
    <!-- ✅ keyにユニークなIDを使用 -->
    <spot-card
      v-for="spot in spots"
      :key="spot.id"
      :spot="spot"
      @click="handleClick(spot)"
    />
  </div>
</template>

<script setup lang="ts">
import type { Spot } from '~/types'

interface Props {
  spots: Spot[]
}

const props = defineProps<Props>()

const handleClick = (spot: Spot) => {
  // 処理
}
</script>
```

### 2. Composition API のベストプラクティス

#### Composableの作成

```typescript
// composables/useSpotSearch.ts
import { ref, computed } from 'vue'
import type { Spot } from '~/types'

export const useSpotSearch = () => {
  const query = ref('')
  const spots = ref<Spot[]>([])
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  const filteredSpots = computed(() => {
    if (!query.value) return spots.value
    return spots.value.filter((spot) =>
      spot.name.toLowerCase().includes(query.value.toLowerCase())
    )
  })

  const search = async (searchQuery: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await $fetch<Spot[]>('/api/v1/spots', {
        params: { q: searchQuery },
      })
      spots.value = response
    } catch (e) {
      error.value = e as Error
    } finally {
      isLoading.value = false
    }
  }

  return {
    query,
    spots,
    isLoading,
    error,
    filteredSpots,
    search,
  }
}
```

#### 使用例

```vue
<script setup lang="ts">
const { query, filteredSpots, isLoading, search } = useSpotSearch()

watch(query, (newQuery) => {
  if (newQuery.length >= 2) {
    search(newQuery)
  }
})
</script>
```

### 3. Pinia ストアの設計

#### ストアの作成（Composition Store）

```typescript
// stores/spot.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Spot } from '~/types'

export const useSpotStore = defineStore('spot', () => {
  // State
  const spots = ref<Spot[]>([])
  const currentSpot = ref<Spot | null>(null)
  const isLoading = ref(false)

  // Getters
  const favoriteSpots = computed(() =>
    spots.value.filter((spot) => spot.isFavorite)
  )

  const spotCount = computed(() => spots.value.length)

  // Actions
  const fetchSpots = async () => {
    isLoading.value = true
    try {
      const response = await $fetch<Spot[]>('/api/v1/spots')
      spots.value = response
    } finally {
      isLoading.value = false
    }
  }

  const setCurrentSpot = (spot: Spot) => {
    currentSpot.value = spot
  }

  const addSpot = (spot: Spot) => {
    spots.value.push(spot)
  }

  const reset = () => {
    spots.value = []
    currentSpot.value = null
  }

  return {
    // State
    spots,
    currentSpot,
    isLoading,
    // Getters
    favoriteSpots,
    spotCount,
    // Actions
    fetchSpots,
    setCurrentSpot,
    addSpot,
    reset,
  }
})
```

#### ストアの使用（storeToRefs）

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useSpotStore } from '~/stores/spot'

const spotStore = useSpotStore()

// ✅ リアクティビティを保持
const { spots, isLoading } = storeToRefs(spotStore)

// ✅ アクションは直接使用
const { fetchSpots, addSpot } = spotStore

onMounted(() => {
  fetchSpots()
})
</script>
```

### 4. Vuetify コンポーネントの活用

#### レスポンシブレイアウト

```vue
<template>
  <v-container>
    <v-row>
      <!-- モバイル: 12列（全幅）、タブレット: 6列（半分）、デスクトップ: 4列（1/3） -->
      <v-col
        v-for="spot in spots"
        :key="spot.id"
        cols="12"
        sm="6"
        md="4"
      >
        <spot-card :spot="spot" />
      </v-col>
    </v-row>
  </v-container>
</template>
```

#### フォームバリデーション

```vue
<template>
  <v-form ref="formRef" @submit.prevent="handleSubmit">
    <v-text-field
      v-model="name"
      :label="$t('spot.form.name')"
      :rules="[rules.required, rules.maxLength(50)]"
    />

    <v-textarea
      v-model="description"
      :label="$t('spot.form.description')"
      :rules="[rules.required]"
    />

    <v-btn type="submit" :loading="isSubmitting">
      {{ $t('common.submit') }}
    </v-btn>
  </v-form>
</template>

<script setup lang="ts">
const formRef = ref()
const name = ref('')
const description = ref('')
const isSubmitting = ref(false)

const rules = {
  required: (v: string) => !!v || 'Required',
  maxLength: (max: number) => (v: string) =>
    !v || v.length <= max || `Max ${max} characters`,
}

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  isSubmitting.value = true
  try {
    // API呼び出し
  } finally {
    isSubmitting.value = false
  }
}
</script>
```

#### ダイアログ管理

```vue
<template>
  <div>
    <v-btn @click="dialog = true">Open Dialog</v-btn>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ $t('dialog.title') }}</v-card-title>
        <v-card-text>
          <!-- コンテンツ -->
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">
            {{ $t('common.cancel') }}
          </v-btn>
          <v-btn color="primary" @click="handleConfirm">
            {{ $t('common.confirm') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
const dialog = ref(false)

const handleConfirm = () => {
  // 処理
  dialog.value = false
}
</script>
```

### 5. i18n（多言語対応）

#### コンポーネント内での使用

```vue
<template>
  <div>
    <!-- テンプレートで直接使用 -->
    <h1>{{ $t('spot.title') }}</h1>

    <!-- プレースホルダー付き -->
    <p>{{ $t('spot.count', { count: spots.length }) }}</p>

    <!-- 複数形対応 -->
    <p>{{ $tc('spot.review', reviewCount) }}</p>
  </div>
</template>

<script setup lang="ts">
// Composition API で使用
const { t, locale } = useI18n()

const message = computed(() => t('welcome.message', { name: userName.value }))

const changeLanguage = (lang: 'ja' | 'en') => {
  locale.value = lang
}
</script>
```

#### 動的キー（注意が必要）

```typescript
// ❌ NG: 完全に動的なキーは避ける
const message = $t(variableKey)

// ✅ OK: 制限された選択肢から選ぶ
const statusKey = `status.${status}` as const
const message = $t(statusKey)

// より安全: switch文で明示的に
const getMessage = (status: string) => {
  switch (status) {
    case 'active':
      return $t('status.active')
    case 'inactive':
      return $t('status.inactive')
    default:
      return $t('status.unknown')
  }
}
```

### 6. TypeScript型定義

#### コンポーネントProps/Emits

```typescript
// types/components.ts
export interface SpotCardProps {
  spot: Spot
  showActions?: boolean
}

export interface SpotCardEmits {
  (e: 'click', spot: Spot): void
  (e: 'favorite', spotId: string): void
}
```

#### API レスポンス型

```typescript
// types/api.ts
export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  perPage: number
}

export interface SpotResponse {
  id: string
  name: string
  description: string
  latitude: number
  longitude: number
  createdAt: string
}
```

### 7. パフォーマンス最適化

#### 遅延ローディング

```typescript
// nuxt.config.ts で設定
export default defineNuxtConfig({
  components: {
    dirs: [
      {
        path: '~/components',
        pathPrefix: false,
      },
    ],
  },
})
```

```vue
<!-- コンポーネントは自動インポート -->
<template>
  <!-- 重いコンポーネントは遅延ロード -->
  <LazySpotMap v-if="showMap" :spots="spots" />
</template>
```

#### Computed vs Watch

```typescript
// ✅ OK: 派生値には computed を使う
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// ✅ OK: 副作用には watch を使う
watch(searchQuery, async (newQuery) => {
  if (newQuery.length >= 2) {
    await fetchResults(newQuery)
  }
})

// ❌ NG: watch で派生値を作らない
watch([firstName, lastName], ([first, last]) => {
  fullName.value = `${first} ${last}`  // computedを使うべき
})
```

#### 不要な再レンダリングの防止

```vue
<script setup lang="ts">
// ✅ OK: コンポーネント外で定数を定義
const STATIC_OPTIONS = ['Option 1', 'Option 2', 'Option 3']

// ❌ NG: setup内で毎回生成される
const options = ['Option 1', 'Option 2', 'Option 3']
</script>
```

### 8. Nuxt.js 固有機能

#### useFetch / useAsyncData

```vue
<script setup lang="ts">
// ✅ SSRで自動的にデータ取得
const { data: spots, pending, error, refresh } = await useFetch<Spot[]>(
  '/api/v1/spots',
  {
    key: 'spots-list',
    // リアクティブなパラメータ
    query: computed(() => ({ genre: selectedGenre.value })),
  }
)

// クライアントサイドのみ
onMounted(() => {
  refresh()
})
</script>
```

#### ミドルウェア

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()

  if (!authStore.isLoggedIn) {
    return navigateTo('/login')
  }
})
```

```vue
<!-- pages/mypage.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})
</script>
```

## プロジェクト固有の規約

### ディレクトリ構造

```
components/
├── beforeLogin/    # 認証前のコンポーネント
├── loggedIn/       # 認証後のコンポーネント
├── spot/           # スポット関連
├── ui/             # 再利用可能なUI
└── user/           # ユーザー関連

composables/        # Composition関数
stores/             # Piniaストア
pages/              # ファイルベースルーティング
types/              # TypeScript型定義
```

### 命名規則

- **コンポーネント**: PascalCase（`UserProfile.vue`）
- **Composables**: `use` + PascalCase（`useAuth.ts`）
- **Stores**: 機能名 + `Store`（`authStore`, `spotStore`）

## よく使うコマンド

```bash
# 開発サーバー起動
cd front && yarn dev

# 型チェック
yarn type-check

# Lint + Format
yarn check

# ビルド
yarn build
```

## ベストプラクティスまとめ

1. **Composition API** を使用（Options APIは使わない）
2. **型定義** を明示的に（`any` 禁止）
3. **i18n** でハードコードテキストを避ける
4. **Pinia** でグローバル状態を管理
5. **storeToRefs** でリアクティビティを保持
6. **computed** で派生値、**watch** で副作用
7. **useFetch** でSSR対応のデータ取得
8. **遅延ローディング** で初期ロードを最適化

## 参考リンク

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vuetify 3 Documentation](https://vuetifyjs.com/)
- [Vue I18n](https://vue-i18n.intlify.dev/)
