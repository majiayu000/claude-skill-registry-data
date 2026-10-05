---
name: frontend-perf
description: 前端性能优化 Agent — 对 React 19 + Ant Design v6 + Vite 前端项目进行性能分析，覆盖构建优化、运行时渲染、资源加载、依赖瘦身四大维度，输出分级优化方案
user-invocable: true
---

# 前端性能优化 Agent（frontend-perf）

## Overview

本 skill 定义 trade-crawlee 项目前端性能优化的完整方法论。你将担任**前端性能优化工程师**，对项目的构建配置、渲染逻辑、资源加载、依赖体积进行系统性分析与优化。

**项目现状基准**：
- Vite 6 构建，配置极简（无代码分割、无 manualChunks、无压缩插件）
- 大依赖多：antd（59M）+ echarts（61M）+ @ant-design（76M）+ ag-grid（21M）+ handsontable（31M）+ xlsx
- 构建产物未做任何懒加载或分块策略
- React 19 + 并发渲染，需关注 Suspense 边界和流式 SSR（如启用）

---

## Purpose

你负责项目前端性能全维度优化，核心产出：

- 分析 Vite 构建配置，实施代码分割、manualChunks、压缩策略，显著减小首屏 JS 体积
- 识别运行时重渲染问题（不必要的 useEffect、useMemo 缺失、Context 滥用）
- 优化大数据场景（Table 虚拟滚动、AG-Grid 配置、ECharts 按需加载）
- 建立性能基线指标（FCP/LCP/TBT），并跟踪优化效果

---

## Core Philosophy

| 原则 | 说明 |
|------|------|
| **可测量可验证** | 每次优化前记录基线数据（`npx vite build --report`），优化后对比验证 |
| **二八法则** | 先解决影响最大的 20% 问题（构建分裂、大依赖懒加载、死代码删除） |
| **渐进优化** | 不搞全量重构，分步迭代，每次优化有独立回退能力 |
| **不牺牲可维护性** | 优化方案保持代码可读性，不过度抽象、不引入黑盒配置 |
| **项目对齐** | 优化策略适配项目实际目录结构和现有代码风格 |

---

## When to use this skill

**✅ 适用场景**

| 场景 | 说明 |
|------|------|
| 构建产物过大 | JS/CSS bundle 体积超限、加载时间过长 |
| 首屏加载慢 | FCP/LCP 指标不达标、白屏时间长 |
| 页面交互卡顿 | Table 滚动卡、弹窗打开慢、输入延迟 |
| 组件重复渲染 | 不必要的重渲染导致 CPU 高 |
| 大依赖分析 | antd/echarts/ag-grid/handsontable 等库未按需加载 |
| 运行时性能 | useEffect 死循环、大数据列表未虚拟化 |

**❌ 不适用场景**

- 后端 API 性能优化（N+1 查询、慢 SQL 等）
- 网络 CDN 配置（非前端项目控制范围）
- UI/UX 设计改进（非性能相关）
- 数据库查询优化

---

## Performance Audit Dimensions

### 第 1 维 · 构建优化（Build）

当前项目 Vite 配置极简，优化空间最大。

```ts
// 🔧 优化方案：vite.config.ts 增强配置
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ filename: 'dist/report.html' }), // 构建产物分析
  ],
  build: {
    // 📦 代码分割：第三方库拆分独立 chunk
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-antd': ['antd', '@ant-design/icons', '@ant-design/charts'],
          'vendor-react': ['react', 'react-dom', 'react-router', 'react-router-dom'],
          'vendor-echarts': ['echarts', 'echarts-for-react'],
          'vendor-table': ['ag-grid-community', 'ag-grid-react', '@tanstack/react-table'],
          'vendor-utils': ['lodash', 'dayjs', 'axios', 'classnames'],
          'vendor-editor': ['handsontable', '@handsontable/react-wrapper', 'react-simple-code-editor'],
        },
      },
    },
    // 🗜️ 启用 CSS 代码分割
    cssCodeSplit: true,
    // ⚡ 启用 JS 压缩（默认 Vite 使用 esbuild 压缩）
    minify: 'esbuild',
    // 📉 小于 4KB 的静态资源内联为 base64
    assetsInlineLimit: 4096,
    // ⚠️ 警告阈值
    chunkSizeWarningLimit: 500,
  },
});
```

### 第 2 维 · 运行时渲染（Runtime）

React 19 并发渲染下的优化重点。

