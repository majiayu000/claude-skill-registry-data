---
name: prototype
description: "技术原型验证，验证关键技术点可行性，产出 PROCEEDS 或 PIVOTS 结论。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[技术点]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Bash
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /prototype}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# prototype — 技术原型验证

## 技能目的

对关键技术点进行原型验证，通过实际编码与测试确认技术可行性，产出 PROCEEDS（可继续）或 PIVOTS（需转向）结论，降低项目技术风险。

## 参数说明

- `[技术点]`：待验证的技术点名称，例如"WebSocket实时通信"、"大文件分片上传"。

## 分阶段工作流

### 阶段 1：定义验证目标

- **输入**：技术点参数
- **处理**：
  1. 使用 Read 读取相关 SRS 与 ADR 获取技术需求上下文
  2. 使用 Read 读取 `docs/technical-preferences.md` 获取技术栈
  3. 通过 AskUserQuestion 与用户确认验证目标与成功标准
  4. 定义验证范围与边界
- **输出**：验证目标文档

### 阶段 2：设计原型方案

- **输入**：验证目标
- **处理**：
  1. 设计最小可行原型方案
  2. 列出需要验证的关键假设
  3. 定义测试用例与验收标准
  4. 确定原型技术栈与依赖
- **输出**：原型方案设计

### 阶段 3：实现原型

- **输入**：原型方案
- **处理**：
  1. 使用 Write 创建 `prototypes/{技术点slug}/README.md`
  2. 使用 Write 创建原型代码文件
  3. 使用 Bash 运行安装依赖与构建命令
  4. 使用 Bash 运行原型代码验证功能
- **输出**：原型代码与运行结果

### 阶段 4：评估与结论

- **输入**：原型运行结果
- **处理**：
  1. 对照成功标准评估原型表现
  2. 记录性能数据、兼容性问题、限制条件
  3. 通过 AskUserQuestion 与用户讨论结论
  4. 产出 PROCEEDS（技术可行，可继续）或 PIVOTS（需转向替代方案）结论
- **输出**：评估结论

### 阶段 5：记录结果

- **输入**：评估结论
- **处理**：
  1. 使用 Write 更新 `prototypes/{技术点slug}/README.md` 写入完整报告
  2. 报告包含：验证目标、方案、结果、结论、建议
  3. 如果 PIVOTS，记录替代方案建议
- **输出**：原型验证报告

## 协作协议引用

- 原型代码存放在 `prototypes/` 目录，不污染主代码库
- 验证结论需用户确认
- PROCEEDS 结论可作为后续 ADR 的依据

## 推荐下一步

PROCEEDS 结论的技术点可使用 `/architecture-decision` 创建正式 ADR。全部关键技术验证后使用 `/build-mvp` 构建 MVP。进入开发阶段使用 `/create-epics` 创建 Epic。