---
name: vue-expert
description: Deep Vue 3 expertise for Composition API, component patterns, Pinia state management, Vue Router, performance optimization, and testing. Use when building.
---

# Vue Expert

Specialized expertise in Vue 3 development, providing deep guidance on Composition API fundamentals, Single File Component architecture, composable design, Pinia state management, Vue Router patterns, performance optimization, testing with Vitest and Vue Test Utils, and advanced TypeScript integration.

## When to Use This Skill

Use this skill for:

- Building Vue 3 applications with the Composition API (ref, reactive, computed, watch)
- Designing Single File Components with typed props, emits, slots, and v-model
- Extracting reusable logic into composables (useAsync, useFetch, useForm)
- Managing application state with Pinia (stores, getters, actions, plugins)
- Configuring Vue Router with guards, lazy loading, nested routes, and meta fields
- Optimizing rendering performance (shallowRef, v-once, v-memo, KeepAlive, async components)
- Testing components and composables with Vitest and Vue Test Utils
- Integrating TypeScript with generic components, typed slots, and module augmentation

**Trigger phrases**: "vue component", "vue composable", "composition api", "ref reactive", "pinia store", "vue router", "vue performance", "vue testing", "vue typescript", "defineProps", "defineEmits", "provide inject", "v-model", "shallowRef", "keepalive", "vue test utils"

## What This Skill Does

Provides Vue 3 expertise including:

- **Composition API**: ref, reactive, computed, watch, watchEffect, lifecycle hooks
- **Component Patterns**: SFC structure, props/emits with TypeScript, slots, provide/inject, v-model
- **Composables**: Custom composable design, async patterns, shared state, dependency injection
- **State Management**: Pinia stores, getters, actions, plugins, SSR hydration, devtools
- **Routing**: Vue Router guards, lazy loading, nested routes, navigation, typed meta fields
- **Performance**: shallowRef, v-once, v-memo, KeepAlive, async components, virtual scrolling
- **Testing**: Vitest, Vue Test Utils, component mounting, composable testing, router/store mocking
- **TypeScript**: Typed props, typed emits, generic components, typed slots, global property augmentation

## Instructions

### Step 1: Master Composition API Fundamentals

**ref and reactive for state management**:

```vue
<script setup lang="ts">
import { ref, reactive, computed, watch, watchEffect, onMounted } from "vue";

// ref for primitives and single values (unwraps in template automatically)
const count = ref(0);
const searchQuery = ref("");

// reactive for objects (deep reactivity by default)
interface UserProfile {
  name: string;
  email: string;
  preferences: {
    theme: "light" | "dark";
    locale: string;
  };
}

const profile = reactive<UserProfile>({
  name: "",
  email: "",
  preferences: {
    theme: "light",
    locale: "en-US",
  },
});

// computed for derived state (cached, recalculates only when dependencies change)
const displayName = computed(() => {
  return profile.name.trim() || "Anonymous User";
});

const filteredResults = computed(() => {
  const query = searchQuery.value.toLowerCase();
  if (!query) return allResults.value;
  return allResults.value.filter((item) =>
    item.title.toLowerCase().includes(query)
  );
});

// Writable computed for two-way derived state
const fullName = computed({
  get: () => `${profile.name}`.trim(),
  set: (value: string) => {
    const [first, ...rest] = value.split(" ");
    profile.name = first ?? "";
  },
});
</script>
```

**watch and watchEffect for side effects**:

```vue
<script setup lang="ts">
import { ref, watch, watchEffect, onMounted, onUnmounted } from "vue";

const userId = ref<string | null>(null);
const userData = ref<User | null>(null);
const loading = ref(false);
const error = ref<Error | null>(null);

// watch: explicit source, access to old and new values, lazy by default
watch(userId, async (newId, oldId) => {
  if (!newId) {
    userData.value = null;
    return;
  }
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`/api/users/${newId}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    userData.value = await response.json();
  } catch (err) {
    error.value = err instanceof Error ? err : new Error(String(err));
  } finally {
    loading.value = false;
  }
});

// watch with options: immediate runs on setup, deep watches nested changes
watch(
  () => profile.preferences,
  (newPrefs) => {
    localStorage.setItem("user-prefs", JSON.stringify(newPrefs));
  },
  { deep: true, immediate: true }
);

// watch multiple sources simultaneously
watch(
  [() => filters.category, () => filters.sortBy, currentPage],
  ([category, sortBy, page]) => {
    fetchProducts({ category, sortBy, page });
  }
);

// watchEffect: auto-tracks dependencies, runs immediately
const stopWatcher = watchEffect((onCleanup) => {
  const controller = new AbortController();

  if (searchQuery.value.length >= 3) {
    fetchSuggestions(searchQuery.value, controller.signal);
  }

  // Cleanup function runs before each re-execution and on unmount
  onCleanup(() => controller.abort());
});

// Lifecycle hooks in Composition API
onMounted(() => {
  document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeyDown);
  stopWatcher();
});
</script>
```

### Step 2: Design Component Patterns

**Single File Component structure with typed props and emits**:

```vue
<script setup lang="ts">
import { computed, useSlots } from "vue";

// Typed props with defaults using withDefaults
interface DataTableProps {
  rows: Record<string, unknown>[];
  columns: {
    key: string;
    label: string;
    sortable?: boolean;
    width?: string;
  }[];
  loading?: boolean;
  striped?: boolean;
  stickyHeader?: boolean;
  emptyMessage?: string;
}

const props = withDefaults(defineProps<DataTableProps>(), {
  loading: false,
  striped: true,
  stickyHeader: false,
  emptyMessage: "No data available",
});

