---
name: ux-design
description: "编写界面UX规范，使用 ux-spec.md 模板定义布局区域、状态、事件流与交互模式。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[界面名]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /ux-design}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# ux-design — UX 规范编写

## 技能目的

为指定界面编写 UX 规范，使用模板引导式定义布局区域、界面状态、事件流与交互模式，确保界面设计有据可依且与 SRS 需求对齐。

## 参数说明

- `[界面名]`：目标界面名称，例如"登录页"、"仪表盘"、"设置面板"。

## 分阶段工作流

### 阶段 1：读取 SRS 并识别界面

- **输入**：界面名参数
- **处理**：
  1. 使用 Read 读取 `docs/product-concept.md` 获取产品上下文
  2. 使用 Glob 扫描 `docs/srs/*.md` 查找引用该界面的 SRS
  3. 使用 Read 读取相关 SRS 的用户故事与界面需求
  4. 使用 Glob 查找 `.claude/docs/templates/ux-spec.md` 模板
- **输出**：界面需求集合 + 模板

### 阶段 2：定义布局区域

- **输入**：界面需求集合
- **处理**：
  1. 通过 AskUserQuestion 与用户讨论界面整体布局
  2. 定义主要区域（导航、内容、侧边栏、页脚等）
  3. 标注各区域的功能职责与响应式断点行为
  4. 定义区域间的层级与视觉权重
- **输出**：布局区域定义

### 阶段 3：定义界面状态

- **输入**：布局区域定义
- **处理**：
  1. 定义每个区域的状态（空状态、加载中、已加载、错误、成功）
  2. 定义界面级状态切换条件
  3. 标注状态切换时的视觉反馈
- **输出**：界面状态矩阵

### 阶段 4：定义事件流

- **输入**：界面状态矩阵
- **处理**：
  1. 为每个用户操作定义事件触发顺序
  2. 标注事件涉及的组件、服务调用、状态变更
  3. 定义异常事件处理流程
  4. 使用 AskUserQuestion 确认关键交互流程
- **输出**：事件流定义

### 阶段 5：定义交互模式

- **输入**：事件流定义
- **处理**：
  1. 定义键盘导航支持
  2. 定义手势/触控交互
  3. 定义无障碍交互模式（ARIA、焦点管理）
  4. 引用设计系统规范中的组件与令牌
- **输出**：交互模式定义

### 阶段 6：写入文件

- **输入**：全部规范内容
- **处理**：
  1. 基于模板填充各章节，向用户展示草稿
  2. 批准后使用 Write 写入 `docs/design/ux/{界面名}.md`
- **输出**：UX 规范文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 设计文档规范
- 参考 `.claude/docs/templates/ux-spec.md` 模板
- 引用 `docs/design/design-system-spec.md` 中的令牌与组件

## 推荐下一步

使用 `/ux-review` 验证 UX 规范的无障碍性与 SRS 对齐度。继续为其他界面编写 UX 规范。完成后进入 `/api-spec` 定义后端 API。