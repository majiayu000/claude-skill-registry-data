---
name: localize
description: "本地化扫描、提取与验证，扫描源码中的硬编码字符串，提取到 i18n 资源文件，验证完整性并生成本地化检查报告。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[语言代码]"
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
    windsurf: {enabled: true, trigger: /localize}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# localize — 本地化扫描与验证

## 技能目的

对项目源码进行本地化扫描，发现硬编码字符串并提取到 i18n 资源文件中，验证多语言资源的完整性与一致性，生成本地化检查报告，确保项目可支持目标语言。

## 参数说明

- `[语言代码]`：目标语言代码，例如 `zh-CN`、`en-US`、`ja-JP`，用于确定资源文件命名与翻译方向。

## 分阶段工作流

### 阶段 1：加载上下文与确认范围

- **输入**：`[语言代码]` 参数
- **处理**：
  1. 使用 Read 读取 `docs/technical-preferences.md` 确认前端框架与 i18n 方案
  2. 使用 Glob 扫描现有 i18n 资源文件（`locales/`、`i18n/`、`*.json`、`*.yaml`）
  3. 使用 Glob 查找源码目录结构确定扫描范围
  4. 通过 AskUserQuestion 与用户确认扫描目录、排除规则与翻译策略
- **输出**：本地化上下文 + 扫描计划

### 阶段 2：扫描源码中的硬编码字符串

- **输入**：扫描计划
- **处理**：
  1. 使用 Grep 在源码中搜索常见的硬编码字符串模式（中文文本、英文 UI 文本、模板字符串中的字面量）
  2. 排除注释、测试数据与配置文件中的非 UI 字符串
  3. 使用 Read 抽样验证匹配结果的相关性
  4. 使用 Bash 执行 i18n 检测工具（如 i18next-parser）辅助扫描
- **输出**：硬编码字符串清单

### 阶段 3：提取到 i18n 资源文件

- **输入**：硬编码字符串清单
- **处理**：
  1. 为每个字符串生成命名空间与键名
  2. 使用 Write 创建或更新目标语言资源文件
  3. 将源码中的硬编码字符串替换为 i18n 调用
  4. 保留原文作为翻译参考
- **输出**：i18n 资源文件 + 更新后的源码

### 阶段 4：验证完整性

- **输入**：i18n 资源文件 + 更新后源码
- **处理**：
  1. 使用 Grep 检查是否仍有遗漏的硬编码字符串
  2. 使用 Read 对比各语言资源文件的键集，标记缺失或多余的键
  3. 使用 Bash 执行 i18n 校验脚本检查格式占位符一致性
  4. 验证动态插值变量在各语言中均存在
- **输出**：完整性验证报告

### 阶段 5：生成本地化检查报告

- **输入**：全部阶段产物
- **处理**：
  1. 汇总扫描结果、提取统计与验证问题
  2. 按严重度排序缺失项与不一致项
  3. 通过 AskUserQuestion 确认报告内容与后续行动
  4. 使用 Write 写入报告至 `docs/reports/localize-[语言代码].md`
- **输出**：本地化检查报告

## 协作协议引用

- 遵循 `docs/examples/COLLABORATIVE-DESIGN-PRINCIPLE.md` 用户驱动协作协议
- 提取与替换代码前需向用户展示草稿并获取批准
- 参考 i18n-specialist Agent 的本地化最佳实践
- 使用 Bash 执行检测与校验脚本

## 推荐下一步

本地化完成后，使用 `/content-audit` 验证文档内容与实现的一致性。无障碍相关本地化使用 `/accessibility-requirements` 检查。发布前使用 `/team-qa` 验证多语言功能。