// Typed emits with payload validation
const emit = defineEmits<{
  sort: [column: string, direction: "asc" | "desc"];
  "row-click": [row: Record<string, unknown>, index: number];
  "selection-change": [selectedRows: Record<string, unknown>[]];
}>();

const slots = useSlots();
const hasFooter = computed(() => !!slots.footer);

function handleSort(columnKey: string) {
  const currentDirection = sortState.value.key === columnKey
    ? sortState.value.direction
    : "asc";
  const nextDirection = currentDirection === "asc" ? "desc" : "asc";
  emit("sort", columnKey, nextDirection);
}
</script>

<template>
  <div class="data-table" :class="{ 'data-table--striped': striped }">
    <div v-if="loading" class="data-table__loading">
      <slot name="loading">
        <span>Loading...</span>
      </slot>
    </div>
    <table v-else-if="rows.length > 0">
      <thead :class="{ 'sticky-header': stickyHeader }">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :style="{ width: col.width }"
            :class="{ sortable: col.sortable }"
            @click="col.sortable ? handleSort(col.key) : undefined"
          >
            <slot :name="`header-${col.key}`" :column="col">
              {{ col.label }}
            </slot>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, index) in rows"
          :key="index"
          @click="emit('row-click', row, index)"
        >
          <td v-for="col in columns" :key="col.key">
            <slot :name="`cell-${col.key}`" :value="row[col.key]" :row="row">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
      <tfoot v-if="hasFooter">
        <tr>
          <td :colspan="columns.length">
            <slot name="footer" />
          </td>
        </tr>
      </tfoot>
    </table>
    <div v-else class="data-table__empty">
      <slot name="empty">
        <p>{{ emptyMessage }}</p>
      </slot>
    </div>
  </div>
</template>
```

**v-model with multiple bindings**:

```vue
<!-- DateRangePicker.vue -->
<script setup lang="ts">
interface DateRange {
  start: string;
  end: string;
}

const startDate = defineModel<string>("start", { required: true });
const endDate = defineModel<string>("end", { required: true });
const isOpen = defineModel<boolean>("open", { default: false });

function selectPreset(preset: "today" | "week" | "month") {
  const now = new Date();
  const start = new Date();
  if (preset === "week") start.setDate(now.getDate() - 7);
  else if (preset === "month") start.setMonth(now.getMonth() - 1);
  startDate.value = start.toISOString().split("T")[0];
  endDate.value = now.toISOString().split("T")[0];
}
</script>

<template>
  <div class="date-range-picker">
    <input type="date" v-model="startDate" />
    <span>to</span>
    <input type="date" v-model="endDate" />
    <div class="presets">
      <button @click="selectPreset('today')">Today</button>
      <button @click="selectPreset('week')">Last 7 days</button>
      <button @click="selectPreset('month')">Last 30 days</button>
    </div>
  </div>
</template>

<!-- Parent usage with multiple v-model bindings -->
<!-- <DateRangePicker v-model:start="from" v-model:end="to" v-model:open="pickerOpen" /> -->
```

**provide/inject for dependency injection**:

```vue
<!-- NotificationProvider.vue -->
<script setup lang="ts">
import { provide, reactive, readonly } from "vue";
import type { InjectionKey } from "vue";

interface Notification {
  id: string;
  type: "success" | "error" | "warning" | "info";
  message: string;
  duration?: number;
}

interface NotificationContext {
  notifications: readonly Notification[];
  notify: (notification: Omit<Notification, "id">) => void;
  dismiss: (id: string) => void;
}

export const NotificationKey: InjectionKey<NotificationContext> =
  Symbol("notification");

const state = reactive<{ notifications: Notification[] }>({
  notifications: [],
});

function notify(notification: Omit<Notification, "id">) {
  const id = crypto.randomUUID();
  state.notifications.push({ ...notification, id });
  const duration = notification.duration ?? 5000;
  if (duration > 0) {
    setTimeout(() => dismiss(id), duration);
  }
}

function dismiss(id: string) {
  const index = state.notifications.findIndex((n) => n.id === id);
  if (index !== -1) state.notifications.splice(index, 1);
}

provide(NotificationKey, {
  notifications: readonly(state.notifications),
  notify,
  dismiss,
});
</script>

<template>
  <slot />
  <Teleport to="body">
    <TransitionGroup name="notification" tag="div" class="notification-stack">
      <div
        v-for="n in state.notifications"
        :key="n.id"
        :class="['notification', `notification--${n.type}`]"
        role="alert"
      >
        <span>{{ n.message }}</span>
        <button @click="dismiss(n.id)" aria-label="Dismiss notification">
          &times;
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>
```

```vue
<!-- Any descendant component -->
<script setup lang="ts">
import { inject } from "vue";
import { NotificationKey } from "./NotificationProvider.vue";

const { notify } = inject(NotificationKey)!;

function handleSave() {
  try {
    // save logic...
    notify({ type: "success", message: "Settings saved successfully." });
  } catch {
    notify({ type: "error", message: "Failed to save settings.", duration: 0 });
  }
}
</script>
```

### Step 3: Build Composables for Reusable Logic

**useAsync composable for async operations**:

```ts
// composables/useAsync.ts
import { ref, type Ref } from "vue";

interface UseAsyncReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  loading: Ref<boolean>;
  execute: (...args: unknown[]) => Promise<T | null>;
  reset: () => void;
}

export function useAsync<T>(
  asyncFn: (...args: unknown[]) => Promise<T>
): UseAsyncReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function execute(...args: unknown[]): Promise<T | null> {
    loading.value = true;
    error.value = null;
    try {
      const result = await asyncFn(...args);
      data.value = result;
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      return null;
    } finally {
      loading.value = false;
    }
  }

  function reset() {
    data.value = null;
    error.value = null;
    loading.value = false;
  }

  return { data, error, loading, execute, reset };
}
```

**useFetch composable with abort and caching**:

```ts
// composables/useFetch.ts
import { ref, watch, toValue, type MaybeRefOrGetter, type Ref } from "vue";

