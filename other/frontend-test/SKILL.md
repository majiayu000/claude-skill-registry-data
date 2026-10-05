---
name: frontend-test
description: 前端自动化测试 Agent — 为 React 19 + Ant Design v6 + TypeScript 5 前端项目生成 Vitest 单元测试、@testing-library/react 组件测试、Playwright E2E 测试，覆盖核心逻辑与边界场景
user-invocable: true
---

# 前端自动化测试 Agent（frontend-test）

## Overview

本 skill 定义 trade-crawlee 项目前端测试开发的完整规范与实践。你将担任**前端测试工程师**，为业务代码生成可运行、高质量的自动化测试用例，并建立项目测试基础设施。

**推荐测试栈**：Vitest（单元测试）+ @testing-library/react（组件测试）+ Playwright（E2E 测试）  
**测试目录约定**：`__tests__/` 目录紧邻被测文件，测试文件命名 `<name>.test.ts` / `<name>.test.tsx`  
**基准工具链**：Vite 构建、TypeScript 5 strict 模式、React 19、Ant Design v6

---

## Purpose

你负责项目前端自动化测试体系，核心产出：

- 建立项目测试基础设施（配置 Vitest、安装依赖、编写测试脚本）
- 为工具函数、Hooks、API 封装层编写**单元测试**，覆盖正常/异常/边界场景
- 为业务组件和页面编写**组件测试**，验证渲染、交互、状态变化
- 指导下编写关键路径的 **E2E 测试**，验证完整用户流程
- 确保测试用例可独立运行、不依赖外部环境、不产生副作用

---

## Core Philosophy

| 原则 | 说明 |
|------|------|
| **测试先行但不教条** | 核心工具函数和业务逻辑必写测试；简单透传组件视情况而定 |
| **贴近用户** | 组件测试模拟用户操作而非测试实现细节 |
| **不 mock 不该 mock 的** | UI 测试 mock API 但不 mock 渲染；单元测试 mock 外部依赖但不 mock 内部逻辑 |
| **绿色为主** | 测试不依赖外部环境（网络/数据库），可离线运行 |
| **边界优先** | 不仅测试 happy path，更侧重空值、异常、边界条件 |

---

## When to use this skill

**✅ 适用场景**

| 场景 | 说明 |
|------|------|
| 初始化测试环境 | 首次搭建 Vitest + @testing-library/react + Playwright |
| 工具函数测试 | 纯函数、计算器、格式化、数据转换（如 `lib/bond/calculator.ts`） |
| API 封装测试 | `api-client.ts`、模块 `api.ts` 的请求/响应处理 |
| 自定义 Hook 测试 | `useFetch`、`usePaginationState`、`useFilterState` 等 |
| 组件渲染测试 | 页面组件渲染、条件渲染、空数据/错误态 |
| 组件交互测试 | 表单提交、按钮点击、搜索、分页切换 |
| 业务逻辑测试 | 列表分页逻辑、筛选状态同步、表单校验 |
| 回归测试 | Bug 修复后添加对应测试防止复现 |

**❌ 不适用场景**

- 纯配置文件的测试（vite.config.ts、tsconfig.json）
- 第三方组件库的内部测试
- 样式视觉测试（无截图对比需求时）
- 后端 NestJS 测试（使用后端测试方案）

---

## Recommended Test Stack

### 核心依赖

| 包 | 用途 | 安装命令 |
|----|------|----------|
| `vitest` | 测试运行器与断言库 | `npm i -D vitest` |
| `@testing-library/react` | React 组件渲染与查询 | `npm i -D @testing-library/react` |
| `@testing-library/jest-dom` | DOM 状态断言扩展 | `npm i -D @testing-library/jest-dom` |
| `@testing-library/user-event` | 用户交互模拟 | `npm i -D @testing-library/user-event` |
| `jsdom` | 浏览器环境模拟 | `npm i -D jsdom` |
| `msw` | API mock 服务（可选） | `npm i -D msw` |
| `@playwright/test` | E2E 测试（可选） | `npm i -D @playwright/test` |

### Vite 配置集成

```ts
// vite.config.ts 中添加 test 配置
/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test-setup.ts',
    css: false,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.d.ts',
        'src/**/*.test.*',
        'src/**/__tests__/**',
      ],
    },
  },
  // ... 其余配置
});
```

### 测试设置文件

```ts
// src/test-setup.ts
import '@testing-library/jest-dom';
```

### package.json 测试脚本

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "e2e": "npx playwright test",
    "e2e:ui": "npx playwright test --ui"
  }
}
```

---

## Testing Patterns

### 1. 工具函数 / 纯函数测试

项目中最适合写单元测试的代码：无副作用的纯函数。

```ts
// 📁 src/lib/bond/calculator.ts
export function calculateYield(price: number, coupon: number, years: number): number {
  if (price <= 0) throw new Error('价格必须大于 0');
  if (years <= 0) throw new Error('期限必须大于 0');
  return (coupon / price) * (1 / years);
}

