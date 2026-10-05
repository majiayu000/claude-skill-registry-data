---
name: smoke-check
description: "运行关键路径冒烟测试，快速验证系统核心功能可用性并生成通过/失败报告。"
license: MIT
metadata:
  model: sonnet
  argument-hint: ""
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Bash
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /smoke-check}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# smoke-check — 关键路径冒烟测试

## 技能目的

识别系统关键路径并运行冒烟测试套件，在最短时间内验证核心功能可用性，生成通过/失败报告，作为发布前与回归后的快速健康检查。

## 参数说明

本技能无参数。自动识别关键路径并执行冒烟测试。

## 分阶段工作流

### 阶段 1：识别关键路径

- **输入**：项目目录
- **处理**：
  1. 使用 Glob 查找 `docs/srs/` 中的核心用例与主流程描述
  2. 使用 Read 读取 `docs/epics/index.md` 获取核心 Epic
  3. 使用 Grep 搜索标记为 `@critical`、`@smoke`、`@p0` 的测试用例
  4. 使用 Glob 查找 `tests/smoke/` 或 `e2e/smoke/` 目录
  5. 若无现成冒烟套件，根据 SRS 关键路径推导必要用例清单
- **输出**：关键路径与冒烟用例清单

### 阶段 2：运行冒烟测试套件

- **输入**：冒烟用例清单
- **处理**：
  1. 使用 Read 读取测试运行配置（`jest.config`、`playwright.config` 等）
  2. 使用 Bash 执行冒烟测试命令（带 `--grep smoke` 或指定目录）
  3. 设置合理超时（单套件不超过 5 分钟）
  4. 捕获 stdout 与 stderr，记录失败用例堆栈
  5. 若环境未就绪，使用 Bash 检查服务依赖（数据库、缓存）是否可达
- **输出**：原始测试结果

### 阶段 3：收集结果

- **输入**：原始测试结果
- **处理**：
  1. 解析测试报告（JUnit XML、JSON、终端输出）
  2. 统计通过数、失败数、跳过数、耗时
  3. 对失败用例归类：断言失败、超时、环境错误、未实现
  4. 关联失败用例与对应的 SRS 关键路径
- **输出**：结构化结果数据

### 阶段 4：生成通过/失败报告

- **输入**：结构化结果
- **处理**：
  1. 使用 Write 生成报告 `docs/test/smoke-report.md`
  2. 报告包含：执行摘要（通过率）、关键路径覆盖矩阵、失败详情、环境信息
  3. 给出明确结论：SMOKE PASS / SMOKE FAIL
  4. 对 FAIL 情况标注阻塞发布，并指明最小修复范围
- **输出**：冒烟测试报告

## 协作协议引用

- 遵循 `.claude/docs/coding-standards.md` 编码规范
- 冒烟报告写入 `docs/test/` 目录
- 冒烟失败即视为发布阻塞，不得跳过

## 推荐下一步

使用 `/gate-check` 进行阶段门禁评估。使用 `/regression-suite` 补充回归用例。使用 `/launch-checklist` 在发布前执行最终验证。