interface UseFetchOptions {
  immediate?: boolean;
  refetch?: boolean;
}

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  loading: Ref<boolean>;
  execute: () => Promise<void>;
  abort: () => void;
}

const cache = new Map<string, { data: unknown; timestamp: number }>();
const STALE_TIME = 5 * 60 * 1000;

export function useFetch<T>(
  url: MaybeRefOrGetter<string>,
  options: UseFetchOptions = {}
): UseFetchReturn<T> {
  const { immediate = true, refetch = true } = options;

  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const loading = ref(false);
  let controller: AbortController | null = null;

  async function execute(): Promise<void> {
    const resolvedUrl = toValue(url);

    // Check cache first
    const cached = cache.get(resolvedUrl);
    if (cached && Date.now() - cached.timestamp < STALE_TIME) {
      data.value = cached.data as T;
      return;
    }

    abort();
    controller = new AbortController();
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(resolvedUrl, {
        signal: controller.signal,
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const json: T = await response.json();
      data.value = json;
      cache.set(resolvedUrl, { data: json, timestamp: Date.now() });
    } catch (err) {
      if (err instanceof Error && err.name !== "AbortError") {
        error.value = err;
      }
    } finally {
      loading.value = false;
    }
  }

  function abort() {
    controller?.abort();
    controller = null;
  }

  if (refetch) {
    watch(() => toValue(url), execute);
  }

  if (immediate) {
    execute();
  }

  return { data, error, loading, execute, abort };
}
```

**useForm composable with validation**:

```ts
// composables/useForm.ts
import { reactive, computed, type UnwrapNestedRefs } from "vue";

type ValidationRule<T> = (value: T) => string | true;
type FieldRules<T> = { [K in keyof T]?: ValidationRule<T[K]>[] };

interface UseFormReturn<T extends Record<string, unknown>> {
  fields: UnwrapNestedRefs<T>;
  errors: Record<keyof T, string[]>;
  isValid: boolean;
  isDirty: boolean;
  validate: () => boolean;
  validateField: (field: keyof T) => void;
  reset: () => void;
  handleSubmit: (onSubmit: (values: T) => void | Promise<void>) => (e: Event) => void;
}

export function useForm<T extends Record<string, unknown>>(
  initialValues: T,
  rules: FieldRules<T> = {}
): UseFormReturn<T> {
  const fields = reactive({ ...initialValues }) as UnwrapNestedRefs<T>;
  const errors = reactive<Record<keyof T, string[]>>(
    Object.keys(initialValues).reduce(
      (acc, key) => ({ ...acc, [key]: [] }),
      {} as Record<keyof T, string[]>
    )
  );
  const touched = reactive<Record<keyof T, boolean>>(
    Object.keys(initialValues).reduce(
      (acc, key) => ({ ...acc, [key]: false }),
      {} as Record<keyof T, boolean>
    )
  );

  const isValid = computed(() =>
    Object.values(errors).every(
      (fieldErrors) => (fieldErrors as string[]).length === 0
    )
  );

  const isDirty = computed(() =>
    Object.keys(initialValues).some(
      (key) => fields[key as keyof T] !== initialValues[key as keyof T]
    )
  );

  function validateField(field: keyof T) {
    const fieldRules = rules[field] ?? [];
    const value = fields[field];
    const fieldErrors: string[] = [];
    for (const rule of fieldRules) {
      const result = rule(value as T[keyof T]);
      if (result !== true) fieldErrors.push(result);
    }
    errors[field] = fieldErrors as never;
  }

  function validate(): boolean {
    for (const field of Object.keys(rules) as (keyof T)[]) {
      validateField(field);
    }
    return isValid.value;
  }

  function reset() {
    Object.assign(fields, initialValues);
    for (const key of Object.keys(errors)) {
      errors[key as keyof T] = [] as never;
    }
  }

  function handleSubmit(onSubmit: (values: T) => void | Promise<void>) {
    return async (e: Event) => {
      e.preventDefault();
      if (validate()) {
        await onSubmit({ ...fields } as T);
      }
    };
  }

  return { fields, errors, isValid, isDirty, validate, validateField, reset, handleSubmit };
}
```

### Step 4: Manage State with Pinia

**Defining a Pinia store with TypeScript**:

```ts
// stores/useProductStore.ts
import { defineStore } from "pinia";
import { computed, ref } from "vue";

interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

interface ProductFilters {
  category: string | null;
  minPrice: number;
  maxPrice: number;
  inStockOnly: boolean;
}

// Setup store syntax (Composition API style, recommended)
export const useProductStore = defineStore("products", () => {
  // State
  const products = ref<Product[]>([]);
  const filters = ref<ProductFilters>({
    category: null,
    minPrice: 0,
    maxPrice: Infinity,
    inStockOnly: false,
  });
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters (computed)
  const filteredProducts = computed(() => {
    return products.value.filter((product) => {
      if (filters.value.category && product.category !== filters.value.category) {
        return false;
      }
      if (product.price < filters.value.minPrice) return false;
      if (product.price > filters.value.maxPrice) return false;
      if (filters.value.inStockOnly && !product.inStock) return false;
      return true;
    });
  });

  const categories = computed(() => {
    const cats = new Set(products.value.map((p) => p.category));
    return Array.from(cats).sort();
  });

  const totalValue = computed(() =>
    products.value.reduce((sum, p) => sum + p.price, 0)
  );

  // Actions
  async function fetchProducts(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await fetch("/api/products");
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      products.value = await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Failed to fetch products";
    } finally {
      loading.value = false;
    }
  }

  async function addProduct(product: Omit<Product, "id">): Promise<Product | null> {
    try {
      const response = await fetch("/api/products", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(product),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const created: Product = await response.json();
      products.value.push(created);
      return created;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Failed to add product";
      return null;
    }
  }

  function updateFilters(newFilters: Partial<ProductFilters>) {
    filters.value = { ...filters.value, ...newFilters };
  }

  function $reset() {
    products.value = [];
    filters.value = { category: null, minPrice: 0, maxPrice: Infinity, inStockOnly: false };
    loading.value = false;
    error.value = null;
  }

  return {
    // State
    products,
    filters,
    loading,
    error,
    // Getters
    filteredProducts,
    categories,
    totalValue,
    // Actions
    fetchProducts,
    addProduct,
    updateFilters,
    $reset,
  };
});
```

**Pinia plugin for persistence and logging**:

```ts
// plugins/piniaLogger.ts
import type { PiniaPluginContext } from "pinia";

export function piniaLogger({ store }: PiniaPluginContext) {
  store.$onAction(({ name, args, after, onError }) => {
    const startTime = performance.now();

    after((result) => {
      const duration = (performance.now() - startTime).toFixed(2);
      console.debug(
        `[Pinia] ${store.$id}.${name}() completed in ${duration}ms`,
        { args, result }
      );
    });

    onError((error) => {
      console.error(`[Pinia] ${store.$id}.${name}() failed`, { args, error });
    });
  });
}

// plugins/piniaPersist.ts
export function piniaPersist({ store }: PiniaPluginContext) {
  const key = `pinia-${store.$id}`;

  // Hydrate from localStorage on store creation
  const saved = localStorage.getItem(key);
  if (saved) {
    try {
      store.$patch(JSON.parse(saved));
    } catch {
      localStorage.removeItem(key);
    }
  }

  // Persist on every state change
  store.$subscribe((_mutation, state) => {
    localStorage.setItem(key, JSON.stringify(state));
  });
}

// main.ts — register plugins
import { createPinia } from "pinia";
import { piniaLogger } from "./plugins/piniaLogger";
import { piniaPersist } from "./plugins/piniaPersist";

const pinia = createPinia();
pinia.use(piniaLogger);
pinia.use(piniaPersist);
```

**Store composition (stores using other stores)**:

```ts
// stores/useCartStore.ts
import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { useProductStore } from "./useProductStore";
import { useAuthStore } from "./useAuthStore";

interface CartItem {
  productId: string;
  quantity: number;
}

export const useCartStore = defineStore("cart", () => {
  const productStore = useProductStore();
  const authStore = useAuthStore();

  const items = ref<CartItem[]>([]);

  const enrichedItems = computed(() =>
    items.value
      .map((item) => {
        const product = productStore.products.find((p) => p.id === item.productId);
        if (!product) return null;
        return {
          ...item,
          name: product.name,
          price: product.price,
          subtotal: product.price * item.quantity,
        };
      })
      .filter(Boolean)
  );

  const total = computed(() =>
    enrichedItems.value.reduce((sum, item) => sum + (item?.subtotal ?? 0), 0)
  );

  function addToCart(productId: string, quantity = 1) {
    if (!authStore.isAuthenticated) {
      throw new Error("Must be logged in to add items to cart");
    }
    const existing = items.value.find((i) => i.productId === productId);
    if (existing) {
      existing.quantity += quantity;
    } else {
      items.value.push({ productId, quantity });
    }
  }

  function removeFromCart(productId: string) {
    items.value = items.value.filter((i) => i.productId !== productId);
  }

  return { items, enrichedItems, total, addToCart, removeFromCart };
});
```

### Step 5: Configure Vue Router Patterns

**Route configuration with lazy loading and typed meta**:

```ts
// router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

// Extend RouteMeta for type-safe meta fields
declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean;
    roles?: string[];
    title?: string;
    transition?: "slide-left" | "slide-right" | "fade";
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("../layouts/DefaultLayout.vue"),
    children: [
      {
        path: "",
        name: "home",
        component: () => import("../pages/HomePage.vue"),
        meta: { title: "Home" },
      },
      {
        path: "products",
        name: "products",
        component: () => import("../pages/ProductsPage.vue"),
        meta: { title: "Products" },
      },
      {
        path: "products/:id",
        name: "product-detail",
        component: () => import("../pages/ProductDetailPage.vue"),
        props: true,
        meta: { title: "Product Detail" },
      },
    ],
  },
  {
    path: "/dashboard",
    component: () => import("../layouts/DashboardLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      {
        path: "",
        name: "dashboard",
        component: () => import("../pages/DashboardPage.vue"),
        meta: { title: "Dashboard", roles: ["user", "admin"] },
      },
      {
        path: "settings",
        name: "settings",
        component: () => import("../pages/SettingsPage.vue"),
        meta: { title: "Settings", roles: ["user", "admin"] },
      },
      {
        path: "admin",
        name: "admin",
        component: () => import("../pages/AdminPage.vue"),
        meta: { title: "Admin Panel", roles: ["admin"] },
      },
    ],
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../pages/LoginPage.vue"),
    meta: { title: "Sign In" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../pages/NotFoundPage.vue"),
    meta: { title: "Page Not Found" },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition;
    if (to.hash) return { el: to.hash, behavior: "smooth" };
    return { top: 0 };
  },
});