// 📁 src/lib/bond/__tests__/calculator.test.ts
import { describe, it, expect } from 'vitest';
import { calculateYield } from '../calculator';

describe('calculateYield', () => {
  // ✅ 正常场景
  it('应正确计算收益率', () => {
    expect(calculateYield(100, 5, 2)).toBeCloseTo(0.025);
    expect(calculateYield(200, 10, 5)).toBeCloseTo(0.01);
  });

  // ❌ 异常场景
  it('价格 <= 0 应抛出异常', () => {
    expect(() => calculateYield(0, 5, 2)).toThrow('价格必须大于 0');
    expect(() => calculateYield(-1, 5, 2)).toThrow('价格必须大于 0');
  });

  it('期限 <= 0 应抛出异常', () => {
    expect(() => calculateYield(100, 5, 0)).toThrow('期限必须大于 0');
  });

  // 🔲 边界场景
  it('小额价格应正常计算', () => {
    const result = calculateYield(0.01, 0.001, 1);
    expect(result).toBeGreaterThan(0);
  });
});
```

### 2. API 请求层测试

对 `api-client.ts` 和模块 `api.ts` 的请求封装做测试。

```ts
// 📁 src/lib/__tests__/api-client.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiClient } from '../api-client';

describe('apiClient', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('应发送 GET 请求并带回 JSON 响应', async () => {
    const mockData = { data: [{ id: 1 }] };
    globalThis.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve(mockData),
    });

    const result = await apiClient('/api/bonds', '');
    expect(result).toEqual(mockData);
    expect(fetch).toHaveBeenCalledWith(
      '/api/bonds',
      expect.objectContaining({
        headers: expect.objectContaining({ 'content-type': 'application/json' }),
      }),
    );
  });

  it('应在网络异常时抛出错误', async () => {
    globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network Error'));
    await expect(apiClient('/api/bonds', '')).rejects.toThrow('Network Error');
  });
});
```

### 3. Hook 测试

自定义 Hooks 使用 `@testing-library/react` 的 `renderHook`。

```ts
// 📁 src/hooks/__tests__/usePaginationState.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { usePaginationState } from '../usePaginationState';

describe('usePaginationState', () => {
  it('应返回初始分页值', () => {
    const { result } = renderHook(() => usePaginationState({ defaultPageSize: 20 }));
    expect(result.current.page).toBe(1);
    expect(result.current.pageSize).toBe(20);
  });

  it('切换页码时应更新 page', () => {
    const { result } = renderHook(() => usePaginationState({ defaultPageSize: 10 }));
    act(() => { result.current.onChange(3); });
    expect(result.current.page).toBe(3);
  });
});
```

### 4. 组件渲染测试

测试组件在不同状态下的渲染输出。

```tsx
// 📁 src/views/bond/__tests__/list.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { App, ConfigProvider } from 'antd';
import BondList from '../list';

// ✅ 包裹 Ant Design App 上下文
function renderWithAntd(ui: React.ReactElement) {
  return render(
    <ConfigProvider>
      <App>{ui}</App>
    </ConfigProvider>,
  );
}

describe('BondList', () => {
  it('应在加载状态时显示 Spin', () => {
    renderWithAntd(<BondList loading />);
    expect(screen.getByRole('status')).toBeInTheDocument(); // antd Spin 角色
  });

  it('应在数据为空时显示 Empty', () => {
    renderWithAntd(<BondList data={[]} />);
    expect(screen.getByText(/暂无数据/)).toBeInTheDocument();
  });

  it('应在错误状态时显示错误提示', () => {
    renderWithAntd(<BondList error="网络错误" />);
    expect(screen.getByText(/网络错误/)).toBeInTheDocument();
  });
});
```

### 5. 组件交互测试

模拟用户操作并验证行为。

```tsx
// 📁 src/views/bond/__tests__/search.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { App, ConfigProvider } from 'antd';
import BondSearch from '../search';

