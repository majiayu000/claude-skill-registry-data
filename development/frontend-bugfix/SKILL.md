---
name: frontend-bugfix
description: |
  Use this skill when debugging frontend test failures (React/TypeScript, Vitest, etc.), fixing bugs in React/TypeScript code, or following TDD methodology for frontend bug fixes. This skill provides the complete bugfix workflow knowledge including error classification, confidence scoring, and TDD best practices.
version: 2.1.0
---

# Frontend Bugfix Workflow Skill

本 skill 提供前端测试 bugfix 的完整工作流知识，包括错误分类体系、置信度评分系统和 TDD 最佳实践。

## 错误分类体系

前端测试失败主要分为以下类型（按频率排序）：

### 1. Mock 层次冲突（71%）

**症状**：Mock 不生效，组件行为异常

**识别特征**：

- 同时存在 `vi.mock` 和 `server.use`
- Hook 返回值与预期不符
- API 调用未被拦截

**解决策略**：选择单一 Mock 层

```typescript
// 选项 A：HTTP Mock（推荐用于集成测试）
server.use(
  http.get('/api/data', () => HttpResponse.json({ data: 'test' }))
);

// 选项 B：Hook Mock（用于单元测试）
vi.mock('@/hooks/useData', () => ({
  useData: () => ({ data: 'test', isLoading: false })
}));
```

### 2. TypeScript 类型不匹配（15%）

**症状**：类型错误、Mock 数据不完整

**识别特征**：

- `as any` 或类型断言
- 缺少必需字段
- 类型定义过时

**解决策略**：使用工厂函数

```typescript
const createMockData = (overrides?: Partial<DataType>): DataType => ({
  id: 1,
  name: 'default',
  ...overrides
});
```

### 3. 异步时序问题（8%）

**症状**：测试间歇性失败

**识别特征**：

- 缺少 `await`
- 使用 `getBy` 而非 `findBy`
- setTimeout 后立即断言

**解决策略**：正确等待

```typescript
// Before
render(<Component />);
expect(screen.getByText('Loaded')).toBeInTheDocument();

// After
render(<Component />);
expect(await screen.findByText('Loaded')).toBeInTheDocument();
```

### 4. 组件渲染问题（4%）

**症状**：组件未按预期渲染

**识别特征**：

- 条件渲染不触发
- 状态更新未反映
- Props 传递错误

**解决策略**：验证渲染条件和状态

### 5. Hook 缓存依赖问题（2%）

**症状**：Hook 返回过时数据

**识别特征**：

- `useEffect` 依赖数组不完整
- `useMemo`/`useCallback` 缓存问题
- 闭包陷阱

**解决策略**：检查并修复依赖数组

## 置信度评分系统

### 评分标准（0-100）

| 分数 | 级别 | 行为 |
| ------ | ------ | ------ |
| 80+ | 高 | 自动执行 |
| 60-79 | 中 | 标记验证后继续 |
| 40-59 | 低 | 暂停询问用户 |
| <40 | 不确定 | 停止收集信息 |

### 置信度计算

```text
置信度 = 证据质量(40%) + 模式匹配(30%) + 上下文完整性(20%) + 可复现性(10%)
```

**证据质量**：

- 高：有代码行号、堆栈、可复现
- 中：有错误信息但缺上下文
- 低：仅有模糊描述

**模式匹配**：

- 高：完全匹配已知模式
- 中：部分匹配
- 低：未知错误类型

**上下文完整性**：

- 高：测试代码 + 源代码 + 配置
- 中：只有测试或源代码
- 低：只有错误信息

**可复现性**：

- 高：稳定复现
- 中：偶发
- 低：环境相关

## TDD 流程

### RED Phase（写失败测试）

```typescript
// 1. 明确期望行为
it('should display error when API fails', async () => {
  // 2. 设置失败场景
  server.use(
    http.get('/api/data', () => HttpResponse.error())
  );

  // 3. 渲染组件
  render(<DataComponent />);

  // 4. 断言期望结果
  expect(await screen.findByText('Error loading data')).toBeInTheDocument();
});
```

### GREEN Phase（最小实现）

```typescript
// 只写让测试通过的最小代码
// 不要优化，不要添加额外功能
```

### REFACTOR Phase（重构）

```typescript
// 改善代码结构
// 保持测试通过
// 消除重复
```

## 质量门禁

| 检查项 | 标准 |
| ---------- | ------ |
| 测试通过率 | 100% |
| 代码覆盖率 | >= 90% |
| 新代码覆盖率 | 100% |
| Lint | 无错误 |
| TypeCheck | 无错误 |

## 常用命令

```bash
# 运行前端测试
make test TARGET=frontend

# 运行特定测试
make test TARGET=frontend FILTER=ComponentName

# 覆盖率检查
make test TARGET=frontend MODE=coverage

# 完整 QA
make qa
```

## 相关文档

文档路径由配置指定（`best_practices_dir`），使用以下关键词搜索：

- **测试最佳实践**：关键词 "testing", "best-practices"
- **Mock 策略**：关键词 "mock", "msw", "vi.mock"
- **问题诊断**：关键词 "troubleshooting", "debugging"
- **实现指南**：关键词 "implementation", "guide"