export default router;
```

**Navigation guards for auth and role checking**:

```ts
// router/guards.ts
import type { Router } from "vue-router";
import { useAuthStore } from "../stores/useAuthStore";

export function registerGuards(router: Router) {
  // Global before guard: authentication and authorization
  router.beforeEach(async (to, _from) => {
    const authStore = useAuthStore();

    // Update document title
    document.title = to.meta.title
      ? `${to.meta.title} | MyApp`
      : "MyApp";

    // Check if route requires authentication
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      return {
        name: "login",
        query: { redirect: to.fullPath },
      };
    }

    // Check role-based access
    if (to.meta.roles && to.meta.roles.length > 0) {
      const hasRole = to.meta.roles.some((role) =>
        authStore.user?.roles.includes(role)
      );
      if (!hasRole) {
        return { name: "dashboard" };
      }
    }

    return true;
  });

  // Global after hook: analytics tracking
  router.afterEach((to, from) => {
    if (to.path !== from.path) {
      trackPageView(to.fullPath, to.meta.title);
    }
  });

  // Per-route error handling
  router.onError((error, to) => {
    // Handle lazy-loaded chunk failures (common after deployments)
    if (
      error.message.includes("Failed to fetch dynamically imported module") ||
      error.message.includes("Loading chunk")
    ) {
      window.location.href = to.fullPath;
    }
  });
}