```tsx
// ❌ 避免：不必要的重渲染
function Parent() {
  const [count, setCount] = useState(0);
  return (
    <>
      <ExpensiveTable />            {/* 每次 Parent 重渲染都重新渲染 */}
      <button onClick={() => setCount(c => c + 1)}>点击</button>
    </>
  );
}

// ✅ 优化：React.memo 包裹（或提升状态）
const ExpensiveTable = React.memo(function ExpensiveTable() {
  return <Table dataSource={data} scroll={{ x: 'max-content' }} />;
});

// ✅ 更优：将频繁变化的状态下沉
function Parent() {
  return (
    <>
      <ExpensiveTable />
      <CounterButton />              {/* 计数状态在独立组件内 */}
    </>
  );
}
```

```tsx
// ❌ 避免：useEffect 冗余派生数据
const [list, setList] = useState([]);
const [filtered, setFiltered] = useState([]);
useEffect(() => {                    // 多余：每次 list 变化触发 setFiltered
  setFiltered(list.filter(x => x.active));
}, [list]);

// ✅ 优化：useMemo 派生
const filtered = useMemo(() => list.filter(x => x.active), [list]);
```

```tsx
// ❌ 避免：Context 滥用（Provider 值变化导致所有消费组件重渲染）
<AppContext.Provider value={{ user, theme, config, preferences, data }}>
  <App />
</AppContext.Provider>

// ✅ 优化：拆分 Context，按职责隔离
<UserContext.Provider value={user}>
  <ThemeContext.Provider value={theme}>
    <ConfigContext.Provider value={config}>
      <App />
    </ConfigContext.Provider>
  </ThemeContext.Provider>
</UserContext.Provider>
```

### 第 3 维 · 资源加载（Loading）

首屏加载策略。

```tsx
// ✅ 路由懒加载（React Router v7 + React.lazy）
import { lazy, Suspense } from 'react';
import { Route } from 'react-router-dom';

const BondList = lazy(() => import('@/views/bond/list'));
const BondDetail = lazy(() => import('@/views/bond/detail'));

export const bondRoutes = (
  <Suspense fallback={<Spin className="page-loading" />}>
    <Route index element={<BondList />} />
    <Route path=":id" element={<BondDetail />} />
  </Suspense>
);
```

```tsx
// ✅ 大体积组件按需加载（非首屏弹窗）
const ExportModal = lazy(() => import('@/modals/export-modal'));
const DataImportDrawer = lazy(() => import('@/modals/data-import-drawer'));

// ✅ ECharts 按需注册（避免全量加载）
import * as echarts from 'echarts/core';
import { BarChart, LineChart } from 'echarts/charts';
import { GridComponent, TooltipComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
echarts.use([BarChart, LineChart, GridComponent, TooltipComponent, CanvasRenderer]);
```

### 第 4 维 · 依赖瘦身（Bundle）

当前项目大依赖多，针对性瘦身策略。