describe('BondSearch', () => {
  it('输入搜索关键词后应触发回调', async () => {
    const user = userEvent.setup();
    const onSearch = vi.fn();

    render(
      <ConfigProvider>
        <App>
          <BondSearch onSearch={onSearch} />
        </App>
      </ConfigProvider>,
    );

    const input = screen.getByPlaceholderText('请输入债券代码');
    await user.type(input, '123456');
    await user.keyboard('{Enter}');

    expect(onSearch).toHaveBeenCalledWith('123456');
  });
});
```

---

## Test Structure Standards

### 目录约定

```
src/
├── lib/
│   ├── bond/
│   │   ├── calculator.ts
│   │   ├── api.ts
│   │   └── __tests__/
│   │       ├── calculator.test.ts    # 工具函数测试
│   │       └── api.test.ts           # API 封装测试
│   ├── api-client.ts
│   └── __tests__/
│       └── api-client.test.ts
├── hooks/
│   ├── useFetch.ts
│   ├── usePaginationState.ts
│   └── __tests__/
│       ├── useFetch.test.ts
│       └── usePaginationState.test.ts
├── views/
│   └── bond/
│       ├── list.tsx
│       ├── search.tsx
│       └── __tests__/
│           ├── list.test.tsx          # 组件渲染测试
│           └── search.test.tsx        # 组件交互测试
└── test-setup.ts                     # 全局测试设置
```

### 命名规范

| 测试对象 | 命名模式 | 示例 |
|----------|----------|------|
| 工具函数 | `<file>.test.ts` | `calculator.test.ts` |
| 组件 | `<file>.test.tsx` | `list.test.tsx` |
| Hook | `<hook>.test.ts` | `useFetch.test.ts` |
| API 层 | `<file>.test.ts` | `api.test.ts` |

### 测试结构（AAA 模式）

```ts
describe('模块/组件名', () => {
  // Arrange（准备）— 初始数据、mock、props
  // Act（执行）— 渲染、触发操作
  // Assert（断言）— 验证结果
  it('应正确执行某功能', () => {
    // Arrange
    const props = { data: [{ id: 1 }] };
    // Act
    render(<Component {...props} />);
    // Assert
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});
```

---

## Workflow

### 标准测试开发流程

```
Step 1 ─ 分析被测代码
          理解代码核心逻辑、输入输出类型、依赖关系、边界条件

Step 2 ─ 确定测试类型
          纯函数 → 单元测试 | 组件 → 渲染/交互测试 | Hook → renderHook

Step 3 ─ 编写测试代码
          按 AAA 模式组织，覆盖：正常场景 + 异常场景 + 边界场景

Step 4 ─ 独立运行验证
          npx vitest run --reporter=verbose 确认全部通过

Step 5 ─ 提交交付
          测试文件路径、覆盖范围、运行结果、未覆盖说明
```

### 覆盖原则

| 覆盖类型 | 要求 | 说明 |
|----------|------|------|
| ✅ 正常场景 | 必测 | 核心功能路径、预期输入输出 |
| ❌ 异常场景 | 必测 | 非法输入、请求失败、空数据 |
| 🔲 边界场景 | 必测 | 空值、极限值、特殊字符、0/1/N 边界 |
| 🔄 交互场景 | 组件必测 | 点击、输入、切换、提交 |

---

## Output Format

```markdown
## 测试文件清单
新增: src/lib/bond/__tests__/calculator.test.ts
新增: src/lib/bond/__tests__/api.test.ts

## 测试覆盖说明

### 正常场景
- calculateYield 正常计算：3 条用例
- apiClient 正常请求：2 条用例

### 异常场景
- calculateYield 价格 < 0 抛出异常：2 条用例
- apiClient 网络异常抛出错误：1 条用例

### 边界场景
- calculateYield 极小值计算：1 条用例
- apiClient 空响应处理：1 条用例

## 运行结果
- `npx vitest run` — PASS  7/7
- 测试覆盖函数：calculator.ts 100%
- 测试覆盖函数：api-client.ts 85%

## 未覆盖场景（后续迭代）
- calculator.ts 大数值精度验证
- api-client.ts Token 过期刷新逻辑
```

---

## Validation Checklist

```markdown
- [ ] 测试可独立运行：npx vitest run 全部通过
- [ ] 覆盖正常场景（happy path）
- [ ] 覆盖异常场景（非法输入、网络错误、空数据）
- [ ] 覆盖边界场景（空值、临界值、特殊字符）
- [ ] 测试不依赖外部环境（网络/数据库/文件系统）
- [ ] 测试不产生永久副作用（不写文件、不修改 DOM 外部）
- [ ] 测试文件命名符合约定（<name>.test.ts / .test.tsx）
- [ ] 测试目录紧邻被测代码（__tests__/ 同级目录）
- [ ] 组件测试包裹了 ConfigProvider + App 上下文
- [ ] 无 console.log / only / skip 残留
```

---

## Constraints（强制红线）

### 测试质量
- 禁止测试写入外部依赖（网络、数据库、文件系统）
- 禁止 mock 被测函数自身逻辑，只 mock 外部依赖（fetch、localStorage）
- 禁止使用 `test.only` / `test.skip` / `describe.skip` 提交（调试临时使用后必须移除）
- 测试代码必须通过 TypeScript 编译检查

### 适配项目规范
- 组件测试必须包裹 `ConfigProvider` + `App` 上下文（antd v6 要求）
- API 测试使用 `globalThis.fetch` mock，不发起真实网络请求
- Hook 测试使用 `renderHook` + `act`，避免直接调用 Hook 函数

### 目录与命名
- 测试文件统一放在 `__tests__/` 目录下，不放在根级 `tests/` 目录
- 避免在测试文件名中添加多余描述（如 `calculator.unit.test.ts` → `calculator.test.ts`）

### 输出约束
- 测试失败时截取完整错误堆栈和失败用例名
- 同一文件内的测试用例描述风格一致（`应...`、`应在...时...`）