function trackPageView(path: string, title?: string) {
  // Analytics integration point
  console.debug("[Analytics]", { path, title });
}
```

**Programmatic navigation and route composable**:

```vue
<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { computed, watch } from "vue";

const router = useRouter();
const route = useRoute();

// Reactive route params
const productId = computed(() => route.params.id as string);
const searchQuery = computed(() => (route.query.q as string) ?? "");
const currentPage = computed(() => Number(route.query.page) || 1);

// Update query params without full navigation
function updateSearch(query: string) {
  router.replace({
    query: {
      ...route.query,
      q: query || undefined,
      page: undefined, // Reset page when search changes
    },
  });
}

function goToPage(page: number) {
  router.push({
    query: { ...route.query, page: page > 1 ? String(page) : undefined },
  });
}

// Navigate after an action
async function handleDelete(id: string) {
  await deleteProduct(id);
  await router.push({ name: "products" });
}

// Watch route changes for data fetching
watch(
  () => route.params.id,
  (newId) => {
    if (newId) fetchProductDetail(newId as string);
  },
  { immediate: true }
);
</script>
```

### Step 6: Optimize Performance

**shallowRef and shallowReactive for large datasets**:

```vue
<script setup lang="ts">
import {
  shallowRef,
  triggerRef,
  computed,
  defineAsyncComponent,
} from "vue";

interface LogEntry {
  id: string;
  timestamp: number;
  level: "info" | "warn" | "error";
  message: string;
  metadata: Record<string, unknown>;
}

// shallowRef: only triggers updates when .value is reassigned,
// not when nested properties change. Ideal for large arrays and objects.
const logEntries = shallowRef<LogEntry[]>([]);

function appendLog(entry: LogEntry) {
  // Must reassign .value to trigger reactivity (push alone will not work)
  logEntries.value = [...logEntries.value, entry];
}

function bulkAppend(entries: LogEntry[]) {
  // Batch update: single reactivity trigger for multiple additions
  logEntries.value = [...logEntries.value, ...entries];
}

// For cases where you must mutate in place, use triggerRef
function clearOldEntries(maxAge: number) {
  const cutoff = Date.now() - maxAge;
  logEntries.value = logEntries.value.filter((e) => e.timestamp > cutoff);
  // If mutating in place instead of reassigning:
  // logEntries.value.splice(0, removeCount);
  // triggerRef(logEntries);
}

const errorCount = computed(
  () => logEntries.value.filter((e) => e.level === "error").length
);
</script>
```

**v-once, v-memo, and KeepAlive**:

```vue
<template>
  <!-- v-once: renders once, never re-renders (static content) -->
  <header v-once>
    <h1>{{ appTitle }}</h1>
    <nav>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>

  <!-- v-memo: skip re-render unless specified dependencies change -->
  <!-- Useful in v-for loops with expensive row rendering -->
  <div class="user-list">
    <div
      v-for="user in users"
      :key="user.id"
      v-memo="[user.name, user.avatar, user.id === selectedId]"
      class="user-card"
      :class="{ selected: user.id === selectedId }"
      @click="selectedId = user.id"
    >
      <img :src="user.avatar" :alt="user.name" />
      <span>{{ user.name }}</span>
      <ExpensiveStatusBadge :status="user.status" />
    </div>
  </div>

  <!-- KeepAlive: caches component instances instead of destroying them -->
  <KeepAlive :include="['ProductList', 'SearchResults']" :max="5">
    <component :is="currentTab" />
  </KeepAlive>
</template>

<script setup lang="ts">
import { ref, onActivated, onDeactivated } from "vue";

// KeepAlive lifecycle hooks
onActivated(() => {
  // Called when component is re-inserted from cache
  // Refresh data that may have gone stale
  refreshData();
});

onDeactivated(() => {
  // Called when component is cached (removed from DOM but kept alive)
  // Pause expensive operations like polling
  stopPolling();
});
</script>
```

**Async components and Suspense**:

```vue
<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";

// Async component with loading and error states
const HeavyChart = defineAsyncComponent({
  loader: () => import("./HeavyChart.vue"),
  loadingComponent: () => import("./ChartSkeleton.vue"),
  errorComponent: () => import("./ChartError.vue"),
  delay: 200,        // Show loading after 200ms (avoids flash for fast loads)
  timeout: 10000,    // Fail after 10 seconds
});

// Simple async component for code splitting
const AdminPanel = defineAsyncComponent(
  () => import("./AdminPanel.vue")
);

const showChart = ref(false);
</script>

