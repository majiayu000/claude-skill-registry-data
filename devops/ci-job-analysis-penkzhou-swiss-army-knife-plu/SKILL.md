---
name: ci-job-analysis
description: CI Job 失败分析知识库，包含失败类型分类、置信度评估、技术栈识别和常见错误模式
---

# CI Job 分析知识库

本知识库提供 GitHub Actions Job 失败分析和修复的专业知识。

## 失败类型分类体系

### 1. 测试失败 (test_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| unit_test | 45% | pytest FAILED, jest FAIL, vitest | 是 |
| integration_test | 30% | integration, api test, mock server | 是 |
| snapshot_test | 15% | snapshot, toMatchSnapshot | 是 |
| other_test | 10% | 其他测试框架 | 部分 |

> **注意**：频率数据基于历史统计，总和为 100%。

**常见根因**：

1. **Mock 数据不完整**：测试 mock 缺少新增字段
2. **API 契约变更**：接口返回格式改变
3. **异步时序问题**：await 缺失或时序错误
4. **环境差异**：CI 环境与本地环境不一致

**修复策略**：

```text
1. 定位失败测试和断言
2. 比较期望值 vs 实际值
3. 追踪数据流到源头
4. 更新 mock 或修复断言
5. 验证修复
```

### 2. E2E 失败 (e2e_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| timeout | 35% | Timeout, 30000ms, waiting for | 是 |
| selector | 30% | strict mode, not found, resolved to | 是 |
| assertion | 20% | expect().toHave, toBeVisible | 是 |
| network | 15% | Route handler, net::ERR | 部分 |

**常见根因**：

1. **选择器过时**：UI 变更导致选择器失效
2. **加载时序**：页面加载慢导致超时
3. **网络拦截失效**：API mock 未正确配置
4. **状态污染**：测试之间状态未隔离

**修复策略**：

```text
1. 分析超时/选择器错误的具体位置
2. 检查 UI 是否变更
3. 添加适当的等待策略
4. 更新选择器或断言
```

### 3. 构建失败 (build_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| typescript | 45% | tsc, error TS, compile | 部分 |
| webpack | 20% | webpack, Module not found | 部分 |
| python | 20% | SyntaxError, ModuleNotFound | 部分 |
| other | 15% | build failed, make error | 否 |

**常见根因**：

1. **类型不匹配**：TypeScript 类型错误
2. **缺失依赖**：import 的模块不存在
3. **语法错误**：代码语法问题
4. **配置错误**：构建配置不正确

### 4. Lint 失败 (lint_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| eslint | 50% | eslint, @typescript-eslint | 是 |
| ruff | 25% | ruff, E501, W503 | 是 |
| prettier | 20% | prettier, formatting | 是 |
| other | 5% | mypy, pylint | 部分 |

**快速修复路径**：

```bash
# ESLint
npx eslint --fix {files}

# Ruff
ruff check --fix {files}

# Prettier
npx prettier --write {files}
```

### 5. 类型检查失败 (type_check_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| typescript | 70% | tsc --noEmit, error TS | 部分 |
| mypy | 30% | mypy, type: ignore | 部分 |

**常见错误类型**：

| 错误码 | 描述 | 自动修复 |
|--------|------|----------|
| TS2345 | 参数类型不匹配 | 否 |
| TS2322 | 类型赋值错误 | 否 |
| TS2339 | 属性不存在 | 否 |
| TS7006 | 隐式 any | 是 |

### 6. 依赖失败 (dependency_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| npm | 40% | npm install, ERESOLVE | 否 |
| pip | 35% | pip install, requirement | 否 |
| yarn | 15% | yarn, resolution | 否 |
| other | 10% | pnpm, poetry | 否 |

**常见问题**：

1. 版本冲突
2. 私有包认证失败
3. 网络问题
4. 锁文件过时

**建议**：依赖问题通常需要手动处理，因为涉及版本策略决策。

### 7. 配置失败 (config_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| env | 50% | env, secret, KEY_ERROR | 否 |
| permission | 30% | permission denied, 403 | 否 |
| config_file | 20% | config, settings | 否 |

**不可自动修复原因**：涉及敏感信息和权限配置，需要人工处理。

### 8. 基础设施失败 (infrastructure_failure)

| 子类型 | 频率 | 关键信号 | 可自动修复 |
|--------|------|----------|-----------|
| runner | 40% | runner, self-hosted | 否 |
| resource | 35% | OOM, killed, disk | 否 |
| network | 25% | network, timeout | 否 |

**不可自动修复原因**：涉及 CI 基础设施，需要运维处理。

---

## 置信度评估体系

### 评分因素