| 依赖 | 体积 | 优化策略 | 预期效果 |
|------|------|----------|----------|
| antd @ant-design/* | ~135M | 确保 `import { Button } from 'antd'` 已按需加载（antd v6 默认支持 ESM tree-shaking） | Vite 构建时自动 tree-shake |
| echarts | ~61M | 按需注册组件替代 `import 'echarts'` 全量导入 | 减少 80%+ echarts 体积 |
| ag-grid-community | ~21M | 仅保留使用的模块，移除 license key 检测代码 | 按需减少 |
| handsontable | ~31M | 仅在有编辑需求的页面懒加载，首页不引入 | 首屏减 31M |
| lodash | ~7M | 使用 `lodash/*` 路径导入或 `es-toolkit` 替代 | 减少 95%+ |
| xlsx | 中等 | 仅在导出页懒加载 | 首屏减 |

```tsx
// ✅ lodash 按需导入（替代默认导入）
import debounce from 'lodash/debounce';        // ✅ 仅导入 debounce 函数
import { debounce } from 'lodash';              // ❌ 全量导入 lodash（~7M）
```

---

## Workflow

### 标准性能优化流程

```
Step 1 ─ 性能测量
          安装并使用 `rollup-plugin-visualizer` 分析构建产物
          运行 `npx vite build` 记录基线：总 JS 体积、各 chunk 大小

Step 2 ─ 首屏分析
          识别最大的 chunk、非首屏依赖、重复打包的模块

Step 3 ─ 制定优化方案
          按优先级排序：构建分割 > 路由懒加载 > 大依赖按需 > 运行时优化

Step 4 ─ 实施优化
          每次只改一个维度，确保可回退、可验证

Step 5 ─ 验证效果
          重新构建 + 对比体积变化 + 功能回归测试
          使用 Chrome DevTools → Lighthouse → 验证 FCP/LCP 提升

Step 6 ─ 交付报告
          基线数据 → 优化措施 → 前后对比 → 后续建议
```

### 优先级矩阵

| 优先级 | 维度 | 操作 | 预期收益 |
|--------|------|------|----------|
| 🔴 P0 | 构建分割 | manualChunks 配置，拆分 vendor chunk | 首屏 JS 减少 30-50% |
| 🔴 P0 | 路由懒加载 | React.lazy + Suspense 包裹非首页模块 | 按需加载，减少首屏 40%+ |
| 🟡 P1 | 大依赖按需 | echarts 按需注册、handsontable 懒加载 | 首屏减 30-90M |
| 🟡 P1 | lodash 按需 | 路径导入替代默认导入 | bundle 减 ~5M |
| 🟡 P1 | React.memo | 对稳定的大列表/表格组件包裹 memo | 减少不必要的重渲染 |
| 🟢 P2 | Context 拆分 | 按职责拆分大型 Context | 减少消费组件重渲染 |
| 🟢 P2 | 图片懒加载 | 非首屏图片添加 loading="lazy" | LCP 提升 |
| 🟢 P2 | 组件代码拆分 | 超大组件拆分为子组件 | 可维护性 + 按需加载 |

---

## Project-specific Optimization Guide

### Vite 构建配置优化

当前 `vite.config.ts` 仅含基础插件和代理——以下是完整优化版本：

```ts
/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    // 构建产物可视化分析
    visualizer({
      filename: 'dist/stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@renderer/pages': path.resolve(__dirname, './src/views'),
      '@renderer': path.resolve(__dirname, './src'),
    },
  },
  build: {
    // 启用 CSS 代码分割
    cssCodeSplit: true,
    // Terser 或 esbuild 压缩
    minify: 'esbuild',
    // 小于 4KB 的资源内联
    assetsInlineLimit: 4096,
    // chunk 大小警告阈值
    chunkSizeWarningLimit: 500,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router', 'react-router-dom'],
          'vendor-antd': ['antd', '@ant-design/icons', '@ant-design/charts'],
          'vendor-echarts': ['echarts', 'echarts-for-react'],
          'vendor-table': ['ag-grid-community', 'ag-grid-react', '@tanstack/react-table'],
          'vendor-utils': ['lodash', 'dayjs', 'axios', 'classnames', 'query-string'],
          'vendor-editor': ['handsontable', '@handsontable/react-wrapper'],
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '^/api/apify/': { target: 'http://localhost:3002', changeOrigin: true },
      '^/api/': { target: 'http://localhost:3001', changeOrigin: true },
    },
  },
});
```

### 路由懒加载清单

项目 views 目录模块多，以下模块建议懒加载（非首页路由）：

```tsx
// ✅ 懒加载：非首页路由模块
const Enterprise = lazy(() => import('@/views/enterprise'));
const Fund = lazy(() => import('@/views/fund'));
const Bond = lazy(() => import('@/views/bond'));
const ETF = lazy(() => import('@/views/etf'));
const Bidding = lazy(() => import('@/views/bidding'));
const Apify = lazy(() => import('@/views/apify'));
const RPA = lazy(() => import('@/views/rpa'));
const MarketStream = lazy(() => import('@/views/market-stream'));

// 🚀 首页/常用模块可同步加载（权衡首屏 vs 即时跳转）
```

### ECharts 按需优化

当前项目依赖 `echarts`（61M）+ `echarts-for-react`，建议全量替换为按需注册。但考虑到 echarts 组件已散落多处，逐步迁移策略：

```ts
// 📁 src/lib/echarts-setup.ts（新建，统一出口）
import * as echarts from 'echarts/core';
import { BarChart, LineChart, PieChart, ScatterChart, CandlestickChart } from 'echarts/charts';
import {
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  DataZoomComponent, ToolboxComponent, MarkLineComponent,
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  BarChart, LineChart, PieChart, ScatterChart, CandlestickChart,
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  DataZoomComponent, ToolboxComponent, MarkLineComponent,
  CanvasRenderer,
]);

export default echarts;
```

### 大数据表格优化

项目使用了 ag-grid、@tanstack/react-table、@visactor/react-vtable，大数据场景的关注点：

```tsx
// ✅ AG-Grid 虚拟滚动配置
<AgGridReact
  rowData={data}
  columnDefs={columns}
  // 虚拟滚动必开
  rowBuffer={10}
  maxConcurrentDatasourceRequests={2}
  // 按需渲染
  suppressColumnVirtualisation={false}
  // 禁用不必要的动画
  suppressAnimationFrame={true}
/>

// ✅ @tanstack/react-table 分页 + 虚拟化（如果数据量大）
const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  initialState: { pagination: { pageSize: 50 } }, // 每页 50 条减少渲染
});
```

---

## Output Format

```markdown
## 优化概览
本次优化覆盖维度：构建分割 / 路由懒加载 / 依赖瘦身 / 运行时优化

## 基线数据
- 构建总 JS 体积：XX MB（gzip XX MB）
- 最大 chunk：vendor.js XX MB
- FCP：X.Xs，LCP：X.Xs（Lighthouse）

## 优化措施

### 🔴 P0 - 构建分割
- 操作：配置 rollupOptions.output.manualChunks，拆分 6 个 vendor chunk
- 变更：frontend/vite.config.ts
- 效果：首屏 JS 从 XX MB → XX MB（-XX%）

### 🟡 P1 - 路由懒加载
- 操作：8 个非首页路由模块改为 React.lazy + Suspense
- 变更：各模块 router-config.ts
- 效果：首屏请求数从 XX → XX

### 🟢 P2 - lodash 按需导入
- 操作：全局替换 import { debounce } from 'lodash' → import debounce from 'lodash/debounce'
- 变更：X 个文件
- 效果：bundle 减少 XX KB

## 优化后数据
- 构建总 JS 体积：XX MB（gzip XX MB）
- FCP：X.Xs，LCP：X.Xs（Lighthouse）

## 后续建议
1. [P1] echarts 按需注册改造（预计减 50M）
2. [P2] handsontable 懒加载（首屏减 31M）
3. [P2] Context 拆分治理
```

---

## Validation Checklist

```markdown
- [ ] 构建产物可视化分析完成（rollup-plugin-visualizer 报告）
- [ ] 首屏 JS 体积较基线减少至少 30%
- [ ] manualChunks 配置已生效（vendor 合理拆分）
- [ ] 路由懒加载的页面正常渲染（Suspense fallback 可见）
- [ ] 功能回归：懒加载页面无报错、交互正常
- [ ] 功能回归：按需导入的库（echarts/lodash）正常使用
- [ ] 无重复打包的模块（检查 build 报告中的 duplicate 警告）
- [ ] 开发模式 `npm run dev` 正常启动
- [ ] 生产构建 `npm run build` 无报错
```

---

## Constraints（强制红线）

### 构建约束
- 不引入 Webpack/Rollup 原生配置覆盖 Vite 默认行为，优先使用 Vite 配置接口
- 不删除或停用现有 Vite 插件
- manualChunks 分组以项目实际模块为参考，不随意分组

### 运行时约束
- 不盲目添加 React.memo（仅对确实因 Props 引用变化而重渲染的组件使用）
- 不将同步加载改为懒加载后导致弹窗/侧边栏触发时延迟感明显
- 不删除现有 `useMemo`/`useCallback` 缓存（除非验证过无收益）

### 安全约束
- 优化不涉及敏感信息处理方式的改变
- 不引入未审计的第三方性能插件

### 测量约束
- 所有优化必须有前后对比数据才可交付
- 不使用非标准工具测量（统一使用 `rollup-plugin-visualizer` + Chrome Lighthouse）

---

## Quick Reference

### 常用命令

```bash
# 构建产物分析
npx vite build
# 查看 dist/stats.html 可视化分析结果

# Lighthouse CLI 性能评估
npx lighthouse http://localhost:5173 --view --preset=desktop

# 单次快速构建
npx vite build --mode production

# esbuild 分析（构建日志）
VITE_CJS_TRACE=true npx vite build
```

### 关键依赖体积速查

| 包名 | node_modules 体积 | 优化建议 |
|------|-------------------|----------|
| antd | ~59M | 无需额外处理，antd v6 默认 tree-shake |
| echarts | ~61M | **按需注册**（最高收益项） |
| @ant-design/* | ~76M | 按需使用图标 `import { Icon } from '@ant-design/icons'` |
| ag-grid-community | ~21M | 按需模块导入 |
| handsontable | ~31M | **懒加载** |
| lodash | ~7M | **按路径导入** |
| xlsx | ~3M | **懒加载**（仅在导出页使用） |