<template>
  <button @click="showChart = true">Load Chart</button>

  <!-- Suspense for coordinating multiple async dependencies -->
  <Suspense v-if="showChart">
    <template #default>
      <HeavyChart :data="chartData" />
    </template>
    <template #fallback>
      <div class="skeleton">Loading chart data...</div>
    </template>
  </Suspense>
</template>
```

**Virtual scrolling for large lists**:

```vue
<script setup lang="ts">
import { ref, computed } from "vue";

interface VirtualListProps {
  items: unknown[];
  itemHeight: number;
  containerHeight: number;
  overscan?: number;
}

const props = withDefaults(defineProps<VirtualListProps>(), {
  overscan: 5,
});

const scrollTop = ref(0);

const totalHeight = computed(() => props.items.length * props.itemHeight);

const visibleRange = computed(() => {
  const start = Math.floor(scrollTop.value / props.itemHeight);
  const visibleCount = Math.ceil(props.containerHeight / props.itemHeight);
  return {
    start: Math.max(0, start - props.overscan),
    end: Math.min(props.items.length, start + visibleCount + props.overscan),
  };
});

const visibleItems = computed(() =>
  props.items.slice(visibleRange.value.start, visibleRange.value.end).map(
    (item, index) => ({
      item,
      index: visibleRange.value.start + index,
      style: {
        position: "absolute" as const,
        top: `${(visibleRange.value.start + index) * props.itemHeight}px`,
        height: `${props.itemHeight}px`,
        width: "100%",
      },
    })
  )
);

function onScroll(event: UIEvent) {
  scrollTop.value = (event.target as HTMLElement).scrollTop;
}
</script>

<template>
  <div
    class="virtual-list"
    :style="{ height: `${containerHeight}px`, overflow: 'auto', position: 'relative' }"
    @scroll="onScroll"
  >
    <div :style="{ height: `${totalHeight}px`, position: 'relative' }">
      <div
        v-for="{ item, index, style } in visibleItems"
        :key="index"
        :style="style"
      >
        <slot :item="item" :index="index" />
      </div>
    </div>
  </div>
</template>
```

### Step 7: Test with Vitest and Vue Test Utils

**Component testing fundamentals**:

```ts
// components/__tests__/LoginForm.test.ts
import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import LoginForm from "../LoginForm.vue";

describe("LoginForm", () => {
  it("submits credentials when form is valid", async () => {
    const wrapper = mount(LoginForm);

    await wrapper.find('input[name="email"]').setValue("user@example.com");
    await wrapper.find('input[name="password"]').setValue("s3cret!");
    await wrapper.find("form").trigger("submit");

    expect(wrapper.emitted("submit")).toBeTruthy();
    expect(wrapper.emitted("submit")![0]).toEqual([
      { email: "user@example.com", password: "s3cret!" },
    ]);
  });

  it("shows validation errors for empty fields", async () => {
    const wrapper = mount(LoginForm);

    await wrapper.find("form").trigger("submit");

    expect(wrapper.text()).toContain("Email is required");
    expect(wrapper.text()).toContain("Password is required");
    expect(wrapper.emitted("submit")).toBeFalsy();
  });

  it("disables submit button while loading", async () => {
    const wrapper = mount(LoginForm, {
      props: { loading: true },
    });

    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes("disabled")).toBeDefined();
    expect(button.text()).toBe("Signing in...");
  });

  it("renders slot content in the footer", () => {
    const wrapper = mount(LoginForm, {
      slots: {
        footer: '<a href="/forgot">Forgot password?</a>',
      },
    });

    expect(wrapper.find("a").text()).toBe("Forgot password?");
    expect(wrapper.find("a").attributes("href")).toBe("/forgot");
  });
});
```

**Testing composables**:

```ts
// composables/__tests__/useFetch.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { ref, nextTick } from "vue";
import { useFetch } from "../useFetch";

describe("useFetch", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("fetches data on mount when immediate is true", async () => {
    const mockData = { id: 1, name: "Product" };
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    } as Response);

    const { data, loading, error } = useFetch<typeof mockData>("/api/products/1");

    expect(loading.value).toBe(true);
    await vi.waitFor(() => expect(loading.value).toBe(false));

    expect(data.value).toEqual(mockData);
    expect(error.value).toBeNull();
  });

  it("sets error on network failure", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("Network error"));

    const { data, error, loading } = useFetch("/api/products/1");

    await vi.waitFor(() => expect(loading.value).toBe(false));

    expect(data.value).toBeNull();
    expect(error.value?.message).toBe("Network error");
  });

  it("refetches when URL changes", async () => {
    const url = ref("/api/products/1");
    vi.mocked(fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ id: 1 }),
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ id: 2 }),
      } as Response);

    const { data } = useFetch<{ id: number }>(url);
    await vi.waitFor(() => expect(data.value?.id).toBe(1));

    url.value = "/api/products/2";
    await vi.waitFor(() => expect(data.value?.id).toBe(2));

    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it("does not fetch when immediate is false", () => {
    const { loading } = useFetch("/api/products", { immediate: false });

    expect(fetch).not.toHaveBeenCalled();
    expect(loading.value).toBe(false);
  });
});
```

**Testing with router and Pinia stores**:

```ts
// pages/__tests__/ProductDetailPage.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { createRouter, createMemoryHistory } from "vue-router";
import ProductDetailPage from "../ProductDetailPage.vue";
import { useProductStore } from "../../stores/useProductStore";

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: "/products/:id", name: "product-detail", component: ProductDetailPage },
      { path: "/products", name: "products", component: { template: "<div />" } },
    ],
  });
}