| 因素 | 权重 | 描述 |
|------|------|------|
| 信号明确性 | 40% | 错误信号是否清晰明确 |
| 文件定位 | 30% | 是否能定位到具体文件和行号 |
| 模式匹配 | 20% | 是否匹配已知错误模式 |
| 上下文完整 | 10% | 是否有完整的堆栈追踪 |

### 置信度阈值

| 分数 | 级别 | 行为 |
|------|------|------|
| >= 80 | 高 | 自动修复 |
| 60-79 | 中 | 询问用户后修复 |
| 40-59 | 低 | 展示分析，建议手动 |
| < 40 | 极低 | 跳过 |

### 置信度调整规则

**提升条件**：

- 找到高相似度历史案例：+10
- 完整的堆栈追踪：+5
- 明确的代码变更点：+5
- 匹配已知错误模式：+5

**降低条件**：

- 涉及多个不相关文件：-10
- 错误消息模糊：-10
- 无法定位具体原因：-15
- 可能涉及配置/权限：-20

---

## 技术栈识别

### 基于文件路径

```yaml
backend:
  patterns:
    - "**/*.py"
    - "tests/backend/**"
    - "tests/unit/**"
    - "src/api/**"
    - "app/**"
  signals:
    - "pytest"
    - "FastAPI"
    - "Django"
    - "Python"

frontend:
  patterns:
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.ts"
    - "tests/frontend/**"
    - "src/components/**"
  signals:
    - "jest"
    - "vitest"
    - "React"
    - "Vue"

e2e:
  patterns:
    - "e2e/**"
    - "tests/e2e/**"
    - "playwright/**"
    - "cypress/**"
  signals:
    - "playwright"
    - "cypress"
    - "puppeteer"
```

### 混合技术栈处理

当检测到多个技术栈时：

1. 按错误数量确定主要技术栈
2. 次要技术栈作为 `secondary_stack`
3. 优先处理主要技术栈的错误

---

## 常见错误模式库

### pytest 错误模式

```text
# 断言失败
FAILED tests/test_xxx.py::test_name - AssertionError: assert X == Y

# 异常未捕获
FAILED tests/test_xxx.py::test_name - ExceptionType: message

# fixture 错误
ERROR tests/test_xxx.py::test_name - fixture 'xxx' not found

# 导入错误
ERROR tests/test_xxx.py - ModuleNotFoundError: No module named 'xxx'
```

### jest/vitest 错误模式

```text
# 断言失败
FAIL src/xxx.test.ts
  ✕ test name (123ms)
    expect(received).toBe(expected)

# 超时
FAIL src/xxx.test.ts
  ✕ test name (5001ms)
    Timeout - Async callback was not invoked within 5000ms

# 快照失败
FAIL src/xxx.test.ts
  ✕ test name
    expect(received).toMatchSnapshot()
```

### playwright 错误模式

```text
# 超时
Error: locator.click: Timeout 30000ms exceeded.
waiting for locator('selector')

# 选择器问题
Error: locator.click: Error: strict mode violation:
locator('selector') resolved to 2 elements

# 断言失败
Error: expect(locator).toBeVisible()
Locator expected to be visible
```

### TypeScript 错误模式

```text
# 类型不匹配
error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'

# 属性不存在
error TS2339: Property 'xxx' does not exist on type 'Y'

# 隐式 any
error TS7006: Parameter 'xxx' implicitly has an 'any' type
```

---

## 修复工作流映射

| 失败类型 | 修复方式 | 关联工作流 |
|----------|----------|-----------|
| test_failure (backend) | bugfix_workflow | /fix-backend |
| test_failure (frontend) | bugfix_workflow | /fix-frontend |
| e2e_failure | bugfix_workflow | /fix-e2e |
| lint_failure | quick_fix | 直接运行 lint --fix |
| type_check_failure | bugfix_workflow | 对应栈工作流 |
| build_failure | bugfix_workflow | 对应栈工作流 |
| dependency_failure | manual | 无 |
| config_failure | manual | 无 |
| infrastructure_failure | manual | 无 |

---

## 历史案例匹配

### 相似度计算

```python
def calculate_similarity(current, historical):
    score = 0

    # 错误类型匹配 (30%)
    if current.failure_type == historical.failure_type:
        score += 30

    # 文件路径匹配 (25%)
    file_overlap = len(set(current.files) & set(historical.files))
    score += min(25, file_overlap * 5)

    # 错误消息相似 (25%)
    message_similarity = text_similarity(current.error, historical.error)
    score += message_similarity * 25

    # 修复模式相似 (20%)
    if current.suggested_fix_type == historical.fix_type:
        score += 20

    return score
```

### 高价值案例特征

值得记录为历史案例的修复：

1. 置信度 >= 80
2. 修复成功
3. 有明确的根因分析
4. 包含可复用的修复方法
5. 涉及常见错误模式
