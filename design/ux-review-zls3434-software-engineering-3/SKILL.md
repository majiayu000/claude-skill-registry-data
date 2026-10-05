---
name: ux-review
description: "验证UX规范的无障碍性与SRS对齐度，检查ARIA、键盘导航、焦点管理与需求覆盖。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[UX规范路径]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /ux-review}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# ux-review — UX 规范审查

## 技能目的

审查指定 UX 规范的无障碍性合规度与 SRS 需求对齐度，检查 ARIA 标注、键盘导航、焦点管理、状态覆盖与需求追溯，输出审查报告。

## 参数说明

- `[UX规范路径]`：待审查的 UX 规范文件路径，例如 `docs/design/ux/login.md`。

## 分阶段工作流

### 阶段 1：读取 UX 规范与关联 SRS

- **输入**：UX 规范路径参数
- **处理**：
  1. 使用 Read 读取 UX 规范文件
  2. 使用 Grep 提取规范中引用的 SRS 需求编号
  3. 使用 Read 读取关联 SRS 的用户故事列表
  4. 使用 Read 读取 `docs/design/design-system-spec.md` 获取组件规范
- **输出**：UX 规范内容 + 关联需求

### 阶段 2：无障碍性检查

- **输入**：UX 规范内容
- **处理**：
  1. 检查是否定义 ARIA 角色与标签
  2. 检查键盘导航路径是否完整（Tab 顺序、快捷键）
  3. 检查焦点管理是否覆盖模态、抽屉等容器
  4. 检查色彩对比度是否达到 WCAG AA 标准
  5. 检查屏幕阅读器兼容性
- **输出**：无障碍性检查清单

### 阶段 3：SRS 对齐度检查

- **输入**：UX 规范 + 关联 SRS
- **处理**：
  1. 逐条验证 SRS 用户故事是否在 UX 规范中有对应界面设计
  2. 检查界面状态是否覆盖所有需求场景
  3. 检查事件流是否满足需求中的业务流程
  4. 标记未覆盖或偏离的需求
- **输出**：SRS 对齐度矩阵

### 阶段 4：设计系统一致性检查

- **输入**：UX 规范 + 设计系统规范
- **处理**：
  1. 验证 UX 规范引用的组件是否在设计系统中定义
  2. 验证使用的令牌是否与设计系统一致
  3. 标记未定义的自定义组件或令牌
- **输出**：设计系统一致性报告

### 阶段 5：输出审查报告

- **输入**：以上所有检查结果
- **处理**：
  1. 汇总无障碍性、SRS 对齐度、设计系统一致性三个维度结论
  2. 使用 Write 生成审查报告
  3. 给出 PASS / CONCERNS / FAIL 结论
- **输出**：UX 审查报告

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 审查规范
- 参考 WCAG 2.1 AA 标准进行无障碍性检查
- 审查报告写入 `docs/design/ux/{界面名}-review.md`

## 推荐下一步

根据审查报告修复问题项。修复后重新运行本技能验证。通过后进入预开发阶段使用 `/create-epics` 创建 Epic。