describe("ProductDetailPage", () => {
  let router: ReturnType<typeof createTestRouter>;

  beforeEach(async () => {
    router = createTestRouter();
    await router.push("/products/abc-123");
    await router.isReady();
  });

  it("displays product details from the store", () => {
    const wrapper = mount(ProductDetailPage, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            initialState: {
              products: {
                products: [
                  { id: "abc-123", name: "Widget", price: 29.99, category: "tools", inStock: true },
                ],
              },
            },
          }),
        ],
      },
    });

    expect(wrapper.text()).toContain("Widget");
    expect(wrapper.text()).toContain("29.99");
  });

  it("calls fetchProducts on mount if store is empty", () => {
    const wrapper = mount(ProductDetailPage, {
      global: {
        plugins: [router, createTestingPinia({ stubActions: false })],
      },
    });

    const store = useProductStore();
    expect(store.fetchProducts).toHaveBeenCalled();
  });

  it("navigates back to product list on delete", async () => {
    const wrapper = mount(ProductDetailPage, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            initialState: {
              products: {
                products: [
                  { id: "abc-123", name: "Widget", price: 29.99, category: "tools", inStock: true },
                ],
              },
            },
          }),
        ],
      },
    });

    await wrapper.find('[data-testid="delete-button"]').trigger("click");
    await wrapper.find('[data-testid="confirm-delete"]').trigger("click");

    expect(router.currentRoute.value.name).toBe("products");
  });
});
```

### Step 8: Integrate TypeScript Deeply

**Typed props with complex types and runtime validation**:

```vue
<script setup lang="ts">
import type { PropType } from "vue";

// Approach 1: defineProps with type-only syntax (preferred)
interface ChartDataset {
  label: string;
  data: number[];
  color: string;
  type: "line" | "bar" | "area";
}

interface ChartConfig {
  title: string;
  datasets: ChartDataset[];
  xLabels: string[];
  yAxis?: {
    min?: number;
    max?: number;
    format?: (value: number) => string;
  };
}

const props = defineProps<{
  config: ChartConfig;
  width?: number;
  height?: number;
  animate?: boolean;
}>();

// Approach 2: defineProps with runtime validation (when defaults are complex)
// Use this when you need validator functions or complex defaults
const propsAlt = defineProps({
  config: {
    type: Object as PropType<ChartConfig>,
    required: true,
    validator: (value: ChartConfig) => {
      return value.datasets.length > 0 && value.xLabels.length > 0;
    },
  },
  width: { type: Number, default: 600 },
  height: { type: Number, default: 400 },
});
</script>
```

**Typed emits with complex payloads**:

```vue
<script setup lang="ts">
interface FormValues {
  name: string;
  email: string;
  role: "admin" | "editor" | "viewer";
}

interface ValidationError {
  field: keyof FormValues;
  message: string;
}

// Typed emits ensure compile-time safety for event payloads
const emit = defineEmits<{
  submit: [values: FormValues];
  cancel: [];
  "validation-error": [errors: ValidationError[]];
  "field-change": [field: keyof FormValues, value: string];
}>();

function handleSubmit() {
  const errors = validate();
  if (errors.length > 0) {
    emit("validation-error", errors);
    return;
  }
  emit("submit", { name: name.value, email: email.value, role: role.value });
}

// TypeScript enforces correct payload types:
// emit("submit", { name: 123 })  // Type error: number is not assignable to string
// emit("cancel", "arg")          // Type error: expected 0 arguments
</script>
```

**Generic components**:

```vue
<!-- GenericSelect.vue -->
<script setup lang="ts" generic="T extends { id: string; label: string }">
import { computed } from "vue";

const props = defineProps<{
  options: T[];
  modelValue: T | null;
  placeholder?: string;
  disabled?: boolean;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: T | null];
}>();

const selectedId = computed(() => props.modelValue?.id ?? "");

function handleChange(event: Event) {
  const target = event.target as HTMLSelectElement;
  const selected = props.options.find((opt) => opt.id === target.value) ?? null;
  emit("update:modelValue", selected);
}
</script>

<template>
  <select
    :value="selectedId"
    :disabled="disabled"
    @change="handleChange"
  >
    <option value="" disabled>
      {{ placeholder ?? "Select an option" }}
    </option>
    <option
      v-for="option in options"
      :key="option.id"
      :value="option.id"
    >
      {{ option.label }}
    </option>
  </select>
</template>

<!-- Usage: TypeScript infers T from the options prop -->
<!--
<GenericSelect
  :options="countries"
  v-model="selectedCountry"
  placeholder="Choose a country"
/>
-->
```

**Typed slots**:

```vue
<!-- TypedDataList.vue -->
<script setup lang="ts" generic="T">
defineProps<{
  items: T[];
  loading?: boolean;
}>();

// Typed slots ensure consumers provide correct slot prop types
defineSlots<{
  default: (props: { item: T; index: number }) => unknown;
  empty: () => unknown;
  loading: () => unknown;
  header: (props: { count: number }) => unknown;
}>();
</script>

<template>
  <div class="data-list">
    <div class="data-list__header">
      <slot name="header" :count="items.length" />
    </div>
    <div v-if="loading" class="data-list__loading">
      <slot name="loading">
        <span>Loading...</span>
      </slot>
    </div>
    <div v-else-if="items.length === 0" class="data-list__empty">
      <slot name="empty">
        <p>No items found.</p>
      </slot>
    </div>
    <div v-else class="data-list__items">
      <div v-for="(item, index) in items" :key="index">
        <slot :item="item" :index="index" />
      </div>
    </div>
  </div>
</template>

<!-- Usage: slot props are fully typed based on T -->
<!--
<TypedDataList :items="users">
  <template #default="{ item, index }">
    <UserCard :user="item" :rank="index + 1" />
  </template>
  <template #header="{ count }">
    <h2>{{ count }} users found</h2>
  </template>
  <template #empty>
    <EmptyState message="No users match your search." />
  </template>
