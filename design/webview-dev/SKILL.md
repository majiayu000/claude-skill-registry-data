---
name: webview-dev
description: Vue3 Webview 前端开发模块。当需要创建 Vue 组件、修改 UI、添加样式、使用 Vite 构建、与 Extension 通信时使用。涵盖组件开发、状态管理、样式系统、API 封装等。
---

# Webview Vue3 前端开发

负责 Webview 前端 UI 的开发，使用 Vue 3 + Vite + TypeScript。

## 目录结构

```
webview/
├─ index.html            # HTML 入口
├─ package.json          # 前端依赖
├─ vite.config.ts        # Vite 配置
├─ tsconfig.json         # TS 配置
└─ src/
    ├─ main.ts           # Vue 入口
    ├─ App.vue           # 根组件
    ├─ api/
    │   └─ vscode.ts     # VS Code 通信 API
    ├─ components/       # 组件目录 (待创建)
    └─ styles/
        └─ main.css      # 全局样式
```

## Instructions

### 1. 创建新组件

在 `webview/src/components/` 下创建：
```vue
<!-- MyComponent.vue -->
<template>
  <div class="my-component">
    <h2>{{ title }}</h2>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue';

const props = defineProps<{
  title: string;
}>();
</script>

<style scoped>
.my-component {
  padding: 16px;
  background: var(--vscode-editor-background);
  border: 1px solid var(--vscode-widget-border);
  border-radius: 8px;
}
</style>
```

### 2. 与 Extension 通信

**发送消息到 Extension：**
```typescript
import { vscode } from '@/api/vscode';

// 发送消息
vscode.postMessage({
  type: 'actionType',
  payload: { data: 'value' }
});
```

**接收 Extension 消息：**
```typescript
import { onMounted, onUnmounted } from 'vue';

onMounted(() => {
  const handler = (event: MessageEvent) => {
    const message = event.data;
    if (message.type === 'responseType') {
      // 处理响应
    }
  };
  window.addEventListener('message', handler);
  
  onUnmounted(() => {
    window.removeEventListener('message', handler);
  });
});
```

### 3. 使用 VS Code 主题变量

```css
/* 常用 VS Code CSS 变量 */
.element {
  color: var(--vscode-foreground);
  background: var(--vscode-editor-background);
  border-color: var(--vscode-widget-border);
}

/* 按钮 */
button {
  background: var(--vscode-button-background);
  color: var(--vscode-button-foreground);
}
button:hover {
  background: var(--vscode-button-hoverBackground);
}

/* 输入框 */
input {
  background: var(--vscode-input-background);
  color: var(--vscode-input-foreground);
  border: 1px solid var(--vscode-input-border);
}

/* 链接 */
a {
  color: var(--vscode-textLink-foreground);
}
```

### 4. 开发模式

```bash
# 启动 Vite 开发服务器 (独立调试 UI)
cd webview && npm run dev

# 构建生产版本
npm run build:web
```

### 5. 添加状态管理 (Pinia)

**安装：**
```bash
cd webview && npm install pinia
```

**配置：**
```typescript
// src/main.ts
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

const app = createApp(App);
app.use(createPinia());
app.mount('#app');
```

**创建 Store：**
```typescript
// src/stores/counter.ts
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  actions: {
    increment() {
      this.count++;
    }
  }
});
```

## Vite 配置说明

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: '../dist/webview',    // 输出到 dist/webview
    emptyOutDir: true,
    rollupOptions: {
      output: {
        // 固定文件名，便于 Extension 引用
        entryFileNames: 'assets/index.js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name].[ext]'
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@shared': path.resolve(__dirname, '../shared')
    }
  }
});
```

## Best Practices

- 使用 `<script setup>` 语法简化组件
- 样式使用 `scoped` 避免污染
- 优先使用 VS Code CSS 变量保持主题一致
- 通信消息类型在 `shared/types/` 定义
- 组件按功能拆分，保持单一职责

## 常见问题

**Q: 样式在 VS Code 中显示异常？**
A: 确保使用 VS Code CSS 变量，不要硬编码颜色

**Q: 热更新不生效？**
A: Vite dev 模式仅用于独立 UI 调试，Extension 中需重新 build