</TypedDataList>
-->
```

**Augmenting global properties and component types**:

```ts
// types/vue-shims.d.ts
import type { AxiosInstance } from "axios";
import type { Router } from "vue-router";

// Augment Vue's ComponentCustomProperties to type this.$http, this.$router, etc.
declare module "vue" {
  interface ComponentCustomProperties {
    $http: AxiosInstance;
    $formatDate: (date: Date | string, locale?: string) => string;
    $formatCurrency: (amount: number, currency?: string) => string;
  }
}

// Augment route meta for type-safe router.beforeEach
declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean;
    roles?: ("admin" | "editor" | "viewer")[];
    title?: string;
    breadcrumb?: string;
  }
}

// Register global components for template type checking (Volar)
declare module "vue" {
  export interface GlobalComponents {
    BaseButton: typeof import("../components/BaseButton.vue")["default"];
    BaseInput: typeof import("../components/BaseInput.vue")["default"];
    BaseModal: typeof import("../components/BaseModal.vue")["default"];
    RouterLink: typeof import("vue-router")["RouterLink"];
    RouterView: typeof import("vue-router")["RouterView"];
  }
}

export {};
```

```ts
// plugins/globals.ts — registering the augmented properties
import type { App } from "vue";
import axios from "axios";

export function registerGlobals(app: App) {
  const http = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 10_000,
  });

  app.config.globalProperties.$http = http;

  app.config.globalProperties.$formatDate = (
    date: Date | string,
    locale = "en-US"
  ) => {
    return new Intl.DateTimeFormat(locale, {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(new Date(date));
  };

  app.config.globalProperties.$formatCurrency = (
    amount: number,
    currency = "USD"
  ) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency,
    }).format(amount);
  };
}
```

## Best Practices

- **Use Composition API for all new components** (Options API is supported but Composition API is the standard for Vue 3)
- **Extract composables when logic is reused** across two or more components
- **Prefer ref over reactive** for top-level state (ref works with primitives and is easier to destructure)
- **Always type defineProps and defineEmits** using the type-only syntax for compile-time safety
- **Use shallowRef for large collections** that are replaced rather than mutated in place
- **Keep components under 200 lines** of script; extract composables or child components when complexity grows
- **Colocate tests with source files** (ComponentName.vue and ComponentName.test.ts in the same directory)
- **Use provide/inject with InjectionKey** for type-safe dependency injection across component trees

## Common Patterns

### Pattern 1: Debounced Search with Composable

```vue
<script setup lang="ts">
import { ref, watch } from "vue";

function useDebouncedRef<T>(initialValue: T, delayMs: number) {
  const value = ref(initialValue) as Ref<T>;
  const debouncedValue = ref(initialValue) as Ref<T>;
  let timeout: ReturnType<typeof setTimeout>;

  watch(value, (newVal) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      debouncedValue.value = newVal;
    }, delayMs);
  });

  return { value, debouncedValue };
}

const { value: searchInput, debouncedValue: debouncedQuery } =
  useDebouncedRef("", 300);

watch(debouncedQuery, async (query) => {
  if (query.length >= 2) {
    results.value = await searchProducts(query);
  }
});
</script>

<template>
  <input v-model="searchInput" placeholder="Search products..." />
  <ProductList :products="results" />
</template>
```

### Pattern 2: Teleport Modal with Focus Trap

```vue
<script setup lang="ts">
import { ref, watch, nextTick, onUnmounted } from "vue";

const props = defineProps<{
  open: boolean;
  title: string;
}>();

const emit = defineEmits<{
  close: [];
}>();

const dialogRef = ref<HTMLDialogElement | null>(null);

watch(
  () => props.open,
  async (isOpen) => {
    await nextTick();
    if (isOpen) {
      dialogRef.value?.showModal();
    } else {
      dialogRef.value?.close();
    }
  }
);

function handleKeydown(event: KeyboardEvent) {
  if (event.key === "Escape") emit("close");
}
</script>

<template>
  <Teleport to="body">
    <dialog
      ref="dialogRef"
      :aria-label="title"
      @keydown="handleKeydown"
      @close="emit('close')"
    >
      <header>
        <h2>{{ title }}</h2>
        <button @click="emit('close')" aria-label="Close dialog">
          &times;
        </button>
      </header>
      <div class="dialog-body">
        <slot />
      </div>
      <footer>
        <slot name="actions" />
      </footer>
    </dialog>
  </Teleport>
</template>
```

## Quality Checklist

- [ ] All components use `<script setup lang="ts">` with typed props and emits
- [ ] Composables follow the `use` prefix convention and return reactive state
- [ ] Pinia stores use the Setup Store syntax with typed state, getters, and actions
- [ ] Route guards check authentication and authorization with typed meta fields
- [ ] Large lists use shallowRef, v-memo, or virtual scrolling for performance
- [ ] Components are tested with Vue Test Utils and Vitest
- [ ] Composables are tested in isolation without mounting components
- [ ] Global types are augmented for router meta, global properties, and components
- [ ] Side effects use watch/watchEffect with proper cleanup via onCleanup
- [ ] v-model bindings use defineModel for clean two-way data flow
- [ ] Provide/inject uses typed InjectionKey for compile-time safety
- [ ] Async components use defineAsyncComponent with loading and error fallbacks

## Related Skills

- `nextjs-expert` - SSR framework patterns applicable to Nuxt (Vue's SSR framework)
- `javascript-cleanup` - JavaScript code quality and cleanup
- `typescript-expert` - Advanced TypeScript patterns and strict configuration
- `unit-tests` - General unit testing strategies
- `performance-review` - Broad performance review methodology
- `test-cases` - Test case design patterns

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
